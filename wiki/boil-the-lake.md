---
title: Boil the Lake
type: concept
tags: [filosofia, productividad, ai, completitud]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# Boil the Lake

> El costo marginal de completitud con AI es casi cero — si la version completa cuesta 70 lineas mas, hacerla siempre.

## Contexto

Filosofia central de Garry Tan sobre como cambio el calculo de "cuanto esfuerzo vale la pena". Antes de AI, los equipos tomaban atajos por tiempo. Hoy, ese razonamiento es pensamiento legacy. Si la version completa existe y AI puede escribirla en segundos, no terminarla es una decision activa de entregar trabajo a medias.

## Detalle

### Lake vs Ocean

La distincion critica que hace operativa la filosofia:

- **Lake (boilable):** un modulo acotado, coverage completa de edge cases, tests de regression, validaciones en boundaries. Tiene tamano finito. Se puede hervir al 100%.
- **Ocean (no boilable):** rewrite completo de sistema legacy, migracion multi-quarter, cambio de stack fundamental. No tiene limite practico — intentar hervirlo entero en una sesion es error de scope, no de ambicion.

La regla: identificar si la tarea es un lake antes de aplicar Boil the Lake. Si es un ocean, partir en lakes.

### Tabla de compresion de tiempos AI vs equipo humano

| Categoria | Multiplicador AI |
|-----------|-----------------|
| Boilerplate | 100x |
| Tests | 50x |
| Features | 30x |
| Bugfix | 20x |
| Arquitectura | 5x |
| Research | 3x |

El ultimo 10% que los equipos solian saltear (edge cases, empty states, error handling) ahora cuesta segundos. "Ship the shortcut" es pensamiento de cuando el tiempo humano era el bottleneck real.

### Anti-patterns

- **"Elijamos B, cubre 90%"** — el 10% restante ya no justifica el trade-off
- **"Dejemos los tests para el follow-up"** — con AI, escribirlos ahora cuesta minutos
- **"Esto tomaria 2 semanas"** — estimar con velocidad humana un trabajo que AI hace en horas
- **Confundir lake con ocean** — aplicar completitud sin acotar el scope primero

## Conexiones

- Relacionado con: [[search-before-building]], [[ai-compression-ratios]], [[sprint-structure-ai]], [[user-sovereignty]]
- Contrasta con: [[generation-verification-loop]] — boil-the-lake es sobre completitud de scope; generation-verification es sobre control de flujo
- Parte de: [[gstack-overview]]
- Ver también: [[garry-tan]] (autor del principio), [[product-management-ai]] (aplicar antes del sprint)

## Fuentes

- `sources/gstack-garry-tan.md` — filosofia de Garry Tan sobre productividad con AI, Boil the Lake como principio central

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/gstack-garry-tan.md`
