---
title: gstack
type: entity
tags: [herramienta, ai, garry-tan, claude-code]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# gstack

> Software factory de 23 skills que transforma Claude Code en un equipo virtual de desarrollo completo — creado por Garry Tan, President & CEO de Y Combinator.

## Contexto

gstack es la implementacion concreta de la filosofia de Garry Tan sobre productividad con AI. No es un framework de prompts — es una CLI compilada con un browser daemon, tokens de seguridad, y skills organizados por fase del ciclo de desarrollo. Construido en ~60 dias, 600K+ lineas de codigo.

## Detalle

### Que es

Una software factory implementada como CLI que extiende Claude Code con 23 slash commands. Cada comando tiene un rol especifico en el ciclo Think → Plan → Build → Review → Test → Ship → Reflect. El agente no opera con prompts genericos — cada skill establece un rol acotado antes de ejecutar.

### Quien

**Garry Tan** — President & CEO de Y Combinator. Construyo gstack como su propio toolchain de desarrollo asistido por AI. Los datos de produccion (600K+ lineas, 1237 contribuciones en 2026, 10K-20K lineas/dia) son su caso de uso personal.

### Stack tecnico

- **Runtime:** Bun — JavaScript/TypeScript nativo, sin Node
- **Browser:** Chromium persistente como daemon
- **CLI:** compilada, ~58MB de binario
- **Comunicacion:** localhost HTTP con bearer token UUID

### Arquitectura

```
CLI (usuario) → HTTP localhost → Browser daemon → Chromium → Claude Code
```

- **Browser daemon:** proceso Chromium que persiste entre comandos, elimina overhead de cold start
- **Latencia:** 100-200ms por operacion (comunicacion local)
- **Referencias al DOM:** via accessibility tree, no via selectors CSS fragiles
- **Seguridad:** localhost-only (no expuesto a red externa), bearer token UUID por sesion, cookie database en modo read-only, decryption de credenciales en memoria (nunca a disco)

### Los 23 skills

Organizados por fase del ciclo de sprint. Ver [[sprint-structure-ai]] para la lista completa con descripcion de cada skill.

### Principios que materializa

- **Boil the Lake:** el costo marginal de completitud es ~0, siempre terminar el trabajo
- **Search Before Building:** buscar en tres capas antes de construir
- **User Sovereignty:** AI recomienda, el humano decide en cada checkpoint

## Conexiones

- Relacionado con: [[sprint-structure-ai]], [[boil-the-lake]], [[search-before-building]], [[ai-compression-ratios]], [[persistent-browser-pattern]], [[generation-verification-loop]]
- Contrasta con: [[multi-model-review]] — enfoque alternativo de revision con multiples modelos
- Parte de: [[agent-skills-ecosystem]] — gstack como el proveedor de skills mas completo (28 skills)
- Ver también: [[garry-tan]] (creador), [[design-system-industrial]] (design system de gstack), [[ai-security-skills]] (skill /cso integrado)

## Fuentes

- `sources/gstack-garry-tan.md` — descripcion tecnica, arquitectura, stack, y filosofia de gstack

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/gstack-garry-tan.md`
