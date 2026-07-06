# Purchasing & Logistics: Vendor Data Validation

**Course Title:** Vendor Data Validation
**Target User:** Sunny — Purchasing & Logistics team
**Prerequisites:** Basic familiarity with spreadsheets (Excel/CSV); no coding experience required.
**Estimated Duration:** 4 hours (split across two 2-hour sessions)
**Format:** Live walkthrough + hands-on portal exercises

---

## Pre-Work: Load Your Institutional Memory

Before starting this course, open the [Master Guide](https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1) alongside your domain-specific NotebookLM notebook. Review both notebooks to understand how the portal operates in your domain before building any prompts or running analyses.

**Your Domain Notebook:** [Sunny's Purchasing Notebook](https://notebooklm.google.com/notebook/c3dc698d-38e7-4d64-8451-0bbca3fa9d97?authuser=1)

> **Workflow Rule:** All prompt generation, data testing, and document templating in this track must be cross-verified against both the Master Guide and your Domain Notebook before use.

---

## Learning Objectives

By the end of this course, Sunny will be able to:

1. Open the Weatherman AI Portal and upload CSV and Excel files for analysis.
2. Validate vendor transit lead times against a reference table.
3. Cross-reference pricing tables and flag discrepancies.
4. Generate summary reports of all found errors for follow-up with vendors.
5. Build and reuse prompt templates to speed up weekly vendor audits.

---

## Lesson Breakdown

### Lesson 1 — First Contact: Your New Audit Partner (60 min)

**Objective:** Get comfortable with the portal and run the first file analysis.

| Segment | Topic | Activity |
|---|---|---|
| 1.1 | What is the Weatherman AI Portal? | Brief overview — the portal reads files, analyzes data, and answers questions, all from your browser. No software install needed. |
| 1.2 | Logging in and selecting your profile | Open the portal URL, select "Sunny" from the sidebar dropdown, and click the paperclip icon to upload a file. |
| 1.3 | Your first prompt — "What's in this file?" | Upload a sample vendor CSV and ask the portal to summarize columns, row count, and data types. |
| 1.4 | Loading more files | Upload a second file and ask for the same summary. |
| 1.5 | Asking follow-up questions | Practice conversational prompts: "Which rows have empty cells?", "Show me the unique values in the 'vendor_name' column", "What date range does this file cover?" |

**Portal Exercises:**

Upload the file `vendor_prices_april.csv` using the paperclip icon, then type this prompt into the chat input:

```
Read vendor_prices_april.csv and tell me:
- How many rows and columns it has
- What each column name is
- Whether any columns have missing values
- The minimum, maximum, and average price in the "unit_cost" column
```

Then upload `vendor_lead_times.csv` and type:

```
Read vendor_lead_times.csv and tell me:
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
| 2.1 | The lead time problem | Vendors promise a transit window (e.g., 5-7 business days). Actual delivery often exceeds it. Finding these manually takes hours. |
| 2.2 | Loading the lead time data | Upload the vendor lead time CSV and a purchase order log together. |
| 2.3 | Cross-referencing with the portal | Ask the portal to compare promised vs. actual lead times row by row and flag any overages. |
| 2.4 | Quantifying the impact | Have the portal calculate the average delay in days and the percentage of orders that arrive late per vendor. |
| 2.5 | Exporting the results | Instruct the portal to write a CSV of all flagged violations for your records. Then download the file using the download button. |

**Portal Exercises:**

Upload both `vendor_lead_times.csv` and `po_log_march.csv` using the paperclip icon. Then type this prompt:

```
I have two files loaded:
1. vendor_lead_times.csv — columns: vendor_name, promised_min_days, promised_max_days
2. po_log_march.csv — columns: po_number, vendor_name, order_date, received_date

For each purchase order, calculate the actual transit time in business days
(order_date to received_date). Compare it to the vendor's promised range.
Flag any PO where the actual transit time exceeds promised_max_days.

Output a table with: po_number, vendor_name, promised_max_days, actual_days, days_over
```

Follow up with:

```
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
| 3.2 | Loading vendor price data | Upload two files: `vendor_contract_prices.csv` and `vendor_invoice_q1.csv`. |
| 3.3 | Cross-referencing items | Ask the portal to find items on the invoice that don't appear in the contract, and vice versa. |
| 3.4 | Spotting price deviations | Instruct the portal to flag every invoice line where the unit price differs from the contracted price. |
| 3.5 | Flagging math errors | Ask the portal to verify that `quantity * unit_cost = line_total` for each row and report mismatches. |

**Portal Exercises:**

Upload both `vendor_contract_prices.csv` and `vendor_invoice_q1.csv`. Then type:

```
I have two files loaded:
1. vendor_contract_prices.csv — columns: item_code, description, unit_price, currency
2. vendor_invoice_q1.csv — columns: invoice_num, item_code, quantity, unit_price, line_total

List any item_code that appears on the invoice but does NOT appear in the contract.
Also list any item_code in the contract that was never ordered on the invoice.
```

Then type:

```
For each row in vendor_invoice_q1.csv, compare the unit_price against the matching
item_code's unit_price in vendor_contract_prices.csv. Flag any row where they differ.

Show me: invoice_num, item_code, contracted_price, invoice_price, difference
Sort by the largest absolute difference first.
```

Then type:

```
Check every row in vendor_invoice_q1.csv and verify that:
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
| 4.2 | Saving prompts for reuse | Save your master audit prompt in a text file so you can copy-paste it each week without retyping. |
| 4.3 | Running the full audit | Upload all four data files, paste the master prompt, and let the portal run the complete audit. |
| 4.4 | Reading the error report | Review the generated `audit_report.csv`, understand the flags, and plan vendor follow-up. |
| 4.5 | Next steps and further learning | Where to go next: using Workspace Presets to automate common tasks, sharing prompts with the team. |

**Portal Exercises:**

Upload all four files: `vendor_lead_times.csv`, `vendor_contract_prices.csv`, `vendor_invoice_q1.csv`, `po_log_march.csv`.

Then paste this master audit prompt:

```
I have four files loaded:
1. vendor_lead_times.csv — promised transit windows per vendor
2. po_log_march.csv — actual purchase order receipts
3. vendor_contract_prices.csv — contracted SKU prices
4. vendor_invoice_q1.csv — Q1 invoice lines

Please do the following, in order:

## Step 1 — Lead time validation
- Calculate actual transit days for each PO
- Flag any where actual > promised_max_days
- Group results by vendor with counts and averages

## Step 2 — Pricing validation
- Find orphaned items (on invoice not in contract, or vice versa)
- Flag unit price mismatches between contract and invoice
- Verify quantity * unit_price = line_total on every invoice row

## Step 3 — Report
- Write a combined CSV called audit_report.csv with ALL violations
- Each row should have: violation_type, vendor, item_code, expected, actual, notes
- Print a summary: total violations found, breakdown by type
```

Download the generated `audit_report.csv` using the download button.

---

## Sample Data Files

The following sample files are provided in the `data/` folder for use during exercises:

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
| Lead-Time Anomaly preset | `presets/lead-time-anomaly/SKILL.md` |
| Customs Tariff Audit preset | `presets/customs-tariff-audit/SKILL.md` |
| Warehouse Balancing preset | `presets/warehouse-balancing/SKILL.md` |
| XLSX Processing preset | `presets/xlsx-processing/SKILL.md` |
| Data Table Validator preset | `presets/data-table-validator/SKILL.md` |

---

## Success Criteria

Sunny can independently:

- [ ] Log into the Weatherman AI Portal and select the Sunny profile
- [ ] Upload CSV or Excel files using the paperclip icon
- [ ] Ask the portal to calculate transit times and flag late deliveries
- [ ] Cross-reference invoice prices against contract prices
- [ ] Verify line-item math on any pricing table
- [ ] Export a structured CSV of all violations
- [ ] Run the weekly audit using the saved prompt template

### High-Impact Operational Presets

**1. Velocity Depletion Predictor** — analyzing sales speed sheets for exact depletion dates.  
**2. Automated Factory Purchase Order Drafter** — writing PO requests for international manufacturing partners.  
**3. B2B Bulk Order Quote Calculator** — structuring volume-based pricing tier tables.  
**4. Custom Packaging & Logistics Planner** — coordinating box dimensions, printing specs, and weight allocations.  
**5. Accounting Invoice Request Auto-Formatter** — standardizing B2B sales data into itemized Markdown tables.
