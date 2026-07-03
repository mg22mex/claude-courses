# Exercise 5 — Capstone: The Automated Design-to-Code Pipeline

## Scenario

This is the capstone exercise that integrates everything from Exercises 1-4. Engineering has requested a complete asset handoff package for the new dashboard redesign. The Design team has a messy creative dump with raw SVGs, unvalidated token files, and an incomplete component spec. Your job is to ingest everything, run the full compliance pipeline (audit, validate, compile, optimize), and produce a perfectly packaged asset library for direct developer hand-off — all within a single Claude Code session.

## Learning Objectives

- Ingest a mixed directory of raw SVG, JSON, CSS, and spec files
- Execute the svg-auditor, design-token-validator, component-spec-compiler, and asset-pack-optimizer skills in sequence
- Cross-reference findings across skills (e.g., token validation feeds into SVG color fixes)
- Compile a complete component spec into CSS variables and Style Dictionary JSON
- Package a production-ready `dist/` directory with all cleaned, verified assets
- Generate a consolidated handoff report for engineering

## Datasets

This exercise uses all files from `data/mock-assets/` plus the inline component spec below.

### Files from `../data/mock-assets/`

| File | Type |
|---|---|
| `icon-cloud-sync.svg` | Raw SVG icon |
| `logo-hero-main.svg` | Raw SVG logo |
| `illustration-dashboard.svg` | Raw SVG illustration |
| `design-tokens.json` | Global JSON token file |
| `component-tokens.css` | CSS component token file |

### Inline Component Spec (`dashboard-spec.md`)

```
# Dashboard Redesign — Component Spec

## Color Palette (Light Mode)

| Token | Value |
|---|---|
| --color-bg-canvas | #F5F7FA |
| --color-bg-card | #FFFFFF |
| --color-bg-sidebar | #1A1A2E |
| --color-text-primary | #1A1A1A |
| --color-text-secondary | #666666 |
| --color-text-on-dark | #FFFFFF |
| --color-border-light | #E8E8E8 |
| --color-border-default | #D0D5DD |
| --color-accent-blue | #1A6FB0 |
| --color-accent-teal | #2A9D8F |
| --color-accent-orange | #F4A261 |
| --color-semantic-success | #2A9D8F |
| --color-semantic-warning | #F4A261 |
| --color-semantic-error | #D92D20 |

## Typography

| Element | Font | Size | Weight | Line Height |
|---|---|---|---|---|
| Sidebar heading | Plus Jakarta Sans | 14px | 700 | 1.25 |
| Card title | Plus Jakarta Sans | 18px | 600 | 1.3 |
| Metric value | Plus Jakarta Sans | 32px | 700 | 1.2 |
| Metric label | Inter | 12px | 500 | 1.4 |
| Table header | Inter | 12px | 600 | 1.4 |
| Table cell | Inter | 14px | 400 | 1.5 |
| Filter label | Inter | 14px | 500 | 1.5 |

## Spacing (4px scale)

xs=4px, sm=8px, md=16px, lg=24px, xl=32px, xxl=48px

## Border Radius

sm=4px, md=8px, lg=12px, xl=16px, full=9999px

## Shadows

card: 0 1px 3px rgba(0,0,0,0.08), dropdown: 0 4px 12px rgba(0,0,0,0.12),
modal: 0 20px 25px rgba(0,0,0,0.15)

## Sidebar Navigation Anatomy

- Width: 240px
- Background: var(--color-bg-sidebar) = #1A1A2E
- Item padding: var(--spacing-sm) var(--spacing-md)
- Item border radius: var(--radius-md) = 8px
- Active item bg: rgba(255,255,255,0.1)
- Hover item bg: rgba(255,255,255,0.05)
- Text: var(--color-text-on-dark) = #FFFFFF
- Active indicator: 3px left border, var(--color-accent-blue)
- Divider: 1px solid rgba(255,255,255,0.1)
- Font: Sidebar heading typography
```

