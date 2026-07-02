# Marketing: Brand Compliance & Copy Optimization with Claude Code

**Course Title:** Brand Compliance & Copy Optimization with Claude Code
**Target User:** Christine — Marketing team
**Prerequisites:** Familiarity with brand style guides, basic markdown editing, and web copy workflows; no coding experience required.
**Estimated Duration:** 4 hours (split across two 2-hour sessions)
**Format:** Live walkthrough + hands-on terminal exercises

---

## Pre-Work: Load Your Institutional Memory

Before starting this course, open the [Master Claude Code Guide](https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1) alongside your domain-specific NotebookLM notebook. Query both notebooks to understand how Claude Code operates in your domain before writing any scripts or building tools.

**Your Domain Notebook:** [Christine's Marketing Notebook](https://notebooklm.google.com/notebook/0a616bb3-6ea7-40c8-b53c-984fa4d977bc?authuser=1)

> **Workflow Rule:** All script generation, data testing, or document templating in this track must cross-verify patterns against both the Master Guide and your Domain Notebook before execution.

---

## Learning Objectives

By the end of this course, Christine will be able to:

1. Load raw marketing copy decks, blog drafts, and ad copy into Claude Code for automated review.
2. Enforce brand style guidelines — flag passive voice, off-tone language, and restricted competitor terms.
3. Verify SEO keyword presence and density across multiple copy assets in a single pass.
4. Strip and normalize messy HTML/Markdown formatting tags from imported web copy.
5. Generate compliant A/B copy variants tailored to different channels (email, social, landing page).
6. Build a reusable weekly brand-compliance review prompt template.

---

## Lesson Breakdown

### Lesson 1 — Automated Brand Auditing (60 min)

**Objective:** Use Claude Code to inspect copy decks and flag every deviation from the brand style guide.

| Segment | Topic | Activity |
|---|---|---|
| 1.1 | The brand compliance problem | Brand guides are long PDFs — enforcing them across dozens of assets is impractical manually. Claude Code reads copy and flags violations instantly. |
| 1.2 | Loading a copy deck | Load `data/raw_copy_deck.md` — a messy marketing file with brand violations, passive voice, and mixed formatting. |
| 1.3 | Running the brand-guardrails skill | Invoke Claude Code with the `brand-guardrails` skill to scan the deck for tone, voice, and terminology violations. |
| 1.4 | Understanding the violation report | Review flagged items: passive voice, off-brand adjectives, competitor mentions, missing CTA structure. |
| 1.5 | Fixing violations interactively | Ask Claude to rewrite flagged sentences in brand-compliant tone and explain each change. |

**CLI Exercises:**

```
# Exercise 1.3 — Run brand guardrails on a copy deck
claude data/raw_copy_deck.md --skill brand-guardrails
```

Prompt:

```
Load data/raw_copy_deck.md and run a full brand compliance audit:

1. Scan for passive voice — flag every instance with line number.
2. Scan for competitor brand mentions (e.g., "like Shopify but better"
   or "unlike Mailchimp").
3. Check tone: identify any sentences that sound too formal (legal jargon)
   or too casual (slang, exclamation marks).
4. Check for missing or broken CTA (call-to-action) construction.
5. Identify any markdown formatting inconsistencies (mixed HTML tags,
   broken bold/italic markers).

Output a violation table: violation_type, line, text_snippet, severity (low/medium/high)
```

```
# Exercise 1.5 — Interactive fixes
Prompt (continuing the same session):

Take the high-severity violations and rewrite each one in brand-compliant tone.
For each rewrite, show me:
- Original line
- Issue
- Rewritten line
- Why the rewrite is on-brand
```

---

### Lesson 2 — SEO Keyword Density Verification (60 min)

**Objective:** Automate keyword presence and density checks across marketing copy assets.

| Segment | Topic | Activity |
|---|---|---|
| 2.1 | SEO keyword density basics | Target keywords must appear with minimum frequency in body copy, headings, and meta descriptions. Manual counting across 20+ pages is impractical. |
| 2.2 | Loading copy assets | Load `data/raw_copy_deck.md` alongside a target keyword list. |
| 2.3 | Counting keyword occurrences | Ask Claude to scan the copy and report occurrences per keyword, with context snippets. |
| 2.4 | Density calculation | Instruct Claude to calculate keyword density as a percentage of total word count, and flag any keyword below the minimum threshold. |
| 2.5 | Keyword gap analysis | Identify which target keywords are missing entirely and suggest natural insertion points. |

**CLI Exercises:**

```
# Exercise 2.3 — Keyword occurrence scan
claude data/raw_copy_deck.md
```

Prompt:

```
I have a copy deck loaded. Here is my target keyword list with minimum
required occurrences:

| Keyword | Min. occurrences |
|---|---|
| "cloud sync" | 3 |
| "real-time backup" | 2 |
| "enterprise security" | 2 |
| "cross-platform" | 1 |
| "zero-downtime" | 1 |
| "file versioning" | 1 |

Scan the document and for each keyword tell me:
- How many times it appears
- The surrounding sentence for each occurrence
- Whether it meets the minimum threshold

Flag any keyword that appears zero times as MISSING.
```

```
# Exercise 2.4 — Density check
Prompt (continuing the same session):

Calculate:
- Total word count of the document (body copy only, exclude headings)
- Keyword density % = (occurrences / total word count) * 100 for each keyword

Flag any keyword with density below 0.5% or above 3.0% (keyword stuffing).

Show me: keyword, occurrences, density(%), status (low/ok/stuffed)
```

```
# Exercise 2.5 — Keyword gap insertion
Prompt (continuing the same session):

For each MISSING keyword, identify a paragraph where it could be
naturally inserted. Show me:
- The original paragraph
- The keyword to insert
- The revised paragraph

Do not force keywords where they don't belong — explain why a
paragraph is a good or bad fit.
```

---

### Lesson 3 — HTML & Markdown Sanitization (60 min)

**Objective:** Clean up raw, messy formatting from imported web copy and normalize it to clean markdown.

| Segment | Topic | Activity |
|---|---|---|
| 3.1 | The formatting mess | Web copy exported from CMS tools often contains raw HTML tags (`<span>`, `<div>`, `<font>`), inline styles, and broken markdown. |
| 3.2 | Inspecting the raw copy | Load `data/raw_copy_deck.md` and identify all HTML artifacts mixed into the markdown. |
| 3.3 | Stripping inline styles | Ask Claude to remove inline `style="..."` attributes, `<!-- comments -->`, and empty tags. |
| 3.4 | Normalizing to clean markdown | Convert remaining HTML (`<strong>` → `**bold**`, `<em>` → `*italic*`, `<a>` → `[text](url)`) and fix broken markdown markers. |
| 3.5 | Formatting consistency check | Verify heading levels are sequential, lists are consistently formatted, and no raw HTML remains. |

**CLI Exercises:**

```
# Exercise 3.2 — Identify formatting artifacts
claude data/raw_copy_deck.md
```

Prompt:

```
Scan the document and catalog every formatting issue:

1. List all raw HTML tags present (e.g., <span>, <div>, <font>, <br>)
2. Count how many lines contain inline style="..." attributes
3. Count how many lines contain HTML comments (<!-- ... -->)
4. Identify any broken markdown markers (e.g., **text with no closing,
   *single asterisks, mismatched brackets)
5. Check if heading levels skip (e.g., h1 → h3 with no h2)

Output a table: issue_type, count, example_line
```

```
# Exercise 3.3 — Strip inline styles
Prompt (continuing the same session):

Remove all of the following from the document:
- Inline style="..." attributes from any HTML tags
- HTML comments and their content (<!-- ... -->)
- Empty tags like <span></span>, <div></div>, <strong></strong>
- <br> and <br/> tags (replace with newlines)

Show me a diff of the top 5 most impactful changes.
```

```
# Exercise 3.4 — Normalize to clean markdown
Prompt (continuing the same session):

Convert remaining HTML formatting to markdown equivalents:
- <strong>text</strong> → **text**
- <em>text</em> → *text*
- <a href="URL">text</a> → [text](URL)
- <h2>text</h2> → ## text
- <p>text</p> → text (paragraph break)
- <ul>/<li> → - list items

After conversion, verify no raw HTML tags remain. Output the
cleaned document as clean_copy_deck.md.
```

---

### Lesson 4 — A/B Variant Generation & Weekly Workflow (60 min)

**Objective:** Generate multiple on-brand copy variants for different channels and package everything into a repeatable weekly review.

| Segment | Topic | Activity |
|---|---|---|
| 4.1 | Variant generation constraints | Different channels have different rules: email subject lines (60 char max), meta descriptions (160 char), hero text (short and punchy). Variants must stay on-brand. |
| 4.2 | Single-source variant generation | Take one approved copy block and generate 3 variants each for: email, social (Instagram/Facebook), and landing page hero. |
| 4.3 | Tone tailoring per channel | Email variants should be slightly warmer; social variants shorter and more urgent; landing page variants benefit-driven. |
| 4.4 | A/B test comparison table | Ask Claude to output variants in a structured table with character count, reading level, and brand-compliance score. |
| 4.5 | Building the weekly brand-review prompt | Create a single prompt that loads the copy deck, runs brand audit + SEO check + formatting sanitization, and writes a report. |

**CLI Exercises:**

```
# Exercise 4.2 — Generate channel variants
claude data/raw_copy_deck.md
```

Prompt:

```
I have a hero section in my copy deck. Extract the main headline and
subheading. Then generate 3 variants for each channel:

**Email variants** (subject line max 60 chars, preheader max 130 chars):
   Variant A — warm and benefit-driven
   Variant B — urgent with scarcity
   Variant C — curiosity gap

**Social variants** (max 150 chars, hashtags, punchy):
   Variant A — Instagram (visual-first language)
   Variant B — Facebook (community-oriented)
   Variant C — LinkedIn (professional/thought-leadership)

**Landing page hero variants** (headline max 70 chars, subhead max 150 chars):
   Variant A — problem-agitation-solution
   Variant B — feature-benefit
   Variant C — social-proof

For each variant, include: character count and a brand-compliance
check (flag if any variant violates brand tone).
```

```
# Exercise 4.5 — Full weekly brand-review prompt
claude data/raw_copy_deck.md < weekly_brand_review.md
```

**weekly_brand_review.md** (create this file during the lesson):

```markdown
I have one file loaded: data/raw_copy_deck.md — this week's marketing copy assets.

Please do the following, in order:

## Step 1 — Brand compliance audit
- Scan for passive voice, competitor mentions, off-tone language
- Flag any sentence missing a CTA or with broken formatting
- Output a violations table with severity ratings

## Step 2 — SEO keyword verification
- Target keywords: "cloud sync" (min 3), "real-time backup" (min 2),
  "enterprise security" (min 2), "cross-platform" (min 1),
  "zero-downtime" (min 1)
- Report keyword counts and density percentages
- Flag missing keywords and suggest insertion points

## Step 3 — Formatting sanitization
- Strip all HTML tags, inline styles, and comments
- Normalize to clean markdown
- Verify no raw HTML remains

## Step 4 — Report
- Write a consolidated CSV called weekly_brand_report.csv with:
  1. "violations" — type, line, snippet, severity
  2. "seo_keywords" — keyword, occurrences, density, status
  3. "formatting_issues" — issue_type, count, example
- Print a terminal summary with total violations, SEO status,
  and formatting issues found
```

---

## Sample Data Files

The following sample files are provided in `data/` for use during exercises:

| File | Description |
|---|---|
| `data/raw_copy_deck.md` | Messy marketing copy with brand violations, broken HTML, passive voice, and competitor mentions |
| `data/raw_email_campaign.md` | Flawed promotional email campaign with broken merge vars, aggressive tone, outdated pricing, and raw HTML styling |
| `data/keyword_targets.csv` | Target keyword list with minimum occurrence thresholds |

---

## Link Directory

| Resource | Path / Location |
|---|---|
| Course slide deck | `training/christine/` |
| Sample data assets | `training/christine/data/` |
| Marketing lab exercises | `training/christine/exercises/marketing-labs.md` |
| Mock raw copy deck | `training/christine/data/raw_copy_deck.md` |
| Mock email campaign | `training/christine/data/raw_email_campaign.md` |
| brand-guardrails skill | `skills/brand-guardrails/SKILL.md` |
| csv-analytics skill | `../mollie/skills/csv-analytics/SKILL.md` |
| data-table-validator skill | `../sunny/skills/data-table-validator/SKILL.md` |

---

## Success Criteria

Christine can independently:

- [ ] Load a copy deck and run a full brand compliance audit using the brand-guardrails skill
- [ ] Scan copy for SEO keyword presence and density against a target list
- [ ] Strip HTML formatting artifacts and normalize to clean markdown
- [ ] Generate channel-specific A/B copy variants that stay on-brand
- [ ] Export a structured CSV of all violations and SEO gaps
- [ ] Run the weekly brand-review pipeline using the saved prompt template
