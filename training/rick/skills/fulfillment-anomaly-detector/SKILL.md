---
name: fulfillment-anomaly-detector
description: Parse fulfillment delay reports, flag carrier underperformance, and auto-generate warehouse status updates with actionable recommendations.
---

# fulfillment-anomaly-detector

An operational agent skill for auditing fulfillment performance across carriers and warehouses. This skill takes a shipment delay log with carrier transit data, computes delay metrics per carrier and warehouse, and produces a structured carrier discrepancy matrix and warehouse status summary. Run this whenever Rick needs to identify underperforming carriers, bottleneck warehouses, or prepare data for logistics review meetings.

---

## 1. Intake & Schema Mapping

### 1.1 Accept input formats

- **`.csv`** / **`.tsv`** — flat delimited files with or without a header row
- **Markdown tables** — inline tables in a `.md` file

### 1.2 Identify required columns

Scan the header row to locate these columns. Report any missing ones immediately and do not proceed until Rick clarifies the mapping.

| Required column | Aliases accepted |
|---|---|
| `order_id` | `order`, `fulfillment_id`, `shipment_id`, `id`, `ref` |
| `warehouse` | `warehouse_code`, `wh`, `origin_warehouse`, `location`, `site` |
| `carrier` | `carrier_name`, `shipper`, `shipping_provider`, `courier`, `logistics_provider` |
| `ship_date` | `shipped_date`, `date_shipped`, `dispatch_date`, `departure_date` |
| `estimated_delivery` | `eta`, `promised_date`, `expected_delivery`, `est_delivery`, `target_date` |
| `actual_delivery` | `delivery_date`, `date_delivered`, `received_date`, `proof_of_delivery` |

Also detect these **optional** columns:

| Optional column | Aliases accepted |
|---|---|
| `status` | `delivery_status`, `shipment_status`, `tracking_status`, `current_status` |
| `destination_region` | `region`, `destination`, `ship_to_region`, `zone` |
| `declared_value` | `value`, `shipment_value`, `insured_value`, `cargo_value` |
| `sku` | `product_code`, `item`, `item_id`, `product` |

### 1.3 Report schema to the user

```
=== FULFILLMENT ANOMALY DETECTOR: SCHEMA CONFIRMED ===
Order ID:            "order_id"              (string)
Warehouse:           "warehouse"             (string)
Carrier:             "carrier"               (string)
Ship Date:           "ship_date"             (date)
Estimated Delivery:  "estimated_delivery"    (date)
Actual Delivery:     "actual_delivery"       (date)

Optional found: status, destination_region, declared_value, sku
Missing:        (none)

Rows loaded: 35
Proceed? (y/n)
```

Wait for Rick to confirm before continuing.

---

## 2. Data Cleansing

### 2.1 Validate and normalise dates

Parse every date column into a uniform `YYYY-MM-DD` format.

- If `actual_delivery` is blank, `"N/A"`, `"NULL"`, or not a parseable date, mark the row as `not_delivered`.
- If `ship_date` or `estimated_delivery` fails to parse, flag as `bad_date` and exclude from transit time calculations.

### 2.2 Validate status field

If a `status` column exists, map it into one of these categories:

| Incoming value | Normalised status |
|---|---|
| `delivered`, `Delivered`, `DELIVERED`, `complete`, `Complete` | `delivered` |
| `delayed`, `Delayed`, `DELAYED`, `late`, `overdue` | `delayed` |
| `in_transit`, `In Transit`, `IN TRANSIT`, `shipped`, `pending` | `in_transit` |
| `exception`, `Exception`, `EXCEPTION`, `damaged`, `lost`, `returned` | `exception` |

If no `status` column exists, infer status heuristically:

- `actual_delivery` is a valid date and ≤ `estimated_delivery` → `delivered` (on time)
- `actual_delivery` is a valid date and > `estimated_delivery` → `delivered` (late)
- `actual_delivery` is blank and today is past `estimated_delivery` → `delayed`
- `actual_delivery` is blank and today is before or equal to `estimated_delivery` → `in_transit`

### 2.3 Remove noise rows

