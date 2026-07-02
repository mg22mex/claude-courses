# Marketing Labs — Advanced Brand & Copy Exercises

Three production-grade exercises for Christine to sharpen her brand compliance, SEO optimization, and copy variant generation skills.

---

## Exercise 1: Automated Brand Auditing

### Scenario

Christine has received a raw copy deck from a freelance copywriter (`raw_copy_deck.md`). The copy contains brand style violations, passive voice, competitor mentions, and mixed HTML/Markdown formatting. Christine needs to audit the deck, flag every violation, and produce a structured report for the copywriter's revision round.

### Dataset

| File | Description |
|---|---|
| `raw_copy_deck.md` | Marketing copy deck with planted brand violations, broken HTML, passive voice, off-tone language, and competitor references |

### Data Challenges Planted

| Challenge | Detail |
|---|---|
| Passive voice sentences | "was created by", "is trusted by", "has been built", "was recommended" — multiple instances |
| Competitor name drops | References to Shopify, Mailchimp, Dropbox in comparative context |
| Off-brand tone | Excessive exclamation marks ("amazing!!!", "forever!!"), superlatives without evidence ("the best solution") |
| Mixed HTML/markdown | Inline `<span style="...">`, `<div class="...">`, HTML comments, broken tags |
| Missing CTAs | FAQ section and pricing table have no call-to-action |
| Legal jargon in body copy | "subject to change without notice", "may be withdrawn at any time" — too formal for brand voice |

### Walkthrough Steps

```
claude raw_copy_deck.md --skill brand-guardrails
```

Alternatively, load without the skill and audit manually:

```
claude raw_copy_deck.md
```

**Step 1 — Initial brand scan:**

```
Step 1 Prompt:
Load raw_copy_deck.md. Perform a brand compliance scan and report:

1. How many instances of passive voice can you find? List each one
   with its line number and the full sentence.
2. Are there any competitor brand names mentioned? List each with
   line number surrounding context.
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

**Step 4 — Generate the audit CSV:**

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

---

## Exercise 2: SEO Content Optimizer

### Scenario

Christine needs to optimize the `raw_copy_deck.md` for search engines. The marketing director has provided a target keyword list with minimum occurrence thresholds. Christine must scan the document, report keyword density, flag missing terms, and suggest natural insertion points — all without making the copy read like keyword-stuffed garbage.

### Dataset

| File | Description |
|---|---|
| `raw_copy_deck.md` | Same copy deck from Exercise 1 (after or before brand audit — Christine's choice) |

Target keyword list (use inline in your prompt):

```csv
keyword,min_occurrences
"cloud sync",3
"real-time backup",2
"enterprise security",2
"cross-platform",1
"zero-downtime",1
"file versioning",1
```

### Walkthrough Steps

```
claude raw_copy_deck.md
```

**Step 1 — Keyword occurrence inventory:**

```
Step 1 Prompt:
I have a target keyword list:

| Keyword | Min. occurrences |
|---|---|
| "cloud sync" | 3 |
| "real-time backup" | 2 |
| "enterprise security" | 2 |
| "cross-platform" | 1 |
| "zero-downtime" | 1 |
| "file versioning" | 1 |

Scan raw_copy_deck.md and for each keyword:
1. Count case-insensitive occurrences in body copy (exclude headings)
2. Show the surrounding sentence for each match
3. Flag if below minimum threshold
4. Note any keyword that appears zero times as MISSING

Output: keyword, occurrences, threshold, status (met/missing/below)
```

**Step 2 — Density calculation:**

```
Step 2 Prompt:
Calculate the total word count of the body copy (skip headings, tables,
and blockquotes). For each keyword, compute:

  density_pct = (occurrences / total_word_count) * 100

Flag any keyword where density < 0.3% (under-optimized) or > 3.0%
(risk of keyword stuffing).

Show me: keyword, occurrences, density(%), status (low/ok/stuffed)
```

**Step 3 — Missing keyword insertion:**

```
Step 3 Prompt:
For every keyword flagged as MISSING or low, identify the best paragraph
in the document where it could be naturally inserted.

For each suggestion, show:
- Original paragraph text
- Target keyword
- Revised paragraph with keyword inserted
- Fit rating (natural / acceptable / awkward)

If no suitable insertion point exists, say so honestly — do not force it.
```

**Step 4 — SEO gap report:**

```
Step 4 Prompt:
Write a CSV called seo_keyword_report.csv with columns:
keyword, occurrences, min_required, density_pct, status, suggested_insertion_point

Also print a terminal summary:

=== SEO KEYWORD OPTIMIZATION REPORT ===
Total word count:        XXX
Keywords meeting target: X of 6
Keywords below target:   X
Keywords missing:        X

