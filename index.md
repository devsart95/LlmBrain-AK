# Index

> Catalogo de todo el conocimiento en la wiki, organizado por categoria.
> El LLM actualiza este archivo en cada operacion INGEST.
> Formato: `- [Pagina](wiki/pagina.md) — resumen | fuentes: N | actualizado: YYYY-MM-DD`

---

## Estado

- Paginas wiki: 68
- Fuentes ingestadas: 9

---

## Filosofia y Principios — AI-Assisted Development

- [Boil the Lake](wiki/boil-the-lake.md) — Costo marginal de completitud ~0 con AI; lake vs ocean, tabla de compresion | fuentes: 1 | actualizado: 2026-04-06
- [Search Before Building](wiki/search-before-building.md) — 3 capas de conocimiento (tried-and-true, popular, first principles), eureka moment | fuentes: 1 | actualizado: 2026-04-06
- [User Sovereignty](wiki/user-sovereignty.md) — AI recomienda, usuario decide. Generation-verification loop. Karpathy, Willison, Anthropic | fuentes: 1 | actualizado: 2026-04-06
- [Generation-Verification Loop](wiki/generation-verification-loop.md) — Patron de interaccion humano-AI: generar, verificar, decidir. Nunca saltear verificacion | fuentes: 1 | actualizado: 2026-04-06
- [AI Compression Ratios](wiki/ai-compression-ratios.md) — Tabla de compresion tiempos equipo humano vs AI-assisted (100x a 3x segun tarea) | fuentes: 1 | actualizado: 2026-04-06

## Ecosistema AI — Skills, Context, Workflows

- [Agent Skills — Ecosistema](wiki/agent-skills-ecosystem.md) — 1060+ skills para Claude Code/Codex/Gemini CLI, 18+ proveedores oficiales | fuentes: 1 | actualizado: 2026-04-07
- [Context Engineering — Patrones](wiki/context-engineering-patterns.md) — Degradation, compression, memory systems, multi-agent patterns | fuentes: 1 | actualizado: 2026-04-07
- [AI Development Workflows](wiki/ai-development-workflows.md) — SDD, TDD, DDD, Reflexion, Kaizen, SADD, code review con 6 agentes | fuentes: 1 | actualizado: 2026-04-07
- [AI Security Skills](wiki/ai-security-skills.md) — Trail of Bits (21 skills), gstack /cso, clawsec, vibesec | fuentes: 1 | actualizado: 2026-04-07
- [Product Management con AI](wiki/product-management-ai.md) — Huryn (40+ frameworks), gstack /office-hours, discovery → strategy → pricing | fuentes: 1 | actualizado: 2026-04-07

## Workflows y Herramientas AI

- [gstack — Overview](wiki/gstack-overview.md) — Software factory de Garry Tan: 23 skills, Bun + Chromium daemon, Claude Code como equipo virtual | fuentes: 1 | actualizado: 2026-04-06
- [Sprint Structure AI](wiki/sprint-structure-ai.md) — Think → Plan → Build → Review → Test → Ship → Reflect. 23 skills por fase | fuentes: 1 | actualizado: 2026-04-06
- [Multi-Model Review](wiki/multi-model-review.md) — Review cross-model (Claude + Codex): hallazgos superpuestos = alta confianza | fuentes: 1 | actualizado: 2026-04-06
- [Persistent Browser Pattern](wiki/persistent-browser-pattern.md) — Chromium daemon: 3-5s → 100-200ms, refs via accessibility tree, seguridad localhost | fuentes: 1 | actualizado: 2026-04-06

## Personas

- [Garry Tan](wiki/garry-tan.md) — President & CEO de Y Combinator, builder, creador de gstack y GBrain | fuentes: 1 | actualizado: 2026-04-06

## UI / UX — Principios y Guidelines

