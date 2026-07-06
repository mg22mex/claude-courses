# Exercise 4 — Executive KPI & Board Room Slide Structuring

## Scenario

The executive team needs a board-ready carrier performance review pack. You have fulfilment data covering multiple carriers across several weeks. Your job is to analyse on-time rates, identify value at risk, and generate a structured board deck outline that the `ppt-generation` preset can turn into a presentation.

## Learning Objectives

- Upload and analyse carrier-level fulfilment data in the Weatherman AI Portal
- Calculate on-time percentages and average delay by carrier and week
- Identify value at risk (total declared value of delayed shipments)
- Rank carriers by performance
- Generate a structured board deck outline
- Use the `ppt-generation` preset to produce a presentation-ready deck

## Dataset

Use `fulfillment_delay_report.csv` from the data directory. Upload it using the paperclip icon.

### File: `fulfillment_delay_report.csv`

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
| Delayed — no actual delivery | FUL-1004 | FedEx, $12,000 at risk |
| Delayed — no actual delivery | FUL-1010 | FedEx, $3,400 at risk |
| Delayed — no actual delivery | FUL-1015 | FedEx, $9,800 at risk |
| Delayed — no actual delivery | FUL-1018 | USPS, $6,500 at risk |
| Late delivery | FUL-1002 | UPS, 2 days late |
| Late delivery | FUL-1005 | USPS, 2 days late |
| Late delivery | FUL-1007 | USPS, 6 days late |
| Late delivery | FUL-1011 | USPS, 4 days late |

## Walkthrough

### Step 1 — Log into the portal and upload fulfilment data

Open the Weatherman AI Portal in your browser. Select "Rick" from the sidebar dropdown. Upload the `fulfillment_delay_report.csv` file using the paperclip icon.

Type this prompt into the chat input:

> "Summarize this fulfilment dataset:
> - How many orders
> - Which carriers are represented
> - The date range covered
> - How many orders have status 'delayed' (no actual_delivery)
> - The total declared value of all shipments"

### Step 2 — Calculate carrier performance KPIs

Type this prompt into the chat input:

> "For each carrier, calculate:
> 1. Total shipments
> 2. On-time deliveries (actual_delivery <= estimated_delivery)
> 3. Late deliveries (actual_delivery > estimated_delivery)
> 4. Delayed shipments (status = 'delayed', no actual_delivery yet)
> 5. On-time percentage
> 6. Average delay in days (for late deliveries)
> 7. Total value at risk (sum of declared_value for delayed + late shipments)
>
> Show the results in a table sorted by on-time percentage ascending."

### Step 3 — Weekly trend analysis

Type this prompt into the chat input:

> "Group the data by week (based on ship_date). For each week, calculate:
> - Total shipments per carrier
> - On-time percentage per carrier per week
>
> Show me a weekly trend table. Identify any carrier whose on-time rate
> dropped significantly from one week to the next."

### Step 4 — Generate a board deck outline using ppt-generation

Upload the `presets/ppt-generation/SKILL.md` file using the paperclip icon, then type this prompt:

> "Run the ppt-generation preset.
>
> Here is the data context:
>
> Carrier Performance Summary:
> - FedEx: 5 shipments, 60% on-time, $25,200 value at risk
> - UPS: 4 shipments, 75% on-time, $0 value at risk
> - DHL: 3 shipments, 100% on-time, $0 value at risk
> - USPS: 4 shipments, 25% on-time, $6,500 value at risk
>
> Reporting period: March 1-10, 2026
> Total shipments: 20
> Total value at risk: $31,700
>
> Generate an 8-slide board deck outline covering:
> 1. Title slide
> 2. Executive summary
> 3. Carrier ranking (on-time %)
> 4. Value at risk by carrier
> 5. Weekly trend analysis
> 6. Root cause summary (which carriers and why)
> 7. Recommendations
> 8. Appendix — data sources and methodology"

### Step 5 — Export the deck outline

Type this prompt into the chat input:

> "Write the generated board deck with these details:
> - Slide titles and purposes
> - Key data points for each slide
> - Visual suggestions (chart types, layout)
> - Speaker notes / talking points for the executive presenter
> - An appendix with data source references"

Use the download button to save the output as `board-deck-outline.md`.

## Expected Output

After completing all steps, you should have:

- A carrier KPI table showing USPS as the worst performer (25% on-time) and DHL as the best (100%)
- A weekly trend analysis showing performance changes over time
- A `board-deck-outline.md` with 8 structured slides ready for presentation building
- Practical experience using the `ppt-generation` executive preset
