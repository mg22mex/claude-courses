---
name: campaign-analytics
description: Ingest unstructured or structured marketing performance logs (Open Rates, CTR, Conversion Rates, ROAS, Ad Spend) and output clean performance summaries, ROI/ROAS calculations, and actionable optimization recommendations for leadership.
---

# campaign-analytics

A structured playbook for analyzing marketing campaign performance data with Claude Code. This skill ingests raw metrics across email, social, search, and display channels, normalizes the data, calculates ROI and ROAS, flags underperforming segments, and produces executive-ready summaries. Run this whenever Christine needs to report on campaign effectiveness or identify optimization opportunities.

---

## 1. Intake & Data Schema

### 1.1 Accept input formats

This skill accepts **one or more** inputs:

- **`.csv`** — Campaign performance export with standard metric columns (see 1.2)
- **`.json`** — API export from ad platforms (Meta Ads, Google Ads, LinkedIn Campaign Manager)
- **Free-form prompt** — Description of campaign performance when structured data is unavailable

If no files are provided, prompt Christine to supply a campaign performance export from the marketing platform.

### 1.2 Normalize to standard schema

Map all incoming data to this standard column set:

```
campaign_id        string   — unique identifier
campaign_name      string   — human-readable name
channel            string   — email / social / search / display / affiliate
start_date         date     — YYYY-MM-DD
end_date           date     — YYYY-MM-DD
impressions        integer  — total impressions / sends
reach              integer  — unique reached users
clicks             integer  — total clicks
ctr                decimal  — click-through rate (%)
conversions        integer  — attributed conversions
conversion_rate    decimal  — conversion rate (%)
revenue            decimal  — attributed revenue (USD)
ad_spend           decimal  — total spend (USD)
roas               decimal  — return on ad spend (revenue / spend)
cost_per_conv      decimal  — cost per conversion (USD)
opens              integer  — email opens only
bounces            integer  — email bounces only
unsubscribes       integer  — email unsubscribes only
```

Flag any channel-required field that is missing (e.g., `opens` required for email, `impressions` required for social).

---

## 2. Performance Calculation Engine

### 2.1 Calculate missing metrics

If any metric is absent, derive it from available columns:

| Missing Metric | Formula |
|---|---|
| CTR | `clicks / impressions * 100` |
| Conversion Rate | `conversions / clicks * 100` |
| ROAS | `revenue / ad_spend` |
| Cost Per Conversion | `ad_spend / conversions` |
| Revenue (if missing ROAS) | `ad_spend * roas` |
| Profit | `revenue - ad_spend - estimated_cogs` |

### 2.2 Period-over-period comparison

If the dataset spans multiple periods (weeks/months/quarters), calculate:

- **Absolute change**: `current_period_value - previous_period_value`
- **Percentage change**: `((current - previous) / previous) * 100`
- **Trend direction**: up / down / flat (flat = change within ±5%)

### 2.3 Channel health scoring

Score each channel on a 0–100 scale based on:

| Factor | Weight | Benchmark |
|---|---|---|
| ROAS | 40% | ≥ 3.0 = excellent, ≥ 1.5 = acceptable, < 1.0 = poor |
| CTR | 20% | ≥ 3% (email), ≥ 1% (social), ≥ 2% (search) |
| Conversion Rate | 20% | ≥ 5% (email), ≥ 3% (social/search) |
| Cost Per Conversion | 20% | ≤ 25% of average order value |

---

## 3. Anomaly & Outlier Detection

### 3.1 Statistical outlier flagging

Use IQR (interquartile range) to flag outlier campaigns:

- Calculate Q1, Q3, and IQR for each metric per channel
- **Mild outlier**: `metric < Q1 - 1.5*IQR` or `metric > Q3 + 1.5*IQR` → warning
- **Extreme outlier**: `metric < Q1 - 3*IQR` or `metric > Q3 + 3*IQR` → alert

### 3.2 Pattern-based flags

| Pattern | Signal | Suggested Action |
|---|---|---|
| High CTR + Low Conversion | Misleading creative or broken landing page | Audit landing page funnel |
| High Spend + Low ROAS | Bid inflation or wrong audience targeting | Reduce spend, refine audience |
| Low Opens + High CTR | Strong subject line, weak deliverability | Check sender reputation |
| Sudden ROAS drop ≥ 30% | Possible tracking break or market shift | Verify pixel + attribution window |
| Zero conversions on high-traffic campaign | Technical integration failure | Check conversion tracking setup |

