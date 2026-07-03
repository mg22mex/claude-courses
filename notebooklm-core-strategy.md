# NotebookLM Core Strategy — Dual-Engine Operational Framework

## The Dual-Engine Equation

```
Master Technical Blueprint Notebook
  + Individual Operational Domain Notebook
  → Claude Code Local Workspace Automation
```

Every training track in this repository operates on a two-notebook model:

1. **Master Engine** — The global Claude Code technical reference (shared across all tracks)
2. **Domain Engine** — The role-specific operational knowledge base (unique per track)

Trainees must consult **both** notebooks before writing scripts, building tools, or generating templates. The Master Engine provides Claude Code mechanics; the Domain Engine provides business context, edge cases, and domain-specific patterns.

---

## Global Reference Link (Master Engine)

**Master Claude Code Guide**
<https://notebooklm.google.com/notebook/4bdb17a3-6657-4d63-adbe-8f63c22521c2?authuser=1>

This notebook covers Claude Code CLI fundamentals, prompt engineering patterns, skill architecture, file I/O conventions, and cross-track integration patterns. Every trainee must be familiar with this reference before proceeding to domain-specific work.

---

## Domain Matrix Binding

Each operational role is bound to a dedicated NotebookLM instance that encodes that domain's processes, data schemas, known edge cases, and automation patterns.

| Track | Role | Domain Notebook URL |
|---|---|---|
| **Rick** | Executive, Entrepreneurship & Management | <https://notebooklm.google.com/notebook/8644375a-5c5f-442d-b35b-fb849e3f93b2?authuser=1> |
| **Sunny** | Purchasing & Logistics | <https://notebooklm.google.com/notebook/c3dc698d-38e7-4d64-8451-0bbca3fa9d97?authuser=1> |
| **Mollie** | Sales & Financials | <https://notebooklm.google.com/notebook/2ab95bfd-ceeb-436d-b41f-85a89e3ca749?authuser=1> |
| **Christine** | Marketing | <https://notebooklm.google.com/notebook/0a616bb3-6ea7-40c8-b53c-984fa4d977bc?authuser=1> |
| **Design** (Paula & Gaby) | Design | <https://notebooklm.google.com/notebook/9f67d0db-49c8-4bc3-b2e5-f08a3528028f?authuser=1> |

---

## Workflow Rules

### Rule 1: Dual Query Before Code

Before generating any script, building any skill, or creating any document template:

1. Query the **Master Claude Code Guide** for technical patterns and CLI conventions.
2. Query the **Domain Notebook** for business rules, data schemas, and known edge cases.
3. Cross-verify the approach against both sources before writing code.

### Rule 2: URL Permanence

The six NotebookLM URLs in this document are permanent references. Do not modify, replace, or regenerate them. Any update to these URLs must be approved at the repository-administrator level and propagated to all syllabi, README, and CLAUDE.md simultaneously.

### Rule 3: Syllabus Binding

Every syllabus must include a dedicated introductory step directing the learner to open their Domain Notebook alongside the Master Guide before proceeding with exercises. This step appears immediately after the course metadata block and before Learning Objectives.

### Rule 4: Cross-Verification in CI

All script generation, data testing, or document templating in this repository must cross-verify patterns against the NotebookLM URLs assigned to that role path. This includes exercise solutions, skill definitions, and sample data processing.

---

## Dependency Graph

```
Master Claude Code Guide
  ├── Rick's Executive Notebook
  ├── Sunny's Purchasing Notebook
  ├── Mollie's Sales Notebook
  ├── Christine's Marketing Notebook
  └── Design Notebook
       └── All → Claude Code Local Workspace
```

The Master Guide is a single source of truth for Claude Code mechanics. Each Domain Notebook is a single source of truth for its operational domain. Neither replaces the other — they are dual engines that must fire together.
