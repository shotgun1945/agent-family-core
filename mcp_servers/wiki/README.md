# family-wiki MCP server

Read-only MCP wrapper around the Family Core `data/wiki/`. Lets any MCP-aware
agent (Claude Code, Cursor, etc.) — especially **child-project sessions** —
query the parent wiki without hardcoding relative paths.

## Tools

| Tool | Purpose |
|------|---------|
| `wiki_index()` | Read `data/wiki/index.md` (entry point + FAQ map) |
| `wiki_search(query, limit=8)` | Ranked JSON search via `scripts/wiki.py search` |
| `wiki_read(path)` | Read a wiki page or list a directory (relative to `data/wiki/`) |

Answer synthesis is **not** done by the server — the calling agent reads
the pages and writes the response. The server (and the wiki) stay
**read-only from children**: ingest/lint and any wiki writes happen in the
Family Core only.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed
- `scripts/wiki.py` present in the Family Core root (ships with this template)

## Run locally (sanity check)

```bash
cd mcp_servers/wiki
uv run --with 'mcp[cli]' mcp dev server.py
```

`mcp dev` opens the MCP inspector so you can call each tool by hand.

## Register in a Claude Code session

Add to the project's `.mcp.json` (or `.claude/settings.json` under
`mcpServers`), replacing the placeholder with your Family Core's
**absolute path**:

```json
{
  "mcpServers": {
    "family-wiki": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "{ABSOLUTE_PATH_TO_FAMILY_CORE}/mcp_servers/wiki",
        "python",
        "server.py"
      ]
    }
  }
}
```

In child projects this lets `mcp__family-wiki__wiki_index`,
`...__wiki_search`, `...__wiki_read` be called directly — no more
`../../{username}/data/wiki/...` path juggling.

> Absolute paths are machine-specific: keep `.mcp.json` out of shared Git
> history, or register per machine.

## Configuration

`FAMILY_CORE_ROOT` env var overrides the project root (defaults to the
repo two levels above this file). Useful if you symlink the server or
run it from elsewhere.
