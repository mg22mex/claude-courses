# Exercise 5 — Capstone: The Automated Supply Chain Validator

## Scenario

A multi-page vendor invoice from **Apex Logistics** (Q2 consolidated) has arrived in a messy format. It contains pricing errors, duplicate lines, mismatched HS codes, expired delivery promises, and negative quantities. Sunny needs to run a full compliance audit and produce a consolidated report with margin leakage alerts.

This exercise combines skills from all prior exercises: schema normalisation (Ex1), lead-time verification (Ex2), tariff auditing (Ex3), and inventory impact analysis (Ex4).

## Learning Objectives

- Detect and clean common invoice data quality issues
- Cross-reference invoice data against master tariff and vendor tables
- Quantify margin leakage from pricing errors, duty overpayments, and duplicate billing
- Generate a unified executive alert

## Dataset

### Raw Vendor Invoice (`apex_q2_invoice.csv`)

```csv
line_id,po_number,item_description,hs_code,qty,unit_price,line_total,currency,order_date,promised_delivery,actual_delivery,notes
1,PO-8801,USB Flash Drive 128GB,8523.80,500,8.50,4250.00,USD,2026-04-01,2026-04-08,2026-04-07,
2,PO-8801,USB Flash Drive 128GB,8523.80,500,8.50,4250.00,USD,2026-04-01,2026-04-08,2026-04-07,DUPLICATE
3,PO-8801,External SSD 1TB,8523.80,200,45.00,9000.00,USD,2026-04-01,2026-04-10,2026-04-12,
4,PO-8802,Processor Chip X100,8542.31,1000,12.00,12000.00,USD,2026-04-03,2026-04-17,2026-04-15,
5,PO-8802,Processor Chip X200,8542.31,500,28.00,14000.00,EUR,2026-04-03,2026-04-17,2026-04-20,
6,PO-8803,Industrial PSU 500W,8504.40,50,85.00,4250.00,USD,2026-04-05,2026-04-12,2026-04-18,
7,PO-8803,Network Switch 24-Port,8517.62,25,320.00,8000.00,USD,2026-04-05,2026-04-15,2026-04-19,
8,PO-8804,USB-C Cable 2m,8536.69,2000,2.50,5000.00,USD,2026-04-07,2026-04-12,2026-04-14,
9,PO-8804,HDMI Cable 3m,8536.69,1500,3.20,4800.00,USD,2026-04-07,2026-04-14,2026-04-16,
10,PO-8805,Laptop Computer Z,8471.30,30,850.00,25500.00,USD,2026-04-08,2026-04-22,2026-04-25,
11,PO-8805,Lithium Battery 12V,8507.60,200,35.00,7000.00,USD,2026-04-08,2026-04-18,2026-04-18,
12,PO-8806,Motherboard Assembly,8473.30,200,95.00,19000.00,USD,2026-04-10,2026-04-20,2026-04-22,
13,PO-8807,USB-C Hub 7-in-1,8536.69,300,18.00,5400.00,USD,2026-04-10,2026-04-17,2026-04-21,
14,PO-8807,Wireless Router AX6000,8517.62,40,180.00,7200.00,USD,2026-04-11,2026-04-21,2026-04-24,
15,PO-8808,Server Rack Screws (Box),7318.15,10,25.00,250.00,USD,2026-04-12,2026-04-15,2026-04-16,
16,PO-8805,Power Cord C13,8544.42,100,-5.00,-500.00,USD,2026-04-08,2026-04-18,2026-04-17,NEGATIVE QTY
17,PO-8802,Warranty Extension,9999.99,1,500.00,500.00,USD,2026-04-03,2026-04-10,2026-04-09,UNKNOWN HS
18,PO-8809,WIDGET SMALL 4IN,7326.20,1000,15.00,15000.00,USD,2026-05-01,2026-05-08,,NOT YET DELIVERED
19,PO-8809,WIDGET SMALL 4IN,7326.20,1000,15.00,15000.00,USD,2026-05-01,2026-05-08,,NOT YET DELIVERED
20,PO-8810,Widget Small 4in,7326.20,500,12.50,6250.00,USD,2026-04-15,2026-04-22,2026-04-21,PRICE DROP
```

### Known Issues Planted in the Data

