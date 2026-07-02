# Sales & Licensing Labs — Advanced Terminal Exercises

Two production-grade exercises for Mollie to sharpen her cross-source analytics and licensing audit skills.

---

## Exercise 1: Disparate Ad-Spend & Revenue Join

### Scenario

Mollie needs to answer a question for the CFO: **which sales channels are actually profitable after accounting for advertising spend?** The Shopify sales data lives in one CSV, and the marketing spend data lives in another. They use different column names, different channel labels, and overlap only partially on dates. Mollie needs to join them, calculate net margins per channel, and identify which campaigns are burning cash.

### Dataset

Two files are provided in this directory:

| File | Description |
|---|---|
| `shopify_sales.csv` | 98 orders across June 2026 — includes dates, channels, SKUs, gross/net sales, shipping, fees |
| `marketing_spend.csv` | Daily ad spend by channel and campaign — includes spend, impressions, clicks, target SKU |

### Data Challenges Planted

| Challenge | Detail |
|---|---|
| Schema mismatch | Spend file uses `channel`; sales file uses `channel` directly but with different channel labels (e.g., `google_shopping` vs. `PLA_Gadget_Q2` campaign naming) |
| Missing days | Some days have sales but zero ad spend recorded (organic/direct traffic) |
| Inconsistent channel labels | `meta_newsfeed` in sales matches `FB_*` campaigns in spend — must normalise |
| Spend with no return | Certain days have ad spend but zero associated sales — those need to be surfaced |
| `ALL` target SKU | Email campaigns target `ALL` rather than a specific SKU — must treat as general marketing |

### Walkthrough Steps

```
claude shopify_sales.csv marketing_spend.csv
```

Alternatively, load both files with the csv-analytics skill:

```
claude shopify_sales.csv marketing_spend.csv --skill csv-analytics
```

**Step 1 — Schema inventory:**

Ask Claude to read both files and print a summary of each.

```
Step 1 Prompt:
I have two files loaded:
1. shopify_sales.csv — order-level sales data
2. marketing_spend.csv — daily ad spend data

For each file, tell me:
- Row count and column names
- Date range covered
- Unique values in any "channel" or "campaign" columns
- Whether there are any blank or null cells
```

**Step 2 — Normalise channel names:**

Channels in the sales file and campaigns in the spend file use different naming conventions. Build a mapping.

```
Step 2 Prompt:
The sales file uses channel values: google_shopping, meta_newsfeed, email, organic, direct, wholesale
The spend file uses campaign values that imply a channel.

Build a normalisation map:
- Any campaign starting with "PLA_" → channel = "google_shopping"
- Any campaign starting with "FB_" → channel = "meta_newsfeed"
- Any campaign starting with "Newsletter" → channel = "email"
- "organic", "direct", "wholesale" have no associated spend — they are zero-cost channels

Show me the mapping you built and ask me to confirm before proceeding.
```

**Step 3 — Aggregate daily sales by channel:**

```
Step 3 Prompt:
Aggregate shopify_sales.csv by date and channel:
- For each (date, channel) pair, calculate:
  - total_gross = sum(gross_sales)
  - total_net = sum(net_sales)
  - total_shipping = sum(shipping)
  - total_fees = sum(fees)
  - order_count = count(order_id)

Show me the first 10 rows of the aggregated table sorted by date.
```

**Step 4 — Join with ad spend (FULL OUTER JOIN):**

```
Step 4 Prompt:
Take the aggregated sales table and the marketing_spend.csv table.
Join them on (date, channel) using a FULL OUTER JOIN.

After the join:
- Fill null spend values with 0
- Fill null sales values with 0
- Flag any row where spend > 0 and gross_sales = 0 as "spend_with_no_return"
- Flag any row where gross_sales > 0 and spend = 0 as "organic_traffic"

Show me the joined table with columns:
date, channel, spend, gross_sales, net_sales, total_fees, order_count
```

**Step 5 — Calculate net margin per channel:**

