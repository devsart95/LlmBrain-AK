---
title: UX Guidelines — Formularios y Accesibilidad
type: concept
tags: [ux, formularios, accesibilidad, aria, wcag]
sources: 1
created: 2026-04-04
updated: 2026-04-04
---

# UX Guidelines — Formularios y Accesibilidad

> Reglas críticas para formularios y accesibilidad web. La mayoría son severidad High o Critical — sin excusas para saltarlas en producción.

## Formularios

| Regla | Do | Don't | Código correcto | Severidad |
|-------|----|-------|----------------|-----------|
| Input Labels | Label visible siempre sobre o al lado del input | Placeholder como único label | `<label>Email</label><input>` | **High** |
| Error Placement | Error debajo del campo relacionado | Error único al top del form | `<input /><span class='text-red-500'>{error}</span>` | Medium |
| Inline Validation | Validar en `onBlur` para la mayoría | Solo validar en submit | `onBlur validation` | Medium |
| Input Types | `email`, `tel`, `number`, `url` según corresponda | `type='text'` para todo | `type='email'` | Medium |
| Autofill Support | `autocomplete` apropiado en cada campo | `autocomplete='off'` en todo | `autocomplete='email'` | High |
| Required Indicators | Asterisco o `(required)` visible | Sin indicación de obligatorio | `* required indicator` | Medium |
| Password Visibility | Toggle mostrar/ocultar contraseña | Sin toggle | `Show/hide password button` | Medium |
| Submit Feedback | Loading → Success/Error después de submit | Sin feedback después de submit | `Loading -> Success message` | **High** |
| Input Affordance | Inputs con border/background visibles | Inputs que parecen texto plano | `Border/background on inputs` | Medium |
| Mobile Keyboards | `inputmode='numeric'` para números en móvil | Teclado default para todo | `inputmode='numeric'` | Medium |
| Never Block Paste | Permitir paste en todos los inputs | Bloquear paste en password | `<input type='password' />` | High |
| Submit Button Enabled | Mostrar spinner, mantener habilitado | `disabled={loading}` | `<button>{loading ? <Spinner /> : 'Submit'}</button>` | Medium |

## Accesibilidad — Reglas Core

| Regla | Do | Don't | Código correcto | Severidad |
|-------|----|-------|----------------|-----------|
| Color Contrast | Mínimo 4.5:1 para texto normal | Texto con bajo contraste | `#333 on white (7:1)` | **High** |
| Color Only | Íconos + texto además del color | Solo rojo/verde para error/success | `Red text + error icon` | **High** |
| Alt Text | `alt` descriptivo en imágenes con contenido | `alt=''` en imágenes con significado | `alt='Dog playing in park'` | **High** |
| Heading Hierarchy | Niveles secuenciales h1→h2→h3 | Saltar niveles o usar headings para estilo | `h1 > h2 > h3` | Medium |
| ARIA Labels | `aria-label` en botones icon-only | Botones sin nombre accesible | `aria-label='Close menu'` | **High** |
| Keyboard Navigation | Tab order visual coherente | Traps de teclado, elementos inaccesibles | `tabIndex` ordenado | **High** |
| Form Labels | `<label for='x'>` o `aria-label` | Solo placeholder | `<label for='email'>` | **High** |
| Error Messages | `role='alert'` o `aria-live` en errores | Solo indicación visual | `role='alert'` | **High** |
| Skip Links | "Skip to main content" link | 100 tabs para llegar al contenido | Skip link al inicio | Medium |
| Screen Reader | HTML semántico + ARIA correcto | Div soup sin semántica | `<nav> <main> <article>` | Medium |
| Motion Sensitivity | `prefers-reduced-motion` en parallax/scroll-jacking | Forzar efectos de scroll | `@media (prefers-reduced-motion)` | **High** |

## Accesibilidad — Reglas Adicionales (web-interface.csv)

| Regla | Do | Don't | Código correcto | Severidad |
|-------|----|-------|----------------|-----------|
| Icon Button Labels | `aria-label` en botones solo-icono | Botón sin label accesible | `<button aria-label='Close'><XIcon /></button>` | **Critical** |
| Keyboard Handlers | `onKeyDown` junto con `onClick` | Solo `onClick` en divs interactivos | `<div onClick={fn} onKeyDown={fn} tabIndex={0}>` | High |
| Semantic HTML | `<button>`, `<a>`, `<label>` antes que ARIA | `<div role='button'>` | `<button onClick={fn}>Submit</button>` | High |
| Aria Live | `aria-live='polite'` en updates async | Updates silenciosos para screen readers | `<div aria-live='polite'>{status}</div>` | Medium |
| Decorative Icons | `aria-hidden='true'` en íconos decorativos | Íconos decorativos anunciados | `<Icon aria-hidden='true' />` | Medium |
| Visible Focus States | `:focus-visible` con ring/outline | Sin indicación de focus | `focus-visible:ring-2 focus-visible:ring-blue-500` | **Critical** |
| Never Remove Outline | Reemplazar `outline` con alternativa visible | `outline-none` solo | `focus:outline-none focus:ring-2` | **Critical** |

## Anti-patterns críticos

```html
<!-- NUNCA hacer esto -->
<meta name='viewport' content='maximum-scale=1'>  <!-- deshabilita zoom -->
<input onPaste={e => e.preventDefault()} />         <!-- bloquea paste -->
<div role='button' onClick={fn}>                    <!-- usar <button> -->
<button><XIcon /></button>                          <!-- sin aria-label -->
```

## Checklist mínimo para producción

- [ ] Todos los inputs tienen `<label>` visible o `aria-label`
- [ ] Errores con `role='alert'` o `aria-live`
- [ ] Contraste texto ≥ 4.5:1
- [ ] Botones icon-only con `aria-label`
- [ ] `focus-visible` en todos los elementos interactivos
- [ ] Submit con feedback de estado (loading + success/error)
- [ ] `prefers-reduced-motion` en animaciones

## Conexiones
- Relacionado con: [[patron-estados-ui]], [[ux-guidelines-navegacion-animacion]], [[ux-guidelines-mobile-touch]], [[react-shadcn-patterns]]
- Contrasta con: [[performance-react-ui]] — accesibilidad y performance no son opuestos
- Ver también: [[sistema-colores-por-dominio]] (contraste 4.5:1 minimo), [[nextjs-best-practices]] (error.tsx + form handling), [[estilos-ui-por-tipo-producto]] (accesibilidad varia por tipo: healthcare vs fintech)

## Fuentes
- `sources/uipro-skill/ux-guidelines.csv` — filas 36-44 (Accessibility), 54-63 (Forms)
- `sources/uipro-skill/web-interface.csv` — secciones Accessibility, Focus, Forms, Anti-Pattern

---

## Timeline

> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-04: creación inicial desde uipro-skill v2.5.0
