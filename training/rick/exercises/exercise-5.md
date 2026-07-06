# Exercise 5 — Capstone: The Strategic Operational Blueprint

## Scenario

This is the capstone exercise that integrates everything from Exercises 1-4. Your company needs a unified strategic operational blueprint that combines inventory health, fulfilment performance, and financial risk into a single executive dashboard. You will upload two datasets, run a multi-phase analysis, and produce a strategic roadmap with clear recommendations.

## Learning Objectives

- Combine multiple datasets into a unified analysis in the Weatherman AI Portal
- Assess inventory health across warehouses (stock levels, reorder points, demand)
- Evaluate carrier fulfilment performance and compute risk scores
- Calculate a composite strategic score for each SKU-warehouse combination
- Generate prioritised recommendations
- Export a complete executive roadmap

## Datasets

This exercise uses two datasets from the data directory:

- `inventory_stock_levels.csv` — SKU-level stock, reorder points, demand
- `fulfillment_delay_report.csv` — Carrier delivery performance

Upload both files using the paperclip icon before starting.

### Inventory Stock Levels (`inventory_stock_levels.csv`)

```csv
sku,warehouse,stock_on_hand,reorder_point,lead_time_days,unit_cost,monthly_demand
WIDG-001,WH-North,320,150,7,4.50,180
WIDG-001,WH-East,85,150,7,4.50,180
WIDG-001,WH-South,410,150,7,4.50,180
WIDG-002,WH-North,200,100,5,6.75,120
WIDG-002,WH-East,45,100,5,6.75,120
WIDG-003,WH-North,42,150,10,12.00,200
WIDG-003,WH-East,210,150,10,12.00,200
GADG-001,WH-North,500,200,14,8.25,250
GADG-001,WH-South,150,200,14,8.25,250
GADG-010,WH-North,75,50,7,15.00,60
GADG-010,WH-East,120,50,7,15.00,60
GADG-010,WH-South,180,50,7,15.00,60
GADG-020,WH-South,30,100,21,22.50,80
SUPR-001,WH-East,600,300,10,3.50,400
SUPR-001,WH-South,200,300,10,3.50,400
SUPR-002,WH-North,90,80,5,9.00,100
SUPR-002,WH-East,150,80,5,9.00,100
SUPR-002,WH-South,300,80,5,9.00,100
```

### Fulfillment Delay Report (`fulfillment_delay_report.csv`)

```csv
order_id,sku,warehouse,carrier,ship_date,estimated_delivery,actual_delivery,status,destination_region,declared_value
FUL-1001,WIDG-001,WH-North,FedEx,2026-03-01,2026-03-05,2026-03-05,delivered,NE,4500.00
FUL-1002,WIDG-002,WH-East,UPS,2026-03-01,2026-03-04,2026-03-06,delivered,SE,3200.00
FUL-1003,GADG-001,WH-South,DHL,2026-03-02,2026-03-06,2026-03-07,delivered,MW,8900.00
FUL-1004,WIDG-003,WH-North,FedEx,2026-03-02,2026-03-06,,delayed,NE,12000.00
FUL-1005,GADG-010,WH-East,USPS,2026-03-03,2026-03-08,2026-03-10,delivered,SE,2500.00
FUL-1006,SUPR-001,WH-South,FedEx,2026-03-03,2026-03-07,2026-03-04,delivered,MW,7800.00
FUL-1007,WIDG-001,WH-North,USPS,2026-03-04,2026-03-09,2026-03-15,delivered,NE,4500.00
FUL-1008,SUPR-002,WH-East,UPS,2026-03-04,2026-03-08,2026-03-08,delivered,SE,6100.00
FUL-1009,GADG-020,WH-South,DHL,2026-03-05,2026-03-11,2026-03-12,delivered,MW,15000.00
FUL-1010,WIDG-002,WH-North,FedEx,2026-03-05,2026-03-09,,delayed,NE,3400.00
FUL-1011,GADG-001,WH-East,USPS,2026-03-06,2026-03-10,2026-03-14,delivered,SE,8900.00
FUL-1012,SUPR-001,WH-South,UPS,2026-03-06,2026-03-10,2026-03-11,delivered,MW,5500.00
FUL-1013,WIDG-003,WH-North,DHL,2026-03-07,2026-03-11,2026-03-11,delivered,NE,3200.00
FUL-1014,GADG-010,WH-East,FedEx,2026-03-07,2026-03-11,2026-03-13,delivered,SE,2500.00
FUL-1015,SUPR-002,WH-South,FedEx,2026-03-08,2026-03-12,,delayed,MW,9800.00
FUL-1016,WIDG-001,WH-North,UPS,2026-03-08,2026-03-12,2026-03-12,delivered,NE,4500.00
FUL-1017,GADG-001,WH-East,DHL,2026-03-09,2026-03-13,2026-03-15,delivered,SE,8900.00
FUL-1018,SUPR-001,WH-South,USPS,2026-03-09,2026-03-13,,delayed,MW,6500.00
FUL-1019,WIDG-002,WH-North,FedEx,2026-03-10,2026-03-14,2026-03-16,delivered,NE,3200.00
FUL-1020,GADG-010,WH-East,UPS,2026-03-10,2026-03-14,2026-03-14,delivered,SE,2500.00
```

