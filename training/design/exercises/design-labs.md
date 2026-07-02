# Design Labs — Advanced SVG & Token Validation Exercises

Three production-grade exercises for the Design team to sharpen their SVG auditing, design token validation, and asset inventory management skills.

---

## Exercise 1: Automated SVG Audit

### Scenario

The Design team has received three SVG assets from an external contractor (`icon-cloud-sync.svg`, `logo-hero-main.svg`, and `illustration-dashboard.svg`). Before handing them off to engineering, the team needs to audit every SVG for structural correctness, brand color compliance, accessibility completeness, and path optimization opportunities.

### Dataset

| File | Description |
|---|---|
| `mock_assets/icon-cloud-sync.svg` | 24×24 cloud sync icon with missing a11y tags, hardcoded brand color, and non-integer viewBox |
| `mock_assets/logo-hero-main.svg` | Company logo SVG with missing viewBox, hardcoded non-brand red, and unused defs |
| `mock_assets/illustration-dashboard.svg` | Dashboard illustration with empty desc tag, overly complex paths, and deprecated font elements |

### Data Challenges Planted

| Challenge | Detail |
|---|---|
| Missing viewBox | `logo-hero-main.svg` has no viewBox attribute — fails silently in some renderers |
| Non-integer viewBox | `icon-cloud-sync.svg` uses `viewBox="0 0 24.5 24.5"` — decimals can cause sub-pixel rendering |
| Hardcoded brand color | `icon-cloud-sync.svg` uses `#0066cc` directly instead of `var(--color-primary)` |
| Non-brand color | `logo-hero-main.svg` uses `#FF0000` (pure red) — not in the approved palette |
| Missing accessibility tags | `icon-cloud-sync.svg` has no `<title>` or `<desc>` elements |
| Empty desc tag | `illustration-dashboard.svg` has `<desc></desc>` — present but empty |
| Editor metadata | `logo-hero-main.svg` contains `sodipodi:namedview` attribute from Inkscape export |
| Unnecessary attributes | Both `icon-cloud-sync.svg` and `logo-hero-main.svg` have `xml:space="preserve"` |
| Unused defs | `logo-hero-main.svg` defines `#unusedGradient` that nothing references |
| Hardcoded fonts | `illustration-dashboard.svg` uses `font-family="Arial"` instead of brand token |
| Non-standard hex colors | `illustration-dashboard.svg` uses `#C0FFEE` and `#BADA55` — joke colors, not brand |

### Walkthrough Steps

```
claude mock_assets/icon-cloud-sync.svg mock_assets/logo-hero-main.svg mock_assets/illustration-dashboard.svg --skill svg-auditor
```

Alternatively, load without the skill:

```
claude mock_assets/icon-cloud-sync.svg mock_assets/logo-hero-main.svg mock_assets/illustration-dashboard.svg
```

**Step 1 — Initial scan:**

```
Step 1 Prompt:
Load all three SVG files and perform an audit:

1. Check viewBox presence for each SVG. Report which files have
   a viewBox, which are missing it, and whether the values are valid.
2. List all hardcoded fill, stroke, and stop-color attributes.
   Flag any that use non-brand colors.
3. Check for accessibility: does each SVG have a <title> and <desc>?
4. Identify any empty groups, unused defs, editor metadata
   (sodipodi:, inkscape:), or xml:space attributes.

Output a table per file.
```

**Step 2 — Fix viewBox and structural issues:**

```
Step 2 Prompt:
Fix the structural issues found:

1. For logo-hero-main.svg: Add a viewBox="0 0 200 60" based on its
   width and height attributes.
2. For icon-cloud-sync.svg: Change viewBox from "0 0 24.5 24.5" to
   "0 0 24 24" (round to integers).
3. Remove xml:space="preserve" from both files.
4. Remove sodipodi:namedview from logo-hero-main.svg.

Show before/after diffs for each change.
```

**Step 3 — Replace hardcoded colors with tokens:**

