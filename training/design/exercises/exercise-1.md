# Exercise 1 — SVG Structural Auditing

## Scenario

The Design team has received three SVG assets from an external contractor (`icon-cloud-sync.svg`, `logo-hero-main.svg`, and `illustration-dashboard.svg`). Before handing them off to engineering, the team needs to run a strict structural audit: check every viewBox for correctness, flag hardcoded colors that should be design tokens, verify accessibility tags are present, and identify path optimization opportunities. This exercise mirrors a real-world design QA gate.

## Learning Objectives

- Load SVG files into Claude Code and inspect raw XML structure
- Interrogate the design Domain NotebookLM to establish strict asset validation baselines
- Parse SVG elements for viewBox correctness, hardcoded styling, and accessibility completeness
- Flag non-compliant attributes (editor metadata, empty groups, unused defs)
- Generate a structured audit report with pass/fail/warn per check

## Dataset

Use the three SVGs from the `data/mock-assets/` directory.

| File | Description |
|---|---|
| `../data/mock-assets/icon-cloud-sync.svg` | 24×24 icon with non-integer viewBox, missing a11y tags, hardcoded brand color |
| `../data/mock-assets/logo-hero-main.svg` | Logo with missing viewBox, non-brand red, Inkscape metadata, unused defs |
| `../data/mock-assets/illustration-dashboard.svg` | Illustration with empty desc, non-standard hex colors, hardcoded font |

### Known Issues Planted in the Data

| Issue | Location | Notes |
|---|---|---|
| Non-integer viewBox | `icon-cloud-sync.svg` | `viewBox="0 0 24.5 24.5"` — causes sub-pixel rendering |
| Missing viewBox | `logo-hero-main.svg` | No viewBox attribute at all |
| Hardcoded brand color | `icon-cloud-sync.svg` | `#0066cc` instead of `var(--color-primary)` |
| Non-brand color | `logo-hero-main.svg` | `#FF0000` — not in the approved palette |
| Missing title/desc | `icon-cloud-sync.svg` | No `<title>` or `<desc>` elements |
| Empty desc tag | `illustration-dashboard.svg` | `<desc></desc>` present but empty |
| Editor metadata | `logo-hero-main.svg` | `sodipodi:namedview` attribute from Inkscape |
| Redundant attributes | `icon-cloud-sync.svg`, `logo-hero-main.svg` | `xml:space="preserve"` |
| Unused defs | `logo-hero-main.svg` | `#unusedGradient` defined but never referenced |
| Hardcoded fonts | `illustration-dashboard.svg` | `font-family="Arial"` instead of brand token |
| Joke/non-standard hex colors | `illustration-dashboard.svg` | `#C0FFEE`, `#BADA55` — not brand colors |

## Walkthrough

### Step 1 — Load SVGs and run preliminary inspection

```bash
claude ../data/mock-assets/icon-cloud-sync.svg ../data/mock-assets/logo-hero-main.svg ../data/mock-assets/illustration-dashboard.svg
```

Prompt:

```
Load all three SVG files. For each file:
1. Show the raw XML opening <svg> tag (first 10 lines).
2. Report whether a viewBox attribute exists and what its value is.
3. List every element that has a fill, stroke, or stop-color attribute.
4. Check for <title> and <desc> elements — are they present and non-empty?
5. Count the number of <path> elements and total path commands.
6. Flag any sodipodi:, inkscape:, or xml:space attributes.

Output a per-file summary table.
```

### Step 2 — Run the svg-auditor skill

```bash
claude ../data/mock-assets/icon-cloud-sync.svg ../data/mock-assets/logo-hero-main.svg ../data/mock-assets/illustration-dashboard.svg --skill svg-auditor
```

Prompt:

