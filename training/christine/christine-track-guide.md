# 📈 Marketing Automation Lab: Guide & Guardrails

Welcome to Christine's Marketing track. Before executing any automated scripts, deployment checks, or local data audits, use this guide alongside **NotebookLM (The Oracle)** to verify track constraints and flag intentional grading traps.

---

## 🛠️ 1. Automation & Token Constraints

Your scripts and validation passes must scan templates and configurations to isolate the following execution breaks:

### 🛑 Broken Token Syntax & Variables
* **Malformed Merge Tags:** Locate and flag the missing closing brace syntax (`{{customer.first_name.`).
* **Variable Mismatches:** Identify where templates use legacy `{{unsubscribe_link}}` fields and automatically update them to the required, active `{{unsubscribe_url}}`.
* **Missing Fallbacks:** Catch instances of greeting copy (e.g., `"Hey"`) lacking an explicit `{{first_name}}` token fallback.
* **Non-Functional Actions:** Ensure unsubscribe links are formatted as true, clickable URLs rather than raw, unlinked plain text.

### 📋 Missing Assets & KPIs
* **Metric Gaps:** Flag the Launch Dashboard and Weekly Report templates if they are missing defined performance metrics and key KPIs.
* **Missing Templates:** Block execution if the launch capstone sequence fails to detect that 3 core email assets are entirely missing their base templates.

---

## 📊 2. Data & Campaign Analytics Traps

The mock data tables, copy decks, and analytics feeds are intentionally seeded with structural and behavioral anomalies. 

### 🔤 Formatting & Copy Violations
* **Mixed Layout Tags:** Locate and strip out raw inline HTML (`<span style="...">`, `<div class="...">`, `<BR>`), empty tags, and legacy HTML comments polluting markdown text.
* **Brand Voice Violations:** Flag instances of passive voice, explicit competitor call-outs (e.g., Shopify, Mailchimp, Dropbox, Google Drive), unverified superlatives, and hyper-aggressive or fear-based messaging.

### 🔍 Search & Metadata Gaps (Exercise 2 & Capstone)
* **Missing SEO Tags:** Identify empty `title_tag` records on active listings (specifically `SKU-002`) and missing meta descriptions (`SKU-008`, `SKU-010`).
* **Unoptimized Media:** Catch generic image alt text blocks (e.g., `"Starter kit box"`) that fail brand keyword optimization.
* **Structural Duplication:** Flag when completely identical body HTML phrasing is lazily copied across separate products (`SKU-007` and `SKU-009`).
* **Keyword Under-indexing:** Enforce the presence of missing primary target keywords like `"enterprise security"`, `"file sharing"`, and `"cloud storage"`.

### 📉 Performance & Trend Failures (Exercise 4)
* **ROAS Failures:** Mark Display Prospecting campaigns (`DISP-2026-002` and `DISP-2026-004`) as unprofitable (ROAS < 1.0x). Flag all 4 social channels if they miss the strict 2.0x target baseline.
* **Funnel Degradation:** Identify the quarter-over-quarter drop in newsletter open rates (4.81% to 4.02%) and rising unsubscribes.
* **Search Drift:** Highlight the performance split where Brand search ROAS is scaling, but Non-Brand search drops below the 3.0x standard.

---

## 🎯 3. Core Validation Criteria

To successfully pass the grading gate, workflows and scripts must execute within these rigid guardrails:

### 🧠 Institutional Memory
* All programmatic script generation, data tests, and template builds **must cross-verify structural patterns** against the *Master Claude Code Guide* and *Christine's Domain Notebook* before executing.

### 📏 Channel Length & Component Constraints
* **Subject Lines:** Strict maximum of **60 characters**.
* **Preheaders:** Strict maximum of **130 characters**.
* **CTAs:** Every layout must enforce exactly **one primary Call-to-Action**. Flag and stop builds if auxiliary sections (Pricing/FAQs) lack a link or contain secondary competing directions.

### 🧮 Math, Scaling, & Pipeline Standards
* **Channel Health Score:** Calculate precisely on a 0–100 scale using this distribution:
  $$\text{Score} = (\text{ROAS} \times 0.40) + (\text{CTR} \times 0.20) + (\text{CVR} \times 0.20) + (\text{CPA} \times 0.20)$$
* **Outlier Detection:** Scripts must isolate data anomalies and trend breaks utilizing the statistical **Interquartile Range (IQR) method**.
* **Pipeline Integrity:** Monitor asset fulfillment and log structural errors if project trackers indicate high levels of incomplete modules (e.g., 5 out of 11 capstone components left as `not_started`). All end-state outputs must successfully parse out into structured, clean `.csv` schemas or print to terminal dashboards.