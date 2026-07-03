# 📦 Purchasing & Logistics Lab: Guide & Guardrails

Welcome to Sunny's Purchasing & Logistics track. Before executing any local catalog normalizers, invoice parsers, or warehouse rebalancing scripts, use this guide alongside **NotebookLM (The Oracle)** to verify track constraints and isolate intentional procurement traps.

---

## 🛠️ 1. Operational Data & Pipeline Traps

Your data-cleaning scripts and extraction pipelines must ingest multi-vendor schemas and scrub out the following structural anomalies:

### 🔤 Schema Alignment & Field Mismatches
* **Inconsistent Headers:** Harmonize incoming datasets that shuffle column naming conventions for product identifiers (`item_code`, `sku`, `part_number`) and cost structures (`unit_price`, `cost_per_unit`, `rate`).
* **Varying Payloads:** Account for structural drift where specific data providers (e.g., Prime Cargo) include auxiliary columns (like `notes`) that do not exist across parallel files.
* **Currency Exposure Trap:** The capstone contains a line billed entirely in **EUR**, while the surrounding line items are in **USD**. Scripts must dynamically flag this row and apply an accurate currency conversion factor.

### 📉 Ledger Overlap & Botched Data Entries
* **Double-Billing Risks:** Catch an identical duplicate row flanking lines 1 and 2 of the capstone invoice.
* **Purchase Order Clones:** Flag duplicated purchase order identifiers (such as `PO-8809`) to verify if it represents a data error or a split shipment.
* **Negative Quantity Trap:** Line 16 of the capstone contains a completely botched inventory value entry: `qty = -100` and `line_total = -500.00`.
* **Data Gaps:** Isolate rows with blank `actual_delivery` fields (representing unreceived stock) or corrupted `actual_received_date` text blocks.

### ⚖️ Customs, Tariffs, & Compliance Exceptions
* **Missing Declarations:** Identify missing `country_of_origin` strings that present custom rejection hazards.
* **Tariff Misclassifications:** Isolate invalid HS codes (e.g., `9999.99` or `7318.15`) and flag components misclassified at a 0% duty rate that should legally settle at **3.5%**.
* **Restricted Cargo:** Instantly block and flag any transit manifests containing networking hardware under HS code `8517.62` that lack an attached export license.
* **Calendar Logistics Exceptions:** Delivery tables feature entries landing on weekends, regional holidays, or marked as `partial=TRUE`. These require isolated validation branches when benchmarking carrier transit times.

---

## 📐 2. System Constraints & Thresholds

To pass the logistics validation gates, scripts must verify internal thresholds and strictly cross-reference external standards:

### 🧠 Institutional Memory Verification
* All script generation, document templating, and automated text parsing **must cross-verify structural logic** against the *Master Claude Code Guide* and *Sunny's Purchasing Notebook* before running any terminal operations.

### 📉 Stockout & Lead-Time Guardrails
* **Inventory Stockout Threshold:** When auditing multi-node distribution clusters, flag any warehouse inventory falling **below 3 days of stock**.
  * *Trap:* Catch the imbalance where the South Warehouse craters to **1.4 days of stock** (50 units on hand vs. 35 daily demand), while the North Warehouse hoards an excess **41.7 days of supply**.
* **Lead-Time Outliers:** Isolate chronic delivery delays (e.g., shipments stretching to 17 days against a 7-day maximum SLA) as well as suspicious fast-tracks (e.g., arrivals tracking at just 2 days when the baseline logistics window is 7–10 days).

### 🧮 Explicit Mathematical Auditing
* Your scripts cannot blindly trust row summaries. They must run programmatic assertions validating every row index via:
  $$\text{quantity} \times \text{unit\_cost} = \text{line\_total}$$
* Recalculate import tariffs manually by executing:
  $$\text{Billed Value} \times \text{Tariff Rate} = \text{Duty Amount}$$
  Compare this target explicitly against the incoming `duty_charged` value to spot custom pricing deviations.

---

## 🎯 3. Core Validation & Output Requirements

Your automated workflows must generate uniform documentation schemas and execute structured final deliverables:

### 📂 Pipeline Data Exports
The terminal pipeline must regularly output intermediate data scripts into clean, structured CSV tables:
1. `normalized_catalog.csv` (A consolidated unified master reference table)
2. `vendor_discrepancy_matrix.csv` (Isolating vendor pricing discrepancies)
3. `inventory_rebalancing_plan.csv` (Warehouse transfer routing maps)
4. `audit_report.csv` (A unified registry compiling every system violation caught)

### 🔄 Repeatable Automation Architecture
* Save a core reusable markdown file named `weekly_audit_prompt.md` in the workspace. This serves as the master template allowing the user to consistently coordinate the entire multi-stage evaluation pipeline in a single terminal execution block.

### 📋 Strict Capstone Output Format
The final capstone evaluation script must synthesize all historical lab rules and generate a clean console string matching this exact casing and spacing structure:

```text
=== MARGIN LEAKAGE ALERT === Vendor: Apex Logistics — Q2 Consolidated
HIGH SEVERITY ISSUES:
Duplicate billing: $X,XXX.XX (line X)
Data errors: $X,XXX.XX (line X — negative qty)
Currency exposure: $X,XXX.XX (line X — EUR not USD)
MEDIUM SEVERITY:
Invalid HS codes: X lines
Late deliveries: X lines ($XX,XXX value at risk)
Restricted items without license: X lines
TOTAL ESTIMATED MARGIN LEAKAGE: $XX,XXX.XX RECOMMENDED ACTION: Hold payment pending vendor correction.