### 3.3 Week-over-week trend breaks

For campaigns running ≥ 3 weeks, detect trend breaks:

- Compare last 7 days vs. prior 7 days
- Flag any metric that changed by ≥ 25% in either direction

---

## 4. Output & Reporting

### 4.1 Executive summary

```
# Campaign Performance Summary — Q3 2026

## Headline numbers
Total ad spend:      $48,200
Total revenue:       $156,400
Blended ROAS:        3.2x
Total conversions:   1,840
Avg cost/conv:       $26.20

## By channel
| Channel | Spend | Revenue | ROAS | Conv. | Trend |
|---|---|---|---|---|---|
| Email    | $8,400  | $42,000 | 5.0x | 520  | ▲ +12% |
| Social   | $22,000 | $52,800 | 2.4x | 680  | ▼ -8%  |
| Search   | $12,800 | $44,800 | 3.5x | 480  | ▲ +5%  |
| Display  | $5,000  | $16,800 | 3.4x | 160  | ▼ -15% |

## 🚨 Alerts
1. Social ROAS dropped 22% WoW — likely audience fatigue
2. Display CTR is 0.4% (below 0.8% benchmark)
3. Email unsubscribes spiked 40% on weekly blast

## Quick wins
- Pause Display retargeting (ROAS 0.8x) and reallocate to Search
- Refresh Social creative set — current set is 12 weeks old
- Segment Email weekly blast by engagement tier to reduce unsubscribes
```

### 4.2 Optimization recommendations

For each flagged issue, output:

```
Issue:     Social ROAS dropped 22% WoW (from 3.1x to 2.4x)
Root cause: Likely audience fatigue (creative set age: 12 weeks)
Severity:   High
Recommendation:
  1. Refresh top-3 ad creatives with new visuals and copy
  2. Split existing audience: engaged (last 30 days) vs. cold
  3. Set frequency cap of 3 impressions/person/week
  4. Re-measure in 7 days; target: restore ROAS to ≥ 3.0x
```

### 4.3 Export options

- **Full dataset**: `campaign_analysis.csv` — enriched with calculated metrics and anomaly flags
- **Executive report**: Terminal printout with summary table, alerts, and quick wins (as shown in 4.1)
- **Leadership deck**: Condensed key-value pairs for slide insertion (ROAS, trend arrows, top alert)

---

## 5. Strictness Rules

| # | Rule | Enforcement |
|---|---|---|
| 1 | ROAS MUST be calculated as `revenue / ad_spend` (never revenue / cost) | Hard calculation rule |
| 2 | Every output MUST include blended ROAS across all channels | Hard output requirement |
| 3 | Any campaign with ROAS < 1.0 MUST be flagged with "🚨 Alert" | Hard rule |
| 4 | Percentage change MUST be labeled with direction (up/down/flat) | Required output format |
| 5 | Outlier detection MUST use IQR method, not standard deviation | Method requirement |
| 6 | Missing required fields (spend, revenue, channel) MUST be flagged before calculation | Hard block |
| 7 | Channel-level breakdown MUST use the normalized channel list (email/social/search/display/affiliate) | Schema requirement |

---

## 6. Edge Cases

| # | Scenario | Handling |
|---|---|---|
| 1 | Single campaign row with no period break | Skip period-over-period comparison; run point-in-time analysis |
| 2 | Zero ad_spend with non-zero revenue (organic/earned) | Flag as organic; exclude from ROAS calculation; report separately |
| 3 | Conversions column is all zeros | Flag possible tracking failure; skip conversion-based metrics; report impressions + clicks only |
| 4 | ROAS is missing and revenue is zero | Flag as "no revenue attributed"; set ROAS to 0.0; treat as non-performing |
| 5 | Dataset has no channel column | Attempt to infer channel from campaign_name keywords (e.g., "FB_" → social, "EM_" → email) |
| 6 | Currency values use inconsistent formats ($1,234.56 vs 1234.56 vs 1.234,56) | Normalize to USD decimal format; flag if parsing is ambiguous |
| 7 | Campaign spans < 7 days with no prior period | Run point-in-time analysis only; mark trend indicators as "insufficient data" |
