# Exercise 4 — Production Asset Pack Optimization

## Scenario

The Design team has accumulated a batch of raw SVG exports from various sources — some from Figma, some from Inkscape, some hand-edited. Before shipping to engineering, the team must run these through automated cleaning steps to clean, minify, strip metadata, enforce naming conventions, and organize them into a strict production-ready folder tree. This exercise mirrors a real Friday-afternoon asset pack handoff.

## Learning Objectives

- Scan and classify a mixed asset directory by file type, size, and category
- Use the `asset-pack-optimizer` workspace preset to automate SVG optimization
- Minify SVG path data, strip editor metadata, and normalize viewBox values
- Enforce kebab-case naming conventions across all assets
- Inject accessibility tags (title, desc, role="img") into every SVG
- Organize optimized assets into a structured `dist/` directory tree
- Produce a manifest CSV and rename log for engineering handoff

## Dataset

Open the Weatherman AI Portal in your browser. Select **"Paula & Gaby"** from the sidebar dropdown. Use the paperclip icon to upload all files from the `data/mock-assets/` folder.

| File | Type | Size | Issues |
|---|---|---|---|
| `icon-cloud-sync.svg` | SVG icon | ~560 B | Non-integer viewBox, hardcoded color, missing a11y, editor metadata |
| `logo-hero-main.svg` | SVG logo | ~1 KB | Missing viewBox, non-brand color, Inkscape metadata, unused defs |
| `illustration-dashboard.svg` | SVG illustration | ~3 KB | Empty desc, non-standard hex, hardcoded fonts, overly complex paths |
| `design-tokens.json` | JSON token file | ~1.5 KB | No SVG processing needed |
| `component-tokens.css` | CSS token file | ~1 KB | No SVG processing needed |

### Known Issues Planted in the Data

| Issue | Location | Notes |
|---|---|---|
| Editor metadata | `logo-hero-main.svg` | `sodipodi:namedview`, `inkscape:*` attributes |
| Redundant attributes | All 3 SVGs | `xml:space="preserve"`, `version="1.1"` |
| Non-integer viewBox | `icon-cloud-sync.svg` | Causes sub-pixel rendering |
| Missing viewBox | `logo-hero-main.svg` | No viewBox attribute |
| Unused defs | `logo-hero-main.svg` | `#unusedGradient` defined but never referenced |
| Hardcoded colors | All 3 SVGs | Should use `currentColor` or token variables |
| Missing a11y tags | `icon-cloud-sync.svg`, `logo-hero-main.svg` | No title/desc/role |
| Overly complex paths | `illustration-dashboard.svg` | High path command count |
| Orphaned assets | `logo-hero-main.svg` | No manifest references this file |

## Walkthrough

### Step 1 — Upload the asset files and scan everything

Open the Weatherman AI Portal in your browser. Select **"Paula & Gaby"** from the sidebar dropdown. Click the paperclip icon and upload all files from `data/mock-assets/`.

Type this prompt:

```
List every file I've uploaded. For each file, report:
- Filename
- Extension
- File size in KB
- Category (SVG icon, SVG logo, SVG illustration, JSON, CSS)
- Naming convention check: is it valid kebab-case?

Sort by category. Flag any naming violations.
```

### Step 2 — Run the asset-pack-optimizer workspace preset

Paste the asset-pack-optimizer system prompt (from `presets/asset-pack-optimizer/SKILL.md`) into the chat input first to configure the AI, then type this prompt:

```
Run the asset-pack-optimizer preset against the uploaded files.

Phase 1 — Directory Classification:
Classify every file:
| File | Extension | Category | Needs SVG Optimization? | Naming OK? |

Phase 2 — SVG Optimization:
For every SVG file, perform these operations:

a) Strip editor metadata:
   - Remove sodipodi:* attributes
   - Remove inkscape:* attributes
   - Remove xml:space="preserve"
   - Remove version="1.1"

b) Fix viewBox:
   - icon-cloud-sync.svg: Round decimals to integers → "0 0 24 24"
   - logo-hero-main.svg: Add viewBox="0 0 200 60"
   - illustration-dashboard.svg: viewBox OK — confirm

c) Remove empty <g></g> groups and unused <defs> sections.

d) Collapse redundant <g> wrappers that don't apply transforms.

e) Replace hardcoded fill/stroke colors:
   - Monochrome icons → currentColor
   - Multi-color illustrations → var(--...) token references

f) Inject accessibility:
   - Add <title> derived from filename
   - Add <desc> describing the visual
   - Add role="img" to root <svg>

After each operation, report the byte reduction per file.
```

### Step 3 — Enforce naming conventions

Type this prompt (continuing the session):

```
Audit all filenames for kebab-case compliance:

Rules:
- Lowercase only
- Words separated by hyphens, not underscores or spaces
- No double hyphens
- No trailing hyphens
- Extensions are lowercase
- No version numbers in filename

Check each file and build a rename plan:

| Original Name | Violation | Corrected Name |
|---|---|---|
| ... | ... | ... |

Apply the renames. If any file is already compliant, mark it as OK.

Write rename-log.csv with columns: original_name, new_name, reason
```

### Step 4 — Build the distribution package

Type this prompt (continuing the session):

```
Create a dist/ directory with this structure:

dist/
├── icons/
│   ├── filled/
│   └── outlined/
├── illustrations/
├── raster/          (if any PNG/JPG files)
├── tokens/
└── manifest.csv

Classification rules:
- SVGs under 10 KB with currentColor → icons/outlined/
- SVGs with multiple colors → illustrations/
- JSON/CSS → tokens/
- Any file not classifiable → other/

After organizing, verify the structure:
- Every SVG has a viewBox
- Every icon SVG uses currentColor
- No filenames contain spaces, underscores, or uppercase

Write manifest.csv with columns:
filename, category, size_before, size_after, savings_pct, issues
```

### Step 5 — Export the optimizer report

Type this prompt (continuing the session):

```
Print a summary:

=== ASSET PACK OPTIMIZER SUMMARY ===
Source directory:       data/mock-assets/

Processing results:
  SVGs scanned:         X
  SVGs optimized:       X
  Path bytes removed:   X (X% avg reduction)
  viewBox fixes:        X
  Color governance:     X hardcoded colors → tokens/currentColor
  Accessibility tags:   X missing titles added

  Naming violations:    X fixed
  Orphans found:        X
  Duplicates found:     X

Output package:
  ✅ dist/icons/         (X files)
  ✅ dist/illustrations/ (X files)
  ✅ dist/tokens/        (X files)
  ✅ dist/manifest.csv
  ✅ dist/rename-log.csv

Status:                 Ready for distribution
```

## Expected Output

After completing all steps, you should have:

- All 3 SVGs optimized with metadata stripped, viewBox normalized, and paths minified
- Hardcoded colors replaced with `currentColor` or token references
- Accessibility tags injected into every SVG
- All naming violations corrected with a rename log
- A `dist/` directory with organized subdirectories (icons, illustrations, tokens)
- A `manifest.csv` with before/after sizes and savings percentages
- A `rename-log.csv` documenting all naming changes
- All files downloadable from the portal
- Practical experience running the `asset-pack-optimizer` workspace preset