Skip rows matching any of these:

- Row is entirely empty
- Row is a header duplicate or column spacer
- Row where `order_id` is blank or `"TOTAL"`, `"SUBTOTAL"`, `"SUM"`

Report the number of skipped rows.

---

## 3. Delay Calculation

### 3.1 Compute transit time and delay

For every row with a valid `ship_date` and a valid `actual_delivery`:

```
transit_days  = actual_delivery - ship_date (calendar days)
delay_days    = actual_delivery - estimated_delivery (calendar days)
```

If Rick asks for **business days**, exclude Saturdays and Sundays. Flag this in the report header.

### 3.2 Classification

| Condition | Status |
|---|---|
| `actual_delivery` is blank and `status` is `in_transit` | `in_transit` |
| `actual_delivery` is blank and `status` is `exception` | `exception` |
| `delay_days ≤ 0` | `on_time` |
| `delay_days > 0 and ≤ 3` | `slight_delay` |
| `delay_days > 3 and ≤ 7` | `moderate_delay` |
| `delay_days > 7` | `severe_delay` |
| `actual_delivery` is blank and past due | `overdue` |

---

## 4. Carrier Discrepancy Matrix

### 4.1 Aggregate by carrier

Group all rows by `carrier` and compute:

```
total_shipments        = count(*)
on_time_count          = count where delay_days ≤ 0
delayed_count          = count where delay_days > 0
on_time_pct            = (on_time_count / (total_shipments - in_transit - exception)) * 100
avg_delay_days         = avg(delay_days) across delayed shipments only
max_delay_days         = max(delay_days)
total_value_at_risk    = sum(declared_value) across delayed shipments
exception_count        = count where status = "exception"
in_transit_count       = count where status = "in_transit"
```

### 4.2 Build the discrepancy matrix

Sort by `on_time_pct` ascending (worst performers first):

```
CARRIER DISCREPANCY MATRIX:
Rank | Carrier         | Shipments | On-Time% | Delayed | Avg Delay | Worst Delay | Val@Risk
-----|-----------------|-----------|----------|---------|-----------|-------------|----------
  1  | TransGlobal     |    8      |   28.6%  |   5     |   5.2 d   |    6 d      | $15,850
  2  | FastShip        |   10      |   60.0%  |   3     |   3.3 d   |    5 d      | $12,700
  3  | PrimeLogistics  |    9      |   71.4%  |   2     |   2.0 d   |    2 d      |  $1,675
  4  | HaulMaster      |    8      |   75.0%  |   2     |   1.5 d   |    2 d      |  $2,100
```

### 4.3 Flag underperforming carriers

| Condition | Flag |
|---|---|
| `on_time_pct < 50%` | `CRITICAL — escalate to logistics director` |
| `on_time_pct >= 50% and < 70%` | `WARNING — below service-level agreement` |
| `on_time_pct >= 70% and < 85%` | `WATCH — needs improvement` |
| `avg_delay_days > 5` | `HARD — chronic delays` |
| `max_delay_days > 10` | `HARD — extreme outlier detected` |
| `exception_rate > 10%` | `DATA_QUALITY — high exception rate` |

---

## 5. Warehouse-Level Analysis

### 5.1 Aggregate by warehouse

Group all rows by `warehouse` and compute:

```
total_shipments        = count(*)
delayed_count          = count where delay_days > 0
avg_delay_days         = avg(delay_days) across delayed shipments only
carriers_used          = distinct carrier names
worst_carrier          = carrier with highest delayed_count in this warehouse
total_value_shipped    = sum(declared_value)
value_at_risk          = sum(declared_value) where delayed
```

### 5.2 Identify bottleneck warehouses

- Flag any warehouse where `delayed_count / total_shipments > 0.25` as `BOTTLENECK — high delay rate`
- Flag any warehouse with only one carrier as `SINGLE_SOURCE — no carrier redundancy`
- Flag any warehouse with `value_at_risk > $10,000` as `HIGH_VALUE — prioritize review`

---

## 6. Output & Reporting

### 6.1 Print the carrier discrepancy matrix to terminal

