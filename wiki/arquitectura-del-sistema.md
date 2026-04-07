---
title: Arquitectura del Sistema — LlmBrain Wiki
type: concept
tags: [arquitectura, llm, wiki, conocimiento, sistema]
sources: 0
created: 2026-04-07
updated: 2026-04-07
---

# Arquitectura del Sistema — LlmBrain Wiki

> Estructura organizativa del sistema LlmBrain: capas, roles, y flujo de informacion entre fuentes, wiki, e indice de busqueda.

## Contexto

El sistema LlmBrain (basado en el patron LLM Wiki de Andrej Karpathy) separa deliberadamente tres capas con responsabilidades distintas. Esta separacion es lo que permite que el conocimiento se acumule, se mantenga consistente, y sea recuperable de forma token-eficiente.

## Detalle

### Las tres capas

```
sources/           # Fuentes crudas — inmutables, verdad de origen
wiki/              # Paginas sintetizadas — el agente es dueno de esta capa
index.md + indice  # Catalogo y busqueda — actualizacion automatica
```

**`sources/`** — verdad de origen. Los archivos aqui no se modifican. Son la evidencia original: respuestas de APIs, articulos clipeados, notas crudas. La trazabilidad de cada afirmacion en la wiki apunta a un archivo en sources.

**`wiki/`** — conocimiento compilado. El LLM lee fuentes, sintetiza, resuelve contradicciones, y crea paginas interconectadas. Esta capa crece con cada INGEST. El formato de cada pagina es deliberado: frontmatter YAML + Compiled Truth (actualizable) + Timeline (append-only).

**`index.md` + wikisearch** — catalogo y recuperacion. El `index.md` es el mapa de la wiki, organizado por categorias. El modulo `wikisearch` convierte las paginas en snippets comprimidos para recuperacion token-eficiente (~2,700 tokens vs ~15,000 del index.md completo en wikis grandes).

### Flujo de una operacion INGEST

```
sources/archivo.md
    ↓ LLM lee y sintetiza
wiki/pagina-nueva.md  (10-15 paginas nuevas o actualizadas)
    ↓ wiki index
indice actualizado → wikisearch disponible
    ↓ log.md
registro de la operacion
```

### Invariante de diseño: separacion de fases

La distincion critica frente a RAG: el ingest es una fase separada de la query. En RAG, el LLM genera respuestas directamente desde los documentos en cada consulta, sin acumular conocimiento. En LlmBrain, el conocimiento se compila una vez durante el ingest y persiste como paginas wiki interconectadas.

| Dimension | RAG | LlmBrain |
|-----------|-----|----------|
| Compilacion | En cada query | Una vez en ingest |
| Conexiones | Calculadas en runtime | Pre-calculadas y persistidas |
| Contradicciones | No detectadas | Resueltas en ingest |
| Costo por query | Alto | Bajo |

### Formato de pagina wiki

Cada pagina sigue el mismo esquema:

```yaml
---
title: Nombre del concepto
type: concept | entity | person | comparison | analysis | overview | brief
tags: [tag1, tag2]
sources: N
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

El body incluye: oneliner, Contexto, Detalle (Compiled Truth), Conexiones, Fuentes, Timeline.

## Conexiones

- Relacionado con: [[ejemplo-rag-vs-llm-wiki]], [[ingest]], [[context-engineering-patterns]]
- Contrasta con: [[chatgpt-file-uploads]] (RAG on-demand vs wiki compilada)
- Parte de: [[ejemplo-rag-vs-llm-wiki]]
- Ver también: [[agent-skills-ecosystem]] (la wiki como memoria long-term del agente)

## Fuentes

- Pendiente de ingest formal — arquitectura derivada del CLAUDE.md del proyecto

---

## Timeline
- 2026-04-07: creacion inicial — gap detectado por lint
