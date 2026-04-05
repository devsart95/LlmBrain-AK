"""CLI: wiki search / get / index / lint / tags"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import click

from wikisearch.config import WIKI_DIR, SOURCES_DIR


@click.group()
def main():
    """wikisearch — busqueda token-eficiente para tu wiki LlmBrain."""
    pass


@main.command()
@click.argument("query")
@click.option("--type", "-t", "types", multiple=True, help="Filtrar por tipo de pagina.")
@click.option("--tag", "-g", "tags", multiple=True, help="Filtrar por tag.")
@click.option("--top", "-n", default=5, show_default=True, help="Numero de resultados.")
@click.option("--strategy", type=click.Choice(["auto", "metadata_only", "bm25", "semantic", "full"]), default="auto")
@click.option("--json", "output_json", is_flag=True, help="Output JSON (para el agente).")
def search(query, types, tags, top, strategy, output_json):
    """Busca en la wiki. Devuelve snippets comprimidos."""
    from wikisearch.search import planner, pipeline
    from wikisearch.sync import needs_sync, sync

    # Sincronizacion automatica si el indice esta desactualizado
    if needs_sync():
        sync(verbose=not output_json)

    hints = {}
    if types:
        hints["types"] = list(types)
    if tags:
        hints["tags"] = list(tags)
    if top:
        hints["top_k"] = top

    plan = planner.plan(query, hints if hints else None)

    if strategy != "auto":
        plan.strategy = strategy

    plan.max_results = top
    response = pipeline.search(plan)

    if output_json:
        click.echo(json.dumps(response.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_search_response(response)


@main.command()
@click.argument("filename")
@click.option("--snippet", is_flag=True, help="Solo mostrar el snippet comprimido.")
def get(filename, snippet):
    """Lee el contenido de una pagina wiki."""
    from wikisearch.index import catalog as cat

    path = WIKI_DIR / filename
    if not path.exists():
        click.echo(f"Error: {filename} no existe en wiki/", err=True)
        sys.exit(1)

    if snippet:
        snips = cat.load_snippets()
        snip = snips.get(filename)
        if snip:
            click.echo(json.dumps(snip.__dict__, ensure_ascii=False, indent=2))
        else:
            click.echo(f"Snippet no encontrado para {filename}. Ejecuta: wiki index", err=True)
    else:
        click.echo(path.read_text())


@main.command("index")
@click.option("--rebuild", is_flag=True, help="Reconstruir indice completo desde cero.")
@click.option("--stats", is_flag=True, help="Mostrar estadisticas del indice.")
@click.option("--json", "output_json", is_flag=True)
def index_cmd(rebuild, stats, output_json):
    """Construye o actualiza el indice de busqueda."""
    from wikisearch.index import catalog as cat
    from wikisearch.sync import sync

    result = sync(force=rebuild, verbose=not output_json)

    if stats or output_json:
        pages = cat.load_catalog()
        stat_data = {**result, **cat.stats(pages)}
        if output_json:
            click.echo(json.dumps(stat_data, ensure_ascii=False, indent=2))
        else:
            _print_stats(stat_data)
    else:
        added = result["added"]
        modified = result["modified"]
        removed = result["removed"]
        unchanged = result["unchanged"]
        click.echo(
            f"Indice actualizado — +"
            f"{added} agregadas, ~{modified} modificadas, "
            f"-{removed} eliminadas, {unchanged} sin cambios"
        )


@main.command()
@click.option("--json", "output_json", is_flag=True)
def tags(output_json):
    """Lista todos los tags con conteo de paginas."""
    from wikisearch.index import catalog as cat

    pages = cat.load_catalog()
    stats = cat.stats(pages)
    by_tag = stats["by_tag"]

    if output_json:
        click.echo(json.dumps(by_tag, ensure_ascii=False, indent=2))
    else:
        click.echo(f"\n{'Tag':<30} {'Paginas':>7}")
        click.echo("-" * 40)
        for tag, count in sorted(by_tag.items(), key=lambda x: -x[1]):
            click.echo(f"{tag:<30} {count:>7}")


@main.command()
@click.option("--json", "output_json", is_flag=True)
def lint(output_json):
    """Health check de la wiki: huerfanas, contradicciones, gaps."""
    from wikisearch.index import catalog as cat

    pages = cat.load_catalog()
    snippets = cat.load_snippets()

    # Detectar paginas huerfanas (no referenciadas en conexiones de otras)
    all_titles = {p.title.lower() for p in pages}
    referenced: set[str] = set()
    for snip in snippets.values():
        for items in snip.connections.values():
            referenced.update(i.lower() for i in items)

    orphans = [p.filename for p in pages if p.title.lower() not in referenced]

    # Detectar conceptos referenciados sin pagina propia
    gaps = [ref for ref in referenced if not any(ref in t for t in all_titles)]

    # Paginas sin tags
    no_tags = [p.filename for p in pages if not p.tags]

    # Paginas sin fuentes
    no_sources = [p.filename for p in pages if p.sources == 0]

    report = {
        "total_pages": len(pages),
        "orphan_pages": sorted(orphans),
        "concept_gaps": sorted(set(gaps))[:20],
        "pages_without_tags": sorted(no_tags),
        "pages_without_sources": sorted(no_sources),
    }

    if output_json:
        click.echo(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_lint_report(report)


# --- Helpers de presentacion ---

def _print_search_response(response) -> None:
    click.echo(f"\nQuery: {response.query}")
    click.echo(f"Estrategia: {response.plan_strategy} | Etapas: {', '.join(response.stages_used)}")
    click.echo(f"Candidatos totales: {response.total_candidates} | Resultados: {len(response.results)}\n")

    for i, r in enumerate(response.results, 1):
        expand = " [leer completo recomendado]" if r.expand_recommended else ""
        click.echo(f"  [{i}] {r.snippet.title}{expand}")
        click.echo(f"       {r.filename} | {r.snippet.type} | tags: {', '.join(r.snippet.tags)}")
        if r.snippet.oneliner:
            click.echo(f"       {r.snippet.oneliner[:120]}")
        click.echo()


def _print_stats(data: dict) -> None:
    click.echo(f"\nTotal paginas: {data.get('total_pages', 0)}")
    click.echo(f"Agregadas: {data.get('added', 0)} | Modificadas: {data.get('modified', 0)} | "
               f"Eliminadas: {data.get('removed', 0)}")
    click.echo("\nPor tipo:")
    for t, n in data.get("by_type", {}).items():
        click.echo(f"  {t:<20} {n}")


def _print_lint_report(report: dict) -> None:
    click.echo(f"\nTotal paginas: {report['total_pages']}")
    _section("Paginas huerfanas (sin referencias entrantes)", report["orphan_pages"])
    _section("Conceptos referenciados sin pagina propia (gaps)", report["concept_gaps"])
    _section("Paginas sin tags", report["pages_without_tags"])
    _section("Paginas sin fuentes", report["pages_without_sources"])


def _section(title: str, items: list) -> None:
    click.echo(f"\n{title} ({len(items)}):")
    if items:
        for item in items[:10]:
            click.echo(f"  - {item}")
        if len(items) > 10:
            click.echo(f"  ... y {len(items) - 10} mas")
    else:
        click.echo("  ninguna")
