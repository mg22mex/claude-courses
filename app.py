import streamlit as st
import requests
import openai
import os
import io
import json
import subprocess
import re
import base64
import pandas as pd
from collections.abc import Callable
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

# Optional: Dropbox SDK (with refresh-token auth support)
try:
    import dropbox

    _DROPBOX_SDK_AVAILABLE = True
except ImportError:
    _DROPBOX_SDK_AVAILABLE = False

# Optional: Google API client (Gmail + Drive)
try:
    from google.oauth2.credentials import Credentials as _GoogleCreds
    from googleapiclient.discovery import build as _google_build

    _GOOGLE_AVAILABLE = True
except ImportError:
    _GOOGLE_AVAILABLE = False

st.set_page_config(page_title="Weatherman Claude Portal", layout="wide")

# ---------------------------------------------------------------------------
# MCP Client — manages stdio-based JSON-RPC connections to MCP servers
# ---------------------------------------------------------------------------

class MCPClient:
    """Minimal MCP client that launches server subprocesses over stdio."""

    def __init__(self, config_path: str = "mcp_config.json"):
        self.servers: dict[str, dict] = {}
        self.processes: dict[str, subprocess.Popen] = {}
        self._req_id: int = 0
        self._load_config(config_path)

    # ------------------------------------------------------------------
    # Config loading
    # ------------------------------------------------------------------

    def _load_config(self, path: str) -> None:
        try:
            with open(path) as f:
                cfg = json.load(f)
            self.servers = cfg.get("mcp_servers", {})
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            st.warning(f"MCP config not available — MCP tools are disabled. ({exc})")
            self.servers = {}

    # ------------------------------------------------------------------
    # Process lifecycle
    # ------------------------------------------------------------------

    def start_server(self, name: str) -> bool:
        """Launch an MCP server subprocess if not already running."""
        if name in self.processes and self.processes[name].poll() is None:
            return True  # already running

        info = self.servers.get(name)
        if not info or not info.get("enabled", False):
            return False

        try:
            proc = subprocess.Popen(
                info["command"],
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.processes[name] = proc
            # Perform initialisation handshake
            resp = self._send_request(name, "initialize", {"protocolVersion": "2024-11-05"})
            return resp is not None
        except Exception:
            return False

    def stop_server(self, name: str) -> None:
        proc = self.processes.pop(name, None)
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

    def stop_all(self) -> None:
        for name in list(self.processes):
            self.stop_server(name)

    # ------------------------------------------------------------------
    # JSON-RPC primitives
    # ------------------------------------------------------------------

    def _send_request(self, name: str, method: str, params: dict | None = None) -> dict | None:
        proc = self.processes.get(name)
        if not proc or proc.poll() is not None:
            return None

        self._req_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._req_id,
            "method": method,
            "params": params or {},
        }
        try:
            proc.stdin.write(json.dumps(request) + "\n")
            proc.stdin.flush()
            line = proc.stdout.readline()
            if line:
                return json.loads(line)
        except Exception:
            return None
        return None

    # ------------------------------------------------------------------
    # MCP protocol methods
    # ------------------------------------------------------------------

    def list_tools(self, name: str) -> list[dict]:
        resp = self._send_request(name, "tools/list")
        if resp and "result" in resp:
            return resp["result"].get("tools", [])
        return []

    def call_tool(self, name: str, tool_name: str, arguments: dict | None = None) -> dict | None:
        return self._send_request(name, "tools/call", {
            "name": tool_name,
            "arguments": arguments or {},
        })


# ---------------------------------------------------------------------------
# Helpers — detection, export, autosave, graphify
# ---------------------------------------------------------------------------

def detect_table_data(text: str) -> str | None:
    """Detect markdown tables or CSV blocks in text and return raw CSV."""
    # 1) Look for markdown tables (lines containing |---|)
    lines = text.strip().splitlines()
    table_lines: list[str] = []
    in_table = False
    for line in lines:
        if "|" in line and "---" in line:
            in_table = True
            continue
        if in_table:
            if "|" in line:
                table_lines.append(line)
            else:
                break

    if table_lines:
        csv_rows: list[str] = []
        for row in table_lines:
            cells = [c.strip() for c in row.split("|") if c.strip()]
            csv_rows.append(",".join(cells))
        return "\n".join(csv_rows)

    # 2) Look for raw CSV blocks
    csv_match = re.search(
        r"(?:```csv\s*\n|```\s*\n)?([\w\s,]+(?:\n[\w\s,.$%@()/-]+)+)",
        text,
    )
    if csv_match:
        candidate = csv_match.group(1).strip()
        if "," in candidate:
            return candidate

    return None