```
Step 3 Prompt:
Replace hardcoded colors with design tokens:

1. icon-cloud-sync.svg: Replace fill="#0066cc" with
   fill="var(--color-primary)"
2. logo-hero-main.svg: Replace fill="#FF0000" with
   fill="var(--color-secondary)". Replace fill="#666666"
   with fill="var(--color-text-secondary)"
3. illustration-dashboard.svg: Replace fill="#C0FFEE" and
   "#BADA55" with appropriate brand colors. Replace fill="#666"
   and fill="#999" with token variables.

Show a table: file, old_color, new_token, line
Show a diff of the most impactful change per file.
```

**Step 4 — Add accessibility tags:**

```
Step 4 Prompt:
Add accessibility elements to SVGs that are missing them:

1. icon-cloud-sync.svg: Add <title>Cloud Sync Icon</title> and
   <desc>Two arrows forming a sync loop around a cloud</desc>
   as the first children of the root <svg>.
2. logo-hero-main.svg: Add <title>DataSync Pro Logo</title> and
   <desc>DataSync Pro company wordmark logo</desc>.
3. illustration-dashboard.svg: The <title> exists but <desc> is
   empty. Add: <desc>Dashboard analytics illustration showing
   a line chart, storage usage bar, and active user metrics</desc>.

Show the updated <svg> opening section for each file.
```

**Step 5 — Remove unused and redundant elements:**

```
Step 5 Prompt:
Clean up unnecessary elements:

1. icon-cloud-sync.svg: Remove the empty <g></g> group.
2. logo-hero-main.svg: Remove the #unusedGradient defs section.
3. illustration-dashboard.svg: Replace hardcoded font-family="Arial"
   with font-family="var(--font-family-body)". Replace hardcoded
   fill="#666" with fill="var(--color-text-secondary)".

Confirm each removal with a brief explanation of why it's safe.
```

**Step 6 — Export audit report:**

```
Step 6 Prompt:
Write a CSV called svg_audit_report.csv with all issues found
and fixes applied. Columns:

file, check, status, severity, detail

Categories to include:
- viewBox (missing, non-integer, fixed)
- colors (hardcoded, non-brand, tokenized)
- accessibility (title missing, desc empty, fixed)
- formatting (empty groups, unused defs, editor metadata, fixed)

Print a terminal summary:

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

---

## Exercise 2: Design Token Validation

### Scenario

The Design team has two token files — a JSON global token schema (`design-tokens.json`) and a CSS component token file (`component-tokens.css`) — that need to be validated before an engineering handoff. The brand's approved color palette and spacing scale must be enforced, and all token references must resolve correctly.

### Dataset

| File | Description |
|---|---|
| `mock_assets/design-tokens.json` | Global token file with color, spacing, typography, shadow, and component tokens |
| `mock_assets/component-tokens.css` | Component-level CSS custom properties referencing global tokens |

### Approved Brand Palette

```
#1A6FB0 (brand-primary)
#2A9D8F (brand-secondary)
#F4A261 (accent)
#264653 (text-primary)
#E9C46A (highlight)
#FFFFFF (white)
#F5F5F5 (bg-light)
#333333 (text-secondary)
```

### Approved Spacing Scale (px)

`4, 8, 12, 16, 24, 32, 48, 64, 96`

### Data Challenges Planted

| Challenge | Detail |
|---|---|
| Wrong brand primary | `design-tokens.json` has `#1A7DB8` instead of approved `#1A6FB0` |
| Missing from approved palette | `#E85D3A` (brand-secondary) is not in the approved palette at all |
| Inconsistent hex format | `#222` (3-char) instead of `#222222` (6-char) |
| Off-scale spacing | `--spacing-md: 18px` — not on the approved scale (nearest: 16 or 24) |
| Non-brand font | `fontFamily.body: 'Comic Sans MS', serif` — not an approved brand typeface |
| Broken reference | `"card": { "border": "{color.border.default}" }` — token `color.border.default` doesn't exist |
| Missing required tokens | No `--color-semantic-success` token. No `--shadow-card` token. |
| Deprecated naming | `--color-cta-background` and `--color-cta-text` — should use `--color-button-*` |
| Undefined variable reference | `component-tokens.css` uses `var(--color-semantic-warning)` which doesn't exist |
| Hardcoded value instead of token | `--card-shadow: 0 2px 4px rgba(0,0,0,0.1)` should reference a shadow token |
| Missing component token sets | No `--badge-*` or `--nav-*` token families defined |

