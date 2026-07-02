---
name: svg-auditor
description: Inspect SVG files for structural correctness (viewBox, aspect ratio), brand color compliance (hardcoded vs token variables), accessibility completeness (title, desc), and path/attribute optimization opportunities.
---

# svg-auditor

A strict operational playbook for auditing SVG assets — icons, logos, and illustrations — against brand design system requirements. This skill checks viewBox correctness, hardcoded color compliance with design tokens, accessibility tag presence, path data efficiency, and unnecessary metadata. Run this whenever the Design team needs to validate SVGs before engineering handoff.

---

## 1. Intake & Format Detection

### 1.1 Accept input formats

This skill accepts **one or more** input files:

- **`.svg`** — Standard SVG files (XML format)
- **`.svgz`** — Compressed SVGs (decompress before analysis)

If no files are provided, prompt the designer to supply SVG files.

### 1.2 Classify each SVG

Inspect each SVG's `viewBox` and dimensions, then classify:

| Heuristic | Classification |
|---|---|
| viewBox is `0 0 24 24`, `0 0 32 32`, or `0 0 16 16` | Icon |
| viewBox is non-square (e.g., `0 0 200 50`, `0 0 400 100`) | Logo / wordmark |
| viewBox is large (e.g., `0 0 800 600`) or contains complex `<path>` elements | Illustration |
| No viewBox attribute found | Unclassified — flag as warning |

If the SVG cannot be classified, output a warning and proceed with generic checks.

---

## 2. ViewBox & Canvas Validation

### 2.1 viewBox presence

Check every SVG for a `viewBox` attribute on the root `<svg>` tag:

- **MISSING** — High severity. File will not scale correctly in most renderers.
- **PRESENT** — Continue to validation.

If `viewBox` is missing, suggest adding one based on `width` and `height` attributes if those exist, otherwise prompt the designer for the intended dimensions.

### 2.2 viewBox format validation

For every viewBox found, validate:

| Check | Pass | Fail |
|---|---|---|
| Contains exactly 4 space-separated values | e.g., `0 0 24 24` | Fewer or more than 4 values |
| All four values are integers | e.g., `0 0 24 24` | Any value is a decimal (e.g., `24.5`) |
| Width and height are positive | e.g., Width 24, Height 24 | Zero or negative values |
| Aspect ratio matches file type classification | Icon should be square | Icon with non-square ratio |

Collect all failures into the violation table.

---

## 3. Color & Style Governance

### 3.1 Hardcoded color detection

Scan every element for hardcoded color attributes:

- `fill="..."` — Most common; flag any value that is not `none`, `currentColor`, or a `var(--...)` token reference
- `stroke="..."` — Same rules as fill
- `stop-color="..."` — For gradient stops
- `color="..."` — Rare but check it

### 3.2 Approved palette cross-reference

If the designer provides an approved color palette, cross-reference every hardcoded color:

| Color value | Status |
|---|---|
| Matches a palette color exactly | Allowed (but flag for tokenization) |
| Close to a palette color but different hex | Flag — suggest correction |
| Not in the palette at all | Flag — non-brand color |
| Uses `var(--...)` syntax | Allowed — tokenized correctly |

If no palette is provided, flag all hardcoded colors generically and suggest tokenization.

### 3.3 Inline style blocks

Check for `<style>` tags and `style="..."` attributes:

- If `<style>` contains color declarations, parse and flag those too
- If `style="..."` overrides fill/stroke, flag it (should be a class or attribute)

---

## 4. Accessibility Tag Audit

### 4.1 Title element presence

Check for a `<title>` element as the first child of the root `<svg>`:

- **PRESENT** — Check it contains non-empty text content
- **MISSING** — High severity; screen readers cannot describe the SVG
- **EMPTY** (`<title></title>`) — Medium severity; exists but provides no value

### 4.2 Description element presence

Check for a `<desc>` element:

- **PRESENT** — Check it contains non-empty text content
- **MISSING** — Low severity (informational)
- **EMPTY** — Low severity (exists but empty)

### 4.3 ARIA considerations

- If the SVG is used as an icon (decorative), flag that `role="img"` and `aria-label` should be set on the `<svg>` element
- If the SVG has interactive elements, flag that those should have `role` and `aria-label` attributes

---

## 5. Path Data & Redundancy Scan

### 5.1 Path complexity flagging

Parse all `<path d="..."` attributes and flag:

| Issue | Threshold | Severity |
|---|---|---|
| Overly precise coordinates | More than 2 decimal places (e.g., `M10.123 20.456`) | medium |
| Excessive path commands | More than 50 commands in a single path | medium |
| Unoptimized path segments | Consecutive `M` moves that could be merged | medium |

### 5.2 Empty and redundant elements

Flag the following:

- Empty `<g></g>` groups with no children
- `<defs>` sections with no `<use>` references pointing to them (unused definitions)
- Elements with both `display="none"` and visible children
- Layers with opacity="0" that serve no purpose

### 5.3 Unnecessary attributes

Flag and suggest removal of:

| Attribute | Reason |
|---|---|
| `xml:space="preserve"` | Legacy Inkscape/Adobe export artifact; not needed for web |
| `version="1.1"` | Not required for SVG rendering in browsers |
| `sodipodi:*` attributes | Inkscape editor metadata; should be stripped |
| `inkscape:*` attributes | Inkscape editor metadata; should be stripped |
| Empty `class=""` or `id=""` | Redundant if not used |

---

## 6. Output & Reporting

### 6.1 Terminal summary table

Print a per-file compliance table:

```
=== SVG AUDIT REPORT ===
Files scanned: 3

 File                     | viewBox | Colors  | A11y    | Paths   | Status
──────────────────────────|─────────|─────────|─────────|─────────|──────────
 icon-cloud-sync.svg      | WARN    | FAIL    | FAIL    | PASS    | FAIL
 logo-hero-main.svg       | FAIL    | FAIL    | FAIL    | WARN    | FAIL
 illustration-dashboard.svg| PASS   | WARN    | WARN    | FAIL    | FAIL
──────────────────────────┴─────────┴─────────┴─────────┴─────────┴──────────

Total violations: 14
  viewBox issues:    3
  Color issues:      4
  Accessibility:     4
  Path/formatting:   3

High severity:  6
Medium severity: 5
Low severity:    3
```

### 6.2 CSV export

If the designer requests a report file, write `svg_audit_report.csv` with columns:

```
file,check,status,severity,detail,suggestion
```

### 6.3 Clean SVG export

When fixes are applied, write the corrected SVGs to `fixed-<original-filename>.svg`. Include an XML comment at the top noting the original file name and audit date:

```xml
<!-- Cleaned by svg-auditor on 2026-07-02. Original: icon-cloud-sync.svg -->
```

---

## 7. Strictness Rules

1. **Never modify the original SVG files.** All fixes are written to new files prefixed with `fixed-`.
2. **Always show diffs.** When changing viewBox, colors, or accessibility attributes, show a before/after diff for every change.
3. **Do not remove `<script>` tags without warning.** If an SVG contains JavaScript, flag it and ask the designer before stripping it.
4. **Respect inline CSS when valid.** If a `<style>` block contains brand-compliant CSS, don't flag it — only flag hardcoded presentation attributes.
5. **One file per audit row.** Each SVG gets its own row in the summary table, even if it passes all checks.
6. **Accessibility is non-negotiable.** Missing `<title>` is always high severity regardless of file type.

---

## 8. Edge Cases

| Situation | Response |
|---|---|
| SVG contains embedded raster images (`<image>` or `<img>`) | Flag as warning — embedded raster defeats the purpose of SVG; suggest linking externally |
| SVG is animated (`<animate>`, `<animateTransform>`) | Run all checks except path optimization on animated elements (moving paths are OK to be complex) |
| viewBox is present but width/height are missing | Flag as medium — uses viewBox aspect ratio but has no explicit dimensions |
| SVG uses external references (`<use href="external.svg#icon">`) | Flag as low severity — external references may not render in all contexts |
| File is 0 bytes or unparseable XML | Abort with "ERROR: File [name] is not valid XML or is empty" |
| Color uses named CSS color (e.g., `red`, `blue`, `black`) | Flag as medium — named colors are valid but should be tokenized |
| SVG has a `<style>` tag but no class attributes using it | Flag as low — redundant style declaration |
| Multiple SVGs with identical viewBox and structure | Flag as medium — possible duplicates; recommend reviewing for consolidation |
| `<desc>` contains auto-generated text ("Created with Sketch", "Exported from Figma") | Flag as low — auto-generated descriptions are not meaningful |
| File encoding is not UTF-8 | Attempt to detect encoding and convert; if detection fails, abort with encoding error |
