"""Indice BM25 sobre titulos + tags + snippets."""
from __future__ import annotations
import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

from wikisearch.config import BM25_FILE, INDEX_DIR
from wikisearch.models import Snippet


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+", text.lower())


def build(snippets: dict[str, Snippet]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    filenames = list(snippets.keys())
    corpus = [_tokenize(s.as_text()) for s in snippets.values()]
    # Guardar corpus tokenizado para rebuild sin re-parsear markdown
    BM25_FILE.write_text(json.dumps({
        "filenames": filenames,
        "corpus": corpus,
    }))


def load() -> tuple[BM25Okapi | None, list[str]]:
    if not BM25_FILE.exists():
        return None, []
    data = json.loads(BM25_FILE.read_text())
    filenames: list[str] = data["filenames"]
    corpus: list[list[str]] = data["corpus"]
    if not corpus:
        return None, []
    return BM25Okapi(corpus), filenames


def search(
    query: str,
    top_k: int = 20,
    restrict_to: list[str] | None = None,
) -> list[tuple[str, float]]:
    bm25, filenames = load()
    if bm25 is None:
        return []

    tokens = _tokenize(query)
    scores = bm25.get_scores(tokens)

    ranked = sorted(
        zip(filenames, scores),
        key=lambda x: -x[1],
    )

    if restrict_to is not None:
        restrict_set = set(restrict_to)
        ranked = [(f, s) for f, s in ranked if f in restrict_set]

    return [(f, s) for f, s in ranked[:top_k] if s > 0]
