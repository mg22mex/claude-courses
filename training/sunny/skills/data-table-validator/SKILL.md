---
name: data-table-validator
description: Intake raw vendor pricing sheets, isolate item codes, verify line totals, and flag pricing discrepancies and orphaned rows against a master cost sheet.
---

# data-table-validator

A strict operational playbook for validating vendor pricing data. This skill takes one or more raw vendor pricing sheets (.csv, .tsv, or .md tables), cross-references them against a master cost sheet, and produces a structured violation report. Run this whenever Sunny receives a new pricing file from a vendor and needs to confirm every line is accurate before approving.

---

## 1. Intake & Schema Mapping

### 1.1 Accept input formats

This skill accepts:

- **`.csv`** — comma-separated, with or without a header row
- **`.tsv`** — tab-separated
- **Markdown tables** — inline tables in a `.md` file or piped directly as text
- **`.xlsx`** — single-sheet or multi-sheet workbooks (each sheet is treated as a separate table)

When a file is loaded, immediately inspect it and confirm the format with Sunny before proceeding.

### 1.2 Identify the required columns

Scan the header row to locate these columns. If any are missing, report immediately and do not proceed with validation until Sunny clarifies the mapping.

| Required column | Aliases accepted |
|---|---|
| `item_code` | `sku`, `part_no`, `product_id`, `code`, `item`, `part_number`, `material` |
| `unit_price` | `price`, `unit_cost`, `cost`, `rate` |
| `quantity` | `qty`, `count`, `pcs`, `units`, `vol` |
| `line_total` | `total`, `amount`, `extended_price`, `net_amount` |

Also detect these **optional** columns if present:

| Optional column | Aliases accepted |
|---|---|
| `currency` | `curr`, `ccy` |
| `description` | `desc`, `item_desc`, `notes` |
| `vendor` | `vendor_name`, `supplier`, `supplier_name` |

### 1.3 Report schema to the user

Print a confirmed schema like this before running any checks:

```
Schema confirmed:
  item_code   → "SKU"           (string)
  unit_price  → "Unit Price"    (numeric)
  quantity    → "QTY"           (numeric — integer)
  line_total  → "Line Total"    (numeric)
  vendor      → "Supplier"      (string)

Optional columns found: currency, description
Missing: (none)

Proceed with validation? (y/n)
```

Wait for Sunny to confirm before continuing.

---

## 2. Data Cleansing

### 2.1 Strip and normalise item codes

For every row in every table:

1. Strip leading/trailing whitespace from the item code.
2. Convert to uppercase.
3. Remove zero-width characters (Unicode `\u200B`, `\u200C`, `\u200D`, `\uFEFF`).
4. Report any code that was modified during cleansing.

### 2.2 Parse numeric fields

Parse `unit_price`, `quantity`, and `line_total` as numerics:

1. Strip currency symbols (`$`, `€`, `£`, `¥`) and thousand separators.
2. Normalise decimal commas to decimal points (e.g., `"12,50"` → `12.50`).
3. If a value cannot be parsed, record it as a `parse_error`.

### 2.3 Remove known-noise rows

Skip rows matching any of these patterns before validation:

- Row is entirely empty
- Row is a subtotal or total line (header contains "total", "subtotal", "sum")
- Row is a page break or formatting spacer (all cells empty except column count matches)

Report the number of skipped rows.

---

## 3. Item Code Isolation

### 3.1 Build the unified item-code index

Collect every unique item code across all loaded tables. For each code, record:

- Which table(s) it appears in
- How many times it appears in each table

### 3.2 Detect duplicates within each table

If the same item code appears more than once in a single table, flag every duplicate occurrence. Duplicate codes inside a single file may indicate:

- Accidental repeated rows
- Deliberate qty-break pricing (requires confirmation from Sunny)
- Split-line shipments (requires confirmation)

Show Sunny the duplicates and ask how to treat them:

```
WARNING: 3 item codes appear multiple times in "invoice_q1":

  1. ITM-0042  — appears 2 times (rows 12, 13)
  2. ITM-0088  — appears 3 times (rows 31, 32, 33)
  3. ITM-0101  — appears 2 times (rows 45, 89)

Treat as errors? (y = flag all, n = keep all, r = review per-code)
```

---

## 4. Line-Total Verification

### 4.1 Verify every row

For every row that has all three of `quantity`, `unit_price`, and `line_total`:

```
expected = round(quantity × unit_price, 2)
match   = abs(expected - line_total) <= 0.01
```

### 4.2 Report mismatches

For every row where `match` is false, output:

```
LINE TOTAL ERROR | item_code | row | qty | unit_price | expected | actual | deviation
```

### 4.3 Partial data handling

