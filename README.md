# agent-family-core

> The **Family Core** template — the parent of your AI family system.

> [!NOTE]
> **Do not fork or edit this repo directly.**
> Copy the onboarding prompt below and paste it to your AI agent — it will set everything up for you.

[![Use this template](https://img.shields.io/badge/Use%20this%20template-2ea44f?style=for-the-badge)](../../generate)

---

## What is this?

The **parent** project that sits at the center of your AI family system — defined entirely in Markdown.

- **No code** — all configuration is `.md` files
- **No database** — files are the agent's memory
- **Parent of all children** — manages skills, rules, and templates that flow down to child projects

---

## Quick Start

### 1. Create your repo

Click **"Use this template"** → **"Create a new repository"**.  
Name it `{username}` (e.g. `alice`, `darlin`).

### 2. Clone locally

```bash
git clone https://github.com/{your-github-id}/{username}.git
cd {username}
```

### 3. Open Claude Code

```bash
claude
```

### 4. Paste the onboarding prompt

Copy the prompt below and paste it into Claude Code as-is.  
The agent will ask you each value one by one and set everything up.

```
Set up my agent-family-core.

Ask me each of the following values one by one, then replace all placeholders and fill in the persona files interactively.

Required:
- username
- AI name
- Backlog prefix (2–3 uppercase letters, e.g. MY)
- Project purpose (one-line description)
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
    ├── financial-planner/         # Child project
    └── telegram-bot/              # Child project (distributable → plugin)
```

**Child vs Plugin:**  
A child is any project in your family system.  
A **plugin** is a child designed to be distributed publicly — packaged so others can use it.

---

## Folder Structure

```
{username}/
├── CLAUDE.md                      # Agent governance constitution
├── .claude/
│   ├── settings.json              # Claude Code settings
│   ├── MEMORY.md                  # Agent memory index
│   ├── skills/                    # Reusable agent behaviors
│   └── templates/family-child/    # Template used by create-child skill
├── data/persona/                  # User & AI persona files
└── docs/                          # Backlog and project documents
```

---

## Managing Children

Skills and rules live in the parent and flow to children via built-in skills.

| Skill | Direction | Purpose |
|-------|-----------|---------|
| `create-child` | Parent → new child | Scaffold a new child project |
| `sync-to-children` | Parent → children | Push updated skills or rules to children |
| `sync-to-core` | Child → Parent | Promote a child-level change back to the parent |

To create a child project, just ask the agent:
```
Create a new child project.
```

---

## License

MIT
