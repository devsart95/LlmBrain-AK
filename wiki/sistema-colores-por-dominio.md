---
title: Sistema de Colores por Dominio de Producto
type: reference
tags: [ui, colores, diseno, paleta, producto]
sources: 1
created: 2026-04-04
updated: 2026-04-04
---

# Sistema de Colores por Dominio de Producto

> Paletas de color curadas por tipo de producto. Cada dominio tiene una psicología de color específica — no todas las apps son azul.

## Tabla de paletas principales

| Tipo de Producto | Primary | Secondary | CTA | Background | Notas |
|-----------------|---------|-----------|-----|-----------|-------|
| SaaS General | `#2563EB` | `#3B82F6` | `#F97316` | `#F8FAFC` | Trust blue + orange CTA contrast |
| Micro SaaS | `#6366F1` | `#818CF8` | `#10B981` | `#F5F3FF` | Indigo primary + emerald CTA |
| B2B SaaS Enterprise | `#0F172A` | `#334155` | `#0369A1` | `#F8FAFC` | Professional navy + blue CTA |
| SaaS Dashboard | `#1E40AF` | `#3B82F6` | `#F59E0B` | `#F8FAFC` | Blue data + amber highlights |
| Financial Dashboard | `#0F172A` | `#1E293B` | `#22C55E` | `#020617` | Dark bg + green indicators |
| Analytics Dashboard | `#1E40AF` | `#3B82F6` | `#F59E0B` | `#F8FAFC` | Blue data + amber highlights |
| Fintech/Crypto | `#F59E0B` | `#FBBF24` | `#8B5CF6` | `#0F172A` | Gold trust + purple tech |
| Banking | `#0F172A` | `#1E3A8A` | `#CA8A04` | `#F8FAFC` | Trust navy + premium gold |
| Healthcare | `#0891B2` | `#22D3EE` | `#059669` | `#ECFEFF` | Calm cyan + health green |
| E-commerce | `#059669` | `#10B981` | `#F97316` | `#ECFDF5` | Success green + urgency orange |
| E-commerce Luxury | `#1C1917` | `#44403C` | `#CA8A04` | `#FAFAF9` | Premium dark + gold accent |
| Education | `#4F46E5` | `#818CF8` | `#F97316` | `#EEF2FF` | Playful indigo + energetic orange |
| Productivity Tool | `#0D9488` | `#14B8A6` | `#F97316` | `#F0FDFA` | Teal focus + action orange |
| Knowledge Base / Docs | `#475569` | `#64748B` | `#2563EB` | `#F8FAFC` | Neutral grey + link blue |
| Portfolio/Personal | `#18181B` | `#3F3F46` | `#2563EB` | `#FAFAFA` | Monochrome + blue accent |
| Restaurant/Food | `#DC2626` | `#F87171` | `#CA8A04` | `#FEF2F2` | Appetizing red + warm gold |
| Legal Services | `#1E3A8A` | `#1E40AF` | `#B45309` | `#F8FAFC` | Authority navy + trust gold |
| Mental Health | `#8B5CF6` | `#C4B5FD` | `#10B981` | `#FAF5FF` | Calming lavender + wellness green |
| Startup Landing | Bold primaries | — | Accent contrast | — | Motion-driven + vibrant |
| AI/Chatbot | `#7C3AED` | `#A78BFA` | `#06B6D4` | `#FAF5FF` | AI purple + cyan interactions |
| Logistics | `#2563EB` | — | — | `#0F172A` | Blue + orange (tracking) + green |

## Psicología del color por función

| Color | Psicología | Usar para |
|-------|-----------|-----------|
| Blue (#2563EB) | Confianza, estabilidad, profesionalismo | SaaS, B2B, productos financieros |
| Green (#059669) | Éxito, salud, crecimiento | CTAs de éxito, healthcare, fintech |
| Orange (#F97316) | Urgencia, energía, conversión | CTAs primarios en sitios de conversión |
| Gold (#CA8A04) | Premium, autoridad, valor | Legal, banking, luxury |
| Purple (#7C3AED) | Innovación, creatividad, AI | Productos AI, tech avanzado |
| Red (#DC2626) | Acción inmediata, apetito, alerta | Errores, food, CTAs de urgencia |
| Cyan (#0891B2) | Calma, salud, claridad | Healthcare, wellness |
| Slate (neutro) | Base profesional | Fondos, textos en B2B/ERP |

## Sistema de estados (universal)

Independiente del dominio, los estados tienen colores fijos:

| Estado | Color | Tailwind |
|--------|-------|---------|
| Éxito | Emerald | `text-emerald-600 bg-emerald-50 border-emerald-200` |
| Error | Red | `text-red-600 bg-red-50 border-red-200` |
| Advertencia | Amber | `text-amber-500 bg-amber-50 border-amber-200` |
| Info | Sky | `text-sky-500 bg-sky-50 border-sky-200` |
| Primario | Blue | `text-blue-600 bg-blue-50 border-blue-200` |

## Badges — patrón correcto

```tsx
// Patrón: bg-{color}-50 text-{color}-700 border border-{color}-200 rounded-sm
<span className="bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-sm px-2 py-0.5 text-xs font-medium">
  Activo
</span>
```

## Red flags de color

- AI purple/pink gradients en productos de gobierno, banca, salud → degrada confianza
- Colores vivos en sidebars → distracción en herramientas de trabajo
- Más de 2 colores primarios en una misma vista → ruido visual
- `text-gray-400 on gray-100` → contraste insuficiente (2.8:1, necesita ≥4.5:1)

## Conexiones
- Relacionado con: [[tipografia-pairings]], [[estilos-ui-por-tipo-producto]], [[design-tokens-comparativa]], [[design-md-format]]
- Parte de: [[ux-guidelines-formularios-accesibilidad]] — color contrast rules
- Ver también: [[design-patterns-dark-mode]] (near-black como regla universal), [[design-system-industrial]] (amber accent de gstack), [[patron-estados-ui]] (estados con paleta fija), [[uipro-design-skills]] (generate-tokens.cjs)

## Fuentes
- `sources/uipro-skill/colors.csv` — 96 paletas por tipo de producto con hex exactos
- `sources/uipro-skill/ux-guidelines.csv` — fila 36: Color Contrast (4.5:1 mínimo)

---

## Timeline

> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-04: creación inicial desde uipro-skill v2.5.0
