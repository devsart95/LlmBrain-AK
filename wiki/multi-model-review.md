---
title: Multi-Model Review
type: concept
tags: [ai, code-review, calidad, workflow]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# Multi-Model Review

> Patron de code review que combina dos modelos de IA independientes para aumentar la confianza en los hallazgos.

## Contexto
En gstack, el workflow de review usa `/review` (Claude) seguido de `/codex` (OpenAI) para analizar el mismo codigo desde perspectivas independientes. El principio es simple: si dos sistemas entrenados de forma distinta llegan al mismo hallazgo, ese hallazgo tiene alta confianza. Si uno encuentra algo que el otro no, es perspectiva complementaria, no ruido.

## Detalle
El flujo tiene dos salidas posibles:

**Hallazgos superpuestos** — alta confianza. Cuando Claude y Codex identifican el mismo bug, el mismo smell, o la misma vulnerabilidad sin coordinacion entre ellos, la probabilidad de falso positivo baja drasticamente. Estos hallazgos deben priorizarse.

**Hallazgos unicos** — perspectiva complementaria. Un modelo puede detectar patrones que el otro no porque tiene diferente entrenamiento, diferente tokenizacion, diferente sesgo de corpus. Estos no se descartan; se evaluan en contexto.

La aplicabilidad va mas alla del code review. Cualquier tarea de analisis — arquitectura, seguridad, UX, documentacion — se beneficia de pasar por dos modelos con prompts independientes. El meta-patron es: usar la divergencia como senal de informacion, no como ruido a suprimir.

## Conexiones
- Relacionado con: [[gstack-overview]], [[sprint-structure-ai]], [[ai-development-workflows]]
- Contrasta con: [[user-sovereignty]] (el humano sigue siendo quien decide que hallazgos actuar)
- Parte de: [[generation-verification-loop]]
- Ver también: [[ai-security-skills]] (Trail of Bits = revisores especializados), [[context-engineering-patterns]] (contexto de cada modelo afecta los hallazgos)

## Fuentes
- `sources/gstack-garry-tan.md` — descripcion del workflow de review cross-model en gstack

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/gstack-garry-tan.md`
