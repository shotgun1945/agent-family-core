# agent-family-core

> The **Family Core** template — the parent of your AI family system.

For full installation instructions, visit the **[agent-family](https://github.com/shotgun1945/agent-family)** repository.

If you already cloned this repo and opened it in your AI agent, paste the prompt below to complete setup:

```
Set up my Family Core.

Step 1: Ask me which language to use (e.g. English / 한국어 / 日本語). Use that language for all output from this point on.

Step 2: Once I answer, show me this form and wait for me to fill it in and send it back:

---
Family name (becomes {username} in all files):
AI name:
Backlog prefix (2–3 uppercase letters, e.g. MY):
---

Step 3: After I submit the form, replace all placeholders. Use today's date for {SETUP_DATE} (YYYY-MM-DD).
Files to update:
- README.md → {family-name}
- CLAUDE.md → {SETUP_DATE}, {username}, {LANGUAGE}, {AI_NAME}, {BACKLOG_PREFIX}
- data/persona/assistant_persona.md → {SETUP_DATE}, {AI_NAME}, {username}
- data/persona/profile.md → {SETUP_DATE}
- data/persona/preferences.md → {SETUP_DATE}
- data/persona/personality.md → {SETUP_DATE}
- data/persona/update_rules.md → {SETUP_DATE}
- data/children_manifest.md → {SETUP_DATE}, {username}
- data/children_registry.md → {SETUP_DATE}, {username}
- docs/README.md → {SETUP_DATE}
- docs/00_backlog/backlog.md → {SETUP_DATE}, {BACKLOG_PREFIX}
- docs/00_backlog/backlog_done.md → {SETUP_DATE}
Note: {username} and {family-name} = family name from the form.

After setup, optionally ask if I want to set up my persona (profile, preferences, personality).
```

---

## What is this?

The **parent** project at the center of your AI family system.

- **Files are memory** — Markdown files are the agent's persistent state
- **Skills are behavior** — one `SKILL.md` = one reusable workflow
- **Parent manages, children execute** — skills and rules flow down from parent to children

---

## Folder Structure

```
{family-name}/
├── CLAUDE.md                      # Agent governance constitution
├── AGENTS.md                      # Agent compatibility entrypoint
├── .claude/
│   ├── settings.json              # Claude Code settings
│   └── skills/                    # Reusable agent behaviors
├── .agents/
│   └── skills/                    # Thin wrappers for broad agent compatibility
├── data/
│   ├── persona/                   # User & AI persona files
│   └── templates/
│       └── child/                 # Template for child projects
│   ├── children_manifest.md       # What gets propagated to children
│   └── children_registry.md       # List of all child projects and plugins
└── docs/                          # Backlog and project documents
```

---

## Skills

| Skill | Purpose |
|-------|---------|
| `create-child` | Scaffold a new child project |
| `sync-to-children` | Push updated skills or rules to children |
| `sync-to-core` | Promote a child-level change back to the parent |

---

## License

MIT
