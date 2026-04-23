---
name: create-child
description: Creates a new child project under the family. Asks whether the child is intended for public distribution — if yes, scaffolds it as a plugin-ready structure from the start.
---

# Create Child

## Purpose
Scaffold a new child project using the template stored in the Family Core.  
If the user intends to distribute it publicly, starts it in plugin-ready structure.

## Before starting
Read these two meta-files to understand the current state:
- `data/children_manifest.md` — what gets propagated (skills list, propagation rules)
- `data/children_registry.md` — which child projects already exist

## Workflow

### 1. Gather required values
Ask the user one by one:
1. Child name (becomes the folder and repo name)
2. Backlog prefix (2–3 uppercase letters)
3. Purpose (one-line description)
4. **"Do you plan to distribute this publicly as a plugin?"** (yes / no / not sure)

### 2. Select structure

**If no / not sure → Child structure**
- Copy `.claude/templates/child/` to `../{username}_children/{child-name}/`
- Replace placeholders

**If yes → Plugin-ready structure**
- Copy `.claude/templates/plugin/` to `../{username}_children/{child-name}/`
- Replace placeholders
- Note: can still be used privately until ready to distribute

### 3. Replace placeholders
- `{child-name}` → child name
- `{username}` → parent repo name (same folder name as the Family Core)
- `{BACKLOG_PREFIX}` → prefix chosen in step 1
- `{PROJECT_PURPOSE}` → purpose chosen in step 1
- `{SETUP_DATE}` → today's date (YYYY-MM-DD)

### 4. Copy propagated skills
Read `data/children_manifest.md` → `자식 로컬 복사 매핑` table.  
For each row, check the `대상 타입` column:
- `all` → copy regardless of child or plugin type
- `child` → copy only if this is a child-type project
- `plugin` → copy only if this is a plugin-type project

### 5. Register in registry
Add a row to `data/children_registry.md` → `## 프로젝트 목록` table:
- 이름: child name
- 타입: `child` or `plugin`
- 목적: one-line purpose
- 경로: `../{username}_children/{child-name}/`

### 6. Report
- Confirm folder created at `../{username}_children/{child-name}/`
- List files created
- List skills copied from manifest
- If plugin-ready: remind user to run `promote-to-plugin` when ready to distribute

## Customization
Edit `.claude/templates/child/` or `.claude/templates/plugin/` to change the default structure for all future children.
