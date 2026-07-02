# Claude Courses

Tailored Claude Code training for operational teams — syllabi, hands-on terminal labs, sample data, and reusable automation skills.

This repository contains four independent training tracks, each built for a specific department user. Every track includes a structured syllabus, a set of practical CLI exercises, realistic sample data, and custom Claude Code skills that automate the workflows taught in the course.

## Tracks

| Track | Team | Focus |
|---|---|---|
| **Rick** | Executive, Entrepreneurship & Management | Executive dashboarding, corporate KPI modeling, strategic planning, PRD & presentation automation |
| **Sunny** | Purchasing & Logistics | Vendor data validation, lead time anomaly detection, customs tariff auditing, warehouse balancing |
| **Mollie** | Sales & Financials | Order-to-profit analysis, CSV analytics, root-cause investigation, financial reconciliation and automated alerting |
| **Christine** | Marketing | Brand compliance, email automation, listing verification, and campaign analytics tracking |
| **Design** (Paula & Gaby) | Design | SVG auditing, design token validation, asset inventory management, component compilation and asset optimization |

## Institutional Memory Infrastructure

This repository is bound to a dual-engine NotebookLM operational framework. Every track has a dedicated Domain Notebook that encodes its processes, data schemas, and edge cases, plus a shared Master Technical Blueprint.

| Role | NotebookLM URL |
|---|---|
| **Master Claude Code Guide** (all tracks) | <https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1> |
| Rick — Executive, Entrepreneurship & Management | <https://notebooklm.google.com/notebook/8644375a-5c5f-442d-b35b-fb849e3f93b2?authuser=1> |
| Sunny — Purchasing & Logistics | <https://notebooklm.google.com/notebook/c3dc698d-38e7-4d64-8451-0bbca3fa9d97?authuser=1> |
| Mollie — Sales & Financials | <https://notebooklm.google.com/notebook/2ab95bfd-ceeb-436d-b41f-85a89e3ca749?authuser=1> |
| Christine — Marketing | <https://notebooklm.google.com/notebook/0a616bb3-6ea7-40c8-b53c-984fa4d977bc?authuser=1> |
| Design (Paula & Gaby) | <https://notebooklm.google.com/notebook/9f67d0db-49c8-4bc3-b2e5-f08a3528028f?authuser=1> |

> **Workflow Rule:** All script generation, data testing, or document templating must cross-verify patterns against both the Master Guide and the relevant Domain Notebook before execution. See `training/NOTEBOOKLM_CORE_STRATEGY.md` for the full framework.

## Repository Structure

```
training/
├── rick/                      # Executive, Entrepreneurship & Management
│   ├── syllabus.md            # Course outline and lesson plans
│   ├── data/                  # Executive dashboards, inventory logs, fulfillment reports
│   ├── exercises/             # Python fulfillment analysis
│   └── skills/                # Automation skills (4)
├── sunny/                     # Purchasing & Logistics
│   ├── syllabus.md            # Course outline and lesson plans
│   ├── data/                  # Vendor CSVs (lead times, invoices, prices)
│   ├── exercises/             # Lab walkthroughs
│   └── skills/                # Automation skills (5)
├── mollie/                    # Sales & Financials
│   ├── syllabus.md
│   ├── data/                  # Shopify exports, ad spend, webhook samples
│   ├── exercises/
│   └── skills/                # Automation skills (4)
├── christine/                 # Marketing
│   ├── syllabus.md
│   ├── data/                  # Copy decks, email campaigns, keyword targets
│   ├── exercises/
│   └── skills/                # Automation skills (4)
└── design/                    # Design
    ├── syllabus.md
    ├── data/mock_assets/      # SVGs, design tokens JSON
    ├── exercises/
    └── skills/                # Automation skills (4)
```

## Skills Summary

21 custom Claude Code skills are distributed across the tracks:

- **Rick** — `fulfillment-anomaly-detector`, `write-a-prd`, `ppt-generation`, `architecture-diagram`
- **Sunny** — `lead-time-anomaly`, `customs-tariff-audit`, `warehouse-balancing`, `xlsx-processing`, `data-table-validator`
- **Mollie** — `csv-analytics`, `monte-carlo-analyze-root-cause`, `reconciliation-engine`, `anomaly-alert-webhook`
- **Christine** — `brand-guardrails`, `email-automation`, `listing-verification`, `campaign-analytics`
- **Design** — `svg-auditor`, `design-token-validator`, `component-spec-compiler`, `asset-pack-optimizer`

Each skill lives in its own directory with a `SKILL.md` defining the prompt and usage. Skills from other tracks can be invoked cross-track by referencing the relative path.

## Sample Data

The `data/` directories contain realistic (but synthetic) operational data:

- **Rick**: Executive dashboards (department budgets, milestone tracking, profit margins), inventory stock levels, fulfillment delay reports with carrier transit data
- **Sunny**: Vendor lead times, purchase orders, invoices, contract prices
- **Mollie**: Shopify order feeds, marketing spend, COGS, ad spend, webhook samples
- **Christine**: Raw copy decks, email campaigns, keyword targets, email send logs, campaign performance data
- **Design**: SVG icons, illustrations, logos, design token JSON

## Getting Started

Each course is self-contained. To run a track:

1. Open Claude Code in this repository root.
2. Open the track's `syllabus.md` for the full curriculum.
3. Work through the lab exercises in `exercises/`.
4. Use the companion skills in `skills/` to automate recurring tasks.

No coding experience is required — only basic familiarity with spreadsheets and file management.

## Requirements

- [Claude Code](https://claude.ai/code) (CLI)
- Access to this repository
- For Mollie's track: Shopify admin access (optional, for real data exports)

## License

Internal use — training materials for operational team onboarding.
