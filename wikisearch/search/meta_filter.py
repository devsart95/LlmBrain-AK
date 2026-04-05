"""Etapa 1: filtro por metadata — costo cero en tokens y embeddings."""
from __future__ import annotations

from wikisearch.models import QueryPlan, WikiPage


def filter_pages(catalog: list[WikiPage], plan: QueryPlan) -> list[WikiPage]:
    candidates = catalog

    if plan.type_filter:
        candidates = [p for p in candidates if p.type in plan.type_filter]

    if plan.tag_filter:
        filter_set = set(plan.tag_filter)
        candidates = [
            p for p in candidates
            if any(t in filter_set or _slug_match(t, filter_set) for t in p.tags)
        ]

    if plan.title_pattern:
        pattern = plan.title_pattern.lower()
        candidates = [p for p in candidates if pattern in p.title.lower()]

    if plan.date_range:
        lo, hi = plan.date_range
        candidates = [p for p in candidates if lo <= p.updated <= hi]

    return candidates


def _slug_match(tag: str, filter_set: set[str]) -> bool:
    """Comparacion flexible: 'llm-wiki' matchea 'llm wiki' o 'LLM Wiki'."""
    normalized = tag.lower().replace(" ", "-")
    return any(
        normalized == f or normalized.startswith(f) or f.startswith(normalized)
        for f in filter_set
    )
