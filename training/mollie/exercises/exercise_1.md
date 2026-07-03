# Exercise 1 — Incident Root-Cause Profiling

## Scenario

The nightly ETL pipeline failed at 2:34 AM. The data team needs a root-cause analysis from the Monte Carlo observability logs. The logs show a cascade of failures: a freshness breach on the `orders` table triggered a volume drop on `payments`, which then caused a null rate spike on the `email` field during the join step. Mollie needs to trace the cascade from first failure to final impact.

## Learning Objectives

- Parse observability incident logs to identify failure sequences
- Classify check failures by severity and dimension
- Trace failure cascades to identify root cause vs. downstream symptoms
- Write a structured root-cause analysis report

## Dataset

### Monte Carlo Incident Log (`monte_carlo_incident_log.csv`)

```csv
timestamp,check_name,status,value,threshold,dimension,severity
2026-06-17 02:15:00,freshness_orders,FAILED,45,15,table,HIGH
2026-06-17 02:15:30,freshness_orders,RETRY,45,15,table,HIGH
2026-06-17 02:16:00,freshness_orders,FAILED,46,15,table,HIGH
2026-06-17 02:20:00,volume_payments,PASS,125000,100000,dimension,LOW
2026-06-17 02:22:00,volume_payments,FAILED,72000,100000,dimension,MEDIUM
2026-06-17 02:24:00,null_rate_email,FAILED,12.5,5.0,field,HIGH
2026-06-17 02:26:00,null_rate_email,FAILED,15.2,5.0,field,HIGH
2026-06-17 02:28:00,freshness_inventory,PASS,8,24,table,LOW
2026-06-17 02:30:00,freshness_orders,FAILED,48,15,table,HIGH
2026-06-17 02:35:00,dim_row_count_orders,FAILED,95000,150000,dimension,HIGH
2026-06-17 02:40:00,volume_payments,FAILED,45000,100000,dimension,CRITICAL
2026-06-17 02:45:00,null_rate_email,FAILED,18.7,5.0,field,CRITICAL
2026-06-17 02:50:00,dim_row_count_payments,FAILED,42000,80000,dimension,HIGH
2026-06-17 03:00:00,volume_customers,PASS,5000,4000,dimension,LOW
2026-06-17 03:10:00,freshness_orders,FAILED,52,15,table,CRITICAL
```

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| First failure cascade | `freshness_orders` fails first (02:15) — this is the root cause |
| Downstream volume drop | `volume_payments` drops from 125K to 72K to 45K — caused by stale orders table |
| Null rate escalation | `null_rate_email` spikes from 12.5% to 18.7% — caused by bad join on stale data |
| Critical escalation | `null_rate_email` and `freshness_orders` both reach CRITICAL by 03:10 |
| Non-impacted checks | `freshness_inventory`, `volume_customers` — unaffected (narrow blast radius) |

## Walkthrough Steps

```
claude monte_carlo_incident_log.csv --skill monte-carlo-analyze-root-cause
```

**Step 1 — Load and classify:**
```
Step 1 Prompt:
Load monte_carlo_incident_log.csv. Show me:
- All unique check_name values
- All unique severity levels
- The chronological sequence of FAILED checks
- Which checks passed vs. failed

Filter to FAILED rows only, sorted by timestamp.
```

**Step 2 — Build the incident timeline:**
```
Step 2 Prompt:
For each FAILED check, calculate the time since the previous failure:
  gap_minutes = current_timestamp - previous_timestamp

Create a timeline table:
timestamp, check_name, severity, gap_minutes, status

Which check failed first? That's the likely root cause.
```

**Step 3 — Trace the failure cascade:**
```
Step 3 Prompt:
Group the failures by dimension (table, dimension, field). For each
dimension, identify:
- The first check that failed in that dimension
- The severity trend (did it get worse over time?)
- The relationship to other dimensions

Draw the cascade: freshness_orders → volume_payments → null_rate_email
Explain how the first failure triggered the downstream failures.
```

**Step 4 — Classify by blast radius:**
```
Step 4 Prompt:
Classify each failed check by blast radius:
- TABLE: affects a single table (narrow)
- DIMENSION: affects a data quality dimension (medium)
- FIELD: affects a specific field (narrow, but high impact)

Which checks have the widest blast radius?
Which checks should be prioritized for investigation?
```

**Step 5 — Export root cause report:**
```
Step 5 Prompt:
Write a file called root_cause_report.csv with the structured findings:
Root cause: freshness_orders (started at 02:15, never recovered)
Cascade: freshness_orders → volume_payments → null_rate_email → dim_row_count_orders
Total duration: XX minutes
Checks affected: X of X
Highest severity: CRITICAL (on X checks)

Then print a terminal summary:

=== INCIDENT ROOT CAUSE ANALYSIS ===
Incident:   Nightly ETL Failure — 2026-06-17
Duration:   XX minutes (02:15 — XX:XX)

ROOT CAUSE: freshness_orders
The orders table stopped receiving fresh data at 02:15.
This caused downstream failures in payments volume (stale join)
and email field quality (null rate spike).

FAILURES BY SEVERITY:
  CRITICAL:  X checks
  HIGH:      X checks
  MEDIUM:    X checks
  LOW:       X checks (passed unaffected)

BLAST RADIUS:
  Tables affected:     orders, payments
  Fields affected:     email
  Unaffected:          inventory, customers

RECOMMENDATION:
  1. Fix the orders table ingestion pipeline (source: Shopify API)
  2. Add backpressure mechanism to prevent downstream processing on stale data
  3. Set up dependency-aware alerting to reduce alert noise from cascading failures
```
