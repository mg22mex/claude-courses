# CLAUDE.md — Claude Courses Project Memory

## Project Overview
This repository (`claude-courses`) hosts tailored training course content, syllabi, and localized automation custom skills designed to onboard different operational teams (Supply Chain/Logistics, Sales, Marketing, Design, Executive) to Claude Code.

## Directory Structure
- `training/syllabi/` — Detailed course curriculum outlines (one markdown file per department/course).
- `training/decks/` — Presentation markdown files optimized specifically for Marp.
- `.claude/skills/` — Custom auto-invokable operational script bundles scoped to this project.
- `.claude/agents/` — Specialized prompt personas and evaluation agents scoped to this project.

## Conventions & Formatting Standards

### Filenames & Assets
- **Filenames**: Use kebab-case for all files and directories (e.g., `supply-chain-syllabus.md`).
- **Assets**: Place images or diagrams in a subdirectory named after the deck (e.g., `training/decks/marketing-deck/assets/`).

### Syllabi Requirements
- Write in clean Markdown.
- Every syllabus must explicitly outline: Course title, target department user, clear learning objectives, modular lesson breakdowns, practical terminal/CLI exercises, and a link directory pointing to relevant local skills.

### Presentation Deck Requirements (Marp)
- All presentation files must live in `training/decks/` as a single document using standard `---` page separators.
- **Strict Header**: Every deck file MUST start with valid Marp YAML frontmatter:
  ```yaml
  ---
  marp: true
  theme: gaia
  paginate: true
  backgroundColor: #f5f5f5
  color: #333
  ---