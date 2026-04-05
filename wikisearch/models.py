from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class WikiPage:
    filename: str
    title: str
    type: str
    tags: list[str]
    sources: int
    created: str
    updated: str
    path: str


@dataclass
class Snippet:
    filename: str
    title: str
    type: str
    tags: list[str]
    sources: int
    updated: str
    oneliner: str
    headers: list[str]
    connections: dict[str, list[str]]
    first_sentences: dict[str, str]

    def as_text(self) -> str:
        """Texto plano para indexacion BM25/embeddings."""
        parts = [self.title]
        parts.extend(self.tags)
        if self.oneliner:
            parts.append(self.oneliner)
        parts.extend(self.first_sentences.values())
        for items in self.connections.values():
            parts.extend(items)
        return " ".join(parts)

    def token_estimate(self) -> int:
        return len(self.as_text().split()) * 4 // 3


@dataclass
class QueryPlan:
    raw_query: str
    text_query: str
    type_filter: list[str] = field(default_factory=list)
    tag_filter: list[str] = field(default_factory=list)
    title_pattern: str | None = None
    date_range: tuple[str, str] | None = None
    strategy: Literal["metadata_only", "bm25", "semantic", "full"] = "bm25"
    max_results: int = 5


@dataclass
class ScoredResult:
    filename: str
    score: float
    snippet: Snippet
    expand_recommended: bool = False


@dataclass
class SearchResponse:
    query: str
    plan_strategy: str
    plan_filters: dict
    stages_used: list[str]
    total_candidates: int
    results: list[ScoredResult]

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "plan": {
                "strategy": self.plan_strategy,
                "filters": self.plan_filters,
            },
            "stages_used": self.stages_used,
            "total_candidates": self.total_candidates,
            "results_count": len(self.results),
            "results": [
                {
                    "rank": i + 1,
                    "score": round(r.score, 4),
                    "filename": r.filename,
                    "expand_recommended": r.expand_recommended,
                    "snippet": {
                        "title": r.snippet.title,
                        "type": r.snippet.type,
                        "tags": r.snippet.tags,
                        "sources": r.snippet.sources,
                        "updated": r.snippet.updated,
                        "oneliner": r.snippet.oneliner,
                        "headers": r.snippet.headers,
                        "connections": r.snippet.connections,
                        "first_sentences": r.snippet.first_sentences,
                    },
                }
                for i, r in enumerate(self.results)
            ],
        }
