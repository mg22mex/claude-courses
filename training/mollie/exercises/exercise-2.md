# Exercise 2 — Deep-Dive Data Freshness Verification

## Scenario

The `orders_etl` pipeline processes data through 5 sequential stages: **Extract -> Normalize -> Join -> Aggregate -> Load**. The pipeline has been failing intermittently for the past 3 days. Stage-level timing logs show that one stage consistently takes 2x longer than the baseline — and during the last run, it timed out completely, causing 6,500 rows to be dropped. Mollie needs to pinpoint exactly where the pipeline stalled.

## Learning Objectives

- Calculate stage-level duration from start/end timestamps
- Identify bottleneck stages by comparing actual vs. baseline duration
- Trace data loss to the specific stage where rows were dropped
- Generate a diagnostic report with bottleneck recommendations

## Dataset

### ETL Timing Log (`etl-timing-log.csv`)

```csv
pipeline_run_id,stage,start_time,end_time,status,rows_processed,error_message
RUN-101,extract,2026-06-17 01:00:00,2026-06-17 01:08:30,success,25000,
RUN-101,normalize,2026-06-17 01:08:30,2026-06-17 01:12:15,success,24800,
RUN-101,join,2026-06-17 01:12:15,2026-06-17 01:28:45,success,24500,
RUN-101,aggregate,2026-06-17 01:28:45,2026-06-17 01:35:00,success,9800,
RUN-101,load,2026-06-17 01:35:00,2026-06-17 01:38:20,success,9800,
RUN-102,extract,2026-06-17 02:00:00,2026-06-17 02:09:15,success,25200,
RUN-102,normalize,2026-06-17 02:09:15,2026-06-17 02:13:30,success,25000,
RUN-102,join,2026-06-17 02:13:30,2026-06-17 02:45:00,success,24800,
RUN-102,aggregate,2026-06-17 02:45:00,2026-06-17 02:52:15,success,9900,
RUN-102,load,2026-06-17 02:52:15,2026-06-17 02:55:40,success,9900,
RUN-103,extract,2026-06-17 03:00:00,2026-06-17 03:10:30,success,24800,
RUN-103,normalize,2026-06-17 03:10:30,2026-06-17 03:15:00,success,24600,
RUN-103,join,2026-06-17 03:15:00,2026-06-17 03:58:00,timeout,18000,Query timed out after 2400s
RUN-103,aggregate,2026-06-17 03:58:00,2026-06-17 04:02:15,success,6200,
RUN-103,load,2026-06-17 04:02:15,2026-06-17 04:04:30,success,6200,
RUN-104,extract,2026-06-17 04:00:00,2026-06-17 04:07:45,success,25100,
RUN-104,normalize,2026-06-17 04:07:45,2026-06-17 04:11:30,success,24900,
RUN-104,join,2026-06-17 04:11:30,2026-06-17 04:36:15,success,24700,
RUN-104,aggregate,2026-06-17 04:36:15,2026-06-17 04:42:30,success,9900,
RUN-104,load,2026-06-17 04:42:30,2026-06-17 04:45:15,success,9900,
```

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| Join stage degradation | Join duration grows across runs: 16.5m -> 31.5m -> 43m -> 24.75m |
| Timeout in RUN-103 | Join stage timed out after 2,400 seconds (40 minutes) |
| Data loss in RUN-103 | 18,000 rows entered join stage, only 6,200 emerged — 6,500 rows lost vs. baseline |
| Baseline row drop | Normalize stage consistently drops 200-400 rows (data quality filtering) |
| Aggregate stage collapse | 24,500 rows -> 9,800 rows is a 60% collapse — normal? Check if expected |

## Walkthrough Steps

Open the Weatherman AI Portal in your browser. Select "Mollie" from the sidebar dropdown. Click the paperclip icon to upload the data file, then type each prompt into the chat input.

**Step 1 — Calculate stage durations:**

```
Step 1 Prompt:
For each stage in each pipeline run, calculate:
  duration_min = (end_time - start_time) in minutes

Show a pivot table:
Run ID | Extract | Normalize | Join | Aggregate | Load | Total
```

**Step 2 — Identify the bottleneck stage:**

```
Step 2 Prompt:
For each stage, calculate the average duration across all runs.
The "join" stage is the suspect — show:
- Run 101 join: XX min
- Run 102 join: XX min
- Run 103 join: XX min (TIMEOUT)
- Run 104 join: XX min

What is the trend? Is the join stage degrading over time?
Which run had the longest join duration?
```

**Step 3 — Trace data loss:**

```
Step 3 Prompt:
For each run, track the row count through each stage:
  RUN-101: 25000 -> 24800 -> 24500 -> 9800 -> 9800
  RUN-102: 25200 -> 25000 -> 24800 -> 9900 -> 9900
  RUN-103: 24800 -> 24600 -> 18000 -> 6200 -> 6200
  RUN-104: 25100 -> 24900 -> 24700 -> 9900 -> 9900

Calculate rows lost per stage per run.
In RUN-103, how many rows were lost in the join stage?
(18000 entered, 6200 emerged from aggregate — but how many left the join stage?)
What is the expected row count after aggregate stage? Compare to baseline.
```

**Step 4 — Correlate duration with data loss:**

```
Step 4 Prompt:
Create a correlation table:
Run ID | Join Duration (min) | Rows Entering Join | Rows After Aggregate | % Retained
 RUN-101 | 16.5 | 24500 | 9800 | 40.0%
 RUN-102 | 31.5 | 24800 | 9900 | 39.9%
 RUN-103 | 43.0 | 18000 | 6200 | 34.4%
 RUN-104 | 24.75 | 24700 | 9900 | 40.1%

Is there a correlation between join duration and row retention?
What does the RUN-103 data loss pattern suggest about the root cause?
```

**Step 5 — Export diagnostic report:**

```
Step 5 Prompt:
Write a file called etl_diagnostic.csv with:
pipeline_run_id, stage, duration_min, rows_in, rows_out, rows_lost, status, flags

Then display a summary:

=== ETL PIPELINE DIAGNOSTIC REPORT ===
Pipeline: orders_etl
Analysis period: 2026-06-17 01:00 -- 04:45

BOTTLENECK: Join Stage
  Avg duration: 28.9 min (vs 15 min baseline)
  Max duration: 43.0 min (RUN-103 -- TIMEOUT)
  Degradation trend: +160% across 4 runs

DATA LOSS:
  Total rows lost (RUN-103 join): ~6,500 (36% of entering rows)
  Probable cause: Query timeout caused partial result set

RECOMMENDATIONS:
  1. Optimize join query — add indexes on order_id and payment_id
  2. Increase query timeout from 2400s to 3600s as temporary mitigation
  3. Add retry logic with exponential backoff on the join stage
  4. Set up stage-level monitoring alerts (duration > 20 min -> WARNING)
```
