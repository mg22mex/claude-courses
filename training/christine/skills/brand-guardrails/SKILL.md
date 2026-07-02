---
name: brand-guardrails
description: Inspect raw marketing copy, flag brand style violations (passive voice, off-tone language, competitor terms), verify SEO keyword density, sanitize HTML/Markdown formatting, and output compliant copy variants.
---

# brand-guardrails

A strict operational playbook for enforcing brand identity guidelines across marketing copy decks, blog drafts, ad copy, and landing page content. This skill handles tone and voice policing, competitor term detection, SEO keyword verification, HTML/Markdown sanitization, and constrained A/B variant generation. Run this whenever Christine needs to audit copy for brand compliance, optimize for SEO keywords, clean up imported web formatting, or generate on-brand copy variants.

---

## 1. Intake & Content Classification

### 1.1 Accept input formats

This skill accepts **one or more** input files:

- **`.md`** — Markdown copy decks, blog drafts, email templates
- **`.csv`** — Ad copy spreadsheets with headline/body/CTA columns
- **`.txt`** — Plain text web copy exports
- **`.html`** — Raw HTML snippets (stripped before analysis)

If no files are provided, prompt Christine to supply a copy deck.

### 1.2 Classify content type

Inspect the file and classify it into one of the following content categories:

| Column heuristic | Content type |
|---|---|
| Contains `subject_line`, `preheader`, `body`, `cta` | Email campaign |
| Contains `headline`, `subhead`, `hero`, `body_copy` | Landing page |
| Contains `caption`, `hashtags`, `post_text` | Social media asset |
| No structured columns, continuous prose | Blog or editorial copy |

If the content type is ambiguous, output a warning and ask Christine to confirm.

---

## 2. Brand Compliance Scan

### 2.1 Passive voice detection

Scan every sentence and flag passive voice constructions. Use the following heuristics:

| Pattern | Flag |
|---|---|
| `is/was/were/been/being + past participle` (e.g., "was created", "is designed") | Passive voice |
| `has been/have been/had been + past participle` | Passive voice |
| `get/got/gotten + past participle` | Passive voice (informal) |

Collect all passive-voice sentences into the violation table.

### 2.2 Competitor term detection

Flag any mention of known competitor brands. Maintain a blocklist:

- `Shopify` (unless quoting a migration story)
- `Mailchimp`, `Klaviyo`, `HubSpot`
- `Salesforce`, `Oracle`, `Adobe`
- `competitor`, `rival platform` (vague references)

If a competitor mention appears inside a code block or a direct quotation, demote severity to `low`. Otherwise flag as `high`.

### 2.3 Tone and voice check

Evaluate every sentence against brand tone rules. Flag deviations:

| Violation | Example | Severity |
|---|---|---|
| Too formal (legal jargon) | "The aforementioned solution shall enable..." | medium |
| Too casual (slang, excessive exclamation marks) | "This is literally the best thing ever!!!" | medium |
| Negative/comparative language about competitors | "Unlike X, we actually work" | high |
| Superlatives without evidence | "The best platform on the market" | medium |
| Off-brand adjectives | Using descriptors outside the approved brand lexicon | medium |

### 2.4 CTA structure validation

Ensure every copy block contains a properly structured call-to-action:

- CTA must contain an **action verb** (Get, Try, Start, Download, Sign up)
- CTA must be **2–5 words** (not "Click here" or long-winded CTAs)
- CTA must not be a **full sentence** (not "You should click this button to learn more")
- CTA must not use **negative framing** (not "Stop losing money")

Flag missing CTAs and malformed CTAs separately.

---

## 3. SEO Keyword Density Verification

### 3.1 Keyword occurrence counting

Accept a target keyword list (inline in the prompt or as a separate file). For each keyword:

1. Count case-insensitive occurrences in the body copy (exclude headings, alt text, URLs).
2. Record the surrounding sentence for each occurrence.
3. Flag any keyword with **zero occurrences** as MISSING.

### 3.2 Density calculation

For each keyword, calculate:

```
density_pct = (occurrences / total_word_count) * 100
```

Apply thresholds:

| Density | Status |
|---|---|
| < 0.3% | low (under-optimized) |
| 0.3% – 3.0% | ok (healthy range) |
| > 3.0% | stuffed (keyword stuffing risk) |

### 3.3 Insertion suggestion

For MISSING keywords, scan the document for paragraphs where the keyword could be naturally inserted. Rank suggestions by contextual fit (high/medium/low) and explain the reasoning.

---

## 4. HTML & Markdown Sanitization

### 4.1 Identify formatting artifacts

Catalog all formatting issues found in the document:

- Raw HTML tags (`<span>`, `<div>`, `<font>`, `<p>`, `<br>`, `<style>`)
- Inline `style="..."` attributes
- HTML comments (`<!-- ... -->`)
- Broken markdown markers (`**text` with no closing, `*single asterisks`)
- Heading level skips (e.g., `#` → `###` with no `##`)

### 4.2 Strip inline cruft

Remove, in order:

1. HTML comments and their content (`<!-- ... -->`)
2. Inline `style` attributes (but keep the tag)
3. Empty tags with no content (`<span></span>`, `<strong></strong>`)
4. `<br>` and `<br/>` — replace with a newline
5. `<div>`, `</div>` — replace with a newline

### 4.3 Normalize to markdown

Convert remaining HTML to markdown equivalents:

| Raw HTML | Markdown |
|---|---|
| `<strong>text</strong>` | `**text**` |
| `<em>text</em>` | `*text*` |
| `<a href="URL">text</a>` | `[text](URL)` |
| `<h1>text</h1>` through `<h6>text</h6>` | `# text` through `###### text` |
| `<p>text</p>` | `text` followed by paragraph break |
| `<ul><li>item</li></ul>` | `- item` |
| `<ol><li>item</li></ol>` | `1. item` |

After conversion, verify **zero raw HTML tags remain**. If any remain, list them as errors.

---

## 5. Variant Generation & Format Enforcement

### 5.1 Extract source content

When Christine asks for A/B variants, extract the source copy block (headline, subhead, body, or CTA). Confirm the source before generating.

### 5.2 Channel constraints

Generate variants according to channel-specific rules:

| Channel | Constraints |
|---|---|
| Email subject | Max 60 characters |
| Email preheader | Max 130 characters |
| Social (Instagram) | Max 150 characters, visual-first language |
| Social (Facebook) | Max 150 characters, community-oriented tone |
| Social (LinkedIn) | Max 150 characters, professional/thought-leadership tone |
| Landing page headline | Max 70 characters |
| Landing page subhead | Max 150 characters |
| Meta description | Max 160 characters |

### 5.3 Tone variants per channel

For each channel, generate exactly 3 variants following these tone patterns:

1. **Warm/benefit-driven** — focuses on what the customer gains, uses inclusive language
2. **Urgent/scarcity** — creates timely action with limited availability framing
3. **Curiosity/social-proof** — leverages questions, statistics, or customer validation

### 5.4 Brand-compliance check per variant

For every generated variant, verify:

- No passive voice
- No competitor terms
- No superlative without evidence
- CTA is properly structured (2–5 words, action verb)
- Character count is within threshold

If a variant fails, do NOT output it — regenerate with a note about what was fixed.

---

## 6. Output & Reporting

### 6.1 Terminal violation table

Print findings in a formatted terminal table:

```
=== BRAND COMPLIANCE REPORT ===
File: raw_copy_deck.md
Total violations found: 14

 Violation Type        | Line | Severity | Snippet
───────────────────────|──────|──────────|──────────────────────────
 Passive voice         |   12 | medium   | "was created by our team"
 Competitor mention    |   24 | high     | "unlike Shopify..."
 Missing CTA           |   42 | high     | (no CTA in section)
 Tone (too casual)     |   31 | low      | "This is amazing!!!"
───────────────────────┴──────┴──────────┴──────────────────────────
```

### 6.2 CSV report export

If Christine requests a report file, write `brand_audit_report.csv` with columns:

```
violation_type,line,text_snippet,severity,recommendation
```

### 6.3 Clean copy export

When sanitization is performed, write the cleaned document as `clean_copy_deck.md`. Include a header comment noting the original file name and date of cleaning.

---

## 7. Strictness Rules

1. **Never modify the original file.** All edits, rewrites, and variants are written to new output files or shown as diffs.
2. **Always show diffs.** When stripping formatting or rewriting copy, show a before/after diff for every change.
3. **Do not guess the brand voice.** If the brand style guide isn't loaded, ask Christine for the brand tone parameters before flagging tone violations.
4. **Context matters for competitor terms.** A competitor name in a code block, quoted customer testimonial, or migration guide context is `low` severity, not `high`.
5. **Character counts are non-negotiable.** Variants that exceed channel limits are rejected and regenerated — never truncated.
6. **SEO insertion must read naturally.** If no natural insertion point exists for a keyword, report "no suitable insertion found" rather than forcing an awkward placement.

---

## 8. Edge Cases

| Situation | Response |
|---|---|
| File contains only HTML with no markdown | Strip all HTML tags, convert to markdown, then run the compliance scan on the result |
| Keyword list is not provided | Ask Christine for the target keywords and minimum thresholds before proceeding |
| Copy deck is empty or all HTML comments | Abort with "ERROR: No copy content found in the provided file" |
| Variant character limit cannot be met | Suggest shortening the source copy first, then regenerate variants |
| Mixed-language copy (e.g., English + Spanish) | Run compliance on each language segment separately; SEO keyword matching is case-insensitive but language-aware |
| CTA is present but uses negative framing ("Stop overpaying") | Flag as medium severity and suggest a positive reframe ("Start saving") |
| Competitor name in URL slug | Flag as low severity — URLs are often auto-generated and may not be editable |
| Document has no headings | Flag as formatting issue: "No headings found — copy lacks structural hierarchy" |
| Generated variant accidentally duplicates an existing variant | Skip duplicate and regenerate a new variant with a different tone approach |
| File encoding is not UTF-8 | Attempt to detect encoding and convert; if detection fails, abort with encoding error |
