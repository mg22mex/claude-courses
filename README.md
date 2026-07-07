# The Weatherman AI Portal

A custom, zero-install Streamlit web application for operational team training — no terminal, no CLI, no developer setup required.

Your entire team accesses the Weatherman AI Portal through a secure browser URL. Each member selects their name from a sidebar dropdown, which automatically loads their pre-configured API settings (DeepSeek / OpenClaude) and master department system profiles. From there, they simply upload their standard business files (.csv, .xlsx, .pdf) and interact using natural-language prompts to complete realistic operational exercises, generate reports, and produce polished deliverables.

Everything lives in one place: the syllabus, the data files, and the workspace presets — all served through a clean web interface.

---

## Team Tracks

| Track | Team | Focus Area |
|---|---|---|
| **Rick** | Executive, Entrepreneurship & Management | Executive dashboarding, corporate KPI modeling, strategic planning, PRD & presentation automation |
| **Sunny** | Purchasing & Logistics | Vendor data validation, lead time analysis, customs tariff auditing, warehouse balancing |
| **Mollie** | Sales & Financials | Order-to-profit analysis, financial reconciliation, root-cause investigation, automated alerting |
| **Christine** | Marketing | Brand compliance, email automation, listing verification, campaign analytics |
| **Design** (Paula & Gaby) | Creative Design | SVG auditing, design token validation, asset inventory management, component compilation and asset optimization |

---

## Institutional Memory Infrastructure

This portal is backed by a dual-notebook system in NotebookLM. Each track has a dedicated Domain Notebook encoding its processes, data schemas, and edge cases, plus a shared Master Guide.

| Role | NotebookLM URL |
|---|---|
| **Master Guide** (all tracks) | <https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1> |
| Rick — Executive, Entrepreneurship & Management | <https://notebooklm.google.com/notebook/8644375a-5c5f-442d-b35b-fb849e3f93b2?authuser=1> |
| Sunny — Purchasing & Logistics | <https://notebooklm.google.com/notebook/c3dc698d-38e7-4d64-8451-0bbca3fa9d97?authuser=1> |
| Mollie — Sales & Financials | <https://notebooklm.google.com/notebook/2ab95bfd-ceeb-436d-b41f-85a89e3ca749?authuser=1> |
| Christine — Marketing | <https://notebooklm.google.com/notebook/0a616bb3-6ea7-40c8-b53c-984fa4d977bc?authuser=1> |
| Design (Paula & Gaby) | <https://notebooklm.google.com/notebook/9f67d0db-49c8-4bc3-b2e5-f08a3528028f?authuser=1> |

---

## Repository Structure

```
training/
├── rick/                      # Executive, Entrepreneurship & Management
│   ├── syllabus.md            # Course outline and lesson plans
│   ├── data/                  # Executive dashboards, inventory logs, fulfillment reports
│   ├── exercises/             # 5 progressive portal walkthroughs
│   └── presets/               # Workspace presets (4)
├── sunny/                     # Purchasing & Logistics
│   ├── syllabus.md            # Course outline and lesson plans
│   ├── data/                  # Vendor CSVs (lead times, invoices, prices)
│   ├── exercises/             # 5 progressive portal walkthroughs
│   └── presets/               # Workspace presets (5)
├── mollie/                    # Sales & Financials
│   ├── syllabus.md
│   ├── data/                  # Shopify exports, ad spend, webhook samples
│   ├── exercises/             # 5 progressive portal walkthroughs
│   └── presets/               # Workspace presets (4)
├── christine/                 # Marketing
│   ├── syllabus.md
│   ├── data/                  # Copy decks, email campaigns, keyword targets
│   ├── exercises/             # 5 progressive portal walkthroughs
│   └── presets/               # Workspace presets (4)
└── design/                    # Design
    ├── syllabus.md
    ├── data/mock-assets/      # SVGs, design tokens JSON
    ├── exercises/             # 5 progressive portal walkthroughs
    └── presets/               # Workspace presets (4)
```

---

## Workspace Presets

21 workspace presets are distributed across the tracks. Each preset is a pre-optimized system prompt that configures the portal AI for a specific operational task:

- **Rick** — `fulfillment-anomaly-detector`, `write-a-prd`, `ppt-generation`, `architecture-diagram`
- **Sunny** — `lead-time-anomaly`, `customs-tariff-audit`, `warehouse-balancing`, `xlsx-processing`, `data-table-validator`
- **Mollie** — `csv-analytics`, `monte-carlo-analyze-root-cause`, `reconciliation-engine`, `anomaly-alert-webhook`
- **Christine** — `brand-guardrails`, `email-automation`, `listing-verification`, `campaign-analytics`
- **Design** — `svg-auditor`, `design-token-validator`, `component-spec-compiler`, `asset-pack-optimizer`

Each preset lives in its own directory within `presets/`. To use a preset from another department, simply switch your sidebar profile or paste the preset's system instructions into your current session.

---

## Sample Data

The `data/` directories contain realistic (but synthetic) operational data:

- **Rick**: Executive dashboards (department budgets, milestone tracking, profit margins), inventory stock levels, fulfillment delay reports with carrier transit data
- **Sunny**: Vendor lead times, purchase orders, invoices, contract prices
- **Mollie**: Shopify order feeds, marketing spend, COGS, ad spend, webhook samples
- **Christine**: Raw copy decks, email campaigns, keyword targets, email send logs, campaign performance data
- **Design**: SVG icons, illustrations, logos, design token JSON

---

## Getting Started

Every track is self-contained in the Weatherman AI Portal. To begin:

1. Open the track's `syllabus.md` — start with your department's page.
2. Read through the lesson plan and exercise overview.
3. Launch each exercise from `exercises/` — instructions guide you through logging into the portal, selecting your preset, uploading your data files, and running natural-language prompts.
4. Reference the `presets/` directory for ready-to-use system instructions that automate recurring departmental tasks.

No coding experience is required — only basic familiarity with spreadsheets and file management.

---

## License

Internal use — training materials for operational team onboarding.

<- Update CLAUDE.md and README.md with global GDrive Sync Active -->