### Walkthrough Steps

```
claude mock_assets/design-tokens.json mock_assets/component-tokens.css --skill design-token-validator
```

Alternatively, load without the skill:

```
claude mock_assets/design-tokens.json mock_assets/component-tokens.css
```

**Step 1 — Schema and structural audit:**

```
Step 1 Prompt:
Load both token files and perform a structural audit:

1. Does design-tokens.json have all required top-level categories
   (color, spacing, typography, shadow)?
2. Are component-tokens.css variables using consistent naming
   conventions (kebab-case)?
3. Count total tokens across both files.

Output a structure summary: file, categories_found, token_count,
missing_categories, naming_issues
```

**Step 2 — Color token validation:**

```
Step 2 Prompt:
Validate all color tokens against this approved palette:

#1A6FB0 (brand-primary), #2A9D8F (brand-secondary), #F4A261 (accent),
#264653 (text-primary), #E9C46A (highlight), #FFFFFF (white),
#F5F5F5 (bg-light), #333333 (text-secondary)

For each color token in design-tokens.json:
1. Report current value
2. If it matches a palette color, mark Pass
3. If it's close but different hex, suggest the correct palette value
4. If it's not in the palette at all, flag as non-brand
5. Check hex format: 6-char lowercase required (flag #222 as wrong format)

Also check component-tokens.css for any hardcoded colors that
should use token variables.

Output: token_name, current, expected, status, action
```

**Step 3 — Typography and spacing validation:**

```
Step 3 Prompt:
Validate typography and spacing tokens:

1. Spacing: Approved scale is 4, 8, 12, 16, 24, 32, 48, 64, 96 (px).
   Check every spacing value in design-tokens.json. Flag 18px as
   off-scale and suggest the nearest scale value.

2. Typography: Approved brand typefaces are:
   - Inter for body copy
   - Plus Jakarta Sans for headings
   - JetBrains Mono for monospace
   Flag 'Comic Sans MS', serif as non-brand. Suggest the correct
   font family.

3. Font sizes: Approved scale is 10, 12, 14, 16, 18, 20, 24, 32, 40, 48, 64 (px).
   Flag any font size not on the scale.

Output: category, token_name, value, issue, suggestion
```

**Step 4 — Reference resolution:**

```
Step 4 Prompt:
Resolve all token references in both files:

1. In design-tokens.json, check {color.border.default} referenced
   by component.card.border. Does this token exist? If not, flag it
   and suggest the correct path (e.g., {color.text.secondary}).

2. Check {color.brand.primary} referenced by component.button.background.
   Does the JSON path color → brand → primary exist? What's its value?

3. In component-tokens.css, check var(--color-semantic-warning).
   Is this token defined anywhere? If not, flag as undefined reference.

4. Check var(--color-cta-background) and var(--color-cta-text).
   Are these still valid or are they deprecated?

Output: file, reference, resolves_to, status (ok/broken/deprecated), fix
```

**Step 5 — Export validation report:**

```
Step 5 Prompt:
Write a CSV called token_audit_report.csv with all issues found.
Columns: token_name, category, current_value, issue, severity, suggested_fix

Print a terminal summary:

=== TOKEN VALIDATION REPORT ===
Files scanned:        2
Total tokens scanned: XX
Total issues:         XX
  Color issues:       X
  Spacing issues:     X
  Typography issues:  X
  Broken references:  X
  Missing tokens:     X
  Deprecated names:   X

High severity:        X
Medium severity:      X
Low severity:         X

Status:               [PASS / MINOR ISSUES / FAIL]
```

