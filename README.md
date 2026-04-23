# agent-family-core

> The **Family Core** template — the parent of your AI family system.

For installation instructions, visit the **[agent-family](https://github.com/shotgun1945/agent-family)** repository.

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
