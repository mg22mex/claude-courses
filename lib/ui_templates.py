"""UI UX Pro Max templates — polished output rendering for the Weatherman AI Portal.

Provides professional report formatting, structured output cards, and
download-optimized document templates for operational AI responses.
"""

from __future__ import annotations

import csv
import io
import textwrap
from datetime import datetime
from typing import Any


# ------------------------------------------------------------------
# Markdown Templates
# ------------------------------------------------------------------

def report_header(title: str, author: str = "Weatherman AI Portal") -> str:
    """Generate a professional report header with metadata."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return (
        "---\n"
        f"# {title}\n"
        f"**Generated:** {now}  \n"
        f"**Source:** {author}  \n"
        "---\n"
    )


def metric_card(label: str, value: str | float, delta: str | None = None, prefix: str = "") -> str:
    """A single KPI metric formatted as a markdown card."""
    val = f"{prefix}{value:,.2f}" if isinstance(value, float) else f"{prefix}{value}"
    lines = [f"### {label}", f"**{val}**"]
    if delta:
        lines.append(f"*vs. {delta}*")
    return "  \n".join(lines) + "\n"


def summary_table(headers: list[str], rows: list[list[str]], caption: str = "") -> str:
    """Render data as a markdown table with optional caption."""
    if not headers or not rows:
        return ""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    sep = "| " + " | ".join("-" * w for w in col_widths) + " |"
    header_line = "| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |"
    body = "\n".join(
        "| " + " | ".join(str(c).ljust(col_widths[i]) if i < len(col_widths) else str(c) for i, c in enumerate(row)) + " |"
        for row in rows
    )
    result = f"{header_line}\n{sep}\n{body}\n"
    if caption:
        result += f"\n*{caption}*\n"
    return result


def anomaly_block(items: list[dict[str, str]], title: str = "Anomalies Detected") -> str:
    """Render anomaly detection results as a flagged block."""
    lines = [f"## ⚠️ {title}", ""]
    for item in items:
        severity = item.get("severity", "medium").upper()
        lines.append(f"### 🔴 {item.get('field', 'Unknown')} — *{severity} Severity*")
        lines.append(f"**Expected:** {item.get('expected', 'N/A')}")
        lines.append(f"**Found:** {item.get('found', 'N/A')}")
        lines.append(f"**Impact:** {item.get('impact', 'N/A')}")
        if item.get("recommendation"):
            lines.append(f"**Recommendation:** {item['recommendation']}")
        lines.append("")
    return "\n".join(lines)


def compliance_section(
    passed: list[str],
    violations: list[dict[str, str]],
    title: str = "Brand Compliance Check",
) -> str:
    """Render brand compliance results: passed items + violation cards."""
    lines = [f"## {title}", ""]
    lines.append(f"### ✅ Passed ({len(passed)})")
    for item in passed:
        lines.append(f"- {item}")
    lines.append("")
    lines.append(f"### ❌ Violations ({len(violations)})")
    for v in violations:
        lines.append(f"- **{v.get('item', 'Unknown')}**: {v.get('issue', 'N/A')}")
        if v.get("guideline"):
            lines.append(f"  - Guideline: {v['guideline']}")
    return "\n".join(lines)


def analysis_section(title: str, body: str, level: int = 2) -> str:
    """Wrap a section of analysis under a heading."""
    return f"{'#' * level} {title}\n\n{body}\n"


def executive_summary(text: str) -> str:
    """Wrap text in an executive summary blockquote."""
    return f"> **Executive Summary**  \n> {textwrap.fill(text, width=80).replace(chr(10), chr(10) + '> ')}\n"


# ------------------------------------------------------------------
# Download Builders
# ------------------------------------------------------------------

def build_csv(data: list[dict[str, Any]], filename: str = "report.csv") -> tuple[str, str, str]:
    """Build CSV content with BOM for Excel compatibility. Returns (content, filename, mime)."""
    if not data:
        return "", filename, "text/csv"
    output = io.StringIO()
    output.write("\ufeff")  # BOM for Excel
    writer = csv.DictWriter(output, fieldnames=list(data[0].keys()))
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue(), filename, "text/csv"


def build_markdown(content: str, title: str = "report", include_meta: bool = True) -> tuple[str, str, str]:
    """Build a complete markdown document. Returns (content, filename, mime)."""
    if include_meta and not content.startswith("---"):
        content = report_header(title) + "\n" + content
    safe_name = title.lower().replace(" ", "-")
    return content, f"{safe_name}.md", "text/markdown"


def build_html_report(content_md: str, title: str = "Weatherman Report") -> tuple[str, str, str]:
    """Wrap markdown content in a styled HTML document for browser viewing / print."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6;
         color: #1a1a2e; }}
  h1 {{ border-bottom: 2px solid #e94560; padding-bottom: 0.5rem; }}
  h2 {{ color: #16213e; margin-top: 2rem; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
  th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; }}
  th {{ background: #16213e; color: white; }}
  blockquote {{ border-left: 4px solid #e94560; margin: 1rem 0; padding: 0.5rem 1rem;
               background: #f8f9fa; }}
  pre {{ background: #1a1a2e; color: #f8f9fa; padding: 1rem; border-radius: 4px; overflow-x: auto; }}
  .meta {{ color: #666; font-size: 0.9rem; margin-bottom: 2rem; }}
</style>
</head>
<body>
  <div class="meta">Generated by Weatherman AI Portal — {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
  <div class="content">{_md_to_simple_html(content_md)}</div>
</body>
</html>"""
    safe_name = title.lower().replace(" ", "-")
    return html, f"{safe_name}.html", "text/html"


def _md_to_simple_html(md: str) -> str:
    """Very basic markdown→HTML conversion for report embedding."""
    import html as html_mod

    lines = md.split("\n")
    out: list[str] = []
    in_table = False
    for line in lines:
        if line.startswith("| "):
            if not in_table:
                out.append("<table>")
                in_table = True
            cells = [f"<td>{html_mod.escape(c.strip())}</td>" for c in line.strip().strip("|").split("|")]
            tag = "th" if "---" in line else "tr"
            out.append(f"  <{tag}>{''.join(cells)}</{tag}>")
        else:
            if in_table:
                out.append("</table>")
                in_table = False
            if line.startswith("# "):
                out.append(f"<h1>{html_mod.escape(line[2:])}</h1>")
            elif line.startswith("## "):
                out.append(f"<h2>{html_mod.escape(line[3:])}</h2>")
            elif line.startswith("### "):
                out.append(f"<h3>{html_mod.escape(line[4:])}</h3>")
            elif line.startswith("> "):
                out.append(f"<blockquote>{html_mod.escape(line[2:])}</blockquote>")
            elif line.startswith("```"):
                out.append("<pre>")
            elif line.strip().startswith("- "):
                out.append(f"<li>{html_mod.escape(line.strip()[2:])}</li>")
            elif line.strip():
                out.append(f"<p>{html_mod.escape(line)}</p>")
            else:
                out.append("")
    if in_table:
        out.append("</table>")
    return "\n".join(out)
