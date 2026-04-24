---
name: create-child
description: Creates a new child project under the family, scaffolded from the template in data/templates/child/.
---

# Create Child

## Purpose
Scaffold a new child project using the template stored in the Family Core.

## Before starting
Read these meta-files to understand the current state:
- `data/children_manifest.md` — what gets propagated (skills list, propagation rules)
- `data/children_registry.md` — which child projects already exist
- `data/templates/child/` — child project template files

## Workflow

### 1. Gather required values
Ask the user one by one:
1. Child name (becomes the folder and repo name)
2. Backlog prefix (2–3 uppercase letters)
3. Purpose (one-line description)

### 2. Copy template
- Copy `data/templates/child/` to `../{username}_children/{child-name}/`

### 3. Replace placeholders
- `{child-name}` → child name
- `{username}` → parent repo name (same folder name as the Family Core)
- `{BACKLOG_PREFIX}` → prefix chosen in step 1
- `{PROJECT_PURPOSE}` → purpose chosen in step 1
- `{SETUP_DATE}` → today's date (YYYY-MM-DD)

### 4. Copy propagated skills
Read `data/children_manifest.md` → `자식 로컬 복사 매핑` table.  
For each row, check the `대상 타입` column:
- `all` → copy to all child projects
- `child` → copy only to child-type projects

### 5. Register in registry
Add a row to `data/children_registry.md` → `## 프로젝트 목록` table:
- 이름: child name
- 타입: `child`
- 목적: one-line purpose
- 경로: `../{username}_children/{child-name}/`

### 6. Report
- Confirm folder created at `../{username}_children/{child-name}/`
- List files created
- List skills copied from manifest

## Customization
Edit `data/templates/child/` to change the default structure for all future children.
