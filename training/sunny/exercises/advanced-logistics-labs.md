# Advanced Logistics Labs — Messy Data Exercises

Three production-grade exercises for Sunny to sharpen her Claude Code auditing skills with realistic, messy vendor data.

---

## Exercise 1: The Broken Freight Sheet

### Scenario

Apex Logistics sent their March freight invoice. The file looks normal at first glance, but their ERP system has been mangling numbers for weeks. Your job: find every overcharge, formatting mistake, and phantom line item before accounts payable cuts the cheque.

### Dataset

Save the following as `apex_freight_march.csv` and load it into Claude Code.

```csv
invoice_no,vendor,service,weight_kg,rate_per_kg,fuel_surcharge_pct,line_total,currency
INV-401,Apex,Air Freight,,12.50,15.0,2875.00,USD
INV-401,Apex,Air Freight,150,12.50,15.0,2156.25,USD
INV-401,Apex,Customs Clearance,1,150.00,0.0,150.00,USD
INV-402,Apex,Sea Freight,2000,4.20,10.0,9240.00,USD
INV-402,Apex,Sea Freight,2000,4.20,10.0,$9,240.00,USD
INV-402,Apex,Port Handling,1,450.00,0.0,450.00,USD
INV-403,Apex,Express Air,25,18.00,12.5,506.25,USD
INV-403,Apex,Express Air,25,18,00,12.5,562.50,USD
INV-403,Apex,Insurance,1,75.00,0.0,75.00,USD
INV-404,Apex,Sea Freight,5000,3.80,8.0,20520.00,USD,,,,
INV-404,Apex,Storage,7,22.50,0.0,157.50,USD
INV-404,Apex,Documentation,1,35.00,0.0,35.00,USD
INV-405,Apex,Air Freight,80,14.00,15.0,,USD
INV-405,Apex,Air Freight,80,14.00,15.0,1288.00,USD
INV-405,Apex,Warehouse Handling,1,120.00,0.0,120.00,USD
INV-405,Apex,Subtotal,241,240.00,0.0,240.00,USD
```

### Known Issues Planted in the Data

| Issue | Where |
|---|---|
| Missing weight (row 1) | INV-401 Air Freight, blank `weight_kg` |
| Duplicate line (rows 3 and 4) | INV-402 Sea Freight appears twice |
| Currency-formatted number (row 5) | `$9,240.00` instead of `9240.00` |
| Broken decimal (row 8) | `18 00` instead of `18.00` for Express Air rate |
| Trailing extra commas (row 10) | INV-404 Sea Freight has `,,,,` at end |
| Missing line total (row 13) | INV-405 Air Freight blank `line_total` |
| Subtotal row that should be excluded (row 16) | INV-405 row labelled "Subtotal" |
| Math error (row 2) | 150 × 12.50 × 1.15 = 2156.25 but 150 × 12.50 = 1875.00, × 1.15 = 2156.25 — check if surcharge was applied correctly |
| Duplicate total (row 5) | INV-402 Sea Freight appears twice — if both paid, Apex gets double |

### Walkthrough Steps

```
claude apex_freight_march.csv
```

**Step 1 — Inventory:**
Ask Claude to read the file and tell you how many rows, what columns exist, and whether there are any obviously blank cells.

```
Step 1 Prompt:
Read apex_freight_march.csv and give me:
- Row count and column names
- Which rows have any blank cells (list them)
- The unique values in "service" and "currency"
```

**Step 2 — Clean and normalise:**
Ask Claude to strip currency formatting, fix the broken decimal, and remove the subtotal row.

```
Step 2 Prompt:
Clean this data:
1. Remove any row where service = "Subtotal" — it's a formatting row, not a real line item
2. Strip "$" and commas from any field that contains them and convert to plain numbers
3. Find the row where rate_per_kg = "18 00" and fix it to 18.00
4. Remove any rows that are entirely empty or contain only commas
5. Show me the cleaned table
```

**Step 3 — Find duplicates:**
Ask Claude to surface any duplicate invoice-service combinations.

```
Step 3 Prompt:
Group by (invoice_no, service). Show me any combination that appears more than once.
These are potential duplicate billings — list the duplicate rows side by side.
```