Keyword stuffing risks:  X
Natural insertions:      X
Awkward insertions:      X (needs copywriter review)

Overall SEO readiness:   [strong / needs work / poor]
```

---

## Exercise 3: A/B Variant Generation Scripting

### Scenario

Christine has a hero section from `raw_copy_deck.md` that needs to be adapted for three different channels: email (welcome campaign), Instagram (awareness ad), and the landing page. Each channel has strict character limits and tone requirements. Christine needs to generate 3 variants per channel — 9 variants total — each staying within brand guidelines and character limits.

### Dataset

| File | Description |
|---|---|
| `raw_copy_deck.md` | Source copy deck (use the hero/headline section) |

### Walkthrough Steps

```
claude raw_copy_deck.md
```

**Step 1 — Extract the hero section:**

```
Step 1 Prompt:
Find the hero section at the top of raw_copy_deck.md. Extract:

1. The main headline (the H1 or largest heading text)
2. The subheading or supporting sentence directly below it
3. The current CTA text and its link

Show me what you found and confirm before generating variants.
```

**Step 2 — Generate email variants:**

```
Step 2 Prompt:
Using the hero headline and subheading as source material, generate
3 email subject line + preheader variants.

Rules:
- Subject line: max 60 characters
- Preheader: max 130 characters
- Must include a CTA action verb

Variant A — Warm/benefit-driven
Variant B — Urgency/scarcity
Variant C — Curiosity/social-proof

Format as a table:
Variant | Subject (chars) | Preheader (chars) | Brand-compliant?
```

**Step 3 — Generate social variants:**

```
Step 3 Prompt:
Using the same source content, generate 3 social media variants.

Rules:
- Max 150 characters per post
- Include 2-3 relevant hashtags

Variant A — Instagram (visual-first, aspirational language)
Variant B — Facebook (community-oriented, conversational)
Variant C — LinkedIn (professional, thought-leadership tone)

For each variant, include:
- Full post text
- Character count
- Hashtags used
- Brand-compliance check pass/fail
```

**Step 4 — Generate landing page hero variants:**

```
Step 4 Prompt:
Generate 3 landing page hero variants (headline + subhead).

Rules:
- Headline: max 70 characters
- Subhead: max 150 characters
- CTA: 2-5 words, action verb, no negative framing

Variant A — Problem-agitation-solution
Variant B — Feature-benefit
Variant C — Social proof / statistical proof

Format:
--- Variant A ---
Headline: [text] (XX chars)
Subhead:  [text] (XX chars)
CTA:      [text]
--- Variant B ---
...
```

**Step 5 — A/B test comparison matrix:**

```
Step 5 Prompt:
Combine all 9 variants into a single comparison table:

Channel | Variant | Headline/Text | Char count | Tone | Brand OK?
--------|---------|--------------|------------|------|----------
Email   | A       | ...          | 58/60      | warm | yes
Email   | B       | ...          | 55/60      | urgent | yes
...     | ...     | ...          | ...        | ...  | ...

Then answer:
1. Which variant per channel do you recommend and why?
2. Are there any variants that are too similar to each other?
3. Which channel had the hardest constraint to work within?
```

**Step 6 — Final variant export:**

```
Step 6 Prompt:
Write the recommended variant for each channel to a file called
recommended_variants.md with this format:

```markdown
# Recommended A/B Variants
Generated: [date]
Source: raw_copy_deck.md

---

## Email — Recommended: Variant [X]
**Subject:** [text]
**Preheader:** [text]
**Why this won:** [reason]

---

## Social — Recommended: Variant [X]
**Platform:** [channel]
**Post:** [text]
**Why this won:** [reason]

---

## Landing Page — Recommended: Variant [X]
**Headline:** [text]
**Subhead:** [text]
**CTA:** [text]
**Why this won:** [reason]
```

Print a confirmation message when the file is written.
```

---

## Data File Reference

| File | Exercise | Description |
|---|---|---|
| `raw_copy_deck.md` | 1, 2, 3 | Mock marketing copy with brand violations, broken HTML, passive voice, and competitor mentions |

### Cross-Reference: Syllabus & Skills

| Resource | Purpose | Path |
|---|---|---|
| Marketing Syllabus | Full course outline for Christine | `../syllabus.md` |
| brand-guardrails skill | Automated brand compliance + variant generation | `../skills/brand-guardrails/SKILL.md` |
| csv-analytics skill | Data join and profitability analysis (adjacent skill) | `../../mollie/skills/csv-analytics/SKILL.md` |
| data-table-validator skill | Pricing and data integrity checks (adjacent skill) | `../../sunny/skills/data-table-validator/SKILL.md` |