- [UX Guidelines — Navegacion y Animacion](wiki/ux-guidelines-navegacion-animacion.md) — Smooth scroll, sticky nav, z-index, timing de animaciones, anti-patterns de layout | fuentes: 1 | actualizado: 2026-04-04
- [UX Guidelines — Formularios y Accesibilidad](wiki/ux-guidelines-formularios-accesibilidad.md) — Labels, validacion inline, ARIA, contraste, skip links, checklist WCAG | fuentes: 1 | actualizado: 2026-04-04
- [UX Guidelines — Mobile y Touch](wiki/ux-guidelines-mobile-touch.md) — Touch targets 44px, responsive breakpoints, teclado virtual, anti-patterns mobile | fuentes: 1 | actualizado: 2026-04-04
- [Patron — Estados UI](wiki/patron-estados-ui.md) — Loading/empty/error/success states, toasts, confirmacion destructiva | fuentes: 1 | actualizado: 2026-04-04

## UI / UX — Sistema de Diseno

- [Sistema de Colores por Dominio](wiki/sistema-colores-por-dominio.md) — Paletas por tipo de producto (SaaS, Fintech, Healthcare...), psicologia del color, badges | fuentes: 1 | actualizado: 2026-04-04
- [Tipografia — Pairings y Sistema](wiki/tipografia-pairings.md) — Font pairings con CSS/Tailwind, escala tipografica DevSar, fuentes prohibidas | fuentes: 1 | actualizado: 2026-04-04
- [Estilos UI por Tipo de Producto](wiki/estilos-ui-por-tipo-producto.md) — Glassmorphism, Neumorphism, Flat, Data-Dense, cuando usar dark mode | fuentes: 1 | actualizado: 2026-04-04
- [Design System Industrial (gstack)](wiki/design-system-industrial.md) — Satoshi + DM Sans + JetBrains Mono, amber accent, dark mode, estetica utilitaria | fuentes: 1 | actualizado: 2026-04-06

## UI / UX — Design Systems Reales (awesome-design-md)

- [DESIGN.md — Formato y Catalogo](wiki/design-md-format.md) — Formato Stitch de Google para AI agents, catalogo de 58 design systems reales | fuentes: 1 | actualizado: 2026-04-06
- [Design Tokens — Comparativa](wiki/design-tokens-comparativa.md) — Tablas cruzadas de 7 sistemas + token architecture 3 capas | fuentes: 2 | actualizado: 2026-04-07
- [Dark Mode — Patrones](wiki/design-patterns-dark-mode.md) — 3 approaches: opacity layers, surface stepping, no dark mode. Regla: nunca pure #000 | fuentes: 1 | actualizado: 2026-04-06
- [Typography — Patrones Reales](wiki/design-patterns-typography.md) — Font stacks de 7 sistemas, tracking comparativo, monospace companions | fuentes: 1 | actualizado: 2026-04-06
- [Shadow Systems — Patrones](wiki/design-patterns-shadow-systems.md) — 5 approaches: shadow-as-border, blue-tinted, multi-layer, border-only, heavy | fuentes: 1 | actualizado: 2026-04-06
- [Spacing — Patrones](wiki/design-patterns-spacing.md) — Gallery emptiness, cinematic pacing, reglas practicas. Base unit 8px universal | fuentes: 1 | actualizado: 2026-04-06

## Herramientas — uipro Design Skills

- [uipro — Skills de Diseño Expandidos](wiki/uipro-design-skills.md) — 6 skills v2.5.0: design (meta-router), design-system, ui-styling, brand, slides, banner-design | fuentes: 1 | actualizado: 2026-04-07

## Stack Tecnico — Next.js / React

- [Next.js 15 — Best Practices](wiki/nextjs-best-practices.md) — App Router, Server Components, caching (breaking change v15), Middleware, env vars | fuentes: 1 | actualizado: 2026-04-04
- [React + shadcn/ui — Patrones](wiki/react-shadcn-patterns.md) — Setup, theming CSS vars, Form + zod, Dialog/Sheet/Tooltip, DataTable | fuentes: 1 | actualizado: 2026-04-04
- [Performance — React y Next.js](wiki/performance-react-ui.md) — Async waterfall, bundle size, barrel imports, RSC, re-renders, JS micro-opts | fuentes: 1 | actualizado: 2026-04-04

