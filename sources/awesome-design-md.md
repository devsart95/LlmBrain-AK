# awesome-design-md — VoltAgent

> Fuente: https://github.com/VoltAgent/awesome-design-md
> Fecha de captura: 2026-04-06
> 58 DESIGN.md extraidos de sitios reales. Formato Stitch (Google).
> Se analizaron en detalle: Linear, Vercel, Stripe, Supabase, Notion, Spotify, Airbnb

## Que es DESIGN.md

Documento plain-text que describe un design system completo para que un AI agent genere UI consistente y pixel-perfect. Formato introducido por Google Stitch.

| Archivo | Lector | Proposito |
|---------|--------|-----------|
| AGENTS.md | Coding agents | Instrucciones de build |
| DESIGN.md | Design agents | Especificaciones visuales |

Cada DESIGN.md cubre: Visual Theme, Color Palette, Typography, Components, Layout, Depth/Elevation, Do's/Don'ts, Responsive, Agent Prompt Guide.

## Catalogo completo (58 sistemas)

### AI & ML (12)
Claude, Cohere, ElevenLabs, Minimax, Mistral AI, Ollama, OpenCode AI, Replicate, RunwayML, Together AI, VoltAgent, xAI

### Developer Tools (14)
Cursor, Expo, Linear, Lovable, Mintlify, PostHog, Raycast, Resend, Sentry, Supabase, Superhuman, Vercel, Warp, Zapier

### Infrastructure (6)
ClickHouse, Composio, HashiCorp, MongoDB, Sanity, Stripe

### Design & Productivity (10)
Airtable, Cal.com, Clay, Figma, Framer, Intercom, Miro, Notion, Pinterest, Webflow

### Fintech & Crypto (4)
Coinbase, Kraken, Revolut, Wise

### Enterprise & Consumer (7)
Airbnb, Apple, IBM, NVIDIA, SpaceX, Spotify, Uber

### Car Brands (5)
BMW, Ferrari, Lamborghini, Renault, Tesla

---

## Analisis detallado — 7 sistemas

### Linear
- Font: Inter Variable (cv01, ss03). Peso signature: 510 (entre regular y medium)
- Color: dark-mode-native, canvas #08090a, brand indigo #5e6ad2
- Texto: primary #f7f8f8, secondary #d0d6e0, tertiary #8a8f98
- Superficies: white opacity layers rgba(255,255,255,0.02-0.05)
- Borders: semi-transparent white rgba(255,255,255,0.05-0.08)
- Monospace: Berkeley Mono
- Focus accent: #7170ff (violet)
- Display letter-spacing: -1.584px@72px, -1.408px@64px, -1.056px@48px
- Filosofia: "Darkness as native medium, information density through subtle gradations of white opacity"

### Vercel
- Font: Geist Sans/Mono. Letter-spacing agresivo: -2.4px a -2.88px en display
- Color: white #ffffff canvas, near-black #171717 text
- Shadow-as-border: box-shadow 0px 0px 0px 1px rgba(0,0,0,0.08) en vez de CSS borders
- Workflow colors: Ship Red #ff5b4f, Preview Pink #de1d8d, Develop Blue #0a72ef
- Spacing: "gallery emptiness" — 80-120px+ entre secciones
- Filosofia: "restraint as engineering, every element earns its pixel"

### Stripe
- Font: sohne-var (custom), OpenType ss01. Peso signature: 300 (light, anti-convention)
- Color: Stripe Purple #533afd, Deep Navy #061b31 (headings, no pure black)
- Shadows: blue-tinted rgba(50,50,93,0.25) — atmosfericos, no neutrales
- Ruby #ea2261, Magenta #f96bee — solo decorativo, nunca interactivo
- Body weight 300-400, buttons 400. Financial data: tnum (tabular numerals)
- Monospace: SourceCodePro 12px/500/2.00 line-height
- Buttons: 4px radius, Cards: 6px radius, border 1px solid #e5edf5
- Filosofia: "lightness and conservative rounding communicate premium financial authority"

