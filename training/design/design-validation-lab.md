# 🎯 Design Validation Lab: Guide & Guardrails

Welcome to the Design Validation Lab. Before you execute any automated terminal audits using your local agent, use this document alongside **NotebookLM (The Oracle)** to verify your constraints and catch the planted grading traps.

---

## 🎨 1. Brand Palette & Token Governance

### Approved Primary Brand Color
* **Primary Hex:** `#1A6FB0`

### 🛑 Color Traps to Flag
* **Incorrect Variant:** `#1A7DB8` (Close, but unapproved)
* **Unapproved Red:** `#E85D3A`
* **Format Violation:** 3-character hex shorthand (e.g., `#222`) must be expanded to strict 6-character hex (`#222222`).

### 📐 Naming Conventions & Requirements
* **Deprecated Patterns:** Legacy naming like `--color-cta-*` must be migrated to `--color-button-*`.
* **Required System Tokens:** Ensure `--color-semantic-success`, `--color-semantic-warning`, `--color-primary`, and `--shadow-card` are fully defined.

---

## 🛠️ 2. Exercise 1: SVG Structural Audit

You are required to inspect the raw XML structure of the three mock assets and resolve the following structural, canvas, and accessibility flaws:

### 📐 Canvas & ViewBox Integrity
* **`icon-cloud-sync.svg`:** ViewBox is non-integer (`0 0 24.5 24.5`), causing sub-pixel rendering risks. Correct to integer scale.
* **`logo-hero-main.svg`:** Completely missing its `viewBox` attribute. Derive it from the hardcoded width/height.

### 🛑 Styling, Editor Metadata, & Redundancies
* **Hardcoded Colors:** Strip unapproved hardcoded values (`#0066cc` in cloud icon; `#FF0000` in main logo) and replace with `var(--...)` tokens or `currentColor`.
* **Joke Hex Codes:** Clean out joke colors (`#C0FFEE` and `#BADA55`) hidden inside `illustration-dashboard.svg`.
* **Hardcoded Typography:** `illustration-dashboard.svg` uses `font-family="Arial"`. Correct this to use an approved brand token.
* **Metadata & Unused Elements:** Strip Inkscape editor metadata (`sodipodi:namedview`, `inkscape:*`), legacy headers (`xml:space="preserve"`, `version="1.1"`), and the unreferenced `#unusedGradient` block in the logo.
* **Path Optimization:** `illustration-dashboard.svg` features a redundant, overly complex path command count requiring minification.

### ♿ Accessibility (A11y) Compliance
* **Missing Elements:** `icon-cloud-sync.svg` completely lacks `<title>` and `<desc>`.
* **Empty Elements:** `illustration-dashboard.svg` contains an empty `<desc></desc>` block.
* **Required Injections:** Every asset must feature clear, descriptive `<title>` and `<desc>` fields along with `role="img"` on the root tag.

---

## ⚡ 3. Exercise 2: CSS & Token Hidden Traps

When parsing `design-tokens.json` and `component-tokens.css`, enforce strict validation rules to catch these intentional environment breaks:

### 📏 Typography & Spacing Scales
* **Modular Spacing Scale:** Values must strictly follow the pixel sequence: `4, 8, 12, 16, 24, 32, 48, 64, 96`. 
  * *Trap:* Watch out for `--spacing-md: 18px` (falls off the scale).
* **Approved Font Sizes:** Typography must fall on: `10, 12, 14, 16, 18, 20, 24, 32, 40, 48, 64`.
* **Typeface Trap:** Flag and eliminate references to `'Comic Sans MS', serif`.

### 🔗 Reference & Dependency Breaks
* **Broken JSON Paths:** Locate and fix `{color.border.default}`, which points to a non-existent dependency path.
* **Undefined Variables:** The CSS tokens reference `var(--color-semantic-warning)`, but the variable is completely undefined in the environment.
* **Hardcoded Values:** Break down hardcoded shadow definitions like `--card-shadow: 0 2px 4px rgba(...)` and map them directly to a system token.
* **Missing Baseline Tokens:** Identify and insert the missing `--color-semantic-success` and `--shadow-card` tokens.