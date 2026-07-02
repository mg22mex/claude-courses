---
name: asset-pack-optimizer
description: Systematically minify SVG paths, validate filename naming conventions, and organize creative assets into rigid distribution-ready directory maps.
---

# asset-pack-optimizer

A terminal automation utility for preparing design assets for engineering handoff. This skill ingests raw asset directories, minifies SVG path data, enforces kebab-case naming conventions, strips metadata bloat, and produces a structured distribution package. Run this whenever the Design team needs to ship a clean, validated asset pack to development.

---

## 1. Intake & Directory Scan

### 1.1 Accept input

- **Directory path** — A folder containing raw SVG files, icons, illustrations, and raster assets
- **`.csv` / `.txt` inventory file** — Asset manifest with filenames, paths, and expected formats
- **Free-form prompt** — Description of the asset set (e.g., "all icons from the new dashboard design")

### 1.2 Directory classification

Scan the input and classify every file:

| Category | Extensions | Optimization Needed |
|---|---|---|
| SVG icon | `.svg` | Path minification, metadata strip, viewBox normalization |
| SVG illustration | `.svg` | Path minification, metadata strip |
| PNG raster | `.png` | No SVG processing; flag format |
| JPEG raster | `.jpg`, `.jpeg` | No SVG processing; flag format |
| JSON data | `.json` | No processing |
| CSS / SCSS | `.css`, `.scss` | No processing |
| Other | — | List separately |

### 1.3 Filename validation

Check every asset filename against kebab-case rules:

- Lowercase only
- Words separated by hyphens, not underscores or spaces
- No double hyphens
- No trailing hyphens
- Extensions are lowercase
- No version numbers in filename (e.g., `icon-v2.svg` → `icon.svg`)

Flag violations with suggested corrections.

---

## 2. SVG Optimization Engine

### 2.1 Path data minification

Apply the following optimizations to every SVG:

- Remove `xml:space="preserve"` — adds bytes, no rendering effect
- Remove `version="1.1"` — only relevant for legacy editors
- Remove `sodipodi:*` and `inkscape:*` attributes — editor metadata
- Remove `id` attributes — unless used as anchor targets
- Remove empty `<g></g>` groups
- Collapse `<g>` groups that don't apply transforms or styles
- Merge adjacent `<path>` elements where stroke/fill are identical
- Remove redundant `fill-rule="evenodd"` when only one sub-path exists

### 2.2 viewBox normalization

- If viewBox is missing: add `viewBox="0 0 {width} {height}"` using the SVG's width/height attributes
- If viewBox uses non-integer values: round to nearest integer
- If width/height attributes differ from viewBox aspect ratio: flag as potential distortion

### 2.3 Color governance

- Flag any hardcoded fill/stroke colors inside SVG `<path>` or `<circle>` elements
- Replace with `currentColor` if the icon is intended to be themeable
- For multi-color illustrations: replace brand colors with CSS variable references

### 2.4 Accessibility injection

- Add `<title>` element if missing — derive from filename (e.g., `icon-cloud-sync.svg` → "Cloud sync icon")
- Add `<desc>` element if missing — generic description of the icon purpose
- Add `role="img"` to the root `<svg>` element

---

## 3. Directory Mapping & Packaging

### 3.1 Distribution directory structure

Generate this output structure:

```
dist/
├── icons/                    # Monochrome, themeable SVG icons
│   ├── filled/              # Filled variants
│   ├── outlined/            # Outlined variants
│   └── animated/            # Animated SVG variants
├── illustrations/           # Multi-color SVG illustrations
│   ├── dashboard/           # Dashboard-specific illustrations
│   └── marketing/           # Marketing page illustrations
├── raster/                  # Non-SVG raster assets (PNG, JPG)
├── fonts/                   # Font files, if any
└── manifest.csv             # Complete asset inventory
```

### 3.2 Asset renaming

Rename non-compliant files:

- `checkout icon.svg` → `checkout-icon.svg`
- `Profile_Avatar_v2.svg` → `profile-avatar.svg`
- `HERO-BANNER.png` → `hero-banner.png`

Maintain a rename log: `old_name → new_name → reason`.

### 3.3 Orphan and duplicate detection

- Flag files in the source directory that are not referenced in any manifest
- Flag duplicate SVGs (same path data, different filenames)
- Flag empty SVG files (zero paths)
- Flag oversized SVGs (> 50 KB for icons, > 200 KB for illustrations)

---

## 4. Output & Reporting

### 4.1 Distribution package

Write to `dist/`:

- Organized subdirectories with optimized files
- `manifest.csv` — columns: filename, category, size_before, size_after, savings_pct, issues
- `rename-log.csv` — columns: original_name, new_name, reason

### 4.2 Terminal summary

```
=== ASSET PACK OPTIMIZER SUMMARY ===
Source directory:       data/mock_assets/

Processing results:
  SVGs scanned:         12
  SVGs optimized:       12
  Path bytes removed:   4,280  (32% avg reduction)
  viewBox fixes:        2
  Color governance:     3 hardcoded colors → currentColor
  Accessibility tags:   4 missing titles added

  Naming violations:    3 fixed
  Orphans found:        1
  Duplicates found:     0
  Oversized files:      1 flagged

Output package:
  ✅ dist/icons/         (6 files, 2 subdirectories)
  ✅ dist/illustrations/ (3 files)
  ✅ dist/raster/        (3 files)
  ✅ dist/manifest.csv
  ✅ dist/rename-log.csv

Status:                 Ready for distribution
```

### 4.3 Quality gate

The output package must pass:

- Every SVG opens correctly (valid XML)
- Every SVG has a viewBox
- Every icon SVG uses `currentColor` for fill/stroke
- No filenames contain spaces, underscores, or uppercase
- manifest.csv has no missing values
- Total package size is less than source size

---

## 5. Strictness Rules

| # | Rule | Enforcement |
|---|---|---|
| 1 | Every SVG MUST have a viewBox attribute after processing | Hard block |
| 2 | Every monochrome icon MUST use `currentColor` for fill/stroke | Hard block |
| 3 | No filenames with spaces, underscores, or uppercase letters in the output | Hard block |
| 4 | All Inkscape/Sodipodi metadata MUST be removed | Hard block |
| 5 | Every SVG MUST have `<title>` and `role="img"` elements | Warning |
| 6 | SVG path data MUST NOT contain unnecessary decimal precision (> 2 decimal places) | Warning |
| 7 | Distribution manifest MUST include size_before, size_after, and savings_pct columns | Hard block |

---

## 6. Edge Cases

| # | Scenario | Handling |
|---|---|---|
| 1 | SVG has zero paths (empty icon) | Flag as broken; do not include in output package |
| 2 | Filename is already kebab-case but uses non-standard extension (`.SVG`) | Rename extension to lowercase; include in rename log |
| 3 | SVG uses external references (`<image href="...">`) | Flag; external refs break offline distribution |
| 4 | Multiple icons share identical path data (duplicates) | Deduplicate; keep one copy, add alias in manifest |
| 5 | Asset set includes animated SVGs with `<animate>` or `<animateTransform>` | Move to `icons/animated/`; flag that animation adds complexity |
| 6 | PNG/JPG assets exist without corresponding SVG versions | Flag as potentially missing vector source |
| 7 | SVG contains embedded `<style>` blocks with non-namespaced selectors | Flag; suggest scoping styles to avoid conflicts |
