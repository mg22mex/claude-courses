# Executive Suite: Entrepreneurship, Strategy & Management

**Course Title:** Executive Suite — Entrepreneurship, Strategy & Management
**Target User:** Rick — Executive Leadership / Entrepreneurship / Management
**Prerequisites:** Familiarity with P&L statements, board reporting, and strategic planning concepts; no coding experience required.
**Estimated Duration:** 4 hours (split across two 2-hour sessions)
**Format:** Live walkthrough + hands-on exercises in the Weatherman AI Portal

---

## Pre-Work: Load Your Institutional Memory

Before starting this course, open the [Master Claude Code Guide](https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1) alongside your domain-specific NotebookLM notebook. Query both notebooks to understand the strategic analysis patterns and business rules that apply to your work in the Weatherman AI Portal.

**Your Domain Notebook:** [Rick's Executive Notebook](https://notebooklm.google.com/notebook/8644375a-5c5f-442d-b35b-fb849e3f93b2?authuser=1)

> **Workflow Rule:** All analysis, report generation, and document templating in this track must cross-verify patterns against both the Master Guide and your Domain Notebook before executing in the portal.

---

## Learning Objectives

By the end of this course, Rick will be able to:

1. Upload and inspect multi-department corporate KPI dashboards and financial logs in the Weatherman AI Portal.
2. Identify budget variances, margin erosion, and overhead creep by analysing department-level P&L data.
3. Model go/no-go decision gates using milestone tracking and risk heatmaps.
4. Generate structured Product Requirement Documents from raw business concepts using the PRD workspace preset.
5. Distill operational data into board-ready presentation decks and architecture diagrams using workspace presets.
6. Deploy a suite of executive workspace presets for recurring strategic planning and reporting workflows.

---

## Lesson Plan

### Lesson 1 — Executive Dashboarding & KPI Tracking (40 min)

**Objective:** Upload corporate operational logs and build a macro-level view of departmental health.

| Segment | Topic | Activity |
|---|---|---|
| 1.1 | Opening the Weatherman AI Portal | Log into the portal, select "Rick" from the sidebar dropdown, and upload the executive dashboard CSV using the paperclip icon. |
| 1.2 | Inspecting the corporate schema | Ask the portal AI to describe columns, data types, and row counts across all departments and quarters. |
| 1.3 | KPI variance analysis | Prompt the portal AI to compare `budget_allocated` vs `budget_spent` and `revenue_target` vs `revenue_actual` per department. |
| 1.4 | Profitability heatmap | Group by department and quarter; compute profit margin trends; flag departments with margin erosion. |

**Portal Exercises:**

Upload the file `executive_dashboard.csv` using the paperclip icon, then type this prompt:

> "Describe the columns, data types, and which departments and quarters are represented. Show me the total budget across all departments."

Then type this prompt:

> "Group by department and quarter. For each, compute profit_margin = (revenue_actual - budget_spent - overhead_cost) / revenue_actual. Sort by margin ascending. Flag any department with margin below 10% or negative margin."

---

### Lesson 2 — Corporate Financial Modeling (40 min)

**Objective:** Analyse budget vs actuals, compute burn rate, and identify overhead allocation issues.

| Segment | Topic | Activity |
|---|---|---|
| 2.1 | Budget vs actual deep-dive | Upload `executive_dashboard.csv` and compute variance percentages per department per quarter. |
| 2.2 | Burn rate analysis | Calculate quarterly and cumulative burn rates; project runway at current spend levels. |
| 2.3 | Overhead allocation | Analyse overhead_cost as a percentage of total spend; flag departments where overhead grew faster than revenue. |
| 2.4 | Full-year projection | Use Q1–Q3 trends to project Q4 outcomes; compare against budget. |

**Portal Exercises:**

Type this prompt into the chat input:

> "For each department, compute budget_variance_pct = (budget_spent - budget_allocated) / budget_allocated * 100. Show me departments where variance exceeds +5% (overspend) or falls below -5% (underspend)."

Then type this prompt:

> "Calculate overhead_ratio = overhead_cost / budget_spent for each department per quarter. Sort by Q4 overhead_ratio descending. Flag any department where overhead_ratio increased for 3+ consecutive quarters."

---

### Lesson 3 — Entrepreneurial Decision Frameworks (40 min)

**Objective:** Model stage-gate decisions, resource allocation scenarios, and milestone-based portfolio reviews.

| Segment | Topic | Activity |
|---|---|---|
| 3.1 | Milestone health assessment | Upload the executive dashboard and compute milestone completion rates per department; flag at-risk milestones. |
| 3.2 | Go/no-go gate modeling | Define a stage-gate framework — ask the portal AI to identify which departments/initiatives should trigger a review based on milestone slippage and budget overspend. |
| 3.3 | Resource reallocation scenarios | Prompt the portal AI to model "what-if" scenarios: redirecting budget from underperforming to overperforming departments. |
| 3.4 | Portfolio risk heatmap | Build a risk matrix combining budget variance, milestone completion, and margin trend into a single composite score. |

**Portal Exercises:**

Type this prompt into the chat input:

> "For each department, compute milestone_completion_pct = milestones_completed / milestones_total * 100. Flag any department where completion_pct < 50% and milestones_at_risk > 2. Label these as 'GATE REVIEW NEEDED'."

Then type this prompt:

> "Create a composite risk score per department: (budget_variance_weight * 0.3) + (milestone_at_risk_ratio * 0.4) + (margin_decline * 0.3). Rank by risk score descending. Show me the top 3 highest-risk departments."

---

### Lesson 4 — Strategic Planning & Portfolio Management (40 min)

**Objective:** Track multi-project milestones, map dependencies, and produce a strategic roadmap.

| Segment | Topic | Activity |
|---|---|---|
| 4.1 | Cross-department dependency mapping | Upload the executive dashboard and identify departments whose milestones are interdependent or share resources. |
| 4.2 | Strategic roadmap generation | Use the dashboard data to produce a quarter-by-quarter roadmap showing initiative phases, milestones, and go/no-go decision points. |
| 4.3 | Resource capacity planning | Compare headcount across departments against budget growth; flag teams that are understaffed relative to spend. |
| 4.4 | Executive summary generation | Ask the portal AI to write a one-page strategic summary synthesising all findings. |

**Portal Exercises:**

Type this prompt into the chat input:

> "Using the executive dashboard data, produce a Q1-Q4 2026 strategic roadmap. Group milestones by quarter and department. Highlight which quarters have the highest concentration of at-risk milestones and recommend which gates should trigger executive reviews."

Then type this prompt:

> "Write a one-page executive summary covering: 1) Overall financial health, 2) Top 3 budget variances, 3) Milestone performance by department, 4) Top 3 recommendations for the next quarter. Use bullet points and a small table for key metrics."

---

### Lesson 5 — Automated Executive Reporting (40 min)

**Objective:** Deploy the executive workspace preset suite — PRD, presentation, and architecture diagram generators.

| Segment | Topic | Activity |
|---|---|---|
| 5.1 | Introducing the write-a-prd preset | Open `presets/write-a-prd/SKILL.md` and review its PRD generation workflow. |
| 5.2 | Running write-a-prd on a concept | Feed a business idea into the PRD preset; review the generated requirements, milestones, and risk register. |
| 5.3 | Generating a board presentation | Use the `ppt-generation` preset to turn the executive dashboard data into a slide deck outline. |
| 5.4 | Creating an architecture diagram | Use the `architecture-diagram` preset to visualise a system or organisational structure. |
| 5.5 | Tying it together — weekly exec cycle | Save the master audit prompt and run the full executive reporting suite. |

**Portal Exercises:**

Upload the write-a-prd preset file, then type this prompt into the chat input:

> "Run the write-a-prd preset. Here is my concept: [paste your initiative idea]. Generate a full PRD with milestones, KPIs, and a risk register."

Upload the executive dashboard CSV, then type this prompt:

> "Run the ppt-generation preset against the executive dashboard data. Generate an 8-slide board deck covering financial health, department performance, risks, and recommendations."

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
| Fulfillment anomaly detector preset | `presets/fulfillment-anomaly-detector/SKILL.md` |
| PRD generator preset | `presets/write-a-prd/SKILL.md` |
| Presentation generator preset | `presets/ppt-generation/SKILL.md` |
| Architecture diagram preset | `presets/architecture-diagram/SKILL.md` |
| Sunny's lead-time-anomaly preset (adjacent) | `../sunny/presets/lead-time-anomaly/SKILL.md` |
| Sunny's warehouse-balancing preset (adjacent) | `../sunny/presets/warehouse-balancing/SKILL.md` |

---

## Success Criteria

Rick can independently:

- [ ] Log into the Weatherman AI Portal and select the Rick profile from the sidebar dropdown
- [ ] Upload the executive dashboard CSV using the paperclip icon
- [ ] Identify all departments with budget variances exceeding +-5%
- [ ] Compute profit margin trends and flag margin erosion
- [ ] Model go/no-go decisions using milestone and risk data
- [ ] Generate a structured PRD from a raw business concept
- [ ] Produce a board-ready presentation deck from operational data
- [ ] Create a Mermaid architecture diagram from a system description
- [ ] Run the full executive workspace preset suite for recurring strategic reviews

### High-Impact Operational Presets

**1. Contract Risk Redliner** — scanning vendor agreements for hidden liability, margin exposure, or IP gaps.  
**2. Strategic Product Launch Reviewer** — evaluating product launch timelines against macro logistics constraints.  
**3. High-Level Partnership Pitch Deck Critic** — critiquing layout and messaging for retail/brand alliances.  
**4. Macro Budget Variance Flagging** — spotting cost anomalies across department financial rollups.  
**5. Executive Briefing Generator** — condensing multi-page reports into 3 mobile-friendly action items.
