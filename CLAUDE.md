# CLAUDE.md — Weatherman AI Portal

## Project Overview
This repository powers **The Weatherman AI Portal** — a custom, zero-install Streamlit web application that delivers operational team training through a browser interface. No terminal, no CLI, no developer setup required.

Each team member accesses the portal via a secure URL, selects their name from a sidebar dropdown, and receives pre-configured API settings and system profiles. Business files (.csv, .xlsx, .pdf) are uploaded through the browser, and all work is done through natural-language prompts.

## Repository Structure
- `training/rick/` — Executive, Entrepreneurship & Management course (Rick). Contains `syllabus.md`, `data/`, `exercises/`, `presets/`.
- `training/sunny/` — Purchasing & Logistics course (Sunny). Contains `syllabus.md`, `data/`, `exercises/`, `presets/`.
- `training/mollie/` — Sales & Financials course (Mollie). Contains `syllabus.md`, `data/`, `exercises/`, `presets/`.
- `training/christine/` — Marketing course (Christine). Contains `syllabus.md`, `data/`, `exercises/`, `presets/`.
- `training/design/` — Design course (Paula & Gaby). Contains `syllabus.md`, `data/mock-assets/`, `exercises/`, `presets/`.
- `portal-flight-manual.md` — Simplified 1-page guide covering how to log in, select a profile, and upload files.

## Dual-Engine Framework

This repository operates on a two-notebook model binding every training track to a Domain Notebook plus the shared Master Guide:

```
Master Guide Notebook (NotebookLM)
  + Individual Domain Notebook (NotebookLM)
  → Weatherman AI Portal Workspace
```

### Workflow Rules

**Rule 1: Dual Query Before Content** — Before generating any system prompt, building any preset, or creating any document template, query the Master Guide for technical patterns AND the Domain Notebook for business rules, data schemas, and known edge cases.

**Rule 2: Portal-Centric Language** — All exercises, syllabi, and presets must frame delivery through the web portal interface (browser upload, sidebar profile selection, natural-language prompts). No terminal commands, CLI references, or developer environment instructions.

**Rule 3: Cross-Verification** — All preset generation, data testing, and document templating must cross-verify patterns against the track's assigned NotebookLM URL before finalizing.

**Rule 4: URL Permanence** — The six NotebookLM URLs in `portal-flight-manual.md` are permanent references. Do not modify, replace, or regenerate them.

## Quality Gates

Every exercise across all tracks must satisfy these structural checks:

| Gate | Requirement |
|---|---|
| **Scenario** | A realistic business context narrative grounded in the track's domain |
| **Learning Objectives** | 4-6 measurable outcomes the learner achieves by completing the exercise |
| **Dataset** | Inline sample data or a path to a file in the track's `data/` subdirectory |
| **Known Issues** | A table of deliberate problems planted in the data that the learner must discover |
| **Walkthrough** | Step-by-step numbered instructions with portal login, file upload, and natural-language prompt examples |
| **Expected Output** | Clear definition of what files and reports the learner produces |

Syllabi must additionally outline: course title, target department user, modular lesson breakdowns, portal-based exercises, and a link directory pointing to relevant presets.

## Conventions & Formatting Standards

### Filenames & Assets
- **Filenames**: Strict lower-case kebab-case for ALL files and directories. Underscores and uppercase are not allowed. Standard conventions (`SKILL.md`, `README.md`) are exempt.
- **Numbered exercises**: Use `exercise-1.md` format (hyphen, not underscore).
- **Assets**: Place all data files in the track's `data/` subdirectory (e.g., `training/mollie/data/`). No data files may live outside `data/`.
- **Presets**: Named `presets/` (not `skills/`). Each preset is a system-instruction template optimized for the web portal chat interface.

### Portal-Centric Language
- Never reference `claude` commands, terminal sessions, bash, shell prompts, or CLI arguments.
- Exercise walkthroughs describe: logging into the portal, selecting a profile from the sidebar dropdown, clicking the paperclip button to upload a file, and pasting natural-language prompts.
- File outputs are produced by the portal AI and downloaded via the browser.
