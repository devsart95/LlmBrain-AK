"""Pipeline de 3 etapas con early exit — el agente recibe solo lo necesario."""
from __future__ import annotations

from wikisearch.index import catalog as cat
from wikisearch.models import QueryPlan, SearchResponse, ScoredResult, Snippet
from wikisearch.search import bm25_rank, meta_filter, reranker


# Si metadata_only devuelve <= este numero, no se necesita BM25
_META_ONLY_THRESHOLD = 5

# Si el top BM25 score es >2x el ultimo, los resultados son claros — no reranquear
_BM25_CLEAR_RATIO = 2.0


def search(plan: QueryPlan) -> SearchResponse:
    pages = cat.load_catalog()
    snippets = cat.load_snippets()
    stages_used: list[str] = []

    # -- Etapa 1: filtro por metadata (siempre) --
    stages_used.append("meta_filter")
    candidates = meta_filter.filter_pages(pages, plan)
    candidate_fns = [p.filename for p in candidates]

    # Early exit: metadata_only con pocos resultados
    if plan.strategy == "metadata_only" and len(candidates) <= _META_ONLY_THRESHOLD:
        results = _pages_to_results(candidates, snippets, base_score=1.0)
        return _build_response(plan, stages_used, len(candidates), results)

    # -- Etapa 2: BM25 --
    stages_used.append("bm25")
    restrict = candidate_fns if candidates else None
    bm25_results = bm25_rank.rank(
        plan.text_query,
        snippets,
        restrict_to=restrict,
        top_k=min(plan.max_results * 4, 20),
    )

    if not bm25_results:
        # Sin resultados BM25 — devolver metadata candidates
        results = _pages_to_results(candidates[:plan.max_results], snippets)
        return _build_response(plan, stages_used, len(candidates), results)

    # Early exit: BM25 con resultado claramente dominante
    if (
        plan.strategy not in ("semantic", "full")
        and len(bm25_results) > 1
        and bm25_results[0].score > _BM25_CLEAR_RATIO * bm25_results[-1].score
    ):
        results = _mark_expand(bm25_results[:plan.max_results], plan)
        return _build_response(plan, stages_used, len(candidates), results)

    # Si BM25 devuelve pocos resultados tampoco necesitamos reranking
    if plan.strategy not in ("semantic", "full") and len(bm25_results) <= plan.max_results:
        results = _mark_expand(bm25_results, plan)
        return _build_response(plan, stages_used, len(candidates), results)

    # -- Etapa 3: reranking semantico --
    stages_used.append("semantic_rerank")
    reranked = reranker.rerank(plan.text_query, bm25_results, top_k=plan.max_results)
    results = _mark_expand(reranked, plan)
    return _build_response(plan, stages_used, len(candidates), results)


def _pages_to_results(
    pages: list,
    snippets: dict[str, Snippet],
    base_score: float = 0.5,
) -> list[ScoredResult]:
    results = []
    for p in pages:
        snip = snippets.get(p.filename)
        if snip:
            results.append(ScoredResult(filename=p.filename, score=base_score, snippet=snip))
    return results


def _mark_expand(results: list[ScoredResult], plan: QueryPlan) -> list[ScoredResult]:
    """Marcar expand_recommended cuando hay 1-2 resultados de alta confianza."""
    if len(results) <= 2 and results:
        for r in results:
            r.expand_recommended = True
    return results


def _build_response(
    plan: QueryPlan,
    stages_used: list[str],
    total_candidates: int,
    results: list[ScoredResult],
) -> SearchResponse:
    return SearchResponse(
        query=plan.raw_query,
        plan_strategy=plan.strategy,
        plan_filters={
            "type_filter": plan.type_filter,
            "tag_filter": plan.tag_filter,
            "title_pattern": plan.title_pattern,
        },
        stages_used=stages_used,
        total_candidates=total_candidates,
        results=results,
    )