```
╔══════════════════════════════════════════════════════════════╗
║            FULFILLMENT ANOMALY DETECTOR — REPORT             ║
╠══════════════════════════════════════════════════════════════╣
║ Period:              June 2026                              ║
║ Total shipments:     35                                     ║
║ Carriers analysed:   4                                      ║
║ Warehouses:          3                                      ║
║                                                            ║
║ On-Time:        18  (51.4%)                                 ║
║ Delayed:        12  (34.3%)                                 ║
║ Exception:       2  ( 5.7%)                                 ║
║ In Transit:      3  ( 8.6%)                                 ║
║                                                            ║
║ Total shipment value:         $73,105.00                    ║
║ Value at risk (delayed):      $32,325.00                    ║
║                                                            ║
║ CRITICAL carriers:  1  (TransGlobal — 28.6% on-time)        ║
║ WARNING carriers:   1  (FastShip — 60.0% on-time)           ║
║ WATCH carriers:     2                                      ║
║                                                            ║
║ BOTTLENECK warehouses:  1  (WH-North — 33% delayed)         ║
╚══════════════════════════════════════════════════════════════╝
```

### 6.2 Write the carrier performance CSV

Write `carrier_performance_<YYYYMMDD>.csv`:

```
rank,carrier,total_shipments,on_time_count,delayed_count,on_time_pct,
avg_delay_days,max_delay_days,total_value_at_risk,flag
1,TransGlobal,8,2,5,28.6,5.2,6,15850.00,CRITICAL
2,FastShip,10,6,3,60.0,3.3,5,12700.00,WARNING
```

### 6.3 Write the warehouse status CSV

Write `warehouse_status_<YYYYMMDD>.csv`:

```
warehouse,total_shipments,delayed_count,delay_rate,carriers_used,value_at_risk,flags
WH-North,12,4,0.33,3,24500.00,BOTTLENECK|HIGH_VALUE
WH-East,11,3,0.27,2,6800.00,BOTTLENECK
WH-South,12,2,0.17,3,1025.00,
```

### 6.4 Write the detailed shipment-level CSV

Write `fulfillment_audit_detail_<YYYYMMDD>.csv`:

```
order_id,carrier,warehouse,ship_date,estimated_delivery,actual_delivery,
delay_days,status,declared_value,flags
ORD-1023,TransGlobal,WH-North,2026-06-08,2026-06-12,2026-06-18,6,
delayed,3750.00,moderate_delay|CRITICAL_carrier
```

---

## 7. Strictness Rules (Do Not Deviate)

1. **Never treat a blank delivery date as delivered.** If `actual_delivery` is empty, it is `not_delivered`. Do not guess or impute the date.
2. **Always separate exception and in-transit from the on-time calculation.** Only delivered shipments count toward the on-time percentage.
3. **Never modify the original file.** All calculations happen in-memory. Output files are separate exports.
4. **Always report the discrepancy matrix sorted worst-first.** The worst-performing carrier must be at the top so Rick sees it immediately.
5. **Always report a value-at-risk total.** Even if `declared_value` is missing, report what you can and note "value column not provided" in the terminal output.
6. **Zero delay is not a flag.** Only flag carriers who actually exceed their estimated delivery window.

---

## 8. Edge Cases

| Situation | Handling |
|---|---|
| No shipments in the file | Print "ERROR: file contains zero shipments" and abort |
| All shipments are in-transit or exception | Print "All shipments are in-transit or exception — cannot compute carrier performance. Re-run when more delivery data is available." |
| Missing `declared_value` column | Skip value-at-risk calculations; print summary without dollar amounts |
| Single shipment in file | Validate normally but warn "only 1 shipment — carrier statistics are not meaningful" |
| `actual_delivery` is before `ship_date` | Flag as `negative_transit — possible data entry error` and exclude from calculations |
| Same `order_id` appears on multiple rows | Flag as `duplicate_order` — check whether it is a split shipment or a data error; ask Rick |
| Carrier name variations (e.g., "FastShip" vs "Fast Ship" vs "fastship") | Normalise by lowercasing and stripping whitespace; report variations found |
