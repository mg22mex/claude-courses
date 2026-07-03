# Exercise 5 — Capstone: The Marketing Launch Campaign Pipeline

## Scenario

Christine is executing a full-scale product launch for **CloudSync Business Edition** — a new B2B tier aimed at small-to-medium teams. She needs to run an integrated workflow that takes a raw launch asset checklist, runs an SEO copy audit on the landing page copy, drafts the automated email launch sequence, and sets up a campaign performance tracking template. This capstone combines all four prior skills: brand compliance (Ex1), listing SEO (Ex2), email automation (Ex3), and campaign analytics (Ex4).

## Learning Objectives

- Ingest and validate a multi-asset launch checklist
- Audit launch copy for brand compliance and SEO keyword presence
- Draft a multi-step email launch sequence with merge tags and brand-voice compliance
- Define campaign performance tracking parameters with target KPIs
- Produce a consolidated pipeline output with all deliverables

## Dataset

### Launch Asset Checklist (`launch_asset_checklist.csv`)

```csv
asset_type,asset_name,status,owner,notes
landing_page,CloudSync Business Edition Landing Page,needs_review,Christine,SEO audit pending — target keywords not yet verified
email_sequence,Launch Announcement Email,needs_review,Christine,Draft exists — needs merge tag validation
email_sequence,Feature Deep Dive Email,not_started,Christine,Use Business Edition feature list
email_sequence,Free Trial Offer Email,not_started,Christine,14-day free trial with no credit card
social_post,LinkedIn Launch Announcement,not_started,Christine,Professional tone — B2B audience
social_post,Twitter Launch Teaser,not_started,Christine,Short and punchy — character limit 280
social_post,Facebook Community Post,not_started,Christine,Community-oriented — customer stories angle
landing_page,Features Comparison Table,needs_review,Christine,Compare Business vs Pro vs Enterprise
email_sequence,Trial Expiration Reminder,not_started,Christine,Day 12 of 14-day trial — urgency
report_template,Launch Performance Dashboard,not_started,Christine,Define KPIs and tracking parameters
report_template,Weekly Launch Report Template,not_started,Christine,Executive summary format
```

### Launch Copy Snippets (`launch_copy_snippets.md`)

Create this file from the content below:

```markdown
# CloudSync Business Edition — Launch Copy

## Hero Section

Introducing CloudSync Business Edition — the platform that was built for teams who need better cloud storage.

Unlike Dropbox or Google Drive, Business Edition was designed with team collaboration at its core.

## Feature Highlights

- Cloud sync for your entire team — keep everyone on the same page
- Real-time backup of all team files — because losing data is for amateurs
- Enterprise security with team management controls
- Cross-platform access from any device

## Pricing

Just $15/seat/month for teams of 5-50. This is literally the best deal in enterprise cloud storage!!!

## CTA

Start Your Free Trial Today — No Credit Card Required!!!

## FAQ

Can I upgrade from Pro? Yes. Your existing files will be migrated automatically.

Is my data secure? Absolutely. AES-256 encryption is used for all data.
```

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| Passive voice in hero | "was built" — should be active voice ("built for teams") |
| Competitor mention | "Unlike Dropbox or Google Drive" — comparative competitor reference |
| Off-tone language | "losing data is for amateurs" — negative framing, unprofessional |
| Superlative without evidence | "literally the best deal" — superlative with no supporting data |
| Excessive exclamation | "!!!" on CTA and pricing section |
| Missing SEO keywords | "file sharing", "cloud storage" not in landing page copy |
| Incomplete assets | 5 of 11 launch assets marked "not_started" |
| Email sequence has no templates | All 3 email assets need full template drafting |
| No performance KPIs defined | Launch Dashboard and Weekly Report templates have no metrics defined |
| Landing page has no meta_description | Missing from the copy deck — needed for SEO |

## Walkthrough Steps

```
claude launch_asset_checklist.csv --skill launch-pipeline
```

**Step 1 — Asset inventory and status assessment:**
```
Step 1 Prompt:
Load launch_asset_checklist.csv. Report:

1. Total assets and breakdown by asset_type
2. Count of assets by status (ready / needs_review / not_started)
3. Which assets are blocking the launch (not_started)?
4. Which assets need immediate attention (needs_review)?

Sort by criticality: launch-blocking assets first.
Estimate overall pipeline readiness as a percentage.
```

