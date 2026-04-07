---
title: Design Patterns — Shadow Systems
type: concept
tags: [diseno, shadows, depth, ui, componentes]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# Design Patterns — Shadow Systems

> Cinco approaches de shadows y depth identificados en sistemas de produccion reales, con criterios de seleccion por contexto.

## Contexto

Las sombras son uno de los mecanismos mas sutiles pero determinantes de la percepcion de calidad en una UI. La diferencia entre un sistema "barato" y uno "premium" frecuentemente se reduce a como se maneja la profundidad. Los sistemas de produccion no usan `box-shadow` por defecto — tienen sistemas deliberados con logica propia.

## Detalle

### 1. Shadow-as-border (Vercel)

```css
box-shadow: 0px 0px 0px 1px rgba(0,0,0,0.08);
```

- Reemplaza CSS `border` completamente
- Ventaja principal: transitions mas suaves, `border-radius` sin clipping visual
- Peso visual mas sutil que un border solido
- Cards stackean multiples shadow layers con propositos distintos: uno para el "border", otro para elevacion, otro para ambient light

**Por que funciona:** elimina la dureza del borde definido sin perder la separacion visual.

### 2. Blue-tinted shadows (Stripe)

```css
box-shadow: 0 13px 27px -5px rgba(50,50,93,0.25), 0 8px 16px -8px rgba(0,0,0,0.3);
```

- `rgba(50,50,93,0.25)` — azul navy pareado con capas negras
- Las sombras absorben el color de marca, creando profundidad "atmosferica"
- "This isn't clinical — it's rich, saturated, premium"
- Asociado a materiales como metal o vidrio oscuro

**Por que funciona:** la sombra con tinte de marca unifica el sistema visualmente, incluso en elementos elevados.

### 3. Multi-layer low-opacity (Notion, Airbnb)

**Notion — 4 capas:**
```css
box-shadow:
  rgba(15,15,15,0.05) 0px 0px 0px 1px,
  rgba(15,15,15,0.1) 0px 3px 6px,
  rgba(15,15,15,0.2) 0px 9px 18px;
```

**Airbnb — 3 capas graduated:**
```css
box-shadow:
  0 2px 4px rgba(0,0,0,0.02),
  0 4px 8px rgba(0,0,0,0.04),
  0 8px 16px rgba(0,0,0,0.1);
```

- Multiples capas de baja opacity acumulan una sombra soft y natural
- Simula como la luz real crea penumbras graduadas alrededor de objetos fisicos
- "Elements feel embedded rather than floating"
- Opacidades individuales: 0.01-0.1 por capa, sumadas producen el efecto

**Por que funciona:** el ojo humano percibe luz fisica que decae gradualmente — una sola sombra dura no existe en la naturaleza.

### 4. No shadows / border-only (Supabase dark)

- Casi cero shadows en dark theme
- Depth expresada exclusivamente via border contrast:
  - Background base: `#1a1a1a`
  - Card level: `#242424`
  - Elevated: `#2e2e2e`
  - Modal: `#363636`
- El border verde (`#3ecf8e`) actua como senal de "elevated state" o focus
- "Separation through line, not gap"

**Por que funciona:** en dark mode las sombras pierden efecto — lo oscuro sobre oscuro no produce contraste. Los borders son la herramienta correcta.

### 5. Heavy shadows (Spotify)

```css
/* Dialogs / modals */
box-shadow: rgba(0,0,0,0.5) 0px 8px 24px;
/* Inputs */
box-shadow: inset 0 0 0 1px rgba(255,255,255,0.1), 0 0 0 2px rgba(255,255,255,0.05);
```

- Opacidad muy alta (0.5) reservada para elementos de maxima jerarquia
- Combinacion `inset` + `outline` para inputs
- El resto de la UI no tiene shadows — el contraste reservado para modals las hace efectivas
- Estrategia de jerarquia: escasez de sombras hace que cada una importe

**Por que funciona:** si todo tiene sombra, nada tiene jerarquia. Spotify usa sombras solo donde necesita maxima atencion.

### Tabla de decision: cuando usar cada approach

| Contexto | Approach recomendado | Referencia |
|----------|---------------------|------------|
| Light mode premium | Multi-layer low-opacity | Notion / Airbnb |
| Light mode clean/tecnico | Shadow-as-border | Vercel |
| Light mode con marca fuerte | Tinted shadows | Stripe |
| Dark mode general | Border-only, sin shadows | Supabase |
| Dark mode — solo modals | Heavy single shadow | Spotify |

## Conexiones

- Relacionado con: [[design-tokens-comparativa]], [[design-patterns-dark-mode]], [[design-patterns-spacing]]
- Contrasta con: [[design-patterns-typography]] (tipografia define jerarquia via peso/tamano; shadows via profundidad)
- Parte de: [[estilos-ui-por-tipo-producto]], [[design-md-format]]
- Ver también: [[design-system-industrial]] (gstack no usa sombras decorativas), [[uipro-design-skills]] (depth como token en design-system skill)

## Fuentes

- `sources/awesome-design-md.md` — analisis de shadow systems de sistemas de produccion reales

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/awesome-design-md.md`
