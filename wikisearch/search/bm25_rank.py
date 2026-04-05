"""Etapa 2: ranking BM25 sobre titulos + tags + snippets."""
from __future__ import annotations

from wikisearch.index import bm25 as bm25_index
from wikisearch.models import ScoredResult, Snippet


def rank(
    query: str,
    snippets: dict[str, Snippet],
    restrict_to: list[str] | None = None,
    top_k: int = 10,
) -> list[ScoredResult]:
    results = bm25_index.search(query, top_k=top_k * 2, restrict_to=restrict_to)

    scored = []
    for filename, score in results[:top_k]:
        snip = snippets.get(filename)
        if snip is None:
            continue
        scored.append(ScoredResult(
            filename=filename,
            score=float(score),
            snippet=snip,
        ))

    return scored