**Step 2 — Brand compliance and SEO copy audit:**
```
Step 2 Prompt:
Load launch_copy_snippets.md. Run a combined brand compliance
and SEO keyword audit:

BRAND SCAN:
1. Find all passive voice instances
2. Find competitor mentions — classify context (comparative/neutral/quote)
3. Flag excessive punctuation, superlatives without evidence, negative framing
4. Identify missing CTAs or poorly structured CTAs

SEO SCAN (target keywords for Business Edition):
| Keyword | Min. occurrences | Target field |
|---|---|---|
| "cloud sync" | 2 | hero + features |
| "team collaboration" | 2 | hero + features |
| "enterprise security" | 1 | features |
| "cross-platform" | 1 | features |
| "file sharing" | 2 | features + FAQ |
| "cloud storage" | 1 | hero |

For each keyword: count occurrences, flag if below minimum,
suggest insertion points for missing ones.

Combine both scans into a single violations table:
issue_type, section, snippet, severity, recommendation
```

**Step 3 — Draft the email launch sequence:**
```
Step 3 Prompt:
Using the product information from launch_copy_snippets.md, draft
a 3-email launch sequence for Business Edition:

Email 1 — Launch Announcement
  Goal: Announce Business Edition to existing customer base
  Subject: Max 60 chars — exciting but professional
  Content: New tier announcement, key benefits, CTA to learn more

Email 2 — Feature Deep Dive
  Goal: Convert interest into trial signups
  Subject: Max 60 chars — value-focused
  Content: Deep dive on team collaboration, security, cross-platform
  CTA: Start free trial

Email 3 — Trial Expiration Reminder
  Goal: Convert trial users to paid subscribers
  Subject: Max 60 chars — urgency without fear
  Content: Trial ending reminder, social proof, CTA to subscribe

For each email:
- Full template with Subject, Preheader, Body, CTA
- Include {{first_name}} and {{unsubscribe_url}} merge tags
- Brand-compliant tone (no ALL CAPS, no exclamation abuse, no negative framing)
- Exactly one primary CTA per email
```

**Step 4 — Define campaign performance tracking:**
```
Step 4 Prompt:
Design the launch performance tracking framework:

1. Define 5 KPIs to track launch success:
   - One top-line business metric (e.g., trial signups)
   - One engagement metric (e.g., landing page CTR)
   - One email metric (e.g., open rate)
   - One conversion metric (e.g., trial-to-paid rate)
   - One downstream metric (e.g., feature adoption)

2. For each KPI, define:
   - Metric name and definition
   - Target value (what "good" looks like)
   - Warning threshold (needs attention)
   - Data source (where to find the data)
   - Reporting frequency

3. Design a one-page Weekly Launch Report template:
   - Header: Campaign name, week number, date range
   - KPI summary table (metric, target, actual, status, trend)
   - Channel performance snapshot (email, social, landing page)
   - Alert section (any KPI below warning threshold)
   - Action items for next week
```

**Step 5 — Consolidated pipeline output:**
```
Step 5 Prompt:
Write three files:

1. launch_compliance_report.csv — all brand and SEO violations found
   in the launch copy: issue_type, section, snippet, severity, recommendation

2. launch_email_sequence.md — all 3 email templates in sequence format
   with subject, preheader, body, CTA for each step

3. launch_tracking_template.md — the weekly launch report template
   with KPI definitions, targets, and dashboard structure

Then print a terminal summary:

=== MARKETING LAUNCH PIPELINE ===
Product: CloudSync Business Edition
Launch assets: 11
Pipeline readiness: XX% (X of 11 complete)

BRAND & SEO AUDIT:
  Total violations found:  X
    Passive voice:         X
    Competitor mentions:   X
    Tone issues:           X
    Missing keywords:      X
    Formatting issues:     X
  Overall copy readiness:  [pass / needs revision / fail]

EMAIL SEQUENCE:
  Emails drafted:  3 of 3
  Merge tags:      {{first_name}}, {{unsubscribe_url}} — all present
  Brand compliance: [pass / needs revision]
  CTA structure:   [pass / needs revision]

TRACKING FRAMEWORK:
  KPIs defined:    5
  Targets set:     5 of 5
  Report template: [complete / incomplete]

PIPELINE STATUS: LAUNCH READINESS REVIEW COMPLETE
  Assets to finalize:  X
  Copy fixes needed:   X
  Ready for launch:    [yes / conditional / no]
```
