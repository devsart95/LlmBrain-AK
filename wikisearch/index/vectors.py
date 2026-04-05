"""Embeddings locales con sentence-transformers — cero API externa."""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np

from wikisearch.config import VECTORS_FILE, EMBEDDING_MODEL, INDEX_DIR
from wikisearch.models import Snippet


_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def build(snippets: dict[str, Snippet]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    if not snippets:
        return
    model = _get_model()
    filenames = list(snippets.keys())
    texts = [s.as_text() for s in snippets.values()]
    vecs = model.encode(texts, show_progress_bar=True, batch_size=32)
    np.savez_compressed(
        VECTORS_FILE,
        vectors=vecs.astype(np.float32),
        filenames=np.array(filenames),
    )


def load() -> tuple[np.ndarray | None, list[str]]:
    if not VECTORS_FILE.exists():
        return None, []
    data = np.load(str(VECTORS_FILE), allow_pickle=True)
    return data["vectors"], list(data["filenames"])


def encode_query(query: str) -> np.ndarray:
    model = _get_model()
    return model.encode([query])[0].astype(np.float32)


def cosine_similarity(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    q = query_vec / (np.linalg.norm(query_vec) + 1e-10)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-10
    return (matrix / norms) @ q