---

## Exercise 3: Image Asset Inventory & Compliance Review

### Scenario

The Design team needs to inventory all files in the `mock_assets/` directory before a sprint handoff. They must catalog every file by type and size, check naming conventions, and cross-reference SVG compliance with the svg-auditor findings.

### Dataset

| File | Description |
|---|---|
| `mock_assets/` directory | 5 files total: 3 SVGs, 1 JSON token file, 1 CSS token file |

### Walkthrough Steps

```
claude mock_assets/
```

**Step 1 — Directory inventory:**

```
Step 1 Prompt:
List every file in the mock_assets/ directory. For each file, report:

1. Filename
2. Extension
3. File size in KB (use your best estimate)
4. Category (SVG icon, SVG logo, SVG illustration, JSON token, CSS token)
5. Whether the filename follows kebab-case (lowercase, hyphens, no spaces)

Sort by category. Flag any naming violations.
```

**Step 2 — Naming convention audit:**

```
Step 2 Prompt:
Audit all filenames for kebab-case compliance:

- All lowercase
- Words separated by hyphens
- No underscores
- No spaces
- No uppercase letters before the extension

For each violation, show:
filename, violation_type, suggested_correction

If a filename uses an underscore instead of a hyphen, flag it
even if it's otherwise correct.
```

**Step 3 — SVG compliance cross-reference:**

```
Step 3 Prompt:
I ran an SVG audit earlier. Cross-reference the results:

For each SVG in the directory, report known issues:
1. icon-cloud-sync.svg — viewBox decimals, missing a11y tags, hardcoded color
2. logo-hero-main.svg — missing viewBox, non-brand red, unused defs, editor metadata
3. illustration-dashboard.svg — empty desc, non-standard hex colors, hardcoded fonts

Create a cross-reference table:
file, viewBox_ok, colors_ok, a11y_ok, formatting_ok, pass/fail
```

**Step 4 — Generate inventory report:**

```
Step 4 Prompt:
Write a CSV called asset_inventory.csv with columns:

filename, extension, size_kb, category, kebab_case_ok, svg_compliance

Print a terminal summary:

=== ASSET INVENTORY REPORT ===
Total files:          5
  SVG icons:         1
  SVG logos:         1
  SVG illustrations: 1
  JSON tokens:       1
  CSS tokens:        1

Naming violations:   0 (all kebab-case)
SVGs with issues:    3
SVGs clean:          0

Overall status:      NEEDS CLEANUP — 3 of 3 SVGs have compliance issues

Recommendation: Run svg-auditor on all 3 SVGs and fix violations
before engineering handoff.
```

---

## Data File Reference

| File | Exercise | Description |
|---|---|---|
| `mock_assets/icon-cloud-sync.svg` | 1, 3 | Icon SVG with viewBox, color, and a11y issues |
| `mock_assets/logo-hero-main.svg` | 1, 3 | Logo SVG with missing viewBox and non-brand colors |
| `mock_assets/illustration-dashboard.svg` | 1, 3 | Illustration SVG with empty desc and non-standard colors |
| `mock_assets/design-tokens.json` | 2 | JSON token file with palette, spacing, and reference errors |
| `mock_assets/component-tokens.css` | 2, 3 | CSS component tokens with undefined variable references |

### Cross-Reference: Syllabus & Skills

| Resource | Purpose | Path |
|---|---|---|
| Design Syllabus | Full course outline for Design team | `../syllabus.md` |
| svg-auditor skill | Automated SVG structural and brand compliance audit | `../skills/svg-auditor/SKILL.md` |
| design-token-validator skill | Token file validation against design system spec | `../skills/design-token-validator/SKILL.md` |
| brand-guardrails skill | Brand compliance for marketing copy (adjacent skill) | `../../christine/skills/brand-guardrails/SKILL.md` |