**Step 4 — Verify line totals:**
The formula is `line_total = weight_kg × rate_per_kg × (1 + fuel_surcharge_pct / 100)`. Rows without weight or with `fuel_surcharge_pct = 0` just use `rate_per_kg` as the flat fee.

```
Step 4 Prompt:
For every non-duplicate row, verify the line_total. The formula is:
- If fuel_surcharge_pct > 0: line_total = weight_kg × rate_per_kg × (1 + fuel_surcharge_pct / 100)
- If fuel_surcharge_pct = 0 or weight_kg is blank: line_total = rate_per_kg (flat fee)

Show me: invoice_no, service, weight_kg, rate_per_kg, surcharge, expected_total, actual_total, deviation.
Flag any row where abs(deviation) > 0.01.
```

**Step 5 — Export findings:**
```
Step 5 Prompt:
Write a CSV called freight_errors.csv with every issue found:
violation_type, invoice_no, service, field, expected, actual, notes
Include duplicates, math errors, formatting issues, and blank fields.
Then give me a terminal summary of total potential overcharge amount.
```

---

## Exercise 2: The Multi-Sheet Inventory Balance

### Scenario

Three warehouses — North, Central, and South — submitted their end-of-month inventory counts. But the tracking IDs don't line up, some SKUs appear in one warehouse's "received" sheet but not in another's "shipped" sheet, and the grand totals disagree. Sunny needs to reconcile all three warehouses and identify where inventory has gone missing, been double-counted, or mislabeled.

### Dataset

Save the following as `warehouse_inventory_march.xlsx` data (represent as three markdown tables). Load all three tables into Claude Code.

**Sheet 1: north_warehouse**

```csv
tracking_id,sku,description,qty_received,qty_shipped,date
TRK-1001,WIDG-001,Widget Small 4in,500,200,2026-03-01
TRK-1002,WIDG-002,Widget Large 8in,300,150,2026-03-02
TRK-1003,GADG-010,Gadget Pro,100,80,2026-03-03
TRK-1004,WIDG-001,Widget Small 4in,400,250,2026-03-05
TRK-1005,GADG-010,Gadget Pro,200,190,2026-03-07
TRK-1006,WIDG-003,Widget X-Large,150,0,2026-03-10
```

**Sheet 2: central_warehouse**

```csv
tracking_id,sku,description,qty_received,qty_shipped,date
TRK-2001,WIDG-001,Widget Small 4in,600,350,2026-03-01
TRK-2002,GADG-010,Gadget Pro,150,120,2026-03-02
TRK-2003,WIDG-002,Widget Large 8in,250,200,2026-03-04
TRK-2004,GADG-020,Gadget Lite,300,250,2026-03-06
TRK-2005,WIDG-001,Widget Small 4in,350,300,2026-03-08
TRK-2006,GADGET-10,Gadget Pro,100,80,2026-03-09
```

**Sheet 3: south_warehouse**

```csv
tracking_id,sku,description,qty_received,qty_shipped,date
TRK-3001,WIDG-001,Widget Small 4in,400,350,2026-03-01
TRK-3002,GADG-010,Gadget Pro,200,180,2026-03-02
TRK-3003,WIDG-003,Widget X-Large,120,100,2026-03-05
TRK-3004,GADG-020,Gadget Lite,250,200,2026-03-07
TRK-3005,WIDG-001,Widget Small 4in,300,300,2026-03-09
TRK-3006,GADG-030,Gadget Max,50,30,2026-03-12
```

### Known Issues Planted in the Data

| Issue | Where |
|---|---|
| SKU mismatch | `GADG-010` in Central sheet 2 row 6 stored as `GADGET-10` — orphan when cross-referenced |
| Orphaned SKU across warehouses | `GADG-030` appears only in South — no other warehouse has it |
| SKU `WIDG-002` missing from South | Appears in North and Central but not South |
| SKU `GADG-020` missing from North | Appears in Central and South but not North |

### Walkthrough Steps

```
claude north_warehouse.csv central_warehouse.csv south_warehouse.csv
```

**Step 1 — Unify SKUs across all warehouses:**
```
Step 1 Prompt:
I have three warehouse inventory tables. Normalise the SKU column across all three:
1. Strip whitespace and uppercase everything
2. Build a unified list of every unique SKU and which warehouse(s) it appears in
3. Flag any SKU that has a naming mismatch (e.g., "GADG-010" vs "GADGET-10")
```