```
Step 5 Prompt:
For every row in the joined table, calculate:
  net_profit = gross_sales - spend - total_fees
  margin_pct = (net_profit / gross_sales) * 100
    (set to NULL if gross_sales = 0)
  roas = gross_sales / spend
    (set to NULL if spend = 0)

Then group by channel and show:
  channel, total_spend, total_gross_sales, total_net_profit, avg_margin_pct, roas

Sort by avg_margin_pct descending.
Which channels have negative margin?
```

**Step 6 — Flag anomalies:**

```
Step 6 Prompt:
Identify these anomalies and write them to a CSV:

1. Days where spend > 0 and gross_sales = 0 (money spent, nothing sold)
2. Days where spend > gross_sales * 2 (spend more than double the revenue)
3. Channels with overall negative net profit
4. Top 3 most expensive campaigns by total spend

Write all findings to ad_spend_anomalies.csv.
```

**Step 7 — Final profitability summary:**

```
Step 7 Prompt:
Print a terminal summary:

=== CHANNEL PROFITABILITY — JUNE 2026 ===
Total gross sales:     $XX,XXX.XX
Total ad spend:        $X,XXX.XX
Total fees:            $X,XXX.XX
Total net profit:      $XX,XXX.XX
Blended margin:        XX.X%

Profitable channels:
  1. Channel X — $X,XXX net (XX% margin)
  2. ...

Unprofitable channels:
  1. Channel X — -$XXX net (negative margin)

Days with spend/no return: X
Total wasted spend:        $X,XXX.XX
```

---

## Exercise 2: License Seat Discrepancy Audit

### Scenario

Mollie manages a B2B SaaS product called **DataSync Pro** that is sold on a per-seat licensing model. Customers buy a certain number of licenses each month, and usage is tracked daily via the product's telemetry. The licensing team has a dispute with **Acme Corp** — Acme claims they only use 45 seats but the telemetry data shows 58 unique users last month. Mollie needs to write a Python loop (inside Claude Code) that audits the seat usage day-by-day, identifies the discrepancy pattern, and produces an evidence file for the dispute.

### Dataset

Save the following two tables as separate files and load them into Claude Code.

**`acme_licenses.csv`** — License entitlement per month:

```csv
customer_id,customer_name,license_type,contract_start,contract_end,total_seats_purchased,seats_allocated,month
CUST-0042,Acme Corp,Enterprise,2026-01-01,2026-12-31,50,50,2026-06
CUST-0042,Acme Corp,Enterprise,2026-01-01,2026-12-31,50,50,2026-05
CUST-0042,Acme Corp,Enterprise,2026-01-01,2026-12-31,50,50,2026-04
CUST-0042,Acme Corp,Enterprise,2026-01-01,2026-12-31,50,50,2026-03
CUST-0187,Beta Industries,Professional,2026-03-01,2026-12-31,25,20,2026-06
CUST-0187,Beta Industries,Professional,2026-03-01,2026-12-31,25,20,2026-05
CUST-0331,Gamma LLC,Starter,2026-02-01,2026-12-31,10,10,2026-06
CUST-0331,Gamma LLC,Starter,2026-02-01,2026-12-31,10,10,2026-05
CUST-0331,Gamma LLC,Starter,2026-02-01,2026-12-31,10,10,2026-04
```

**`acme_usage_june.csv`** — Daily active seat usage for June 2026:

