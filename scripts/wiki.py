#!/usr/bin/env python3
"""Common wiki tooling for the Family Core markdown wiki layer."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
import os
from pathlib import Path
from typing import Any


WIKI_ROOT_DEFAULT = Path("data/wiki")
STALE_DAYS_DEFAULT = 60

SKIP_NAMES = {"README.md", "index.md", "log.md", "wiki_rule.md"}
PAGE_DIRS = ["concepts", "synthesis", "analysis"]
SEARCH_SNIPPET_CHARS = 220
VALID_PAGE_TYPES = {"concept", "entity", "synthesis", "analysis"}
REQUIRED_SECTIONS: dict[str, list[str | list[str]]] = {
    "concept": ["한 줄 정의", ["핵심 내용", "개요", "핵심 특징"], "연관 개념"],
    "entity": ["한 줄 정의"],
    "synthesis": [],
    "analysis": ["결론"],
}

BACKLINK_MARKER_START = "<!-- backlinks:auto -->"
BACKLINK_MARKER_END = "<!-- /backlinks:auto -->"
BACKLINK_HEADING = "## 백링크"
BACKLINK_BLOCK_RE = re.compile(
    re.escape(BACKLINK_MARKER_START) + r".*?" + re.escape(BACKLINK_MARKER_END),
    re.DOTALL,
)


def parse_frontmatter(path: Path) -> dict[str, Any]:
    """Parse a small YAML frontmatter subset without external dependencies."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return {}

    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}

    result: dict[str, Any] = {}
    current_list_key: str | None = None
    list_items: list[str] = []

    for line in content[4:end].splitlines():
        if re.match(r"^\s+-\s", line):
            item = re.sub(r"^\s+-\s*", "", line).strip()
            if current_list_key is not None:
                list_items.append(item)
            continue

        if current_list_key is not None:
            result[current_list_key] = list_items
            current_list_key = None
            list_items = []

        if ":" not in line:
            continue

        key, _, raw = line.partition(":")
        key = key.strip()
        value = raw.strip()

        if not value:
            current_list_key = key
            list_items = []
        elif value.startswith("["):
            result[key] = [item.strip().strip("'\"") for item in value.strip("[]").split(",") if item.strip()]
        else:
            result[key] = value.strip("'\"")

    if current_list_key is not None:
        result[current_list_key] = list_items

    return result


def resolve_wiki_root(root: str | None, wiki: str | None) -> Path:
    if wiki:
        path = Path(wiki)
        return path.resolve() if path.is_absolute() else (Path(root or ".") / path).resolve()
    return (Path(root or ".") / WIKI_ROOT_DEFAULT).resolve()


def infer_project_root(wiki_root: Path, root: str | None) -> Path:
    if root:
        return Path(root).resolve()
    if wiki_root.name == "wiki" and wiki_root.parent.name == "data":
        return wiki_root.parent.parent.resolve()
    return Path.cwd().resolve()


def get_wiki_pages(wiki_root: Path) -> list[Path]:
    pages: list[Path] = []
    for subdir in PAGE_DIRS:
        directory = wiki_root / subdir
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.md")):
            if path.name not in SKIP_NAMES:
                pages.append(path)
    return pages


def get_search_pages(wiki_root: Path) -> list[Path]:
    pages = []
    index_path = wiki_root / "index.md"
    if index_path.exists():
        pages.append(index_path)
    pages.extend(get_wiki_pages(wiki_root))
    return pages


def rel(wiki_root: Path, page: Path) -> str:
    return page.relative_to(wiki_root).as_posix()


def get_index_links(wiki_root: Path) -> set[str]:
    index_path = wiki_root / "index.md"
    if not index_path.exists():
        return set()
    content = index_path.read_text(encoding="utf-8")
    return set(re.findall(r"\[.*?\]\(([^)]+\.md)\)", content))


def get_log_created_paths(wiki_root: Path) -> set[str]:
    log_path = wiki_root / "log.md"
    if not log_path.exists():
        return set()
    content = log_path.read_text(encoding="utf-8")
    return set(re.findall(r"\[[\d-]+\] CREATED ([\w/.\-]+\.md)", content))


