# 📊 Data Observability & Financial Reconciliation Lab: Guide & Guardrails

Welcome to Mollie's Sales and Financials track. Before executing any local pipeline scripts, data reconciliation engines, or alert webhooks, use this guide alongside **NotebookLM (The Oracle)** to verify track constraints and isolate intentional engineering traps.

---

## 🛠️ 1. Pipeline & Data Observability Traps

Your observability configurations and automated scripts must parse logs to differentiate true engineering root causes from cascading downstream symptoms:

### ⏱️ Freshness Cascades (Exercise 1)
* **The Root Cause:** A table freshness failure strikes the `orders` table precisely at **2:15 AM**.
* **Downstream Symptoms:** 
  * `volume_payments` artificially tanks in a step-down pattern: $125\text{K} \rightarrow 72\text{K} \rightarrow 45\text{K}$ due to the stale upstream data.
  * `null_rate_email` spikes from **12.5% to 18.7%** driven by broken SQL `JOIN` logic on the stale dataset.

### 📉 Degradation & Timeout Limits (Exercise 2)
* **The Performance Trap:** The pipeline's `Join` stage progressively degrades across execution runs ($16.5\text{m} \rightarrow 31.5\text{m} \rightarrow 43\text{m}$).
* **The Execution Wall:** Run `RUN-103` hits a hard timeout wall at **40 minutes (2,400 seconds)**, resulting in exactly **6,500 lost rows** relative to baseline.
* **Normal Behavior vs. Anomaly:** Do not flag expected data loss. The baseline data naturally features a `Normalize` stage that filters **200–400 rows** for quality, and an `Aggregate` stage that intentionally collapses row volume by **60%**.

### 🚨 Live Webhook Metric Breaches (Exercise 4)
Ingested payloads are hard-coded to trigger the following operational rule alerts:
* **CRITICAL:** `payments_volume` drops below **50,000**.
* **CRITICAL:** `queue_depth` exceeds **10,000**.
* **WARNING:** High API latency, transaction failures, and spiking 5xx error rates.

---

## 💸 2. Financial Reconciliation Errors

The internal accounting ledgers, Shopify pipelines, and gateway transaction files are seeded with settlement mismatches.

### 🔍 Payout Gaps & Fee Structures (Exercise 3)
* **Edge-Case Isolation:** Isolate a gateway timeout transaction (`TXN-20260602-005`), a customer dispute refund, a cancelled/voided order, and a mismatched record where ledger/gateway balances align but the metadata notes conflict.
* **Dynamic Fee Parsing:** Engines must dynamically apply distinct fee matrix logic for **Stripe** and **PayPal** to audit expected vs. actual processing costs.

### 💀 Raw Transaction Anomalies (Exercise 5 Capstone)
Audit the capstone raw data tables to scrub out:
* **Duplicate Billing:** Two identical transactions Sharing the same timestamp, payment amount, and `orderID`.
* **Data Errors:** A negative `-$50.00` ledger entry indicating an unmapped or undocumented reversal.
* **Stale Hangs:** A pending transaction left un-settled for **over 20 hours**.
* **Failed States:** An outright failed transaction block requiring root-cause documentation.

### 📉 Margin & Ad Spend Drops
* **Channel Drift:** Flag marketing channels suffering a month-over-month margin drop greater than **5%**.
* **Product Thresholds:** Measure product margins against a strict **trailing 4-week average**.
* **Data Gaps:** Catch calendar dates with zero orders ("missing days") and days featuring active ad spend but zero revenue.

---

## 🎯 3. Core Validation & Scoring Gateways

To pass the financial grading matrix, automated scripts must apply explicit formulas and output structured payloads.

### 🧮 Mathematical Rules & Join Strategies
* **Discrepancy Tolerance:** Enforcement must utilize a rigid **$0.01 tolerance threshold** between settlement sheets and the ledger.
* **Profit Calculations:** Gross profit metrics must map lines directly to COGS using the formula:
  $$\text{item\_margin} = \frac{\text{item\_price} - \text{unit\_cost}}{\text{item\_price}}$$
* **Order Margins:** Deduct COGS, shipping expenses, gateway fees, and applied discount codes from total gross revenue.
* **Outlier Detection:** Mark order totals that scale beyond **3 standard deviations** from the population mean ($3\sigma$).
* **Join Logic:** Reconciliation engines **must use a full outer join** between internal ledgers and processor reports to guarantee unmatched rows aren't dropped.
* **Bottleneck Isolation:** Compute stage-level delta logs using precise start/end timestamps to isolate pipeline bottlenecks.

### 📋 Structural Output Formats
* **CRITICAL Alerts:** Must output formatted as **Slack Block Kit JSON** payloads.
* **WARNING Alerts:** Must output formatted as **Microsoft Teams Adaptive Card JSON** payloads.
* **Batching Protocol:** WARNING alerts can be batched together; CRITICAL alerts **must never be batched** and must stream instantly.
* **Capstone Deliverable:** A unified, consolidated pipeline asset consisting of the formal audit report, the live JSON alert payload, and an investigation breakdown summary.