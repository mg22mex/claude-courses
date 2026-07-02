# CLAUDE.md — Claude Courses Project Memory

## Project Overview
This repository (`claude-courses`) hosts tailored training course content, syllabi, and localized automation custom skills designed to onboard different operational teams (Supply Chain/Logistics, Sales, Marketing, Design, Executive) to Claude Code.

## Directory Structure
- `training/rick/` — Executive, Entrepreneurship & Management course (Rick). Contains `syllabus.md`, `data/`, `exercises/`, `skills/`.
- `training/sunny/` — Purchasing & Logistics course (Sunny). Contains `syllabus.md`, `data/`, `exercises/`, `skills/`.
- `training/mollie/` — Sales & Financials course (Mollie). Contains `syllabus.md`, `data/`, `exercises/`, `skills/`.
- `training/christine/` — Marketing course (Christine). Contains `syllabus.md`, `data/`, `exercises/`, `skills/`.
- `training/design/` — Design course (Paula & Gaby). Contains `syllabus.md`, `data/mock_assets/`, `exercises/`, `skills/`.

## Conventions & Formatting Standards

### Filenames & Assets
- **Filenames**: Use kebab-case for all files and directories (e.g., `supply-chain-syllabus.md`).
- **Assets**: Place data files in the person's `data/` directory (e.g., `training/mollie/data/`).

### Syllabi Requirements
- Write in clean Markdown.
- Every syllabus must explicitly outline: Course title, target department user, clear learning objectives, modular lesson breakdowns, practical terminal/CLI exercises, and a link directory pointing to relevant local skills.

### NotebookLM Cross-Verification
- All script generation, data testing, or document templating must cross-verify patterns against the track's assigned NotebookLM URLs before execution.
- The master reference is `training/NOTEBOOKLM_CORE_STRATEGY.md`, which defines the Dual-Engine framework binding the Master Claude Code Guide to each Domain Notebook.
- Syllabi must include a "Pre-Work: Load Your Institutional Memory" section (after metadata, before Learning Objectives) directing learners to query their Domain Notebook alongside the Master Guide.

