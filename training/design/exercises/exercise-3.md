# Exercise 3 — Component Specification Compiling

## Scenario

The Figma design team has delivered a structured component spec for a new button system and typography scale. Engineering needs CSS custom properties and a platform-agnostic Style Dictionary JSON file extracted from those specs. The Design team will use the `component-spec-compiler` workspace preset to systematically convert raw layout coordinates, dimensions, and visual properties into uniform CSS variables and a style dictionary.

## Learning Objectives

- Interpret structured design specification documents
- Use the `component-spec-compiler` workspace preset to generate CSS custom properties from raw specs
- Build platform-agnostic Style Dictionary JSON with `{value, type}` format
- Generate component-specific token blocks (button system with states)
- Cross-reference all generated `var(--...)` references to confirm they resolve
- Export both CSS and JSON outputs for engineering handoff

## Dataset

Use the inline design spec below. Open the Weatherman AI Portal, select **"Paula & Gaby"** from the sidebar dropdown, and paste the full spec directly into the chat input.

### Inline Design Spec

```
# Button System — Design Specification

## Color Palette

| Role | Default | Hover | Active | Disabled |
|---|---|---|---|---|
| Primary BG | #1A6FB0 | #155892 | #104273 | #A0C4E8 |
| Secondary BG | #2A9D8F | #21867A | #1A6F65 | #A8D5D0 |
| Text on Primary | #FFFFFF | #FFFFFF | #FFFFFF | #999999 |
| Text on Secondary | #FFFFFF | #FFFFFF | #FFFFFF | #999999 |
| Border | #D0D5DD | #1A6FB0 | #1A6FB0 | #E8E8E8 |
| Danger BG | #D92D20 | #B8261B | #9C1F16 | #F5C6C2 |
| Text on Danger | #FFFFFF | #FFFFFF | #FFFFFF | #999999 |

## Typography

| Element | Font Family | Size | Weight | Line Height | Letter Spacing |
|---|---|---|---|---|---|
| H1 | Plus Jakarta Sans | 32px | 700 | 1.25 | -0.02em |
| H2 | Plus Jakarta Sans | 24px | 700 | 1.3 | -0.01em |
| H3 | Plus Jakarta Sans | 20px | 600 | 1.35 | 0 |
| Body | Inter | 16px | 400 | 1.5 | 0 |
| Body Small | Inter | 14px | 400 | 1.5 | 0 |
| Button Label | Inter | 14px | 600 | 1.25 | 0.01em |
| Caption | Inter | 12px | 400 | 1.4 | 0 |
| Mono | JetBrains Mono | 14px | 400 | 1.5 | 0 |

## Spacing (4px Base Scale)

| Token | Value |
|---|---|
| xs | 4px |
| sm | 8px |
| md | 16px |
| lg | 24px |
| xl | 32px |
| xxl | 48px |

## Border Radius

| Token | Value |
|---|---|
| sm | 4px |
| md | 8px |
| lg | 12px |
| full | 9999px |

## Shadow / Elevation

| Level | Value |
|---|---|
| sm | 0 1px 2px rgba(0,0,0,0.05) |
| md | 0 4px 6px rgba(0,0,0,0.07) |
| lg | 0 10px 15px rgba(0,0,0,0.10) |
| xl | 0 20px 25px rgba(0,0,0,0.15) |

## Button Anatomy

- Padding: sm (8px) horizontal, xs (4px) vertical — increased to
  sm (8px) vertical for large variant
- Border: 1px solid for secondary/outline, transparent for primary/danger
- Border radius: md (8px)
- Font: Button Label typography settings
- Min width: 80px (small), 120px (default), 160px (large)
- Height: 32px (small), 40px (default), 48px (large)
```

### Known Issues Planted in the Data

| Issue | Notes |
|---|---|
| Inconsistent letter spacing | H1 uses `-0.02em`, H2 uses `-0.01em`, H3 has `0` — verify against brand standards |
| Missing dark mode | No dark mode color values provided — only light mode |
| No responsive breakpoints | Spec does not define how tokens change at different viewports |
| Button anatomy references global tokens | Padding values are semantic names (sm, xs) — must resolve to actual px values |

## Walkthrough

### Step 1 — Review the component-spec-compiler workspace preset

Open the Weatherman AI Portal in your browser. Select **"Paula & Gaby"** from the sidebar dropdown. Paste the component-spec-compiler system prompt (from `presets/component-spec-compiler/SKILL.md`) into the chat input to configure the AI.

Type this prompt:

```
Read the component-spec-compiler preset definition and summarize:
- What input formats does it accept?
- What output files does it generate?
- What naming conventions does it enforce?
- What are the hard-block strictness rules?
```

### Step 2 — Load the design spec and run the preset

Type this prompt:

```
Run the component-spec-compiler preset. Here is the design spec:

COLOR PALETTE
- Primary: default #1A6FB0, hover #155892, active #104273, disabled #A0C4E8
- Secondary: default #2A9D8F, hover #21867A, active #1A6F65, disabled #A8D5D0
- Text on primary: #FFFFFF (all states except disabled: #999999)
- Text on secondary: #FFFFFF (all states except disabled: #999999)
- Border: default #D0D5DD, focus/hover #1A6FB0, disabled #E8E8E8
- Danger: default #D92D20, hover #B8261B, active #9C1F16, disabled #F5C6C2
- Text on danger: #FFFFFF (all states except disabled: #999999)

TYPOGRAPHY — see the full type scale in the spec above.

SPACING (4px base): xs=4px, sm=8px, md=16px, lg=24px, xl=32px, xxl=48px

BORDER RADIUS: sm=4px, md=8px, lg=12px, full=9999px

SHADOWS: sm/md/lg/xl as defined above.

BUTTON ANATOMY:
- 3 sizes: small (32px h, 80px min-w), default (40px h, 120px min-w),
  large (48px h, 160px min-w)
- 4 variants: primary, secondary, danger, outline
- 5 states per variant: default, hover, active, disabled, focus
- Padding: horizontal sm (8px), vertical xs (4px), large vertical sm (8px)
- Border radius: md (8px)
- Font: Button Label typography

Generate:
1. CSS custom properties (component-tokens-output.css)
2. JSON Style Dictionary (style-dictionary-output.json)
3. Component-specific button tokens (component-tokens-button.css)
```

### Step 3 — Generate CSS custom properties

Type this prompt (continuing the session):

```
Generate the CSS custom properties file with these sections:

1. /* Color palette */
   - Naming: --color-{role}-{state}
   - Example: --color-primary-default, --color-primary-hover

2. /* Typography */
   - Naming: --typography-{element}-{property}
   - Example: --typography-h1-size, --typography-body-font-family

3. /* Spacing */
   - Naming: --spacing-{token}
   - Example: --spacing-xs, --spacing-md

4. /* Border radius */
   - Naming: --radius-{token}
   - Example: --radius-sm, --radius-md

5. /* Shadows */
   - Naming: --shadow-{level}
   - Example: --shadow-sm, --shadow-lg

All values must match the spec exactly. All hex in 6-char lowercase.
All spacing in px. Line heights unitless.
```

### Step 4 — Generate the Style Dictionary JSON

Type this prompt (continuing the session):

```
Now generate a Style Dictionary JSON file with:

Required structure:
{
  "color": {
    "primary": {
      "default": { "value": "#1A6FB0", "type": "color" },
      ...
    }
  },
  "typography": { ... },
  "spacing": { ... },
  "borderRadius": { ... },
  "shadow": { ... }
}

Rules:
- Nested structure by category, 3 levels deep max
- Each token has "value" and "type" fields
- Types: color, dimension, number, string
- Raw values only — no var(--...) references in the JSON
```

### Step 5 — Generate component-specific button tokens

Type this prompt (continuing the session):

```
Using the generated CSS variables, create component-specific button tokens.

Naming convention: --button-{variant}-{property}-{state}

Required coverage per variant (primary, secondary, danger, outline):

| Property | States per variant |
|---|---|
| bg | default, hover, active, disabled |
| text | default, hover, active, disabled |
| border | default, hover, active, disabled, focus |
| radius | single value per variant |
| padding | single value per variant |

Plus global button tokens (shared across variants):
- --button-font-family
- --button-font-size
- --button-font-weight
- --button-small-height, --button-default-height, --button-large-height
- --button-small-min-width, --button-default-min-width, --button-large-min-width

Cross-reference verification: After generating the block, confirm that
every var(--...) reference resolves to a variable defined in Step 3.

Output a verification table: component_token, references, resolves (yes/no)
```

### Step 6 — Export and summarize

Type this prompt (continuing the session):

```
Write all generated files:
- component-tokens-output.css
- style-dictionary-output.json
- component-tokens-button.css

Then print a summary:

=== COMPONENT SPEC COMPILER SUMMARY ===
Source spec:            button-system-spec.md

Tokens generated:
  Color:                XX variables (X states x X categories)
  Typography:           XX variables (X levels x X properties)
  Spacing:              X variables (X-step scale)
  Border & Radius:      X variables
  Shadow:               X variables (X elevation levels)
  Component (button):   XX variables

Cross-reference:        All var(--...) resolved: YES/NO
Files written:
  ✅ component-tokens-output.css
  ✅ style-dictionary-output.json
  ✅ component-tokens-button.css

Status:                 Ready for engineering handoff
```

## Expected Output

After completing all steps, you should have:

- A complete CSS custom properties file with color, typography, spacing, border, and shadow sections
- A platform-agnostic Style Dictionary JSON with `{value, type}` format across all categories
- A component-specific button token block covering all 4 variants x 5 states
- A cross-reference verification confirming all `var(--...)` references resolve
- All files downloadable from the portal for engineering handoff
- Practical experience running the `component-spec-compiler` workspace preset for design-to-code handoff
