---
title: Generation-Verification Loop
type: concept
tags: [ai, workflow, agentes, patron]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# Generation-Verification Loop

> El patron correcto de interaccion humano-AI: la IA genera recomendaciones, el humano verifica y decide, siempre en ese orden.

## Contexto
El anti-patron mas comun con agentes de IA es el modelo "actua y avisa despues": la IA ejecuta una accion, luego informa al usuario lo que hizo. Esto invierte el flujo de control de forma peligrosa. gstack, basado en investigacion de Anthropic y en las filosofias de Karpathy y Willison, propone el patron inverso como default obligatorio.

## Detalle
El loop tiene una estructura fija:

1. **AI genera** — recomendaciones, codigo, analisis, plan de accion
2. **Usuario verifica** — lee, evalua, tiene contexto que la AI no tiene
3. **Usuario decide** — aprueba, modifica, rechaza
4. La AI nunca salta el paso 2 por "confianza en el resultado"

**Evidencia de Anthropic Research:** usuarios expertos interrumpen a Claude MAS seguido que usuarios novatos, no menos. Contra-intuitivo pero logico: expertise significa saber exactamente cuando el modelo va por mal camino. Mas hands-on = mejor uso, no desconfianza.

**Karpathy — "Iron Man suit":** la IA es la armadura que amplifica las capacidades del humano. Tony Stark sigue siendo el piloto. La armadura no aterriza sola y entrega el informe.

**Willison — "agents are merchants of complexity":** sin un humano verificando en el loop, no sabes lo que esta pasando. Los agentes autonomos acumulan deuda de comprension. El loop de verificacion es el mecanismo que mantiene esa deuda en cero.

## Conexiones
- Relacionado con: [[user-sovereignty]], [[ejemplo-rag-vs-llm-wiki]], [[multi-model-review]], [[sprint-structure-ai]]
- Contrasta con: [[boil-the-lake]] (boil-the-lake es sobre scope; este patron es sobre control de flujo)
- Parte de: [[gstack-overview]]
- Ver también: [[garry-tan]] (Iron Man suit — el humano sigue siendo el piloto), [[ai-development-workflows]] (SDD y checkpoints)

## Fuentes
- `sources/gstack-garry-tan.md` — patron descrito en el contexto del workflow de gstack y referencias a Anthropic, Karpathy, Willison

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/gstack-garry-tan.md`