### Known Issues Planted Across All Data

| Issue | Location | Exercise Cross-Reference |
|---|---|---|
| Non-integer viewBox | `icon-cloud-sync.svg` | Exercise 1 (SVG audit) |
| Missing viewBox | `logo-hero-main.svg` | Exercise 1 (SVG audit) |
| Hardcoded colors | All 3 SVGs | Exercise 1 (color tokenization) |
| Missing a11y tags | `icon-cloud-sync.svg`, `logo-hero-main.svg` | Exercise 1 (accessibility) |
| Wrong brand primary | `design-tokens.json` | Exercise 2 (color validation) |
| Off-scale spacing | `design-tokens.json` | Exercise 2 (spacing validation) |
| Broken references | `design-tokens.json`, `component-tokens.css` | Exercise 2 (reference resolution) |
| Deprecated token names | `component-tokens.css` | Exercise 2 (naming conventions) |
| Editor metadata | `logo-hero-main.svg` | Exercise 4 (SVG optimization) |
| No dark mode in spec | `dashboard-spec.md` | Exercise 3 (spec completeness) |

## Walkthrough

### Phase A — SVG Audit & Fix (Exercise 1 skills)

```bash
claude ../data/mock-assets/icon-cloud-sync.svg ../data/mock-assets/logo-hero-main.svg ../data/mock-assets/illustration-dashboard.svg
```

Prompt:

```
Run a complete SVG audit on all three files:

1. viewBox check: presence, integer values, positive dimensions
2. Color governance: flag every hardcoded fill/stroke, cross-reference
   against #1A6FB0, #2A9D8F, #F4A261 as the brand palette
3. Accessibility: check title, desc, role="img"
4. Redundancy: empty groups, unused defs, editor metadata

After the audit, fix all issues:
- Correct viewBox values (decimals → integers, add missing viewBox)
- Replace hardcoded colors with var(--color-*) tokens
- Add title, desc, role="img" where missing
- Strip sodipodi:*, inkscape:*, xml:space attributes
- Remove empty groups and unused defs

Save corrected SVGs as fixed-icon-cloud-sync.svg, fixed-logo-hero-main.svg,
and fixed-illustration-dashboard.svg.
```

### Phase B — Token Validation & Fix (Exercise 2 skills)

Continue in the same session:

```
Now load ../data/mock-assets/design-tokens.json and
../data/mock-assets/component-tokens.css.

Run a full token validation:

1. Schema check: required categories (color, spacing, typography, shadow)
2. Color validation against approved palette:
   #1A6FB0, #2A9D8F, #F4A261, #264653, #E9C46A,
   #FFFFFF, #F5F5F5, #333333
3. Spacing validation against 4px modular scale (4,8,12,16,24,32,48,64,96)
4. Typography: approved typefaces (Inter, Plus Jakarta Sans, JetBrains Mono)
5. Resolve all {reference} and var(--...) references
6. Flag deprecated naming (--color-cta-* → --color-button-*)

Fix all issues found:
- Correct off-palette colors
- Fix spacing values to nearest scale step
- Update font families to brand typefaces
- Resolve broken references
- Rename deprecated tokens
- Add missing required tokens (--color-semantic-success, --shadow-card)

Save corrected files as design-tokens-fixed.json and
component-tokens-fixed.css.
```

### Phase C — Component Spec Compilation (Exercise 3 skills)

Continue in the session. Load the Dashboard Redesign spec:

