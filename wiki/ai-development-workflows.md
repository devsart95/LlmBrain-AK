---
title: AI Development Workflows
type: concept
tags: [ai, workflow, desarrollo, testing, calidad]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# AI Development Workflows

> Patrones de desarrollo con AI agents que van mas alla del "chat con el LLM" — metodologias estructuradas para producir software production-ready con agentes.

## Contexto

A medida que los agentes AI se integran en el ciclo de desarrollo, emergen patrones especificos de como estructurar el trabajo para maximizar calidad y reducir errores. Estos patrones son extraidos de skills de NeoLab, obra/superpowers, gstack, y la comunidad de Claude Code.

## Detalle

### Spec-Driven Development (SDD)

Transforma prompts vagos en implementaciones production-ready via tres etapas:
1. Planning estructurado — el agente genera un plan detallado antes de codear
2. Diseno de arquitectura — decisions de estructura antes de implementar
3. Quality gates con LLM-as-Judge — un segundo LLM evalua el output del primero

El spec es el contrato entre humano y agente. Sin spec, el agente optimiza para lo que infiere — con spec, optimiza para lo que se pidio explicitamente.

### Test-Driven Development (TDD) con AI

El agente sigue el mismo ciclo red-green-refactor que un desarrollador humano:
1. Escribir tests que fallen
2. Implementar hasta que pasen
3. Refactorizar manteniendo tests verdes

Complementado con **Subagent-Driven Development**: multiples subagentes ejecutan tareas en paralelo, cada uno con su scope acotado.

### Domain-Driven Development (DDD)

- Clean Architecture + SOLID + design patterns aplicados con AI
- El agente respeta boundaries de dominio y no mezcla capas
- Las instrucciones al agente deben reflejar la arquitectura del sistema, no solo la tarea inmediata

### Reflexion Pattern

Self-refinement loop donde el LLM revisa su propio output antes de entregarlo:
1. Generar respuesta inicial
2. Auto-critica: buscar errores, inconsistencias, mejoras
3. Refinar y entregar

Fuerza al agente a "pensar dos veces". Aumenta latencia pero reduce errores significativamente.

### Kaizen — Mejora Continua

Metodologia japonesa aplicada a desarrollo con AI: multiples approaches analiticos aplicados incrementalmente, sin grandes refactors de una sola vez. Reduce el riesgo de cambios disruptivos.

### Subagent-Dispatched Development (SADD)

- Despacha subagentes independientes para tareas individuales y acotadas
- Code review checkpoints entre iteraciones — no merge sin revision
- Desarrollo rapido pero con puntos de control humano
- Cada subagente tiene contexto minimo necesario para su tarea

### Code Review con Agentes Especializados (NeoLab)

6 agentes especializados revisan un PR en paralelo, cada uno con un angulo distinto:

| Agente | Responsabilidad |
|--------|----------------|
| Bug-hunter | Buscar bugs logicos y edge cases |
| Security-auditor | Vulnerabilidades y superficie de ataque |
| Code-quality-reviewer | Calidad, legibilidad, patrones |
| Contracts-reviewer | Interfaces, tipos, contratos entre modulos |
| Historical-context-reviewer | Consistencia con el historial del repo |
| Test-coverage-reviewer | Cobertura y calidad de tests |

Cada agente emite un reporte independiente. El humano consolida y decide.

### Testing Anti-Patterns (obra/superpowers)

- Identificar practicas de testing inefectivas que consumen tiempo sin aportar confianza
- Complementado con **systematic-debugging** (metodologia estructurada) y **root-cause-tracing** (ir al origen, no al sintoma)

## Conexiones
- Relacionado con: [[sprint-structure-ai]], [[multi-model-review]], [[context-engineering-patterns]], [[generation-verification-loop]], [[user-sovereignty]]
- Contrasta con: [[boil-the-lake]] (boil-the-lake es sobre completitud; estos workflows son sobre estructura del proceso)
- Parte de: [[agent-skills-ecosystem]]
- Ver también: [[ai-security-skills]] (Subagent-Driven Development + security review), [[product-management-ai]] (discovery antes del SDD), [[garry-tan]] (gstack como referencia de implementacion)

## Fuentes
- `sources/awesome-agent-skills.md` — patrones extraidos de skills de NeoLab, obra/superpowers, gstack y comunidad

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-07: creacion inicial desde `sources/awesome-agent-skills.md`
