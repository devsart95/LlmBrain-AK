"""MCP Server — 4 tools para el agente LLM."""
from __future__ import annotations
import json

from fastmcp import FastMCP

from wikisearch.config import WIKI_DIR
from wikisearch.index import catalog as cat
from wikisearch.search import pipeline, planner
from wikisearch.sync import needs_sync, sync

mcp = FastMCP(
    name="wikisearch",
    instructions=(
        "Herramientas de busqueda para la wiki LlmBrain. "
        "NUNCA leer wiki/ manualmente — usar estas tools. "
        "Flujo optimo: wiki_tags() → wiki_search() → wiki_get() solo si necesario."
    ),
)


@mcp.tool()
def wiki_search(
    query: str,
    types: list[str] | None = None,
    tags: list[str] | None = None,
    top_k: int = 5,
) -> str:
    """
    Busca en la wiki. Devuelve snippets comprimidos (~150 tokens por resultado).
    NO devuelve paginas completas — usar wiki_get() para eso.

    Args:
        query: La pregunta o termino a buscar.
        types: Filtrar por tipo. Valores: concept, entity, person, comparison, analysis, overview.
        tags: Filtrar por tags (lista de strings).
        top_k: Numero de resultados (default 5, max 10).
    """
    _maybe_sync()
    hints = {}
    if types:
        hints["types"] = types
    if tags:
        hints["tags"] = tags
    hints["top_k"] = min(top_k, 10)

    plan = planner.plan(query, hints if hints else None)
    plan.max_results = hints["top_k"]
    response = pipeline.search(plan)
    return json.dumps(response.to_dict(), ensure_ascii=False)


@mcp.tool()
def wiki_get(filename: str) -> str:
    """
    Lee el contenido completo de una pagina wiki.
    Usar solo despues de wiki_search() para las paginas que realmente necesitas.

    Args:
        filename: Nombre del archivo (e.g. 'ejemplo-rag-vs-llm-wiki.md')
    """
    path = WIKI_DIR / filename
    if not path.exists():
        return f"ERROR: {filename} no existe en wiki/"
    return path.read_text()


@mcp.tool()
def wiki_tags() -> str:
    """
    Lista todos los tags de la wiki con conteo de paginas.
    Usar antes de wiki_search() para explorar el dominio disponible.
    Costo: ~200 tokens de respuesta.
    """
    _maybe_sync()
    pages = cat.load_catalog()
    stats = cat.stats(pages)
    return json.dumps({
        "total_pages": stats["total_pages"],
        "by_type": stats["by_type"],
        "by_tag": stats["by_tag"],
    }, ensure_ascii=False)


@mcp.tool()
def wiki_index(rebuild: bool = False) -> str:
    """
    Sincroniza el indice de busqueda con el estado actual de wiki/.
    Llamar al final de cada operacion INGEST.

    Args:
        rebuild: Si True, reconstruye el indice completo desde cero.
    """
    result = sync(force=rebuild, verbose=False)
    pages = cat.load_catalog()
    stats = cat.stats(pages)
    return json.dumps({**result, **stats}, ensure_ascii=False)


def _maybe_sync() -> None:
    if needs_sync():
        sync(verbose=False)


if __name__ == "__main__":
    mcp.run()