```csv
date,customer_id,active_seats,unique_users,total_api_calls,peak_concurrent
2026-06-01,CUST-0042,44,48,12500,38
2026-06-02,CUST-0042,45,49,13100,40
2026-06-03,CUST-0042,46,50,12800,42
2026-06-04,CUST-0042,45,49,12200,41
2026-06-05,CUST-0042,47,51,13500,43
2026-06-06,CUST-0042,42,46,11800,38
2026-06-07,CUST-0042,40,44,11200,36
2026-06-08,CUST-0042,48,52,14100,44
2026-06-09,CUST-0042,49,53,14500,45
2026-06-10,CUST-0042,50,54,15200,46
2026-06-11,CUST-0042,50,55,14800,47
2026-06-12,CUST-0042,51,56,15300,48
2026-06-13,CUST-0042,49,54,14600,46
2026-06-14,CUST-0042,48,53,14200,44
2026-06-15,CUST-0042,52,57,15800,49
2026-06-16,CUST-0042,53,58,16200,50
2026-06-17,CUST-0042,54,59,16800,52
2026-06-18,CUST-0042,55,60,17100,53
2026-06-19,CUST-0042,53,58,16500,51
2026-06-20,CUST-0042,52,57,16100,49
2026-06-21,CUST-0042,50,55,15500,47
2026-06-22,CUST-0042,51,56,15800,48
2026-06-23,CUST-0042,53,58,16300,50
2026-06-24,CUST-0042,54,59,16700,52
2026-06-25,CUST-0042,55,60,17000,53
2026-06-26,CUST-0042,54,59,16600,51
2026-06-27,CUST-0042,52,57,16000,49
2026-06-28,CUST-0042,50,55,15400,47
2026-06-29,CUST-0042,48,53,14800,45
2026-06-30,CUST-0042,46,51,14000,43
```

### Discrepancy Pattern Built Into the Data

| Observation | Detail |
|---|---|
| Acme claims 45 seats used | Their contention is that `active_seats` hovers around 45–55 |
| Actual `unique_users` | Ranges from 44 to 60 — **peaks at 60 on June 18 and June 25** |
| Licenses purchased | 50 seats paid, 50 allocated |
| Overage pattern | Usage grows through the month, exceeding 50 after June 10, peaking at 60 in the third week — consistent with a month-end project push |
| `unique_users` vs `active_seats` | `unique_users` always exceeds `active_seats` by 3–6 — suggests shared seats or floating licensing |

### Walkthrough Steps

```
claude acme_licenses.csv acme_usage_june.csv
```

**Step 1 — Load and inspect:**

```
Step 1 Prompt:
I have two files:
1. acme_licenses.csv — license entitlements per customer
2. acme_usage_june.csv — daily active seat usage for June 2026

Filter both files to customer CUST-0042 (Acme Corp) only.
Tell me:
- How many seats Acme purchased
- The date range of the usage data
- The min, max, and average active_seats and unique_users for the month
```

**Step 2 — Identify overage days:**

```
Step 2 Prompt:
Acme Corp purchased 50 seats. For each day in the usage data, calculate:
  seat_overage = active_seats - 50  (negative means under, positive means over)
  user_overage = unique_users - 50

Flag any day where either value is > 0.

Show me a table: date, active_seats, seats_over_50, unique_users, users_over_50
How many days had more than 50 active seats? How many had more than 50 unique users?
```

**Step 3 — Write a Python loop for audit (inside Claude Code):**

```
Step 3 Prompt:
Write and execute a Python script that does the following audit. Run it inside Claude Code:

```python
import csv
from collections import defaultdict

