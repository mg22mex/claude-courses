# Design: SVG Auditing, Design Tokens & Asset Management with Claude Code

**Course Title:** SVG Auditing, Design Tokens & Asset Management with Claude Code
**Target User:** Design team (Paula & Gaby)
**Prerequisites:** Familiarity with SVG files, design tokens, and basic file management; no coding experience required.
**Estimated Duration:** 5 hours (split across five 1-hour sessions)
**Format:** Live walkthrough + hands-on terminal exercises

---

## Pre-Work: Load Your Institutional Memory

Before starting this course, open the [Master Claude Code Guide](https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1) alongside your domain-specific NotebookLM notebook. Query both notebooks to understand how Claude Code operates in your domain before writing any scripts or building tools.

**Your Domain Notebook:** [Design Team Notebook](https://notebooklm.google.com/notebook/9f67d0db-49c8-4bc3-b2e5-f08a3528028f?authuser=1)

> **Workflow Rule:** All script generation, data testing, or document templating in this track must cross-verify patterns against both the Master Guide and your Domain Notebook before execution.

---

## Learning Objectives

By the end of this course, the Design team will be able to:

1. Interrogate the design Domain NotebookLM to establish strict asset validation baselines before writing any audit scripts.
2. Parse raw SVG XML elements and flag broken paths, missing viewBox attributes, and non-standard inline styling using the svg-auditor skill.
3. Read and parse structured JSON design token files, verifying hex codes, font scale values, and spacing variables against the approved master system using the design-token-validator skill.
4. Convert raw layout coordinates, dimensions, and visual properties into CSS custom properties and platform-agnostic style dictionaries using the component-spec-compiler skill.
5. Programmatically clean, compress, strip metadata from, and organize batches of visual assets into production-ready folder trees using the asset-pack-optimizer skill.
6. Run an end-to-end design-to-code pipeline that ingests raw asset dumps, executes compliance checks, compiles theme specifications, and packages an optimized asset library for developer handoff.

---

## Lesson Breakdown

### Lesson 1 — SVG Structural Auditing (60 min)

**Objective:** Interrogate the design Domain NotebookLM to establish strict asset validation baselines, then use Claude Code to parse raw SVG XML elements and flag broken paths, missing viewBox attributes, and non-standard inline styling.

| Segment | Topic | Activity |
|---|---|---|
| 1.1 | Loading the Domain Notebook | Open the Design NotebookLM and query for SVG validation baselines, brand color standards, and accessibility requirements before writing any audit scripts. |
| 1.2 | Loading SVG files into Claude Code | Load three sample SVGs from `data/mock-assets/` — an icon, logo, and illustration. |
| 1.3 | Running the svg-auditor skill | Invoke Claude Code with the `svg-auditor` skill to scan all three SVGs for viewBox, color governance, accessibility, and path redundancy. |
| 1.4 | Parsing viewBox and canvas issues | Review flagged viewBox problems: missing viewBox, non-integer values, incorrect aspect ratios. |
| 1.5 | Tokenizing colors and stripping metadata | Replace hardcoded colors with `var(--...)` tokens. Strip editor metadata (sodipodi, inkscape, xml:space). |

**Lab:** `exercises/exercise-1.md` — SVG Structural Auditing

**CLI Exercises:**

```
# Exercise 1.3 — Run SVG audit on icon set
claude data/mock-assets/icon-cloud-sync.svg data/mock-assets/logo-hero-main.svg data/mock-assets/illustration-dashboard.svg --skill svg-auditor
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

---

### Lesson 2 — Automated Design Token Validation (60 min)

**Objective:** Build local prompt workflows to read and parse structured JSON design token files, verifying that hex codes, font scale values, and spacing variables match the approved master system.

| Segment | Topic | Activity |
|---|---|---|
| 2.1 | The token management problem | Design token files accumulate drift. Claude Code can diff token values against a spec and flag every inconsistency. |
| 2.2 | Loading token files | Load `design-tokens.json` and `component-tokens.css` from `data/mock-assets/`. |
| 2.3 | Running the design-token-validator skill | Invoke Claude Code with the `design-token-validator` skill. |
| 2.4 | Color and spacing validation | Review flagged color values outside the approved palette, inconsistent hex formats, and spacing values off the modular scale. |
| 2.5 | Token reference resolution and missing tokens | Identify broken `{reference}` paths and missing required tokens. |

**Lab:** `exercises/exercise-2.md` — Automated Design Token Validation

**CLI Exercises:**

```
# Exercise 2.3 — Run token validation
claude data/mock-assets/design-tokens.json data/mock-assets/component-tokens.css --skill design-token-validator
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

---

### Lesson 3 — Component Specification Compiling (60 min)

**Objective:** Leverage the `component-spec-compiler` skill to systematically convert raw layout coordinates, dimensions, and visual properties into uniform CSS custom properties and platform-agnostic style dictionaries.

| Segment | Topic | Activity |
|---|---|---|
| 3.1 | The spec-to-code gap | Designers produce pixel specs in Figma. Engineers need CSS variables and token files. Claude Code automates the conversion. |
| 3.2 | Loading a design spec | Load a structured component spec with color swatches, type scale, spacing grid, and button anatomy. |
| 3.3 | Generating CSS custom properties | Convert the spec into namespaced `--color-*`, `--typography-*`, `--spacing-*`, and `--radius-*` variables. |
| 3.4 | Building a Style Dictionary JSON | Generate a platform-agnostic JSON token file following the `{value, type}` format with category groupings. |
| 3.5 | Component-specific token blocks | For component anatomy specs (button system), generate self-contained component token blocks referencing global variables. |

**Lab:** `exercises/exercise-3.md` — Component Specification Compiling

**CLI Exercises:**

```
# Exercise 3.3 — Generate CSS custom properties from a spec
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

---

### Lesson 4 — Production Asset Pack Optimization (60 min)

**Objective:** Execute automated terminal utilities (`asset-pack-optimizer`) to programmatically clean, compress, strip metadata from, and organize batches of visual assets into strict production-ready folder trees.

| Segment | Topic | Activity |
|---|---|---|
| 4.1 | The asset handoff problem | Raw SVG exports contain editor metadata, non-standard filenames, and bloated path data. Engineering needs clean, optimized assets. |
| 4.2 | Scanning and classifying an asset directory | Load the `data/mock-assets/` directory and classify every file by type — SVG icon, SVG illustration, JSON, CSS. |
| 4.3 | SVG path minification and metadata stripping | For each SVG: remove Inkscape/Sodipodi metadata, empty groups, redundant attributes. Normalize viewBox and inject accessibility tags. |
| 4.4 | Naming convention enforcement | Audit all filenames for kebab-case compliance. Fix violations: uppercase → lowercase, underscores → hyphens, version suffixes stripped. |
| 4.5 | Distribution packaging | Generate a `dist/` directory with organized subdirectories (icons/filled, icons/outlined, illustrations, tokens) and a manifest CSV. |

**Lab:** `exercises/exercise-4.md` — Production Asset Pack Optimization

**CLI Exercises:**

```
# Exercise 4.2 — Classify assets in a directory
claude data/mock-assets/
```

Prompt:

```
Scan all files in data/mock-assets/ and classify each:

| File | Extension | Category | Naming OK? |
|---|---|---|---|

Category: SVG icon / SVG illustration / JSON token / CSS token / raster / other
Naming: is it valid kebab-case? Flag any violations.

Also report: total files, SVGs, non-SVGs.
```

```
# Exercise 4.3 — Minify and optimize SVGs
claude data/mock-assets/*.svg --skill asset-pack-optimizer
```

Prompt:

```
Run the asset-pack-optimizer on every SVG in data/mock-assets/:

1. Strip editor metadata: sodipodi:*, inkscape:*, xml:space, version
2. Remove empty <g></g> groups and unused <defs>
3. Normalize viewBox (fix decimals, add missing values)
4. Replace hardcoded colors with currentColor or token variables
5. Add missing <title>, <desc>, and role="img"

Output: per-file table with bytes before, bytes after, savings %,
and issues found.
```

---

### Lesson 5 — Capstone: The Automated Design-to-Code Pipeline (60 min)

**Objective:** An end-to-end laboratory where the Design team ingests a raw, messy creative asset dump, executes automated code-level compliance checks, compiles theme specifications, and packages a perfectly optimized asset library for direct developer hand-off.

| Segment | Topic | Activity |
|---|---|---|
| 5.1 | The complete handoff workflow | Engineering needs verified SVGs, validated tokens, compiled style dictionaries, and an organized package. One Claude Code session can deliver all four. |
| 5.2 | SVG audit + token validation pipeline | Run svg-auditor and design-token-validator in sequence; cross-reference findings (token colors feed into SVG fixes). |
| 5.3 | Component spec compilation | Compile the dashboard redesign spec into CSS variables and Style Dictionary JSON. |
| 5.4 | Asset optimization and packaging | Run asset-pack-optimizer on all corrected files; produce dist/ with manifest and rename log. |
| 5.5 | Consolidated handoff report | Generate a single engineering handoff report with quality gate results and recommendations. |

**Lab:** `exercises/exercise-5.md` — Capstone: The Automated Design-to-Code Pipeline

**CLI Exercises:**

```
# Exercise 5.2 — Run the full pipeline
claude ../data/mock-assets/
```

Prompt:

```
Run the complete design-to-code pipeline:

1. SVG Audit: Run svg-auditor on all SVGs. Fix viewBox, colors,
   a11y, and metadata issues. Save corrected SVGs.

2. Token Validation: Run design-token-validator on design-tokens.json
   and component-tokens.css. Fix colors, spacing, references, and
   naming. Save corrected token files.

3. Spec Compilation: Compile the dashboard redesign spec into
   component-tokens-output.css and style-dictionary-output.json.

4. Asset Optimization: Run asset-pack-optimizer to create dist/
   with organized subdirectories, manifest.csv, and rename-log.csv.

5. Handoff Report: Write handoff_report.md with consolidated
   findings and quality gate results.

Print the final quality gate summary for engineering sign-off.
```

---

## Sample Data Files

The following sample files are provided in `data/mock-assets/` for use during exercises:

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
| Sample data assets | `training/design/data/mock-assets/` |
| Exercise 1 — SVG Structural Auditing | `training/design/exercises/exercise-1.md` |
| Exercise 2 — Automated Design Token Validation | `training/design/exercises/exercise-2.md` |
| Exercise 3 — Component Specification Compiling | `training/design/exercises/exercise-3.md` |
| Exercise 4 — Production Asset Pack Optimization | `training/design/exercises/exercise-4.md` |
| Exercise 5 — Capstone: Design-to-Code Pipeline | `training/design/exercises/exercise-5.md` |
| svg-auditor skill | `skills/svg-auditor/SKILL.md` |
| design-token-validator skill | `skills/design-token-validator/SKILL.md` |
| component-spec-compiler skill | `skills/component-spec-compiler/SKILL.md` |
| asset-pack-optimizer skill | `skills/asset-pack-optimizer/SKILL.md` |
| brand-guardrails skill | `../christine/skills/brand-guardrails/SKILL.md` |

---

## Success Criteria

The Design team can independently:

- [ ] Interrogate the design Domain NotebookLM to establish asset validation baselines before writing audit scripts
- [ ] Parse raw SVG XML elements and flag broken paths, missing viewBox attributes, and non-standard inline styling using the svg-auditor skill
- [ ] Read and parse structured JSON design token files, verifying hex codes, font scale values, and spacing variables using the design-token-validator skill
- [ ] Convert raw layout coordinates, dimensions, and visual properties into CSS custom properties and platform-agnostic style dictionaries using the component-spec-compiler skill
- [ ] Programmatically clean, compress, strip metadata from, and organize visual assets into production-ready folder trees using the asset-pack-optimizer skill
- [ ] Run an end-to-end design-to-code pipeline that ingests raw asset dumps, executes compliance checks, compiles theme specifications, and packages an optimized asset library for developer handoff
