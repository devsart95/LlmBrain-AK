"""Catalog: indice de metadata de todas las paginas wiki."""
from __future__ import annotations
import json
from pathlib import Path

import frontmatter

from wikisearch.config import (
    WIKI_DIR, CATALOG_FILE, SNIPPETS_FILE, INDEX_DIR, EXCLUDED_FILES
)
from wikisearch.models import WikiPage, Snippet
from wikisearch.index import snippets as snippet_gen


def load_catalog() -> list[WikiPage]:
    if not CATALOG_FILE.exists():
        return []
    data = json.loads(CATALOG_FILE.read_text())
    return [WikiPage(**p) for p in data]


def load_snippets() -> dict[str, Snippet]:
    if not SNIPPETS_FILE.exists():
        return {}
    data = json.loads(SNIPPETS_FILE.read_text())
    return {k: Snippet(**v) for k, v in data.items()}


def save_catalog(pages: list[WikiPage]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    CATALOG_FILE.write_text(json.dumps([p.__dict__ for p in pages], default=str))


def save_snippets(snips: dict[str, Snippet]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    SNIPPETS_FILE.write_text(json.dumps(
        {k: v.__dict__ for k, v in snips.items()}, default=str
    ))


def scan_wiki_pages() -> list[Path]:
    if not WIKI_DIR.exists():
        return []
    return [
        p for p in WIKI_DIR.glob("*.md")
        if p.name not in EXCLUDED_FILES
    ]


def parse_page(path: Path) -> WikiPage:
    post = frontmatter.load(str(path))
    meta = post.metadata
    return WikiPage(
        filename=path.name,
        title=str(meta.get("title", path.stem)),
        type=str(meta.get("type", "concept")),
        tags=list(meta.get("tags", [])),
        sources=int(meta.get("sources", 0)),
        created=str(meta.get("created", "")),
        updated=str(meta.get("updated", "")),
        path=str(path),
    )


def build_full(verbose: bool = False) -> tuple[list[WikiPage], dict[str, Snippet]]:
    pages = []
    snips = {}
    for path in scan_wiki_pages():
        if verbose:
            print(f"  indexando {path.name}")
        page = parse_page(path)
        pages.append(page)
        snips[path.name] = snippet_gen.generate(path)
    save_catalog(pages)
    save_snippets(snips)
    return pages, snips


def stats(pages: list[WikiPage]) -> dict:
    by_type: dict[str, int] = {}
    by_tag: dict[str, int] = {}
    for p in pages:
        by_type[p.type] = by_type.get(p.type, 0) + 1
        for t in p.tags:
            by_tag[t] = by_tag.get(t, 0) + 1
    return {
        "total_pages": len(pages),
        "by_type": dict(sorted(by_type.items(), key=lambda x: -x[1])),
        "by_tag": dict(sorted(by_tag.items(), key=lambda x: -x[1])),
    }
