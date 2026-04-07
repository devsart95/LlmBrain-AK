---
title: INGEST — Operacion de Ingest de Fuentes
type: concept
tags: [workflow, llm, wiki, conocimiento, proceso]
sources: 0
created: 2026-04-07
updated: 2026-04-07
---

# INGEST — Operacion de Ingest de Fuentes

> Proceso por el cual el LLM lee una fuente nueva, dialoga con el usuario sobre los takeaways, y actualiza o crea paginas wiki interconectadas.

## Contexto

INGEST es la operacion central de crecimiento del LlmBrain. Sin ingest, la wiki no crece. El ingest no es un proceso batch silencioso — es un dialogo entre el LLM y el usuario que determina que informacion se incorpora, con que enfasis, y como se conecta al conocimiento existente.

La filosofia de Karpathy al respecto: "Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize."

## Detalle

### El proceso paso a paso

1. **Leer la fuente completa** — el LLM lee `sources/archivo.md` sin interrupciones
2. **Discutir con el usuario** — presentar los takeaways clave, preguntar que enfatizar
3. **Confirmar antes de escribir** — el usuario decide que se incorpora y con que angulo
4. **Crear o actualizar paginas wiki** — tipicamente 10-15 paginas por ingest: nuevas entidades, conceptos clave, comparaciones
5. **Resolver contradicciones** — si la nueva informacion contradice algo existente, el LLM lo detecta y resuelve o marca para discusion
6. **Actualizar `index.md`** — agregar nuevas entradas en la categoria correcta
7. **Registrar en `log.md`** — entrada con fecha, fuente, paginas creadas/actualizadas
8. **Ejecutar `wiki index`** — sincronizar el indice de busqueda

### Tipos de fuentes

- **Articulos / papers** — clipeados con Obsidian Web Clipper a `sources/`
- **Respuestas de APIs / web** — guardadas en `sources/raw/` para trazabilidad
- **Notas propias** — archivos markdown en `sources/`
- **Conversaciones exportadas** — logs de chats con LLMs sobre el dominio

### Invariante: el ingest es un dialogo

El error mas comun al hacer ingest es tratar al LLM como un procesador batch. Si el LLM escribe 15 paginas sin interaccion humana, es probable que enfatice lo que infiere que importa, no lo que realmente importa para el usuario.

El checkpoint despues del paso 2 (discutir takeaways) es el momento de mas valor: el LLM trae su sintesis, el usuario aporta el contexto de negocio, y juntos definen el angulo de la compilacion.

### Diferencia con RAG

En RAG, el documento se indexa como chunks sin interpretacion. En LlmBrain, el ingest produce paginas wiki con:
- Contexto explicativo (por que importa)
- Conexiones con conocimiento previo
- Contradicciones resueltas
- Timeline de evidencia

Esas paginas son el resultado del dialogo humano-LLM, no del procesamiento automatico del documento.

## Conexiones

- Relacionado con: [[arquitectura-del-sistema]], [[ejemplo-rag-vs-llm-wiki]], [[user-sovereignty]]
- Contrasta con: [[chatgpt-file-uploads]] (upload automatico sin dialogo vs ingest como proceso deliberado)
- Parte de: [[arquitectura-del-sistema]]
- Ver también: [[context-engineering-patterns]] (el ingest produce el contexto long-term del sistema), [[generation-verification-loop]] (el paso de "discutir con el usuario" es el loop de verificacion)

## Fuentes

- Pendiente de ingest

---

## Timeline
- 2026-04-07: creacion inicial — gap detectado por lint