# Read the license file
licenses = []
with open("acme_licenses.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        licenses.append(row)

# Read the usage file
usage = []
with open("acme_usage_june.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        usage.append(row)

# Filter to Acme Corp (CUST-0042)
acme_license = [r for r in licenses if r["customer_id"] == "CUST-0042"]
acme_usage = [r for r in usage if r["customer_id"] == "CUST-0042"]

if not acme_license:
    print("ERROR: No license record found for CUST-0042")
    exit(1)

seats_purchased = int(acme_license[0]["total_seats_purchased"])

# Audit each day
violations = []
total_overage_days = 0
peak_unique = 0
peak_active = 0

for day in acme_usage:
    active = int(day["active_seats"])
    unique = int(day["unique_users"])
    date = day["date"]

    if active > peak_active:
        peak_active = active
    if unique > peak_unique:
        peak_unique = unique

    if active > seats_purchased:
        violations.append({
            "date": date,
            "type": "active_seats_overage",
            "value": active,
            "over_by": active - seats_purchased
        })
        total_overage_days += 1

    if unique > seats_purchased:
        violations.append({
            "date": date,
            "type": "unique_users_overage",
            "value": unique,
            "over_by": unique - seats_purchased
        })

# Generate summary
print("=== LICENSE AUDIT: Acme Corp (CUST-0042) ===")
print(f"Seats purchased: {seats_purchased}")
print(f"Period: {acme_usage[0]['date']} to {acme_usage[-1]['date']}")
print(f"Days with overage: {total_overage_days} / {len(acme_usage)}")
print(f"Peak active seats: {peak_active} (over by {max(0, peak_active - seats_purchased)})")
print(f"Peak unique users: {peak_unique} (over by {max(0, peak_unique - seats_purchased)})")
print(f"Total violations: {len(violations)}")
print()

# Write violations to CSV
with open("acme_license_audit.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "type", "value", "over_by", "notes"])
    writer.writeheader()
    for v in violations:
        v["notes"] = f"{v['type']} exceeds {seats_purchased} seat license by {v['over_by']}"
        writer.writerow(v)

print("Written: acme_license_audit.csv")
print()

# Monthly summary for billing
total_overage_user_days = sum(
    v["over_by"] for v in violations if v["type"] == "unique_users_overage"
)
print("BILLING IMPACT ESTIMATE")
print(f"Total overage user-days: {total_overage_user_days}")
print(f"Average daily overage: {total_overage_user_days / len(acme_usage):.1f} users")
```

Run this script and report what it found.
```

**Step 4 — Segment the overage pattern:**

```
Step 4 Prompt:
Look at the overage pattern over time. The usage data shows a clear trend:
- Early June (days 1–9): generally under 50 seats
- Mid June (days 10–20): consistently over 50 seats, growing to a peak
- Late June (days 21–30): still over but declining

Calculate the average overage for each week:
  Week 1 (June 1–7):  avg unique_users
  Week 2 (June 8–14): avg unique_users
  Week 3 (June 15–21): avg unique_users
  Week 4 (June 22–30): avg unique_users

Which week had the highest average overage? What might explain this pattern?
```

**Step 5 — Final evidence pack:**

```
Step 5 Prompt:
Write a single CSV called acme_license_dispute_evidence.csv with the following sections:

1. Summary row: customer, seats_purchased, peak_usage, max_overage, total_overage_days
2. Detail rows: one row per day with date, active_seats, unique_users, active_overage, user_overage, notes
3. Footer row: totals

Also print a terminal summary suitable for attaching to the dispute email:

=== LICENSE DISPUTE EVIDENCE: Acme Corp ===
Customer:      Acme Corp (CUST-0042)
License type:  Enterprise (50 seats)
Period:        June 2026

Acme claims:        45 active seats (disputed)
Our records show:
  Peak active seats:   XX (over by X on XX Jun)
  Peak unique users:  XX (over by X on XX Jun)
  Days over 50 seats:  XX of 30 days

Conclusion: Acme Corp exceeded their 50-seat license on XX days in June 2026,
with a peak overage of X seats. The month-end project push (Jun 15–25) drove
the highest usage. Acme's claim of 45 seats is not supported by telemetry.
Recommended action: Invoice for overage per contract terms.
```

---

## Data File Reference

| File | Exercise | Description |
|---|---|---|
| `shopify_sales.csv` | Exercise 1 | 98 Shopify orders, June 2026, with channel + SKU detail |
| `marketing_spend.csv` | Exercise 1 | Daily ad spend by channel + campaign, June 2026 |
| `acme_licenses.csv` | Exercise 2 | License entitlement records for 3 customers |
| `acme_usage_june.csv` | Exercise 2 | Daily active seat and unique user telemetry for Acme Corp |

### Cross-Reference: Syllabus & Skills

| Resource | Purpose | Path |
|---|---|---|
| Sales & Financials Syllabus | Full course outline for Mollie | `../syllabus.md` |
| csv-analytics skill | Automated join + profitability playbook | `../skills/csv-analytics/SKILL.md` |
| data-table-validator skill | Pricing/orphan detection (adjacent skill) | `../../sunny/skills/data-table-validator/SKILL.md` |