## Arquitectura y Conceptos del Sistema

- [Arquitectura del Sistema](wiki/arquitectura-del-sistema.md) — Tres capas (sources/wiki/indice), flujo INGEST, formato de paginas | fuentes: 0 | actualizado: 2026-04-07
- [INGEST — Operacion de Ingest](wiki/ingest.md) — Proceso de incorporacion de fuentes: dialogo LLM-usuario, 8 pasos, diferencia con RAG | fuentes: 0 | actualizado: 2026-04-07
- [ChatGPT File Uploads](wiki/chatgpt-file-uploads.md) — Alternativa RAG on-demand: ventajas, limitaciones, comparativa con LlmBrain | fuentes: 0 | actualizado: 2026-04-07

## Awesome Claude Code — Ecosistema

- [Awesome Claude Code — Catálogo](wiki/awesome-claude-code.md) — repo curado hesreallyhim: 7 categorías, ~150 recursos, criterio de calidad alto | fuentes: 1 | actualizado: 2026-04-07
- [Ralph Wiggum Technique](wiki/ralph-wiggum-technique.md) — loop autónomo hasta done: spec observable, circuit breakers, ralph-orchestrator, ralph-playbook | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Tooling Ecosystem](wiki/claude-code-tooling-ecosystem.md) — claude-devtools, ccflare, claude-squad, claudekit, Dippy, crystal, session managers | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Orquestadores](wiki/claude-code-orquestadores.md) — claude-squad, claude-swarm, Auto-Claude, TSK, Ruflo, sudocode, taxonomía de cuándo usar cada uno | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Hooks Ecosystem](wiki/claude-code-hooks-ecosystem.md) — SDKs TS/Python/PHP/Go, TDD Guard, parry, Dippy, TypeScript Quality Hooks, patterns | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Slash Commands Catalog](wiki/claude-code-slash-commands-catalog.md) — /fix-pr, /common-ground, /tdd, /context-prime, /create-prp por categoría con ejemplos | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — CLAUDE.md Ejemplos Reales](wiki/claude-code-claude-md-ejemplos.md) — Metabase, HASH, LangGraphJS, SteadyStart, qué funciona y qué no | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Agent Skills Catalog](wiki/claude-code-agent-skills-catalog.md) — Trail of Bits, Scientific Skills, Everything CC, Fullstack, RIPER, AB Method, criterios de evaluación | fuentes: 1 | actualizado: 2026-04-07

## Claude Code — Docs Oficiales

- [Claude Code — Hooks](wiki/claude-code-hooks.md) — 25+ eventos del lifecycle, tipos command/prompt/agent/http, exit codes, casos de uso con JSON real | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Skills](wiki/claude-code-skills.md) — SKILL.md: frontmatter, string substitutions, disable-model-invocation, context:fork, preprocessing shell | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Subagentes](wiki/claude-code-subagentes.md) — Context window aislado, specialización por rol, isolation:worktree, Writer/Reviewer pattern | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Memory y CLAUDE.md](wiki/claude-code-memory.md) — Dos sistemas: instrucciones manuales + auto-memory. Scopes, paths frontmatter, límites, qué incluir | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Settings y Configuración](wiki/claude-code-settings.md) — 4 scopes jerárquicos, merge de arrays, permission rules, managed settings para orgs | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Agent Teams](wiki/claude-code-agent-teams.md) — Experimental: teammates con comunicación bidireccional, shared task list, plan approval, casos de uso | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Best Practices](wiki/claude-code-best-practices.md) — La constraint fundamental, workflow Explore→Plan→Implement→Commit, failure patterns, fan-out | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — MCP](wiki/claude-code-mcp.md) — Model Context Protocol: servidores locales/remotos, registry, OAuth, Elicitation, hooks MCP | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Sistema de Permisos](wiki/claude-code-permisos.md) — Modos default/auto/bypass, allow/deny rules, clasificador ML, sandboxing, flujo de decisión | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Context Window y Compaction](wiki/claude-code-context-window.md) — Constraint fundamental, /compact, /rewind, /btw, checkpoints, degradación de performance | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — Patrones de Workflow](wiki/claude-code-workflow-patterns.md) — Explore→Plan→Implement→Commit, non-interactive, fan-out, Writer/Reviewer, git worktrees | fuentes: 1 | actualizado: 2026-04-07
- [Claude Code — CLI Referencia](wiki/claude-code-cli-referencia.md) — Todos los flags CLI, comandos REPL, keybindings, patrones de uso frecuente | fuentes: 1 | actualizado: 2026-04-07

