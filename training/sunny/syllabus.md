# Purchasing & Logistics: Vendor Data Validation with Claude Code

**Course Title:** Vendor Data Validation with Claude Code
**Target User:** Sunny — Purchasing & Logistics team
**Prerequisites:** Basic familiarity with spreadsheets (Excel/CSV); no coding experience required.
**Estimated Duration:** 4 hours (split across two 2-hour sessions)
**Format:** Live walkthrough + hands-on terminal exercises

---

## Pre-Work: Load Your Institutional Memory

Before starting this course, open the [Master Claude Code Guide](https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1) alongside your domain-specific NotebookLM notebook. Query both notebooks to understand how Claude Code operates in your domain before writing any scripts or building tools.

**Your Domain Notebook:** [Sunny's Purchasing Notebook](https://notebooklm.google.com/notebook/c3dc698d-38e7-4d64-8451-0bbca3fa9d97?authuser=1)

> **Workflow Rule:** All script generation, data testing, or document templating in this track must cross-verify patterns against both the Master Guide and your Domain Notebook before execution.

---

## Learning Objectives

By the end of this course, Sunny will be able to:

1. Open and navigate Claude Code in the terminal.
2. Load raw CSV and Excel files into Claude Code for analysis.
3. Ask Claude Code to validate vendor transit lead times against a reference table.
4. Instruct Claude Code to cross-reference pricing tables and flag discrepancies.
5. Generate summary reports of all found errors for follow-up with vendors.
6. Build and reuse small prompt templates to speed up weekly vendor audits.

---

## Lesson Breakdown

### Lesson 1 — First Contact: Your New Audit Partner (60 min)

**Objective:** Get comfortable with Claude Code and run the first file analysis.

| Segment | Topic | Activity |
|---|---|---|
| 1.1 | What is Claude Code? | Brief overview — Claude Code reads files, runs scripts, and answers questions about data, all from the terminal. No GUI needed. |
| 1.2 | Launching Claude Code | Open your terminal and run `claude` to enter interactive mode. Pass a file directly: `claude data/vendor_prices_april.csv` |
| 1.3 | Your first prompt — "What's in this file?" | Load a sample vendor CSV and ask Claude to summarize columns, row count, and data types. |
| 1.4 | Loading CSV files | Use `claude data/vendor_lead_times.csv` and ask for the same summary. Claude Code reads CSVs natively. |
| 1.5 | Asking follow-up questions | Practice conversational prompts: "Which rows have empty cells?", "Show me the unique values in the 'vendor_name' column", "What date range does this file cover?" |

**CLI Exercises:**

```
# Exercise 1.3 — Load a CSV and get a summary
claude data/vendor_prices_april.csv
```

Prompt to use inside Claude Code:

```
Read data/vendor_prices_april.csv and tell me:
- How many rows and columns it has
- What each column name is
- Whether any columns have missing values
- The minimum, maximum, and average price in the "unit_cost" column
```

```
# Exercise 1.4 — Load a CSV file
claude data/vendor_lead_times.csv
```

Prompt:

```
Read data/vendor_lead_times.csv and tell me:
- How many rows and columns it has
- What each column name is
- What the unique vendor_name values are
- The range of promised_min_days and promised_max_days across all vendors
```

---

### Lesson 2 — Validating Vendor Transit Lead Times (60 min)

**Objective:** Compare actual vs. promised lead times and flag violations.

| Segment | Topic | Activity |
|---|---|---|
| 2.1 | The lead time problem | Vendors promise a transit window (e.g., 5–7 business days). Actual delivery often exceeds it. Finding these manually takes hours. |
| 2.2 | Loading the lead time data | Load the vendor lead time CSV and a purchase order log together. |
| 2.3 | Cross-referencing with Claude | Ask Claude to compare promised vs. actual lead times row by row and flag any overages. |
| 2.4 | Quantifying the impact | Have Claude calculate the average delay in days and the percentage of orders that arrive late per vendor. |
| 2.5 | Exporting the results | Instruct Claude to write a CSV of all flagged violations for your records. |

**CLI Exercises:**

```
# Exercise 2.3 — Validate lead times
claude data/vendor_lead_times.csv data/po_log_march.csv
```

Prompt:

```
I have two files loaded:
1. data/vendor_lead_times.csv — columns: vendor_name, promised_min_days, promised_max_days
2. data/po_log_march.csv — columns: po_number, vendor_name, order_date, received_date

For each purchase order, calculate the actual transit time in business days
(order_date to received_date). Compare it to the vendor's promised range.
Flag any PO where the actual transit time exceeds promised_max_days.

Output a table with: po_number, vendor_name, promised_max_days, actual_days, days_over
```

```
# Exercise 2.4 — Vendor performance summary
Prompt (continuing the same session):

From the violations you found, group them by vendor and tell me:
- Total number of late orders per vendor
- Average days overdue per vendor
- The worst offender (vendor with the most late orders)
Write the full violations table to a file called lead_time_violations.csv
```

---

### Lesson 3 — Parsing Spreadsheets and Finding Pricing Errors (60 min)

**Objective:** Catch unit-price mismatches, missing rows, and calculation errors in vendor pricing tables.

| Segment | Topic | Activity |
|---|---|---|
| 3.1 | Common pricing errors | Wrong unit prices, quantity breaks that don't add up, items on the invoice not in the contract, currency mismatches. |
| 3.2 | Loading vendor price data | Load two CSV files: `vendor_contract_prices.csv` (contracted SKU prices) and `vendor_invoice_q1.csv` (Q1 invoice lines). |
| 3.3 | Cross-referencing items | Prompt Claude to find items on the invoice that don't appear in the contract, and vice versa. |
| 3.4 | Spotting price deviations | Instruct Claude to flag every invoice line where the unit price differs from the contracted price. |
| 3.5 | Flagging math errors | Ask Claude to verify that `quantity × unit_cost = line_total` for each row and report mismatches. |

**CLI Exercises:**

```
# Exercise 3.3 — Find orphaned items
claude data/vendor_contract_prices.csv data/vendor_invoice_q1.csv
```

Prompt:

```
I have two files loaded:
1. `data/vendor_contract_prices.csv` — columns: item_code, description, unit_price, currency
2. `data/vendor_invoice_q1.csv` — columns: invoice_num, item_code, quantity, unit_price, line_total

List any item_code that appears on the invoice but does NOT appear in the contract.
Also list any item_code in the contract that was never ordered on the invoice.
```

```
# Exercise 3.4 — Price deviation check
Prompt (continuing the same session):

For each row in `data/vendor_invoice_q1.csv`, compare the unit_price against the matching
item_code's unit_price in `data/vendor_contract_prices.csv`. Flag any row where they differ.

Show me: invoice_num, item_code, contracted_price, invoice_price, difference
Sort by the largest absolute difference first.
```

```
# Exercise 3.5 — Math validation
Prompt (continuing the same session):

Check every row in `data/vendor_invoice_q1.csv` and verify that:
  quantity * unit_price == line_total

Report any rows where this does not match. For each error, show:
invoice_num, item_code, quantity, unit_price, expected_total, actual_line_total, difference
```

---

### Lesson 4 — Building Your Weekly Audit Workflow (60 min)

**Objective:** Combine everything into a repeatable audit that Sunny can run every week.

| Segment | Topic | Activity |
|---|---|---|
| 4.1 | The audit prompt template | Create a single prompt that loads files, checks lead times, scans pricing, and writes a report — all in one go. |
| 4.2 | Saving prompts as files | Write your master audit prompt to a `.md` file so you can reuse it without retyping. |
| 4.3 | Running the audit in one command | Use `claude` with the prompt file piped in to run the full audit. |
| 4.4 | Reading the error report | Review the generated `audit_report.csv`, understand the flags, and plan vendor follow-up. |
| 4.5 | Next steps & further learning | Where to go next: creating custom skills in `.claude/skills/`, sharing prompts with the team, connecting Claude Code to email or Slack for automated alerts. |

**CLI Exercises:**

```
# Exercise 4.3 — Run the full audit
claude data/vendor_lead_times.csv data/vendor_contract_prices.csv data/vendor_invoice_q1.csv data/po_log_march.csv < weekly_audit_prompt.md
```

**weekly_audit_prompt.md** (create this file during the lesson):

```markdown
I have four files loaded:
1. data/vendor_lead_times.csv — promised transit windows per vendor
2. data/po_log_march.csv — actual purchase order receipts
3. data/vendor_contract_prices.csv — contracted SKU prices
4. data/vendor_invoice_q1.csv — Q1 invoice lines

Please do the following, in order:

## Step 1 — Lead time validation
- Calculate actual transit days for each PO
- Flag any where actual > promised_max_days
- Group results by vendor with counts and averages

## Step 2 — Pricing validation
- Find orphaned items (on invoice not in contract, or vice versa)
- Flag unit price mismatches between contract and invoice
- Verify quantity × unit_price = line_total on every invoice row

## Step 3 — Report
- Write a combined CSV called audit_report.csv with ALL violations
- Each row should have: violation_type, vendor, item_code, expected, actual, notes
- Print a summary: total violations found, breakdown by type
```

---

## Sample Data Files

The following sample files are provided in `data/` for use during exercises:

| File | Description |
|---|---|
| `vendor_lead_times.csv` | 6 vendors with promised transit windows (5 columns, ~20 rows) |
| `po_log_march.csv` | 50 purchase orders from March with actual received dates |
| `vendor_contract_prices.csv` | Contracted SKU prices (20 SKUs, 5 columns) |
| `vendor_invoice_q1.csv` | Q1 invoice lines (32 line items, 6 columns) |
| `vendor_prices_april.csv` | Simple single-sheet CSV for Lesson 1 warm-up |

---

## Link Directory

| Resource | Path / Location |
|---|---|
| Course materials | `training/sunny/` |
| Sample data assets | `training/sunny/data/` |
| Exercise 1 — Vendor Data Ingestion & Schema Alignment | `training/sunny/exercises/exercise-1.md` |
| Exercise 2 — Lead-Time Profiling & Vendor Performance | `training/sunny/exercises/exercise-2.md` |
| Exercise 3 — Customs Tariff & Margin Auditing | `training/sunny/exercises/exercise-3.md` |
| Exercise 4 — Multi-Warehouse Rebalancing Optimization | `training/sunny/exercises/exercise-4.md` |
| Exercise 5 — Capstone Supply Chain Validator | `training/sunny/exercises/exercise-5.md` |
| lead-time-anomaly skill | `skills/lead-time-anomaly/SKILL.md` |
| customs-tariff-audit skill | `skills/customs-tariff-audit/SKILL.md` |
| warehouse-balancing skill | `skills/warehouse-balancing/SKILL.md` |
| xlsx-processing skill | `skills/xlsx-processing/SKILL.md` |
| data-table-validator skill | `skills/data-table-validator/SKILL.md` |

---

## Success Criteria

Sunny can independently:

- [ ] Launch Claude Code and load CSV or Excel files
- [ ] Ask Claude to calculate transit times and flag late deliveries
- [ ] Cross-reference invoice prices against contract prices
- [ ] Verify line-item math on any pricing table
- [ ] Export a structured CSV of all violations
- [ ] Run the weekly audit using the saved prompt template
