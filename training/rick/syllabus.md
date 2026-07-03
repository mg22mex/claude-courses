# Executive Suite: Entrepreneurship, Strategy & Management with Claude Code

**Course Title:** Executive Suite — Entrepreneurship, Strategy & Management
**Target User:** Rick — Executive Leadership / Entrepreneurship / Management
**Prerequisites:** Familiarity with P&L statements, board reporting, and strategic planning concepts; no coding experience required.
**Estimated Duration:** 4 hours (split across two 2-hour sessions)
**Format:** Live walkthrough + hands-on terminal + Claude Code exercises

---

## Pre-Work: Load Your Institutional Memory

Before starting this course, open the [Master Claude Code Guide](https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1) alongside your domain-specific NotebookLM notebook. Query both notebooks to understand how Claude Code operates in your domain before writing any scripts or building tools.

**Your Domain Notebook:** [Rick's Executive Notebook](https://notebooklm.google.com/notebook/8644375a-5c5f-442d-b35b-fb849e3f93b2?authuser=1)

> **Workflow Rule:** All script generation, data testing, or document templating in this track must cross-verify patterns against both the Master Guide and your Domain Notebook before execution.

---

## Learning Objectives

By the end of this course, Rick will be able to:

1. Load and inspect multi-department corporate KPI dashboards and financial logs in Claude Code.
2. Identify budget variances, margin erosion, and overhead creep by analysing department-level P&L data.
3. Model go/no-go decision gates using milestone tracking and risk heatmaps.
4. Generate structured Product Requirement Documents from raw business concepts using the PRD automation skill.
5. Distill operational data into board-ready presentation decks and architecture diagrams using automation skills.
6. Deploy a suite of executive automation skills for recurring strategic planning and reporting workflows.

---

## Lesson Plan

### Lesson 1 — Executive Dashboarding & KPI Tracking (40 min)

**Objective:** Load corporate operational logs and build a macro-level view of departmental health.

| Segment | Topic | Activity |
|---|---|---|
| 1.1 | Opening Claude Code in the repo | Navigate to `training/rick/data/`, launch `claude`, and load the executive dashboard CSV. |
| 1.2 | Inspecting the corporate schema | Ask Claude to describe columns, data types, and row counts across all departments and quarters. |
| 1.3 | KPI variance analysis | Prompt Claude to compare `budget_allocated` vs `budget_spent` and `revenue_target` vs `revenue_actual` per department. |
| 1.4 | Profitability heatmap | Group by department and quarter; compute profit margin trends; flag departments with margin erosion. |

**CLI Exercises:**

```
# Exercise 1.2 — Inspect the executive dashboard schema
claude data/executive_dashboard.csv
> "Describe the columns, data types, and which departments and quarters are represented. Show me the total budget across all departments."
```

```
# Exercise 1.4 — Department profitability heatmap
claude data/executive_dashboard.csv
> "Group by department and quarter. For each, compute profit_margin = (revenue_actual - budget_spent - overhead_cost) / revenue_actual. Sort by margin ascending. Flag any department with margin below 10% or negative margin."
```

---

### Lesson 2 — Corporate Financial Modeling (40 min)

**Objective:** Analyse budget vs actuals, compute burn rate, and identify overhead allocation issues.

| Segment | Topic | Activity |
|---|---|---|
| 2.1 | Budget vs actual deep-dive | Load `executive_dashboard.csv` and compute variance percentages per department per quarter. |
| 2.2 | Burn rate analysis | Calculate quarterly and cumulative burn rates; project runway at current spend levels. |
| 2.3 | Overhead allocation | Analyse overhead_cost as a percentage of total spend; flag departments where overhead grew faster than revenue. |
| 2.4 | Full-year projection | Use Q1–Q3 trends to project Q4 outcomes; compare against budget. |

**CLI Exercises:**

```
# Exercise 2.1 — Budget variance deep-dive
claude data/executive_dashboard.csv
> "For each department, compute budget_variance_pct = (budget_spent - budget_allocated) / budget_allocated * 100. Show me departments where variance exceeds +5% (overspend) or falls below -5% (underspend)."
```

```
# Exercise 2.3 — Overhead efficiency
claude data/executive_dashboard.csv
> "Calculate overhead_ratio = overhead_cost / budget_spent for each department per quarter. Sort by Q4 overhead_ratio descending. Flag any department where overhead_ratio increased for 3+ consecutive quarters."
```

---

### Lesson 3 — Entrepreneurial Decision Frameworks (40 min)

**Objective:** Model stage-gate decisions, resource allocation scenarios, and milestone-based portfolio reviews.

| Segment | Topic | Activity |
|---|---|---|
| 3.1 | Milestone health assessment | Load the executive dashboard and compute milestone completion rates per department; flag at-risk milestones. |
| 3.2 | Go/no-go gate modeling | Define a stage-gate framework — ask Claude to identify which departments/initiatives should trigger a review based on milestone slippage and budget overspend. |
| 3.3 | Resource reallocation scenarios | Prompt Claude to model "what-if" scenarios: redirecting budget from underperforming to overperforming departments. |
| 3.4 | Portfolio risk heatmap | Build a risk matrix combining budget variance, milestone completion, and margin trend into a single composite score. |

**CLI Exercises:**

```
# Exercise 3.1 — Milestone health check
claude data/executive_dashboard.csv
> "For each department, compute milestone_completion_pct = milestones_completed / milestones_total * 100. Flag any department where completion_pct < 50% and milestones_at_risk > 2. Label these as 'GATE REVIEW NEEDED'."
```

```
# Exercise 3.4 — Portfolio risk heatmap
claude data/executive_dashboard.csv
> "Create a composite risk score per department: (budget_variance_weight * 0.3) + (milestone_at_risk_ratio * 0.4) + (margin_decline * 0.3). Rank by risk score descending. Show me the top 3 highest-risk departments."
```

---

### Lesson 4 — Strategic Planning & Portfolio Management (40 min)

**Objective:** Track multi-project milestones, map dependencies, and produce a strategic roadmap.

| Segment | Topic | Activity |
|---|---|---|
| 4.1 | Cross-department dependency mapping | Load the executive dashboard and identify departments whose milestones are interdependent or share resources. |
| 4.2 | Strategic roadmap generation | Use the dashboard data to produce a quarter-by-quarter roadmap showing initiative phases, milestones, and go/no-go decision points. |
| 4.3 | Resource capacity planning | Compare headcount across departments against budget growth; flag teams that are understaffed relative to spend. |
| 4.4 | Executive summary generation | Ask Claude to write a one-page strategic summary synthesising all findings. |

**CLI Exercises:**

```
# Exercise 4.2 — Strategic roadmap
claude data/executive_dashboard.csv
> "Using the executive dashboard data, produce a Q1–Q4 2026 strategic roadmap. Group milestones by quarter and department. Highlight which quarters have the highest concentration of at-risk milestones and recommend which gates should trigger executive reviews."
```

```
# Exercise 4.4 — One-page executive summary
claude data/executive_dashboard.csv
> "Write a one-page executive summary covering: 1) Overall financial health, 2) Top 3 budget variances, 3) Milestone performance by department, 4) Top 3 recommendations for the next quarter. Use bullet points and a small table for key metrics."
```

---

### Lesson 5 — Automated Executive Reporting (40 min)

**Objective:** Deploy the executive skill suite — PRD, presentation, and architecture diagram generators.

| Segment | Topic | Activity |
|---|---|---|
| 5.1 | Introducing the write-a-prd skill | Open `skills/write-a-prd/SKILL.md` and review its PRD generation workflow. |
| 5.2 | Running write-a-prd on a concept | Feed a business idea into the PRD skill; review the generated requirements, milestones, and risk register. |
| 5.3 | Generating a board presentation | Use `ppt-generation` to turn the executive dashboard data into a slide deck outline. |
| 5.4 | Creating an architecture diagram | Use `architecture-diagram` to visualise a system or organisational structure. |
| 5.5 | Tying it together — weekly exec cycle | Save the master audit prompt and run the full executive reporting suite in one command. |

**CLI Exercises:**

```
# Exercise 5.2 — Generate a PRD
claude skills/write-a-prd/SKILL.md
> "Run the write-a-prd skill. Here is my concept: [paste your initiative idea]. Generate a full PRD with milestones, KPIs, and a risk register."
```

```
# Exercise 5.3 — Generate a board presentation
claude data/executive_dashboard.csv skills/ppt-generation/SKILL.md
> "Run the ppt-generation skill against the executive dashboard data. Generate a 8-slide board deck covering financial health, department performance, risks, and recommendations."
```

---

## Data Dictionary

### executive_dashboard.csv

| Column | Description |
|---|---|
| `dept_id` | Unique department identifier |
| `department` | Department name (Engineering, Sales, Marketing, Operations, R&D) |
| `quarter` | Fiscal quarter (Q1, Q2, Q3, Q4) |
| `fiscal_year` | Fiscal year |
| `budget_allocated` | Approved budget for the quarter in USD |
| `budget_spent` | Actual spend for the quarter in USD |
| `headcount` | Number of employees in the department |
| `milestones_total` | Total milestones planned for the quarter |
| `milestones_completed` | Milestones completed on time |
| `milestones_at_risk` | Milestones flagged as behind schedule or blocked |
| `revenue_target` | Revenue target for the quarter in USD |
| `revenue_actual` | Actual revenue generated in USD |
| `overhead_cost` | Non-payroll operational overhead in USD |
| `profit_margin_pct` | Profit margin as a percentage |

### inventory_stock_levels.csv

| Column | Description |
|---|---|
| `sku` | Stock keeping unit identifier |
| `warehouse` | Warehouse code (e.g., WH-North, WH-East, WH-South) |
| `stock_on_hand` | Current units available in the warehouse |
| `reorder_point` | Minimum stock level before auto-reorder triggers |
| `lead_time_days` | Supplier lead time in calendar days |
| `unit_cost` | Cost per unit in USD |
| `monthly_demand` | Average monthly demand in units |

### fulfillment_delay_report.csv

| Column | Description |
|---|---|
| `order_id` | Unique fulfillment order identifier |
| `sku` | SKU being shipped |
| `warehouse` | Originating warehouse |
| `carrier` | Shipping carrier name |
| `ship_date` | Date the order left the warehouse |
| `estimated_delivery` | Promised delivery date |
| `actual_delivery` | Actual delivery date (blank if not yet delivered) |
| `status` | `delivered`, `in_transit`, `delayed`, `exception` |
| `destination_region` | Destination region code |
| `declared_value` | Declared shipment value in USD |

---

## Link Directory

| Resource | Path / Location |
|---|---|
| Course materials | `training/rick/` |
| Executive dashboard data | `training/rick/data/executive_dashboard.csv` |
| Inventory stock levels | `training/rick/data/inventory_stock_levels.csv` |
| Fulfillment delay report | `training/rick/data/fulfillment_delay_report.csv` |
| Exercise 1 — Source Material Parsing | `training/rick/exercises/exercise-1.md` |
| Exercise 2 — Enterprise Architecture Modeling | `training/rick/exercises/exercise-2.md` |
| Exercise 3 — Rigid Product Requirement Drafting | `training/rick/exercises/exercise-3.md` |
| Exercise 4 — Executive KPI & Board Room Slide Structuring | `training/rick/exercises/exercise-4.md` |
| Exercise 5 — Capstone Strategic Blueprint | `training/rick/exercises/exercise-5.md` |
| Fulfillment anomaly detector skill | `skills/fulfillment-anomaly-detector/SKILL.md` |
| PRD generator skill | `skills/write-a-prd/SKILL.md` |
| Presentation generator skill | `skills/ppt-generation/SKILL.md` |
| Architecture diagram skill | `skills/architecture-diagram/SKILL.md` |
| Sunny's lead-time-anomaly skill (adjacent) | `../sunny/skills/lead-time-anomaly/SKILL.md` |
| Sunny's warehouse-balancing skill (adjacent) | `../sunny/skills/warehouse-balancing/SKILL.md` |

---

## Success Criteria

Rick can independently:

- [ ] Launch Claude Code and load the executive dashboard CSV
- [ ] Identify all departments with budget variances exceeding ±5%
- [ ] Compute profit margin trends and flag margin erosion
- [ ] Model go/no-go decisions using milestone and risk data
- [ ] Generate a structured PRD from a raw business concept
- [ ] Produce a board-ready presentation deck from operational data
- [ ] Create a Mermaid architecture diagram from a system description
- [ ] Run the full executive skill suite for recurring strategic reviews
