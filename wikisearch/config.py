from pathlib import Path
import os

# Raiz del repo — puede sobreescribirse con env var WIKI_ROOT
WIKI_ROOT = Path(os.environ.get("WIKI_ROOT", Path(__file__).parent.parent))

WIKI_DIR = WIKI_ROOT / "wiki"
SOURCES_DIR = WIKI_ROOT / "sources"
INDEX_DIR = WIKI_ROOT / ".wiki_index"

# Archivos del indice
CATALOG_FILE = INDEX_DIR / "catalog.json"
SNIPPETS_FILE = INDEX_DIR / "snippets.json"
VECTORS_FILE = INDEX_DIR / "vectors.npz"
BM25_FILE = INDEX_DIR / "bm25.json"
MANIFEST_FILE = INDEX_DIR / "manifest.json"

# Modelo de embeddings — local, sin API
EMBEDDING_MODEL = "thenlper/gte-small"
EMBEDDING_DIM = 384

# Parametros de busqueda
DEFAULT_TOP_K = 5
BM25_TOP_K = 20        # candidatos para reranking semantico
SNIPPET_MAX_CHARS = 800

# Paginas internas que no se indexan como wiki pages
EXCLUDED_FILES = {"_template.md"}
