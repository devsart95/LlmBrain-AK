---
title: Estilos UI por Tipo de Producto
type: comparison
tags: [ui, diseno, estilos, producto, saas, ecommerce]
sources: 1
created: 2026-04-04
updated: 2026-04-04
---

# Estilos UI por Tipo de Producto

> Qué estilo visual usar según el dominio del producto. No toda app es flat minimalista — el estilo comunica la propuesta de valor.

## Tabla de decisión

| Producto | Estilo primario | Fuente/Tipografía | Key Effects | Anti-pattern |
|----------|----------------|------------------|-------------|-------------|
| **SaaS (General)** | Glassmorphism + Flat | Professional + Hierarchy | Hover 200-250ms, smooth transitions | Excessive animation, dark by default |
| **Micro SaaS** | Flat + Vibrant Block | Bold + Clean | Large CTA hover 300ms, scroll reveal | Complex onboarding |
| **B2B SaaS Enterprise** | Trust + Minimal | Formal + Clear | Subtle section transitions | Playful design, hidden features |
| **SaaS Dashboard** | Data-Dense + Heat Map | Clear + Readable | Hover tooltips, chart zoom, real-time pulse | Ornate design, slow rendering |
| **Fintech/Crypto** | Glassmorphism + Dark OLED | Modern + Confident | Real-time chart anim, alert pulse | Light backgrounds, no security indicators |
| **Banking** | Minimalism + Accessible | Professional + Trustworthy | Smooth state transitions, number anim | Playful design |
| **Healthcare** | Neumorphism + Accessible | Readable + Large 16px+ | Soft box-shadow, smooth press 150ms | Bright neon, motion-heavy |
| **E-commerce** | Vibrant Block-based | Engaging + Clear hierarchy | Card hover lift 200ms, scale effect | Flat without depth |
| **E-commerce Luxury** | Liquid Glass + Glassmorphism | Elegant + Refined | Chromatic aberration, fluid 400-600ms | Vibrant/Block-based |
| **Education** | Claymorphism + Micro-interactions | Friendly + Engaging | Soft press 200ms, fluffy elements | Dark modes, complex jargon |
| **Portfolio/Personal** | Motion-Driven + Minimalism | Expressive + Variable | Parallax 3-5 layers, scroll reveals | Corporate templates |
| **Startup Landing** | Motion-Driven + Vibrant Block | Modern + Energetic | Scroll-triggered, parallax | Static design, no mobile |
| **Mental Health** | Neumorphism + Accessible | Calming + Readable | Soft press, breathing animations | Bright neon, motion overload |
| **Restaurant/Food** | Vibrant Block + Motion | Appetizing + Clear | Food image reveal, menu hover | Low-quality imagery |
| **Government/Public** | Accessible + Minimalism | Clear + Large | Clear focus rings 3-4px, skip links | Ornate, low contrast, motion |

## Estilos visuales — descripción

### Minimalism / Flat
- Espacios blancos amplios, grid limpio, sin sombras decorativas
- Tailwind: 10/10, Bootstrap: 9/10
- Para: Enterprise, dashboards, herramientas profesionales
- Complexity: Low

### Glassmorphism
- Fondos con backdrop-blur, bordes semitransparentes, capas de profundidad
- `backdrop-blur-md bg-white/10 border border-white/20`
- Para: SaaS moderno, fintech, landing pages tech
- Complexity: Medium

### Neumorphism
- Soft UI: sombras duales (oscura + clara), efecto extruido
- Accesibilidad: riesgo de bajo contraste — verificar WCAG
- Para: wellness, healthcare, apps de meditación
- Complexity: Medium-High

### Vibrant & Block
- Colores sólidos vibrantes, bloques de color como elemento estructural
- Para: E-commerce, micro SaaS, conversión directa
- Complexity: Low-Medium

### Data-Dense
- Tipografía pequeña-precisa, tablas densas, dashboards de información
- Para: Analytics, ERP, dashboards operativos
- Complexity: Medium

### Motion-Driven
- Animaciones como narrativa: scroll reveals, parallax, page transitions
- Budget: máximo 1-2 animaciones por view
- Para: Portfolios, agencias, landing pages premium
- Complexity: High

## Cuándo usar dark mode

| Caso | Dark mode recomendado |
|------|----------------------|
| Fintech/Crypto | Sí — dark OLED como default |
| Financial Dashboard | Sí — mejor para datos en tiempo real |
| Herramienta de desarrollador | Sí — preferencia del usuario |
| B2B Enterprise | No default — toggle opcional |
| Healthcare | No — interferencia con accesibilidad |
| Government/Public | No — accesibilidad primero |

## Señales de cognitive misalignment

Según EvoSkills (paper 2026): los humanos organizamos UI para que otros humanos la entiendan. El LLM puede necesitar estructura distinta para operarla. En productos donde el agente AI accede a la UI programáticamente, priorizar:
- Clases semánticas descriptivas en vez de utilitarias
- `data-testid` y `aria-label` consistentes
- Estado en URL siempre (facilita scraping/testing)

## Conexiones
- Relacionado con: [[sistema-colores-por-dominio]], [[tipografia-pairings]]
- Contrasta con: [[patron-estados-ui]] — los estados son universales, el estilo no

## Fuentes
- `sources/uipro-skill/ui-reasoning.csv` — 95 patrones por tipo de producto
- `sources/uipro-skill/styles.csv` — 67 estilos visuales con checklists

## Log de cambios
- 2026-04-04: creación inicial desde uipro-skill v2.5.0
