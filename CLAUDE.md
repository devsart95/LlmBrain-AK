# WikiJRS — Schema v0.1

> Este archivo es el schema de la wiki. Define como Claude debe operar, estructurar y mantener el conocimiento.
> Basado en el patron LLM Wiki de Andrej Karpathy.

---

## Arquitectura (patron Karpathy)

```
WikiJRS/
├── sources/           # Fuentes crudas — inmutables, verdad de origen
│   └── assets/        # Imagenes descargadas localmente (Obsidian Web Clipper)
├── wiki/              # Paginas generadas por Claude — Claude es dueno de esta capa
├── schema/            # Documentacion interna: decisiones, changelog del schema
├── index.md           # Catalogo por categoria — siempre actualizado
├── log.md             # Registro cronologico de actividad — append-only
└── CLAUDE.md          # Este archivo — schema y reglas de operacion
```

---

## Modelo de operacion

### Modelo de IA
- **Ingest / Query / Lint:** Opus 4.6 (`/model opus`) — razonamiento profundo, conexiones entre conceptos
- **Busqueda y lectura:** Sonnet 4.6 — rapido y eficiente para recuperar contexto
- Cambiar a Opus antes de cualquier operacion de ingest o lint

### Roles
- **Human:** curar fuentes, explorar, preguntar, decidir
- **Claude:** resumir, cross-referenciar, mantener consistencia, bookkeeping

---

## Operaciones

### INGEST — agregar nueva fuente
Trigger: "ingest [fuente]" o depositar archivo en `sources/`

Proceso:
1. Leer y comprender la fuente completa
2. **Discutir con el usuario:** presentar los takeaways clave, preguntar que enfatizar, confirmar antes de escribir
3. Escribir pagina de resumen de la fuente en `wiki/`
4. Crear o actualizar 10-15 paginas wiki relacionadas (entidades, conceptos, comparaciones)
5. Actualizar `index.md` con nuevas entradas
6. Registrar en `log.md`: fecha, fuente, paginas afectadas

> Karpathy: *"Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize."*
> El ingest es un dialogo, no un proceso batch silencioso.

### QUERY — consultar el conocimiento
Trigger: pregunta directa sobre el dominio

Proceso:
1. Leer `index.md` primero para identificar paginas relevantes
2. Drill down: leer las paginas identificadas
3. Sintetizar respuesta con citas a paginas wiki
4. **Archivar la respuesta:** si es valiosa (comparacion, analisis, conexion nueva), guardarla como nueva pagina wiki — las exploraciones componen el conocimiento igual que las fuentes

Formatos de salida posibles segun la pregunta:
- Pagina markdown (default)
- Tabla comparativa
- Slide deck via Marp
- Chart via matplotlib (si hay datos)
- Canvas / overview

### LINT — health check
Trigger: "/lint" o periodicamente

Proceso (deteccion):
1. Detectar paginas huerfanas (sin links entrantes)
2. Identificar afirmaciones contradictorias entre paginas
3. Marcar claims desactualizados (verificar contra fuentes)
4. Detectar gaps: conceptos referenciados pero sin pagina propia, cross-references faltantes
5. Identificar data gaps que podrian cubrirse con una busqueda web

Proceso (proactivo — igual de importante):
6. Sugerir nuevas preguntas a investigar que la wiki no responde aun
7. Sugerir nuevas fuentes a buscar para cubrir los gaps detectados
8. Generar reporte en `log.md`

---

## Estructura de paginas wiki

Cada pagina en `wiki/` sigue este formato:

```markdown
# [Titulo de la entidad o concepto]

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
- `sources/nombre-archivo.md` — [descripcion breve]
- [Link externo] — [descripcion]

## Log de cambios
- YYYY-MM-DD: [que se agrego/cambio]
```

---

## Convenciones

- Nombres de archivo: `kebab-case.md`
- Links internos: `[[nombre-de-pagina]]` o `[texto](../wiki/pagina.md)`
- Fechas: ISO 8601 (`YYYY-MM-DD`)
- Idioma wiki: por definir (ver cuestionario)
- Una pagina por entidad/concepto. Si crece mucho → dividir con `concepto-parte-1.md`

---

## index.md — estructura

El index es un catalogo, no un menu de navegacion. Debe reflejar el estado real de la wiki.
Claude lo lee primero en cada QUERY para navegar eficientemente sin necesidad de RAG.

Formato de cada entrada:
```
- [Nombre de pagina](wiki/nombre.md) — resumen en una linea | fuentes: N | actualizado: YYYY-MM-DD
```

Categorias: **pendiente de definir en cuestionario**

## Schema — co-evolucion

Este CLAUDE.md es un documento vivo. A medida que se descubre que funciona para el dominio especifico, actualizar las convenciones, formatos y workflows aqui. El schema mejora con la wiki.

> Karpathy: *"You and the LLM co-evolve this over time as you figure out what works for your domain."*

---

## log.md — estructura

Formato parseble con unix tools (grep, awk):

```
## [YYYY-MM-DD] INGEST | nombre-de-fuente.md
- Paginas creadas: wiki/pagina-1.md, wiki/pagina-2.md
- Paginas actualizadas: wiki/pagina-existente.md
- Observaciones: [notas del proceso]

## [YYYY-MM-DD] QUERY | texto de la consulta
- Paginas consultadas: wiki/x.md, wiki/y.md
- Nueva pagina creada: wiki/nueva.md (o ninguna)

## [YYYY-MM-DD] LINT | health-check
- Huerfanas: wiki/x.md
- Contradicciones: wiki/a.md vs wiki/b.md
- Gaps: [concepto sin pagina]
```

---

## Evaluacion de necesidad de codigo

**Estado actual: no se necesita codigo.**

Razon: la wiki opera completamente dentro de Claude Code. Las operaciones de ingest/query/lint son comandos de Claude. El schema es este CLAUDE.md.

**Cuando agregar codigo (Python CLI):**
- Wiki supera 100 paginas y la busqueda por Grep se vuelve lenta
- Se necesita busqueda semantica/vectorial
- Se quiere lint automatizado via cron
- Se necesita exportar a otros formatos (HTML, PDF)

**Stack sugerido si se necesita:**
- Python 3.12 + `mistletoe` (parse markdown) + `chromadb` (vector search)
- CLI minimo: `wiki ingest <file>`, `wiki search <query>`, `wiki lint`
- Sin servidor, sin base de datos — todo en archivos locales
- Alternativa: [`qmd`](https://github.com/tobi/qmd) — motor de busqueda local BM25/vector con CLI y servidor MCP nativo

## Herramientas opcionales compatibles

- **[qmd](https://github.com/tobi/qmd)**: busqueda semantica local sobre archivos markdown, incluye MCP server para integracion directa con Claude
- **Obsidian**: visualizacion de graph view y navegacion de links internos `[[pagina]]`
- **Obsidian Web Clipper**: convierte articulos web a markdown antes de poner en `sources/`. Usar "Download attachments" (hotkey configurable) para bajar imagenes a `sources/assets/` — permite que Claude las lea directamente sin depender de URLs externas
- **Marp**: exportar paginas wiki a presentaciones markdown
- **Dataview** (plugin Obsidian): queries dinamicas sobre el frontmatter YAML de las paginas wiki — si Claude agrega `tags`, `date`, `sources` en el frontmatter, Dataview genera tablas y listas automaticas

---

*Schema v0.1 — 2026-04-04*
