# Exercise 4 — Multi-Warehouse Inventory Rebalancing

## Scenario

Three warehouses — North, Central, and South — hold stock of the same SKUs but with very different inventory positions. North is overloaded on Widget Small while South is nearly out. Central has excess Gadget Pro units expiring soon. Sunny needs to analyze all three warehouses, identify stock imbalances, and recommend inter-warehouse transfers before the monthly distribution deadline.

## Learning Objectives

- Calculate days of stock across multiple warehouses
- Flag stockout risks (< 3 days of stock)
- Identify overstocked items for potential rebalancing
- Generate transfer recommendations to optimize inventory distribution

## Dataset

### North Warehouse (`north_inventory.csv`)

```csv
sku,description,stock_on_hand,daily_demand,lead_time_days,max_capacity
WIDG-001,Widget Small 4in,5000,120,5,8000
WIDG-002,Widget Large 8in,150,8,7,500
GADG-010,Gadget Pro,40,5,10,200
GADG-020,Gadget Lite,600,15,6,1000
GADG-030,Gadget Max,10,2,14,50
```

### Central Warehouse (`central_inventory.csv`)

```csv
sku,description,stock_on_hand,daily_demand,lead_time_days,max_capacity
WIDG-001,Widget Small 4in,200,40,5,500
WIDG-002,Widget Large 8in,300,12,7,400
GADG-010,Gadget Pro,250,15,10,300
GADG-020,Gadget Lite,80,10,6,200
GADG-030,Gadget Max,30,5,14,100
```

### South Warehouse (`south_inventory.csv`)

```csv
sku,description,stock_on_hand,daily_demand,lead_time_days,max_capacity
WIDG-001,Widget Small 4in,50,35,5,100
WIDG-002,Widget Large 8in,200,15,7,300
GADG-010,Gadget Pro,15,8,10,50
GADG-020,Gadget Lite,300,20,6,400
GADG-030,Gadget Max,0,1,14,20
```

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| North overstocked on WIDG-001 | 5000 units vs 120 daily demand = 41.7 days of stock |
| South near stockout on WIDG-001 | 50 units vs 35 daily demand = 1.4 days of stock |
| South stockout on GADG-030 | 0 units on hand, daily demand = 1 |
| Central overstocked on GADG-010 | 250 units vs 15 daily demand = 16.7 days (may expire) |
| North near stockout on GADG-030 | 10 units vs 2 daily demand = 5 days of stock |
| Central low on GADG-020 | 80 units vs 10 daily demand = 8 days |

## Walkthrough Steps

Open the Weatherman AI Portal in your browser. Select **Sunny** from the sidebar dropdown. Click the paperclip icon to upload all three files: `north_inventory.csv`, `central_inventory.csv`, and `south_inventory.csv`.

**Step 1 — Calculate days of stock per warehouse:**

Type this prompt into the chat input:

```
For each warehouse, calculate days_of_stock per SKU:
  days_of_stock = stock_on_hand / daily_demand

Build a combined table:
SKU | North Stock | North Days | Central Stock | Central Days | South Stock | South Days

Flag any SKU-warehouse where days_of_stock < 3 as "STOCKOUT RISK"
Flag any where days_of_stock > 30 as "OVERSTOCKED"
```

**Step 2 — Identify stock imbalances:**

Type this prompt:

```
For each SKU, compare days_of_stock across all three warehouses.
Identify transfer opportunities where:
- One warehouse has > 20 days of stock (surplus)
- Another warehouse has < 7 days of stock (deficit)

Show: SKU, surplus_warehouse, surplus_days, deficit_warehouse, deficit_days
```

**Step 3 — Calculate transfer quantities:**

Type this prompt:

```
For each transfer opportunity, calculate the recommended transfer quantity:
  target_stock = deficit_warehouse_daily_demand * 14 (2 weeks buffer)
  transfer_qty = target_stock - deficit_warehouse_stock_on_hand

Cap the transfer at 50% of the surplus warehouse's excess:
  available = surplus_stock - (surplus_daily_demand * 14)

Show: SKU, from_warehouse, to_warehouse, transfer_qty, available, status
```

**Step 4 — Generate rebalancing plan:**

Type this prompt:

```
Build the complete rebalancing plan. For each transfer, check if:
1. The surplus warehouse has enough available stock
2. The receiving warehouse has capacity (stock + transfer <= max_capacity)
3. The transfer quantity is at least 10 units (minimum economical transfer)

Flag any transfer that violates these rules.
```

**Step 5 — Export and summarize:**

Type this prompt:

```
Write a file called rebalance_plan.csv with columns:
sku, from_warehouse, to_warehouse, transfer_qty, reason, approval_required

Then print the final summary:

=== WAREHOUSE REBALANCING PLAN ===
Warehouses analyzed:    3 (North, Central, South)
SKUs tracked:           5

Stockout risks:         X
Overstocked items:      X
Transfer opportunities: X

Transfers recommended:
  North -> South:    X units (SKU)
  Central -> North:  X units (SKU)
  ...

After rebalancing, stockout risk items: X
After rebalancing, overstocked items:   X

Recommended action: Approve transfers and update WMS by end of week.
```

Click the download button to save the generated CSV file.
