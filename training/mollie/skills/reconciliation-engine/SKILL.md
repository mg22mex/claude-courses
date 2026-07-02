---
name: reconciliation-engine
description: Cross-reference payment settlement tables against core order ledgers to isolate financial drops, platform fee discrepancies, and payout mismatches.
---

# reconciliation-engine

A structured blueprint for reconciling transaction logs against order ledgers using Claude Code. This skill ingests settlement reports and order data, cross-verifies amounts, flags discrepancies, and produces a financial reconciliation report. Run this whenever Mollie needs to isolate payout gaps or platform fee errors.

---

## 1. Intake & Schema

### 1.1 Accept input formats

This skill accepts **two or more** inputs — at minimum one settlement file and one order ledger:

- **`.csv`** — Payout settlement reports from payment gateways (Stripe, PayPal, Shopify Payments), order ledger exports
- **`.json`** — Payout batch records, platform fee statements
- **Free-form prompt** — Date range, gateway, and expected totals when files are unavailable

If no files are supplied, prompt Mollie to provide the settlement export and order ledger.

### 1.2 Normalized schema

Map incoming columns to these canonical fields:

| Canonical Field | Settlement Source | Order Ledger Source |
|---|---|---|
| `transaction_id` | txn_id, gateway_ref, stripe_charge_id | order_id, transaction_ref |
| `order_id` | order_number, invoice_id | order_id, order_number |
| `gross_amount` | amount, total, settlement_amount | total_price, grand_total |
| `fee` | fee, gateway_fee, processing_fee | transaction_fee, payment_fee |
| `net_amount` | net, payout_amount, settlement_net | — (calculated) |
| `currency` | currency, currency_code | currency |
| `transaction_date` | created, settlement_date, paid_at | created_at, paid_at |
| `gateway` | source, payment_method | gateway, payment_gateway |
| `status` | status, txn_status | financial_status, fulfillment_status |

### 1.3 Validate input completeness

Before processing, verify:

- Both files have matching date ranges (warn if off by more than 1 day)
- Required columns exist in each file (prompt Mollie to map if column names differ)
- No empty files or files with only header rows

---

## 2. Cross-Reference Engine

### 2.1 Join on transaction ID

Perform a **full outer join** between settlement records and order ledger records on `transaction_id`:

```
Matched:    Present in both files
Settlement only:  In settlement file but not in order ledger
Ledger only:      In order ledger but not in settlement file
```

### 2.2 Amount discrepancy detection

For every matched row, calculate:

```
amount_diff = settlement.gross_amount - ledger.gross_amount
fee_diff    = settlement.fee - ledger.fee
```

Flag any row where:

- `|amount_diff| > 0.01` — gross amount mismatch
- `|fee_diff| > 0.01` — fee discrepancy
- Net amount can't be derived: `settlement.net_amount != settlement.gross_amount - settlement.fee`

### 2.3 Missing transaction isolation

- **Settlement-only records**: These are payouts without matching orders — possible test transactions, duplicate payouts, or data entry errors
- **Ledger-only records**: These are orders that were never settled — possible failed captures, voided transactions, or gateway sync failures

### 2.4 Aggregated reconciliation

Summarize by gateway and by day:

| Gateway | Settled Amount | Ledger Amount | Difference | Fee Variance | Record Count |
|---|---|---|---|---|---|
| Stripe | $12,450.00 | $12,448.50 | +$1.50 | -$0.75 | 142 |
| PayPal | $3,200.00 | $3,250.00 | -$50.00 | $0.00 | 38 |

---

## 3. Payout Mismatch Diagnosis

### 3.1 Platform fee audit

Compare per-transaction fees against the expected rate:

```
expected_fee = gross_amount * fee_percentage + flat_fee
fee_overcharge = actual_fee - expected_fee
```

Flag any gateway where average `fee_overcharge > 0` across more than 5% of transactions.

### 3.2 Expected vs. actual payout

Calculate:

```
expected_payout = sum(all settled net_amounts)
actual_payout  = sum(settlement amounts in payout batch)
payout_gap     = expected_payout - actual_payout
```

If `|payout_gap| > 0.50`, flag and isolate which transactions are missing from the batch.

### 3.3 Currency conversion flag

If settlement and ledger use different currencies, flag every row for manual review. Do not auto-convert.

---

## 4. Output & Reporting

### 4.1 Discrepancy table

Output a table with all flagged items:

```
| Type | Transaction ID | Settlement Amt | Ledger Amt | Diff | Fee Diff | Action |
|---|---|---|---|---|---|---|
| Amount mismatch | txn_001 | $25.00 | $24.50 | +$0.50 | $0.00 | Review |
| Missing from ledger | txn_002 | $15.00 | — | — | — | Find order |
| Missing from settlement | ord_003 | — | $30.00 | — | — | Check capture |
```

### 4.2 Summary rollup

```
=== RECONCILIATION SUMMARY ===
Date range:             2026-06-01 → 2026-06-30
Total transactions:     285
Matched OK:             270  (94.7%)
Amount mismatches:        8  (2.8%)
Missing from ledger:      4  (1.4%)
Missing from settlement:  3  (1.1%)
Fee discrepancies:        5  (1.8%)

Payout gap:             -$12.40  (expected $15,430.00, actual $15,417.60)

Overall status:         REVIEW RECOMMENDED
```

### 4.3 Export options

Offer to write the discrepancy table as `reconciliation_report.csv` and the full joined dataset as `reconciliation_full_export.csv`.

---

## 5. Strictness Rules

| # | Rule | Enforcement |
|---|---|---|
| 1 | Every matched transaction MUST have `|amount_diff| ≤ 0.01` to be marked OK | Hard block on misclassification |
| 2 | Full outer join MUST be used — never inner join | Hard block — silent matching hides orphans |
| 3 | Currency columns MUST be compared; auto-conversion is forbidden | Hard block if attempted |
| 4 | Fee audit MUST calculate expected fee using the gateway's published rate | Warning |
| 5 | Payout gap MUST be reported even if zero | Hard block — missing $0.00 gap means skipped calculation |
| 6 | Settlement-only records MUST be listed, never silently ignored | Hard block |
| 7 | Any file with < 10 rows MUST be flagged as possibly a test extract | Warning |

---

## 6. Edge Cases

| # | Scenario | Handling |
|---|---|---|
| 1 | Settlement file uses gateway reference IDs, order ledger uses internal order IDs | Attempt fuzzy match on amount + date; flag unmatcheable rows |
| 2 | Refund transactions: negative amounts in settlement file | Compare absolute values; flag as refund, not mismatch |
| 3 | Multi-currency file contains mixed currencies in same column | Split by currency before reconciling; never sum across currencies |
| 4 | Fee column is missing from settlement file | Estimate fee as gross - net; flag as estimated, not actual |
| 5 | Order ledger has duplicate order IDs (split shipments) | Sum all splits for same order_id before comparing |
| 6 | Settlement file covers 31 days but ledger only covers 30 | Trim to overlapping date range; flag the excluded day |
| 7 | Payout batch includes subscription renewals with zero-fee trials | Flag zero-amount transactions separately; exclude from fee audit |