def markdown_links(content: str) -> list[str]:
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
    return [link.strip() for link in links if link.strip()]


def is_external_link(link: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link)) or link.startswith("#")


def resolve_markdown_link(project_root: Path, wiki_root: Path, source_page: Path, link: str) -> Path | None:
    if is_external_link(link):
        return None
    target = link.split("#", 1)[0].strip()
    if not target or not target.endswith(".md"):
        return None

    target_path = Path(target)
    if target_path.is_absolute():
        return target_path
    if target.startswith("data/wiki/"):
        return (project_root / target_path).resolve()
    if target.startswith(tuple(f"{directory}/" for directory in PAGE_DIRS)):
        return (wiki_root / target_path).resolve()
    return (source_page.parent / target_path).resolve()


def check_orphans(wiki_root: Path, pages: list[Path], index_links: set[str]) -> list[str]:
    return [rel(wiki_root, page) for page in pages if rel(wiki_root, page) not in index_links]


def check_stale(wiki_root: Path, pages: list[Path], stale_days: int) -> list[dict[str, Any]]:
    cutoff = date.today() - timedelta(days=stale_days)
    stale: list[dict[str, Any]] = []
    for page in pages:
        frontmatter = parse_frontmatter(page)
        updated_str = str(frontmatter.get("updated", "")).strip()
        if not updated_str:
            continue
        try:
            updated = date.fromisoformat(updated_str)
        except ValueError:
            continue
        if updated < cutoff:
            stale.append(
                {
                    "path": rel(wiki_root, page),
                    "updated": updated_str,
                    "days_ago": (date.today() - updated).days,
                }
            )
    return sorted(stale, key=lambda item: item["days_ago"], reverse=True)


def check_no_sources(wiki_root: Path, pages: list[Path]) -> list[str]:
    no_sources: list[str] = []
    for page in pages:
        page_path = rel(wiki_root, page)
        if not page_path.startswith("concepts/"):
            continue
        frontmatter = parse_frontmatter(page)
        if not frontmatter.get("sources", []):
            no_sources.append(page_path)
    return no_sources


def check_log_index_mismatch(wiki_root: Path, index_links: set[str], log_created: set[str]) -> list[str]:
    wiki_prefixes = tuple(f"{directory}/" for directory in PAGE_DIRS)
    return sorted(
        path
        for path in log_created
        if path.startswith(wiki_prefixes)
        and path not in index_links
        and (wiki_root / path).exists()
    )


def check_broken_links(project_root: Path, wiki_root: Path, pages: list[Path]) -> list[dict[str, str]]:
    broken: list[dict[str, str]] = []
    scan_pages = [wiki_root / "index.md", *pages]
    for page in scan_pages:
        if not page.exists():
            continue
        content = page.read_text(encoding="utf-8")
        for link in markdown_links(content):
            target = resolve_markdown_link(project_root, wiki_root, page, link)
            if target is None or target.exists():
                continue
            broken.append(
                {
                    "path": rel(wiki_root, page),
                    "target": link,
                }
            )
    return broken


def source_exists(project_root: Path, wiki_root: Path, source: str) -> bool:
    if not source or source.startswith(("inline:", "mcp:", "http://", "https://")):
        return True
    source_path = Path(source)
    if source_path.is_absolute():
        return source_path.exists()
    if source.startswith("data/"):
        return (project_root / source_path).exists()
    return (wiki_root / source_path).exists() or (project_root / source_path).exists()


def check_missing_source_paths(project_root: Path, wiki_root: Path, pages: list[Path]) -> list[dict[str, str]]:
    missing: list[dict[str, str]] = []
    for page in pages:
        frontmatter = parse_frontmatter(page)
        sources = frontmatter.get("sources", [])
        if isinstance(sources, str):
            sources = [sources]
        if not isinstance(sources, list):
            continue
        for source in sources:
            source_text = str(source).strip()
            if source_exists(project_root, wiki_root, source_text):
                continue
            missing.append({"path": rel(wiki_root, page), "source": source_text})
    return missing


