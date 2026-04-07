---
title: DESIGN.md Format
type: concept
tags: [diseno, ai, herramienta, design-system]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# DESIGN.md Format

> Documento plain-text que describe un design system completo para que agentes de IA generen UI visualmente consistente con un producto real.

## Contexto

Formato introducido por Google Stitch. La idea: así como `AGENTS.md` le dice a un AI agent cómo construir el proyecto, `DESIGN.md` le dice cómo debe verse. El agente lo lee al inicio y mantiene coherencia visual sin necesidad de screenshots ni Figma tokens exportados.

El repositorio **awesome-design-md** centraliza 58 `DESIGN.md` de sitios reales — Vercel, Stripe, Linear, Notion, Airbnb, Spotify, Supabase, entre otros — organizados por categoría de producto.

## Detalle

### Contenido típico de un DESIGN.md

- **Visual Theme** — tono general, personalidad, filosofía de diseño
- **Color Palette** — backgrounds, texto, accents, estados (success/error/warning)
- **Typography** — fuentes, pesos, tracking, escala tipográfica
- **Components** — botones, inputs, cards, modales, badges
- **Layout** — grid, breakpoints, contenedores máximos
- **Depth / Elevation** — sombras, z-index, borders
- **Do's / Don'ts** — restricciones explícitas para el agente
- **Responsive** — comportamiento en mobile, tablet, desktop
- **Agent Prompt Guide** — instrucciones directas al LLM sobre cómo aplicar el sistema

### Diferencia clave con AGENTS.md

| Archivo | Propósito |
|---------|-----------|
| `AGENTS.md` | Instrucciones de build: stack, comandos, convenciones de código |
| `DESIGN.md` | Especificaciones visuales: colores, tipografía, componentes, tono |

Ambos coexisten. AGENTS.md es para el cómo se construye, DESIGN.md para el cómo se ve.

### Categorías en awesome-design-md (58 sistemas)

| Categoría | Cantidad | Ejemplos |
|-----------|----------|---------|
| AI & ML | 12 | — |
| Developer Tools | 14 | Vercel, Linear, Supabase |
| Infrastructure | 6 | — |
| Design & Productivity | 10 | Notion, Figma |
| Fintech & Crypto | 4 | Stripe |
| Enterprise & Consumer | 7 | Airbnb |
| Car Brands | 5 | — |

### Uso práctico

1. Identificar el sitio cuyo estilo se quiere emular
2. Copiar su `DESIGN.md` a la raíz del proyecto
3. El agente de IA lo lee como contexto de sesión
4. Todas las decisiones de UI (colores, spacing, tipografía) quedan ancladas al sistema documentado

## Conexiones

- Relacionado con: [[design-tokens-comparativa]], [[tipografia-pairings]], [[sistema-colores-por-dominio]], [[uipro-design-skills]]
- Contrasta con: [[estilos-ui-por-tipo-producto]] (DESIGN.md es un sistema codificado; estilos-ui es una guia de decision)
- Parte de: [[design-patterns-dark-mode]]
- Ver también: [[agent-skills-ecosystem]] (Google Stitch publica sus propios DESIGN.md como skills), [[design-patterns-shadow-systems]], [[design-patterns-spacing]], [[design-patterns-typography]]

## Fuentes

- `sources/awesome-design-md.md` — colección de 58 DESIGN.md de productos reales, organizados por categoría, con análisis de patrones comunes

---

## Timeline
> Evidencia cronológica append-only. Cada entrada registra cuando y de donde llegó la información.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creación inicial desde `sources/awesome-design-md.md`
