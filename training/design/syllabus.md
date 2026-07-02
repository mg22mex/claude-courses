# Design: SVG Auditing, Design Tokens & Asset Management with Claude Code

**Course Title:** SVG Auditing, Design Tokens & Asset Management with Claude Code
**Target User:** Design team
**Prerequisites:** Familiarity with SVG files, design tokens, and basic file management; no coding experience required.
**Estimated Duration:** 6 hours (split across three 2-hour sessions)
**Format:** Live walkthrough + hands-on terminal exercises

---

## Learning Objectives

By the end of this course, the Design team will be able to:

1. Load SVG files into Claude Code and audit them for viewBox correctness, hardcoded colors, and missing accessibility tags.
2. Replace hardcoded SVG styling attributes with design token variables using Claude's batch editing capabilities.
3. Validate design token files (CSS custom properties and JSON token schemas) against a brand design system specification.
4. Scan asset directories to produce a structured inventory of image formats, dimensions, and naming convention violations.
5. Generate CSV audit reports for handoff to engineering and brand teams.
6. Build a reusable weekly design review prompt that validates all new assets before handoff.
7. Convert Figma design specs (color palettes, typography matrices, border dimensions) into CSS custom properties and platform-agnostic style dictionaries.
8. Minify SVG paths, enforce naming conventions, and package assets into structured distribution-ready directories.

---

## Lesson Breakdown

### Lesson 1 — SVG Asset Auditing & Optimization (60 min)

**Objective:** Use Claude Code to load SVG files, inspect them for structural correctness, brand color compliance, and accessibility completeness.

| Segment | Topic | Activity |
|---|---|---|
| 1.1 | Why SVG auditing matters | SVGs are text files — Claude Code can inspect viewBox, colors, and accessibility tags inline, catching issues before they reach production. |
| 1.2 | Loading SVG files | Load three sample SVGs from `data/mock_assets/` — an icon, logo, and illustration. |
| 1.3 | Running the svg-auditor skill | Invoke Claude Code with the `svg-auditor` skill to scan all three SVGs. |
| 1.4 | Understanding viewBox and canvas issues | Review flagged viewBox problems: missing viewBox, non-integer values, incorrect aspect ratios. |
| 1.5 | Color governance and path optimization | Identify hardcoded colors that should be CSS token variables. Flag overly complex path data for optimization. |

**CLI Exercises:**

```
# Exercise 1.3 — Run SVG audit on icon set
claude data/mock_assets/icon-cloud-sync.svg data/mock_assets/logo-hero-main.svg data/mock_assets/illustration-dashboard.svg --skill svg-auditor
```

Prompt:

```
Load the three SVG files and run a full audit:

1. Check each SVG for viewBox presence and correctness. Flag any
   missing, zero, or non-integer viewBox values.
2. Scan every element for hardcoded fill, stroke, and stop-color
   attributes. Flag non-brand colors.
3. Check for accessibility: does each SVG have a <title> element?
   A <desc> element? Flag missing ones.
4. Identify empty groups (<g></g>), unused <defs>, and unnecessary
   attributes like xml:space, version, sodipodi:*.

Output a table per file: check, status (pass/fail/warn), detail
```

```
# Exercise 1.4 — Fix viewBox and accessibility
Prompt (continuing the same session):

For each SVG that failed the viewBox or accessibility checks:

1. Show me the current viewBox value and the corrected value.
2. Add missing <title> and <desc> elements where absent.
   - <title> should describe the icon purpose
   - <desc> should provide context for screen readers
3. Show a before/after diff for each change.
```

```
# Exercise 1.5 — Replace hardcoded colors with tokens
Prompt (continuing the same session):

For each SVG with hardcoded fill/stroke colors:

1. Replace any instance of #0066cc with var(--color-primary).
2. Replace #FF0000 or #ff0000 with var(--color-danger).
3. Any other hardcoded hex color — flag it and suggest the correct
   design token based on the file's context.

Output a table: file, old_color, new_token, line_number
Show a diff summary for the most impactful change per file.
```

---