**Step 2 — Find orphaned SKUs:**
```
Step 2 Prompt:
Using the unified SKU list:
- List any SKU that appears in only one warehouse (orphaned stock)
- List any SKU that is missing from a warehouse where you'd expect it (e.g., appears in 2 of 3)
- For each orphan, show the total qty_received and qty_shipped
```

**Step 3 — Reconcile received vs shipped per SKU:**
```
Step 3 Prompt:
For each SKU across all warehouses, calculate:
  total_received = sum(qty_received)
  total_shipped = sum(qty_shipped)
  remaining = total_received - total_shipped

Sort by remaining descending. Flag any SKU where remaining is negative
(more shipped than received — data error or missing receiving record).
```

**Step 4 — Detect cross-warehouse transfer gaps:**
```
Step 4 Prompt:
Treat the three warehouses as a flow: North ships to Central, Central ships to South.

For each SKU, compare what North shipped vs. what Central received.
Flag mismatches. Then compare what Central shipped vs. what South received.

Show a table: sku, north_shipped, central_received, gap_1, central_shipped, south_received, gap_2.
```

**Step 5 — Export:**
```
Step 5 Prompt:
Write a CSV called inventory_reconciliation.csv with:
- All orphaned SKUs and which warehouse they live in
- All negative-remaining SKUs
- All transfer gaps between warehouses
Add a terminal summary: total SKUs, orphans found, transfer gaps, negative balances.
```

---

## Exercise 3: The Lead-Time Discrepancy Matrix

### Scenario

Sunny manages 10 vendor routes with promised delivery windows. The procurement team has been tracking actual delivery dates in a messy PO log that includes weekend deliveries, holiday exceptions, and partially received orders. She needs to build a lead-time discrepancy matrix to identify which vendors are consistently late and quantify the financial impact of the delays.

### Dataset

Save the following as `lead_time_matrix.csv`.

