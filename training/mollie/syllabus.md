# Sales & Financials: Order-to-Profit Analysis with Claude Code

**Course Title:** Order-to-Profit Analysis with Claude Code
**Target User:** Mollie — Sales & Financials team
**Prerequisites:** Familiarity with Shopify admin, basic CSV/spreadsheet experience; no coding experience required.
**Estimated Duration:** 6 hours (split across three 2-hour sessions)
**Format:** Live walkthrough + hands-on terminal exercises

---

## Pre-Work: Load Your Institutional Memory

Before starting this course, open the [Master Claude Code Guide](https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1) alongside your domain-specific NotebookLM notebook. Query both notebooks to understand how Claude Code operates in your domain before writing any scripts or building tools.

**Your Domain Notebook:** [Mollie's Sales Notebook](https://notebooklm.google.com/notebook/2ab95bfd-ceeb-436d-b41f-85a89e3ca749?authuser=1)

> **Workflow Rule:** All script generation, data testing, or document templating in this track must cross-verify patterns against both the Master Guide and your Domain Notebook before execution.

---

## Learning Objectives

By the end of this course, Mollie will be able to:

1. Load and inspect raw Shopify order exports and webhook payloads in Claude Code.
2. Join advertising spend data with gross sales data to calculate true profit per channel.
3. Calculate and track profit margin trends across products, channels, and time periods.
4. Detect anomalies — outliers, missing orders, margin compression, and data gaps.
5. Generate a consolidated profit-and-loss report from disparate data sources.
6. Build a reusable weekly sales-review prompt template.
7. Reconcile payment settlement reports against order ledgers to isolate payout mismatches and platform fee discrepancies.
8. Parse data observability alerts and format structured Slack/Teams webhook JSON payloads for operations response.

---

## Lesson Breakdown

### Lesson 1 — Loading Shopify Order Data (60 min)

**Objective:** Pull orders from Shopify into Claude Code and understand the data shape.

| Segment | Topic | Activity |
|---|---|---|
| 1.1 | Where the data lives | Shopify admin → Orders → Export CSV. Also: webhook JSON payloads from the Shopify "orders/create" topic. |
| 1.2 | Loading an order export CSV | Load `data/shopify_orders_2026-06.csv` and inspect columns: order ID, line items, totals, discounts, shipping, taxes. |
| 1.3 | Loading a webhook JSON payload | Load a raw `data/shopify_webhook_sample.json` — nested JSON with order items, customer data, and fulfillment status. |
| 1.4 | Flattening nested data | Ask Claude to unroll line items from the webhook payload into a flat table (one row per line item). |
| 1.5 | Filtering and scoping | Filter by date range, order status (paid vs. pending vs. cancelled), and sales channel (online, POS, wholesale). |

**CLI Exercises:**

```
# Exercise 1.2 — Inspect a Shopify order export
claude data/shopify_orders_2026-06.csv
```

Prompt:

```
Read data/shopify_orders_2026-06.csv and tell me:
- How many rows and columns
- What each column name is
- Which date range is covered (look for the "created_at" column)
- The total gross sales amount across all rows
- How many orders are cancelled vs. completed vs. pending
```

```
# Exercise 1.3 — Load a webhook JSON payload
claude data/shopify_webhook_sample.json
```

Prompt:

```
This is a Shopify "orders/create" webhook payload. Walk me through:
- What order ID and order number is this?
- How many line items are in the order?
- What is the total price, subtotal, and shipping cost?
- What payment gateway was used?
- What is the "landing_site" or "referring_site" value?
```

```
# Exercise 1.4 — Flatten line items
Prompt (continuing the same session):

Take the line_items array from this webhook and flatten it into a table.
One row per line item. Columns: order_id, order_number, item_name, sku,
quantity, price, total_discount, total_line_item.

Also expand the "tax_lines" for each item — if taxes exist, add a
tax_rate column.
```

---

### Lesson 2 — Joining Ad Spend with Gross Sales (60 min)

**Objective:** Match advertising spend data to Shopify sales data and calculate net results per channel.

| Segment | Topic | Activity |
|---|---|---|
| 2.1 | The reconciliation problem | Ad spend comes from Google Ads / Meta dashboards (CSV). Sales come from Shopify. They use different date labels, channel names, and granularity. |
| 2.2 | Loading the ad spend matrix | Load `data/ad_spend_june_2026.csv` — columns: date, channel, campaign, spend, impressions, clicks. |
| 2.3 | Loading the sales table | Load `data/shopify_orders_2026-06.csv` alongside it. |
| 2.4 | Joining on date + channel | Instruct Claude to aggregate daily gross sales by channel, then join with the ad spend table on `date` and `channel`. |
| 2.5 | Calculating net income | Compute `net = gross_sales - ad_spend` per channel per day. Find which channels are losing money. |

**CLI Exercises:**

```
# Exercise 2.4 — Join ad spend with sales
claude data/ad_spend_june_2026.csv data/shopify_orders_2026-06.csv
```

Prompt:

```
I have two files:
1. data/ad_spend_june_2026.csv — columns: date, channel, campaign, spend, impressions, clicks
   - "channel" values are: "google_shopping", "google_search", "meta_newsfeed", "meta_stories",
     "email", "organic", "direct"
2. data/shopify_orders_2026-06.csv — columns: order_id, created_at, total_price, channel, ...

Step 1: Aggregate the Shopify orders by date and channel. For each (date, channel) pair,
sum up total_price as gross_sales.

Step 2: Join the aggregated sales with the ad spend table on date and channel.
Use a LEFT JOIN — keep every ad spend row even if there were no sales.

Step 3: Show me the joined table with columns:
date, channel, spend, gross_sales, (gross_sales - spend) as net

Step 4: Highlight every row where net is negative.
```

```
# Exercise 2.5 — Channel profitability summary
Prompt (continuing the same session):

Roll up the joined table by channel. For each channel, show me:
- Total spend
- Total gross sales
- Net (gross - spend)
- ROAS (gross / spend), rounded to 2 decimals

Sort by net descending. Which channels are unprofitable?
```

---

### Lesson 3 — Profit Margin Tracking (60 min)

**Objective:** Calculate and monitor profit margins at the product, order, and channel level.

| Segment | Topic | Activity |
|---|---|---|
| 3.1 | What goes into a margin | COGS (cost of goods sold), shipping, transaction fees, discounts, and ad spend. Each lives in a different data source. |
| 3.2 | Loading the cost data | Load `data/product_cogs.csv` (SKU → unit cost) and `data/shopify_fees.csv` (transaction fees per order). |
| 3.3 | Joining COGS to orders | Match each line item's SKU to its COGS, then calculate `item_margin = (item_price - unit_cost) / item_price`. |
| 3.4 | Full-profit order view | For each order: `order_margin = (total_revenue - total_cogs - shipping - fees - discounts) / total_revenue`. |
| 3.5 | Margin reporting by channel | Average margin % per channel. Flag any channel where margin dropped more than 5% month-over-month. |

**CLI Exercises:**

```
# Exercise 3.3 — Add COGS to line items
claude data/shopify_orders_2026-06.csv data/product_cogs.csv
```

Prompt:

```
I have two files:
1. data/shopify_orders_2026-06.csv — columns include: order_id, item_sku, item_price, quantity, ...
2. data/product_cogs.csv — columns: sku, unit_cost, supplier

Step 1: For every line item row in the orders file, look up the matching
unit_cost from data/product_cogs.csv by SKU.

Step 2: Calculate:
   line_revenue = item_price * quantity
   line_cogs    = unit_cost * quantity
   line_margin  = (line_revenue - line_cogs) / line_revenue * 100

Step 3: Flag every line item where line_margin < 15%.
Those are low-margin products — we need to watch them.

Step 4: What is the minimum, maximum, and average margin across all line items?
```

```
# Exercise 3.5 — Channel margin comparison
claude data/shopify_orders_2026-06.csv data/product_cogs.csv data/shopify_fees.csv
```

Prompt:

```
Load all three files. Use the orders, COGS, and transaction fees to calculate
the average profit margin per sales channel.

For each order:
  total_net = total_price - total_cogs - shipping_cost - transaction_fee

Margin (%) = (total_net / total_price) * 100

Group by channel and show: channel, avg_margin(%), total_net, total_revenue.
Sort by avg_margin ascending (worst first).

Then tell me: which channel has the thinnest margin, and by how much
does it trail the best-performing channel?
```

---

### Lesson 4 — Anomaly Detection & Weekly Workflow (60 min)

**Objective:** Spot data anomalies and package everything into a repeatable weekly review.

| Segment | Topic | Activity |
|---|---|---|
| 4.1 | Types of anomalies | Missing days (no orders on a weekday), margin dips, zero-revenue ad spend days, spike in cancelled orders, outlier order totals. |
| 4.2 | Detecting gaps in the order log | Ask Claude to scan the date column and flag any calendar dates with zero orders. |
| 4.3 | Statistical outliers | Instruct Claude to flag orders where `total_price` is more than 3 standard deviations from the mean. |
| 4.4 | Margin anomaly alerts | Compare each product's current margin to its trailing 4-week average. Flag drops beyond a threshold. |
| 4.5 | Building the weekly sales-review prompt | Create a single prompt that loads all data sources, runs the full pipeline, and writes a report. |

**CLI Exercises:**

```
# Exercise 4.2 — Find missing dates
claude data/shopify_orders_2026-06.csv
```

Prompt:

```
Scan the "created_at" column and build a list of every calendar date from
the earliest order to the latest order. Mark any weekday (Monday–Friday)
that has zero orders as a MISSING DATE.

Show me the list of missing dates, if any. Also count how many weekends
(Saturday–Sunday) had orders — those may indicate off-hours fulfillment.
```

```
# Exercise 4.3 — Price outlier detection
Prompt (continuing the same session):

Calculate the mean and standard deviation of "total_price" across all orders.

Flag any order where:
  abs(order_total - mean) > 3 * standard_deviation

For each outlier, show: order_id, total_price, mean, std_dev, z_score.
Explain what might cause this — is it a wholesale bulk order, a refund,
or a data error?
```

```
# Exercise 4.5 — Full weekly review
claude data/shopify_orders_2026-06.csv data/product_cogs.csv data/shopify_fees.csv data/ad_spend_june_2026.csv < weekly_sales_review.md
```

**weekly_sales_review.md** (create this file during the lesson):

```markdown
I have four files loaded:
1. data/shopify_orders_2026-06.csv — all June orders
2. data/product_cogs.csv — cost of goods per SKU
3. data/shopify_fees.csv — transaction fees per order
4. data/ad_spend_june_2026.csv — advertising spend by channel and day

Please do the following, in order:

## Step 1 — Data integrity check
- Scan for missing dates (weekdays with zero orders)
- Flag any order totals that are >3 standard deviations from the mean
- Report any rows with null/missing values

## Step 2 — Profit margin by product
- Join orders with COGS
- Calculate margin % per line item
- Flag every product where margin < 15%

## Step 3 — Ad spend reconciliation
- Aggregate daily gross sales by channel
- Join with ad spend on (date, channel)
- Report net income per channel
- Highlight unprofitable channels (negative net)

## Step 4 — Report
- Write a consolidated CSV called weekly_sales_report.csv with these sheets/sections:
  1. "margin_by_product" — SKU, margin%, change_vs_last_month
  2. "channel_pnl" — channel, gross, spend, net, roas
  3. "anomalies" — type, order_id, date, value, threshold, notes
- Print a terminal summary with total revenue, total ad spend, blended margin, and anomaly count
```

---

### Lesson 5 — Payment Reconciliation Engine (60 min)

**Objective:** Cross-reference payment settlement reports against the order ledger to isolate financial drops, platform fee discrepancies, and missing transactions.

| Segment | Topic | Activity |
|---|---|---|
| 5.1 | The reconciliation problem | Payment gateways (Stripe, PayPal) send settlement reports. The order ledger tracks every order. Discrepancies between them mean missing money or unaccounted fees. |
| 5.2 | Loading settlement and ledger data | Load `data/payout_reconciliation.csv` alongside `data/shopify_orders_2026-06.csv` — two views of the same transactions, with intentional mismatches. |
| 5.3 | Full outer join cross-reference | Perform a full outer join on transaction_id. Classify each row: matched OK, amount mismatch, missing from ledger, missing from settlement. |
| 5.4 | Platform fee audit | For each gateway, calculate expected fees vs. actual fees. Flag overcharges and inconsistent fee percentages. |
| 5.5 | Payout gap calculation | Sum settled net amounts vs. expected payout total. Isolate which transactions are missing from payout batches and flag pending/voided statuses. |

**CLI Exercises:**

```
# Exercise 5.3 — Full reconciliation cross-reference
claude data/payout_reconciliation.csv data/shopify_orders_2026-06.csv
```

Prompt:

```
Load data/payout_reconciliation.csv and data/shopify_orders_2026-06.csv.

Step 1: Normalize column names. Map the settlement file's
transaction_id → order_id, gross_amount → total_price, fee → transaction_fee.

Step 2: Perform a FULL OUTER JOIN on transaction_id (settlement) / order_id
(ledger). For each row, classify as:
- "matched" — present in both files and amounts agree within $0.01
- "amount mismatch" — present in both but amounts differ by more than $0.01
- "settlement only" — in settlement file but not in order ledger
- "ledger only" — in order ledger but not in settlement file

Step 3: Output a discrepancy table with all non-matched rows.

Step 4: Calculate total settled amount, total ledger amount, and the
net difference.
```

```
# Exercise 5.4 — Fee audit by gateway
Prompt (continuing the same session):

Using the joined dataset:

1. Group by gateway (stripe vs. paypal).
2. For each gateway, calculate:
   - Total gross amount processed
   - Total fees charged
   - Average fee percentage (total_fees / total_gross * 100)
   - Transaction count
3. Compare against expected fee rates:
   - Stripe: 2.9% + $0.30 per transaction
   - PayPal: 3.5% + $0.49 per transaction
4. Flag any gateway where actual avg fee rate exceeds expected by
   more than 0.5 percentage points.

Output a gateway fee audit table with expected vs. actual rates.
```

```
# Exercise 5.5 — Payout gap isolation
Prompt (continuing the same session):

Using the reconciliation results:

1. List all transactions where payout_id is missing (status = "pending").
   Why might each one be pending?
2. Calculate the expected total payout = SUM(net_amount) for all
   settled transactions.
3. Compare against the actual payouts by payout_id. Is there a gap?
4. Identify transactions with "refunded" or "voided" status.
   Should these be excluded from the expected payout?

Output a payout gap summary table.
```

---

### Lesson 6 — Anomaly Alert Webhook Automation (60 min)

**Objective:** Parse data observability alerts and generate structured Slack/Teams webhook JSON payloads for real-time operations notification.

| Segment | Topic | Activity |
|---|---|---|
| 6.1 | Alerting and observability | Data pipelines generate alerts for freshness drops, volume anomalies, and schema changes. These need to reach operations in their messaging platform of choice. |
| 6.2 | Loading a Monte Carlo alert | Load a simulated Monte Carlo alert JSON — a freshness alert on the orders table with severity, observed value, and threshold. |
| 6.3 | Alert classification and severity mapping | Classify the alert dimension (freshness, volume, null_ratio, schema_change) and assign severity (CRITICAL, WARNING, INFO) based on magnitude. |
| 6.4 | Slack webhook payload generation | Transform the alert into a Slack Block Kit JSON payload with header, fields table, message, and investigation button. |
| 6.5 | Teams webhook payload generation | Transform the same alert into a Microsoft Teams Adaptive Card JSON payload with matching content. |

**CLI Exercises:**

```
# Exercise 6.2 — Load and classify an alert
```

Prompt:

```
I have a simulated Monte Carlo alert JSON:

{
  "id": "mc_alert_001",
  "table_name": "public.orders",
  "dimension": "freshness",
  "severity": "critical",
  "actual_value": "Last update 6 hours ago",
  "threshold": "Last update within 1 hour",
  "triggered_at": "2026-07-02T08:15:00Z",
  "description": "The orders table has not received new data for 6 hours. Expected refresh interval is 1 hour.",
  "url": "https://getmontecarlo.com/monitor/orders-freshness"
}

Classify this alert:
- Dimension: freshness / volume / null_ratio / distribution / schema_change?
- Severity: critical / warning / info?
- Suggested Slack channel: what should it be?
```

```
# Exercise 6.4 — Generate Slack webhook JSON
Prompt (continuing the same session):

Generate a Slack Block Kit webhook payload for the alert above.

Rules:
- Channel: #data-ops-alerts-critical for CRITICAL, #data-ops-alerts-warnings for WARNING
- Use the Block Kit format with header, section fields, and actions blocks
- Include an "Investigate in Monte Carlo" button pointing to the alert URL
- The message field must be in a section block, not the header

Output the complete JSON payload.
Validate it: no trailing commas, valid JSON, all variables resolved.
```

```
# Exercise 6.5 — Generate Teams webhook JSON
Prompt (continuing the same session):

Generate a Microsoft Teams Adaptive Card payload for the same alert.

Rules:
- Use Adaptive Card schema version 1.4
- Use FactSet for the key-value pairs
- Color the header based on severity (attention for CRITICAL, warning for WARNING)
- Include an Action.OpenUrl for investigation

Output the complete JSON payload. Validate it.
```

---

## Sample Data Files

The following sample files are provided in `data/` for use during exercises:

| File | Description |
|---|---|
| `data/shopify_orders_2026-06.csv` | 20 Shopify orders from June 2026 across 6 channels |
| `data/shopify_webhook_sample.json` | Single "orders/create" webhook payload (nested JSON) |
| `data/product_cogs.csv` | COGS master list (20 SKUs with unit cost and supplier) |
| `data/shopify_fees.csv` | Transaction fees per order (payment gateway + flat fee) |
| `data/ad_spend_june_2026.csv` | Daily ad spend by channel (Google, Meta, email, organic) |
| `data/payout_reconciliation.csv` | Payout settlement report with 36 transactions across Stripe and PayPal, including pending, refunded, and voided edge cases |

---

## Link Directory

| Resource | Path / Location |
|---|---|
| Course slide deck | `training/mollie/` |
| Sample data assets | `training/mollie/data/` |
| Exercise 1 — Incident Root-Cause Profiling | `training/mollie/exercises/exercise_1.md` |
| Exercise 2 — Deep-Dive Data Freshness Verification | `training/mollie/exercises/exercise_2.md` |
| Exercise 3 — Automated Financial Reconciliation Engine | `training/mollie/exercises/exercise_3.md` |
| Exercise 4 — Multi-Source Webhook Payload Orchestration | `training/mollie/exercises/exercise_4.md` |
| Exercise 5 — Capstone Data Observability & Alerting Pipeline | `training/mollie/exercises/exercise_5.md` |
| Shopify sales mock data | `training/mollie/data/shopify_sales.csv` |
| Marketing spend mock data | `training/mollie/data/marketing_spend.csv` |
| csv-analytics skill | `skills/csv-analytics/SKILL.md` |
| reconciliation-engine skill | `skills/reconciliation-engine/SKILL.md` |
| anomaly-alert-webhook skill | `skills/anomaly-alert-webhook/SKILL.md` |
| xlsx-processing skill | `../sunny/skills/xlsx-processing/SKILL.md` |
| data-table-validator skill | `../sunny/skills/data-table-validator/SKILL.md` |

---

## Success Criteria

Mollie can independently:

- [ ] Load and summarise a Shopify order CSV and a webhook JSON payload
- [ ] Flatten nested JSON line items into a flat table
- [ ] Join ad spend data with gross sales and flag unprofitable channels
- [ ] Calculate profit margins at the product, order, and channel level
- [ ] Detect missing dates, price outliers, and margin compression
- [ ] Run the full weekly sales-review pipeline using the saved prompt template
- [ ] Reconcile settlement reports against order ledgers and isolate payout mismatches
- [ ] Generate platform-specific webhook JSON payloads from observability alerts
