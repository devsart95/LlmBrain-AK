# Decisiones de diseno — WikiJRS

Registro de decisiones arquitectonicas y de schema. Por que las cosas son como son.

---

## 2026-04-04 — Patron base: Karpathy LLM Wiki

**Decision:** Adoptar el patron de wiki incremental de Andrej Karpathy.

**Alternativas consideradas:**
- RAG clasico (retrieval sobre vectores): descartado porque redescubre conocimiento en cada query en lugar de acumularlo
- Notion/Obsidian manual: descartado porque el overhead de mantenimiento (cross-references, consistencia) es prohibitivo sin IA
- Base de datos estructurada: descartado por rigidez — el conocimiento no tiene schema fijo

**Por que este patron:**
- El conocimiento se acumula y compone — cada ingest hace la wiki mas valiosa
- Claude maneja el overhead de mantenimiento (links, consistencia, clasificacion)
- Human-in-the-loop para curation y decision, AI para bookkeeping
- Zero dependencias iniciales — opera 100% dentro de Claude Code

---

## 2026-04-04 — Stack: Claude Code puro (sin codigo inicial)

**Decision:** No escribir codigo en Fase 1.

**Razon:** Las tres operaciones core (ingest/query/lint) son 100% ejecutables por Claude Code con acceso al filesystem. Agregar un CLI Python seria overhead sin beneficio en esta escala.

**Trigger para Fase 2 (agregar codigo):**
- Wiki >100 paginas O busqueda semantica necesaria OR lint automatizado via cron

---

## 2026-04-04 — Modelo: Opus para pensar, Sonnet para ejecutar

**Decision:** Opus 4.6 en operaciones de ingest/query/lint. Sonnet 4.6 para busqueda y lectura.

**Razon:** Ingest requiere razonamiento profundo para conectar conceptos entre paginas. Query requiere sintesis de multiple fuentes. Lint requiere detectar contradicciones sutiles. Sonnet es suficiente para Grep/Read/busqueda de contexto.
