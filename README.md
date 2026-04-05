# LlmBrain-AK

[![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-5B21B6?style=flat-square)](https://claude.ai/code)
[![Agente](https://img.shields.io/badge/agente-cualquier_LLM-0EA5E9?style=flat-square)](#)
[![Patron](https://img.shields.io/badge/patron-Karpathy_LLM_Wiki-10B981?style=flat-square)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

**Una base de conocimiento personal mantenida por un agente LLM — no un chatbot, un segundo cerebro persistente.**

> Implementacion del patron [LLM Wiki de Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

---

## El problema con RAG

La mayoria usa los LLMs como buscadores: pregunta, respuesta, olvido. Los sistemas RAG tradicionales (NotebookLM, ChatGPT file uploads) redescubren el conocimiento desde cero en cada consulta. No acumulan nada.

> *"The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping."*
> — Andrej Karpathy

---

## La idea

En lugar de recuperar fragmentos al momento de la consulta, el LLM **construye y mantiene una wiki persistente** que se compone con el tiempo.

Cada vez que agregas una fuente, el agente no solo la indexa — la lee, discute los takeaways clave contigo, y actualiza 10-15 paginas relacionadas: resuelve contradicciones, completa gaps, refuerza cross-references. **El conocimiento se compila una vez y se mantiene actualizado**, no se re-deriva en cada query.

```
RAG tradicional:   fuente → chunks → vector store → recuperar en cada query
LlmBrain-AK:       fuente → dialogo → wiki persistente → consulta directa
```

---

## Arquitectura

```
LlmBrain-AK/
│
├── sources/               # Fuentes crudas — inmutables, verdad de origen
│   ├── articulo.md        # Papers, articulos, notas, transcripciones
│   └── assets/            # Imagenes descargadas localmente
│
├── wiki/                  # Paginas generadas por el LLM — el agente es dueno de esta capa
│   ├── _template.md       # Template con frontmatter para nuevas paginas
│   └── concepto-a.md      # Una pagina por entidad, concepto o tema
│
├── index.md               # Catalogo de contenido — se actualiza en cada ingest
├── log.md                 # Registro cronologico append-only de toda actividad
├── CLAUDE.md              # Schema operativo para Claude Code
├── AGENTS.md              # Schema operativo para otros agentes (Codex, OpenCode)
└── SETUP.md               # Guia de inicializacion para nuevos dominios
```

**Regla fundamental:** el humano escribe en `sources/`. El LLM escribe en `wiki/`. Nunca al reves.

---

## Flujo del sistema

```mermaid
flowchart LR
    H([Human])
    W[(wiki/)]
    IDX[index.md]
    LOG[log.md]

    H -->|deposita fuente| IG[INGEST]
    IG -->|discute takeaways| H
    IG --> W
    IG --> IDX
    IG --> LOG

    H -->|hace pregunta| Q[QUERY]
    Q --> IDX
    IDX --> W
    W --> Q
    Q -->|respuesta + citas| H
    Q -.->|archiva si es valiosa| W

    H -->|pide health-check| L[LINT]
    L --> W
    L --> LOG
    L -->|sugiere fuentes nuevas| H
```

---

## Las tres operaciones

### `INGEST` — agregar una fuente nueva

```
"ingest sources/articulo.md"
```

1. El agente lee la fuente completa
2. **Discute los takeaways clave contigo** — confirma que enfatizar antes de escribir
3. Crea la pagina de resumen en `wiki/`
4. Actualiza 10-15 paginas relacionadas (entidades, conceptos, comparaciones)
5. Actualiza `index.md` y registra en `log.md`

El ingest es un dialogo, no un proceso batch silencioso.

---

### `QUERY` — consultar la wiki

```
"que dice la wiki sobre X?"
"compara A con B"
"genera un resumen ejecutivo de todo lo que se sabe sobre Y"
```

1. `wiki_search(query)` — recupera snippets comprimidos sin leer archivos
2. `wiki_get(filename)` — lee solo las paginas que realmente necesitas
3. Sintetiza respuesta con citas
4. **Archiva la respuesta como nueva pagina wiki** si es valiosa — las exploraciones componen el conocimiento igual que las fuentes

Formatos de salida disponibles segun la consulta:

| Formato | Cuando usarlo |
|---------|--------------|
| Pagina markdown | respuesta narrativa, analisis |
| Tabla comparativa | contrastar conceptos o entidades |
| Slide deck (Marp) | presentar hallazgos |
| Chart (matplotlib) | datos cuantitativos |
| Canvas / overview | mapa del dominio completo |

---

### `LINT` — health check de la wiki

```
"lint the wiki"
```

**Deteccion:**
- Paginas huerfanas (sin links entrantes)
- Afirmaciones contradictorias entre paginas
- Claims desactualizados por fuentes mas recientes
- Conceptos referenciados pero sin pagina propia
- Data gaps resolubles con una busqueda web

**Proactivo:**
- Sugiere nuevas preguntas que la wiki aun no responde
- Sugiere nuevas fuentes a buscar para cubrir los gaps
- Genera reporte completo en `log.md`

---

## Quickstart

```bash
# 1. Clonar
git clone https://github.com/devsart95/LlmBrain-AK
cd LlmBrain-AK

# 2. Instalar el modulo de busqueda
pip install -e .

# 3. Leer SETUP.md y configurar el dominio
# Editar CLAUDE.md con tus categorias

# 4. Abrir con Claude Code (carga el MCP automaticamente via .mcp.json)
claude .

# 5. Cambiar a Opus para operaciones profundas
/model opus

# 6. Primer ingest
# Depositar un archivo en sources/, luego:
# "ingest sources/mi-articulo.md"

# 7. Consultar — el agente usa wiki_search() automaticamente
# "que dice la wiki sobre X?"

# 8. Mantenimiento periodico
# "lint the wiki"
```

Ver `SETUP.md` para la guia completa de inicializacion.

---

## Asignacion de modelos

| Operacion | Modelo | Razon |
|-----------|--------|-------|
| Ingest | **Opus** | Razonamiento profundo, conexiones entre conceptos |
| Lint | **Opus** | Deteccion de contradicciones, sugerencias proactivas |
| Query | **Opus** | Sintesis multi-fuente |
| Busqueda / lectura | **Sonnet** | Rapido y eficiente para recuperar contexto |

---

## Motor de busqueda — `wikisearch`

A medida que la wiki crece, el agente no puede leer todo para responder una pregunta. Una wiki de 500 paginas tiene `index.md` solo con ~15,000 tokens. Leer 10 paginas para responder algo simple son otros ~15,000. El costo se vuelve prohibitivo.

`wikisearch` es el modulo Python incluido en el repo que resuelve esto.

### Que resuelve

**Sin modulo:** el agente lee `index.md` + las paginas que parecen relevantes — entre 10,000 y 18,000 tokens por query tipica.

**Con modulo:** el agente recibe snippets comprimidos (~150 tokens cada uno) y solo llama `wiki_get()` para las paginas que realmente necesita leer. **~2,700 tokens por query tipica. 85% menos.**

### Como funciona

Pipeline de 3 etapas con early exit — sale en la etapa mas barata que sea suficiente:

```
Etapa 1 — MetaFilter    filtra por frontmatter YAML (type, tags, title)
                         costo: 0ms, 0 tokens
                         500 paginas → 10-30 candidatos

Etapa 2 — BM25          ranking lexical sobre titulos + tags + snippets
                         costo: <5ms, sin API, sin embeddings
                         30 candidatos → top-10

Etapa 3 — SemanticRerank similitud coseno sobre embeddings precalculados
                         costo: ~50ms en CPU, sin API externa
                         top-10 → top-5 reordenados por relevancia semantica
```

Si la etapa 1 devuelve 1-3 resultados claros, no se ejecutan las siguientes. La mayoria de queries con filtros explicitos (`types=["comparison"]`) terminan en etapa 1.

### Tecnologia

| Componente | Libreria | Detalle |
|------------|----------|---------|
| BM25 | `rank-bm25` | Algoritmo BM25Okapi sobre corpus tokenizado en disco |
| Embeddings | `sentence-transformers` | Modelo `gte-small` (33M params, 384 dims, ~67MB, 100% local) |
| Similitud | `numpy` | Cosine similarity sobre matriz `.npz` — sin vector DB |
| Frontmatter | `python-frontmatter` | Parseo de YAML en cada pagina wiki |
| CLI | `click` | `wiki search`, `wiki get`, `wiki tags`, `wiki lint`, `wiki index` |
| MCP Server | `fastmcp` | 4 tools disponibles directamente en Claude Code |

Sin servidor. Sin API externa. Todo corre en CPU local.

### Uso

```bash
# Instalar
pip install -e .

# Construir el indice (primera vez — ~55s por descarga del modelo)
wiki index

# Buscar
wiki search "RAG vs LLM Wiki"
wiki search "arquitectura" --type concept --top 3

# Leer una pagina especifica
wiki get ejemplo-rag-vs-llm-wiki.md

# Explorar el dominio antes de buscar
wiki tags

# Health check
wiki lint
```

### MCP en Claude Code

El archivo `.mcp.json` en la raiz del repo configura el servidor automaticamente. Al abrir el proyecto con `claude .`, el agente tiene disponibles estas tools nativas:

| Tool | Que hace |
|------|----------|
| `wiki_search(query, types, tags)` | Devuelve snippets, no paginas completas |
| `wiki_get(filename)` | Lee una pagina especifica — usar solo cuando el snippet no alcanza |
| `wiki_tags()` | Lista tags con conteo — para explorar el dominio antes de buscar |
| `wiki_index(rebuild)` | Sincroniza el indice despues de un ingest |

### Indice incremental

El indice se actualiza automaticamente cuando el agente llama `wiki_index()` al final de cada ingest. Compara `mtime` + `size` de cada archivo y solo re-indexa lo que cambio. Un ingest tipico (15 paginas nuevas) tarda ~800ms en sincronizar.

---

## Herramientas opcionales

| Herramienta | Funcion |
|-------------|---------|
| [Obsidian](https://obsidian.md) | Graph view para visualizar conexiones entre paginas, renderiza `[[wiki-links]]` |
| [Obsidian Web Clipper](https://obsidian.md/clipper) | Convierte articulos web a markdown antes del ingest |
| [Marp](https://marp.app) | Presentaciones desde paginas wiki en markdown |
| [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) | Queries dinamicas sobre el frontmatter YAML de las paginas |

---

## Privacidad

`sources/` y `wiki/` contienen tu conocimiento personal. Si el contenido es sensible, agregar al `.gitignore`:

```gitignore
sources/**/*.pdf
sources/**/*.md
wiki/*.md
!wiki/_template.md
!wiki/.gitkeep
```

Los archivos de framework (`CLAUDE.md`, `AGENTS.md`, `index.md`, `log.md`, `SETUP.md`) no contienen datos personales.

---

## Nota

Este repositorio es intencionalmente un punto de partida, no un framework rigido. La estructura de directorios, las convenciones de las paginas, el schema del agente — todo depende de tu dominio y tus preferencias. Tomar lo que sirve, ignorar lo que no. El agente puede ayudarte a adaptar el sistema desde el primer dia.

---

## Creditos

Patron original por [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
Implementacion por [devsart95](https://github.com/devsart95) — Paraguay