### Supabase
- Font: Circular (geometric, rounded terminals). Monospace: Source Code Pro
- Color: dark-mode-native, #171717 background, green #3ecf8e accent
- Casi cero shadows en dark theme — depth via border contrast y surface color
- Borders: #242424 (subtle) → #2e2e2e (standard) → #363636 (prominent)
- HSL-based semantic tokens con alpha channels para layering translucido
- Pill buttons: 9999px radius. Cards: 8-16px radius
- Section spacing: 90-128px ("cinematic pacing")
- Filosofia: "separation through line, not gap"

### Notion
- Font: NotionInter (Inter modificado). 4 weights: 400, 500, 600, 700
- Color: light-mode focused, warm near-black rgba(0,0,0,0.95), background #ffffff
- Alt background: #f6f5f4 (warm white, yellow-brown undertones)
- Notion Blue #0075de (singular accent for CTAs)
- Multi-layer shadows: 4 capas con opacity 0.01-0.05 cada una
- Whisper border: 1px solid rgba(0,0,0,0.1)
- Alternacion de secciones white ↔ warm white para ritmo visual
- Display letter-spacing: -2.125px@64px, -1.875px@54px
- OpenType: lnum + locl en display/heading
- Filosofia: "approachable minimalism through warm neutrals"

### Spotify
- Font: SpotifyMixUI/SpotifyMixUITitle (CircularSp family). Soporte i18n extenso
- Color: dark-mode-native, #121212 background, Green #1ed760 (solo funcional)
- Sistema binario de weights: 700 bold o 400 regular (600 sparingly)
- Buttons uppercase con letter-spacing +1.4-2px
- Escala compacta: 10px-24px (rango chico)
- Heavy shadow: rgba(0,0,0,0.5) 0px 8px 24px
- Inset borders para inputs: rgb(18,18,18) 0px 1px 0px, rgb(124,124,124) 0px 0px 0px 1px inset
- Filosofia: "content-first darkness — UI recedes, album art is the primary source of color"

### Airbnb
- Font: Airbnb Cereal VF (variable). Weights 500-700 solamente, no thin weights
- Color: light-mode, Rausch Red #ff385c (singular accent), near-black #222222 (warm text)
- Three-layer card shadow: 0.02 + 0.04 + 0.1 opacity graduated
- Negative tracking en headings (-0.18px a -0.44px) para "intimate, cozy headings"
- Photography-first: imagenes son hero content
- No dark mode
- 61+ responsive breakpoints
- Filosofia: "warmth matters over pure black, photography is the hero"

---

## Patrones transversales identificados

### Dark mode approaches
1. Opacity layers (Linear, Supabase): superficies como capas de white opacity sobre negro
2. Surface stepping (Spotify): colores solidos escalonados #121212 → #181818 → #1f1f1f
3. No dark mode (Notion, Airbnb): warm neutrals como base, no lo necesitan

### Typography patterns
- Custom variable fonts: sohne-var (Stripe), Airbnb Cereal VF, Geist (Vercel)
- Modified standard: NotionInter (Notion), Inter Variable (Linear)
- Geometric sans: Circular (Supabase), CircularSp (Spotify)
- Aggressive negative tracking en display: Vercel (-2.88px), Notion (-2.125px), Linear (-1.584px), Stripe (-1.4px)
- Positive tracking: Spotify buttons (+1.4-2px uppercase)

### Shadow systems
- Shadow-as-border (Vercel): box-shadow reemplaza CSS borders
- Blue-tinted (Stripe): rgba(50,50,93,0.25) — shadows con color de marca
- Multi-layer (Notion, Airbnb): 3-5 capas con opacity bajisima (0.01-0.05)
- No shadows (Supabase dark): depth solo via borders
- Heavy shadows (Spotify): opacity alta (0.3-0.5) para modals/dialogs

### Spacing philosophy
- Gallery emptiness (Vercel): 80-120px+ entre secciones
- Cinematic pacing (Supabase): 90-128px entre secciones
- Tight internal + dramatic external (todos): 16-24px dentro, 64-128px entre
- Base unit: 8px (universal)

### Color strategy
- Singular accent: Notion Blue, Rausch Red, Spotify Green, Supabase Green, Stripe Purple
- Near-black not pure black: todos usan #121212-#222222, nunca #000000
- Warm vs cool: Airbnb/Notion (warm neutrals) vs Linear/Vercel (cool grays/zinc)