### Lesson 2 — Design Token Validation (60 min)

**Objective:** Validate CSS custom properties and JSON token files against a design system specification, flagging inconsistencies, missing tokens, and broken references.

| Segment | Topic | Activity |
|---|---|---|
| 2.1 | The token management problem | Design token files grow organically and accumulate drift. Claude Code can diff token values against a spec and flag every inconsistency. |
| 2.2 | Loading token files | Load `design-tokens.json` and `component-tokens.css` from `data/mock_assets/`. |
| 2.3 | Running the design-token-validator skill | Invoke Claude Code with the `design-token-validator` skill. |
| 2.4 | Color and spacing validation | Review flagged color values outside the approved palette, inconsistent hex formats, and spacing values off the modular scale. |
| 2.5 | Token reference resolution and missing tokens | Identify broken `{reference}` paths and missing required tokens. |

**CLI Exercises:**

```
# Exercise 2.3 — Run token validation
claude data/mock_assets/design-tokens.json data/mock_assets/component-tokens.css --skill design-token-validator
```

Prompt:

```
Load both token files and perform a validation:

1. Check design-tokens.json structure: does it have the required
   top-level categories (color, spacing, typography, shadow)?
2. Validate every color value against this approved palette:
   #1A6FB0 (brand-primary), #2A9D8F (brand-secondary),
   #F4A261 (accent), #264653 (text-primary), #E9C46A (highlight),
   #FFFFFF (white), #F5F5F5 (bg-light), #333333 (text-secondary)
3. Check that all hex values use 6-character lowercase format.
4. Validate spacing values against the modular scale:
   4, 8, 12, 16, 24, 32, 48, 64 (px). Flag anything not on this scale.
5. Check that all {reference} values resolve to existing tokens.
6. Flag any tokens using deprecated naming conventions (e.g.,
   --color-cta-* should be --color-button-*).

Output a validation table per category.
```

```
# Exercise 2.4 — Fix color and spacing inconsistencies
Prompt (continuing the same session):

For each flagged color inconsistency:

1. If the value is close to a palette color, suggest the correct palette
   value and show a diff.
2. If the hex format is wrong (e.g., #222 vs #222222), normalize to
   6-character lowercase.
3. For spacing values off the modular scale, suggest the nearest
   scale value.

Show me: token_name, current_value, corrected_value, reason
```

```
# Exercise 2.5 — Fix broken references and add missing tokens
Prompt (continuing the same session):

1. For each broken token reference (e.g., {color.brand.primary} that
   doesn't resolve), update the reference path to match the actual
   token structure in the file.
2. Identify missing required tokens and suggest their values based on
   the palette:
   - --color-semantic-success: #2A9D8F
   - --shadow-card: 0 2px 8px rgba(0,0,0,0.1)
3. For deprecated token names, show the old name and the replacement.

Write the corrected file as design-tokens-fixed.json.
```

---

### Lesson 3 — Image Asset Inventory & Metadata Review (60 min)

**Objective:** Scan directories of image assets and produce structured inventories with format, dimension, and naming convention checks.

| Segment | Topic | Activity |
|---|---|---|
| 3.1 | Why asset inventory matters | Design directories accumulate orphaned assets, wrong formats, and inconsistent naming. Claude Code can inventory an entire folder in seconds. |
| 3.2 | Scanning a directory | Ask Claude to list all files in `data/mock_assets/` and classify each by type (SVG, PNG, JPG, JSON, CSS). |
| 3.3 | Format and naming checks | Check that all image files use approved formats, that filenames follow kebab-case, and that no orphaned duplicates exist. |
| 3.4 | SVG compliance cross-check | Re-run the svg-auditor checks on any SVGs in the directory and append the results to the inventory. |
| 3.5 | Exporting the inventory CSV | Write a structured CSV with file metadata for handoff to engineering. |

**CLI Exercises:**

```
# Exercise 3.2 — Inventory scan
claude data/mock_assets/
```

Prompt:

```
List every file in the data/mock_assets/ directory. For each file, report:
- Filename
- Extension
- File size (KB)
- Category (SVG icon, SVG logo, SVG illustration, JSON, CSS, other)

Sort by category. Flag any file that doesn't use kebab-case naming.
```

```
# Exercise 3.3 — Naming convention audit
Prompt (continuing the same session):

Check all filenames against kebab-case conventions:

- Should be lowercase
- Words separated by hyphens, not underscores or spaces
- No uppercase letters in the filename (extension can be lowercase)

Flag any violations: filename, violation_type, suggested_correction
```

```
# Exercise 3.5 — Export asset inventory
Prompt (continuing the same session):

Write an inventory CSV called asset_inventory.csv with columns:

filename, extension, size_kb, category, kebab_case_ok, svg_issues

For the svg_issues column, cross-reference with the svg-auditor
findings: if an SVG had viewBox issues, write "viewBox"; if it had
missing accessibility tags, write "a11y"; if clean, write "pass".

Print a terminal summary:

=== ASSET INVENTORY REPORT ===
Total files:          XX
SVG files:            X
JSON token files:     X
CSS token files:      X
Other:                X

Naming violations:    X
SVGs with issues:     X
SVGs clean:           X

Overall status:       [all good / needs cleanup / needs review]
```

---

### Lesson 4 — Building the Weekly Design Review Pipeline (60 min)

**Objective:** Package all checks into a single reusable prompt that validates new design assets before engineering handoff.

| Segment | Topic | Activity |
|---|---|---|
| 4.1 | The weekly review problem | Handing off design assets without validation causes engineering churn. A single Claude prompt can catch issues before they leave the design team. |
| 4.2 | Building the combined review prompt | Create a prompt that loads all new SVGs + token files, runs svg-auditor + token-validator, and writes a single consolidated report. |
| 4.3 | Running the full pipeline | Load the `data/mock_assets/` directory and run the full weekly review. |
| 4.4 | Reading the consolidated report | The report includes SVG violations, token inconsistencies, and naming issues in one CSV. |
| 4.5 | Iterating until clean | Fix issues, re-run the review, and confirm all checks pass before marking the assets as ready for handoff. |

**CLI Exercises:**

```
# Exercise 4.2 — Create the weekly review prompt
```

Create a file called `weekly-design-review.md` with this content during the lesson:

```markdown
I have the following files loaded from data/mock_assets/:
- All .svg files
- design-tokens.json
- component-tokens.css

Please do the following, in order:

## Step 1 — SVG Audit
Run a full audit on every SVG file:
- viewBox presence and correctness
- Hardcoded fill/stroke colors (flag non-brand colors)
- Accessibility tags (title, desc)
- Empty groups, unused defs, unnecessary attributes
Output a violations table.

## Step 2 — Token Validation
Run a full validation on design-tokens.json and component-tokens.css:
- Check all color values against approved palette
- Check spacing values against modular scale
- Resolve all token references
- Flag missing required tokens and deprecated names
Output a validation table.

## Step 3 — Asset Inventory
List all files in the directory:
- Filename, extension, size
- Kebab-case naming check
- Cross-reference SVG issues from Step 1

## Step 4 — Consolidated Report
Write a single CSV called design_weekly_report.csv with sections:
1. "svg_violations" — file, check, status, detail
2. "token_issues" — token_name, category, issue, fix
3. "naming_issues" — filename, violation, suggestion

Print a summary with:
- Total SVG issues found
- Total token issues found
- Total naming issues found
- Overall readiness flag (PASS / MINOR ISSUES / FAIL)
```

```
# Exercise 4.3 — Run the full pipeline
claude data/mock_assets/*.svg data/mock_assets/design-tokens.json data/mock_assets/component-tokens.css < weekly-design-review.md
```

```
# Exercise 4.5 — Iterate until clean
Prompt (continuing the same session):

Take the consolidated report and fix all issues found:

1. Fix viewBox and accessibility on SVGs first.
2. Replace hardcoded colors with design tokens.
3. Fix token values and broken references.
4. Rename any files with naming violations.

After each fix round, confirm the change. When all fixes are
applied, re-run the checks and confirm the report shows PASS.
```