```csv
po_number,vendor_name,route,order_date,promised_min_days,promised_max_days,actual_received_date,partial,value_usd
PO-1001,Swift Logistics,Route A,2026-03-01,5,7,2026-03-09,FALSE,12500.00
PO-1002,Global Haulers,Route B,2026-03-01,7,10,2026-03-10,FALSE,8400.00
PO-1003,Prime Cargo,Route C,2026-03-02,3,5,2026-03-06,FALSE,22000.00
PO-1004,Swift Logistics,Route A,2026-03-03,5,7,2026-03-11,FALSE,15000.00
PO-1005,Northern Freight,Route D,2026-03-03,10,14,2026-03-18,FALSE,32000.00
PO-1006,Global Haulers,Route B,2026-03-04,7,10,2026-03-13,FALSE,5600.00
PO-1007,Prime Cargo,Route C,2026-03-05,3,5,2026-03-10,FALSE,18000.00
PO-1008,Swift Logistics,Route A,2026-03-06,5,7,2026-03-12,FALSE,9200.00
PO-1009,Coastal Shipping,Route E,2026-03-06,8,12,2026-03-17,FALSE,45000.00
PO-1010,Northern Freight,Route D,2026-03-07,10,14,2026-03-20,FALSE,28000.00
PO-1011,Swift Logistics,Route A,2026-03-08,5,7,2026-03-25,FALSE,30000.00
PO-1012,Global Haulers,Route B,2026-03-08,7,10,2026-03-17,FALSE,7500.00
PO-1013,Prime Cargo,Route C,2026-03-09,3,5,2026-03-13,FALSE,16500.00
PO-1014,Coastal Shipping,Route E,2026-03-10,8,12,2026-03-20,FALSE,52000.00
PO-1015,Northern Freight,Route D,2026-03-10,10,14,2026-03-23,FALSE,31000.00
PO-1016,Swift Logistics,Route A,2026-03-11,5,7,2026-03-17,FALSE,11000.00
PO-1017,Global Haulers,Route B,2026-03-11,7,10,2026-03-21,FALSE,6300.00
PO-1018,Prime Cargo,Route C,2026-03-12,3,5,2026-03-14,FALSE,19800.00
PO-1019,Coastal Shipping,Route E,2026-03-12,8,12,2026-03-22,FALSE,48000.00
PO-1020,Swift Logistics,Route A,2026-03-12,5,7,2026-03-19,FALSE,13500.00
PO-1021,Swift Logistics,Route A,2026-03-13,5,7,2026-03-26,FALSE,27500.00
PO-1022,Northern Freight,Route D,2026-03-13,10,14,2026-03-24,TRUE,15000.00
PO-1023,Global Haulers,Route B,2026-03-14,7,10,2026-03-24,FALSE,8200.00
PO-1024,Prime Cargo,Route C,2026-03-14,3,5,2026-03-18,FALSE,21000.00
PO-1025,Coastal Shipping,Route E,2026-03-14,8,12,2026-03-21,FALSE,35000.00
PO-1026,Prime Cargo,Route C,2026-03-15,3,5,2026-03-17,FALSE,14500.00
PO-1027,Swift Logistics,Route A,2026-03-15,5,7,2026-03-21,FALSE,16800.00
PO-1028,Northern Freight,Route D,2026-03-15,10,14,2026-03-26,FALSE,42000.00
PO-1029,Global Haulers,Route B,2026-03-15,7,10,2026-03-17,FALSE,4800.00
PO-1030,Coastal Shipping,Route E,2026-03-16,8,12,2026-03-25,FALSE,38000.00
PO-1031,Swift Logistics,Route A,2026-03-16,5,7,2026-03-22,FALSE,14000.00
PO-1032,Prime Cargo,Route C,2026-03-16,3,5,2026-03-28,FALSE,25000.00
PO-1033,Global Haulers,Route B,2026-03-17,7,10,2026-03-26,FALSE,6900.00
PO-1034,Coastal Shipping,Route E,2026-03-17,8,12,2026-03-24,FALSE,41000.00
PO-1035,Northern Freight,Route D,2026-03-17,10,14,2026-03-27,FALSE,33500.00
PO-1036,Swift Logistics,Route A,2026-03-18,5,7,2026-03-24,FALSE,10500.00
PO-1037,Prime Cargo,Route C,2026-03-18,3,5,2026-03-21,FALSE,17500.00
PO-1038,Global Haulers,Route B,2026-03-18,7,10,2026-03-27,FALSE,7200.00
PO-1039,Coastal Shipping,Route E,2026-03-18,8,12,2026-03-28,FALSE,46000.00
PO-1040,Prime Cargo,Route C,2026-03-19,3,5,2026-04-01,FALSE,22000.00
PO-1041,Swift Logistics,Route A,2026-03-19,5,7,2026-03-25,FALSE,12500.00
PO-1042,Northern Freight,Route D,2026-03-19,10,14,2026-03-28,FALSE,29500.00
PO-1043,Global Haulers,Route B,2026-03-19,7,10,2026-03-28,FALSE,5100.00
PO-1044,Coastal Shipping,Route E,2026-03-19,8,12,2026-04-01,FALSE,39000.00
PO-1045,Prime Cargo,Route C,2026-03-20,3,5,2026-03-23,FALSE,16000.00
PO-1046,Swift Logistics,Route A,2026-03-20,5,7,2026-03-27,FALSE,19500.00
PO-1047,Northern Freight,Route D,2026-03-20,10,14,2026-03-25,FALSE,37000.00
PO-1048,Global Haulers,Route B,2026-03-20,7,10,2026-03-26,FALSE,4400.00
PO-1049,Coastal Shipping,Route E,2026-03-20,8,12,2026-04-02,FALSE,43000.00
PO-1050,Swift Logistics,Route A,2026-03-21,5,7,FALSE,FALSE,15000.00
```

### Known Issues Planted in the Data

| Issue | Where |
|---|---|
| PO-1011 Swift Route A | 18 days actual vs 5–7 promised — extreme outlier (17 days late) |
| PO-1029 Global Haulers | 2 days actual vs 7–10 promised — arrived early, but also suspicious (partial data error?) |
| PO-1050 Swift Route A | `actual_received_date` = "FALSE" — data entry error, never received |
| PO-1032 Prime Cargo | 12 days actual vs 3–5 promised — severely late |
| PO-1040 Prime Cargo | 13 days actual vs 3–5 promised — severely late |
| PO-1044 Coastal Shipping | same pattern, arrives just before or at 12 days max |
| Partial shipment PO-1022 | Marked `partial = TRUE` — needs different handling |
| PO-1001 Swift Route A | 8 days actual vs 5–7 promised — 1 day over but on a high-value order |

