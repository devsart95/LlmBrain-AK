---
title: UX Guidelines — Navegación y Animación
type: concept
tags: [ux, navegacion, animacion, layout, web]
sources: 1
created: 2026-04-04
updated: 2026-04-04
---

# UX Guidelines — Navegación y Animación

> Reglas de interacción para navegación, animaciones y layout web. Cada regla tiene severidad y código de referencia.

## Navegación

| Regla | Plataforma | Do | Don't | Código correcto | Severidad |
|-------|-----------|-----|-------|----------------|-----------|
| Smooth Scroll | Web | `scroll-behavior: smooth` en html | Saltar sin transición | `html { scroll-behavior: smooth; }` | High |
| Sticky Nav | Web | `padding-top` igual al alto del nav | Nav superpuesta al contenido | `pt-20` (si nav es `h-20`) | Medium |
| Active State | All | Highlight con color/underline | Sin feedback visual de ubicación | `text-primary border-b-2` | Medium |
| Back Button | Mobile | Preservar navigation history | Romper el botón back del browser | `history.pushState()` | High |
| Deep Linking | All | URL refleja estado actual | URLs estáticas para contenido dinámico | Query params o hash | Medium |
| Breadcrumbs | Web | Usar en sitios con 3+ niveles | En sitios flat de un nivel | `Home > Category > Product` | Low |

## Animación

| Regla | Plataforma | Do | Don't | Código correcto | Severidad |
|-------|-----------|-----|-------|----------------|-----------|
| Excessive Motion | All | Animar 1-2 elementos por view máximo | Animar todo lo que se mueve | Hero animation única | High |
| Duration Timing | All | 150-300ms para micro-interacciones | Animaciones >500ms en UI | `transition-all duration-200` | Medium |
| Reduced Motion | All | Respetar `prefers-reduced-motion` | Ignorar configuración del usuario | `@media (prefers-reduced-motion: reduce)` | High |
| Loading States | All | Skeleton screens o spinners | UI congelada sin feedback | `animate-pulse skeleton` | High |
| Hover vs Tap | All | Usar click/tap para acciones primarias | Solo hover para acciones importantes | `onClick handler` | High |
| Continuous Animation | All | Solo para loading indicators | Iconos decorativos con animación infinita | `animate-spin on loader` | Medium |
| Transform Performance | Web | `transform` y `opacity` para animaciones | Animar `width/height/top/left` | `transform: translateY()` | Medium |
| Easing Functions | All | `ease-out` al entrar, `ease-in` al salir | `linear` en transiciones UI | `ease-out` | Low |

## Layout

| Regla | Do | Don't | Código correcto | Severidad |
|-------|----|-------|----------------|-----------|
| Z-Index Management | Sistema de escala (10, 20, 30, 50) | Valores arbitrarios grandes | `z-10 z-20 z-50` | High |
| Content Jumping | Reservar espacio para contenido async | Images sin dimensiones | `aspect-ratio` o `fixed height` | High |
| Overflow Hidden | Testear que todo encaja antes de aplicar | `overflow-hidden` sin verificar | `overflow-auto` con scroll | Medium |
| Viewport Units | Usar `dvh` o compensar mobile browser | `100vh` en móviles | `min-h-dvh` o `min-h-screen` | Medium |
| Container Width | Limitar a 65-75ch para texto | Texto a full viewport | `max-w-prose` o `max-w-3xl` | Medium |
| Fixed Positioning | Compensar safe areas y otros elementos fijos | Apilar múltiples fixed sin cuidado | Fixed nav + fixed bottom con gap | Medium |
| Stacking Context | Entender qué crea nuevo stacking context | Asumir z-index funciona cross-context | Parent con z-index aísla hijos | Medium |

## Anti-patterns

- `transition-all` → especificar propiedades: `transition-colors duration-200`
- `z-[9999]` → usar escala: `z-50`
- `h-screen` en móviles → `min-h-dvh`
- Animaciones en `width/height` → usar `transform: scaleX()`

## Conexiones
- Relacionado con: [[patron-estados-ui]], [[ux-guidelines-formularios-accesibilidad]], [[ux-guidelines-mobile-touch]], [[design-patterns-spacing]]
- Parte de: [[estilos-ui-por-tipo-producto]]
- Ver también: [[performance-react-ui]] (animaciones con transform, no width/height), [[react-shadcn-patterns]] (Tabs, Sheet, Dialog — componentes con navegacion), [[design-patterns-shadow-systems]] (z-index management)

## Fuentes
- `sources/uipro-skill/ux-guidelines.csv` — reglas UX con Do/Don't y código (filas 1-21)
- `sources/uipro-skill/web-interface.csv` — guidelines web específicas

---

## Timeline

> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-04: creación inicial desde uipro-skill v2.5.0
