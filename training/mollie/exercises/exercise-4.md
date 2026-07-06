# Exercise 4 — Multi-Source Webhook Payload Orchestration

## Scenario

Operations needs automated Slack alerts when critical system metrics breach thresholds. Mollie needs to configure the anomaly-alert-webhook preset to classify incoming metric readings by severity, build platform-specific payloads (Slack Block Kit + Teams Adaptive Card), and enforce webhook delivery rules.

## Learning Objectives

- Classify metric readings against severity thresholds
- Build structured Slack Block Kit JSON payloads
- Build structured Teams Adaptive Card JSON payloads
- Apply multi-alert batching rules (CRITICAL never batched)
- Verify message truncation and variable resolution rules

## Dataset

### Metrics Thresholds (`metrics-thresholds.json`)

```json
{
  "metrics": [
    {
      "name": "payments_volume",
      "value": 45000,
      "threshold_critical": 50000,
      "threshold_warning": 75000,
      "unit": "transactions",
      "description": "Daily payments processed"
    },
    {
      "name": "failed_transactions",
      "value": 320,
      "threshold_critical": 500,
      "threshold_warning": 200,
      "unit": "failures",
      "description": "Failed payment attempts"
    },
    {
      "name": "api_latency_p99",
      "value": 2800,
      "threshold_critical": 3000,
      "threshold_warning": 1500,
      "unit": "ms",
      "description": "P99 API response latency"
    },
    {
      "name": "queue_depth",
      "value": 12500,
      "threshold_critical": 10000,
      "threshold_warning": 5000,
      "unit": "messages",
      "description": "Message queue backlog"
    },
    {
      "name": "error_rate_5xx",
      "value": 4.2,
      "threshold_critical": 5.0,
      "threshold_warning": 2.0,
      "unit": "percent",
      "description": "HTTP 5xx error rate"
    }
  ]
}
```

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| payments_volume below critical | 45,000 < 50,000 — CRITICAL alert (revenue impact) |
| failed_transactions above warning | 320 > 200 — WARNING alert |
| api_latency_p99 above warning | 2,800ms > 1,500ms — WARNING alert (approaching CRITICAL) |
| queue_depth above critical | 12,500 > 10,000 — CRITICAL alert (backlog growing) |
| error_rate_5xx above warning | 4.2% > 2.0% — WARNING alert (approaching CRITICAL) |

## Walkthrough Steps

Open the Weatherman AI Portal in your browser. Select "Mollie" from the sidebar dropdown. Click the paperclip icon to upload the data file, then type each prompt into the chat input.

**Step 1 — Classify metrics by severity:**

```
Step 1 Prompt:
Upload metrics_thresholds.json. For each metric, determine severity:
- If value >= threshold_critical -> CRITICAL
- If value >= threshold_warning -> WARNING
- Otherwise -> INFO

Also calculate how far each metric is beyond its threshold:
  severity_magnitude = (value - threshold) / threshold * 100

Show: metric_name, value, threshold, severity, magnitude_pct
```

**Step 2 — Apply batching rules:**

```
Step 2 Prompt:
Apply the alert batching rules:
1. CRITICAL alerts MUST be sent individually (never batched)
2. WARNING and INFO alerts may be batched up to 5 per payload

How many individual webhook payloads are needed for CRITICAL alerts?
How many batched payloads for WARNING/INFO alerts?
Show the grouping plan.
```

**Step 3 — Build Slack Block Kit payload for a CRITICAL alert:**

```
Step 3 Prompt:
For the most severe CRITICAL metric (queue_depth), build a Slack
Block Kit JSON payload with:
1. Header block: CRITICAL: Queue Depth Alert — bold text
2. Fields block: metric_name, value, threshold, severity_magnitude_pct,
   unit, and a "View Dashboard" link as "https://monitoring.internal/dashboards/queue-depth"
3. Context block with timestamp
4. Actions block with "Acknowledge" and "Escalate" buttons

The payload must use valid Slack Block Kit JSON format with type,
text, fields, accessory, and action_id properties.
```

**Step 4 — Build Teams Adaptive Card for a WARNING batch:**

```
Step 4 Prompt:
Batch the two WARNING alerts (failed_transactions, api_latency_p99)
into a single Teams Adaptive Card payload with:
1. FactSet showing each metric's name, value, threshold, and magnitude
2. Action.OpenUrl button labeled "View Operations Dashboard"
   pointing to "https://monitoring.internal/dashboards/ops"
3. TextBlock summary: "2 WARNING alerts detected — review recommended"

The payload must use valid Teams Adaptive Card JSON format with
$schema, type, body, and actions properties.
```

**Step 5 — Verify and export:**

```
Step 5 Prompt:
Verify these delivery rules:
1. All {variable} placeholders are resolved (none left in output)
2. No text field exceeds 500 characters (truncate with [truncated] suffix)
3. CRITICAL alerts are individual (never batched)

Write two files:
1. slack_alert_critical.json — the CRITICAL alert (queue_depth)
2. teams_alert_warning_batch.json — the WARNING batch

Then display the summary:

=== WEBHOOK PAYLOAD ORCHESTRATION SUMMARY ===
Source: metrics_thresholds.json (5 metrics)

CLASSIFICATION:
  CRITICAL: 2 alerts (individual delivery)
  WARNING:  2 alerts (batched — 1 payload)
  INFO:     1 alert (suppressed — no action needed)

PAYLOADS GENERATED:
  Slack Block Kit:  1 (CRITICAL — queue_depth)
  Teams Adaptive Card: 1 (WARNING batch — failed_txns + latency)

VARIABLE RESOLUTION:  All resolved
MESSAGE TRUNCATION:   None needed (all under 500 chars)
BATCHING RULES:       Compliant

Delivery endpoints:
  Slack:    https://hooks.slack.com/services/...
  Teams:    https://outlook.office.com/webhook/...

Status: READY FOR DELIVERY
```
