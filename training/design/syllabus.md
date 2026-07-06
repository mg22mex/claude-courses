# Design: SVG Auditing, Design Tokens & Asset Management

**Course Title:** SVG Auditing, Design Tokens & Asset Management
**Target User:** Design team (Paula & Gaby)
**Prerequisites:** Familiarity with SVG files, design tokens, and basic file management; no coding experience required.
**Estimated Duration:** 5 hours (split across five 1-hour sessions)
**Format:** Live walkthrough + hands-on portal exercises

---

## Pre-Work: Load Your Institutional Memory

Before starting this course, open the [Master Guide Notebook](https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1) alongside your domain-specific NotebookLM notebook. Query both notebooks to understand how the system operates in your domain before building any prompts or tools.

**Your Domain Notebook:** [Design Team Notebook](https://notebooklm.google.com/notebook/9f67d0db-49c8-4bc3-b2e5-f08a3528028f?authuser=1)

> **Workflow Rule:** All prompt generation, data testing, or document templating in this track must cross-verify patterns against both the Master Guide and your Domain Notebook before proceeding.

---

## Learning Objectives

By the end of this course, the Design team will be able to:

1. Interrogate the design Domain NotebookLM to establish strict asset validation baselines before building any audit prompts.
2. Parse raw SVG XML elements and flag broken paths, missing viewBox attributes, and non-standard inline styling using the svg-auditor workspace preset.
3. Read and parse structured JSON design token files, verifying hex codes, font scale values, and spacing variables against the approved master system using the design-token-validator workspace preset.
4. Convert raw layout coordinates, dimensions, and visual properties into CSS custom properties and platform-agnostic style dictionaries using the component-spec-compiler workspace preset.
5. Programmatically clean, compress, strip metadata from, and organize batches of visual assets into production-ready folder trees using the asset-pack-optimizer workspace preset.
6. Run an end-to-end design-to-code pipeline that ingests raw asset dumps, executes compliance checks, compiles theme specifications, and packages an optimized asset library for developer handoff.

---

## Lesson Breakdown

### Lesson 1 — SVG Structural Auditing (60 min)

**Objective:** Interrogate the design Domain NotebookLM to establish strict asset validation baselines, then use the portal AI to parse raw SVG XML elements and flag broken paths, missing viewBox attributes, and non-standard inline styling.

| Segment | Topic | Activity |
|---|---|---|
| 1.1 | Loading the Domain Notebook | Open the Design NotebookLM and query for SVG validation baselines, brand color standards, and accessibility requirements before building any audit prompts. |
| 1.2 | Loading SVG files into the portal | Open the Weatherman AI Portal, select "Paula & Gaby" from the sidebar dropdown, and upload three sample SVGs using the paperclip icon. |
| 1.3 | Running the svg-auditor workspace preset | Paste the svg-auditor system prompt into the portal chat input, then instruct the AI to scan all three SVGs for viewBox, color governance, accessibility, and path redundancy. |
| 1.4 | Parsing viewBox and canvas issues | Review flagged viewBox problems: missing viewBox, non-integer values, incorrect aspect ratios. |
| 1.5 | Tokenizing colors and stripping metadata | Replace hardcoded colors with `var(--...)` tokens. Strip editor metadata (sodipodi, inkscape, xml:space). |

**Lab:** `exercises/exercise-1.md` — SVG Structural Auditing

---

### Lesson 2 — Automated Design Token Validation (60 min)

**Objective:** Build prompt workflows to read and parse structured JSON design token files, verifying that hex codes, font scale values, and spacing variables match the approved master system.

| Segment | Topic | Activity |
|---|---|---|
| 2.1 | The token management problem | Design token files accumulate drift. The portal AI can diff token values against a spec and flag every inconsistency. |
| 2.2 | Loading token files | Upload `design-tokens.json` and `component-tokens.css` into the portal chat using the paperclip icon. |
| 2.3 | Running the design-token-validator workspace preset | Paste the design-token-validator system prompt into the chat input, then instruct the AI to validate all tokens. |
| 2.4 | Color and spacing validation | Review flagged color values outside the approved palette, inconsistent hex formats, and spacing values off the modular scale. |
| 2.5 | Token reference resolution and missing tokens | Identify broken `{reference}` paths and missing required tokens. |

**Lab:** `exercises/exercise-2.md` — Automated Design Token Validation

---

### Lesson 3 — Component Specification Compiling (60 min)

**Objective:** Leverage the `component-spec-compiler` workspace preset to systematically convert raw layout coordinates, dimensions, and visual properties into uniform CSS custom properties and platform-agnostic style dictionaries.

| Segment | Topic | Activity |
|---|---|---|
| 3.1 | The spec-to-code gap | Designers produce pixel specs in Figma. Engineers need CSS variables and token files. The portal AI automates the conversion. |
| 3.2 | Loading a design spec | Paste a structured component spec with color swatches, type scale, spacing grid, and button anatomy into the chat input. |
| 3.3 | Generating CSS custom properties | Instruct the AI to convert the spec into namespaced `--color-*`, `--typography-*`, `--spacing-*`, and `--radius-*` variables. |
| 3.4 | Building a Style Dictionary JSON | Instruct the AI to generate a platform-agnostic JSON token file following the `{value, type}` format with category groupings. |
| 3.5 | Component-specific token blocks | For component anatomy specs (button system), generate self-contained component token blocks referencing global variables. |

**Lab:** `exercises/exercise-3.md` — Component Specification Compiling

---

### Lesson 4 — Production Asset Pack Optimization (60 min)

**Objective:** Use the `asset-pack-optimizer` workspace preset to programmatically clean, compress, strip metadata from, and organize batches of visual assets into strict production-ready folder trees.

| Segment | Topic | Activity |
|---|---|---|
| 4.1 | The asset handoff problem | Raw SVG exports contain editor metadata, non-standard filenames, and bloated path data. Engineering needs clean, optimized assets. |
| 4.2 | Scanning and classifying an asset directory | Upload the mock-assets folder into the portal chat and instruct the AI to classify every file by type. |
| 4.3 | SVG path minification and metadata stripping | For each SVG: remove Inkscape/Sodipodi metadata, empty groups, redundant attributes. Normalize viewBox and inject accessibility tags. |
| 4.4 | Naming convention enforcement | Instruct the AI to audit all filenames for kebab-case compliance and fix violations. |
| 4.5 | Distribution packaging | Instruct the AI to generate a `dist/` directory with organized subdirectories (icons/filled, icons/outlined, illustrations, tokens) and a manifest CSV. |

**Lab:** `exercises/exercise-4.md` — Production Asset Pack Optimization

---

### Lesson 5 — Capstone: The Automated Design-to-Code Pipeline (60 min)

**Objective:** An end-to-end laboratory where the Design team ingests a raw, messy creative asset dump, executes automated compliance checks, compiles theme specifications, and packages a perfectly optimized asset library for direct developer hand-off.

| Segment | Topic | Activity |
|---|---|---|
| 5.1 | The complete handoff workflow | Engineering needs verified SVGs, validated tokens, compiled style dictionaries, and an organized package. One portal session can deliver all four. |
| 5.2 | SVG audit + token validation pipeline | Run svg-auditor and design-token-validator in sequence; cross-reference findings (token colors feed into SVG fixes). |
| 5.3 | Component spec compilation | Compile the dashboard redesign spec into CSS variables and Style Dictionary JSON. |
| 5.4 | Asset optimization and packaging | Run asset-pack-optimizer on all corrected files; produce `dist/` with manifest and rename log. |
| 5.5 | Consolidated handoff report | Generate a single engineering handoff report with quality gate results and recommendations. |

**Lab:** `exercises/exercise-5.md` — Capstone: The Automated Design-to-Code Pipeline

---

## Sample Data Files

The following sample files are provided in `data/mock-assets/` for use during exercises:

| File | Description |
|---|---|
| `icon-cloud-sync.svg` | Icon SVG (24x24) with missing accessibility tags, hardcoded color, and non-integer viewBox |
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
| svg-auditor workspace preset | `presets/svg-auditor/SKILL.md` |
| design-token-validator workspace preset | `presets/design-token-validator/SKILL.md` |
| component-spec-compiler workspace preset | `presets/component-spec-compiler/SKILL.md` |
| asset-pack-optimizer workspace preset | `presets/asset-pack-optimizer/SKILL.md` |
| brand-guardrails workspace preset | `../christine/presets/brand-guardrails/SKILL.md` |

---

## Success Criteria

The Design team can independently:

- [ ] Interrogate the design Domain NotebookLM to establish asset validation baselines before building audit prompts
- [ ] Parse raw SVG XML elements and flag broken paths, missing viewBox attributes, and non-standard inline styling using the svg-auditor workspace preset
- [ ] Read and parse structured JSON design token files, verifying hex codes, font scale values, and spacing variables using the design-token-validator workspace preset
- [ ] Convert raw layout coordinates, dimensions, and visual properties into CSS custom properties and platform-agnostic style dictionaries using the component-spec-compiler workspace preset
- [ ] Programmatically clean, compress, strip metadata from, and organize visual assets into production-ready folder trees using the asset-pack-optimizer workspace preset
- [ ] Run an end-to-end design-to-code pipeline that ingests raw asset dumps, executes compliance checks, compiles theme specifications, and packages an optimized asset library for developer handoff

---

### High-Impact Operational Presets

**1. Custom Corporate Gift Structural Conceptor** — visual, material, and packaging concepts for luxury gifting sets.  
**2. Vending Machine Packaging Designer** — sleek cardboard unboxing aesthetics for automated retail (airports).  
**3. Lifestyle Photography Asset Director** — lighting, environment, and styling directions for retail photo sheets.  
**4. Product Carousel Asset Visual Descriptive Assistant** — alt-text, layout concepts, and graphics for web production.  
**5. Custom Print Mockup Specification Builder** — translating logo files into precise placement/dimensions for manufacturing vectors.
