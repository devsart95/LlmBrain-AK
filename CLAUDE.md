# LlmBrain — Schema

> Schema operativo del agente. Define como el LLM debe operar, estructurar y mantener el conocimiento.
> Basado en el patron LLM Wiki de Andrej Karpathy.
> Copiar, adaptar a tu dominio, y co-evolucionar con el agente.

---

## Arquitectura

```
mi-wiki/
├── sources/           # Fuentes crudas — inmutables, verdad de origen
│   └── assets/        # Imagenes descargadas localmente (Obsidian Web Clipper)
├── wiki/              # Paginas generadas por el LLM — el agente es dueno de esta capa
├── schema/            # Decisiones de diseno internas (gitignoreado)
├── index.md           # Catalogo por categoria — siempre actualizado
├── log.md             # Registro cronologico de actividad — append-only
└── CLAUDE.md          # Este archivo — schema y reglas de operacion
```

---

## Modelo de operacion

### Modelo de IA
- **Ingest / Query / Lint:** Opus (`/model opus`) — razonamiento profundo, conexiones entre conceptos
- **Busqueda y lectura:** Sonnet — rapido y eficiente para recuperar contexto
- Cambiar a Opus antes de cualquier operacion de ingest o lint

### Roles
- **Human:** curar fuentes, explorar, preguntar, decidir, co-evolucionar el schema
- **LLM:** resumir, cross-referenciar, mantener consistencia, bookkeeping

---

## Operaciones

### INGEST — agregar una fuente nueva
Trigger: `"ingest sources/archivo.md"`

1. Leer y comprender la fuente completa
2. **Discutir con el usuario:** presentar los takeaways clave, preguntar que enfatizar, confirmar antes de escribir
3. Escribir pagina de resumen de la fuente en `wiki/`
4. Crear o actualizar 10-15 paginas wiki relacionadas (entidades, conceptos, comparaciones)
5. Actualizar `index.md` con nuevas entradas
6. Registrar en `log.md`
7. Ejecutar `wiki_index()` (o `wiki index` en CLI) para sincronizar el indice de busqueda

> *"Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize."* — Karpathy

El ingest es un dialogo, no un proceso batch silencioso.

---

### QUERY — consultar la wiki
Trigger: pregunta directa sobre el dominio

**Con modulo wikisearch (MCP activo):**
1. `wiki_tags()` — explorar el dominio si la pregunta es amplia
2. `wiki_search(query, types=[], tags=[])` — recuperar snippets comprimidos (~150 tokens cada uno)
3. Evaluar snippets — llamar `wiki_get(filename)` SOLO para las paginas que realmente necesitas leer
4. Sintetizar respuesta con citas
5. **Archivar si es valiosa** → nueva pagina wiki + ejecutar `wiki_index()`

**Sin modulo (fallback):**
1. Leer `index.md` para identificar paginas relevantes
2. Drill down sobre esas paginas
3. Sintetizar respuesta con citas
4. Archivar si es valiosa

> **NUNCA leer wiki/ completo ni hacer Glob sobre wiki/. Siempre buscar primero.**

Formatos de salida posibles segun la pregunta:
- Pagina markdown (default)
- Tabla comparativa
- Slide deck via Marp
- Chart via matplotlib (si hay datos)
- Canvas / overview del dominio

---

### LINT — health check
Trigger: `"lint the wiki"`

**Deteccion:**
1. Paginas huerfanas (sin links entrantes)
2. Afirmaciones contradictorias entre paginas
3. Claims desactualizados por fuentes mas recientes
4. Conceptos referenciados pero sin pagina propia, cross-references faltantes
5. Data gaps resolubles con una busqueda web

**Proactivo:**
6. Sugerir nuevas preguntas que la wiki aun no responde
7. Sugerir nuevas fuentes a buscar para cubrir los gaps
8. Generar reporte completo en `log.md`

---

## Estructura de paginas wiki

Ver `wiki/_template.md` para el archivo listo para copiar.

Cada pagina incluye frontmatter YAML obligatorio:

```yaml
---
title: Nombre del concepto o entidad
type: concept | entity | person | comparison | analysis | overview
tags: [tag1, tag2]
sources: 0
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Cuerpo de la pagina:

```markdown
# Titulo

> Una linea de definicion / resumen ejecutivo

## Contexto
[Por que importa, donde aparece]

## Detalle
[Contenido principal]

## Conexiones
- Relacionado con: [[Concepto A]], [[Persona B]]
- Contrasta con: [[Concepto C]]
- Parte de: [[Categoria/Tema]]

## Fuentes
- `sources/nombre-archivo.md` — descripcion breve

## Log de cambios
- YYYY-MM-DD: creacion inicial
```

El frontmatter permite usar Dataview en Obsidian para generar tablas dinamicas por `type`, `tags`, o `sources`.

---

## Convenciones

- Nombres de archivo: `kebab-case.md`
- Links internos: `[[nombre-de-pagina]]` o `[texto](../wiki/pagina.md)`
- Fechas: ISO 8601 (`YYYY-MM-DD`)
- Una pagina por entidad/concepto

---

## index.md — estructura

El index es un catalogo, no un menu de navegacion. El LLM lo lee primero en cada QUERY.
Formato de cada entrada:

```
- [Nombre de pagina](wiki/nombre.md) — resumen en una linea | fuentes: N | actualizado: YYYY-MM-DD
```

Organizar por categorias relevantes al dominio (definir al inicializar la wiki).

---

## log.md — estructura

Formato parseble con unix tools:

```
## [YYYY-MM-DD] INGEST | nombre-de-fuente.md
- Paginas creadas: wiki/pagina-1.md, wiki/pagina-2.md
- Paginas actualizadas: wiki/pagina-existente.md

## [YYYY-MM-DD] QUERY | texto de la consulta
- Paginas consultadas: wiki/x.md, wiki/y.md
- Nueva pagina creada: wiki/nueva.md (o ninguna)

## [YYYY-MM-DD] LINT | health-check
- Huerfanas: wiki/x.md
- Contradicciones: wiki/a.md vs wiki/b.md
- Gaps: [concepto sin pagina]
- Nuevas fuentes sugeridas: [lista]
```

---

## Schema — co-evolucion

Este archivo es un documento vivo. A medida que se descubre que funciona para el dominio especifico, actualizar convenciones, formatos y workflows aqui.

> *"You and the LLM co-evolve this over time as you figure out what works for your domain."* — Karpathy

---

## Herramientas opcionales

- **[qmd](https://github.com/tobi/qmd)**: busqueda semantica local BM25/vector, CLI + MCP server para integracion directa
- **Obsidian**: graph view para visualizar conexiones, renderiza `[[wiki-links]]`
- **Obsidian Web Clipper**: convierte articulos web a markdown. Usar "Download attachments" para bajar imagenes a `sources/assets/`
- **Marp**: exportar paginas wiki a presentaciones markdown
- **Dataview** (plugin Obsidian): queries dinamicas sobre frontmatter YAML de las paginas

## Modulo de busqueda — wikisearch

Instalado en el repo. Activa recuperacion token-eficiente para la wiki.

### Instalacion
```bash
uv pip install -e .
# o: pip install -e .
```

### Reduccion de tokens vs leer manualmente

| Metodo | Tokens por query tipica |
|--------|------------------------|
| Sin modulo (leer index + 5 paginas) | ~10,000-18,000 |
| Con modulo (snippets + 2 get) | ~2,700 |
| Wiki de 500 paginas sin modulo | index.md solo ~15,000 |

### CLI
```bash
wiki index              # sincronizar indice
wiki search "query"     # buscar (snippets)
wiki get pagina.md      # leer pagina completa
wiki tags               # explorar el dominio
wiki lint               # health check
```

### MCP Server (Claude Code)
El archivo `.mcp.json` esta en la raiz del repo.
Tools disponibles: `wiki_search`, `wiki_get`, `wiki_tags`, `wiki_index`.
