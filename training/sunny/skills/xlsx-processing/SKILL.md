---
name: xlsx-processing
description: Parse, inspect, and audit raw spreadsheet data (.xlsx, .csv, .tsv) — handle cell types, detect anomalies, and flag pricing discrepancies.
---

# xlsx-processing

An operational playbook for loading, parsing, and auditing spreadsheet files. Handles Excel workbooks and flat CSV/TSV files. Use this whenever Sunny needs to inspect a vendor file she's never seen before, check for data quality issues, or prepare tables for deeper validation.

---

## 1. File Intake

### 1.1 Load the file

Pass the file path to Claude Code on launch:

```
claude vendor_submission.xlsx
```

Claude Code reads `.xlsx`, `.csv`, and `.tsv` natively. No special library setup is needed.

### 1.2 Inventory the contents

Always start by asking for a full inventory of what was loaded:

- **For workbooks (.xlsx):** List every sheet name, its row count, and its column headers. Note whether any sheets appear empty (0 rows or a single header row with no data).
- **For flat files (.csv/.tsv):** Print the row count, column count, and all column names. Note the delimiter that was detected.

### 1.3 Identify cell-level issues

Scan each column and report:

| Issue | How to detect |
|---|---|
| Truly empty cells | `null`, `NaN`, or blank — flag the row and column |
| Placeholder empties | Values like `"-"`, `"N/A"`, `"."`, `"0"` — treat as suspicious, flag separately |
| Mixed types in a column | e.g., numbers in a column that is mostly text, or a date column that contains the string "TBD" |
| Currency formatting | e.g., `"$ 12.50"` or `"EUR 10,00"` — note the format so downstream math uses parsed numerics |
| Trailing whitespace | e.g., `"ABC-123 "` — this will break lookups; flag it |

---

## 2. Schema Normalisation

### 2.1 Infer column semantics

Map every column to an expected type. Use these conventions:

| Pattern in header | Expected type |
|---|---|
| `item_code`, `sku`, `part_no`, `product_id` | string — lookup key |
| `unit_price`, `unit_cost`, `line_total`, `amount` | numeric (float) |
| `quantity`, `qty`, `count`, `pcs` | numeric (integer) |
| `date`, `order_date`, `received_date`, `delivery_date` | date |
| `vendor_name`, `vendor`, `supplier` | string — categorical |
| `currency`, `curr` | string — categorical (ISO 4217 code) |
| `description`, `desc`, `notes`, `comments` | string — free text (skip from validation) |

### 2.2 Cast columns to their expected types

Explicitly convert each column. When a cast fails (e.g., `"12.5O"` cannot parse as a float), record it as a type-violation error:

```
item_code: "AB-123" , unit_price: "12.5O"  ← TYPE ERROR in unit_price
```

### 2.3 Normalise text keys

For lookup columns (item codes, vendor names):

1. Strip leading/trailing whitespace.
2. Uppercase the value (prevents "abc-123" vs "ABC-123" mismatches).
3. Flag any duplicate keys — same code appearing more than once in the same table.

---

## 3. Cell-Level Auditing

### 3.1 Out-of-range checks

For every numeric column, compute min, max, mean, and median. Flag values that fall outside reasonable bounds:

- **unit_price < 0 or > 1,000,000** — likely data entry error
- **quantity ≤ 0** — impossible order
- **line_total < 0** — missing negative sign or credit notated as negative
- **Dates** outside the expected range (e.g., a 2026 date in a Q1 2025 file)

### 3.2 Pattern checks on item codes

Item codes usually follow a known pattern (e.g., `XXX-9999`). Compare every code against the expected regex. Flag codes that deviate:

```
Expected pattern: ^[A-Z]{3}-\d{4}$
Violations: "AB-123" (wrong format), "ABC-123" (missing digit), "ABC-01234" (extra digit)
```

### 3.3 Currency consistency

If a `currency` column exists, verify every row in the file uses the same currency code. Mixed currencies in a single pricing sheet must be flagged — converting without explicit rates would be wrong.

---

## 4. Pricing Discrepancy Detection

### 4.1 Line total verification

For every row that has `quantity`, `unit_price`/`unit_cost`, and `line_total`:

```
expected_total = round(quantity × unit_price, 2)
deviation      = abs(expected_total - actual_line_total)
```

Flag any row where `deviation > 0.01`. Report the row key (item code or row number), the expected total, the actual total, and the difference.

### 4.2 Duplicate line detection

Group by `(item_code, unit_price)`. Find groups with >1 occurrence — these may be accidental duplicate entries. Report them.

### 4.3 Unit-price drift (for multi-sheet workbooks)

If the workbook has both a "contract" / "master" sheet and an "invoice" sheet:

1. Join on `item_code`.
2. For each matched pair, compute `price_diff = invoice_price - contract_price`.
3. Flag any row where `abs(price_diff) > 0.01`.

---

## 5. Output Format

Always produce two outputs:

### 5.1 Summary (printed to the terminal)

```
=== AUDIT SUMMARY ===
File: vendor_submission.xlsx
Rows inspected: 1,240
Columns: 8

Violations found: 14
  - Empty cells:         3
  - Type errors:         2
  - Line total mismatch: 4
  - Price deviation:     3
  - Orphaned items:      2

Hard errors (must fix):   9
Warnings (review):        5
```

### 5.2 Detailed report (written to a CSV file)

Write every violation as a row in `audit_report.csv`:

```
violation_type,sheet,row,item_code,field,expected,actual,notes
empty_cell,invoice_q1,42,ABC-1001,unit_price,,,Missing unit price
line_total_mismatch,invoice_q1,58,ABC-2005,line_total,1250.00,1250.01,Deviation: 0.01
price_deviation,invoice_q1,71,ABC-3002,unit_price,15.00,15.50,Overcharged by 0.50
```

---

## 6. Edge Cases

| Situation | Handling |
|---|---|
| File has zero rows (header only) | Report "empty file — no data to audit" and stop |
| File has no recognizable numeric columns | Cannot run pricing checks; print column inventory and note "no pricing columns detected" |
| Item code column missing | Warn: "no item code column found — orphan detection and joins are skipped" |
| Multiple sheets with no clear "main" sheet | Process each sheet independently and prefix every violation with the sheet name |
| Row count > 10,000 | Suggest Sunny split the file by vendor or month and audit in chunks |
| File is password-protected | Tell Sunny: "this file is encrypted — please provide an unprotected copy" |
