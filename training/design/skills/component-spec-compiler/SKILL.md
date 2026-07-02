---
name: component-spec-compiler
description: Convert Figma styling guidelines, typography matrices, and border dimensions into clean CSS variables and uniform style dictionaries for web and mobile.
---

# component-spec-compiler

A systematic blueprint for translating visual design specifications into code-ready style tokens. This skill ingests Figma-style layout specs, color matrices, typography scales, and border/shadow definitions, and produces structured CSS custom properties and JSON style dictionaries. Run this whenever the Design team needs to hand off pixel-perfect component specs to engineering.

---

## 1. Intake & Spec Schema

### 1.1 Accept input formats

- **`.md` / `.txt`** — Structured design spec documents (color swatches, type scales, spacing grids, border radii)
- **`.json` / `.css`** — Existing token files to be updated or cross-referenced
- **Free-form prompt** — Describe the component library (button system, card grid, form fields) when no spec file is available

### 1.2 Spec categories

Classify the incoming spec into one or more categories:

| Category | Description | Output Target |
|---|---|---|
| Color palette | Hex/rgba swatches for backgrounds, text, borders, states | CSS custom properties, JSON color tokens |
| Typography matrix | Font family, weight, size, line height, letter spacing per level | CSS typography classes, JSON type tokens |
| Spacing grid | Padding, margin, gap values (4px base scale or custom) | CSS spacing properties, JSON spacing tokens |
| Border & radius | Border width, style, color per variant; corner radii | CSS border tokens |
| Shadow & elevation | Box shadow values per elevation level (0–4+) | CSS shadow tokens |
| Component anatomy | Specific component layout (e.g., button: pad, font, border, state colors) | Complete component token set |

### 1.3 Validate spec completeness

Check that the spec includes:

- Minimum viable values per category
- State variants for interactive components (default, hover, active, disabled, focus)
- Responsive breakpoints if layout is viewport-dependent
- Dark mode values if applicable

Flag any missing required values — prompt the designer to fill gaps before generating code.

---

## 2. Token Generation Engine

### 2.1 CSS custom properties

Generate clean, namespaced `--category-property-variant` variables:

```css
/* Color palette */
--color-primary-default: #1A6FB0;
--color-primary-hover: #155892;
--color-primary-active: #104273;
--color-primary-disabled: #A0C4E8;

--color-text-primary: #1A1A1A;
--color-text-secondary: #666666;
--color-text-disabled: #AAAAAA;

--color-bg-primary: #FFFFFF;
--color-bg-secondary: #F5F7FA;
--color-bg-disabled: #E8E8E8;

--color-border-default: #D0D5DD;
--color-border-focus: #1A6FB0;
--color-border-error: #D92D20;

/* Typography */
--typography-font-family-primary: 'Inter', -apple-system, sans-serif;
--typography-font-family-mono: 'JetBrains Mono', monospace;
--typography-h1-size: 32px;
--typography-h1-weight: 700;
--typography-h1-line-height: 1.25;
--typography-h1-letter-spacing: -0.02em;

/* Spacing */
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
--spacing-xxl: 48px;

/* Border radius */
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-full: 9999px;

/* Shadows */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);
```

### 2.2 JSON style dictionary

Generate a platform-agnostic token file following the Style Dictionary format:

```json
{
  "color": {
    "primary": {
      "default": { "value": "#1A6FB0", "type": "color" },
      "hover":   { "value": "#155892", "type": "color" },
      "active":  { "value": "#104273", "type": "color" },
      "disabled":{ "value": "#A0C4E8", "type": "color" }
    }
  },
  "typography": {
    "h1": {
      "fontFamily": { "value": "Inter", "type": "string" },
      "fontSize":   { "value": "32px",  "type": "dimension" },
      "fontWeight": { "value": "700",   "type": "number" }
    }
  },
  "spacing": {
    "md": { "value": "16px", "type": "dimension" }
  }
}
```

### 2.3 Component-specific tokens

For component anatomy specs, generate a self-contained block:

```css
/* Button component tokens */
--button-primary-bg-default: var(--color-primary-default);
--button-primary-bg-hover: var(--color-primary-hover);
--button-primary-text: #FFFFFF;
--button-primary-border-default: transparent;
--button-primary-padding: var(--spacing-sm) var(--spacing-lg);
--button-primary-font: var(--typography-font-family-primary);
--button-primary-font-size: 14px;
--button-primary-radius: var(--radius-md);
```

---

## 3. Spec-to-Output Rules

### 3.1 Naming conventions

- All tokens use `--category-property-modifier` kebab-case format
- Component tokens use `--component-property-modifier` pattern
- Boolean states (hover, active, disabled, focus) are always the last modifier
- Never use camelCase or snake_case in CSS token names

### 3.2 Units

- All spacing values MUST be in px (not rem, em, or %)
- Font sizes in px (not pt)
- Line heights unitless (1.25, 1.5)
- Letter spacing in em
- Border widths in px
- Shadow spread/blur in px

### 3.3 Color format

- Always output hex for solid colors: `#RRGGBB`
- Always output `rgba()` for colors with opacity
- Never output named colors (`red`, `blue`) or shorthand hex (`#333`)

---

## 4. Output & Reporting

### 4.1 Generated files

Write to the working directory:

| File | Content |
|---|---|
| `component-tokens-output.css` | All CSS custom properties with category groups and comments |
| `style-dictionary-output.json` | Platform-agnostic JSON token file |
| `component-tokens-{component}.css` | Component-specific token block (if component anatomy was provided) |

### 4.2 Terminal summary

```
=== COMPONENT SPEC COMPILER SUMMARY ===
Source spec:            button-system-spec.md

Tokens generated:
  Color:                12 variables (4 states × 3 categories)
  Typography:           20 variables (4 levels × 5 properties)
  Spacing:               8 variables (8-step scale)
  Border & Radius:       8 variables (4 radii + 4 border styles)
  Shadow:                4 variables (4 elevation levels)
  Component (button):   12 variables

Files written:
  ✅ component-tokens-output.css
  ✅ style-dictionary-output.json
  ✅ component-tokens-button.css

Status:                 Ready for engineering handoff
```

### 4.3 Cross-reference verification

After generation, cross-check:

- Do all `var(--...)` references in component tokens resolve to a defined variable?
- Are there naming conflicts or duplicates?
- Do mobile platform constraints differ (e.g., React Native uses `fontSize` not `font-size`)?
- If mobile output requested, generate a separate React Native `StyleSheet` export

---

## 5. Strictness Rules

| # | Rule | Enforcement |
|---|---|---|
| 1 | Every generated token MUST be in kebab-case format | Hard block |
| 2 | All spacing values MUST be in px, never rem/em | Hard block |
| 3 | Every `var(--...)` reference in component tokens MUST resolve to a defined variable | Hard block |
| 4 | Color output MUST use hex (`#RRGGBB`) for solids and `rgba()` for opacities | Hard block |
| 5 | Component tokens MUST include states (hover, active, disabled, focus) | Warning |
| 6 | Generated CSS MUST include category header comments (`/* Color */`, `/* Typography */`) | Warning |
| 7 | Style Dictionary JSON MUST use the `value`, `type` structure | Warning |

---

## 6. Edge Cases

| # | Scenario | Handling |
|---|---|---|
| 1 | Spec contains only hex colors without named categories | Infer category from context (backgrounds, text, borders); flag as auto-categorized |
| 2 | Typography matrix has inconsistent line-height values across levels | Normalize to nearest 0.25 increment; flag the adjustment |
| 3 | Spacing values don't follow a recognizable scale | Generate as-is but flag that no modular scale was detected |
| 4 | Spec has conflicting values (two different primary blues) | Flag both; ask designer to confirm which is canonical |
| 5 | Component anatomy references a category that wasn't provided (e.g., shadow missing) | Generate the component tokens with `TBD` placeholders; flag as incomplete |
| 6 | Spec includes responsive breakpoints without values | Flag; omit breakpoints from output |
| 7 | Dark mode values provided for some but not all tokens | Generate what exists; flag incomplete dark mode coverage |