### Walkthrough Steps

```
claude lead_time_matrix.csv
```

**Step 1 — Calculate actual transit days:**
```
Step 1 Prompt:
Calculate the actual transit time for every PO:
  actual_days = actual_received_date - order_date (calendar days)

Skip any row where actual_received_date is not a valid date (mark as "unreceived").
For partial shipments (partial = TRUE), flag them separately in the output.

Show me: po_number, vendor, route, promised_max_days, actual_days, days_over, value_usd.
```

**Step 2 — Flag late deliveries:**
```
Step 2 Prompt:
For each PO where actual_days > promised_max_days, calculate:
  days_overdue = actual_days - promised_max_days
  overage_cost = (days_overdue / promised_max_days) * value_usd  (linear cost allocation)

Sort by days_overdue descending. Show the top 10 worst offenders.
```

**Step 3 — Build the vendor discrepancy matrix:**
```
Step 3 Prompt:
Group by vendor_name and build a discrepancy matrix showing:
  vendor_name
  total_pos
  on_time_count (actual_days <= promised_max_days)
  late_count
  on_time_pct
  avg_days_overdue (among late POS only)
  worst_days_overdue
  total_overage_cost
  total_value_at_risk

Sort by on_time_pct ascending (worst performers first).
```

**Step 4 — Route-level analysis:**
```
Step 4 Prompt:
Group by route. For each route, show:
  route, vendors_on_route, total_pos, avg_days_overdue, total_value

Then identify: which route has the worst average delay?
Which vendor is dragging down that route's performance?
```

**Step 5 — Flag critical anomalies:**
```
Step 5 Prompt:
Identify these anomalies:
1. Orders where actual_days < promised_min_days — arrived suspiciously early
2. Orders where actual_days > promised_max_days * 2 — extreme lateness
3. Orders where actual_received_date is not a valid date
4. Orders with partial = TRUE — flag for separate follow-up

Write a file called lead_time_anomalies.csv with all anomalies found.
```

**Step 6 — Final summary:**
```
Step 6 Prompt:
Print a discrepancy matrix summary:

=== LEAD-TIME DISCREPANCY MATRIX ===
Period: March 2026
Total POs: 50
On-time:      XX (XX%)
Late:         XX (XX%)
Unreceived:   X

Cost impact:
  Total PO value:         $XXX,XXX
  Value at risk (late):   $XX,XXX
  Estimated overage cost: $X,XXX

Worst vendor:  XXXXX (XX% late, avg XX days over)
Worst route:   Route X (avg XX days over)

Vendor ranking (best → worst):
1. Vendor X — XX% on-time
2. ...
```

---

## Data File Reference

All datasets are plain CSV — save each to a file, then load with `claude filename.csv`. For Exercise 2, treat each markdown table as a separate file named after the warehouse.

| File | Exercise |
|---|---|
| `apex_freight_march.csv` | Exercise 1 — The Broken Freight Sheet |
| `north_warehouse.csv` | Exercise 2 — Multi-Sheet Inventory Balance |
| `central_warehouse.csv` | Exercise 2 — Multi-Sheet Inventory Balance |
| `south_warehouse.csv` | Exercise 2 — Multi-Sheet Inventory Balance |
| `lead_time_matrix.csv` | Exercise 3 — Lead-Time Discrepancy Matrix |

### Cross-Reference: Syllabus & Skills

| Resource | Purpose | Path |
|---|---|---|
| Purchasing & Logistics Syllabus | Full course outline for Sunny | `../syllabus.md` |
| lead-time-anomaly skill | Automated lead-time discrepancy detection | `../skills/lead-time-anomaly/SKILL.md` |
| customs-tariff-audit skill | Tariff code and rate validation | `../skills/customs-tariff-audit/SKILL.md` |
| warehouse-balancing skill | Multi-warehouse inventory reconciliation | `../skills/warehouse-balancing/SKILL.md` |
| xlsx-processing skill | Excel file reading and transformation | `../skills/xlsx-processing/SKILL.md` |
| data-table-validator skill | Pricing and data integrity checks (adjacent skill) | `../skills/data-table-validator/SKILL.md` |
