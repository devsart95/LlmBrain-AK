---
title: Design Patterns — Dark Mode
type: concept
tags: [diseno, dark-mode, colores, ui]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# Design Patterns — Dark Mode

> Tres approaches distintos para implementar dark mode identificados en sistemas de diseño de productos reales, con una regla universal que todos comparten.

## Contexto

El dark mode no es un solo patrón. Al analizar los DESIGN.md de Linear, Supabase, Spotify, Notion y Airbnb emergen tres estrategias diferenciadas según el posicionamiento del producto. La elección del approach comunica algo sobre la identidad del sistema.

## Detalle

### 1. Opacity Layers (Linear, parcialmente Supabase)

Las superficies se construyen como capas de white opacity sobre un near-black base. No hay colores de superficie fijos — la profundidad emerge de la acumulación de transparencias.

- **Linear:** `rgba(255,255,255,0.02)` a `rgba(255,255,255,0.05)` para superficies elevadas
- **Borders:** semi-transparent white `rgba(255,255,255,0.05-0.08)` en vez de colores sólidos
- **Ventaja:** transiciones suaves entre estados, sensación de profundidad natural sin saturar
- **Filosofía:** "Darkness as the native medium" — el producto vive en oscuridad, no la tolera

### 2. Surface Stepping (Spotify, Supabase)

Colores sólidos escalonados. Cada nivel de la jerarquía visual tiene un valor hexadecimal preciso y un propósito semántico claro.

**Spotify:**
```
#121212 → #181818 → #1f1f1f → #252525
background  card       element    hover
```

**Supabase borders (3 niveles de prominencia):**
```
#242424 → #2e2e2e → #363636
subtle     default    prominent
```

- **Ventaja:** predecible, fácil de implementar, tokens explícitos
- **Filosofía Spotify:** "Content-first darkness — UI recedes, album art is the primary source of color"
- El UI es neutro para que el contenido (arte, música) sea el protagonista visual

### 3. No Dark Mode (Notion, Airbnb)

Algunos productos simplemente no lo necesitan. En vez de fondos oscuros, usan warm neutrals como base que rompen el blanco puro sin ir a dark.

**Notion:**
- Background: `#f6f5f4` (warm off-white)
- Text: `rgba(0,0,0,0.95)` — near-black con transparencia mínima
- Section alternation: white ↔ warm white para ritmo visual
- La fotografía y el contenido son el hero

**Airbnb:**
- Background: `#f2f2f2` (light warm gray)
- Text: `#222222` — near-black, no pure black
- Photography-driven: las imágenes de propiedades son el color principal de cada pantalla

### Regla universal

**NUNCA pure `#000000` como background.** Sin excepción entre los 7 sistemas analizados.

| Sistema | Background oscuro |
|---------|------------------|
| Linear | `#08090a` |
| Supabase | `#0f0f0f` / `#171717` |
| Spotify | `#121212` |

El pure black causa demasiado contraste, aplana la jerarquía visual y da sensación de inacabado. El near-black permite que las capas de elevación sean visibles.

## Conexiones

- Relacionado con: [[design-tokens-comparativa]], [[sistema-colores-por-dominio]], [[design-patterns-shadow-systems]]
- Contrasta con: [[estilos-ui-por-tipo-producto]] (estilos-ui define cuando usar dark; este doc define como implementarlo)
- Parte de: [[design-md-format]]
- Ver también: [[design-system-industrial]] (dark mode como default en gstack), [[react-shadcn-patterns]] (CSS variables para temas), [[design-patterns-spacing]] (el dark void de Supabase)

## Fuentes

- `sources/awesome-design-md.md` — análisis de patrones dark mode en Linear, Supabase, Spotify, Notion y Airbnb

---

## Timeline
> Evidencia cronológica append-only. Cada entrada registra cuando y de donde llegó la información.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creación inicial desde `sources/awesome-design-md.md`
