---
title: UX Guidelines — Mobile y Touch
type: concept
tags: [ux, mobile, touch, responsive, web]
sources: 1
created: 2026-04-04
updated: 2026-04-04
---

# UX Guidelines — Mobile y Touch

> Reglas para experiencias táctiles y responsivas. Mobile-first es el default — las excepciones se justifican.

## Touch

| Regla | Do | Don't | Código correcto | Severidad |
|-------|----|-------|----------------|-----------|
| Touch Target Size | Mínimo 44×44px en botones | Botones pequeños difíciles de tocar | `min-h-[44px] min-w-[44px]` | **High** |
| Touch Spacing | Mínimo 8px entre targets adyacentes | Elementos táctiles apilados sin espacio | `gap-2 between buttons` | Medium |
| Gesture Conflicts | Evitar swipe horizontal en contenido principal | Override de gestos del sistema | Scroll vertical como primario | Medium |
| Tap Delay | `touch-action: manipulation` elimina delay 300ms | Tap nativo sin optimización | `touch-action: manipulation` | Medium |
| Pull to Refresh | Deshabilitar donde no es necesario | Habilitado por default en todas partes | `overscroll-behavior: contain` | Low |
| Haptic Feedback | Para confirmaciones y acciones importantes | Vibración excesiva | `navigator.vibrate(10)` | Low |

## Responsive

| Regla | Do | Don't | Código correcto | Severidad |
|-------|----|-------|----------------|-----------|
| Mobile First | Estilos mobile base + breakpoints para crecer | Desktop-first con max-width queries | `Default mobile + md: lg: xl:` | Medium |
| Breakpoint Testing | Testear en 320, 375, 414, 768, 1024, 1440 | Solo testear en tu dispositivo | Multiple device testing | Medium |
| Touch Friendly | Targets más grandes en mobile | Mismo tamaño tiny que desktop | Botones más grandes en mobile | **High** |
| Readable Font Size | Mínimo 16px en body mobile | Texto pequeño en móvil | `text-base` o mayor | **High** |
| Viewport Meta | `width=device-width initial-scale=1` | Viewport incorrecto o faltante | `<meta name='viewport' content='width=device-width, initial-scale=1'>` | **High** |
| Horizontal Scroll | Contenido dentro del viewport | Contenido más ancho que el viewport | `max-w-full overflow-x-hidden` | **High** |
| Image Scaling | `max-width: 100%` en imágenes | Imágenes con ancho fijo que desbordan | `max-w-full h-auto` | Medium |
| Table Handling | `overflow-x-auto` wrapper o layout card | Tablas que rompen el layout | `overflow-x-auto` wrapper | Medium |

## Back Button (Mobile)

El botón back es uno de los gestos más frecuentes en mobile. Romperlo destruye la confianza del usuario.

```js
// Correcto — pushState preserva historial
history.pushState({}, '', '/nueva-ruta')

// Incorrecto — location.replace rompe el back
location.replace('/nueva-ruta')
```

## Teclado virtual (Mobile)

```html
<!-- Tipos de teclado por contexto -->
<input type="email" />          <!-- teclado con @ -->
<input type="tel" />            <!-- teclado numérico telefónico -->
<input type="number" />         <!-- teclado numérico -->
<input inputmode="numeric" />   <!-- numérico sin spinner +/- -->
<input inputmode="decimal" />   <!-- numérico con punto decimal -->
```

## Checklist mobile mínimo

- [ ] Todos los botones ≥ 44×44px
- [ ] Gap ≥ 8px entre elementos táctiles
- [ ] `touch-action: manipulation` en interactivos
- [ ] Font size ≥ 16px en body
- [ ] Viewport meta presente
- [ ] Sin scroll horizontal
- [ ] Tablas con `overflow-x-auto`
- [ ] `overscroll-behavior: contain` donde pull-to-refresh no aplica

## Conexiones
- Relacionado con: [[ux-guidelines-formularios-accesibilidad]], [[ux-guidelines-navegacion-animacion]], [[patron-estados-ui]]
- Parte de: [[patron-estados-ui]]
- Ver también: [[react-shadcn-patterns]] (Dialog, Sheet — componentes que necesitan touch-friendly sizing), [[nextjs-best-practices]] (viewport meta y responsive en Next.js), [[design-patterns-spacing]] (8px base unit aplica tambien en mobile)

## Fuentes
- `sources/uipro-skill/ux-guidelines.csv` — filas 22-27 (Touch), 64-71 (Responsive)

---

## Timeline

> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-04: creación inicial desde uipro-skill v2.5.0
