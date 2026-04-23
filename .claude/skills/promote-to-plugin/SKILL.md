---
name: promote-to-plugin
description: Promotes an existing child project to a distributable plugin. Prepares it for registration in agent-family and public distribution.
---

# Promote to Plugin

## Purpose
Transform a child project that started as a personal project into a publicly distributable plugin — ready to be registered in agent-family and shared via GitHub Template.

## When to use
- A child project has matured and is worth sharing publicly
- A child was created with plugin intent from the start and is now ready to distribute

## Workflow

### 1. Identify the child
- If not specified: list child projects under `../{username}_children/` and ask which one to promote

### 2. Review readiness
Ask the user to confirm:
- [ ] Core functionality is stable
- [ ] README is written for public users (not just personal notes)
- [ ] No personal/private data is embedded in the project files

### 3. Apply plugin structure
Changes to make in the child project:
- Rewrite `README.md` as a public-facing usage guide (if not already done)
- Add `docs/90_logs/CHANGELOG.md` for release notes
- Ensure `CLAUDE.md` has no hardcoded personal references — use relative paths only
- Add `.github/` with issue templates if missing

### 4. Register in agent-family
- Add an entry to `../{agent-family-path}/plugins/registry.md`:
  ```
  - [{child-name}](https://github.com/{owner}/{child-name}) — {purpose}
  ```

### 5. Report
- List all changes made
- Remind user to:
  1. Push the child repo to GitHub as a **public** repo
  2. Enable **Template repository** in repo Settings if others should fork it
  3. Notify agent-family maintainer (or submit PR) if this is a community plugin
