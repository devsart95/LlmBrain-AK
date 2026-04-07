---
title: Context Engineering Patterns
type: concept
tags: [ai, context, agentes, memoria, optimizacion]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Context Engineering Patterns

> Patrones de diseno para gestionar el contexto de agentes AI — la disciplina de estructurar, comprimir y mantener la informacion que el agente necesita para operar correctamente.

## Contexto

El contexto es todo lo que el agente "sabe" en un momento dado: system prompt, conversacion, tool results, archivos leidos. La calidad del output depende directamente de la calidad del contexto. Context Engineering es la disciplina de optimizar esa capa.

## Detalle

### Context Degradation — 4 patrones de fallo

1. **Lost-in-middle**: informacion en el centro del contexto se ignora — el modelo atiende principalmente el inicio y el final
2. **Context poisoning**: informacion incorrecta contamina el razonamiento de toda la sesion
3. **Context distraction**: informacion irrelevante consume atencion y degrada la respuesta
4. **Context clash**: instrucciones contradictorias entre diferentes fuentes (CLAUDE.md vs system prompt vs tool result)

### Context Compression

Estrategias para mantener la informacion critica mientras se reduce el tamano total:
- **Summarization**: reemplazar transcripcion verbatim por resumen estructurado
- **Selective extraction**: extraer solo los campos relevantes de tool results grandes
- **Hierarchical compression**: comprimir con diferentes niveles de detalle segun la distancia temporal

Ejemplo concreto: wikisearch reduce queries tipicas de ~10,000-18,000 tokens a ~2,700 tokens via snippets comprimidos en lugar de leer paginas completas.

### Memory Systems

| Tipo | Descripcion | Ejemplo |
|------|-------------|---------|
| Short-term | Conversacion actual, tool results recientes | Contexto de sesion activa |
| Long-term | Archivos persistentes entre sesiones | CLAUDE.md, MEMORY.md, wiki |
| Graph-based | Long-term memory en estructura de grafo | data-structure-protocol — menos tokens, refactors mas seguros |

### Multi-Agent Patterns

- **Orchestrator**: un agente principal coordina subagentes especializados — mayor control, posible cuello de botella
- **Peer-to-peer**: agentes al mismo nivel colaboran directamente — mas flexible, mas dificil de auditar
- **Hierarchical**: cadena de mando con delegacion — predecible, escalable, pero mas latencia

### Tool Design

El diseno de las interfaces de tools que los agentes usan afecta directamente la calidad del contexto:
- **Architectural reduction**: simplificar la interfaz del tool reduce errores del agente y tokens consumidos
- Tools que devuelven demasiado contexto fuerzan al agente a filtrar, introduciendo riesgo de lost-in-middle

## Conexiones
- Relacionado con: [[ejemplo-rag-vs-llm-wiki]], [[generation-verification-loop]], [[agent-skills-ecosystem]], [[multi-model-review]]
- Contrasta con: [[boil-the-lake]] (boil-the-lake maximiza scope; context engineering optimiza tokens)
- Parte de: [[ai-development-workflows]]
- Ver también: [[sprint-structure-ai]] (cada skill = contexto acotado por rol), [[persistent-browser-pattern]] (estado persistente entre sesiones)

## Fuentes
- `sources/awesome-agent-skills.md` — patrones de context engineering extraidos de skills de la comunidad

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-07: creacion inicial desde `sources/awesome-agent-skills.md`
