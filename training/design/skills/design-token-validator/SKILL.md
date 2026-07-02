---
name: design-token-validator
description: Validate CSS custom properties and JSON design token files against a brand design system — check color values against an approved palette, spacing against a modular scale, resolve token references, and flag missing or deprecated tokens.
---

# design-token-validator

A strict operational playbook for validating design token files — CSS custom properties or JSON token schemas — against a brand design system specification. This skill checks color values against an approved palette, validates spacing against a modular scale, resolves cross-references between tokens, and flags missing required tokens or deprecated naming conventions. Run this whenever the Design team needs to verify token file integrity before pushing to engineering.

---

## 1. Intake & Token Format Detection

### 1.1 Accept input formats

This skill accepts **one or more** input files:

- **`.json`** — JSON token files with structured token categories (e.g., `{ "color": { "brand": { "primary": "#..." } } }`)
- **`.css`** — CSS custom properties files (e.g., `--color-brand-primary: #...;`)
- **`.js` / `.ts`** — JavaScript/TypeScript token export files (auto-detect and parse)

If no files are provided, prompt the designer to supply token files.

### 1.2 Auto-detect format

Inspect each file and classify:

| File extension | Detected format |
|---|---|
| `.json` | JSON token schema |
| `.css` | CSS custom properties |
| `.js` or `.ts` | JS/TS module (attempt to evaluate or extract object) |
| Any other extension | Attempt to parse as JSON first, then CSS, then abort |

### 1.3 Parse and normalize

Normalize all formats to a common internal structure:

| Category | CSS example | JSON example |
|---|---|---|
| Color | `--color-primary: #1A6FB0` | `"color": { "primary": "#1A6FB0" }` |
| Spacing | `--spacing-md: 16px` | `"spacing": { "md": "16px" }` |
| Typography | `--font-body: 'Inter', sans-serif` | `"typography": { "fontBody": "'Inter', sans-serif" }` |
| Shadow | `--shadow-sm: 0 1px 2px rgba(0,0,0,0.05)` | `"shadow": { "sm": "0 1px 2px rgba(0,0,0,0.05)" }` |

---

## 2. Schema & Structural Validation

### 2.1 Required top-level categories

Check that the token file contains all required categories:

| Category | Required? |
|---|---|
| `color` | Yes |
| `spacing` | Yes |
| `typography` | Yes |
| `shadow` | Recommended |
| `animation` | Optional |

Any missing required category is flagged as high severity.

### 2.2 Token naming convention

Flag tokens that don't follow the established naming convention:

| Convention | Example |
|---|---|
| kebab-case CSS custom properties | `--color-brand-primary` |
| dot-notation JSON keys | `"color.brand.primary"` |
| Category → subcategory → variant | Three levels deep |

Flag any token name that uses inconsistent separators (underscores, camelCase in CSS), deprecated prefixes (`--btn-` instead of `--button-`), or unclear naming.

---

## 3. Color Token Validation

### 3.1 Approved palette cross-reference

Accept an approved color palette (inline in the prompt or as a separate file). For every color token, check:

| Finding | Severity |
|---|---|
| Value matches a palette color exactly | Pass (allowed) |
| Value is close to a palette color but different hex | Medium — suggest correction |
| Value is not in the palette | High — non-brand color |
| Value is a `var(--...)` reference | Pass (resolves at runtime) |
| Value is a named CSS color (`red`, `blue`) | Medium — should be explicit hex or token |

### 3.2 Hex format consistency

For all hex values, enforce:

- Must be 6 characters (not 3 — `#FFF` → `#FFFFFF`)
- Must be lowercase (not `#1A6FB0` vs `#1a6fb0` — pick one, flag violations)
- No uppercase or mixed case

### 3.3 Deprecated color names

Flag tokens whose names suggest they are deprecated or legacy:

- `--color-cta-*` → should be `--color-button-*`
- `--color-*old*`, `--color-*legacy*`, `--color-*deprecated*`
- `--color-brand-*` that reference retired brand colors

---

## 4. Typography & Spacing Validation

### 4.1 Font stack validation

Check every `font-family` token against the approved brand typefaces:

| Approved typefaces | Example usage |
|---|---|
| Inter | `--font-family-body: 'Inter', sans-serif` |
| Plus Jakarta Sans | `--font-family-heading: 'Plus Jakarta Sans', sans-serif` |
| JetBrains Mono | `--font-family-mono: 'JetBrains Mono', monospace` |

Flag any font not in the approved list. Flag any `font-family` that uses `serif` as fallback when the brand uses `sans-serif`.