---

### Lesson 5 — Component Spec Compiler (60 min)

**Objective:** Translate Figma design specifications — color palettes, typography matrices, spacing grids, and border dimensions — into clean CSS custom properties and JSON style dictionaries for engineering handoff.

| Segment | Topic | Activity |
|---|---|---|
| 5.1 | The spec-to-code gap | Designers produce pixel specs in Figma. Engineers need CSS variables and token files. Manual conversion is slow and error-prone — Claude Code can automate it. |
| 5.2 | Loading a component spec | Load a structured design spec document with color swatches, type scale, spacing grid, and button anatomy. |
| 5.3 | Generating CSS custom properties | Convert the spec into namespaced `--color-*`, `--typography-*`, `--spacing-*`, and `--radius-*` variables. |
| 5.4 | Building a Style Dictionary JSON | Generate a platform-agnostic JSON token file following the `{value, type}` format. Include category groupings. |
| 5.5 | Component-specific tokens | For component anatomy specs (e.g., button system), generate self-contained component token blocks referencing the global variables. |

**CLI Exercises:**

```
# Exercise 5.3 — Generate CSS custom properties from a spec
```

Prompt:

```
I have the following design spec for a button component:

COLORS
- Primary (default): #1A6FB0
- Primary (hover): #155892
- Text on primary: #FFFFFF
- Border: #D0D5DD
- Background secondary: #F5F7FA

TYPOGRAPHY
- Button label: Inter, 14px, 600 weight, 1.25 line height
- Body: Inter, 16px, 400 weight, 1.5 line height
- Heading 1: Inter, 32px, 700 weight, 1.25 line height, -0.02em letter spacing

SPACING (4px base scale)
- xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px

BORDER RADIUS
- sm: 4px, md: 8px, lg: 12px, full: 9999px

Generate:

1. CSS custom properties file with sections:
   /* Color palette */, /* Typography */, /* Spacing */, /* Border radius */

2. Naming convention: --category-property-modifier
   Example: --color-primary-hover, --typography-h1-size

3. All spacing in px. All colors as 6-character hex.
```

```
# Exercise 5.4 — Generate Style Dictionary JSON
Prompt (continuing the same session):

Take the same spec and generate a Style Dictionary JSON file.

Format requirements:
- Nested object structure by category
- Each token has "value" and "type" fields
- Types: color, dimension, number, string
- No nested CSS variable references — just the raw values

Categories to include: color, typography, spacing, borderRadius
```

```
# Exercise 5.5 — Component token block
Prompt (continuing the same session):

Using the generated CSS variables, create component-specific tokens for
the button system:

Required states: default, hover, active, disabled, focus
Properties per state: background, text, border
Also include: padding, font, font-size, border-radius

Naming: --button-{variant}-{property}-{state}

Output the component token block and cross-reference every
var(--...) to confirm it resolves to a defined variable above.
```

---

### Lesson 6 — Asset Pack Optimizer (60 min)

**Objective:** Minify SVG path data, validate naming conventions, strip editor metadata, and organize assets into a distribution-ready directory package.

| Segment | Topic | Activity |
|---|---|---|
| 6.1 | The asset handoff problem | Raw SVG exports from design tools contain editor metadata, non-standard filenames, and bloated path data. Engineering needs clean, optimized assets. |
| 6.2 | Scanning an asset directory | Load the `data/mock_assets/` directory and classify every file by type — SVG icon, SVG illustration, PNG, JSON, CSS. |
| 6.3 | SVG path minification | For each SVG: remove Inkscape/Sodipodi metadata, empty groups, and redundant attributes. Normalize viewBox and inject accessibility tags. |
| 6.4 | Naming convention enforcement | Audit all filenames for kebab-case compliance. Fix violations: uppercase → lowercase, underscores → hyphens, version suffixes stripped. |
| 6.5 | Distribution packaging | Generate a `dist/` directory with organized subdirectories (icons/filled, icons/outlined, illustrations, raster) and a manifest CSV. |

**CLI Exercises:**

