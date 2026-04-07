---
title: Design System Industrial (gstack)
type: reference
tags: [diseno, ui, tipografia, colores]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# Design System Industrial (gstack)

> El sistema de diseno de gstack: estetica industrial y utilitaria que prioriza densidad de informacion sobre decoracion SaaS generica.

## Contexto
La mayoria de los productos SaaS modernos comparten una estetica intercambiable: colores pastel, bordes suaves, ilustraciones isometricas. gstack elige deliberadamente la direccion opuesta. El design system esta pensado para builders y desarrolladores — usuarios que quieren informacion densa, jerarquia clara, y un producto que se siente como herramienta profesional, no como landing page.

## Detalle

### Tipografia
- **Satoshi** — display, headings. Geometrica moderna con caracter propio
- **DM Sans** — body y UI. Legible en densidades altas
- **JetBrains Mono** — data, code, numeros. Descrita como "la fuente de personalidad" del sistema. Donde aparece JetBrains Mono, hay datos o codigo — señal visual de contexto

### Color
- **Amber accent** — `#F59E0B` (primario) / `#D97706` (hover). Evoca cursor de terminal, diferencia inmediata de cualquier blue-600 generico
- **Zinc grays** — base cool-toned, no warm. Mas industrial que slate
- **Dark mode por defecto** — near-black `#0C0C0C`, no pure black. Reduce fatiga visual en sesiones largas
- Semantica de color igual que cualquier sistema robusto: color comunica estado, no decora

### Tecnica visual
- **SVG noise overlay** — opacity 0.03 sobre fondos, 0.02 sobre cards. Agrega materialidad y textura sin ser "generic SaaS template". Resultado: superficie que se siente real, no plana
- Sin gradientes decorativos, sin ilustraciones, sin stock art

### Motion
- Minimal-funcional: animaciones solo donde comunican estado
- 150ms ease-out para transiciones de UI
- 250ms maximo — nada mas largo

### Layout
- Grid de 12 columnas
- max-width 1200px
- border-radius: 12px en cards, 8px en inputs/botones

### Contraste con sistema DevSar
| Dimension | gstack | DevSar |
|-----------|--------|--------|
| Tipografia UI | Satoshi / DM Sans | Inter / IBM Plex Sans |
| Base de color | Zinc | Slate |
| Acento primario | Amber `#F59E0B` | Blue-600 |
| Mono | JetBrains Mono | JetBrains Mono |
| Dark mode | Default | Opcional |
| Noise overlay | Si (SVG) | No |

Ambos sistemas comparten JetBrains Mono para codigo y el principio de que color comunica estado. La divergencia es de personalidad de producto, no de principios de diseno.

## Conexiones
- Relacionado con: [[tipografia-pairings]], [[sistema-colores-por-dominio]], [[estilos-ui-por-tipo-producto]], [[design-tokens-comparativa]]
- Contrasta con: [[uipro-design-skills]] (gstack tiene su propio design system, no usa uipro)
- Parte de: [[gstack-overview]]
- Ver también: [[garry-tan]] (autor del design system), [[design-patterns-dark-mode]] (dark mode como default en gstack), [[design-patterns-typography]] (Satoshi y DM Sans en contexto)

## Fuentes
- `sources/gstack-garry-tan.md` — especificaciones completas del design system de gstack

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/gstack-garry-tan.md`
