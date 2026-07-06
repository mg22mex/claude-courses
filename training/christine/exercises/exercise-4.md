# Exercise 4 — Campaign Analytics Reporting & ROAS Optimization

## Scenario

The marketing director needs a comprehensive performance review of all Q1–Q2 2026 campaigns across email, social, search, display, and affiliate channels. Christine must ingest the raw campaign performance data, calculate blended and per-channel ROAS, score channel health, detect anomalies, and produce an executive-ready summary with actionable optimization recommendations.

## Learning Objectives

- Ingest and normalize multi-channel campaign performance data
- Calculate blended ROAS and per-channel ROAS, CTR, conversion rates, and cost per conversion
- Score channel health using weighted factors (ROAS, CTR, conversion rate, cost per conversion)
- Detect statistical outliers and trend breaks using IQR method
- Generate an executive summary with alerts and quick-win recommendations

## Dataset

| File | Description |
|---|---|
| `../data/campaign_performance_data.csv` | Multi-channel campaign performance data (Q1–Q2 2026) with 21 campaigns across 5 channels |

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| Display Prospecting losing money | DISP-2026-002 (Q1) ROAS 0.70x, DISP-2026-004 (Q2) ROAS 0.73x — both below 1.0x |
| Social channels underperforming | All 4 social campaigns have ROAS below 2.0x, well under the 3.0x benchmark |
| Q1 vs Q2 search trend | Brand search ROAS dropped from 5.50x to 6.39x (improved), but Non-Brand dropped from 2.67x to 2.98x (still under 3.0x) |
| Email newsletter decline | Newsletter open rates declining across Q1→Q2 (4.81% → 4.02% CTR), unsubscribe rates rising (185 → 260 → 270 → 265) |
| Cart abandonment improvement | Q1 vs Q2 cart abandonment shows higher recovery in Q2 across all steps |
| Affiliate steady but flat | ROAS consistently 4.2–4.3x — no growth, but not declining |

## Walkthrough Steps

Open the Weatherman AI Portal in your browser. Select "Christine" from the sidebar dropdown. Click the paperclip icon and upload `campaign_performance_data.csv`.

**Step 1 — Data inspection and normalization:**

Type this prompt into the chat input:

```
Load campaign_performance_data.csv. Show me:

1. Total campaigns, date range, and channels present
2. For each channel: number of campaigns, date span
3. Which channels have missing fields (e.g., social has no opens/bounces)
4. Total ad spend, total revenue, and total conversions across all campaigns
5. Any campaigns with zero or missing revenue, zero ad_spend, or zero conversions

Summarize the dataset health before proceeding to calculations.
```

**Step 2 — Blended and per-channel ROAS:**

Type this prompt into the chat input (continuing the same session):

```
Calculate the following:

1. BLENDED (all channels):
   - Total ad spend: $X,XXX.XX
   - Total revenue: $X,XXX.XX
   - Blended ROAS: X.XXx
   - Total conversions: X,XXX
   - Blended cost per conversion: $XX.XX

2. PER CHANNEL: For each channel (email, social, search, display, affiliate):
   - Total spend, total revenue, ROAS
   - Total conversions, cost per conversion
   - Average CTR
   - Average conversion rate

3. Flag each channel:
   - ROAS ≥ 3.0x → GREEN (healthy)
   - ROAS ≥ 1.0x but < 3.0x → YELLOW (underperforming)
   - ROAS < 1.0x → RED (money-losing)

Show a channel breakdown table with ROAS health status.
```

**Step 3 — Channel health scoring:**

Type this prompt into the chat input (continuing the same session):

```
Score each channel on a 0–100 health scale using weighted factors:

| Factor | Weight | Benchmark |
|---|---|---|
| ROAS | 40% | ≥ 3.0 = excellent, ≥ 1.5 = acceptable, < 1.0 = poor |
| CTR | 20% | ≥ 3% (email), ≥ 1% (social), ≥ 2% (search) |
| Conversion Rate | 20% | ≥ 5% (email), ≥ 3% (social/search) |
| Cost Per Conversion | 20% | ≤ $25 (email), ≤ $40 (social/search/display) |

For each channel:
- Calculate sub-score per factor (0–100)
- Apply weight and sum to get channel health score
- Rank channels from highest to lowest

Flag any channel scoring below 50 as CRITICAL.
```

**Step 4 — Anomaly and outlier detection:**

Type this prompt into the chat input (continuing the same session):

```
Use IQR method to detect outlier campaigns within each channel:

For each channel group:
1. Calculate Q1, Q3, and IQR for ROAS and CTR
2. Flag mild outliers (metric < Q1 - 1.5*IQR or > Q3 + 1.5*IQR)
3. Flag extreme outliers (metric < Q1 - 3*IQR or > Q3 + 3*IQR)

Also flag pattern-based anomalies:
- High CTR + Low Conversion Rate → misleading creative or broken landing page
- High Spend + Low ROAS → bid inflation or wrong audience
- Sudden ROAS drop ≥ 30% period-over-period → tracking break or market shift

Show each anomaly with campaign name, metric values, and suggested investigation.
```

**Step 5 — Export executive summary:**

Type this prompt into the chat input (continuing the same session):

```
Write a file called campaign_analysis_report.txt with:

=== CAMPAIGN PERFORMANCE EXECUTIVE SUMMARY ===
Period: Q1–Q2 2026 (January — June)
Channels tracked: 5 (email, social, search, display, affiliate)
Total campaigns:  21

HEADLINE NUMBERS:
  Total ad spend:      $XX,XXX.XX
  Total revenue:       $XXX,XXX.XX
  Blended ROAS:        X.XXx
  Total conversions:   X,XXX
  Avg cost/conv:       $XX.XX

CHANNEL HEALTH RANKINGS:
  1. [Channel] — XX/100 — ROAS X.XXx — [Healthy/At Risk/Critical]
  2. [Channel] — XX/100 — ROAS X.XXx — [Healthy/At Risk/Critical]
  3. [Channel] — XX/100 — ROAS X.XXx — [Healthy/At Risk/Critical]
  4. [Channel] — XX/100 — ROAS X.XXx — [Healthy/At Risk/Critical]
  5. [Channel] — XX/100 — ROAS X.XXx — [Healthy/At Risk/Critical]

ALERTS:
  CRITICAL — Display channel ROAS 0.70x (money-losing)
  CRITICAL — Social channel ROAS below 2.0x across all campaigns
  WARNING  — Email newsletter CTR declining, unsubscribes rising
  WARNING  — Non-Brand Search ROAS still below 3.0x benchmark

QUICK WINS:
  1. Pause Display Prospecting (ROAS 0.70x) — reallocate to Search Brand (ROAS 5.50x+)
  2. Refresh social creative set — all campaigns running 6+ months on same assets
  3. Segment email newsletter by engagement tier to reduce unsubscribe rate
  4. Increase Non-Brand Search bid on top-performing queries to push ROAS above 3.0x

STATUS: ANALYSIS COMPLETE — 2 CRITICAL, 2 WARNING alerts
```

## Expected Output

- A dataset health summary with structural checks
- Blended and per-channel ROAS breakdown with status flags
- Weighted channel health scores with rankings
- Anomaly detection report using IQR method
- A downloadable `campaign_analysis_report.txt` executive summary
