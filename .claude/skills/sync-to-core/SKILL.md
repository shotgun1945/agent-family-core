---
name: sync-to-core
description: Promotes a change made in a child project back to the Family Core. Use when a child-level improvement to a skill or rule should become part of the core.
---

# Sync to Core

## Purpose
Bring a change from a child project up to the Family Core — the reverse of `sync-to-children`.

## When to use
- A skill was improved or fixed in a child project
- A new rule was added to a child that should apply to all children
- A child's template or prompt was refined and should update the core's version

## Before starting
Read `data/children_manifest.md` to check which skills are currently designated for propagation (`자식 로컬 복사 매핑` table).  
Only skills listed there are candidates for core promotion.

## Workflow

### 1. Identify the change
- Ask the user which file(s) in the child project should be promoted
- Show a diff or summary of what changed

### 2. Review for core compatibility
- Check if the change is child-specific or genuinely universal
- If child-specific content is mixed in, ask the user to confirm what to extract
- Verify the skill is listed in `data/children_manifest.md` → `자식 로컬 복사 매핑`
  - If not listed, ask the user if it should be added to the manifest first

### 3. Apply to core
- Copy or merge the change into the corresponding file in the Family Core
- For skills: update `.claude/skills/{skill-name}/SKILL.md` in core
- For CLAUDE.md rules: add to the appropriate section
- If a new skill is being promoted: add it to the manifest's `자식 로컬 복사 매핑` table

### 4. Confirm propagation
- Ask if the updated core change should immediately be pushed to other children via `sync-to-children`

### 5. Report
- Summarize what was updated in core
- List changes made to `data/children_manifest.md` (if any)
- List next steps if propagation is needed

## Notes
- Never blindly overwrite core files — always review the diff first
- Child-specific fields (backlog prefix, purpose, core path) must be stripped before promoting
