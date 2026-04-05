---
title: Tipografía — Pairings y Sistema
type: reference
tags: [ui, tipografia, fuentes, google-fonts, tailwind]
sources: 1
created: 2026-04-04
updated: 2026-04-04
---

# Tipografía — Pairings y Sistema

> Combinaciones de fuentes curadas con código listo para copiar. Cada pairing tiene CSS import y config Tailwind.

## Pairings por contexto

### Profesional / SaaS / ERP

| Pairing | Heading | Body | Mood | Mejor para |
|---------|---------|------|------|-----------|
| **Classic Professional** | Inter | Inter | Limpio, funcional | SaaS, dashboards, ERP, herramientas |
| **Data Dense** | IBM Plex Sans | IBM Plex Sans | Técnico, preciso | Dashboards de datos, analytics |
| **Modern Corporate** | Poppins | Open Sans | Moderno, accesible | SaaS corporativo, startups B2B |

```tsx
// Inter — preferido DevSar para UI general
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

// IBM Plex Sans — preferido DevSar para dashboards
import { IBM_Plex_Sans } from 'next/font/google'
const ibmPlexSans = IBM_Plex_Sans({
  weight: ['400', '500', '600', '700'],
  subsets: ['latin'],
  variable: '--font-ibm-plex'
})
```

### Tech / Startup

| Pairing | Heading | Body | Mood | Mejor para |
|---------|---------|------|------|-----------|
| Tech Startup | Space Grotesk | DM Sans | Técnico, innovador | Dev tools, AI products |
| Engineering | JetBrains Mono | Inter | Código, precisión | Documentación técnica, CLI tools |
| Bold Tech | Sora | Plus Jakarta Sans | Energético, moderno | Startups de tecnología |

### Premium / Editorial

| Pairing | Heading | Body | Mood | Mejor para |
|---------|---------|------|------|-----------|
| Classic Elegant | Playfair Display | Inter | Elegante, premium | Luxury brands, editoriales |
| Editorial Modern | DM Serif Display | DM Sans | Sofisticado, legible | Revistas, portfolios premium |

### Friendly / Consumer

| Pairing | Heading | Body | Mood | Mejor para |
|---------|---------|------|------|-----------|
| Warm & Readable | Nunito | Source Sans 3 | Amigable, accesible | Apps consumer, educación |
| Rounded Modern | Outfit | Outfit | Moderno, amigable | Consumer apps, apps móviles |

## Escala tipográfica — sistema DevSar

| Uso | Tamaño | Weight | Tailwind |
|-----|--------|--------|---------|
| Body/UI base | 14px | 400 | `text-sm font-normal` |
| Tablas | 13px | 400 | `text-[13px] font-normal` |
| Labels | 14px | 500 | `text-sm font-medium` |
| Headings | 16-32px | 600 | `text-base/xl/2xl font-semibold` |
| Monospace | 13px | 400 | `font-mono text-[13px]` |

## Reglas tipográficas

| Regla | Do | Don't | Severidad |
|-------|----|-------|-----------|
| Line Height | 1.5-1.75 para body | Cramped (`leading-none`) | Medium |
| Line Length | 65-75ch max para texto largo | Full width paragraphs | Medium |
| Font Loading | `font-display: swap` + fallback similar | FOIT (Flash of Invisible Text) | Medium |
| Contrast | `text-gray-900 on white` | `text-gray-400 on gray-100` | **High** |
| Heading Clarity | Diferencia clara de tamaño/weight | Headings similares al body | Medium |

## Fuentes PROHIBIDAS (DevSar)

```
Geist, Poppins*, Nunito*, Comic Sans, Roboto, Montserrat, Open Sans*,
Lato, Raleway, Quicksand
```
*Permitidas solo en contextos consumer/friendly específicos con justificación.

## Font weights válidos

| Weight | Uso | Tailwind |
|--------|-----|---------|
| 400 | Body, texto normal | `font-normal` |
| 500 | Labels, captions | `font-medium` |
| 600 | Headings, títulos | `font-semibold` |
| 700 | Solo énfasis máximo | `font-bold` |

Weights 100, 200, 800, 900 no se usan sin justificación explícita.

## Config Tailwind — setup completo

```ts
// tailwind.config.ts
import { fontFamily } from 'tailwindcss/defaultTheme'

export default {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)', ...fontFamily.sans],
        mono: ['JetBrains Mono', ...fontFamily.mono],
        display: ['IBM Plex Sans', ...fontFamily.sans], // dashboards
      },
    },
  },
}
```

## Conexiones
- Relacionado con: [[sistema-colores-por-dominio]], [[estilos-ui-por-tipo-producto]]

## Fuentes
- `sources/uipro-skill/typography.csv` — 56 pairings con CSS import y Tailwind config
- `sources/uipro-skill/ux-guidelines.csv` — filas 72-77 (Typography rules)

## Log de cambios
- 2026-04-04: creación inicial desde uipro-skill v2.5.0
