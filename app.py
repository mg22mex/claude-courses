import streamlit as st
import requests
import openai
import os
import io
import json
import subprocess
import re
import pandas as pd
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

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
        "DROPBOX_ACCESS_TOKEN",
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


def read_dropbox_meta(path: str = "") -> dict:
    """Read Dropbox folder metadata (enterprise hook stub)."""
    token = _secret_get("DROPBOX_ACCESS_TOKEN")
    if not token:
        msg = "read_dropbox_meta: DROPBOX_ACCESS_TOKEN is not configured."
        st.warning(msg)
        return {"ok": False, "error": msg}
    try:
        st.info(f"📁 Dropbox metadata read started — path '{path or '/'}'")
        resp = requests.post(
            "https://api.dropboxapi.com/2/files/list_folder",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={"path": path or "", "recursive": False},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        st.success(f"✅ Dropbox metadata retrieved — {len(data.get('entries', []))} entries.")
        return {"ok": True, "result": data}
    except Exception as exc:
        st.error(f"read_dropbox_meta failed: {exc}")
        return {"ok": False, "error": str(exc)}


NATIVE_ENTERPRISE_TOOLS: dict[str, Callable[..., dict]] = {
    "sync_to_monday": sync_to_monday,
    "post_to_slack": post_to_slack,
    "read_dropbox_meta": read_dropbox_meta,
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
    tool_lines = "\n".join(f"  - `{name}`" for name in NATIVE_ENTERPRISE_TOOLS)
    secret_lines = "\n".join(f"  - {name}" for name in configured)
    return (
        "\n\n## Available Enterprise Data & Integration Hooks\n"
        "To invoke a native integration hook, output a JSON tool call block exactly like this:\n\n"
        "```tool_call\n{\"server\": \"enterprise\", \"tool\": \"TOOL_NAME\", \"arguments\": {...}}\n```\n\n"
        f"**Configured secrets:**\n{secret_lines}\n\n"
        f"**Native tools:**\n{tool_lines}"
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
    st.info(f"📡 Sellerboard links active: {', '.join(sb_startup)}")
else:
    print("[WEATHERMAN] WARNING — No Sellerboard links found in os.environ or st.secrets.")
    st.warning("📡 Sellerboard links not configured — live metrics injection disabled.")

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
        core_parts = [master_prompt, f"\n\n## Active Task Directives\n{preset_instructions}"]
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

    col_metrics = st.columns(3)
    if user in OPERATIONAL_TRACKS:
        sb_types = _sellerboard_available()
        if "daily" in sb_types or "product" in sb_types:
            playground_df = sellerboard_dataframe("daily")
            if playground_df is not None and not playground_df.empty:
                col_metrics[0].metric("Rows Available", len(playground_df))
                col_metrics[1].metric("Columns", len(playground_df.columns))
                numeric_cols = playground_df.select_dtypes(include="number").columns.tolist()
                if numeric_cols:
                    col_metrics[2].metric("Numeric Fields", len(numeric_cols))

                with st.expander("View Raw Live Dataset", expanded=True):
                    st.dataframe(playground_df, use_container_width=True)

                # ------------------------------------------------------------------
                # This layout is intentionally wide open for custom ad-hoc widget
                # injections, Plotly charts, Altair specs, or download hooks.
                # Any Streamlit component can be added below without restructuring
                # the preset architecture. Future AI prompts will receive the full
                # context including this dataframe and the user's chat instructions.
                # ------------------------------------------------------------------

                # ------------------------------------------------------------------
                # 🔧 Enterprise Integration Diagnostics
                # ------------------------------------------------------------------
                with st.expander("🔧 Enterprise Integration Diagnostics", expanded=False):
                    st.caption(
                        "Test connectivity for your configured enterprise integrations. "
                        "Each button performs a lightweight handshake — no data is modified."
                    )

                    diag_cols = st.columns(4)

                    with diag_cols[0]:
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

                    with diag_cols[1]:
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

                    with diag_cols[2]:
                        if st.button("Test Dropbox Access", key="diag_dropbox"):
                            with st.spinner("Probing Dropbox API..."):
                                token = _secret_get("DROPBOX_ACCESS_TOKEN")
                                token = token.strip().strip("'").strip('"') if token else None
                                if not token:
                                    st.warning("⚠️  DROPBOX_ACCESS_TOKEN not configured")
                                else:
                                    try:
                                        resp = requests.post(
                                            "https://api.dropboxapi.com/2/users/get_current_account",
                                            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                                            json=None,
                                            timeout=15,
                                        )
                                        resp.raise_for_status()
                                        st.success("✅ Connected successfully")
                                    except Exception as e:
                                        st.error(f"❌ Connection Failed: {e}")

                    with diag_cols[3]:
                        if st.button("Test Triple Whale Link", key="diag_triplewhale"):
                            with st.spinner("Probing Triple Whale API..."):
                                token = _secret_get("TRIPLEWHALE_API_KEY")
                                token = token.strip().strip("'").strip('"') if token else None
                                if not token:
                                    st.warning("⚠️  TRIPLEWHALE_API_KEY not configured")
                                else:
                                    try:
                                        resp = requests.post(
                                            "https://api.triplewhale.com/api/v2/data-in/products",
                                            headers={"X-TW-API-Key": token, "Content-Type": "application/json"},
                                            json={},
                                            timeout=15,
                                        )
                                        if resp.status_code == 200 or resp.status_code == 400:
                                            st.success("✅ Connected successfully")
                                        elif resp.status_code in (401, 403):
                                            st.error("❌ Connection Failed: Check Token Permissions")
                                        else:
                                            st.error(f"❌ Connection Failed: HTTP {resp.status_code}")
                                    except requests.exceptions.ConnectionError:
                                        st.error("❌ Connection Failed: Cannot reach Triple Whale API")
                                    except Exception as e:
                                        st.error(f"❌ Connection Failed: {e}")

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