```
Now compile the dashboard spec into CSS and JSON tokens.

Use the following spec for the Dashboard Redesign:

[Paste the dashboard-spec.md content above]

Generate:
1. component-tokens-output.css — CSS custom properties for:
   - Color palette (canvas, card, sidebar, text, border, accent, semantic)
   - Typography (sidebar, card title, metric, table, filter styles)
   - Spacing (4px scale: xs through xxl)
   - Border radius (sm through full)
   - Shadows (card, dropdown, modal)

2. style-dictionary-output.json — Style Dictionary format with
   {value, type} per token

3. component-tokens-sidebar.css — Component-specific tokens for
   the Sidebar Navigation anatomy (width, bg, item padding,
   active/hover states, active indicator, divider, font)

Cross-reference verification: after generation, confirm every
var(--...) resolves to a defined variable in your CSS output.
```

### Phase D — Asset Pack Optimization (Exercise 4 skills)

Continue in the session:

```
Now optimize and package all processed assets.

Step 1 — Directory classification:
Scan the working directory for all fixed SVG files, token files,
and spec files. Classify each by type.

Step 2 — SVG final pass:
For each fixed SVG, confirm:
- viewBox is present and valid
- No editor metadata remains
- Hardcoded colors are replaced
- Accessibility tags exist

Step 3 — Build dist/ directory:

dist/
├── icons/
│   ├── filled/
│   └── outlined/
├── illustrations/
├── tokens/
│   ├── global/
│   ├── component/
│   └── spec/
├── manifest.csv
└── rename-log.csv

Step 4 — Generate manifest:
Write manifest.csv with: filename, category, size_before, size_after,
savings_pct, quality_checks (pass/fail per check)

Write rename-log.csv with any renames applied.
```

### Phase E — Consolidated Engineering Handoff Report

Prompt (continuing the session):

```
Produce a single consolidated handoff report covering all phases.

Write handoff_report.md with these sections:

1. Executive Summary
   - Total assets processed
   - Overall quality gate status (PASS / MINOR ISSUES / FAIL)

2. SVG Audit Summary
   - Files audited: X
   - Issues found: X (viewBox, colors, a11y, formatting)
   - Issues fixed: X
   - Byte reduction: X% average

3. Token Validation Summary
   - Files validated: X
   - Tokens scanned: X
   - Issues found: X (color, spacing, typography, references, naming)
   - Issues fixed: X

4. Component Spec Compilation
   - Spec compiled: dashboard-spec.md
   - CSS variables generated: X
   - JSON tokens generated: X
   - Component blocks: sidebar navigation

5. Distribution Package
   - dist/ structure: X directories, X files
   - manifest.csv: complete
   - rename-log.csv: complete

6. Quality Gate Results
   - All SVGs have valid viewBox: YES/NO
   - All icons use currentColor: YES/NO
   - All filenames are kebab-case: YES/NO
   - All token references resolve: YES/NO
   - No hardcoded brand colors remain: YES/NO

7. Recommendations
   - Items deferred or requiring manual review
   - Suggested next sprint additions (dark mode, responsive tokens)

Print a terminal gate summary:

=== DESIGN-TO-CODE PIPELINE — QUALITY GATE ===
SVGs audited & fixed:   3/3  ✅
Tokens validated:        2/2  ✅
Spec compiled:           1/1  ✅
Assets packaged:         X/X  ✅
References resolved:     ALL  ✅
Kebab-case naming:       ALL  ✅

Overall:                 PASS ✅
Package:                 dist/
Report:                  handoff_report.md
```

## Expected Output

After completing all phases, you should have:

- **Phase A**: 3 corrected SVGs (`fixed-*.svg`) with valid viewBox, tokenized colors, a11y tags, no metadata
- **Phase B**: 2 corrected token files (`-fixed.json`, `-fixed.css`) with validated colors, spacing, typography, and resolved references
- **Phase C**: 3 generated files (`component-tokens-output.css`, `style-dictionary-output.json`, `component-tokens-sidebar.css`)
- **Phase D**: A `dist/` directory with organized subdirectories, `manifest.csv`, and `rename-log.csv`
- **Phase E**: A `handoff_report.md` with consolidated findings and quality gate results
- A complete, engineering-ready asset handoff package
- Practical experience running the full automated Design-to-Code pipeline
