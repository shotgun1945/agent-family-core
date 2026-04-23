# agent-family-core

> The **Family Core** template — the parent of your AI family system.

> [!NOTE]
> **Do not clone or fork this repo.**
> Open it in your AI agent and paste the onboarding prompt below — the agent sets everything up for you.

---

## What is this?

The **parent** project at the center of your AI family system — defined entirely in Markdown, no code required.

- **No code in the parent** — all configuration is `.md` files
- **Files are memory** — Markdown files are the agent's persistent state
- **Skills are behavior** — one `SKILL.md` = one reusable workflow
- **Parent manages, children execute** — skills and rules flow down from parent to children

---

## How to use

### 1. Open this repo in your AI agent

In Claude Code, Cursor, or any AI agent that reads `CLAUDE.md`:

```
Open this repo as the working directory.
```

### 2. Paste the onboarding prompt

Copy the prompt below and paste it into your AI agent as-is.  
The agent will ask you each value one by one, set up the core, then offer available plugins to install.

```
Set up my agent-family system.

Ask me each of the following values one by one, then set up the Family Core.
After core setup, fetch the plugin registry from:
https://raw.githubusercontent.com/shotgun1945/agent-family/main/plugins/registry.md
List available plugins and ask which ones I want to install.

Required (core):
- username
- AI name
- Backlog prefix (2–3 uppercase letters, e.g. MY)
- Language (default language for all responses and documents, e.g. English / 한국어 / 日本語)
```

---

## Family Structure

Family Core is the **parent**. Child projects live alongside it and inherit its skills and rules.

```
{username}_family/
├── {username}/                    # Family Core (this repo — parent)
│   ├── CLAUDE.md                  # Governance constitution
│   ├── data/persona/              # Who the user is, who the AI is
│   └── .claude/skills/            # Skills managed here, propagated to children
└── {username}_children/
    ├── financial-planner/         # Child project (personal)
    └── telegram-bot/              # Plugin (installed from registry)
```

**Child vs Plugin:**
A **child** is a personal project created locally via `create-child`.  
A **plugin** is an official project installed from the registry via `install-plugin`.

---

## Folder Structure

```
{username}/
├── CLAUDE.md                      # Agent governance constitution
├── .claude/
│   ├── settings.json              # Claude Code settings
│   ├── MEMORY.md                  # Agent memory index
│   ├── skills/                    # Reusable agent behaviors
│   └── templates/                 # Scaffolding used by create-child skill
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
