---
title: RAG vs LLM Wiki
type: comparison
tags: [arquitectura, llm, conocimiento]
sources: 0
created: 2026-04-04
updated: 2026-04-04
---

# RAG vs LLM Wiki

> Dos estrategias para usar LLMs con documentos propios. RAG recupera en cada query. LLM Wiki compila una vez y mantiene.

## Contexto

Cuando se quiere que un LLM responda preguntas sobre una coleccion de documentos propios, hay dos enfoques fundamentalmente distintos. La eleccion determina si el conocimiento se acumula o se redescubre constantemente.

## Detalle

### RAG (Retrieval-Augmented Generation)

Flujo en cada consulta:
1. La pregunta se convierte en un vector de embedding
2. Se buscan los chunks mas similares en el vector store
3. El LLM recibe los chunks recuperados y genera una respuesta

**Problema central:** el LLM parte de cero en cada query. No construye nada entre consultas. Preguntas que requieren sintetizar cinco documentos obligan al sistema a encontrar y conectar fragmentos en tiempo real, sin contexto acumulado.

### LLM Wiki

Flujo separado en dos fases:

**Fase de ingest (una vez por fuente):**
1. El LLM lee la fuente completa
2. Discute takeaways con el usuario
3. Crea y actualiza 10-15 paginas wiki interconectadas
4. Resuelve contradicciones con el conocimiento previo

**Fase de query (cada consulta):**
1. El LLM lee el index para navegar la wiki
2. Las paginas relevantes ya estan sintetizadas y conectadas
3. La respuesta se construye sobre conocimiento compilado

**Diferencia clave:** las conexiones entre conceptos, las contradicciones resueltas y las sintesis ya existen antes de la pregunta.

### Comparacion directa

| Dimension | RAG | LLM Wiki |
|-----------|-----|----------|
| Conocimiento acumulado | No | Si — crece con cada ingest |
| Costo por query | Alto (busqueda + generacion) | Bajo (lectura de paginas) |
| Contradicciones | No detectadas | Resueltas en ingest |
| Infraestructura | Vector store, embeddings | Archivos markdown |
| Mantenimiento | Automatico (re-indexar) | LLM hace bookkeeping |
| Preguntas de sintesis | Fragmentadas | Respuestas pre-construidas |

## Conexiones

- Relacionado con: [[ingest]], [[context-engineering-patterns]], [[user-sovereignty]]
- Contrasta con: [[chatgpt-file-uploads]], [[arquitectura-del-sistema]]
- Parte de: [[arquitectura-del-sistema]]
- Ver también: [[generation-verification-loop]] (el LLM wiki requiere verificacion humana en el ingest), [[agent-skills-ecosystem]] (skills como alternativa a RAG para dominios especificos)

## Fuentes

- Gist original de Andrej Karpathy (fuente externa, no ingestada como archivo)

---

## Timeline

> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-04: creacion como pagina de ejemplo del sistema
