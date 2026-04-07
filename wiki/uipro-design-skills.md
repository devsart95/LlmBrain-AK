---
title: uipro — Skills de Diseño Expandidos (v2.5.0+)
type: reference
tags: [herramienta, diseno, ui, ai, skills]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# uipro — Skills de Diseño Expandidos

> 6 skills de diseño agregados en v2.5.0: design (meta-skill), design-system, ui-styling, brand, slides, banner-design. Cubren desde tokens hasta identidad corporativa completa.

## Contexto

El skill `ui-ux-pro-max` (uipro) empezo como un motor de reglas UX y paletas de color. En v2.5.0 se expandio a un ecosistema completo de diseno que cubre brand identity, token architecture, presentaciones y assets visuales. El skill `design` actua como router central que delega a sub-skills especializados.

## Detalle

### Arquitectura de routing

```
/design [tipo]
    ├── brand         → voz, identidad visual, messaging, assets
    ├── design-system → tokens (3 capas), component specs, Tailwind
    ├── ui-styling    → shadcn/ui + Tailwind + canvas visual
    ├── logo          → 55 estilos, 30 paletas, Gemini AI (built-in)
    ├── cip           → 50+ deliverables corporativos (built-in)
    ├── slides        → HTML + Chart.js, copywriting formulas (built-in)
    ├── banner        → 22 estilos, social/ads/web/print (built-in)
    ├── social-photos → HTML→screenshot, multi-plataforma (built-in)
    └── icon          → 15 estilos, SVG, Gemini 3.1 Pro (built-in)
```

### Skill: `design-system`

El mas relevante para desarrollo. Implementa token architecture de 3 capas:

| Capa | Proposito | Ejemplo |
|------|-----------|---------|
| **Primitive** | Valores raw | `--color-blue-600: #2563EB` |
| **Semantic** | Alias por proposito | `--color-primary: var(--color-blue-600)` |
| **Component** | Token especifico | `--button-bg: var(--color-primary)` |

Scripts incluidos:
- `generate-tokens.cjs` — genera CSS variables desde config JSON
- `validate-tokens.cjs` — audita uso correcto en `src/`
- `embed-tokens.cjs` — inyecta tokens en componentes

References clave: token-architecture, primitive-tokens, semantic-tokens, component-tokens, component-specs, states-and-variants, tailwind-integration.

### Skill: `brand`

Gestiona identidad de marca como codigo:

- `docs/brand-guidelines.md` → source of truth
- `scripts/sync-brand-to-tokens.cjs` → sincroniza guidelines a design tokens CSS
- `scripts/inject-brand-context.cjs` → inyecta contexto de marca en prompts AI
- `scripts/validate-asset.cjs` → valida assets contra guidelines
- `scripts/extract-colors.cjs` → extrae paleta de imagenes

References: voice-framework, visual-identity, messaging-framework, consistency-checklist, logo-usage-rules, approval-checklist.

### Skill: `ui-styling`

Combina 3 capas:
- **Componentes:** shadcn/ui (Radix UI primitives, copy-paste model)
- **Styling:** Tailwind CSS (utility-first, zero runtime)
- **Visual:** Canvas (composiciones de alta calidad, filosofia-driven)

Overlap con `react-shadcn-patterns` de la wiki — este skill es la version ejecutable con scripts y templates.

### Skill: `slides`

Presentaciones HTML estrategicas:
- Layouts predefinidos con design tokens
- Chart.js integrado para data visualization
- Copywriting formulas (AIDA, PAS, etc.)
- Backgrounds y tipografia contextual por tipo de slide

### Skill: `banner-design`

Banners multi-formato:
- 22 estilos (minimalist, gradient, glassmorphism, 3D, neon, duotone, editorial...)
- Plataformas: Facebook, Twitter/X, LinkedIn, YouTube, Instagram, Google Display, web hero, print
- Generacion AI via Gemini (Flash para fondos, Pro para hero visuals)
- Safe zone rules: contenido critico en 70-80% central

### Skill: `design` (meta-router)

Unifica todo. Capacidades built-in adicionales:
- **Logo:** 55 estilos, 30 paletas, 25 guias por industria. Scripts de busqueda y generacion AI
- **CIP (Corporate Identity Program):** 50+ deliverables, 20 estilos, 20 industrias. Mockups automaticos
- **Social Photos:** HTML→screenshot, templates multi-plataforma (Instagram, Facebook, LinkedIn, TikTok, Pinterest, Threads)
- **Icon:** 15 estilos, SVG output, Gemini 3.1 Pro

## Conexiones

- Relacionado con: [[design-tokens-comparativa]], [[react-shadcn-patterns]], [[design-md-format]], [[sistema-colores-por-dominio]], [[tipografia-pairings]]
- Contrasta con: [[design-system-industrial]] (gstack tiene su propio design system, no usa uipro)
- Parte de: [[agent-skills-ecosystem]]
- Ver también: [[estilos-ui-por-tipo-producto]] (uipro cubre esos estilos como skills ejecutables), [[patron-estados-ui]] (ui-styling skill incluye los cuatro estados)

## Fuentes

- GitHub `nextlevelbuilder/ui-ux-pro-max-skill` — release v2.5.0 y commits post-release (hasta 2026-04-07)

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-07: creacion inicial desde repo GitHub ui-ux-pro-max-skill, analisis de 6 SKILL.md files (design, design-system, ui-styling, brand, slides, banner-design)
