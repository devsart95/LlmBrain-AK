"""Query planner — heuristicas deterministas, sin LLM."""
from __future__ import annotations
import re

from wikisearch.models import QueryPlan


# Patrones de comparacion
_COMPARE_RE = re.compile(
    r"(?:compar[ae]|diferencia|versus|vs\.?)\s+(.+?)\s+(?:con|y|vs\.?|versus)\s+(.+)",
    re.IGNORECASE,
)
_VS_RE = re.compile(r"(.+?)\s+vs\.?\s+(.+)", re.IGNORECASE)

# Patrones de tipo
_WHAT_IS_RE = re.compile(r"^(?:que es|what is|define|definicion de)\s+(.+)", re.IGNORECASE)
_WHO_IS_RE = re.compile(r"^(?:quien es|who is)\s+(.+)", re.IGNORECASE)
_OVERVIEW_RE = re.compile(r"^(?:resumen|overview|mapa|todo sobre|todo lo que sabe)\s+(.+)", re.IGNORECASE)

# Keywords de expansion
_EXPAND_KEYWORDS = re.compile(
    r"\b(?:detalle|completo|full|todo|explica|explique|profundidad|everything)\b",
    re.IGNORECASE,
)


def plan(query: str, hints: dict | None = None) -> QueryPlan:
    """
    Genera un QueryPlan a partir de la query.
    hints permite al agente MCP ser explicito sobre filtros:
        {"types": ["comparison"], "tags": ["rag"], "top_k": 3}
    """
    p = QueryPlan(raw_query=query, text_query=query.strip())

    # -- Hints explicitos del agente (maxima prioridad) --
    if hints:
        p.type_filter = hints.get("types", [])
        p.tag_filter = hints.get("tags", [])
        p.max_results = hints.get("top_k", 5)
        if p.type_filter or p.tag_filter:
            p.strategy = "metadata_only"
        else:
            p.strategy = "bm25"
        return p

    # -- Heuristicas --

    # Comparacion: "X vs Y", "compara X con Y"
    m = _COMPARE_RE.search(query) or _VS_RE.search(query)
    if m:
        p.type_filter = ["comparison"]
        p.tag_filter = [_slugify(m.group(1)), _slugify(m.group(2))]
        p.strategy = "metadata_only"
        return p

    # Definicion: "que es X"
    m = _WHAT_IS_RE.match(query)
    if m:
        p.type_filter = ["concept", "entity"]
        p.title_pattern = m.group(1).strip()
        p.strategy = "bm25"
        return p

    # Persona: "quien es X"
    m = _WHO_IS_RE.match(query)
    if m:
        p.type_filter = ["person"]
        p.title_pattern = m.group(1).strip()
        p.strategy = "bm25"
        return p

    # Overview: "resumen de X", "todo sobre X"
    m = _OVERVIEW_RE.match(query)
    if m:
        p.type_filter = ["overview", "analysis"]
        p.tag_filter = [_slugify(m.group(1))]
        p.strategy = "metadata_only"
        return p

    # Busqueda con expansion explicita
    if _EXPAND_KEYWORDS.search(query):
        p.strategy = "semantic"
        p.max_results = 3
        return p

    # Fallback: BM25 sobre la query completa
    p.strategy = "bm25"
    return p


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")