### 4.2 Modular spacing scale

Validate spacing values against the brand modular scale:

**Approved scale (px):** 4, 8, 12, 16, 24, 32, 48, 64, 96

| Finding | Severity |
|---|---|
| Value matches a scale step | Pass |
| Value is between scale steps | Medium — suggest nearest step |
| Value is negative | High — negative spacing is usually an error except for `*-negative` tokens |
| Unit is `em` or `rem` where `px` is expected | Low — confirm intent with designer |

### 4.3 Typography scale

If typography size tokens exist, validate against a font-size scale:

**Approved sizes (px):** 10, 12, 14, 16, 18, 20, 24, 32, 40, 48, 64

Flag any font-size value not on the scale.

---

## 5. Token Reference Resolution

### 5.1 Reference syntax detection

Detect token references in all values:

| Format | Example |
|---|---|
| CSS `var()` | `var(--color-brand-primary)` |
| JSON `{reference}` | `{color.brand.primary}` |
| JSON `$ref` | `{ "$ref": "color.brand.primary" }` |

### 5.2 Reference resolution

For every reference found:

1. Extract the referenced token path
2. Search the parsed token tree for the referenced token
3. If the reference resolves to an existing token → Pass
4. If the reference does not resolve → High severity (broken reference)
5. If the reference creates a circular chain (A → B → A) → High severity

### 5.3 Orphan tokens

Flag tokens that are defined but never referenced by any other token — these may be dead code.

---

## 6. Output & Reporting

### 6.1 Terminal validation table

Print findings in a formatted terminal table:

```
=== DESIGN TOKEN VALIDATION REPORT ===
Files scanned: 2
Tokens scanned: 42

 Category      | Issues | High | Med | Low
───────────────|────────|──────|─────|─────
 Color         |      5 |    2 |   2 |   1
 Spacing       |      2 |    0 |   2 |   0
 Typography    |      1 |    1 |   0 |   0
 Shadow        |      1 |    1 |   0 |   0
 References    |      2 |    2 |   0 |   0
───────────────┴────────┴──────┴─────┴─────
Total issues: 11 (High: 6, Medium: 4, Low: 1)
```

### 6.2 CSV export

If the designer requests a report file, write `token_audit_report.csv` with columns:

```
token_name,category,current_value,issue,severity,suggested_fix
```

### 6.3 Corrected file export

When fixes are applied, write the corrected token file with the same format as the input but with `-fixed` appended to the filename (e.g., `design-tokens-fixed.json`). Include a JSON comment or CSS comment noting the original file name and audit date.

---

## 7. Strictness Rules

1. **Never modify the original token files.** All fixes are written to new files with `-fixed` suffix.
2. **Always show the palette cross-reference.** When flagging colors, show which palette color is closest and what the correct value should be.
3. **Do not guess the approved palette.** If the palette is not loaded alongside the token files, ask the designer to provide it before running color validation.
4. **Broken references block progression.** A broken token reference is always high severity — the file will produce runtime CSS errors or undefined JSON values.
5. **Component tokens depend on global tokens.** If the global token file has issues, flag those first before analyzing component-level token files.
6. **One row per token per issue.** If a single token has multiple issues (wrong color AND wrong format), output separate rows for each.

---

## 8. Edge Cases

| Situation | Response |
|---|---|
| File contains both CSS and JSON syntax in a single file | Abort with "ERROR: Mixed format detected. Provide CSS or JSON files separately." |
| Token value is a gradient or complex color function (`linear-gradient(...)`, `hsl(...)`, `rgba(...)`) | Flag as informational — complex values need manual review for brand compliance |
| Token file has no color tokens at all | Flag as high severity — every design system must define a color palette |
| JSON token uses nested structure 5+ levels deep | Flag as warning — deep nesting reduces readability; suggest flattening to 3 levels |
| CSS custom property is commented out (`/* --color-x: value; */`) | Flag as low severity — commented-out tokens may be unintentionally disabled |
| Token value is `initial`, `inherit`, `unset` | Flag as medium — these are not real values and indicate incomplete token definitions |
| Float value for spacing (e.g., `14.5px`) | Flag as medium — spacing values should be integers |
| Token file is empty (0 bytes or empty object `{}`) | Abort with "ERROR: Token file is empty" |
| Reference chain is circular (A → B → C → A) | Flag as high severity — circular reference; suggest removing one link in the chain |
| Same token defined twice with different values | Flag as high severity — duplicate definition; last value wins but intent is ambiguous |