- If `quantity` is missing but `unit_price` and `line_total` exist → infer `quantity = line_total / unit_price`, flag as `inferred_qty`.
- If `unit_price` is missing but `quantity` and `line_total` exist → infer `unit_price = line_total / quantity`, flag as `inferred_price`.
- If two of the three fields are missing → cannot verify; flag as `unverifiable`.

---

## 5. Cross-Reference Against Master Cost Sheet

### 5.1 Identify the master

If multiple tables are loaded, look for one that represents the master/contract:

- Sheet/table named `"contract"`, `"master"`, `"contract_prices"`, `"price_list"`, or `"catalog"`
- Table with the most rows is presumed to be the master (heuristic)
- If no master can be identified, ask Sunny: "Which table contains the reference pricing?"

### 5.2 Find orphaned items

**Orphan A — invoice items not in master:**

Every item code appearing in the vendor's invoice/pricing sheet that does NOT appear in the master cost sheet. These are items Sunny is being charged for that have no contracted price. Flag every one.

**Orphan B — master items not in invoice:**

Every item code in the master that never appears in the vendor's invoice. These are items that were contracted but never ordered. Flag these only as a summary count (they are informational, not necessarily errors).

### 5.3 Compare unit prices

For every item code that appears in BOTH the master and the invoice:

```
price_diff = invoice_unit_price - master_unit_price
pct_diff   = (price_diff / master_unit_price) × 100
```

Flag any row where `abs(price_diff) > 0.01`. Sort the output by absolute price difference descending so the largest overcharges appear first.

```
PRICE DEVIATION | item_code | master_price | invoice_price | diff | pct
```

---

## 6. Output & Reporting

### 6.1 Print a terminal summary

```
╔══════════════════════════════════════════════════╗
║         DATA TABLE VALIDATOR — REPORT           ║
╠══════════════════════════════════════════════════╣
║ Tables loaded:        2                         ║
║ Rows inspected:       1,240                     ║
║ Rows skipped (noise): 4                         ║
║                                                  ║
║ LINE TOTAL ERRORS      12                        ║
║ PRICE DEVIATIONS        8                        ║
║ ORPHANED ITEMS          3                        ║
║ UNVERIFIABLE ROWS       1                        ║
║ PARSE ERRORS            2                        ║
║                                                  ║
║ STATUS: FAIL — 26 issues found                  ║
╚══════════════════════════════════════════════════╝
```

Status is **PASS** if zero issues found, **FAIL** otherwise.

### 6.2 Write a detailed CSV

Write `validation_report_<YYYYMMDD>.csv` with these columns:

```
violation_type,table,row,item_code,field,expected,actual,notes
```

One row per violation. Include every issue type so Sunny can sort/filter in her spreadsheet software.

### 6.3 Write a summary JSON (for programmatic use)

Write `validation_report_<YYYYMMDD>.json` containing a machine-readable version:

```json
{
  "status": "FAIL",
  "tables_loaded": 2,
  "rows_inspected": 1240,
  "issues": {
    "line_total_errors": 12,
    "price_deviations": 8,
    "orphaned_items": 3,
    "unverifiable_rows": 1,
    "parse_errors": 2
  },
  "violations": [
    {
      "type": "line_total_error",
      "table": "invoice_q1",
      "row": 42,
      "item_code": "ITM-0042",
      "expected": 1250.00,
      "actual": 1250.01
    }
  ]
}
```

---

## 7. Strictness Rules (Do Not Deviate)

1. **Never round away a discrepancy.** If `abs(expected - actual) > 0.01`, flag it. A penny matters when multiplied across thousands of line items.
2. **Never skip orphan detection.** Always cross-reference all loaded tables. If only one table is loaded, tell Sunny: "Only one table provided — cannot detect orphans against a master. Provide a master cost sheet to enable cross-reference."
3. **Never modify the original file.** All cleansing and normalisation happens in-memory. Output reports are separate files.
4. **Never proceed without confirmation on ambiguous schemas.** If the column mapping is uncertain, present the options and wait for Sunny to choose.
5. **Always report totals.** Even if zero violations are found, print the summary box showing PASS so Sunny knows validation ran fully.

---

## 8. Edge Cases

| Situation | Handling |
|---|---|
| File is empty (0 rows) | Print "ERROR: file is empty" and abort |
| No numeric columns found | Print "ERROR: no pricing columns detected — cannot validate" |
| Item code column missing entirely | Continue validation using row numbers as identifiers, note "no item codes — orphan detection disabled" |
| Single row in file | Validate normally but warn "only 1 row — verify file is complete" |
| File size > 5 MB | Warn and suggest splitting before proceeding |
| Extremely large price deviations (>100%) | Flag but also note "deviation exceeds 100% — possible data error or currency mismatch" |
| Mixed currencies in one table | Flag every row that deviates from the majority currency. Do NOT convert. |
