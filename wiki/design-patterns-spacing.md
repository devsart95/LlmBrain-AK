---
title: Design Patterns — Spacing
type: concept
tags: [diseno, spacing, layout, ui]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# Design Patterns — Spacing

> Patrones de spacing extraidos de sistemas de produccion reales: Vercel, Supabase, Notion, Spotify y Airbnb.

## Contexto

El spacing no es estetica — es jerarquia visual. La distancia entre elementos comunica relacion: lo que esta junto pertenece junto, lo que esta separado es independiente. Los sistemas de produccion tienen spacing systems deliberados, no "lo que se ve bien" en cada componente.

## Detalle

### Base unit universal: 8px

Sin excepcion en los sistemas analizados. Scale tipico derivado:

```
4 — 8 — 12 — 16 — 24 — 32 — 48 — 64 — 96 — 128
```

Cualquier valor fuera de este scale indica un micro-adjustment especifico (Notion) o un error de diseño.

### Patron compartido: tight internal + dramatic external

El patron mas consistente en todos los sistemas:

- **Interno (dentro de cards/contenedores):** 16-24px padding
- **Externo (entre secciones mayores):** 64-128px

El contraste entre densidad interna y espacio externo es lo que crea jerarquia visual. No hay forma de comunicar "esto es una seccion nueva" sin el salto dramatico.

### "Gallery Emptiness" (Vercel)

- 80-120px+ entre secciones de marketing/landing
- "Abundance of whitespace communicates confidence"
- Filosofia: si el producto es bueno, no necesita comprimir contenido para justificarse
- Balancea la tipografia comprimida (tracking -2.88px) con espacio generoso — cada seccion respira
- El whitespace no es espacio vacio — es affordance para que el ojo descanse antes del proximo mensaje

### "Cinematic Pacing" (Supabase)

- 90-128px entre major sections
- "Each section is its own scene in the dark void"
- Internal spacing: 16-24px — el contenido tecnico es denso por naturaleza
- La transicion entre secciones es casi cinematografica: pausa larga, escena nueva
- Coherente con el dark theme — el fondo oscuro absorbe el espacio y lo hace mas dramatico

### Organic Scale (Notion)

- No estrictamente rigido: incluye valores fraccionarios (`5.6px`, `6.4px`) para micro-adjustments tipograficos
- Section spacing: 64-120px
- Separador visual adicional: alternacion `white ↔ warm white` entre secciones, no solo espacio
- "Density with breathing room" — 12-24px entre items de lista, secciones con espacio dramatico

### Content-First Compact (Spotify)

- Text size range compacto: 10-24px
- Spacing minimal: el contenido (album art, portadas) llena el espacio
- La UI se minimiza alrededor del contenido — los elementos de control son subordinados
- Grid de cards: spacing ajustado para maximizar visibilidad de imagenes

### Photography-Driven (Airbnb)

- Spacing al servicio de las imagenes, no al reves
- Cards con `border-radius: 20px` — el spacing interno "curvo" acompaña las imagenes
- 61+ responsive breakpoints para adaptar grid a cualquier viewport
- Section spacing: 64-96px en listings, mas generoso en landing/marketing

### Regla practica para proyectos propios

| Contexto | Valor recomendado |
|----------|------------------|
| Base unit | 8px (no negociable) |
| Internal padding (cards/containers) | 16-24px |
| Gap entre items de lista | 8-12px |
| Gap entre grupos relacionados | 24-32px |
| Section spacing (apps/dashboards) | 64-96px |
| Section spacing (landing/marketing) | 80-128px |
| Max-width contenido | 1200px |

El max-width de 1200px es el punto de convergencia de Notion, Vercel y Supabase — no es coincidencia. Mas alla de 1280px las lineas de texto se vuelven dificiles de seguir.

## Conexiones

- Relacionado con: [[design-tokens-comparativa]], [[estilos-ui-por-tipo-producto]], [[design-patterns-typography]]
- Contrasta con: [[design-patterns-shadow-systems]] (shadows y spacing son mecanismos de jerarquia complementarios)
- Parte de: [[design-md-format]], [[ux-guidelines-navegacion-animacion]]
- Ver también: [[uipro-design-skills]] (design-system skill define spacing tokens), [[patron-estados-ui]] (layout de estados empty/error), [[ux-guidelines-mobile-touch]] (spacing minimo en mobile)

## Fuentes

- `sources/awesome-design-md.md` — analisis de spacing systems de sistemas de produccion reales

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/awesome-design-md.md`