### Known Issues Planted in the Data

| Issue | Location | Notes |
|---|---|---|
| Below reorder point | WIDG-003 @ WH-North | 42 units vs reorder 150 |
| Below reorder point | WIDG-002 @ WH-East | 45 units vs reorder 100 |
| Below reorder point | GADG-001 @ WH-South | 150 units vs reorder 200 |
| Below reorder point | SUPR-001 @ WH-South | 200 units vs reorder 300 |
| Single point of failure | GADG-020 @ WH-South | Only stocked at one warehouse |
| Carrier delays | FedEx | 3 shipments delayed, $25,200 at risk |
| Carrier delays | USPS | 1 delayed + 3 late shipments, $6,500 at risk |

## Walkthrough

### Phase A — Inventory Health Assessment

Type this prompt into the chat input:

> "Using the inventory_stock_levels.csv file:
>
> For each SKU-warehouse combination, classify inventory status:
> - OUT_OF_STOCK: stock_on_hand <= 0
> - BELOW_REORDER: stock_on_hand < reorder_point
> - LOW_STOCK: stock_on_hand < reorder_point * 1.5
> - HEALTHY: everything else
>
> Also calculate days_of_stock = stock_on_hand / (monthly_demand / 30).
>
> Flag any SKU-warehouse that is BELOW_REORDER or worse.
> Show results in a table sorted by severity (worst first)."

### Phase B — Fulfilment Health Assessment

Type this prompt into the chat input:

> "Using the fulfillment_delay_report.csv file:
>
> For each carrier, calculate:
> - Total shipments
> - On-time count and percentage
> - Delayed count (status = 'delayed' or actual > estimated)
> - Average delay in days
> - Total value at risk
>
> Classify carrier risk:
> - HIGH: on-time < 80%
> - MEDIUM: on-time 80-90%
> - LOW: on-time > 90%
>
> Show a carrier health table sorted by risk (highest first)."

### Phase C — Strategic Scoring

Type this prompt into the chat input:

> "Combine the inventory and fulfilment analyses.
>
> For each SKU-warehouse combo, calculate a strategic score:
> - Base severity from inventory health:
>   - OUT_OF_STOCK = 5.0
>   - BELOW_REORDER = 3.0
>   - LOW_STOCK = 2.0
>   - HEALTHY = 0.0
> - Add carrier modifier based on the WORST carrier risk:
>   - HIGH = +3.0
>   - MEDIUM = +1.5
>   - LOW = +0.5
>
> Generate recommendations:
> - Score >= 6: CRITICAL — Immediate escalation
> - Score >= 4: WARNING — Review within 7 days
> - Score >= 2: MONITOR — Track in weekly review
> - Score < 2: OK — No action required
>
> Show the complete strategic scoring table."

### Phase D — Build the Executive Dashboard

Type this prompt into the chat input:

> "Using the combined analysis, produce a unified executive summary:
>
> 1. **Inventory Health Overview**
>    - Count of SKUs in each status category
>    - Total value of at-risk inventory (sum of stock_on_hand * unit_cost for BELOW_REORDER items)
>
> 2. **Fulfilment Health Overview**
>    - On-time rate per carrier
>    - Total value at risk
>
> 3. **Strategic Roadmap**
>    - Number of CRITICAL, WARNING, MONITOR, and OK items
>    - Top 5 highest-scored items with their recommendations"

### Phase E — Export the Blueprint

Type this prompt into the chat input:

> "Write the complete strategic operational blueprint, including:
> 1. Executive summary (one page)
> 2. Inventory health section with status counts and at-risk valuation
> 3. Fulfilment health section with carrier rankings
> 4. Strategic scoring table with all SKU-warehouse combinations
> 5. Prioritised recommendations (CRITICAL items first)
> 6. Appendix with data source descriptions
>
> Also create a CSV table with columns:
> sku, warehouse, stock_on_hand, inventory_status, carrier_risk,
> strategic_score, recommendation"

Use the download button to save the blueprint as `strategic-roadmap.md` and the CSV table as `strategic-roadmap.csv`.

## Expected Output

After completing all phases, you should have:

- A complete inventory health assessment across all 18 SKU-warehouse combos
- A carrier risk evaluation for all 4 carriers
- A strategic score for every combination
- A `strategic-roadmap.md` with the full executive blueprint (approximately 3-5 pages)
- A `strategic-roadmap.csv` with machine-readable prioritised recommendations
- A list of CRITICAL items requiring immediate executive attention
