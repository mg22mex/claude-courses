# Exercise 1 — Vendor Data Ingestion & Schema Alignment

## Scenario

Three vendors — **Apex Logistics**, **Global Haulers**, and **Prime Cargo** — each submitted their product catalog as a CSV file. Unfortunately, each vendor uses different column names for the same data. You need to unify all three into a single consistent schema so the procurement team can run cross-vendor price comparisons.

## Learning Objectives

- Map inconsistent vendor schemas into a uniform data model
- Identify unmappable or ambiguous columns
- Flag missing required fields
- Generate a consolidated, normalized vendor catalog

## Dataset

Create three files from the tables below, or paste them inline in your prompt.

### Vendor A: Apex Logistics (`apex_catalog.csv`)

```csv
item_code,description,unit_price,currency,moq,lead_time_days
APX-100,Widget Small 4in,12.50,USD,100,7
APX-101,Widget Large 8in,18.75,USD,50,10
APX-102,Gadget Pro,45.00,USD,25,14
APX-103,Gadget Lite,22.00,USD,100,5
APX-104,Gadget Max,89.00,USD,10,21
```

### Vendor B: Global Haulers (`global_catalog.csv`)

```csv
sku,product_name,cost_per_unit,currency_code,minimum_order,delivery_lead
GLB-200,Widget Small 4in,11.90,USD,150,9
GLB-201,Widget Large 8in,17.50,USD,100,12
GLB-202,Gadget Pro,43.00,USD,50,14
GLB-999,Super Widget,200.00,USD,5,30
```

### Vendor C: Prime Cargo (`prime_catalog.csv`)

```csv
part_number,title,rate,curr,min_qty,estimated_delivery,notes
PRM-300,Widget Small 4in,13.00,USD,200,6,low stock priority
PRM-301,Widget Large 8in,19.50,USD,75,8,
PRM-302,Gadget Pro,47.00,USD,30,10,
PRM-303,Gadget Lite,23.50,USD,150,7,new supplier
PRM-304,Gadget Max,92.00,USD,15,18,
PRM-999,Unknown Part,999.00,USD,1,5,price needs verification
```

### Known Issues Planted in the Data

| Issue | Where |
|---|---|
| Column name mismatch | `item_code` vs `sku` vs `part_number` — all mean product ID |
| Column name mismatch | `unit_price` vs `cost_per_unit` vs `rate` — all mean price |
| Column name mismatch | `currency` vs `currency_code` vs `curr` |
| Column name mismatch | `moq` vs `minimum_order` vs `min_qty` |
| Column name mismatch | `lead_time_days` vs `delivery_lead` vs `estimated_delivery` |
| Orphan SKU — `GLB-999` Super Widget | Appears only in Global Haulers — no equivalent in other vendors |
| Orphan SKU — `PRM-999` Unknown Part | Suspicious part number and price — needs investigation |
| Missing field | Prime Cargo has `notes` column — no equivalent in other schemas |

## Walkthrough Steps

```
claude apex_catalog.csv global_catalog.csv prime_catalog.csv
```

**Step 1 — Schema inventory:**
```
Step 1 Prompt:
I have three vendor catalog files. For each file, show me:
- Row count and column names
- The data type of each column (string, number, etc.)
- Any blank or missing cells
- The range of prices and lead times

Present this as a schema comparison table.
```

**Step 2 — Build a unified column mapping:**
```
Step 2 Prompt:
Create a mapping table that translates each vendor's column names
into a unified schema with these canonical fields:
- product_id
- product_name
- unit_price (USD)
- currency
- min_order_qty
- lead_time_days

Show me the mapping as a table:
Canonical Field | Apex Column | Global Column | Prime Column
```

**Step 3 — Transform to unified schema:**
```
Step 3 Prompt:
Transform all three vendor catalogs into the unified schema.
For each vendor file, output a clean table using the canonical
column names. If a vendor is missing a field (e.g., Prime Cargo
has no direct "min_order_qty" — use "min_qty"), map what you can.
Flag any values that seem suspicious.
```

**Step 4 — Flag unmappable columns and orphans:**
```
Step 4 Prompt:
Identify:
1. Any column in a vendor file that has NO equivalent in the unified schema
   (e.g., Prime Cargo's "notes" column — what should we do with this data?)
2. Any product that appears in only one vendor's catalog (orphans)
3. Any product_id that looks suspicious or non-standard

Explain the business impact of each finding.
```

**Step 5 — Export consolidated catalog:**
```
Step 5 Prompt:
Write a CSV called consolidated_vendor_catalog.csv with all products
from all three vendors in the unified schema. Add a "vendor" column
to identify the source. Add a "notes" column for any flags.

Then print a terminal summary:

=== VENDOR CATALOG CONSOLIDATION SUMMARY ===
Vendors processed:    3
Total products:       XX
Products in unified:  XX
Orphan products:      X
Suspicious entries:   X
Unmappable columns:   X (list them)

Consolidated file: consolidated_vendor_catalog.csv
```
