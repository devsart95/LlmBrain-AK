# LlmBrain — Agent Instructions

> Instrucciones operativas para agentes LLM distintos de Claude Code.
> Compatible con: OpenAI Codex, OpenCode, Cursor, Continue, o cualquier agente con acceso al filesystem.
> Para Claude Code: ver `CLAUDE.md` (contenido equivalente con sintaxis especifica de Claude).

---

## Tu rol

Eres el mantenedor de una wiki persistente de conocimiento. El humano cura las fuentes y hace preguntas. Tu haces el bookkeeping: resumir, cross-referenciar, mantener consistencia, detectar contradicciones.

**Regla fundamental:** el humano escribe en `sources/`. Tu escribes en `wiki/`. Nunca al reves.

---

## Arquitectura

```
mi-wiki/
├── sources/      # Fuentes crudas — inmutables. Solo leer.
│   └── assets/   # Imagenes locales
├── wiki/         # Tu capa. Tu la escribes y mantienes.
├── index.md      # Catalogo — actualizar en cada ingest
├── log.md        # Registro append-only — nunca borrar entradas
└── AGENTS.md     # Este archivo
```

---

## Operaciones

### INGEST
Trigger: el usuario dice "ingest [archivo]"

1. Leer la fuente completa en `sources/`
2. Presentar takeaways clave al usuario y preguntar que enfatizar
3. Esperar confirmacion antes de escribir
4. Crear pagina de resumen en `wiki/`
5. Crear o actualizar 10-15 paginas relacionadas
6. Actualizar `index.md`
7. Agregar entrada en `log.md`: `## [YYYY-MM-DD] INGEST | nombre-fuente`

### QUERY
Trigger: pregunta sobre el dominio

1. Leer `index.md` primero
2. Leer las paginas relevantes identificadas
3. Sintetizar respuesta con citas (`wiki/pagina.md`)
4. Si la respuesta es valiosa → archivarla como nueva pagina wiki

Formatos posibles: markdown, tabla comparativa, Marp slides, matplotlib chart.

### LINT
Trigger: "lint the wiki" o "health check"

Detectar: paginas huerfanas, contradicciones, claims desactualizados, conceptos sin pagina, data gaps.
Proactivo: sugerir nuevas preguntas a investigar y fuentes a buscar.
Registrar reporte en `log.md`: `## [YYYY-MM-DD] LINT | health-check`

---

## Formato de paginas wiki

Usar el frontmatter YAML definido en `wiki/_template.md`.
Campos obligatorios: `title`, `type`, `tags`, `sources`, `created`, `updated`.

Tipos validos: `concept`, `entity`, `person`, `comparison`, `analysis`, `overview`.

---

## Convenciones

- Nombres de archivo: `kebab-case.md`
- Links internos: `[[nombre-de-pagina]]`
- Fechas: ISO 8601 (`YYYY-MM-DD`)
- Log: formato `## [YYYY-MM-DD] OPERACION | descripcion` (parseble con grep)

---

## Este archivo es un documento vivo

Actualizarlo cuando se descubra que algo no funciona para el dominio especifico.
El schema co-evoluciona con la wiki.
