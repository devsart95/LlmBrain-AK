"""Etapa 3: re-ranking semantico — solo cuando BM25 no es suficiente."""
from __future__ import annotations

import numpy as np

from wikisearch.index import vectors as vec_index
from wikisearch.models import ScoredResult


# Peso del score semantico vs BM25 en la combinacion final
_SEMANTIC_WEIGHT = 0.6
_BM25_WEIGHT = 0.4


def rerank(
    query: str,
    candidates: list[ScoredResult],
    top_k: int = 5,
) -> list[ScoredResult]:
    if not candidates:
        return []

    vecs, filenames = vec_index.load()
    if vecs is None:
        # Embeddings no disponibles — devolver orden BM25
        return candidates[:top_k]

    fn_to_idx = {fn: i for i, fn in enumerate(filenames)}
    query_vec = vec_index.encode_query(query)

    # Normalizar scores BM25 al rango [0, 1]
    bm25_scores = np.array([r.score for r in candidates])
    max_bm25 = bm25_scores.max()
    bm25_norm = bm25_scores / max_bm25 if max_bm25 > 0 else bm25_scores

    # Calcular similitud coseno solo para los candidatos
    indexed = [r for r in candidates if r.filename in fn_to_idx]
    missing = len(candidates) - len(indexed)
    if missing:
        import sys
        print(f"[wikisearch] warning: {missing} resultado(s) sin vector — ejecuta 'wiki index'", file=sys.stderr)

    if not indexed:
        return candidates[:top_k]

    candidate_vecs = np.array([vecs[fn_to_idx[r.filename]] for r in indexed])

    sem_scores = vec_index.cosine_similarity(query_vec, candidate_vecs)
    sem_norm = (sem_scores + 1) / 2  # mapear [-1,1] a [0,1]

    final_scores = _BM25_WEIGHT * bm25_norm[:len(sem_norm)] + _SEMANTIC_WEIGHT * sem_norm

    reranked = [
        ScoredResult(
            filename=r.filename,
            score=float(final_scores[i]),
            snippet=r.snippet,
        )
        for i, r in enumerate(indexed[:len(sem_norm)])
    ]

    reranked.sort(key=lambda x: -x.score)
    return reranked[:top_k]
