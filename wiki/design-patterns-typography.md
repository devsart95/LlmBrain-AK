---
title: Design Patterns — Typography
type: concept
tags: [diseno, tipografia, fuentes, ui]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# Design Patterns — Typography

> Comparativa de font stacks reales extraidos de 7 sistemas de produccion: Stripe, Airbnb, Vercel, Notion, Linear, Supabase y Spotify.

## Contexto

Los sistemas de diseño de produccion no usan fuentes "por defecto". Cada eleccion tipografica comunica un posicionamiento de marca. Analizar los stacks reales revela patrones recurrentes y decisiones conscientes que van mas alla de la estetica.

## Detalle

### Custom variable fonts (premium feel)

**sohne-var (Stripe)**
- Peso signature: 300 — "anti-convention: light, confident"
- OpenType `ss01` obligatorio en todos los contextos
- Financial data renderizado con `tnum` (tabular numerals) para alineacion columnar

**Airbnb Cereal VF**
- Solo weights 500-700 habilitados en el sistema
- "Avoiding thin weights creates confident messaging" — la ausencia de pesos ligeros es intencional
- Variable font permite microajustes de peso sin cargar fuentes adicionales

**Geist (Vercel)**
- Tracking agresivo: -2.4px a -2.88px en display sizes
- "Compressed, urgent, engineered" — comunica velocidad y precision tecnica
- El tracking negativo extremo es la firma visual mas reconocible de Vercel

### Modified standard fonts

**NotionInter (Inter modificado)**
- 4 weights: 400 / 500 / 600 / 700
- OpenType `lnum` + `locl` activados en contextos display
- Modificacion sutil de Inter original para mejor rendering en su UI densa

**Inter Variable (Linear)**
- OpenType `cv01` + `ss03` activados
- Peso signature: 510 (valor intermedio via variable font, imposible con fuentes estaticas)

### Geometric sans (friendly/approachable)

**Circular (Supabase)**
- Terminals redondeados — comunica apertura, accesibilidad
- Casi exclusivamente weight 400 en body; el bold como concepto no existe en el sistema
- Contrasta con el resto de elementos oscuros del dark theme

**CircularSp (Spotify)**
- Sistema binario: 700 o 400 unicamente, sin intermedios
- Rango de tamaños compacto: 10-24px — el contenido (album art) domina, no el texto

### Monospace companions

Cada sistema empareja su fuente display con un monospace especifico:

| Sistema | Monospace |
|---------|-----------|
| Vercel | Geist Mono |
| Linear | Berkeley Mono |
| Supabase / Stripe | Source Code Pro |
| DevSar / gstack | JetBrains Mono |

### Patron universal: negative tracking en display

Todos los sistemas comprimen sus headlines. El tracking negativo comunica precision y confianza:

| Sistema | Tracking display |
|---------|-----------------|
| Vercel | -2.88px (mas agresivo) |
| Notion | -2.125px |
| Linear | -1.584px |
| Stripe | -1.4px |
| Airbnb | -0.44px (mas sutil) |

**Excepcion notable:** Spotify usa +1.4-2px en buttons uppercase — inversion deliberada para legibilidad en contexto musical.

### Patron: near-black not pure black para texto

Ningun sistema de produccion usa `#000000` para texto principal:

- **Airbnb:** `#222222` — "warmth matters"
- **Notion:** `rgba(0,0,0,0.95)` — warm near-black, permite que el fondo respire
- **Stripe:** `#061b31` — navy profundo, ni siquiera gris, sino azul nocturno

El pure black crea contraste excesivo y se percibe como "sin pulir" en UI premium.

## Conexiones

- Relacionado con: [[tipografia-pairings]], [[design-tokens-comparativa]], [[design-patterns-spacing]]
- Contrasta con: [[design-patterns-shadow-systems]] (tipografia y shadows son dos ejes de jerarquia visual distintos)
- Parte de: [[design-system-industrial]], [[design-md-format]]
- Ver también: [[design-system-industrial]] (Satoshi + DM Sans de gstack), [[nextjs-best-practices]] (next/font para carga de fuentes), [[uipro-design-skills]] (design-system skill con token architecture)

## Fuentes

- `sources/awesome-design-md.md` — analisis de font stacks de 7 sistemas de produccion reales

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/awesome-design-md.md`