def check_frontmatter_schema(wiki_root: Path, pages: list[Path]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for page in pages:
        page_path = rel(wiki_root, page)
        frontmatter = parse_frontmatter(page)
        missing: list[str] = []
        invalid: list[str] = []
        for key in ["updated", "type"]:
            if not frontmatter.get(key):
                missing.append(key)
        page_type = frontmatter.get("type")
        if page_type and page_type not in VALID_PAGE_TYPES:
            invalid.append("type")
        if page_path.startswith("concepts/"):
            for key in ["domain", "sources"]:
                if key not in frontmatter:
                    missing.append(key)
        if missing or invalid:
            issues.append({"path": page_path, "missing": missing, "invalid": invalid})
    return issues


def check_ledger(wiki_root: Path, filename: str, id_prefix: str) -> dict[str, Any]:
    """Meta check for a wiki ledger file (contradictions.md, open_questions.md).

    Returns presence, open/resolved counts, and any structural issues — content
    judgment is an LLM pass per the wiki-lint skill.
    """
    path = wiki_root / filename
    if not path.exists():
        return {"present": False, "open": 0, "resolved": 0, "issues": ["missing"]}
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {"present": True, "open": 0, "resolved": 0, "issues": [f"read_error: {exc}"]}

    issues: list[str] = []
    open_count = 0
    resolved_count = 0
    section: str | None = None
    entry_re = re.compile(rf"^###\s+\[{re.escape(id_prefix)}-\d+\]")
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip().lower()
            if heading.startswith("open"):
                section = "open"
            elif heading.startswith("resolved"):
                section = "resolved"
            else:
                section = None
            continue
        if section and entry_re.match(stripped):
            if section == "open":
                open_count += 1
            else:
                resolved_count += 1

    ids = re.findall(rf"###\s+\[({re.escape(id_prefix)}-\d+)\]", content)
    duplicate = sorted({cid for cid in ids if ids.count(cid) > 1})
    if duplicate:
        issues.append(f"duplicate_ids: {','.join(duplicate)}")

    return {"present": True, "open": open_count, "resolved": resolved_count, "issues": issues}


def check_contradictions_ledger(wiki_root: Path) -> dict[str, Any]:
    return check_ledger(wiki_root, "contradictions.md", "C")


def check_open_questions_ledger(wiki_root: Path) -> dict[str, Any]:
    return check_ledger(wiki_root, "open_questions.md", "Q")


def compute_backlinks(project_root: Path, wiki_root: Path, pages: list[Path]) -> dict[str, list[str]]:
    """Map page rel-path -> sorted list of pages that link to it.

    Only counts links from other wiki content pages (concepts/synthesis/analysis).
    index.md and log.md are excluded as sources to avoid noise.
    """
    inbound: dict[str, set[str]] = {rel(wiki_root, page): set() for page in pages}
    page_set = set(inbound.keys())
    for source in pages:
        source_rel = rel(wiki_root, source)
        try:
            content = source.read_text(encoding="utf-8")
        except OSError:
            continue
        body = BACKLINK_BLOCK_RE.sub("", content)
        for link in markdown_links(body):
            target = resolve_markdown_link(project_root, wiki_root, source, link)
            if target is None:
                continue
            try:
                target_rel = target.relative_to(wiki_root).as_posix()
            except ValueError:
                continue
            if target_rel == source_rel:
                continue
            if target_rel in page_set:
                inbound[target_rel].add(source_rel)
    return {key: sorted(value) for key, value in inbound.items()}


def parse_backlink_block(content: str) -> set[str] | None:
    """Return the set of rel paths listed inside the backlinks marker, or None if absent."""
    match = BACKLINK_BLOCK_RE.search(content)
    if not match:
        return None
    return set(re.findall(r"\(([^)]+\.md)\)", match.group(0)))


def render_backlink_block(wiki_root: Path, page: Path, inbound: list[str]) -> str:
    if not inbound:
        body = "_(없음)_"
    else:
        lines = []
        for target_rel in inbound:
            target = wiki_root / target_rel
            try:
                content = target.read_text(encoding="utf-8")
                title = extract_title(content, fallback=target.stem)
            except OSError:
                title = target.stem
            rel_link = os.path.relpath(wiki_root / target_rel, start=page.parent).replace(os.sep, "/")
            lines.append(f"- [{title}]({rel_link})")
        body = "\n".join(lines)
    return f"{BACKLINK_MARKER_START}\n{BACKLINK_HEADING}\n\n{body}\n{BACKLINK_MARKER_END}"


def check_backlinks(
    wiki_root: Path,
    pages: list[Path],
    backlink_map: dict[str, list[str]],
) -> tuple[list[str], list[dict[str, Any]]]:
    """Return (missing, stale).

    - missing: pages that have inbound links but no backlink marker block.
    - stale: pages whose existing marker block diverges from computed inbound set.
    """
    missing: list[str] = []
    stale: list[dict[str, Any]] = []
    for page in pages:
        page_rel = rel(wiki_root, page)
        inbound = backlink_map.get(page_rel, [])
        try:
            content = page.read_text(encoding="utf-8")
        except OSError:
            continue
        listed = parse_backlink_block(content)
        if listed is None:
            if inbound:
                missing.append(page_rel)
            continue
        listed_norm: set[str] = set()
        for entry in listed:
            target = resolve_markdown_link(wiki_root.parent.parent, wiki_root, page, entry)
            if target is None:
                continue
            try:
                listed_norm.add(target.relative_to(wiki_root).as_posix())
            except ValueError:
                continue
        if listed_norm != set(inbound):
            stale.append(
                {
                    "path": page_rel,
                    "expected": inbound,
                    "found": sorted(listed_norm),
                }
            )
    return missing, stale


def check_required_sections(wiki_root: Path, pages: list[Path]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for page in pages:
        content = page.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(page)
        page_type = str(frontmatter.get("type", ""))
        required = REQUIRED_SECTIONS.get(page_type, [])
        if not required:
            continue
        headings = set(extract_headings(content))
        missing: list[str] = []
        for section in required:
            if isinstance(section, list):
                if not any(alt in headings for alt in section):
                    missing.append(" | ".join(section))
            elif section not in headings:
                missing.append(section)
        if missing:
            issues.append({"path": rel(wiki_root, page), "missing": missing})
    return issues


def build_lint_result(project_root: Path, wiki_root: Path, stale_days: int) -> dict[str, Any]:
    pages = get_wiki_pages(wiki_root)
    index_links = get_index_links(wiki_root)
    log_created = get_log_created_paths(wiki_root)

    orphans = check_orphans(wiki_root, pages, index_links)
    stale = check_stale(wiki_root, pages, stale_days)
    no_sources = check_no_sources(wiki_root, pages)
    mismatch = check_log_index_mismatch(wiki_root, index_links, log_created)
    broken_links = check_broken_links(project_root, wiki_root, pages)
    missing_source_paths = check_missing_source_paths(project_root, wiki_root, pages)
    frontmatter_schema = check_frontmatter_schema(wiki_root, pages)
    missing_sections = check_required_sections(wiki_root, pages)
    backlink_map = compute_backlinks(project_root, wiki_root, pages)
    backlinks_missing, backlinks_stale = check_backlinks(wiki_root, pages, backlink_map)
    contradictions = check_contradictions_ledger(wiki_root)
    contradictions_issue = 1 if (not contradictions["present"] or contradictions["issues"]) else 0
    open_questions = check_open_questions_ledger(wiki_root)
    open_questions_issue = 1 if (not open_questions["present"] or open_questions["issues"]) else 0
    total_issues = (
        len(orphans)
        + len(stale)
        + len(no_sources)
        + len(mismatch)
        + len(broken_links)
        + len(missing_source_paths)
        + len(frontmatter_schema)
        + len(missing_sections)
        + len(backlinks_missing)
        + len(backlinks_stale)
        + contradictions_issue
        + open_questions_issue
    )

    return {
        "checked_at": date.today().isoformat(),
        "project_root": project_root.as_posix(),
        "wiki_root": wiki_root.as_posix(),
        "pages_scanned": len(pages),
        "orphan": orphans,
        "stale": stale,
        "no_sources": no_sources,
        "log_index_mismatch": mismatch,
        "broken_links": broken_links,
        "missing_source_paths": missing_source_paths,
        "frontmatter_schema": frontmatter_schema,
        "missing_sections": missing_sections,
        "backlinks_missing": backlinks_missing,
        "backlinks_stale": backlinks_stale,
        "contradictions": contradictions,
        "open_questions": open_questions,
        "total_issues": total_issues,
    }


def strip_frontmatter(content: str) -> str:
    if not content.startswith("---"):
        return content
    end = content.find("\n---", 3)
    if end == -1:
        return content
    return content[end + 4 :].lstrip()


def extract_title(content: str, fallback: str) -> str:
    body = strip_frontmatter(content)
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def extract_headings(content: str) -> list[str]:
    return [line.lstrip("#").strip() for line in strip_frontmatter(content).splitlines() if line.startswith("#")]


def query_terms(query: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", query.casefold()).strip()
    return [term for term in normalized.split(" ") if term]


def score_text(text: str, terms: list[str], weight: int) -> tuple[int, list[str]]:
    haystack = text.casefold()
    score = 0
    matches: list[str] = []
    for term in terms:
        count = haystack.count(term)
        if count <= 0:
            continue
        score += count * weight
        matches.append(term)
    return score, matches


def make_snippet(content: str, terms: list[str]) -> str:
    body = re.sub(r"\s+", " ", strip_frontmatter(content)).strip()
    if not body:
        return ""
    lowered = body.casefold()
    hit_positions = [lowered.find(term) for term in terms if lowered.find(term) >= 0]
    start = max(min(hit_positions) - 60, 0) if hit_positions else 0
    snippet = body[start : start + SEARCH_SNIPPET_CHARS].strip()
    if start > 0:
        snippet = "..." + snippet
    if start + SEARCH_SNIPPET_CHARS < len(body):
        snippet += "..."
    return snippet


def search_wiki(wiki_root: Path, query: str, limit: int) -> dict[str, Any]:
    terms = query_terms(query)
    phrase = re.sub(r"\s+", " ", query.casefold()).strip()
    results: list[dict[str, Any]] = []

    for page in get_search_pages(wiki_root):
        try:
            content = page.read_text(encoding="utf-8")
        except OSError:
            continue
        frontmatter = parse_frontmatter(page)
        path = rel(wiki_root, page)
        title = extract_title(content, fallback=page.stem)
        headings = " ".join(extract_headings(content))
        metadata = " ".join(
            str(value)
            for key, value in frontmatter.items()
            if key in {"type", "domain", "tags", "aliases", "sources"}
        )

        score = 0
        all_matches: list[str] = []
        for text, weight in [
            (path, 12),
            (title, 10),
            (metadata, 8),
            (headings, 6),
            (content, 1),
        ]:
            partial_score, matches = score_text(text, terms, weight)
            score += partial_score
            all_matches.extend(matches)

        if phrase and phrase in content.casefold():
            score += 20

        if score <= 0:
            continue

        results.append(
            {
                "path": path,
                "title": title,
                "type": frontmatter.get("type"),
                "domain": frontmatter.get("domain"),
                "score": score,
                "matches": sorted(set(all_matches)),
                "snippet": make_snippet(content, terms),
            }
        )

    results.sort(key=lambda item: (-int(item["score"]), str(item["path"])))
    return {
        "query": query,
        "wiki_root": wiki_root.as_posix(),
        "results": results[:limit],
        "total_matches": len(results),
    }


def command_lint(args: argparse.Namespace) -> int:
    wiki_root = resolve_wiki_root(args.root, args.wiki)
    if not wiki_root.exists():
        print(json.dumps({"error": f"wiki root not found: {wiki_root}"}, ensure_ascii=False), file=sys.stderr)
        return 1

    project_root = infer_project_root(wiki_root, args.root)
    result = build_lint_result(project_root, wiki_root, args.stale_days)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def apply_backlinks(
    project_root: Path,
    wiki_root: Path,
    insert_missing: bool,
    dry_run: bool,
) -> dict[str, Any]:
    pages = get_wiki_pages(wiki_root)
    backlink_map = compute_backlinks(project_root, wiki_root, pages)
    updated: list[str] = []
    inserted: list[str] = []
    skipped_no_marker: list[str] = []

    for page in pages:
        page_rel = rel(wiki_root, page)
        inbound = backlink_map.get(page_rel, [])
        try:
            content = page.read_text(encoding="utf-8")
        except OSError:
            continue
        new_block = render_backlink_block(wiki_root, page, inbound)
        match = BACKLINK_BLOCK_RE.search(content)
        if match:
            if match.group(0) == new_block:
                continue
            new_content = content[: match.start()] + new_block + content[match.end() :]
            if not dry_run:
                page.write_text(new_content, encoding="utf-8")
            updated.append(page_rel)
            continue
        if not inbound:
            continue
        if not insert_missing:
            skipped_no_marker.append(page_rel)
            continue
        trailing = "" if content.endswith("\n") else "\n"
        new_content = content + trailing + "\n" + new_block + "\n"
        if not dry_run:
            page.write_text(new_content, encoding="utf-8")
        inserted.append(page_rel)

    return {
        "wiki_root": wiki_root.as_posix(),
        "dry_run": dry_run,
        "updated": updated,
        "inserted": inserted,
        "skipped_no_marker": skipped_no_marker,
    }


def command_backlinks(args: argparse.Namespace) -> int:
    wiki_root = resolve_wiki_root(args.root, args.wiki)
    if not wiki_root.exists():
        print(json.dumps({"error": f"wiki root not found: {wiki_root}"}, ensure_ascii=False), file=sys.stderr)
        return 1
    project_root = infer_project_root(wiki_root, args.root)
    result = apply_backlinks(project_root, wiki_root, args.insert, args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def command_search(args: argparse.Namespace) -> int:
    wiki_root = resolve_wiki_root(args.root, args.wiki)
    if not wiki_root.exists():
        print(json.dumps({"error": f"wiki root not found: {wiki_root}"}, ensure_ascii=False), file=sys.stderr)
        return 1

    result = search_wiki(wiki_root, args.query, args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Common tooling for the Family Core wiki layer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    lint_parser = subparsers.add_parser("lint", help="Run wiki health checks and print JSON")
    lint_parser.add_argument("--root", help="Project root. Default: current directory")
    lint_parser.add_argument("--wiki", help="Wiki root path. Default: data/wiki under --root")
    lint_parser.add_argument(
        "--stale-days",
        type=int,
        default=STALE_DAYS_DEFAULT,
        dest="stale_days",
        help=f"Days before a page is considered stale. Default: {STALE_DAYS_DEFAULT}",
    )
    lint_parser.set_defaults(func=command_lint)

    backlinks_parser = subparsers.add_parser(
        "backlinks",
        help="Regenerate backlink sections inside <!-- backlinks:auto --> markers",
    )
    backlinks_parser.add_argument("--root", help="Project root. Default: current directory")
    backlinks_parser.add_argument("--wiki", help="Wiki root path. Default: data/wiki under --root")
    backlinks_parser.add_argument(
        "--insert",
        action="store_true",
        help="Append a new marker block to pages with inbound links but no existing marker",
    )
    backlinks_parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Compute changes without writing files",
    )
    backlinks_parser.set_defaults(func=command_backlinks)

    search_parser = subparsers.add_parser("search", help="Search wiki pages and print ranked JSON results")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--root", help="Project root. Default: current directory")
    search_parser.add_argument("--wiki", help="Wiki root path. Default: data/wiki under --root")
    search_parser.add_argument("--limit", type=int, default=8, help="Maximum results to return. Default: 8")
    search_parser.set_defaults(func=command_search)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
