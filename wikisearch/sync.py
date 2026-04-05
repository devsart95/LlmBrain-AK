"""Sincronizacion incremental del indice — lazy rebuild, sin watcher."""
from __future__ import annotations
import json
import os
from pathlib import Path

from wikisearch.config import INDEX_DIR, MANIFEST_FILE, WIKI_DIR, EXCLUDED_FILES
from wikisearch.index import bm25 as bm25_idx
from wikisearch.index import catalog as cat
from wikisearch.index import snippets as snip_gen
from wikisearch.index import vectors as vec_idx


def _file_fingerprint(path: Path) -> tuple[float, int]:
    stat = path.stat()
    return stat.st_mtime, stat.st_size


def _load_manifest() -> dict[str, tuple[float, int]]:
    if not MANIFEST_FILE.exists():
        return {}
    raw = json.loads(MANIFEST_FILE.read_text())
    return {k: tuple(v) for k, v in raw.items()}


def _save_manifest(manifest: dict[str, tuple[float, int]]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps({k: list(v) for k, v in manifest.items()}))


def needs_sync() -> bool:
    manifest = _load_manifest()
    current = {
        p.name: _file_fingerprint(p)
        for p in cat.scan_wiki_pages()
    }
    return current != manifest


def sync(force: bool = False, verbose: bool = False) -> dict:
    """
    Sincroniza el indice incrementalmente.
    Devuelve stats: {added, modified, removed, unchanged}.
    """
    INDEX_DIR.mkdir(exist_ok=True)

    manifest = _load_manifest()
    pages = cat.scan_wiki_pages()
    current: dict[str, tuple[float, int]] = {p.name: _file_fingerprint(p) for p in pages}

    if not force:
        added = {n for n in current if n not in manifest}
        removed = {n for n in manifest if n not in current}
        modified = {
            n for n in current
            if n in manifest and current[n] != manifest[n]
        }
        unchanged = set(current) - added - modified
    else:
        added = set(current)
        removed = set()
        modified = set()
        unchanged = set()

    if not (added or removed or modified) and not force:
        return {"added": 0, "modified": 0, "removed": 0, "unchanged": len(unchanged)}

    # Cargar estado actual del indice
    catalog_pages = {p.filename: p for p in cat.load_catalog()}
    snippet_map = cat.load_snippets()

    # Procesar cambios
    for filename in added | modified:
        path = WIKI_DIR / filename
        if verbose:
            action = "+" if filename in added else "~"
            print(f"  {action} {filename}")
        page = cat.parse_page(path)
        snip = snip_gen.generate(path)
        catalog_pages[filename] = page
        snippet_map[filename] = snip

    for filename in removed:
        if verbose:
            print(f"  - {filename}")
        catalog_pages.pop(filename, None)
        snippet_map.pop(filename, None)

    # Guardar catalog y snippets
    cat.save_catalog(list(catalog_pages.values()))
    cat.save_snippets(snippet_map)

    # Reconstruir BM25 (rapido — corpus en memoria)
    bm25_idx.build(snippet_map)

    # Actualizar vectores solo si hubo cambios
    if added or modified or removed:
        if verbose:
            print("  recalculando embeddings...")
        vec_idx.build(snippet_map)

    _save_manifest(current)

    return {
        "added": len(added),
        "modified": len(modified),
        "removed": len(removed),
        "unchanged": len(unchanged),
    }
