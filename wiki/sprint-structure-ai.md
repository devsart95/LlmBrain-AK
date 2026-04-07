---
title: Sprint Structure AI
type: concept
tags: [workflow, ai, productividad, proceso]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# Sprint Structure AI

> Ciclo de desarrollo estructurado para trabajo con AI — fases definidas con roles especificos para el agente en cada etapa.

## Contexto

El insight central de gstack: "structured roles over blank prompts". Darle al AI un rol especifico y acotado produce mejor output que instrucciones genericas. Un agente con el prompt "sos un arquitecto senior revisando este modulo para seguridad" opera diferente a uno con "revisa esto". La estructura del sprint formaliza esto en un ciclo completo.

## Detalle

### El ciclo

```
Think → Plan → Build → Review → Test → Ship → Reflect
```

Cada fase tiene skills asignados. El agente no cambia de rol arbitrariamente — la fase define que tipo de razonamiento se espera.

### Los 23 skills organizados por fase

**Planning**
- `/think` — razonamiento exploratorio sobre el problema antes de planificar
- `/plan` — descomposicion de la tarea en pasos accionables
- `/estimate` — estimacion de esfuerzo y complejidad

**Design**
- `/design-system` — arquitectura de componentes y sistema visual
- `/design-api` — contratos de API, schemas, y estructura de endpoints
- `/design-db` — modelado de datos y relaciones

**Implementation**
- `/build` — ejecucion de implementacion segun el plan
- `/refactor` — mejora de codigo existente sin cambiar comportamiento
- `/migrate` — migracion de datos, schemas, o dependencias

**QA**
- `/review` — code review pre-merge con criterio tecnico
- `/review-ui` — auditoria visual de interfaz
- `/review-security` — auditoria de seguridad con OWASP + STRIDE
- `/review-docker` — auditoria de Dockerfiles y configuracion de contenedores
- `/qa` — quality assurance de codigo y flujos
- `/investigate` — root cause debugging con metodologia sistematica

**Deploy**
- `/deploy` — preparacion y ejecucion de deploy
- `/rollback` — reversion controlada ante fallo

**Security**
- `/audit-security` — auditoria amplia de postura de seguridad
- `/hardening` — aplicacion de medidas de hardening

**Safety**
- `/dry-run` — simular ejecucion sin efectos reales
- `/checkpoint` — guardar estado antes de operacion de alto riesgo
- `/diff` — revisar cambios antes de aplicar

**Meta**
- `/model` — cambiar el modelo activo segun la fase

### Por que roles especificos > prompts genericos

Un agente con rol de reviewer busca activamente problemas. Un agente con rol de builder busca activamente soluciones. El mismo LLM produce outputs cualitativamente diferentes segun el rol asignado. Los skills de gstack codifican esto: cada slash command lleva un system prompt que establece el rol antes de recibir el input del usuario.

## Conexiones

- Relacionado con: [[gstack-overview]], [[boil-the-lake]], [[multi-model-review]], [[ai-development-workflows]], [[user-sovereignty]]
- Contrasta con: prompts genericos sin estructura de rol ni fase
- Parte de: [[gstack-overview]]
- Ver también: [[ai-security-skills]] (skills de seguridad del ciclo), [[product-management-ai]] (skills de planning del ciclo), [[generation-verification-loop]] (checkpoints en cada fase)

## Fuentes

- `sources/gstack-garry-tan.md` — ciclo de sprint y lista de 23 skills de gstack

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/gstack-garry-tan.md`