```
# Exercise 6.2 — Classify assets in a directory
claude data/mock_assets/
```

Prompt:

```
Scan all files in data/mock_assets/ and classify each:

| File | Extension | Category | Naming OK? |
|---|---|---|---|

Category: SVG icon / SVG illustration / JSON token / CSS token / raster / other
Naming: is it valid kebab-case? Flag any violations.

Also report: total files, SVGs, non-SVGs.
```

```
# Exercise 6.3 — Minify a set of SVGs
claude data/mock_assets/*.svg
```

Prompt:

```
Load every SVG file from data/mock_assets/ and optimize each one:

1. Remove these attributes if present:
   - xml:space, version, sodipodi:*, inkscape:*, id

2. Remove empty <g></g> groups.

3. Check viewBox — is it present? Non-integer? Missing?
   Fix any issues found.

4. After cleanup, measure the byte reduction per file.

5. Check for missing accessibility:
   - Missing <title> → add derived from filename
   - Missing <desc> → add
   - Missing role="img" → add

Output: per-file table with bytes before, bytes after, savings %,
and issues found.
```

```
# Exercise 6.4 — Rename, package and manifest
Prompt (continuing the session, covering all files in data/mock_assets/):

1. Audit all filenames for kebab-case violations.
2. Build a rename plan: old_name → new_name → reason.
3. Create a dist/ directory with:
   - icons/ (SVGs under 10 KB with currentColor)
   - illustrations/ (multi-color SVGs)
   - raster/ (PNG, JPG files)
   - tokens/ (JSON, CSS)
4. Write manifest.csv: filename, category, size_before, size_after,
   savings_pct, issues
5. Write rename-log.csv

Output a terminal summary like:

=== ASSET PACK OPTIMIZER SUMMARY ===
SVGs optimized:   X
Bytes removed:    X (X% avg)
Naming fixes:     X
Files packaged:   X into dist/
Status:           Ready for distribution
```

---

## Sample Data Files

The following sample files are provided in `data/mock_assets/` for use during exercises:

| File | Description |
|---|---|
| `icon-cloud-sync.svg` | Icon SVG (24×24) with missing accessibility tags, hardcoded color, and non-integer viewBox |
| `logo-hero-main.svg` | Logo SVG with missing viewBox, hardcoded non-brand red, and unused defs |
| `illustration-dashboard.svg` | Illustration SVG with empty desc tag, overly complex paths, and deprecated elements |
| `design-tokens.json` | JSON token file with non-palette colors, off-scale spacing, broken references, and missing required tokens |
| `component-tokens.css` | CSS token file with undefined variable references, hardcoded values, and incomplete component token sets |

---

## Link Directory

| Resource | Path / Location |
|---|---|
| Course slide deck | `training/design/` |
| Sample data assets | `training/design/data/mock_assets/` |
| Design lab exercises | `training/design/exercises/design-labs.md` |
| svg-auditor skill | `skills/svg-auditor/SKILL.md` |
| design-token-validator skill | `skills/design-token-validator/SKILL.md` |
| component-spec-compiler skill | `skills/component-spec-compiler/SKILL.md` |
| asset-pack-optimizer skill | `skills/asset-pack-optimizer/SKILL.md` |
| brand-guardrails skill | `../christine/skills/brand-guardrails/SKILL.md` |

---

## Success Criteria

The Design team can independently:

- [ ] Load SVG files and run a full audit for viewBox, color governance, and accessibility using the svg-auditor skill
- [ ] Replace hardcoded SVG styling with design token variables and show before/after diffs
- [ ] Validate design token files against a brand color palette and modular spacing scale
- [ ] Fix broken token references, missing tokens, and deprecated naming conventions
- [ ] Scan an asset directory and produce a structured inventory CSV with naming and format checks
- [ ] Run the weekly design review pipeline and confirm all checks pass before handoff
- [ ] Compile Figma design specs into CSS custom properties and platform-agnostic JSON style dictionaries
- [ ] Minify SVGs, enforce kebab-case naming, and package assets into structured distribution directories
