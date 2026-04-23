---
name: install-plugin
description: Installs an official plugin from the agent-family registry into the family's children directory. Fetches the registry via raw URL, lists available plugins, and clones the selected one.
---

# Install Plugin

## Purpose
Browse and install official agent-family plugins into `../{username}_children/`.  
Plugins are maintained as independent Git repositories and stay connected to their source for future updates.

## Before starting
Read `data/children_registry.md` to check which plugins are already installed.

## Workflow

### 1. Fetch the registry
Read the plugin registry via raw URL:
```
https://raw.githubusercontent.com/shotgun1945/agent-family/main/plugins/registry.md
```
Parse the `## Available Plugins` table and list available plugins to the user.

### 2. Select a plugin
Ask the user which plugin(s) to install.  
If already installed (present in `data/children_registry.md`), warn the user and ask to confirm reinstall.

### 3. Clone the plugin repo
```bash
git clone {plugin-repo} ../{username}_children/{plugin-name}
```
Keep `.git` intact — this allows future updates via `git pull`.

### 4. Replace placeholders
In the cloned plugin's files, replace:
- `{username}` → parent repo name
- `{SETUP_DATE}` → today's date (YYYY-MM-DD)
- Any other placeholders defined in the plugin's `CLAUDE.md`

### 5. Register in registry
Add a row to `data/children_registry.md` → `## 프로젝트 목록` table:
- 이름: plugin name
- 타입: `plugin`
- 목적: plugin description from registry
- 경로: `../{username}_children/{plugin-name}/`

### 6. Report
- Confirm plugin installed at `../{username}_children/{plugin-name}/`
- Remind user: to update the plugin later, run `git pull` inside the plugin folder

## Updating a plugin
To update an installed plugin to the latest version:
```bash
cd ../{username}_children/{plugin-name}
git pull
```
