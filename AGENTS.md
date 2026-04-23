# Agent Instructions (Project entrypoint)

This template's canonical governance is in `CLAUDE.md`.

## Source of truth
- Always read `CLAUDE.md` first and follow it as the single source of truth.

## Skills
- Some agents discover repo skills under `.agents/skills/<skill-name>/SKILL.md`.
- In this template, `.agents/skills/**/SKILL.md` are thin wrappers intended for broad agent compatibility.
- The canonical skill content lives in `.claude/skills/<skill-name>/SKILL.md`.
- When a wrapper skill is invoked, read the canonical file and follow it exactly.

## Adding Skills and Rules
- Add new skills to `.claude/skills/<skill-name>/SKILL.md` (canonical), and add a thin wrapper at `.agents/skills/<skill-name>/SKILL.md`.
- Keep wrapper `name`/`description` aligned with the canonical skill; keep wrapper bodies minimal and delegation-only.
- Keep project rules in `CLAUDE.md` as the single source of truth.
- If using Cursor rules, keep `.cursor/rules/project-context.mdc` as the only `alwaysApply: true` rule; keep others `alwaysApply: false`.
