# Exercise 5 — Capstone: The Data Observability & Alerting Pipeline

## Scenario

Mollie needs to build an automated observability engine that checks an incoming raw transaction table, flags discrepancies, runs a full reconciliation, and fires off a correctly formatted incident alert. This capstone combines all prior skills: root-cause profiling (Ex1), freshness verification (Ex2), reconciliation (Ex3), and webhook orchestration (Ex4).

## Learning Objectives

- Run data quality checks on a raw transaction table
- Detect and classify anomalies (duplicates, negatives, stale pending, amount mismatches)
- Cross-reference transactions against known ledger entries
- Generate structured incident alerts in Slack Block Kit format
- Produce a consolidated pipeline output with report, alert, and summary

## Dataset

### Raw Transactions (`raw-transactions-today.csv`)

```csv
txn_id,order_id,amount,gateway,status,timestamp
TXN-7001,ORD-1001,125.00,stripe,completed,2026-06-17 08:01:00
TXN-7002,ORD-1002,89.50,stripe,completed,2026-06-17 08:03:00
TXN-7003,ORD-1003,250.00,paypal,completed,2026-06-17 08:05:00
TXN-7004,ORD-1004,45.00,stripe,completed,2026-06-17 08:07:00
TXN-7005,ORD-1005,500.00,paypal,completed,2026-06-17 08:10:00
TXN-7006,ORD-1006,32.99,stripe,completed,2026-06-17 08:12:00
TXN-7007,ORD-1002,89.50,stripe,completed,2026-06-17 08:15:00
TXN-7008,ORD-1007,175.00,paypal,pending,2026-06-16 12:00:00
TXN-7009,ORD-1008,-50.00,stripe,completed,2026-06-17 08:20:00
TXN-7010,ORD-1009,1000.00,stripe,completed,2026-06-17 08:22:00
TXN-7011,ORD-1010,65.00,paypal,failed,2026-06-17 08:25:00
TXN-7012,ORD-1011,220.00,stripe,completed,2026-06-17 08:28:00
TXN-7013,ORD-1012,150.00,paypal,completed,2026-06-17 08:30:00
TXN-7014,ORD-1013,75.00,stripe,completed,2026-06-17 08:32:00
TXN-7015,ORD-1014,310.00,stripe,completed,2026-06-17 08:35:00
TXN-7016,ORD-1015,42.50,paypal,completed,2026-06-17 08:38:00
TXN-7017,ORD-1016,600.00,stripe,pending,2026-06-17 08:40:00
TXN-7018,ORD-1001,125.00,stripe,completed,2026-06-17 08:01:00
TXN-7019,ORD-1017,85.00,paypal,completed,2026-06-17 08:42:00
TXN-7020,ORD-1018,195.00,stripe,completed,2026-06-17 08:45:00
TXN-7021,ORD-1019,280.00,stripe,completed,2026-06-17 08:48:00
TXN-7022,ORD-1020,55.00,paypal,completed,2026-06-17 08:50:00
TXN-7023,ORD-1021,410.00,stripe,completed,2026-06-17 08:52:00
TXN-7024,ORD-1022,95.00,stripe,completed,2026-06-17 08:55:00
TXN-7025,ORD-1023,330.00,paypal,pending,2026-06-17 08:58:00
```

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| Duplicate transaction | TXN-7004 and TXN-7018 both reference ORD-1001, same amount ($125), same timestamp — duplicate billing |
| Negative amount | TXN-7009 has amount -$50.00 — data entry error or reversal without reference |
| Stale pending > 19h | TXN-7008 created 2026-06-16 12:00, still pending — 20+ hours without settlement |
| Failed transaction | TXN-7011 status = "failed" — needs root cause investigation |
| Amount mismatch | TXN-7007 is a duplicate of TXN-7002 (same ORD-1002, same amount $89.50) |

## Walkthrough Steps

Open the Weatherman AI Portal in your browser. Select "Mollie" from the sidebar dropdown. Click the paperclip icon to upload the data file, then type each prompt into the chat input.

**Step 1 — Data quality checks and anomaly detection:**

```
Step 1 Prompt:
Upload raw_transactions_today.csv. Run these quality checks:
1. Find exact duplicate rows (same order_id, same amount, same timestamp)
2. Find rows with negative amounts
3. Find rows with status = "failed"
4. Find rows with status = "pending" that are older than 1 hour

Summarize: total issues found, by category.
```

**Step 2 — Root cause timeline:**

```
Step 2 Prompt:
For each anomaly, create a root-cause entry:
- duplicate_billing: TXN-7004 / TXN-7018 on ORD-1001 — likely double charge
- negative_amount: TXN-7009 — $50.00 negative — reversal without reference ID
- stale_pending: TXN-7008 — 20+ hours pending — gateway capture failure?
- failed_txn: TXN-7011 — investigate payment processor error

Sort by severity (duplicate = CRITICAL, stale_pending = HIGH, etc.)
Show a timeline of when each issue first appeared.
```

**Step 3 — Financial reconciliation:**

```
Step 3 Prompt:
Calculate the financial impact of each anomaly:
- Duplicate: $125.00 (TXN-7018) — potential double payout
- Negative amount: -$50.00 (TXN-7009) — needs reversal documentation
- Stale pending: $175.00 (TXN-7008) — unrecognized revenue
- Failed txn: $65.00 (TXN-7011) — lost sale

Total at risk: $XX.XX

Also sum all completed transactions:
  Total completed amount: $X,XXX.XX
  Total pending amount:   $XXX.XX
  Total failed amount:    $XX.XX
  Grand total:            $X,XXX.XX
```

**Step 4 — Alert payload generation:**

```
Step 4 Prompt:
Build a Slack Block Kit JSON payload for the most critical finding
(the duplicate billing). Include:
1. Header: CRITICAL: Duplicate Billing Detected
2. Fields: txn_ids, order_id, amount, gateway, timestamp
3. Context block: "Auto-detected by Observability Pipeline — 2026-06-17"
4. Actions: "Investigate in Ledger" -> "https://finance.internal/orders/ORD-1001"
   and "Acknowledge"

Write the payload to alert_payload.json.
```

**Step 5 — Export consolidated pipeline output:**

```
Step 5 Prompt:
Write two files:

1. incident_report.csv — all anomalies found:
   txn_id, order_id, issue_type, severity, amount, gateway, description

2. pipeline_summary.txt — executive dashboard:

   === OBSERVABILITY PIPELINE — DAILY SUMMARY ===
   Date: 2026-06-17
   Source: raw_transactions_today.csv (25 txns)

   ANOMALIES DETECTED: X
     CRITICAL: 1 — Duplicate billing (ORD-1001, $125.00)
     HIGH:     1 — Stale pending > 19h (TXN-7008, $175.00)
     MEDIUM:   1 — Negative amount (TXN-7009, -$50.00)
     LOW:      1 — Failed transaction (TXN-7011, $65.00)

   FINANCIAL IMPACT:
     Total at risk:        $415.00
     Recognized revenue:   $X,XXX.XX
     Unrecognized (pending): $XXX.XX

   ALERTS FIRED:
     Slack Block Kit payload written to alert_payload.json

   PIPELINE STATUS: COMPLETE — 4 anomalies found, 1 alert fired
```
