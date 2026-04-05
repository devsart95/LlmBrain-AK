"""Genera snippets comprimidos de paginas wiki — sin LLM, solo heuristicas."""
from __future__ import annotations
import re
from pathlib import Path

import frontmatter

from wikisearch.config import SNIPPET_MAX_CHARS
from wikisearch.models import Snippet


_SKIP_SECTIONS = {"fuentes", "sources", "log de cambios", "changelog", "log"}
_BLOCKQUOTE_RE = re.compile(r"^>\s+(?!\*)(.+)$", re.MULTILINE)
_WIKI_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
_H2_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def generate(path: Path) -> Snippet:
    post = frontmatter.load(str(path))
    content: str = post.content
    meta = post.metadata

    return Snippet(
        filename=path.name,
        title=str(meta.get("title", path.stem)),
        type=str(meta.get("type", "concept")),
        tags=list(meta.get("tags", [])),
        sources=int(meta.get("sources", 0)),
        updated=str(meta.get("updated", "")),
        oneliner=_extract_oneliner(content),
        headers=_extract_headers(content),
        connections=_extract_connections(content),
        first_sentences=_extract_first_sentences(content),
    )


def _extract_oneliner(content: str) -> str:
    m = _BLOCKQUOTE_RE.search(content)
    if m:
        return m.group(1).strip()[:SNIPPET_MAX_CHARS]
    # fallback: primera linea no vacia que no sea heading
    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith(">"):
            return line[:SNIPPET_MAX_CHARS]
    return ""


def _extract_headers(content: str) -> list[str]:
    return _H2_RE.findall(content)


def _extract_connections(content: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {"related": [], "contrasts": [], "part_of": []}
    in_section = False
    for line in content.split("\n"):
        if re.match(r"^##\s+Conexiones", line, re.IGNORECASE):
            in_section = True
            continue
        if in_section and re.match(r"^##\s+", line):
            break
        if not in_section:
            continue
        items = _WIKI_LINK_RE.findall(line)
        if not items:
            continue
        ll = line.lower()
        if "relacionado" in ll:
            result["related"] = items
        elif "contrasta" in ll or "contrastar" in ll:
            result["contrasts"] = items
        elif "parte de" in ll:
            result["part_of"] = items
    return result


def _extract_first_sentences(content: str) -> dict[str, str]:
    result: dict[str, str] = {}
    current: str | None = None
    for line in content.split("\n"):
        if re.match(r"^##\s+", line):
            current = re.sub(r"^##\s+", "", line).strip()
            continue
        if current is None or current.lower() in _SKIP_SECTIONS:
            continue
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith(">"):
            if current not in result:
                result[current] = stripped[:300]
    return result