def build_md_export(messages: list[dict]) -> str:
    """Render the full conversation as a markdown transcript."""
    lines = ["# Weatherman AI Portal — Chat Export", f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    for msg in messages:
        role_label = "**User**" if msg["role"] == "user" else "**Assistant**"
        lines.append(f"---\n### {role_label}\n{msg['content']}\n")
    return "\n".join(lines)


def autosave_chat(messages: list[dict]) -> None:
    """Append a timestamped snapshot of the conversation to the chat_history directory."""
    if not messages:
        return
    history_dir = Path("chat_history")
    history_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = history_dir / f"session_{timestamp}.md"
    md = build_md_export(messages)
    path.write_text(md, encoding="utf-8")


def render_graphify_section() -> None:
    """Check for the Graphify HTML output and render it, or show a fallback banner."""
    with st.expander("🌐 Interactive Workspace Map", expanded=False):
        graph_path = Path("graphify-out/graph.html")
        if graph_path.exists():
            html_data = graph_path.read_text(encoding="utf-8")
            st.html(html_data)
        else:
            st.info(
                "📊 **Repository map not yet generated.**\n\n"
                "A baseline repository audit needs to be triggered to populate the "
                "interactive ecosystem map. This will visualize all training tracks, "
                "presets, data assets, and their relationships in a browsable node graph."
            )


# ---------------------------------------------------------------------------
# Cloud Secrets & Enterprise Data Hooks (Hugging Face Spaces)
# ---------------------------------------------------------------------------

def _secret_get(key: str) -> str | None:
    """Read a deployment secret from env or Streamlit secrets without raising."""
    val = os.environ.get(key)
    if val:
        return val
    try:
        return st.secrets.get(key, "") or None
    except Exception:
        return None


def init_cloud_secrets() -> dict[str, str | None]:
    """Safe-check Hugging Face / cloud environment variables at startup."""
    keys = (
        "MONDAY_API_TOKEN",
        "SLACK_BOT_TOKEN",
        "DROPBOX_REFRESH_TOKEN",
        "DROPBOX_APP_KEY",
        "DROPBOX_APP_SECRET",
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET",
        "GOOGLE_REFRESH_TOKEN",
        "FATHOM_API_KEY",
        "TRIPLEWHALE_API_KEY",
        "SELLERBOARD_DAILY_LINK",
        "SELLERBOARD_PRODUCT_LINK",
    )
    return {key: _secret_get(key) for key in keys}


@st.cache_data(ttl=300, show_spinner=False)
def fetch_sellerboard_data(report_type: str = "daily") -> bytes | None:
    """Fetch live Sellerboard CSV and return raw bytes for stable cache keys."""
    link_key = (
        "SELLERBOARD_DAILY_LINK"
        if report_type == "daily"
        else "SELLERBOARD_PRODUCT_LINK"
    )
    url = _secret_get(link_key)
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        if not resp.text.strip():
            raise ValueError("Empty response body — CSV link may be expired or unauthorized")
        return resp.text.encode("utf-8")
    except Exception as exc:
        status = getattr(resp, "status_code", "N/A") if "resp" in dir() else "N/A"
        print(f"[SELLERBOARD] HTTP {status} — {exc}")
        st.session_state.setdefault("_sellerboard_errors", []).append(str(exc))
        return None


@st.cache_data
def _sellerboard_available() -> list[str]:
    """Check Sellerboard links independently of other enterprise secrets.

    Returns a list of report types ('daily', 'product') for which a live
    CSV link is configured.  Checks os.environ FIRST (visible path for
    HF Spaces), then falls back to st.secrets.  Lightweight — no HTTP.
    """
    types = []
    # explicit os.environ check so the path is obvious in HF Space logs
    daily_url = os.environ.get("SELLERBOARD_DAILY_LINK")
    if not daily_url:
        try:
            daily_url = st.secrets.get("SELLERBOARD_DAILY_LINK", "") or None
        except Exception:
            daily_url = None
    if daily_url:
        types.append("daily")

    product_url = os.environ.get("SELLERBOARD_PRODUCT_LINK")
    if not product_url:
        try:
            product_url = st.secrets.get("SELLERBOARD_PRODUCT_LINK", "") or None
        except Exception:
            product_url = None
    if product_url:
        types.append("product")

    return types


def sellerboard_dataframe(report_type: str = "daily") -> pd.DataFrame | None:
    """Parse cached Sellerboard CSV bytes into a Pandas DataFrame."""
    raw = fetch_sellerboard_data(report_type)
    if raw is None:
        return None
    try:
        return pd.read_csv(io.StringIO(raw.decode("utf-8")))
    except Exception as exc:
        st.session_state.setdefault("_sellerboard_errors", []).append(str(exc))
        return None


# ---------------------------------------------------------------------------
# Sellerboard column mapping for fulfillment-anomaly-detector schema
# ---------------------------------------------------------------------------

SELLERBOARD_FULFILLMENT_COLUMN_MAP: dict[str, str] = {
    # Explicit Sellerboard column → fulfillment-anomaly-detector schema
    "fulfillment_rate": "on_time_pct",
    "return_rate": "return_rate",
    "on_time_delivery": "on_time_delivery",
    # General aliases (section 1.2 of SKILL.md)
    "order": "order_id",
    "fulfillment_id": "order_id",
    "shipment_id": "order_id",
    "warehouse_code": "warehouse",
    "wh": "warehouse",
    "origin_warehouse": "warehouse",
    "carrier_name": "carrier",
    "shipper": "carrier",
    "shipping_provider": "carrier",
    "courier": "carrier",
    "logistics_provider": "carrier",
    "shipped_date": "ship_date",
    "date_shipped": "ship_date",
    "dispatch_date": "ship_date",
    "departure_date": "ship_date",
    "eta": "estimated_delivery",
    "promised_date": "estimated_delivery",
    "expected_delivery": "estimated_delivery",
    "est_delivery": "estimated_delivery",
    "target_date": "estimated_delivery",
    "delivery_date": "actual_delivery",
    "date_delivered": "actual_delivery",
    "received_date": "actual_delivery",
    "proof_of_delivery": "actual_delivery",
}


def normalize_sellerboard_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename Sellerboard CSV columns to fulfillment-anomaly-detector schema.

    Applies the alias mapping from SELLERBOARD_FULFILLMENT_COLUMN_MAP so the
    downstream AI always receives columns matching the expected schema
    (order_id, warehouse, carrier, ship_date, estimated_delivery,
    actual_delivery). Unknown columns are kept as-is.
    """
    renamed = df.rename(columns=SELLERBOARD_FULFILLMENT_COLUMN_MAP)
    matched = set(SELLERBOARD_FULFILLMENT_COLUMN_MAP.keys()) & set(df.columns)
    unmatched = set(df.columns) - set(SELLERBOARD_FULFILLMENT_COLUMN_MAP.keys())
    if matched:
        print(f"[SELLERBOARD] Column mapping: {len(matched)} columns remapped: {sorted(matched)}")
    if unmatched:
        print(f"[SELLERBOARD] Column mapping: {len(unmatched)} columns passed through: {sorted(unmatched)[:10]}")
    return renamed


def build_sellerboard_context(report_type: str = "daily", max_rows: int = 50, normalize_columns: bool = False) -> str:
    """Expose a compact Sellerboard snapshot for model context during analysis.

    Set *normalize_columns=True* to remap CSV column headers to the
    fulfillment-anomaly-detector schema defined in SELLERBOARD_FULFILLMENT_COLUMN_MAP.
    """
    df = sellerboard_dataframe(report_type)
    if df is None or df.empty:
        label = report_type.replace("_", " ").title()
        return (
            f"\n\n---\n### Live Sellerboard {label} Report\n"
            "CRITICAL SYSTEM ERROR: The Live Sellerboard CSV data stream failed to download. "
            "The server returned an empty string or network error. "
            "DO NOT hallucinate metrics. Explicitly tell the user that the data failed to "
            "fetch from the configured URL.\n"
        )
    if normalize_columns:
        df = normalize_sellerboard_columns(df)
    preview = df.head(max_rows).to_csv(index=False)
    label = report_type.replace("_", " ").title()
    return (
        f"\n\n---\n### Live Sellerboard {label} Report\n"
        f"*{len(df)} rows total, showing first {min(max_rows, len(df))}*\n\n"
        f"```csv\n{preview}\n```\n"
    )


def build_sellerboard_system_block(report_types: list[str]) -> str:
    """Return a system-prompt block telling the model live Sellerboard data is auto-injected."""
    types_desc = " and ".join(f"`{t}`" for t in report_types)
    return (
        "\n\n## Live Sellerboard Data (Auto-Injected)\n"
        "For operational roles (Rick, Sunny, Mollie), live Sellerboard CSV data is "
        "automatically fetched and injected into **every user message**. "
        "You do **not** need to call any tool or ask for it. "
        "The data appears below the user's prompt with a "
        "`### Live Sellerboard ... Report` section header. "
        "Read it directly, reference the figures in your analysis, "
        "and answer questions using the live data.\n"
        f"**Reports auto-injected:** {types_desc}."
    )


def sync_to_monday(
    board_id: str = "",
    item_name: str = "",
    column_values: dict | None = None,
) -> dict:
    """Push a row to Monday.com via GraphQL (enterprise hook stub)."""
    token = _secret_get("MONDAY_API_TOKEN")
    if not token:
        msg = "sync_to_monday: MONDAY_API_TOKEN is not configured."
        st.warning(msg)
        return {"ok": False, "error": msg}
    query = """
    mutation ($board_id: ID!, $item_name: String!, $column_values: JSON!) {
      create_item(board_id: $board_id, item_name: $item_name, column_values: $column_values) {
        id
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "board_id": board_id,
            "item_name": item_name,
            "column_values": json.dumps(column_values or {}),
        },
    }
    try:
        st.info(f"📋 Monday.com sync started — board {board_id}, item '{item_name}'")
        resp = requests.post(
            "https://api.monday.com/v2",
            headers={"Authorization": token, "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if "errors" in data:
            err = data["errors"][0].get("message", str(data["errors"]))
            st.error(f"sync_to_monday failed: {err}")
            return {"ok": False, "error": err}
        st.success("✅ Monday.com item created successfully.")
        return {"ok": True, "result": data}
    except Exception as exc:
        st.error(f"sync_to_monday failed: {exc}")
        return {"ok": False, "error": str(exc)}


def post_to_slack(channel: str = "", text: str = "") -> dict:
    """Post a message to Slack (enterprise hook stub)."""
    token = _secret_get("SLACK_BOT_TOKEN")
    if not token:
        msg = "post_to_slack: SLACK_BOT_TOKEN is not configured."
        st.warning(msg)
        return {"ok": False, "error": msg}
    try:
        st.info(f"💬 Slack post started — channel {channel or '#general'}")
        resp = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"channel": channel, "text": text},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            err = data.get("error", "unknown Slack API error")
            st.error(f"post_to_slack failed: {err}")
            return {"ok": False, "error": err}
        st.success("✅ Slack message posted successfully.")
        return {"ok": True, "result": data}
    except Exception as exc:
        st.error(f"post_to_slack failed: {exc}")
        return {"ok": False, "error": str(exc)}


# ---------------------------------------------------------------------------
# Team Slack User ID map — bypasses conversations.list entirely for DMs
# ---------------------------------------------------------------------------
_TEAM_SLACK_IDS: dict[str, str] = {
    # (all keys stored lowercase for case-insensitive matching)
    "sunny": "U066ARLFH4K",
    "sajjad": "U066ARLFH4K",
    "rick": "U4Y0JPMD4",
    "rick reichmuth": "U4Y0JPMD4",
    "diego": "U5206HQ00",
    "diego marquez": "U5206HQ00",
    "allyse": "U08F1V0FPDY",
    "allyse c": "U08F1V0FPDY",
    "stifany": "UQC0FDA2Z",
    "stifany ong": "UQC0FDA2Z",
    "paula": "U04PH54YZ3N",
    "paula bacolod": "U04PH54YZ3N",
    "arqam": "U08E1C77J77",
    "mollie": "U03SW53P95E",
    "mollie cutillo": "U03SW53P95E",
    "marco": "U0AMTGG4XRD",
    "marco gastelum": "U0AMTGG4XRD",
}

# Build a set of known names for quick matching
_TEAM_KNOWN_NAMES: set[str] = set(_TEAM_SLACK_IDS.keys())


def slack_dm_history(contact_name: str, limit: int = 10) -> dict:
    """Fetch DM history with a team member by name — bypasses ``conversations.list`` entirely.

    Looks up *contact_name* (case-insensitive) in the hardcoded team roster,
    resolves the Slack user ID, opens a DM via ``conversations.open``, and
    fetches recent messages with ``conversations.history``.

    Supported names: sunny/sajjad, rick, diego, allyse, stifany, paula,
    arqam, mollie, marco (including full names).
    """
    token = _secret_get("SLACK_BOT_TOKEN")
    if not token:
        return {"ok": False, "error": "SLACK_BOT_TOKEN not configured"}

    key = contact_name.strip().lower()
    user_id = _TEAM_SLACK_IDS.get(key)
    if not user_id:
        return {
            "ok": False,
            "error": f"Unknown team member '{contact_name}'. Known names: {', '.join(sorted(_TEAM_KNOWN_NAMES))}",
        }

    try:
        # Step 1: open DM (create if it doesn't exist yet)
        open_resp = requests.post(
            "https://slack.com/api/conversations.open",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={"users": user_id},
            timeout=15,
        )
        open_data = open_resp.json()
        if not open_data.get("ok"):
            return {"ok": False, "error": f"conversations.open failed: {open_data.get('error', 'unknown')}"}

        dm_channel_id = open_data["channel"]["id"]

        # Step 2: fetch history
        hist_resp = requests.get(
            "https://slack.com/api/conversations.history",
            headers={"Authorization": f"Bearer {token}"},
            params={"channel": dm_channel_id, "limit": limit},
            timeout=15,
        )
        hist_data = hist_resp.json()
        if not hist_data.get("ok"):
            return {"ok": False, "error": f"conversations.history failed: {hist_data.get('error', 'unknown')}"}

        messages = []
        for msg in hist_data.get("messages", []):
            messages.append({
                "ts": msg.get("ts", ""),
                "user": msg.get("user", ""),
                "text": msg.get("text", ""),
            })
        return {
            "ok": True,
            "contact_name": contact_name,
            "user_id": user_id,
            "dm_channel_id": dm_channel_id,
            "messages": messages,
            "count": len(messages),
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def search_slack_messages(channel: str = "", limit: int = 10) -> dict:
    """Read recent messages from a Slack channel.

    Resolves ``#channel-name`` to a channel ID via ``conversations.list``,
    then fetches history with ``conversations.history``.
    """
    token = _secret_get("SLACK_BOT_TOKEN")
    if not token:
        return {"ok": False, "error": "SLACK_BOT_TOKEN not configured"}
    try:
        channel_id = channel
        if channel.startswith("#"):
            name_wanted = channel.lstrip("#").lower()
            resp = requests.get(
                "https://slack.com/api/conversations.list",
                headers={"Authorization": f"Bearer {token}"},
                params={"types": "public_channel,private_channel", "limit": 200},
                timeout=15,
            )
            data = resp.json()
            if not data.get("ok"):
                return {"ok": False, "error": f"conversations.list failed: {data.get('error', 'unknown')}"}
            for ch in data.get("channels", []):
                if ch.get("name", "").lower() == name_wanted:
                    channel_id = ch["id"]
                    break
            else:
                return {"ok": False, "error": f"Channel '{channel}' not found in workspace"}
        if not channel_id:
            return {"ok": False, "error": "No channel specified — use #channel-name format"}

        resp = requests.get(
            "https://slack.com/api/conversations.history",
            headers={"Authorization": f"Bearer {token}"},
            params={"channel": channel_id, "limit": limit},
            timeout=15,
        )
        data = resp.json()
        if not data.get("ok"):
            return {"ok": False, "error": data.get("error", "unknown Slack error")}

        messages = []
        for msg in data.get("messages", []):
            messages.append({
                "ts": msg.get("ts", ""),
                "user": msg.get("user", ""),
                "text": msg.get("text", ""),
            })
        return {"ok": True, "channel": channel, "channel_id": channel_id, "messages": messages, "count": len(messages)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def get_dropbox_client() -> "dropbox.Dropbox | None":
    """Create a Dropbox SDK client using refresh-token OAuth flow.

    The SDK handles short-lived token refreshes automatically, keeping
    the session alive without manual token-exchange calls.
    """
    if not _DROPBOX_SDK_AVAILABLE:
        return None
    refresh_token = _secret_get("DROPBOX_REFRESH_TOKEN")
    app_key = _secret_get("DROPBOX_APP_KEY")
    app_secret = _secret_get("DROPBOX_APP_SECRET")
    if not refresh_token or not app_key or not app_secret:
        return None
    try:
        return dropbox.Dropbox(
            oauth2_refresh_token=refresh_token,
            app_key=app_key,
            app_secret=app_secret,
        )
    except Exception:
        return None


def read_dropbox_meta(path: str = "") -> dict:
    """Read Dropbox folder metadata using the SDK (enterprise hook stub)."""
    dbx = get_dropbox_client()
    if not dbx:
        msg = "read_dropbox_meta: Dropbox SDK unavailable or refresh token not configured."
        st.warning(msg)
        return {"ok": False, "error": msg}
    try:
        st.info(f"📁 Dropbox metadata read started — path '{path or '/'}'")
        result = dbx.files_list_folder(path=path or "", recursive=False)
        entries = [{"name": e.name, "path": e.path_lower} for e in result.entries]
        st.success(f"✅ Dropbox metadata retrieved — {len(entries)} entries.")
        return {"ok": True, "result": {"entries": entries}}
    except Exception as exc:
        st.error(f"read_dropbox_meta failed: {exc}")
        return {"ok": False, "error": str(exc)}


def get_google_credentials() -> tuple["_GoogleCreds | None", str | None]:
    if not _GOOGLE_AVAILABLE:
        return None, "Google API client libraries are not installed."

    client_id = _secret_get("GOOGLE_CLIENT_ID")
    client_secret = _secret_get("GOOGLE_CLIENT_SECRET")
    refresh_token = _secret_get("GOOGLE_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        return None, "Missing configuration keys."

    try:
        c_id = client_id.strip().strip("'").strip('"')
        c_secret = client_secret.strip().strip("'").strip('"')
        r_token = refresh_token.strip().strip("'").strip('"')

        # Manually verify token via requests
        payload = {
            "client_id": c_id,
            "client_secret": c_secret,
            "refresh_token": r_token,
            "grant_type": "refresh_token"
        }
        res = requests.post("https://oauth2.googleapis.com/token", data=payload, timeout=10)
        data = res.json()

        if res.status_code != 200:
            return None, f"Google OAuth Endpoint rejected credentials: {data.get('error_description', data.get('error', res.text))}"

        access_token = data.get("access_token")

        creds = _GoogleCreds(
            token=access_token,
            refresh_token=r_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=c_id,
            client_secret=c_secret,
            scopes=["https://www.googleapis.com/auth/gmail.modify", "https://www.googleapis.com/auth/drive"]
        )
        return creds, None
    except Exception as exc:
        return None, str(exc)


def test_google_gmail() -> dict:
    """Verify Gmail API connectivity by fetching the profile."""
    creds, error = get_google_credentials()
    if error:
        return {"ok": False, "error": error}
    try:
        service = _google_build("gmail", "v1", credentials=creds)
        profile = service.users().getProfile(userId="me").execute()
        email = profile.get("emailAddress", "unknown")
        return {"ok": True, "email": email}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def test_google_drive() -> dict:
    """Verify Google Drive API connectivity by listing the first file."""
    creds, error = get_google_credentials()
    if error:
        return {"ok": False, "error": error}
    try:
        service = _google_build("drive", "v3", credentials=creds)
        result = service.files().list(pageSize=1).execute()
        files = result.get("files", [])
        return {"ok": True, "file_count": len(files)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def test_fathom_connection() -> dict:
    """Verify Fathom API connectivity via X-Api-Key header."""
    api_key = _secret_get("FATHOM_API_KEY")
    if not api_key:
        return {"ok": False, "error": "FATHOM_API_KEY not configured"}
    try:
        resp = requests.get(
            "https://api.fathom.ai/external/v1/meetings",
            headers={"X-Api-Key": api_key},
            timeout=15,
        )
        resp.raise_for_status()
        return {"ok": True}
    except requests.exceptions.RequestException as e:
        return {"ok": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Tool-callable wrappers — Gmail, Drive, Fathom
# ---------------------------------------------------------------------------


def search_gmail_messages(query: str = "", max_results: int = 5) -> dict:
    """Search Gmail messages and return subject/from/snippet for each match."""
    creds, error = get_google_credentials()
    if error:
        return {"ok": False, "error": error}
    try:
        service = _google_build("gmail", "v1", credentials=creds)
        result = service.users().messages().list(
            userId="me", q=query, maxResults=max_results
        ).execute()
        messages = result.get("messages", [])
        if not messages:
            return {"ok": True, "messages": [], "count": 0}

        details = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId="me", id=msg["id"]
            ).execute()
            headers = {
                h["name"]: h["value"]
                for h in msg_data.get("payload", {}).get("headers", [])
            }
            details.append({
                "id": msg["id"],
                "thread_id": msg_data.get("threadId", ""),
                "subject": headers.get("Subject", ""),
                "from": headers.get("From", ""),
                "date": headers.get("Date", ""),
                "snippet": msg_data.get("snippet", ""),
            })
        return {"ok": True, "messages": details, "count": len(details)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def list_gdrive_files(page_size: int = 10) -> dict:
    """List files from Google Drive with name, type, size, and timestamps."""
    creds, error = get_google_credentials()
    if error:
        return {"ok": False, "error": error}
    try:
        service = _google_build("drive", "v3", credentials=creds)
        result = service.files().list(
            pageSize=page_size,
            fields="files(id, name, mimeType, size, createdTime, modifiedTime)",
        ).execute()
        files = result.get("files", [])
        return {"ok": True, "files": files, "count": len(files)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def read_gdrive_file_content(file_id: str) -> dict:
    """Read a Google Drive file's content by ID (text export for Docs/Sheets, raw text otherwise)."""
    creds, error = get_google_credentials()
    if error:
        return {"ok": False, "error": error}
    try:
        service = _google_build("drive", "v3", credentials=creds)
        meta = service.files().get(
            fileId=file_id, fields="id, name, mimeType"
        ).execute()
        mime = meta.get("mimeType", "")

        if mime == "application/vnd.google-apps.document":
            raw = service.files().export(
                fileId=file_id, mimeType="text/plain"
            ).execute()
        elif mime == "application/vnd.google-apps.spreadsheet":
            raw = service.files().export(
                fileId=file_id, mimeType="text/csv"
            ).execute()
        else:
            raw = service.files().get_media(fileId=file_id).execute()

        text = raw.decode("utf-8") if isinstance(raw, bytes) else str(raw)
        truncated = len(text) > 50000
        return {
            "ok": True,
            "name": meta["name"],
            "mime_type": mime,
            "content": text[:50000],
            "truncated": truncated,
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


class _HTMLToTextParser(HTMLParser):
    """Lightweight HTML-to-text extractor that collects visible text."""

    def __init__(self) -> None:
        super().__init__()
        self._text_parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self._skip = True
        if tag in ("br", "tr", "p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6"):
            self._text_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self._skip = False

    def handle_data(self, data: str) -> None:
        if not self._skip:
            stripped = data.strip()
            if stripped:
                self._text_parts.append(stripped + " ")

    def get_text(self) -> str:
        return "".join(self._text_parts).strip()


def _gmail_decode_body(payload: dict) -> str:
    """Recursively extract plain-text body from a Gmail message payload.

    Falls back to HTML-to-text extraction when no ``text/plain`` part is
    available (e.g. Fathom HTML-only recap emails).
    """
    if payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
        raw = payload["body"]["data"]
        try:
            return base64.urlsafe_b64decode(raw).decode("utf-8", errors="replace")
        except Exception:
            return base64.b64decode(raw).decode("utf-8", errors="replace")

    if payload.get("mimeType") == "text/html" and payload.get("body", {}).get("data"):
        raw = payload["body"]["data"]
        try:
            decoded = base64.urlsafe_b64decode(raw).decode("utf-8", errors="replace")
        except Exception:
            decoded = base64.b64decode(raw).decode("utf-8", errors="replace")
        # Debug: print a snippet of the raw HTML before parsing
        snippet = decoded[:300].replace("\n", " ").strip()
        print(f"[_gmail_decode_body] text/html payload snippet: {snippet}", flush=True)
        parser = _HTMLToTextParser()
        parser.feed(decoded)
        result = parser.get_text()
        return result if result else "(HTML content — text extraction produced no output)"

    if "parts" in payload:
        texts = []
        for part in payload["parts"]:
            chunk = _gmail_decode_body(part)
            if chunk:
                texts.append(chunk)
        return "\n".join(texts)
    return ""


def fetch_fathom_meetings(limit: int = 5, query: str = "") -> dict:
    """Fetch recent meeting records from Fathom API, with automatic Gmail fallback.

    Attempts the Fathom API first. Falls back to Gmail when the API returns
    empty, missing the expected structure, or errors. The Gmail fallback
    searches for Fathom recap emails broadly and extracts Meeting Purpose,
    Key Takeaways, and Topics from the message body.
    """
    # --- Primary route: Fathom API ---
    api_key = _secret_get("FATHOM_API_KEY")
    fathom_error = None
    if api_key:
        try:
            resp = requests.get(
                f"https://api.fathom.ai/external/v1/meetings?limit={limit}",
                headers={"X-Api-Key": api_key},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            # Safely extract meetings list — handle dict, bare list, any shape
            if isinstance(data, dict):
                meetings = data.get("meetings") or []
            elif isinstance(data, list):
                meetings = data
            else:
                meetings = []

            if len(meetings) > 0:
                result: dict = {"ok": True, "source": "fathom_api", "meetings": meetings, "count": len(meetings)}
                if query:
                    ql = query.lower()
                    result["meetings"] = [m for m in meetings if ql in str(m).lower()]
                    result["count"] = len(result["meetings"])
                return result
            fathom_error = "Fathom API returned empty meetings list"
        except Exception as exc:
            fathom_error = str(exc)
    else:
        fathom_error = "FATHOM_API_KEY not configured"

    # --- Automated Gmail fallback ---
    creds, gerror = get_google_credentials()
    if gerror:
        return {"ok": False, "error": f"Fathom unavailable ({fathom_error}); Gmail fallback also failed: {gerror}"}

    try:
        service = _google_build("gmail", "v1", credentials=creds)

        # Broad Fathom-related email search
        gmail_query = "(from:no-reply@fathom.video OR subject:Fathom OR subject:Recap)"
        if query:
            gmail_query += f" {query}"
        list_result = service.users().messages().list(
            userId="me", q=gmail_query, maxResults=limit
        ).execute()

        messages = list_result.get("messages", [])
        if not messages:
            return {"ok": True, "source": "gmail_fallback",
                    "meetings": [], "count": 0,
                    "note": f"No Fathom recap emails found matching query. Fathom API: {fathom_error}"}

        meetings = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId="me", id=msg["id"], format="full"
            ).execute()

            headers = {
                h["name"]: h["value"]
                for h in msg_data.get("payload", {}).get("headers", [])
            }
            body = _gmail_decode_body(msg_data.get("payload", {}))
            # Truncate very long bodies
            truncated = len(body) > 10000
            body = body[:10000]

            meetings.append({
                "id": msg["id"],
                "date": headers.get("Date", ""),
                "subject": headers.get("Subject", ""),
                "from": headers.get("From", ""),
                "body": body,
                "truncated": truncated,
            })

        return {"ok": True, "source": "gmail_fallback",
                "meetings": meetings, "count": len(meetings),
                "note": f"Retrieved from Gmail Fathom recap emails (Fathom API fallback: {fathom_error})"}

    except Exception as exc:
        return {"ok": False, "error": f"Fathom unavailable ({fathom_error}); Gmail fallback failed: {exc}"}


NATIVE_ENTERPRISE_TOOLS: dict[str, Callable[..., dict]] = {
    "sync_to_monday": sync_to_monday,
    "post_to_slack": post_to_slack,
    "search_slack_messages": search_slack_messages,
    "slack_dm_history": slack_dm_history,
    "read_dropbox_meta": read_dropbox_meta,
    "search_gmail_messages": search_gmail_messages,
    "search_gmail": search_gmail_messages,
    "list_gdrive_files": list_gdrive_files,
    "read_gdrive_file_content": read_gdrive_file_content,
    "fetch_fathom_meetings": fetch_fathom_meetings,
}


def execute_native_tool(tool_name: str, arguments: dict | None = None) -> dict:
    """Bridge native Python enterprise hooks into the MCP execution loop."""
    fn = NATIVE_ENTERPRISE_TOOLS.get(tool_name)
    if not fn:
        return {"ok": False, "error": f"Unknown native tool: {tool_name}"}
    return fn(**(arguments or {}))


def build_enterprise_tools_block(cloud_secrets: dict[str, str | None]) -> str:
    """Describe available native enterprise hooks for the system prompt."""
    configured = [k for k, v in cloud_secrets.items() if v]
    if not configured:
        return ""
    tool_lines = (
        "  - `sync_to_monday(board_id, item_name, column_values?)` — Push a row to Monday.com\n"
        "  - `post_to_slack(channel, text)` — Post a message to a Slack channel\n"
        "  - `search_slack_messages(channel, limit?)` — Read recent messages from a Slack channel (use #channel-name format, limit defaults to 10)\n"
        "  - `slack_dm_history(contact_name, limit?)` — Fetch DM history with a team member by name. "
        "Bypasses conversations.list entirely. Supports: sunny/sajjad, rick, diego, allyse, "
        "stifany, paula, arqam, mollie, marco (limit defaults to 10)\n"
        "  - `read_dropbox_meta(path?)` — List entries in a Dropbox folder\n"
        "  - `search_gmail(query, max_results?)` — Search Gmail messages; returns subject/from/date/body for each match\n"
        "  - `list_gdrive_files(page_size?)` — List Google Drive files with metadata\n"
        "  - `read_gdrive_file_content(file_id)` — Read a Drive file's text content by ID\n"
        "  - `fetch_fathom_meetings(limit?, query?)` — Fetch meetings from Fathom API; auto-falls back to Gmail recap search if Fathom returns empty or is unreachable. `query` filters by keyword (e.g. \"Rick\", \"Weekly\")"
    )
    routing_directive = (
        "\n\n## Tool Routing Rules\n"
        "When the user mentions **Slack**, **messages**, **DMs**, **channels**, or asks about "
        "conversations, direct messages, or contact history — use Slack tools only.\n"
        "  - To **read a channel**: use `search_slack_messages`\n"
        "  - To **read DMs with a team member**: use `slack_dm_history`\n"
        "  - To **send a message**: use `post_to_slack`\n"
        "IMPORTANT: `slack_dm_history` bypasses `conversations.list` entirely — it uses a hardcoded "
        "team roster. Do NOT try to resolve team member names via `search_slack_messages` or any "
        "other channel-listing approach. Look up the person directly in `slack_dm_history`.\n"
        "When the user asks about their **email**, **inbox**, or specific Gmail queries — "
        "use `search_gmail`.\n"
        "Choose the tool that matches the user's stated platform. If they say "
        "\"check my Slack\", do NOT check Gmail."
    )
    secret_lines = "\n".join(f"  - {name}" for name in configured)
    return (
        "\n\n## Available Enterprise Data & Integration Hooks\n"
        "To invoke a native integration hook, output a JSON tool call block exactly like this:\n\n"
        "```tool_call\n{\"server\": \"enterprise\", \"tool\": \"TOOL_NAME\", \"arguments\": {...}}\n```\n\n"
        f"**Configured secrets:**\n{secret_lines}\n\n"
        f"**Native tools (call via enterprise server):**\n{tool_lines}"
        f"{routing_directive}"
    )


OPERATIONAL_TRACKS = frozenset({"Rick", "Sunny", "Mollie"})


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------

st.title("⚡ Weatherman AI Portal")
st.caption("Zero-install enterprise workspace backed by DeepSeek & OpenClaude")

# --- Secrets & Configuration ---
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY") or st.secrets.get("DEEPSEEK_API_KEY", "")
GITHUB_RAW_URL = "https://raw.githubusercontent.com/mg22mex/claude-courses/main"
CLOUD_SECRETS = init_cloud_secrets()

# Startup diagnostics — log Sellerboard link detection to HF Space logs
sb_startup = _sellerboard_available()
if sb_startup:
    print(f"[WEATHERMAN] Sellerboard links detected: {', '.join(sb_startup)}")
else:
    print("[WEATHERMAN] WARNING — No Sellerboard links found in os.environ or st.secrets.")

# Initialise MCP client (lazy — servers are started on demand)
mcp_client = MCPClient("mcp_config.json")

# ------------------------------------------------------------------
# Sidebar — Team, Engine, Preset Selection
# ------------------------------------------------------------------

st.sidebar.header("Workspace Settings")

# --- AI Engine Selector (Requirement #1: Dual-Engine Routing) ---
engine_choice = st.sidebar.radio(
    "Select AI Engine",
    ["DeepSeek-R1 (Data/Reasoning)", "DeepSeek-V3 (Creative/Copy/Fast)"],
)

# --- Team Member Selector ---
user = st.sidebar.selectbox(
    "Who is logging in today?",
    ["Select Name", "General / Master Guide", "Rick", "Sunny", "Christine", "Mollie", "Paula & Gabby"],
)

folder_map = {
    "General / Master Guide": "",
    "Rick": "training/rick",
    "Sunny": "training/sunny",
    "Christine": "training/christine",
    "Mollie": "training/mollie",
    "Paula & Gabby": "training/design",
}

preset_map = {
    "General / Master Guide": ["global-onboarding", "portal-flight-manual-lookup", "open-ended-playground"],
    "Rick": ["fulfillment-anomaly-detector", "write-a-prd", "ppt-generation", "architecture-diagram", "open-ended-playground"],
    "Sunny": ["lead-time-anomaly", "customs-tariff-audit", "warehouse-balancing", "xlsx-processing", "data-table-validator", "open-ended-playground"],
    "Mollie": ["csv-analytics", "monte-carlo-analyze-root-cause", "reconciliation-engine", "anomaly-alert-webhook", "open-ended-playground"],
    "Christine": ["brand-guardrails", "email-automation", "listing-verification", "campaign-analytics", "open-ended-playground"],
    "Paula & Gabby": ["svg-auditor", "design-token-validator", "component-spec-compiler", "asset-pack-optimizer", "open-ended-playground"],
}

PRESET_LABELS: dict[str, str] = {
    "open-ended-playground": "Open-Ended Data Playground 🔓",
}

# Block rendering until a user is selected
if user == "Select Name":
    st.warning("Please select your name in the sidebar to activate your custom prompt presets.")
    render_graphify_section()
    st.stop()

dept_path = folder_map[user]

# --- Detect profile switch and clear stale context ---
if st.session_state.get("_active_user") != user:
    if "messages" in st.session_state and st.session_state.messages:
        print(f"[WEATHERMAN] Profile switch: '{st.session_state._active_user}' -> '{user}'. Clearing {len(st.session_state.messages)} stale message(s).")
    st.session_state.messages = []
    st.session_state._active_user = user

# --- Preset Dropdown (with display labels) ---
preset_options = preset_map[user]
preset_display_labels = [PRESET_LABELS.get(p, p) for p in preset_options]
selected_label = st.sidebar.selectbox("Select Workspace Preset Task", preset_display_labels)
selected_preset = preset_options[preset_display_labels.index(selected_label)]

# --- Backend model mapping (Requirement #1: exact API handles) ---
model_to_use = "deepseek-reasoner" if engine_choice == "DeepSeek-R1 (Data/Reasoning)" else "deepseek-chat"

# ------------------------------------------------------------------
# System Prompt Loading
# ------------------------------------------------------------------

with st.spinner("Loading your personalized workspace preset..."):
    try:
        if dept_path == "":
            master_prompt_url = f"{GITHUB_RAW_URL}/SYSTEM_PROMPT.md"
            preset_prompt_url = f"{GITHUB_RAW_URL}/training/general/presets/{selected_preset}/instructions.md"
        else:
            master_prompt_url = f"{GITHUB_RAW_URL}/{dept_path}/presets/SYSTEM_PROMPT.md"
            preset_prompt_url = f"{GITHUB_RAW_URL}/{dept_path}/presets/{selected_preset}/instructions.md"

        master_resp = requests.get(master_prompt_url)
        master_prompt = master_resp.text if master_resp.status_code == 200 else "You are a helpful assistant for Weatherman."

        if selected_preset == "open-ended-playground":
            preset_instructions = (
                "You are in an open-ended sandbox. There are no strict rubrics, "
                "no predefined tasks, and no scoring criteria. The user has full "
                "freedom to explore, build, analyze, or generate whatever they need. "
                "Support them with clean code, actionable insights, and well-structured "
                "output. Use the available enterprise tools and MCP servers when they "
                "add value. If the user is unsure where to start, suggest a few "
                "high-impact directions based on the data and context available."
            )
        else:
            preset_resp = requests.get(preset_prompt_url)
            preset_instructions = preset_resp.text if preset_resp.status_code == 200 else f"Execute operational task: {selected_preset}."

        # Build tool-aware system prompt (Requirement #2: MCP tool descriptions)
        enabled_servers = [k for k, v in mcp_client.servers.items() if v.get("enabled")]
        mcp_block = ""
        if enabled_servers:
            server_lines = "\n".join(
                f"  - **{name}**: {info['description']}"
                for name, info in mcp_client.servers.items()
                if info.get("enabled")
            )
            mcp_block = (
                "\n\n## Available MCP Enterprise Tools\n"
                "You have access to the following enterprise systems. When you need to "
                "interact with one, output a JSON tool call block exactly like this:\n\n"
                "```tool_call\n{\"server\": \"SERVER_NAME\", \"tool\": \"TOOL_NAME\", \"arguments\": {...}}\n```\n\n"
                f"**Enabled servers:**\n{server_lines}"
            )

        # Build core prompt parts individually so a single failure doesn't nuke the entire prompt
        core_parts = [
            master_prompt,
            f"\n\n## Active Task Directives\n{preset_instructions}",
            "\n\n## Current Context\n"
            f"Today's date is **July 13, 2026**. All date-sensitive reasoning, "
            f"queries about \"recent\" messages, and relative-time references should "
            f"use this date as the present. Do not rely on your training cutoff or "
            f"any other date.",
        ]
        if mcp_block:
            core_parts.append(mcp_block)
        try:
            et_block = build_enterprise_tools_block(CLOUD_SECRETS)
            if et_block:
                core_parts.append(et_block)
        except Exception as exc:
            print(f"[WEATHERMAN] Enterprise tools block skipped: {exc}")

        system_prompt = "".join(core_parts)

        # Append Sellerboard-awareness for operational tracks that have live links configured
        # (uses its own secret resolution, decoupled from other enterprise secrets)
        if user in OPERATIONAL_TRACKS:
            sb_types = _sellerboard_available()
            if sb_types:
                system_prompt += build_sellerboard_system_block(sb_types)

    except Exception as exc:
        print(f"[WEATHERMAN] CRITICAL — System prompt construction failed: {exc}")
        system_prompt = "You are a helpful assistant for Weatherman."

st.sidebar.success(f"{user}'s Profile & Preset Loaded!")

# ------------------------------------------------------------------
# File Uploader
# ------------------------------------------------------------------

uploaded_file = st.file_uploader("Attach operational data sheets (.xlsx, .csv, .pdf)", type=["xlsx", "csv", "pdf"])
file_context = ""
if uploaded_file is not None:
    st.info(f"📎 Attached: {uploaded_file.name}")
    file_context = f"\n\n[Attached File Content from {uploaded_file.name}]:\n" + str(uploaded_file.read())

# ------------------------------------------------------------------
# Graphify Section (Requirement #4)
# ------------------------------------------------------------------

render_graphify_section()

# ------------------------------------------------------------------
# Open-Ended Data Playground
# ------------------------------------------------------------------

if selected_preset == "open-ended-playground":
    st.divider()
    st.header("🔓 Open-Ended Data Playground")
    st.caption(
        "No rubrics, no scoring criteria, no fixed tasks — just a live data stream "
        "and a blank canvas. Build dashboards, run ad-hoc analysis, prototype tools, "
        "or explore the dataset however you see fit."
    )

    if user in OPERATIONAL_TRACKS:
        sb_types = _sellerboard_available()
        if "daily" in sb_types or "product" in sb_types:
            playground_df = sellerboard_dataframe("daily")
            if playground_df is not None and not playground_df.empty:

                # ------------------------------------------------------------------
                # 🔧 Enterprise Integration Diagnostics
                # ------------------------------------------------------------------
                with st.expander("🔧 Enterprise Integration Diagnostics", expanded=False):
                    st.caption(
                        "Test connectivity for your configured enterprise integrations. "
                        "Each button performs a lightweight handshake — no data is modified."
                    )

                    # Row 1 — existing services
                    diag_row1 = st.columns(4)

                    with diag_row1[0]:
                        if st.button("Test Monday.com Connection", key="diag_monday"):
                            with st.spinner("Probing Monday.com API..."):
                                token = _secret_get("MONDAY_API_TOKEN")
                                token = token.strip().strip("'").strip('"') if token else None
                                if not token:
                                    st.warning("⚠️  MONDAY_API_TOKEN not configured")
                                else:
                                    try:
                                        resp = requests.post(
                                            "https://api.monday.com/v2",
                                            headers={"Authorization": token, "API-Version": "2023-10"},
                                            json={"query": "query { boards(limit: 1) { id name } }"},
                                            timeout=15,
                                        )
                                        resp.raise_for_status()
                                        st.success("✅ Connected successfully")
                                    except Exception as e:
                                        st.error(f"❌ Connection Failed: {e}")

                    with diag_row1[1]:
                        if st.button("Test Slack Integration", key="diag_slack"):
                            with st.spinner("Probing Slack API..."):
                                token = _secret_get("SLACK_BOT_TOKEN")
                                token = token.strip().strip("'").strip('"') if token else None
                                if not token:
                                    st.warning("⚠️  SLACK_BOT_TOKEN not configured")
                                else:
                                    try:
                                        resp = requests.get(
                                            "https://slack.com/api/auth.test",
                                            headers={"Authorization": f"Bearer {token}"},
                                            timeout=15,
                                        )
                                        data = resp.json()
                                        if resp.status_code == 200 and data.get("ok"):
                                            st.success("✅ Connected successfully")
                                        else:
                                            st.error(f"❌ Connection Failed: {data.get('error', 'Check Token Permissions')}")
                                    except Exception as e:
                                        st.error(f"❌ Connection Failed: {e}")

                    with diag_row1[2]:
                        if st.button("Test Dropbox Access", key="diag_dropbox"):
                            with st.spinner("Probing Dropbox API..."):
                                dbx = get_dropbox_client()
                                if not dbx:
                                    st.warning("⚠️  Dropbox client unavailable — check DROPBOX_REFRESH_TOKEN / SDK install")
                                else:
                                    try:
                                        account = dbx.users_get_current_account()
                                        st.success(f"✅ Connected as {account.name.display_name}")
                                    except Exception as e:
                                        st.error(f"❌ Connection Failed: {e}")

                    with diag_row1[3]:
                        if st.button("Test Triple Whale Link", key="diag_triplewhale"):
                            with st.spinner("Probing Triple Whale API..."):
                                token = _secret_get("TRIPLEWHALE_API_KEY")
                                token = token.strip().strip("'").strip('"') if token else None
                                if not token:
                                    st.warning("⚠️  TRIPLEWHALE_API_KEY not configured")
                                else:
                                    try:
                                        resp = requests.get(
                                            "https://api.triplewhale.com/api/v2/users/api-keys/me",
                                            headers={"x-api-key": token},
                                            timeout=15,
                                        )
                                        if resp.status_code == 200:
                                            st.success("✅ Connected successfully")
                                        elif resp.status_code in (401, 403):
                                            st.error("❌ Connection Failed: Check Token Permissions")
                                        else:
                                            st.error(f"❌ Connection Failed: HTTP {resp.status_code}")
                                    except requests.exceptions.ConnectionError:
                                        st.error("❌ Connection Failed: Cannot reach Triple Whale API")
                                    except Exception as e:
                                        st.error(f"❌ Connection Failed: {e}")

                    # Row 2 — Google (Gmail, Drive) and Fathom
                    diag_row2 = st.columns(4)

                    with diag_row2[0]:
                        if st.button("Test Google Gmail", key="diag_gmail"):
                            with st.spinner("Probing Gmail API..."):
                                result = test_google_gmail()
                                if result.get("ok"):
                                    st.success(f"✅ Gmail connected — {result['email']}")
                                else:
                                    st.error(f"❌ Gmail Failed: {result.get('error', 'unknown')}")

                    with diag_row2[1]:
                        if st.button("Test Google Drive", key="diag_drive"):
                            with st.spinner("Probing Google Drive API..."):
                                result = test_google_drive()
                                if result.get("ok"):
                                    st.success(f"✅ Drive connected — {result['file_count']} files found")
                                else:
                                    st.error(f"❌ Drive Failed: {result.get('error', 'unknown')}")

                    with diag_row2[2]:
                        if st.button("Test Fathom API", key="diag_fathom"):
                            with st.spinner("Probing Fathom API..."):
                                result = test_fathom_connection()
                                if result.get("ok"):
                                    st.success("✅ Fathom connected successfully")
                                else:
                                    st.error(f"❌ Fathom Failed: {result.get('error', 'unknown')}")

                    with diag_row2[3]:
                        # spare slot
                        pass

            else:
                st.info("📡 Live Sellerboard data stream returned empty — upload a file below to get started.")
        else:
            st.info("📡 No Sellerboard links configured. Upload a file below to populate the playground.")
    else:
        st.info("📁 Upload a file below to populate the playground with data.")

    st.divider()

# ------------------------------------------------------------------
# Chat Interface
# ------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_key" not in st.session_state:
    # Track the last message count we autosaved at
    st.session_state.conversation_key = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.last_autosave_count = 0

# Render existing messages with export buttons
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

    # (Requirement #3: Export options below each assistant response)
    if msg["role"] == "assistant":
        col_a, col_b, _ = st.columns([1, 1, 4])
        # Markdown export for this single response
        md_bytes = msg["content"].encode("utf-8")
        col_a.download_button(
            label="📄 Download .md",
            data=md_bytes,
            file_name=f"response_{i}.md",
            mime="text/markdown",
            key=f"dl_md_{i}",
        )
        # CSV export if table data is detected
        csv_data = detect_table_data(msg["content"])
        if csv_data:
            col_b.download_button(
                label="📊 Download .csv",
                data=csv_data.encode("utf-8"),
                file_name=f"table_{i}.csv",
                mime="text/csv",
                key=f"dl_csv_{i}",
            )

# ------------------------------------------------------------------
# Chat Input & Multi-Step MCP Execution Loop (Requirements #1 & #2)
# ------------------------------------------------------------------

if prompt := st.chat_input("Ask a question, run a baseline template, or analyze data..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build payload
    full_user_content = prompt + file_context if file_context else prompt

    # Inject live Sellerboard data for operational analysis tracks
    # (uses its own secret-resolution path — decoupled from other enterprise secrets)
    sb_types = _sellerboard_available() if user in OPERATIONAL_TRACKS else []
    # Enable column normalization for the fulfillment-anomaly-detector to map
    # Sellerboard CSV headers to the detector's expected schema fields.
    normalize_sb = selected_preset == "fulfillment-anomaly-detector"
    sb_ctx_parts = []
    if "daily" in sb_types:
        sb_ctx_parts.append(build_sellerboard_context("daily", normalize_columns=normalize_sb))
    if "product" in sb_types:
        sb_ctx_parts.append(build_sellerboard_context("product", normalize_columns=normalize_sb))
    # Filter out empty results from failed downloads so the elif error branch triggers
    sb_ctx_parts = [p for p in sb_ctx_parts if p]
    if sb_ctx_parts:
        preview = sb_ctx_parts[0][:200]
        print(f"[SELLERBOARD] Injecting {len(sb_ctx_parts)} report(s). Preview: {preview!r}")
        full_user_content += "".join(sb_ctx_parts)
    elif sb_types:
        # Links configured but downloads failed or returned empty — inject error so the model
        # knows data is missing instead of hallucinating local file paths.
        errors = st.session_state.pop("_sellerboard_errors", [])
        if errors:
            print(f"[SELLERBOARD] Download errors: {' | '.join(errors)}")
        err_msg = (
            "\n\n---\n### Live Sellerboard Data\n"
            "System Error: Sellerboard data stream could not be loaded from the environment link.\n"
        )
        print(f"[SELLERBOARD] WARNING — All {len(sb_types)} configured report(s) returned empty/failed. Injecting error marker.")
        full_user_content += err_msg

    # Initialise DeepSeek client (Requirement #1: model routing)
    client = openai.OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com/v1")

    # ---- Multi-step MCP execution loop (Requirement #2) ----
    message_payload = [
        {"role": "system", "content": system_prompt},
        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
    ]
    # Replace the last user message content with the combined version
    message_payload[-1]["content"] = full_user_content

    max_tool_turns = 5
    final_response = ""
    tool_used = False

    # Status log for real-time visibility (Requirement #2: st.status())
    # Log payload structure to HF Space logs for debugging
    sys_role_count = sum(1 for m in message_payload if m["role"] == "system")
    user_role_count = sum(1 for m in message_payload if m["role"] == "user")
    sys_preview = message_payload[0]["content"][:300] if sys_role_count else "[MISSING]"
    print(f"[WEATHERMAN] API payload: {len(message_payload)} messages ({sys_role_count} system, {user_role_count} user). "
          f"System prompt start: {sys_preview!r}")
    if "Sellerboard" in message_payload[0]["content"]:
        print("[WEATHERMAN] Sellerboard awareness block IS in system prompt.")
    if "Live Sellerboard" in message_payload[-1]["content"]:
        idx = message_payload[-1]["content"].find("Live Sellerboard")
        print(f"[WEATHERMAN] Sellerboard data IS in last user message (starts at char {idx}).")

    with st.status("🤖 DeepSeek is processing your request...", expanded=True) as status:
        for turn in range(max_tool_turns):
            stream = client.chat.completions.create(
                model=model_to_use,
                messages=message_payload,
                stream=True,
            )

            collected = ""
            reasoning_collected = ""
            response_placeholder = st.empty()

            for chunk in stream:
                delta = chunk.choices[0].delta
                # R1 model may include reasoning_content before content
                rc = getattr(delta, "reasoning_content", None)
                if rc:
                    reasoning_collected += rc
                    response_placeholder.markdown(
                        f"🧠 *Thinking...*\n\n```\n{reasoning_collected}\n```▌"
                    )
                if delta.content:
                    collected += delta.content
                    response_placeholder.markdown(collected + "▌")

            response_placeholder.markdown(collected)

            # Check for tool calls embedded in the response
            tool_call_match = re.search(
                r"```tool_call\n(\{.*?\})\n```", collected, re.DOTALL
            )

            if not tool_call_match:
                # No more tool calls — this is the final answer
                final_response = collected
                status.update(label="✅ Response complete", state="complete")
                break

            # ---- Execute MCP tool (Requirement #2) ----
            tool_used = True
            tc = json.loads(tool_call_match.group(1))
            server_name = tc.get("server", "")
            tool_name = tc.get("tool", "")
            arguments = tc.get("arguments", {})

            status.update(
                label=f"🔧 Executing MCP tool: {server_name}::{tool_name}",
                state="running",
            )

            # ---- Native enterprise hooks (Monday, Slack, Dropbox) ----
            if server_name == "enterprise":
                result = execute_native_tool(tool_name, arguments)
                clean_text = collected[: tool_call_match.start()].strip()
                tool_result_msg = (
                    f"{clean_text}\n\n"
                    f"[Tool Result — enterprise::{tool_name}]:\n"
                    f"{json.dumps(result, indent=2)}"
                )
                message_payload.append({"role": "user", "content": tool_result_msg})
                status.update(
                    label=f"📋 Enterprise hook {tool_name} finished — feeding back to DeepSeek"
                )
                continue

            # Attempt to start the server if not already running
            if server_name not in mcp_client.processes:
                started = mcp_client.start_server(server_name)
                if not started:
                    status.update(
                        label=f"⚠️ Server '{server_name}' not available — skipping tool call.",
                        state="error",
                    )
                    # Inject a fallback message so the model can still respond
                    tool_result_msg = (
                        f"[Tool {server_name}::{tool_name}] Error: "
                        f"Server '{server_name}' is not enabled or the command is unavailable."
                    )
                else:
                    status.update(label=f"✅ Connected to {server_name}")
            else:
                status.update(label=f"🔄 Calling {server_name}::{tool_name}...")

            if server_name in mcp_client.processes:
                result = mcp_client.call_tool(server_name, tool_name, arguments)
                status.update(
                    label=f"📋 Tool {server_name}::{tool_name} returned — feeding back to DeepSeek"
                )

                # Strip the tool_call block from the collected text so we keep only the
                # model's conversational text
                clean_text = collected[: tool_call_match.start()].strip()
                tool_result_msg = (
                    f"{clean_text}\n\n"
                    f"[Tool Result — {server_name}::{tool_name}]:\n"
                    f"{json.dumps(result, indent=2) if result else 'No result returned.'}"
                )

            # Append the tool result as a user-role message so the model sees it
            message_payload.append({"role": "user", "content": tool_result_msg})
            status.update(label=f"🤖 DeepSeek is processing tool results (turn {turn + 1}/{max_tool_turns})...")

        else:
            # Exhausted max_tool_turns without a final answer
            final_response = collected if collected else "Max tool turns reached. Please rephrase your request."
            status.update(label="⚠️ Max tool turns reached", state="error")

    # If no tool was used the full turn, final_response is already set from the break above.
    # For the tool-used path where we broke out, final_response is also set.
    # Edge case: collected from the last loop iteration
    if not final_response:
        final_response = collected

    # Display the final assistant message
    with st.chat_message("assistant"):
        st.markdown(final_response)

    st.session_state.messages.append({"role": "assistant", "content": final_response})

    # Export buttons for the fresh response (Requirement #3)
    msg_index = len(st.session_state.messages) - 1
    col_a, col_b, _ = st.columns([1, 1, 4])
    md_bytes = final_response.encode("utf-8")
    col_a.download_button(
        label="📄 Download .md",
        data=md_bytes,
        file_name=f"response_{msg_index}.md",
        mime="text/markdown",
        key=f"dl_md_fresh_{msg_index}",
    )
    csv_data = detect_table_data(final_response)
    if csv_data:
        col_b.download_button(
            label="📊 Download .csv",
            data=csv_data.encode("utf-8"),
            file_name=f"table_{msg_index}.csv",
            mime="text/csv",
            key=f"dl_csv_fresh_{msg_index}",
        )

    # ------------------------------------------------------------------
    # Automated long-term storage (Requirement #3: autosave)
    # ------------------------------------------------------------------
    autosave_chat(st.session_state.messages)

