---
title: Design Tokens — Comparativa de Sistemas
type: comparison
tags: [diseno, tokens, tipografia, colores, spacing]
sources: 2
created: 2026-04-06
updated: 2026-04-07
---

# Design Tokens — Comparativa de Sistemas

> Análisis cruzado de tokens de diseño (tipografía, color, spacing, border-radius) en 7 sistemas de productos reales de referencia.

## Contexto

Los design tokens son las decisiones atómicas de un sistema visual: qué fuente, qué peso, qué color de fondo, cuánto espacio entre secciones. Comparar estos valores entre productos maduros revela patrones universales y decisiones de posicionamiento. Esta tabla cubre Linear, Vercel, Stripe, Supabase, Notion, Spotify y Airbnb — todos con `DESIGN.md` documentado en awesome-design-md.

## Detalle

### Tipografía

| Sistema | Font principal | Tipo | Peso signature | Display tracking |
|---------|---------------|------|---------------|-----------------|
| Linear | Inter Variable | Modified standard | 510 | -1.584px@72px |
| Vercel | Geist Sans | Custom | Regular | -2.88px@display |
| Stripe | sohne-var | Custom variable | 300 (light!) | -1.4px@56px |
| Supabase | Circular | Geometric sans | 400 | Standard |
| Notion | NotionInter | Modified Inter | 700 headlines | -2.125px@64px |
| Spotify | CircularSp | Geometric sans | 700/400 binario | +1.4-2px buttons |
| Airbnb | Cereal VF | Custom variable | 500-700 | -0.44px@28px |

**Patrón universal:** negative tracking en display es la norma. La mayoría invierte en una fuente custom o una variación de Inter/Circular. El único que usa positive tracking es Spotify — y solo en botones, para énfasis.

### Estrategia de color

| Sistema | Background | Primary text | Accent | Approach |
|---------|-----------|-------------|--------|----------|
| Linear | #08090a | #f7f8f8 | Indigo #5e6ad2 | Dark-native, opacity layers |
| Vercel | #ffffff | #171717 | Workflow colors | Light, restraint |
| Stripe | #ffffff | #061b31 (navy) | Purple #533afd | Light, premium |
| Supabase | #171717 | #fafafa | Green #3ecf8e | Dark-native, borders |
| Notion | #ffffff | rgba(0,0,0,0.95) | Blue #0075de | Light, warm |
| Spotify | #121212 | #ffffff | Green #1ed760 | Dark-native, content-first |
| Airbnb | #ffffff | #222222 | Rausch Red #ff385c | Light, warm |

**Insight clave:** "near-black never pure black" es universal. Los fondos oscuros van de #08090a a #171717, nunca #000000. Los textos claros evitan pure white puro (#ffffff solo Spotify y Supabase). Los fondos claros usan text con leve alpha (Notion) o near-black suave (Airbnb #222222).

### Spacing de secciones

| Sistema | Section spacing | Base unit | Filosofía |
|---------|----------------|-----------|-----------|
| Vercel | 80-120px+ | 8px | "Gallery emptiness" |
| Supabase | 90-128px | 8px | "Cinematic pacing" |
| Notion | 64-120px | 8px | Organic, non-rigid |
| Spotify | Standard | 8px | Compact, content-first |
| Airbnb | Standard | 8px | Photography-driven |

**El 8px base unit es universal.** Las diferencias están en la escala: productos developer-first (Vercel, Supabase) usan white space agresivo como señal de confianza. Productos content-first (Spotify, Airbnb) priorizan densidad de contenido.

### Border-radius

| Sistema | Buttons | Cards | Pills |
|---------|---------|-------|-------|
| Linear | Near-transparent bg | Luminance stepping | — |
| Vercel | Standard | Shadow-as-border | — |
| Stripe | 4px | 6px | — |
| Supabase | 6px ghost / 9999px pill | 8-16px | 9999px |
| Notion | 4px | 12-16px | 9999px |
| Spotify | 9999px pill | 6-8px | 500-9999px |
| Airbnb | 8px | 20px | — |

Spotify usa pill como firma visual. Airbnb y Notion escalan hacia cards redondeadas (20px, 16px) para calidez. Stripe mantiene radios pequeños — señal de seriedad financiera.

### Token Architecture — Patrón de 3 capas

Los sistemas maduros estructuran tokens en 3 capas. Este patrón está formalizado en el skill `design-system` de uipro:

```
Primitive (valores raw)  →  Semantic (alias por propósito)  →  Component (específico)
```

| Capa | Qué define | Ejemplo | Cuándo cambiar |
|------|-----------|---------|----------------|
| **Primitive** | Valores absolutos | `--color-blue-600: #2563EB` | Rebrand completo |
| **Semantic** | Intención de uso | `--color-primary: var(--color-blue-600)` | Cambio de tema/accent |
| **Component** | Token puntual | `--button-bg: var(--color-primary)` | Ajuste de componente |

**Ventaja:** cambiar el accent color de toda la app es un cambio de 1 línea en la capa semantic. Los 7 sistemas analizados usan alguna variante de este patrón — Linear y Vercel lo implementan con CSS custom properties; Stripe y Airbnb con tokens compilados en build time.

**Herramientas uipro:**
- `generate-tokens.cjs` — genera CSS vars desde config JSON
- `validate-tokens.cjs` — audita uso correcto en `src/`
- `tailwind-integration` reference — mapeo de tokens a Tailwind theme

## Conexiones

- Relacionado con: [[design-md-format]], [[tipografia-pairings]], [[sistema-colores-por-dominio]], [[uipro-design-skills]], [[design-patterns-typography]]
- Contrasta con: [[estilos-ui-por-tipo-producto]] (tokens son la implementacion atomica; estilos-ui es la decision estrategica)
- Parte de: [[design-patterns-dark-mode]]
- Ver también: [[design-system-industrial]] (gstack tokens: amber accent, zinc grays), [[design-patterns-shadow-systems]] (shadows como tokens), [[design-patterns-spacing]] (8px base unit)

## Fuentes

- `sources/awesome-design-md.md` — análisis de 7 sistemas de diseño extraídos de DESIGN.md de productos reales
- GitHub `nextlevelbuilder/ui-ux-pro-max-skill` — skill `design-system` v1.0.0 (token architecture, scripts)

---

## Timeline
> Evidencia cronológica append-only. Cada entrada registra cuando y de donde llegó la información.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creación inicial desde `sources/awesome-design-md.md`
- 2026-04-07: enrich — token architecture de 3 capas desde skill `design-system` de uipro v2.5.0
