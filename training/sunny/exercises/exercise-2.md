# Exercise 2 — Automated Lead-Time Profiling

## Scenario

Sunny needs to audit 10 vendor routes against their promised delivery windows. The procurement team has been tracking actual delivery dates in a PO log, but the data contains weekend deliveries, holiday exceptions, and partially received orders. She needs to build a lead-time discrepancy matrix to identify which vendors are consistently late and quantify the financial impact.

## Learning Objectives

- Calculate actual vs. promised lead times from PO data
- Group and rank vendors by on-time performance
- Identify outlier deliveries and data quality issues
- Quantify financial exposure from late deliveries

## Dataset

Reference the existing file at `../data/lead_time_matrix.csv` (50 POs across 5 vendors, March 2026).

If the file is not yet available, save this inline data:

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
```

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| Extreme late outlier | PO-1011 Swift Route A — 17 days actual vs 7 max |
| Suspiciously early | PO-1029 Global Haulers — 2 days actual vs 7-10 promised |
| Data error | Some rows may have invalid `actual_received_date` values |
| Partial shipment | PO-1022 marked partial=TRUE — needs separate handling |

## Walkthrough Steps

Open the Weatherman AI Portal in your browser. Select **Sunny** from the sidebar dropdown. Click the paperclip icon to upload `lead_time_matrix.csv`.

**Step 1 — Calculate actual transit days:**

Type this prompt into the chat input:

```
Calculate the actual transit time for every PO:
  actual_days = actual_received_date - order_date (calendar days)

Skip any row where actual_received_date is not a valid date.
Mark partial shipments separately.

Show: po_number, vendor, route, promised_max_days, actual_days, days_over, value_usd.
```

**Step 2 — Flag late deliveries:**

Type this prompt:

```
For each PO where actual_days > promised_max_days, calculate:
  days_overdue = actual_days - promised_max_days
  overage_cost = (days_overdue / promised_max_days) * value_usd

Sort by days_overdue descending. Show the top 10 worst offenders.
```

**Step 3 — Build vendor discrepancy matrix:**

Type this prompt:

```
Group by vendor_name and build a matrix:
  vendor_name, total_pos, on_time_count, late_count, on_time_pct,
  avg_days_overdue, worst_days_overdue, total_overage_cost, total_value_at_risk

Sort by on_time_pct ascending (worst performers first).
```

**Step 4 — Route-level analysis:**

Type this prompt:

```
Group by route. For each route show:
  route, vendors_on_route, total_pos, avg_days_overdue, total_value

Which route has the worst average delay?
Which vendor is dragging down that route's performance?
```

**Step 5 — Export findings:**

Type this prompt:

```
Write a file called lead_time_discrepancy_matrix.csv with:
- Vendor-level summary rows
- Route-level summary rows
- All anomaly flags

Then print the final discrepancy matrix:

=== LEAD-TIME DISCREPANCY MATRIX ===
Period: March 2026
Total POs: XX
On-time:  XX (XX%)
Late:     XX (XX%)

Cost impact:
  Total PO value:         $XXX,XXX
  Value at risk (late):   $XX,XXX
  Estimated overage cost: $X,XXX

Worst vendor:  XXXXX (XX% late)
Worst route:   Route X
```

Click the download button to save the generated CSV file.
