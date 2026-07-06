# Exercise 2 — Automated Design Token Validation

## Scenario

The Design team maintains two token files — a JSON global schema (`design-tokens.json`) and a CSS component token file (`component-tokens.css`). Before the sprint handoff to engineering, every token must be validated against the brand's approved color palette, spacing modular scale, and typography typefaces. Broken references and deprecated naming conventions must be caught and corrected.

## Learning Objectives

- Upload and parse structured JSON and CSS design token files in the Weatherman AI Portal
- Build prompt workflows for systematic token-by-token validation
- Verify hex color codes against an approved brand palette
- Validate spacing values against a modular scale
- Resolve token references and flag broken or circular dependency chains
- Identify missing required tokens and deprecated naming patterns

## Dataset

Open the Weatherman AI Portal in your browser. Select **"Paula & Gaby"** from the sidebar dropdown. Use the paperclip icon to upload the two token files from `data/mock-assets/`.

| File | Description |
|---|---|
| `design-tokens.json` | Global token schema with color, spacing, typography, shadow, and component tokens |
| `component-tokens.css` | Component-level CSS custom properties referencing global tokens |

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

### Approved Font Sizes (px)

`10, 12, 14, 16, 18, 20, 24, 32, 40, 48, 64`

### Known Issues Planted in the Data

| Issue | Location | Notes |
|---|---|---|
| Wrong brand primary | `design-tokens.json` | `#1A7DB8` instead of approved `#1A6FB0` |
| Missing from approved palette | `design-tokens.json` | `#E85D3A` is not a brand color |
| Inconsistent hex format | `design-tokens.json` | `#222` (3-char) instead of `#222222` |
| Off-scale spacing | `design-tokens.json` | `--spacing-md: 18px` — not on modular scale |
| Non-brand font | `design-tokens.json` | `'Comic Sans MS', serif` — not approved |
| Broken reference | `design-tokens.json` | `{color.border.default}` does not exist |
| Missing required tokens | `design-tokens.json` | No `--color-semantic-success`, no `--shadow-card` |
| Deprecated naming | `component-tokens.css` | `--color-cta-*` should be `--color-button-*` |
| Undefined var reference | `component-tokens.css` | `var(--color-semantic-warning)` is not defined anywhere |
| Hardcoded value instead of token | `component-tokens.css` | `--card-shadow: 0 2px 4px rgba(...)` should reference shadow token |

## Walkthrough

### Step 1 — Upload token files and run the design-token-validator workspace preset

Open the Weatherman AI Portal in your browser. Select **"Paula & Gaby"** from the sidebar dropdown. Click the paperclip icon and upload both token files. Then paste the design-token-validator system prompt (from `presets/design-token-validator/SKILL.md`) into the chat input first to configure the AI.

Type this prompt:

```
Load both token files and run a structural audit:

1. Does design-tokens.json have all required top-level categories
   (color, spacing, typography, shadow)? Flag any missing.

2. Does component-tokens.css use consistent kebab-case naming?

3. Count total tokens across both files and output a structure summary:
   file, categories_found, token_count, missing_categories, naming_issues
```

### Step 2 — Validate all color tokens

Type this prompt (continuing the same session):

```
Validate every color token against this approved palette:

#1A6FB0 (brand-primary)   #2A9D8F (brand-secondary)   #F4A261 (accent)
#264653 (text-primary)     #E9C46A (highlight)          #FFFFFF (white)
#F5F5F5 (bg-light)         #333333 (text-secondary)

For each color token in design-tokens.json:
1. Report the current value.
2. If it matches a palette color exactly → Pass.
3. If it's close but different hex → suggest the correct palette value.
4. If it's not in the palette at all → flag as non-brand (HIGH).
5. Check hex format: must be 6-char lowercase. Flag #222 as wrong format.

Also scan component-tokens.css for any hardcoded color values that
should reference a token variable instead.

Output columns: token_name, current_value, expected_value, status, action
```

### Step 3 — Validate typography and spacing

Type this prompt (continuing the session):

```
Validate typography and spacing against brand standards:

1. SPACING — Approved scale (px): 4, 8, 12, 16, 24, 32, 48, 64, 96
   - Check every spacing value in design-tokens.json.
   - Flag 18px as off-scale; suggest nearest scale value (16 or 24).
   - If any value uses em or rem when px is expected, flag as warning.

2. TYPOGRAPHY — Approved typefaces:
   - Inter (body copy)
   - Plus Jakarta Sans (headings)
   - JetBrains Mono (monospace)
   - Flag 'Comic Sans MS', serif as non-brand.
   - Suggest the correct brand typeface.

3. FONT SIZES — Approved scale (px): 10, 12, 14, 16, 18, 20, 24, 32, 40, 48, 64
   - Check every font-size value.
   - Flag any value not on the scale.

Output: category, token_name, value, issue, suggestion
```

### Step 4 — Resolve token references

Type this prompt (continuing the session):

```
Resolve all token references across both files:

1. In design-tokens.json, find {color.border.default} referenced by
   component.card.border. Does color.border.default exist anywhere in
   the token tree? If not, suggest the correct path.

2. Check {color.brand.primary} referenced by component.button.background.
   Does color → brand → primary exist? What is its value?

3. In component-tokens.css, find var(--color-semantic-warning).
   Is this token defined anywhere in either file? If not, flag as
   undefined reference (HIGH severity).

4. Check var(--color-cta-background) and var(--color-cta-text):
   Are these still valid or are they deprecated? If deprecated, suggest
   the new --color-button-* equivalents.

5. Check for circular references (A → B → A). Flag if found.

Output: file, reference, resolves_to, status (ok/broken/deprecated), suggested_fix
```

### Step 5 — Fix token issues and write corrected files

Type this prompt (continuing the session):

```
Fix all the issues found:

1. Correct color values to match the approved palette:
   - #1A7DB8 → #1A6FB0
   - #E85D3A → nearest palette color or remove
   - #222 → #222222

2. Fix spacing: 18px → 16px (nearest approved scale value).

3. Fix typography: 'Comic Sans MS', serif → 'Inter', sans-serif.

4. Fix broken references:
   - {color.border.default} → {color.text.secondary}
   - var(--color-semantic-warning) is undefined; define it or replace
     with var(--color-accent)

5. Rename deprecated tokens:
   - --color-cta-background → --color-button-primary-bg
   - --color-cta-text → --color-button-primary-text

6. Add missing required tokens:
   - --color-semantic-success: #2A9D8F
   - --shadow-card: 0 2px 8px rgba(0,0,0,0.1)

Write the corrected files as design-tokens-fixed.json and
component-tokens-fixed.css.

After fixes, confirm: do all var(--...) references resolve to a
defined token? Show a cross-reference verification table.
```

### Step 6 — Export the token audit report

Type this prompt (continuing the session):

```
Write token_audit_report.csv with all issues found.
Columns: token_name, category, current_value, issue, severity, suggested_fix

Print a summary:

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

## Expected Output

After completing all steps, you should have:

- A color validation table with palette cross-reference results
- Spacing and typography values corrected to brand standards
- All broken token references resolved
- Deprecated naming conventions updated to current patterns
- Missing required tokens added
- Corrected files: `design-tokens-fixed.json` and `component-tokens-fixed.css` (downloadable via the portal)
- A `token_audit_report.csv` documenting every issue and fix
- Practical experience running the `design-token-validator` workspace preset
