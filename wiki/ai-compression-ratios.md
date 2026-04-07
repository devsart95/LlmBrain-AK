---
title: AI Compression Ratios
type: reference
tags: [ai, productividad, metricas]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# AI Compression Ratios

> Multiplicadores de velocidad documentados por Garry Tan al construir gstack — cuanto mas rapido produce AI comparado con un equipo humano equivalente.

## Contexto

Garry Tan construyo gstack (software factory de 23 skills para Claude Code) en aproximadamente 60 dias, generando 600K+ lineas de codigo. El ritmo sostenido fue de 10K-20K lineas por dia y 1237 contribuciones registradas en 2026. Estos numeros permiten derivar ratios de compresion por categoria de trabajo.

## Detalle

### Tabla de compresion por categoria

| Categoria | Multiplicador AI | Notas |
|-----------|-----------------|-------|
| Boilerplate | 100x | Scaffolding, repeticion estructural, setup de proyecto |
| Tests | 50x | Happy path + edge cases + mocks |
| Features | 30x | Implementacion completa de una funcionalidad acotada |
| Bugfix | 20x | Diagnosis + fix + test de regresion |
| Arquitectura | 5x | Diseno de sistema, decisiones de estructura, trade-offs |
| Research | 3x | Evaluacion de opciones, comparacion de herramientas, due diligence |

### Implicaciones operativas

**El ultimo 10% ya no cuesta nada extra.** Los equipos humanos optimizaban tomando atajos: sin tests, sin empty states, sin manejo de error exhaustivo. Ese recorte existia porque el tiempo era el bottleneck. Con AI, el boilerplate que tomaba 2 dias toma 20 minutos. El costo marginal de completitud colapso.

**"Ship the shortcut" es pensamiento legacy.** La logica de "hagamos el 80% y despues iteramos" tenia sentido cuando el 20% restante costaba semanas. Hoy ese argumento ya no aplica en categorias donde el multiplicador es 30x o mas.

**Los multiplicadores menores (arquitectura, research) reflejan donde el juicio humano sigue siendo el factor limitante.** AI puede generar opciones y analizar trade-offs, pero la decision requiere contexto de negocio, historia del proyecto, y criterio que el modelo no tiene. Ahi el multiplicador es bajo porque el tiempo humano sigue siendo el bottleneck correcto.

### Datos de Garry Tan

- Proyecto: gstack (software factory para Claude Code)
- Tiempo total: ~60 dias
- Lineas generadas: 600K+
- Ritmo: 10K-20K lineas/dia
- Contribuciones en 2026: 1237

## Conexiones

- Relacionado con: [[boil-the-lake]], [[sprint-structure-ai]], [[gstack-overview]], [[search-before-building]]
- Contrasta con: estimaciones de velocidad basadas en productividad de equipo humano tradicional
- Parte de: [[gstack-overview]]
- Ver también: [[garry-tan]] (datos de produccion de gstack), [[ai-development-workflows]] (como aprovechar estos multiplicadores)

## Fuentes

- `sources/gstack-garry-tan.md` — datos de produccion de gstack y ratios de compresion por categoria

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/gstack-garry-tan.md`
