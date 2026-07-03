# Exercise 1 — Brand Compliance & Voice Enforcement

## Scenario

Christine has received a raw copy deck from a freelance copywriter (`raw_copy_deck.md`). The copy contains brand style violations, passive voice, competitor mentions, and mixed HTML/Markdown formatting. Christine needs to audit the deck against core brand parameters, flag every violation, and produce a structured report.

## Learning Objectives

- Load and inspect a raw marketing copy deck for brand compliance
- Detect passive voice, competitor mentions, off-tone language, and formatting issues
- Classify violations by severity (high/medium/low)
- Generate a structured audit report with rewrite recommendations
- Export findings to a reusable CSV format

## Dataset

| File | Description |
|---|---|
| `../data/raw_copy_deck.md` | Marketing copy deck with planted brand violations, broken HTML, passive voice, off-tone language, and competitor references |

### Known Issues Planted in the Data

| Issue | Detail |
|---|---|
| Passive voice sentences | "was created by", "is trusted by", "has been built", "was recommended" — multiple instances |
| Competitor name drops | References to Shopify, Mailchimp, Dropbox in comparative context |
| Off-brand tone | Excessive exclamation marks ("amazing!!!", "forever!!"), superlatives without evidence ("the best solution") |
| Mixed HTML/markdown | Inline `<span style="...">`, `<div class="...">`, HTML comments, broken tags |
| Missing CTAs | FAQ section and pricing table have no call-to-action |
| Legal jargon in body copy | "subject to change without notice", "may be withdrawn at any time" — too formal for brand voice |

## Walkthrough Steps

```
claude ../data/raw_copy_deck.md --skill brand-guardrails
```

**Step 1 — Initial brand scan:**
```
Step 1 Prompt:
Load ../data/raw_copy_deck.md. Perform a brand compliance scan and report:

1. How many instances of passive voice can you find? List each one
   with its line number and the full sentence.
2. Are there any competitor brand names mentioned? List each with
   line number and surrounding context.
3. Flag any sentences that use excessive punctuation (!!!),
   superlatives without evidence, or slang.
4. Identify any sections that lack a call-to-action.

Organize findings in a table: issue_type, line, snippet, severity
```

**Step 2 — Competitor context analysis:**
```
Step 2 Prompt:
For each competitor mention you found, classify the context:
- Comparative ("unlike X...") → high severity
- Customer quote mentioning previous vendor → medium severity
- General reference with no comparison → low severity

Explain why context matters for competitor mentions and which
ones need immediate rewriting.
```

**Step 3 — Tone and voice report:**
```
Step 3 Prompt:
Analyze the overall tone of the document:

1. Identify 3 sentences that sound too formal for the brand
   (legal or corporate jargon).
2. Identify 3 sentences that sound too casual or salesy.
3. Rate the document overall: consistent / mostly consistent /
   inconsistent with brand voice.

For each flagged sentence, suggest a brand-compliant rewrite.
```

**Step 4 — Generate the audit report:**
```
Step 4 Prompt:
Write a CSV called brand_audit_violations.csv with all violations found.
Columns: violation_type, line, text_snippet, severity, recommendation.

Include at least these violation types in the CSV:
- passive_voice
- competitor_mention
- off_tone
- missing_cta
- formatting_issue
- superlative_no_evidence

Print a terminal summary:

=== BRAND AUDIT SUMMARY ===
File: raw_copy_deck.md
Total violations:      XX
  Passive voice:       X
  Competitor mentions: X
  Tone issues:         X
  Missing CTAs:        X
  Formatting issues:   X
  Superlatives:        X

High severity:         X
Medium severity:       X
Low severity:          X

Document rating:       [consistent / mostly consistent / inconsistent]
```
