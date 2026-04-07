# Log de actividad

> Registro cronologico append-only de todas las operaciones.
> El LLM escribe aqui. Nunca borrar entradas.
> Formato: `## [YYYY-MM-DD] OPERACION | descripcion` — parseble con unix tools.

---

## [2026-04-07] INGEST | Claude Agent SDK + MCP Docs + Vercel AI SDK
- Páginas creadas: agent-sdk-overview, agent-sdk-hooks, agent-sdk-sessions, agent-sdk-subagentes, mcp-arquitectura, mcp-build-server, mcp-seguridad, vercel-ai-sdk-overview, vercel-ai-sdk-tools, vercel-ai-sdk-streaming, vercel-ai-sdk-agentes
- Total wiki: 61 páginas

## [2026-04-07] INGEST | Claude Code Official Docs
- Páginas creadas: claude-code-hooks, claude-code-skills, claude-code-subagentes, claude-code-memory, claude-code-settings, claude-code-agent-teams, claude-code-best-practices, claude-code-mcp, claude-code-permisos, claude-code-context-window, claude-code-workflow-patterns, claude-code-cli-referencia
- Fuente: https://code.claude.com/docs
- Cobertura: hooks (25+ eventos, 4 tipos, exit codes), skills (frontmatter completo, preprocessing shell, paths), subagentes (worktree isolation, Writer/Reviewer, auto-memory), memory y CLAUDE.md (dos sistemas, reglas modulares, límites), settings (4 scopes, merge behavior, managed), agent teams (experimental, shared task list, plan approval), best practices (constraint fundamental, failure patterns, fan-out), MCP (local/remoto, registry, OAuth, Elicitation), permisos (modos, allow/deny, clasificador ML, sandboxing), context window (compaction, rewind, degradación), workflow patterns (ciclo base, Plan Mode, non-interactive), CLI referencia (flags, REPL commands, keybindings)

---

## [2026-04-07] LINT | fix crosslinks + gap pages
- Crosslinks agregados: 34 paginas (todas las paginas existentes actualizadas con secciones Conexiones expandidas)
- Paginas creadas: wiki/arquitectura-del-sistema.md, wiki/chatgpt-file-uploads.md, wiki/ingest.md
- Estado del grafo: antes 0 conexiones entrantes → despues 34+ paginas con conexiones cruzadas
- Gaps resueltos del lint: arquitectura del sistema, chatgpt file uploads, ingest (index y ingest eran operaciones del sistema, no slugs de wiki)
- Conexiones promedio por pagina: 4-6 links salientes + 1-4 Ver tambien
- index.md actualizado: nueva categoria "Arquitectura y Conceptos del Sistema" con 3 entradas

## [2026-04-07] ENRICH | design-tokens-comparativa.md
- Fuentes consultadas: GitHub `nextlevelbuilder/ui-ux-pro-max-skill` — skill `design-system` SKILL.md
- Secciones actualizadas: Detalle (nueva subseccion Token Architecture), Conexiones, Fuentes
- Timeline entry agregado: si
- Dato clave: patron de 3 capas (primitive→semantic→component) formalizado con ejemplos y herramientas

## [2026-04-07] ENRICH | nueva pagina uipro-design-skills.md
- Fuentes consultadas: GitHub `nextlevelbuilder/ui-ux-pro-max-skill` — 6 SKILL.md files, releases, commits post-v2.5.0
- Pagina creada: `wiki/uipro-design-skills.md` — overview de 6 skills de diseno (design, design-system, ui-styling, brand, slides, banner-design)
- Cobertura: arquitectura de routing, token architecture, brand-as-code, slides con Chart.js, banner multi-formato, logo/CIP/social-photos/icon

---

## [2026-04-07] INGEST | awesome-agent-skills.md
- Fuente: `sources/awesome-agent-skills.md` (GitHub repo VoltAgent/awesome-agent-skills — 1060+ skills)
- Proveedores analizados: Anthropic, Microsoft, Vercel, Cloudflare, Google, Trail of Bits, Expo, Hugging Face, gstack, NeoLab, obra, Huryn
- Paginas creadas (5):
  - `wiki/agent-skills-ecosystem.md` — overview del ecosistema y catalogo por proveedor
  - `wiki/context-engineering-patterns.md` — degradation, compression, memory, multi-agent
  - `wiki/ai-development-workflows.md` — SDD, TDD, DDD, Reflexion, Kaizen, SADD
  - `wiki/ai-security-skills.md` — Trail of Bits, gstack /cso, clawsec, vibesec
  - `wiki/product-management-ai.md` — Huryn frameworks, gstack /office-hours
