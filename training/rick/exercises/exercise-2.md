# Exercise 2 — Enterprise Architecture Modeling

## Scenario

Your company operates multiple warehouses that stock overlapping SKUs. When a warehouse runs low on a critical SKU, the system needs to know which other warehouses can fulfill the gap. You need to build a dependency map showing how warehouses are connected through shared inventory, and identify single points of failure where only one warehouse stocks a particular SKU.

## Learning Objectives

- Load and inspect multi-warehouse inventory data
- Map SKU-to-warehouse and warehouse-to-SKU relationships
- Build a warehouse dependency graph based on shared SKUs
- Calculate criticality scores for each warehouse
- Identify single points of failure in the distribution network
- Export findings to a structured report

## Dataset

Use `inventory_stock_levels.csv` from the data directory.

### File: `../data/inventory_stock_levels.csv`

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

### Known Issues Planted in the Data

| Issue | Location | Notes |
|---|---|---|
| Single-warehouse SKU | GADG-020 | Only stocked at WH-South — single point of failure |
| Below reorder point | WIDG-003 @ WH-North | 42 units vs reorder point 150 |
| Below reorder point | WIDG-002 @ WH-East | 45 units vs reorder point 100 |
| Below reorder point | GADG-001 @ WH-South | 150 units vs reorder point 200 |
| Below reorder point | SUPR-001 @ WH-South | 200 units vs reorder point 300 |

## Walkthrough

### Step 1 — Load and inspect inventory data

```bash
claude ../data/inventory_stock_levels.csv
```

Prompt:

```
Describe this inventory dataset:
- How many rows and columns
- What each column means
- How many unique SKUs and warehouses
- Which SKUs are stocked in multiple warehouses vs a single warehouse
```

### Step 2 — Build SKU-warehouse relationship map

```
For each SKU, list all warehouses that stock it. Group by SKU.
Then for each warehouse, list all SKUs it holds. Group by warehouse.

Show me both views in a single report.
```

### Step 3 — Build the warehouse dependency graph

```
Two warehouses are "connected" if they stock at least one common SKU.
Build a dependency graph:
- WH-North <--> [list of connected warehouses]
- WH-East  <--> [list of connected warehouses]
- WH-South <--> [list of connected warehouses]

Explain which warehouse would be the most disruptive if it went offline.
```

### Step 4 — Criticality analysis

```
For each SKU, determine how many warehouses stock it:
- SKUs stocked in exactly 1 warehouse are "exclusive" to that warehouse
- SKUs stocked in 2+ warehouses have redundancy

Calculate per warehouse:
- Total SKUs held
- Number of exclusive SKUs (only stocked here)
- Criticality percentage = (exclusive / total) * 100

Flag any warehouse with criticality >= 50% as HIGH risk.
```

### Step 5 — Export dependency and criticality report

```
Write a structured report to a file called architecture_report.md containing:

1. **SKU-Warehouse Map** — table of every SKU and the warehouses that stock it
2. **Dependency Graph** — text representation of warehouse connections
3. **Criticality Analysis** — table with warehouse, total_skus, exclusive_skus, criticality_pct, risk_level
4. **Single Points of Failure** — list of SKUs with no redundancy
5. **Recommendations** — 2-3 suggestions for reducing dependency risk

Also export the criticality table as criticality_report.csv.
```

## Expected Output

After completing all steps, you should have:

- A complete SKU-warehouse relationship map (14 SKUs × 3 warehouses)
- A warehouse dependency graph showing WH-North as the most connected node
- Criticality analysis flagging WH-South as HIGH risk (GADG-020 is exclusive)
- An `architecture_report.md` with the full analysis
- A `criticality_report.csv` with machine-readable scores
