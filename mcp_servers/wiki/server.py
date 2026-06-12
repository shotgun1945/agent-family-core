"""Family Core wiki MCP server.

Exposes the data/wiki layer as three read-only tools so that any MCP-aware
agent (Claude Code, Cursor, etc.) — especially child-project sessions — can
query the parent wiki without knowing its absolute path. Synthesis stays on
the agent side: the calling agent reads the pages and writes the answer.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

PROJECT_ROOT = Path(
    os.environ.get(
        "FAMILY_CORE_ROOT",
        Path(__file__).resolve().parents[2],
    )
).resolve()
WIKI_ROOT = PROJECT_ROOT / "data" / "wiki"
WIKI_SCRIPT = PROJECT_ROOT / "scripts" / "wiki.py"

mcp = FastMCP("family-wiki")


def _safe_wiki_path(rel_path: str) -> Path:
    candidate = (WIKI_ROOT / rel_path).resolve()
    if WIKI_ROOT not in candidate.parents and candidate != WIKI_ROOT:
        raise ValueError(f"path escapes wiki root: {rel_path}")
    return candidate


@mcp.tool()
def wiki_index() -> str:
    """Return data/wiki/index.md — the wiki entry point and FAQ map.

    Call this first when answering a knowledge / concept / entity question
    that the family wiki may already cover.
    """
    return (WIKI_ROOT / "index.md").read_text(encoding="utf-8")


@mcp.tool()
def wiki_search(query: str, limit: int = 8) -> str:
    """Search wiki pages and return ranked JSON results.

    Thin wrapper around `scripts/wiki.py search`. Use when the index alone
    does not pinpoint the right concept/entity/synthesis page. Returned
    snippets are *candidates only* — read the actual page with `wiki_read`
    before citing it in an answer.
    """
    result = subprocess.run(
        [
            "python3",
            str(WIKI_SCRIPT),
            "search",
            query,
            "--root",
            str(PROJECT_ROOT),
            "--limit",
            str(limit),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return json.dumps(
            {"error": "wiki.py search failed", "stderr": result.stderr.strip()},
            ensure_ascii=False,
        )
    return result.stdout


@mcp.tool()
def wiki_read(path: str) -> str:
    """Read a wiki page by path relative to data/wiki.

    Examples:
        wiki_read("concepts/entities/redis.md")
        wiki_read("synthesis/operating_overview.md")
        wiki_read("index.md")

    Refuses paths that escape the wiki root.
    """
    target = _safe_wiki_path(path)
    if not target.exists():
        return json.dumps(
            {"error": "not found", "path": path}, ensure_ascii=False
        )
    if target.is_dir():
        entries = sorted(p.name for p in target.iterdir())
        return json.dumps(
            {"path": path, "type": "directory", "entries": entries},
            ensure_ascii=False,
        )
    return target.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