- Cobertura: ecosistema de skills, context engineering, workflows de desarrollo, seguridad, product management

---

## [2026-04-06] INGEST | awesome-design-md.md
- Fuente: `sources/awesome-design-md.md` (GitHub repo VoltAgent/awesome-design-md — 58 DESIGN.md de sitios reales)
- Sistemas analizados en detalle: Linear, Vercel, Stripe, Supabase, Notion, Spotify, Airbnb
- Paginas creadas (6):
  - `wiki/design-md-format.md` — formato DESIGN.md y catalogo
  - `wiki/design-tokens-comparativa.md` — tablas cruzadas de 7 sistemas
  - `wiki/design-patterns-dark-mode.md` — 3 approaches de dark mode
  - `wiki/design-patterns-typography.md` — font stacks y tracking comparativo
  - `wiki/design-patterns-shadow-systems.md` — 5 approaches de shadows/depth
  - `wiki/design-patterns-spacing.md` — patrones de spacing reales
- Cobertura: tipografia, color, spacing, shadows, dark mode, border-radius de 7 design systems de produccion

---

## [2026-04-06] INGEST | gstack-garry-tan.md
- Fuente: `sources/gstack-garry-tan.md` (GitHub repo garrytan/gstack + README, ARCHITECTURE, DESIGN, ETHOS, SKILL, CLAUDE, AGENTS)
- Paginas creadas (11):
  - `wiki/gstack-overview.md` — overview de la herramienta
  - `wiki/boil-the-lake.md` — filosofia de completitud
  - `wiki/search-before-building.md` — 3 capas de conocimiento
  - `wiki/user-sovereignty.md` — AI recomienda, usuario decide
  - `wiki/generation-verification-loop.md` — patron de interaccion humano-AI
  - `wiki/ai-compression-ratios.md` — tabla de compresion tiempos
  - `wiki/sprint-structure-ai.md` — ciclo Think→Ship con 23 skills
  - `wiki/multi-model-review.md` — review cross-model
  - `wiki/persistent-browser-pattern.md` — Chromium daemon
  - `wiki/design-system-industrial.md` — design system utilitario
  - `wiki/garry-tan.md` — persona
- Cobertura: 3 principios filosoficos, 23 skills catalogados, arquitectura tecnica, design system, metricas de productividad

---

## [2026-04-06] SCHEMA | mejoras inspiradas en GBrain (Garry Tan)
- Fuente: https://gist.github.com/garrytan/49c88e83cf8d7ae95e087426368809cb
- Cambios en CLAUDE.md:
  - Nueva operacion ENRICH — enriquecer paginas con datos externos
  - Nueva operacion BRIEF — sintesis ejecutiva cross-domain
  - LINT ampliado con backlinks, links rotos, grafo de conexiones, candidatos a enrich
  - Tipo `brief` agregado al frontmatter
  - Roadmap de vector search (embeddings) documentado
  - Arquitectura actualizada con `sources/raw/`
  - Formatos de log para ENRICH y BRIEF
- Template actualizado: estructura Compiled Truth (arriba) + Timeline (abajo, append-only)
- 11 paginas wiki migradas al nuevo formato (Log de cambios → Timeline)
- Directorio `sources/raw/` creado para datos de enrichment

---

## [2026-04-04] INGEST | uipro-skill v2.5.0 �� UI/UX Pro Max
- Fuente: `sources/uipro-skill/` (SKILL.md + 10 CSVs, 1406 líneas)
- Extra��do de: uipro-cli v2.5.0, assets locales npm (sin descarga externa)
- Paginas creadas (10):
  - `wiki/ux-guidelines-navegacion-animacion.md`
  - `wiki/ux-guidelines-formularios-accesibilidad.md`
  - `wiki/ux-guidelines-mobile-touch.md`
  - `wiki/patron-estados-ui.md`
  - `wiki/sistema-colores-por-dominio.md`
  - `wiki/tipografia-pairings.md`
  - `wiki/estilos-ui-por-tipo-producto.md`
  - `wiki/nextjs-best-practices.md`
  - `wiki/react-shadcn-patterns.md`
  - `wiki/performance-react-ui.md`
- Cobertura: 98 UX guidelines, 95 product patterns, 56 font pairings, 96 color palettes, 44 React performance patterns, 39 Next.js rules, 61 shadcn conventions

---

## [YYYY-MM-DD] SETUP | inicializacion
- Estructura base creada: `sources/`, `wiki/`
- Schema definido en `CLAUDE.md`

---
