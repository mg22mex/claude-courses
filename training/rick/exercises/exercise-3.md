# Exercise 3 — Rigid Product Requirement Drafting

## Scenario

Your executive team has a list of high-level business ideas that need to be translated into structured Product Requirements Documents (PRDs). Each idea is a single sentence — your job is to decompose it into a formal PRD with problem statement, success metrics, milestones, functional requirements, and risk assessment using the `write-a-prd` skill.

## Learning Objectives

- Load raw business concepts into Claude Code
- Use the `write-a-prd` skill to generate structured PRDs
- Define success metrics and KPIs for each initiative
- Map milestones with go/no-go decision gates
- Assess risks and document mitigations
- Generate multiple PRDs in batch

## Dataset

Use the inline sample ideas below.

### Sample Business Ideas (`ideas.txt`)

```
Build an AI-powered chatbot that answers customer order status questions in real-time using our order database.
Create a vendor portal where suppliers can upload invoices, track payment status, and update lead times.
Add a predictive inventory reordering engine that forecasts demand using historical sales and seasonality.
Launch a mobile app for warehouse pickers with barcode scanning, voice navigation, and real-time task assignment.
```

### Known Issues Planted in the Data

| Issue | Location | Notes |
|---|---|---|
| Vague scope | All 4 ideas | Single-sentence concepts need decomposition |
| Missing constraints | Ideas 1, 3 | No mention of data sources or integration requirements |
| No user segmentation | Ideas 2, 4 | Different user roles not identified |
| No success criteria | All 4 ideas | No metrics defined for what "done" looks like |

## Walkthrough

### Step 1 — Review the write-a-prd skill

Start Claude Code and open the skill definition:

```bash
claude skills/write-a-prd/SKILL.md
```

Prompt:

```
Read skills/write-a-prd/SKILL.md and summarize:
- What inputs does the PRD skill expect?
- What sections will it generate?
- What rules and constraints does it enforce?
```

### Step 2 — Load and inspect the business ideas

```bash
claude
```

Paste the following:

```
I have a list of 4 business ideas. Here they are:

1. Build an AI-powered chatbot that answers customer order status questions
   in real-time using our order database.
2. Create a vendor portal where suppliers can upload invoices, track payment
   status, and update lead times.
3. Add a predictive inventory reordering engine that forecasts demand using
   historical sales and seasonality.
4. Launch a mobile app for warehouse pickers with barcode scanning, voice
   navigation, and real-time task assignment.

For each idea, tell me:
- Who are the primary users?
- What problem does it solve?
- What would success look like in measurable terms?
```

### Step 3 — Generate a PRD for one idea using the skill

```
Run the write-a-prd skill. Here is the concept:

Title: AI Customer Order Status Chatbot
Concept: Build an AI-powered chatbot that answers customer order status
queries in real-time by connecting to our order database. Customers can
ask "Where is my order?" and get instant tracking updates without calling
support.

Additional context:
- Target users: B2B customers, customer support team
- Existing systems: Order management system (OMS), warehouse management
  system (WMS), Shopify storefront
- Constraints: Must integrate with existing Slack-based support workflow
- Timeline: MVP desired within 3 months

Generate a complete PRD with milestones, KPIs, and risk register.
```

### Step 4 — Generate PRDs for the remaining ideas

Repeat the skill invocation for the remaining three ideas. For each one, provide reasonable context about target users, existing systems, and constraints.

After generating all four PRDs, prompt:

```
Review all four generated PRDs and compare them:
- Which has the clearest problem statement?
- Which has the highest risk score?
- Which has the shortest time-to-MVP?
- Are there any common dependencies across multiple PRDs?

Create a portfolio summary table with: idea name, estimated MVP timeline,
top risk, primary success metric.
```

### Step 5 — Export the PRD portfolio

```
Write a portfolio overview to prd_portfolio_summary.md containing:
1. A cover page with the date and portfolio scope
2. A summary table comparing all 4 PRDs
3. Recommendations for prioritization (which to fund first, which to defer)
4. A risk heatmap showing which ideas carry the most execution risk

Save each generated PRD as prd_idea_01.md through prd_idea_04.md
in a generated_prds/ directory.
```

## Expected Output

After completing all steps, you should have:

- 4 structured PRD documents covering all sections of the `write-a-prd` template
- A `prd_portfolio_summary.md` comparing all initiatives
- A prioritization recommendation based on timeline, risk, and impact
- Practical experience with the `write-a-prd` executive skill