| Issue | Line | Detail |
|---|---|---|
| Duplicate line | 2 | Exact duplicate of line 1 — double billing risk |
| Currency mismatch | 5 | EUR but all others are USD — conversion not applied |
| Late delivery | 6, 7, 12, 13, 14 | Actual delivery after promised date |
| Wrong HS code | 15 | 7318.15 (metal screws) — not in tariff table |
| Negative quantity | 16 | qty = -100, line_total = -500.00 — data error |
| Unknown HS code | 17 | 9999.99 doesn't exist in tariff table |
| Missing delivery | 18, 19 | actual_delivery is blank — unreceived |
| Duplicate PO-8809 | 18, 19 | Same PO appears twice — duplicate or split? |
| Price discrepancy | 20 | unit_price 12.50 vs 15.00 on line 18 for same item |
| HS code: screws | 15, 18, 19, 20 | 7318.20 and 7326.20 need verification |

## Walkthrough Steps

Open the Weatherman AI Portal in your browser. Select **Sunny** from the sidebar dropdown. Click the paperclip icon to upload `apex_q2_invoice.csv` and `tariff_regulatory_table.csv` (from Exercise 3).

**Step 1 — Ingestion, cleaning, and schema normalisation:**

Type this prompt into the chat input:

```
Load apex_q2_invoice.csv. Perform initial data quality checks:
1. Row count and column inventory
2. Identify and flag duplicate rows (exact duplicates)
3. Identify rows with negative quantities or prices
4. Identify rows with missing critical fields (actual_delivery, hs_code)
5. Identify rows where currency != "USD"

Create a cleaned version: remove exact duplicates, flag negative values
for review, note currency mismatches but preserve the row.
```

**Step 2 — Lead-time and delivery compliance:**

Type this prompt:

```
For every row with a valid actual_delivery date:
1. Calculate actual_delivery_days = actual_delivery - order_date
2. Compare against promised_delivery - order_date (promised_lead_time)
3. Flag any row where actual_delivery > promised_delivery as LATE
4. Calculate days_overdue and value_at_risk

Show a delivery compliance table with all flags.
```

**Step 3 — HS code and tariff audit:**

Type this prompt:

```
Load tariff_regulatory_table.csv. Left-join the cleaned invoice
against the tariff table on hs_code.

For each row:
1. If hs_code not found in tariff table -> flag INVALID_HS_CODE
2. Calculate correct_duty = line_total * duty_rate_pct / 100
3. Flag any restricted items (export_license_required, hazardous_material)

Show: line_id, item, hs_code, duty_rate, correct_duty, flags.
```

**Step 4 — Inventory and pricing impact:**

Type this prompt:

```
For each line item, assess pricing impact:
1. Check if unit_price is negative -> flag DATA_ERROR
2. For currency != USD, flag for manual conversion review
3. Group by PO number. Flag POs with multiple invoice lines that
   appear to be duplicate billings (same PO, same item, same qty)
4. Calculate total margin leakage:
   - Duplicate lines: full line_total
   - Duty overpayment on misclassified HS codes
   - Currency conversion exposure

Show a consolidated margin leakage table.
```

**Step 5 — Generate consolidated report and alert:**

Type this prompt:

```
Write two output files:

1. compliance_report.csv — all findings with columns:
   line_id, issue_type, severity, description, financial_impact

2. margin_leakage_alert.txt — executive alert:

   === MARGIN LEAKAGE ALERT ===
   Vendor: Apex Logistics — Q2 Consolidated

   HIGH SEVERITY ISSUES:
   - Duplicate billing: $X,XXX.XX (line X)
   - Data errors: $X,XXX.XX (line X — negative qty)
   - Currency exposure: $X,XXX.XX (line X — EUR not USD)

   MEDIUM SEVERITY:
   - Invalid HS codes: X lines
   - Late deliveries: X lines ($XX,XXX value at risk)
   - Restricted items without license: X lines

   TOTAL ESTIMATED MARGIN LEAKAGE: $XX,XXX.XX
   RECOMMENDED ACTION: Hold payment pending vendor correction.

Then print a pipeline summary:

   === PIPELINE COMPLETE ===
   Input:    apex_q2_invoice.csv (20 raw lines)
   Cleaned:  XX lines (X duplicates removed, X flagged)
   Audited:  XX lines across X checks
   Output:   compliance_report.csv, margin_leakage_alert.txt
   Status:   PAYMENT NOT RECOMMENDED — see alert for details
```

Click the download button to save both generated files.
