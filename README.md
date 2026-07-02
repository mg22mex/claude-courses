# Claude Courses

Tailored Claude Code training for operational teams — syllabi, hands-on terminal labs, sample data, and reusable automation skills.

This repository contains four independent training tracks, each built for a specific department user. Every track includes a structured syllabus, a set of practical CLI exercises, realistic sample data, and custom Claude Code skills that automate the workflows taught in the course.

## Tracks

| Track | Team | Focus |
|---|---|---|
| **Sunny** | Purchasing & Logistics | Vendor data validation, lead time anomaly detection, customs tariff auditing, warehouse balancing |
| **Mollie** | Sales & Financials | Order-to-profit analysis, CSV analytics, root-cause investigation |
| **Christine** | Marketing | Brand compliance, copy optimization, SEO keyword verification |
| **Design** (Paula & Gaby) | Design | SVG auditing, design token validation, asset inventory management |

## Repository Structure

```
training/
├── sunny/                     # Purchasing & Logistics
│   ├── syllabus.md            # Course outline and lesson plans
│   ├── data/                  # Vendor CSVs (lead times, invoices, prices)
│   ├── exercises/             # Lab walkthroughs
│   └── skills/                # Automation skills (5)
├── mollie/                    # Sales & Financials
│   ├── syllabus.md
│   ├── data/                  # Shopify exports, ad spend, webhook samples
│   ├── exercises/
│   └── skills/                # Automation skills (2)
├── christine/                 # Marketing
│   ├── syllabus.md
│   ├── data/                  # Copy decks, email campaigns, keyword targets
│   ├── exercises/
│   └── skills/                # Automation skills (1)
└── design/                    # Design
    ├── syllabus.md
    ├── data/mock_assets/      # SVGs, design tokens JSON
    ├── exercises/
    └── skills/                # Automation skills (2)
```

## Skills Summary

10 custom Claude Code skills are distributed across the tracks:

- **Sunny** — `lead-time-anomaly`, `customs-tariff-audit`, `warehouse-balancing`, `xlsx-processing`, `data-table-validator`
- **Mollie** — `csv-analytics`, `monte-carlo-analyze-root-cause`
- **Christine** — `brand-guardrails`
- **Design** — `svg-auditor`, `design-token-validator`

Each skill lives in its own directory with a `SKILL.md` defining the prompt and usage. Skills from other tracks can be invoked cross-track by referencing the relative path.

## Sample Data

The `data/` directories contain realistic (but synthetic) operational data:

- **Sunny**: Vendor lead times, purchase orders, invoices, contract prices
- **Mollie**: Shopify order feeds, marketing spend, COGS, ad spend, webhook samples
- **Christine**: Raw copy decks, email campaigns, keyword targets
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
