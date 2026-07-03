# CLAUDE.md — Claude Courses Project Memory

## Project Overview
This repository (`claude-courses`) hosts tailored training course content, syllabi, and localized automation custom skills designed to onboard different operational teams (Supply Chain/Logistics, Sales, Marketing, Design, Executive) to Claude Code.

## Dual-Engine Framework

This repository operates on a two-notebook model that binds every training track to a Domain Notebook plus the shared Master Guide:

```
Master Technical Blueprint Notebook
  + Individual Operational Domain Notebook
  → Claude Code Local Workspace Automation
```

### Workflow Rules

**Rule 1: Dual Query Before Code** — Before generating any script, building any skill, or creating any document template, query the Master Claude Code Guide for technical patterns AND the Domain Notebook for business rules, data schemas, and known edge cases. Cross-verify the approach against both before writing code.

**Rule 2: Syllabus Binding** — Every syllabus must include a "Pre-Work: Load Your Institutional Memory" section after the course metadata block and before Learning Objectives, directing learners to open their Domain Notebook alongside the Master Guide.

**Rule 3: Cross-Verification** — All script generation, data testing, and document templating must cross-verify patterns against the track's assigned NotebookLM URL before execution.

**Rule 4: URL Permanence** — The six NotebookLM URLs in `notebooklm-core-strategy.md` are permanent references. Do not modify, replace, or regenerate them. Any update must be approved at the repository-administrator level and propagated to all syllabi, README, and CLAUDE.md simultaneously.

## Directory Structure
- `training/rick/` — Executive, Entrepreneurship & Management course (Rick). Contains `syllabus.md`, `data/`, `exercises/`, `skills/`.
- `training/sunny/` — Purchasing & Logistics course (Sunny). Contains `syllabus.md`, `data/`, `exercises/`, `skills/`.
- `training/mollie/` — Sales & Financials course (Mollie). Contains `syllabus.md`, `data/`, `exercises/`, `skills/`.
- `training/christine/` — Marketing course (Christine). Contains `syllabus.md`, `data/`, `exercises/`, `skills/`.
- `training/design/` — Design course (Paula & Gaby). Contains `syllabus.md`, `data/mock-assets/`, `exercises/`, `skills/`.

## Quality Gates

Every exercise across all tracks must satisfy these structural checks:

| Gate | Requirement |
|---|---|
| **Scenario** | A realistic business context narrative grounded in the track's domain |
| **Learning Objectives** | 4-6 measurable outcomes the learner achieves by completing the exercise |
| **Dataset** | Inline sample data or a path to a file in the track's `data/` subdirectory |
| **Known Issues** | A table of deliberate problems planted in the data that the learner must discover |
| **Walkthrough** | Step-by-step numbered instructions with CLI commands and prompt examples |
| **Expected Output** | Clear definition of what files and reports the learner produces |

Syllabi must additionally outline: course title, target department user, modular lesson breakdowns, practical terminal/CLI exercises, and a link directory pointing to relevant local skills.

## Conventions & Formatting Standards

### Filenames & Assets
- **Filenames**: Strict lower-case kebab-case for ALL files and directories. Underscores and uppercase are not allowed. Standard conventions (`SKILL.md`, `README.md`) are exempt.
- **Numbered exercises**: Use `exercise-1.md` format (hyphen, not underscore).
- **Assets**: Place all data files in the track's `data/` subdirectory (e.g., `training/mollie/data/`). No data files may live outside `data/`.

### NotebookLM Cross-Verification
- The master reference is `notebooklm-core-strategy.md`, which defines the Dual-Engine framework binding the Master Claude Code Guide to each Domain Notebook.
- The system profile is `notebooklm-system-prompt.md`, which defines the Master Architectural Engine's authority, boundaries, and output patterns.
