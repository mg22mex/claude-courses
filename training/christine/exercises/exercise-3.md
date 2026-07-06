# Exercise 3 — Automated Outbound Email Flow Generation

## Scenario

Christine needs to design and draft a multi-step automated email sequence for a new customer segment. Using the email-automation workspace preset, she will build a structured welcome flow with correct merge tags, brand-voice compliance, and conditional branching. She will also validate an existing flawed email template and analyze a send log for performance issues.

## Learning Objectives

- Design multi-step email sequences with timing, triggers, and goals
- Validate email templates for merge tag correctness and CAN-SPAM compliance
- Enforce brand-voice constraints (subject length, CTA structure, tone)
- Analyze email send logs for deliverability and engagement trends
- Generate campaign-ready email templates with campaign spec sheets

## Dataset

| File | Description |
|---|---|
| `../data/raw_email_campaign.md` | Flawed promotional email with broken merge vars, aggressive tone, and missing unsubscribe link |
| `../data/email_send_log.csv` | Email send log with open rates, click rates, bounces, and unsubscribes across 20 sends |

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| Broken merge tag syntax | `{{customer.first_name,` missing closing braces — malformed variable |
| Hardcoded greeting | "Hey" with no `{{first_name}}` fallback |
| Missing unsubscribe URL | `{{unsubscribe_link}}` instead of `{{unsubscribe_url}}`, formatted as plain text not a link |
| Aggressive tone | Excessive exclamation marks, ALL CAPS, fear-based language ("you are literally falling behind", "STOP MAKING EXCUSES") |
| Competitor mentions | References to Dropbox and Google Drive in negative comparative context |
| Multiple CTAs | "BUY NOW BEFORE IT'S TOO LATE" plus secondary links — no single primary CTA |
| No visible unsubscribe in footer | Unsubscribe link is plain text at the very bottom, not formatted as a clickable link |
| Broken HTML formatting | Mixed `<div>`, `<span>`, `<BR>`, inline styles throughout |

## Walkthrough Steps

Open the Weatherman AI Portal in your browser. Select "Christine" from the sidebar dropdown. Click the paperclip icon and upload `raw_email_campaign.md`.

**Step 1 — Merge tag validation:**

Type this prompt into the chat input:

```
Scan raw_email_campaign.md and report on merge tag health:

1. Which merge tags are present (e.g., {{first_name}}, {{unsubscribe_url}},
   {{offer_code}}, {{expiry_date}})?
2. Which required tags are MISSING?
3. Are there any hardcoded "Dear Customer" or generic greetings
   where {{first_name}} should be used?
4. Is {{unsubscribe_url}} formatted as a clickable link
   (<a href="{{unsubscribe_url}}">Unsubscribe</a>) or as plain text?
5. Are there any broken braces or misspelled variable names?
6. Does the template use {{customer.email}} or similar exposed
   raw identifiers in the body?

Output a tag consistency table: tag, status, line_number, recommendation
```

**Step 2 — Brand-voice and layout audit:**

Type this prompt into the chat input (continuing the same session):

```
Audit the email template against brand rules:

1. Subject line length — is it ≤ 60 characters? If not, suggest a trim.
2. Preheader text — is there one? Is it ≤ 130 characters?
3. Count passive voice instances. List each with line number.
4. Does the email have exactly ONE primary CTA button/link?
   If zero or multiple, flag it.
5. Check for ALL CAPS, exclamation marks, slang, or competitor mentions.
6. Verify unsubscribe link is visible in the footer as a clickable link.
7. Flag any fear-based or negative framing ("falling behind", "mistake",
   "amateur", "embarrassed").

Rate the email overall: [compliant / needs revision / non-compliant]
```

**Step 3 — Design a 3-step welcome flow:**

Type this prompt into the chat input (continuing the same session):

```
Design a 3-step welcome email sequence for new CloudSync subscribers.

Target segment: New signups (free trial)
Goal: Convert free trial to paid subscription within 14 days

For each step, define:
- Trigger condition (what happens to start the step)
- Delay (time after trigger)
- Template goal (what this step should achieve)
- Success metric (measurable outcome)

Step 1 — "Getting Started" (educational, warm)
Step 2 — "Feature Deep Dive" (value demonstration)
Step 3 — "Your Trial is Ending" (urgency + conversion)

For each step, write the full email template including:
- Subject line (≤ 60 chars)
- Preheader (≤ 130 chars)
- Body copy with {{first_name}} and {{unsubscribe_url}} merge tags
- Exactly one primary CTA button per email
- Brand-compliant tone (no fear, no ALL CAPS, no exclamation abuse)

Include a Campaign Spec Sheet table.
```

**Step 4 — Send log performance analysis:**

Open the Weatherman AI Portal in your browser. Select "Christine" from the sidebar dropdown. Click the paperclip icon and upload `email_send_log.csv`.

Type this prompt into the chat input:

```
Load email_send_log.csv and analyze performance:

1. Calculate aggregate metrics:
   - Average delivery rate
   - Average open rate (unique_opens / delivered)
   - Average click-through rate (unique_clicks / delivered)
   - Average bounce rate
   - Average unsubscribe rate

2. For the weekly newsletter series (EM-2026-002, EM-2026-006):
   - Show open rate trend across sends
   - Flag any edition where open rate dropped significantly
   - Identify whether unsubscribe rates are rising

3. For the welcome flow (EM-2026-001 and EM-2026-005):
   - Compare Q1 vs Q2 welcome flow performance
   - Which step has the highest drop-off in each flow?
   - Which version performs better overall?

4. Deliverability flags:
   - Are any campaigns showing bounce rates above 2%?
   - Are spam complaint rates above 0.1%?

Output a performance summary per campaign family with specific recommendations.
```

**Step 5 — Export the campaign package:**

Type this prompt into the chat input (continuing the send-log session):

```
Write two files:

1. welcome_flow_step_1.md — the Step 1 "Getting Started" email template
   with all merge tags, subject line, preheader, body, and CTA

2. send_log_analysis.txt — performance analysis with:

=== EMAIL PERFORMANCE ANALYSIS ===
Period: January — June 2026
Total campaigns tracked: 20 sends across 6 campaign families

AGGREGATE METRICS:
  Avg delivery rate:    XX.X%
  Avg open rate:        XX.X%
  Avg click-through:    XX.X%
  Avg bounce rate:      XX.X%
  Avg unsubscribe rate: XX.X%

CAMPAIGN FAMILY BREAKDOWN:
  Welcome Flow (Q1 v1):  Open rate XX% | CTR XX% | Unsub X.X%
  Welcome Flow (Q2 v2):  Open rate XX% | CTR XX% | Unsub X.X%
  Newsletter Series:     Open rate XX% | CTR XX% | Trend: [improving/declining/stable]
  Promo Blast:           Open rate XX% | CTR XX% | Unsub X.X%
  Cart Abandonment:      Open rate XX% | CTR XX% | Recovery rate XX%

ALERTS:
  - [Campaign]: [issue] — [recommendation]

STATUS: ANALYSIS COMPLETE
```

## Expected Output

- A merge tag consistency table with status per tag
- A brand-voice and layout audit with violations and fixes
- A 3-step welcome flow design with full email templates and spec sheet
- A send log performance analysis with aggregate metrics and alerts
- Downloadable files: `welcome_flow_step_1.md` and `send_log_analysis.txt`
