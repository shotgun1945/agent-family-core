---
name: sync-to-children
description: Propagates updated skills, rules, or templates from the Family Core to child projects. Use when core-level changes should be distributed to all or specific children.
---

# Sync to Children

## Purpose
Push changes made in the Family Core outward to child projects — keeping all children in sync with the latest skills and rules.

## Before starting
Read these two meta-files:
- `data/children_manifest.md` — the single source of truth for what gets propagated. Check the `자식 로컬 복사 매핑` table for the list of skills to copy.
- `data/children_registry.md` — the list of all child projects (paths, names, types).

## What gets propagated
Only items listed in `data/children_manifest.md` → `자식 로컬 복사 매핑` are propagated.  
Do **not** propagate files not listed in the manifest.

## Workflow

### 1. Identify what changed
- Check which skills or rules were modified in the core
- Cross-reference with the manifest — only manifest-listed items are propagated
- Confirm with the user which children should receive the update

### 2. Locate child projects
- Read `data/children_registry.md` to get the full list of child paths
- Let the user select targets (all or specific children)

### 3. Copy changes to each target child
- For each row in `자식 로컬 복사 매핑`: copy the source file to the child's target path
- Copy the source file to the child's target path
- Do not overwrite child-specific sections (backlog prefix, purpose, persona refs, etc.)

### 4. Report
- List which files were updated in each child
- Flag any conflicts that need manual review

## Notes
- Always confirm before overwriting files in child projects
- Child-specific content (backlog, persona references) must not be touched
- `data/children_manifest.md` is never copied to children — children reference it from the parent
