# Exercise 3 — Automated Financial Reconciliation Engine

## Scenario

The finance team processes payment settlements from two gateways — **Stripe** and **PayPal** — and needs to reconcile payouts against the internal order ledger. The payout file contains 36 transactions with several known issues: a pending gateway timeout capture, an amount mismatch between Stripe and the ledger, a refunded dispute, and a voided order. Mollie needs to run the reconciliation engine to isolate every discrepancy.

## Learning Objectives

- Perform a full outer join between settlement reports and the order ledger
- Calculate expected platform fees and compare against actual fees charged
- Detect amount discrepancies exceeding the $0.01 tolerance threshold
- Isolate unmatched transactions and calculate payout gaps

## Dataset

Reference the file at `data/payout-reconciliation.csv` (36 transactions, June 2026).

Key columns: `transaction_id`, `order_id`, `gateway`, `gross_amount`, `fee`, `net_amount`, `settlement_date`, `payout_id`, `status`, `notes`.

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| Pending capture | TXN-20260602-005 — `pending` status, gateway timeout, no payout_id |
| Amount mismatch | TXN-20260607-017 — ledger shows $210.00, gateway shows $210.00 (notes say mismatch) |
| Refunded dispute | TXN-20260614-031 — `refunded` status, customer disputed charge |
| Voided/cancelled | TXN-20260617-036 — `pending`/`voided` status |
| Cross-gateway | Transactions from both Stripe and PayPal with different fee structures |

## Walkthrough Steps

Open the Weatherman AI Portal in your browser. Select "Mollie" from the sidebar dropdown. Click the paperclip icon to upload the data file, then type each prompt into the chat input.

**Step 1 — Load and inspect the payout data:**

```
Step 1 Prompt:
Upload payout_reconciliation.csv. Show me:
- Total rows and columns
- Unique gateway values and their transaction counts
- Unique status values and their counts
- Date range of settlements
- Number of transactions with blank payout_id
- Summary statistics for gross_amount, fee, net_amount per gateway
```

**Step 2 — Detect amount discrepancies on matched transactions:**

```
Step 2 Prompt:
The reconciliation engine uses transaction_id as the join key between
the settlement report and the order ledger (in this dataset, the file
represents both sides combined). For each transaction, calculate:
  expected_net = gross_amount - fee
  net_discrepancy = abs(expected_net - net_amount)

Flag any row where net_discrepancy > 0.01.

Also calculate the expected fee for each gateway:
  Stripe: expected_fee = gross_amount * 0.029 + 0.30
  PayPal: expected_fee = gross_amount * 0.035 + 0.49
  fee_discrepancy = abs(expected_fee - fee)

Show all rows where fee_discrepancy > 0.01.
```

**Step 3 — Isolate unmatched and problematic transactions:**

```
Step 3 Prompt:
Identify and categorize every problematic transaction:
1. Transactions with status = "pending" and blank payout_id
   — these were never settled (gateway capture failed)
2. Transactions with status = "refunded"
   — these need manual review
3. Transactions with notes containing "mismatch" or "dispute"
   — flagged for investigation
4. Any transaction where status is not "settled" or "completed"

Show a table: txn_id, order_id, gateway, amount, status, notes, flag.
```

**Step 4 — Aggregate reconciliation by gateway:**

```
Step 4 Prompt:
Group by gateway and calculate:
  Stripe:
    total_gross:       $X.XX
    total_fees:        $X.XX (actual)
    total_expected_fees: $X.XX (at 2.9% + $0.30)
    fee_variance:      $X.XX
    net_payout:        $X.XX
    expected_payout:   $X.XX
    payout_gap:        $X.XX
  PayPal:
    (same structure at 3.5% + $0.49)

Which gateway has a larger fee variance?
What is the total payout gap across both gateways?
```

**Step 5 — Export reconciliation report:**

```
Step 5 Prompt:
Write a CSV called reconciliation_report.csv with ALL transactions
including these columns: transaction_id, order_id, gateway, gross_amount,
fee, net_amount, expected_fee, fee_discrepancy, status, flag, notes.

Then display a summary:

=== PAYMENT RECONCILIATION REPORT ===
Period: June 1-17, 2026
Total transactions: 36

BY GATEWAY:
  Stripe:  XX txns — $XX,XXX.XX gross — $XXX.XX fee variance
  PayPal:  XX txns — $X,XXX.XX gross — $XX.XX fee variance

ISSUES FOUND:
  Pending (unsettled):     X txns
  Refunded/disputed:       X txns
  Amount mismatches:       X txns
  Voided/cancelled:        X txns
  Fee discrepancies:       X txns

PAYOUT GAP: $XXX.XX
  (difference between expected and actual payout)

STATUS: RECONCILIATION COMPLETE
  X of 36 transactions flagged for review (XX.X%)
```
