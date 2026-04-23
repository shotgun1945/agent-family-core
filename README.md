# agent-family-core

> The **Family Core** template — the parent of your AI family system.

For full installation instructions, visit the **[agent-family](https://github.com/shotgun1945/agent-family)** repository.

If you already cloned this repo and opened it in your AI agent, paste the prompt below to complete setup:

```
Set up my Family Core.

Ask me the following values one by one (starting with language), then replace all placeholders. Use today's date for {SETUP_DATE} (YYYY-MM-DD).

Required:
- Language (e.g. English / 한국어 / 日本語) — ask this first, then use it for all output
- Family name (this becomes {username} in all files)
- AI name
- Backlog prefix (2–3 uppercase letters, e.g. MY)

Files to update after collecting values:
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
Note: {username} and {family-name} = family name entered above.

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
├── .claude/
│   ├── settings.json              # Claude Code settings
│   ├── MEMORY.md                  # Agent memory index
│   ├── skills/                    # Reusable agent behaviors
│   └── templates/
│       ├── child/                 # Template for personal child projects
│       └── plugin/                # Starting point for plugin developers
├── data/
│   ├── persona/                   # User & AI persona files
│   ├── children_manifest.md       # What gets propagated to children
│   └── children_registry.md       # List of all child projects and plugins
└── docs/                          # Backlog and project documents
```

---

## Skills

| Skill | Purpose |
|-------|---------|
| `create-child` | Scaffold a new personal child project |
| `install-plugin` | Browse registry and install an official plugin |
| `promote-to-plugin` | Promote a child to a distributable plugin |
| `sync-to-children` | Push updated skills or rules to children |
| `sync-to-core` | Promote a child-level change back to the parent |

---

## License

MIT