```
Run the svg-auditor skill against all three files.

For each SVG, perform these checks in order:

1. viewBox Validation:
   - Is viewBox present? If missing, flag HIGH severity.
   - Are all 4 values present and space-separated?
   - Are all values integers? Flag decimals.
   - Are width and height positive?

2. Color Governance:
   - Scan for fill, stroke, and stop-color attributes.
   - Flag any hardcoded hex values that are not `none`, `currentColor`,
     or `var(--...)` references.
   - Cross-reference against approved palette:
     #1A6FB0 (brand-primary), #2A9D8F (brand-secondary), #F4A261 (accent)

3. Accessibility:
   - Is `<title>` present and non-empty?
   - Is `<desc>` present and non-empty?
   - Should role="img" be added?

4. Path & Redundancy:
   - Count path commands per <path> element.
   - Flag empty <g></g> groups.
   - Flag unused <defs> sections.
   - Flag sodipodi:*, inkscape:*, xml:space attributes.

Output a compliance table per file with: check, status (pass/fail/warn), severity, detail.
```

### Step 3 — Fix viewBox and structural issues

Prompt (continuing the same session):

```
Fix the structural issues found:

1. logo-hero-main.svg: Add viewBox="0 0 200 60" based on its
   width/height attributes. Explain why this value.

2. icon-cloud-sync.svg: Change viewBox from "0 0 24.5 24.5"
   to "0 0 24 24". Explain why integers matter.

3. Remove xml:space="preserve" from both files where present.

4. Remove sodipodi:namedview from logo-hero-main.svg entirely.

5. Remove the empty #unusedGradient defs section from
   logo-hero-main.svg — nothing references it.

Show a before/after diff for every change.
```

### Step 4 — Replace hardcoded colors with design tokens

Prompt (continuing the session):

```
Replace hardcoded colors with design token variables:

1. icon-cloud-sync.svg: Replace fill="#0066cc" with
   fill="var(--color-primary)".

2. logo-hero-main.svg:
   - Replace fill="#FF0000" with fill="var(--color-secondary)"
   - Replace fill="#666666" with fill="var(--color-text-secondary)"

3. illustration-dashboard.svg:
   - Replace fill="#C0FFEE" with an appropriate brand token
   - Replace fill="#BADA55" with an appropriate brand token
   - Replace fill="#666" with fill="var(--color-text-secondary)"
   - Replace fill="#999" with fill="var(--color-text-disabled)"
   - Replace font-family="Arial" with font-family="var(--typography-font-family-body)"

Output a table: file, old_value, new_token, line_number.
Show a side-by-side diff for the most impactful change per file.
```

### Step 5 — Add accessibility tags

Prompt (continuing the session):

```
Add or fix accessibility elements:

1. icon-cloud-sync.svg: Add as first children of <svg>:
   - <title>Cloud Sync Icon</title>
   - <desc>Two arrows forming a sync loop around a cloud</desc>
   - Add role="img" to the root <svg> element

2. logo-hero-main.svg: Add as first children of <svg>:
   - <title>DataSync Pro Logo</title>
   - <desc>DataSync Pro company wordmark logo</desc>
   - Add role="img" to the root <svg> element

3. illustration-dashboard.svg:
   - <title> already exists — confirm it's non-empty
   - Replace empty <desc></desc> with:
     <desc>Dashboard analytics illustration showing a line chart,
     storage usage bar, and active user metrics</desc>

Show the updated <svg> opening section for each file.
```

### Step 6 — Export the SVG audit report

Prompt (continuing the session):

```
Write svg_audit_report.csv with all issues found and fixes applied.
Columns: file, check, status, severity, detail

Categories:
- viewBox (missing, non-integer, fixed)
- colors (hardcoded, non-brand, tokenized)
- accessibility (title missing, desc empty, role missing, fixed)
- formatting (empty groups, unused defs, editor metadata, fixed)

Then print a terminal summary:

=== SVG AUDIT REPORT ===
Files audited:      3
Total issues:       XX
  viewBox:          X
  Colors:           X
  Accessibility:    X
  Formatting:       X

Fixed:              XX
Remaining:          X
Status:             [PASS / MINOR ISSUES / FAIL]
```

## Expected Output

After completing all steps, you should have:

- A per-file compliance table showing pass/fail/warn for viewBox, colors, accessibility, and formatting
- Corrected viewBox values on all three SVGs
- All hardcoded colors replaced with `var(--...)` design token references
- Accessibility tags (title, desc, role="img") added to every SVG
- Editor metadata and empty groups removed
- A `svg_audit_report.csv` with every issue documented
- Practical experience running the `svg-auditor` skill in a QA gate workflow
