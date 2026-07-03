# Exercise 1 — Source Material Parsing & Synthesis

## Scenario

Your executive team uses a shared operational log to post daily status updates across departments — Fulfillment, Inventory, Procurement, Operations, and Finance. These entries are free-text with no standard format. You need to parse this raw log into a structured executive summary that classifies each entry by status (positive, warning, critical), extracts quantitative metrics, and produces a department-level heatmap.

## Learning Objectives

- Load unstructured operational log text into Claude Code
- Classify free-text entries by severity using keyword patterns
- Extract quantitative metrics (percentages, dollar amounts, unit counts)
- Generate a structured department-level status summary
- Produce an executive brief with actionable recommendations

## Dataset

Use the inline sample data below, or create `raw_operations_log.csv` from it.

### Inline Operational Log

```csv
department,timestamp,entry
Fulfillment,2026-06-17 08:15,NW1 pick rate dropped to 85% — two pickers out sick. Backlog 320 units. ETA recovery 48h.
Fulfillment,2026-06-17 09:30,Carrier FedEx missed yesterday's pickup at Central. 1200 units delayed. Escalated to account rep.
Inventory,2026-06-17 10:00,WIDG-003 stock at North warehouse = 42 units. Reorder point is 150. Reorder triggered (PO-8910).
Inventory,2026-06-17 11:20,Cycle count complete at South. GADG-010 variance: +12 units found (overage).
Procurement,2026-06-17 08:45,PO-8812 with Apex Logistics marked OVERDUE by 6 days. No communication from vendor.
Procurement,2026-06-17 13:00,New supplier Coastal Shipping onboarded. Terms net-45. Lead time 8-12 days. Contract signed.
Procurement,2026-06-17 14:30,Swift Logistics rate increase notice: +7% on Route A effective July 1. Rebate negotiation requested.
Operations,2026-06-17 07:00,Nightly batch job completed: 12400 orders processed. 99.2% success rate. 98 failed (timeout).
Operations,2026-06-17 12:00,WMS v3.2 upgrade scheduled for June 22 02:00-05:00. Downtime window approved.
Operations,2026-06-17 15:00,SSO login issue reported by 3 warehouse staff. Ticket INC-20260617-004 created. Priority P2.
Finance,2026-06-17 09:00,AP run completed. PO-8800 through PO-8815 approved. Total disbursement $247,320.82.
Finance,2026-06-17 16:00,Acme Corp invoice INV-402 under review — duplicate line items flagged. Payment held.
```

### Known Issues Planted in the Data

| Issue | Location | Notes |
|---|---|---|
| Critical carrier delay | Fulfillment entry 2 | FedEx missed pickup, 1200 units delayed, escalated |
| Stock below reorder | Inventory entry 1 | WIDG-003 at 42 units vs reorder point 150 |
| Overdue PO with no communication | Procurement entry 1 | PO-8812 overdue by 6 days |
| Batch job failures | Operations entry 1 | 98 orders timed out (0.8% failure rate) |
| Duplicate invoice flagged | Finance entry 2 | INV-402 under review, payment held |

## Walkthrough

### Step 1 — Load and inspect the raw log

Start Claude Code and load the operational log:

```bash
claude
```

Paste the following prompt:

```
Load this operational log and tell me:
- How many entries there are
- Which departments are represented
- The time range covered
- Any entries that contain monetary values, percentages, or unit counts
```

### Step 2 — Classify entries by severity

Prompt Claude to classify each entry:

```
For each entry in the operational log, classify it as one of:
- CRITICAL: mentions failed, outage, breach, missing, escalated, timeout, hold, or overdue
- WARNING: mentions delayed, flagged, under review, backlog, variance, dropped, or slow
- POSITIVE: everything else (completed, approved, signed, onboarded, resolved)

Show me a table with: department, timestamp, status, and the first 60 characters of the entry.
```

### Step 3 — Generate a department status heatmap

```
Group the classified entries by department. For each department, count how many
CRITICAL, WARNING, and POSITIVE entries they have. Show me:
- Department name
- Total entries
- Count per status
- The percentage of entries that are CRITICAL or WARNING

Flag any department where more than 30% of entries are non-positive.
```

### Step 4 — Extract quantitative metrics

```
From the operational log, extract every quantitative data point. Show me:
- The entry text
- What metric was found (e.g., "pick rate", "backlog", "success rate", "disbursement")
- The numeric value
- The unit (%, USD, units, days)

List all metrics in a single table, sorted by unit type.
```

### Step 5 — Produce the executive summary

```
Write a one-page executive summary covering:
1. **Period**: The date range covered
2. **Department Health**: Number of CRITICAL items per department
3. **Key Metrics**: The 3 most important numbers from the log
4. **Action Items**: Specific items that need immediate follow-up
5. **Recommendations**: 2-3 suggestions for the next operations sync

Format this as a markdown brief suitable for sharing with the executive team.
Write it to a file called executive_brief.md.
```

## Expected Output

After completing all steps, you should have:

- A classified table of all 12 entries with status labels
- A department heatmap flagging Fulfillment and Procurement as elevated risk
- An extracted metrics table with ~8-10 quantitative data points
- An `executive_brief.md` file with a structured one-page summary
