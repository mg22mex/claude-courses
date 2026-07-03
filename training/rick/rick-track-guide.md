# 📈 Executive Operations Lab: Guide & Guardrails

Welcome to Rick's Operations track. Before executing any raw log parsers, supply chain dependency mappers, or automated PRD builders, use this guide alongside **NotebookLM (The Oracle)** to verify track constraints and isolate intentional executive traps.

---

## 🛠️ 1. Operational Data & Scripting Traps

Your data extraction tools and evaluation scripts must parse unstructured logs and dependency sets to expose the following hidden operational risks:

### 🔤 Unstructured Log Anomalies (Exercise 1)
Your parsing engine must comb through raw text lines to flag five distinct system failures:
* A missed FedEx pickup stranding **1,200 delayed units**.
* An overdue purchase order (`PO-8812`) lingering with zero communication.
* A batch processing failure blocking **98 orders** (exactly a `0.8%` failure rate).
* A duplicate invoice instance (`INV-402`) stuck under review.
* Crucial inventory levels dropping safely below their reorder thresholds.

### 🛑 Single Points of Failure & Deficits (Exercise 2 & 5)
* **The Supply Chain Trap:** Ingest the inventory master lists to find the single point of failure: SKU `GADG-020` is exclusively housed at a single site (`WH-South`).
* **The Stock Deficits:** Flag multiple items sitting below reorder safety limits:
  * `WIDG-003` at `WH-North` (**42 units** remaining vs. a `150` reorder trigger).
  * `WIDG-002` at `WH-East`.
  * Both `GADG-001` and `SUPR-001` stuck at `WH-South`.

### 📝 Vague Business Concept Traps (Exercise 3)
* The PRD validation task feeds the agent four brief, single-sentence product ideas. Scripts must reject them or flag them as incomplete because they lack success criteria metrics. 
* Specifically, **Ideas 1 and 3** are missing data/integration constraints, while **Ideas 2 and 4** lack user segmentation profiles.

### 💸 Financial Value at Risk (Exercise 4 & 5)
Fulfillment databases blend routine shipping delays (UPS at 2 days late; USPS tracking up to 6 days late) with open-ended shipments missing delivery dates. Isolate the high-exposure target traps:
* **FedEx Shipments:** High-value risk entries tracking at **$12,000**, **$9,800**, and **$3,400**.
* **USPS Shipments:** A high-exposure transit lines holding **$6,500** at risk.

---

## 📐 2. System Constraints & Scaling Limits

Pipelines must enforce exact evaluation ranges and cross-reference organizational documentation boundaries:

### 🧠 Institutional Memory Gatekeeper
* All script generation, automated testing, or data templating **must cross-verify structural patterns** against both the *Master Claude Code Guide* and *Rick's Domain Notebook* prior to any local terminal execution.

### 🧮 Mathematical & Dataset Boundaries
* **Budget Variance Threshold:** Financial scripts must flag budget deviations that breach exactly **±5%**.
* **Log Extraction:** Exercise 1 scripts must successfully pull exactly **8–10 distinct quantitative metrics** from the raw text blocks.
* **Exact Item Counts:** Enforce rigid array and dataset validations:
  * A **12-entry** unstructured operational log file.
  * An inventory matrix mapping exactly **14 SKUs** across **3 warehouses**.
  * A strategic analysis dataset mapping **18 total SKU-warehouse combinations** across **4 logistics carriers**.

---

## 🎯 3. Core Validation & Output Rules

To clear the progressive executive track, workflows must output specific file naming structures and explicit data schemas:

### 📂 Exercise 1–4 Artifact Requirements
* **Exercise 1 (Logs):** Output a classified table of all 12 log entries, an extracted metrics sheet, a department risk heatmap flagging `Fulfillment` and `Procurement` as **"elevated risk,"** and a clean `executive_brief.md`.
* **Exercise 2 (Supply Chain):** Output a warehouse dependency graph (verifying `WH-North` as the most connected gateway), a critical site analysis identifying `WH-South` as a **HIGH risk** node, an `architecture_report.md`, and a clean `criticality_report.csv`.
* **Exercise 3 (Product):** Invoke the local `write-a-prd` tool to yield 4 structured PRD assets, an overview document named `prd_portfolio_summary.md`, and an explicit priority grid balancing timeline, risk, and impact.
* **Exercise 4 (Logistics):** Output a carrier performance matrix concluding that **USPS is the worst performer** (25% on-time) and **DHL is the best** (100%). Generate a `board_deck_outline.md` limited to exactly **8 slides** configured for downstream presentation automation.

### 🏁 Exercise 5: Capstone Master Deliverables
The capstone script must merge all tracking metrics to output:
1. `strategic_roadmap.md` (A comprehensive executive report spanning roughly 3–5 pages).
2. `strategic_roadmap.csv` (A machine-readable file outlining priority action steps).
3. A strategic operational health score calculated for every single SKU-warehouse pairing.
4. A dedicated index of "CRITICAL" items requiring instant executive intervention.