## Claude Agent SDK

- [Agent SDK — Overview](wiki/agent-sdk-overview.md) — query(), tools built-in, hooks callbacks, subagentes, MCP, sesiones, Python/TS | fuentes: 1 | actualizado: 2026-04-07
- [Agent SDK — Hooks](wiki/agent-sdk-hooks.md) — PreToolUse/PostToolUse/Stop, HookMatcher, permissionDecision, updatedInput, webhooks | fuentes: 1 | actualizado: 2026-04-07
- [Agent SDK — Sesiones](wiki/agent-sdk-sessions.md) — continue vs resume vs fork, ClaudeSDKClient, cross-host sessions, session_id | fuentes: 1 | actualizado: 2026-04-07
- [Agent SDK — Subagentes](wiki/agent-sdk-subagentes.md) — Map-Reduce, worktree isolation, AgentTeams experimental, patterns de especialización | fuentes: 1 | actualizado: 2026-04-07

## MCP — Model Context Protocol

- [MCP — Arquitectura](wiki/mcp-arquitectura.md) — Host/Client/Server, stdio vs HTTP, JSON-RPC 2.0, tools/resources/prompts, lifecycle | fuentes: 1 | actualizado: 2026-04-07
- [MCP — Construir un Server](wiki/mcp-build-server.md) — TypeScript + Python, tool/resource/prompt registration, HTTP transport, Inspector | fuentes: 1 | actualizado: 2026-04-07
- [MCP — Seguridad](wiki/mcp-seguridad.md) — Prompt injection, tool shadowing, confused deputy, trust levels, mitigaciones | fuentes: 1 | actualizado: 2026-04-07

## Vercel AI SDK

- [Vercel AI SDK — Overview](wiki/vercel-ai-sdk-overview.md) — generateText/streamText/generateObject, provider Anthropic, useChat, tool calling intro | fuentes: 1 | actualizado: 2026-04-07
- [Vercel AI SDK — Tool Calling](wiki/vercel-ai-sdk-tools.md) — Zod schema, execute, maxSteps, stopWhen, needsApproval, multi-tool paralelo | fuentes: 1 | actualizado: 2026-04-07
- [Vercel AI SDK — Streaming](wiki/vercel-ai-sdk-streaming.md) — TextStream, DataStream, useChat, streamObject, RSC streaming, onChunk, cancellation | fuentes: 1 | actualizado: 2026-04-07
- [Vercel AI SDK — Agentes](wiki/vercel-ai-sdk-agentes.md) — ToolLoopAgent, onStepFinish, multi-agente, PersistentAgent, streaming agent UI | fuentes: 1 | actualizado: 2026-04-07

## Ejemplos y Referencias

- [Ejemplo — RAG vs LLM Wiki](wiki/ejemplo-rag-vs-llm-wiki.md) — Comparativa del patron Karpathy vs RAG tradicional | fuentes: 0 | actualizado: 2026-04-04
