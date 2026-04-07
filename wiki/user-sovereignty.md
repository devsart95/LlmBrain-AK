---
title: User Sovereignty
type: concept
tags: [filosofia, ai, agentes, decision-making]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# User Sovereignty

> AI recomienda, el usuario decide — regla que overridea todas las demas en cualquier workflow con agentes.

## Contexto

A medida que los agentes AI ganan capacidad de accion autonoma, el riesgo de que el sistema tome decisiones que el usuario no aprobo explicitamente crece. User Sovereignty es el principio que mantiene al humano como autoridad final, independientemente de cuan alineada parezca la recomendacion del agente.

## Detalle

### El principio

AI genera, humano verifica y aprueba. Esta secuencia no es opcional ni omitible cuando el resultado tiene impacto real. El agente puede tener razon el 95% del tiempo — ese 5% restante justifica el loop.

**Dos modelos de acuerdo = senal fuerte, no mandato.** Cuando dos LLMs diferentes concluyen lo mismo, es evidencia util. No es prueba suficiente para actuar sin revision humana.

### Referencias que informan este principio

- **Karpathy — "Iron Man suit":** el mejor uso de AI no es el piloto automatico, sino el exoesqueleto que amplifica las capacidades humanas. El humano sigue en el cockpit.
- **Simon Willison — "agents are merchants of complexity":** cada grado de autonomia que se le da a un agente agrega superficie de error. La complejidad tiene costo. Mas autonomia requiere mas inversion en verificacion.
- **Anthropic research:** expertos interrumpen MAS a los agentes AI que novatos — porque entienden mejor donde puede fallar el sistema y que consecuencias tiene dejarlo correr sin checkpoints.

### Patron: Generation-Verification Loop

```
AI genera → Human revisa → Human aprueba → AI ejecuta siguiente paso
```

El loop no se aplica igual a cada accion. La calibracion correcta:

- **Alta consecuencia** (deploy, migration, delete): checkpoint obligatorio antes de ejecutar
- **Media consecuencia** (nuevo modulo, cambio de schema): revision de diff antes de commit
- **Baja consecuencia** (boilerplate, formateo, tests): puede fluir con revision post-hoc

### Anti-patterns

- **Incorporar sin preguntar:** el agente escribe codigo, lo guarda, y avisa despues. El humano perdio la oportunidad de redirigir antes del trabajo.
- **Asumir que acuerdo = proof:** dos modelos recomiendan lo mismo → implementar directamente. El acuerdo reduce incertidumbre, no la elimina.
- **Cambiar y avisar despues:** acciones irreversibles o de alto impacto ejecutadas antes de obtener confirmacion explicita.

## Conexiones

- Relacionado con: [[boil-the-lake]], [[search-before-building]], [[sprint-structure-ai]], [[generation-verification-loop]]
- Contrasta con: [[ejemplo-rag-vs-llm-wiki]] — donde el agente opera con mayor autonomia en tareas de recuperacion de informacion
- Parte de: [[gstack-overview]]
- Ver también: [[garry-tan]] (Iron Man suit analogy), [[multi-model-review]] (dos modelos de acuerdo ≠ mandato), [[ai-development-workflows]]

## Fuentes

- `sources/gstack-garry-tan.md` — User Sovereignty como principio de diseno en workflows con AI agents

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/gstack-garry-tan.md`
