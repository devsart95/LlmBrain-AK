# gstack — Garry Tan

> Fuente: https://github.com/garrytan/gstack
> Fecha de captura: 2026-04-06
> Archivos consultados: README.md, ARCHITECTURE.md, DESIGN.md, ETHOS.md, SKILL.md, CLAUDE.md, AGENTS.md

## Descripcion

gstack es un "software factory" open-source de Garry Tan (President & CEO de Y Combinator) que transforma Claude Code en un equipo de ingenieria virtual. 23 skills especializados como slash commands, organizados como roles: CEO, Designer, Eng Manager, QA, CSO, Release Manager, Doc Engineer.

## Estadisticas clave

- 600,000+ lineas de codigo de produccion en 60 dias (35% tests)
- 10,000-20,000 lineas/dia
- 1,237 contribuciones en GitHub en 2026
- MIT license, gratuito

## Filosofia — ETHOS.md

### 1. Boil the Lake
El costo marginal de completitud es ~0 con AI. Si la implementacion completa cuesta 70 lineas mas que el shortcut, hacer la completa. Siempre.

"Lake" = boilable (100% test coverage de un modulo, todos los edge cases). "Ocean" = no boilable (rewrite completo, migracion multi-quarter). Hervir lagos. Marcar oceanos como fuera de scope.

Tabla de compresion:
| Tipo de tarea | Equipo humano | AI-assisted | Compresion |
|---------------|--------------|-------------|------------|
| Boilerplate / scaffolding | 2 dias | 15 min | ~100x |
| Test writing | 1 dia | 15 min | ~50x |
| Feature implementation | 1 semana | 30 min | ~30x |
| Bug fix + regression test | 4 horas | 15 min | ~20x |
| Architecture / design | 2 dias | 4 horas | ~5x |
| Research / exploration | 1 dia | 3 horas | ~3x |

Anti-patterns:
- "Elijamos B, cubre 90% con menos codigo" (si A es 70 lineas mas, elegir A)
- "Dejemos los tests para un PR de seguimiento" (tests son el lago mas barato)
- "Esto tomaria 2 semanas" (decir: "2 semanas humano / ~1 hora AI-assisted")

### 2. Search Before Building
Tres capas de conocimiento:

Layer 1 — Tried and true: patrones estandar, battle-tested. Riesgo: asumir que lo obvio es correcto sin cuestionar.

Layer 2 — New and popular: best practices actuales, blog posts, tendencias. Buscar pero scrutinizar — "humans are subject to mania. Mr. Market is either too fearful or too greedy."

Layer 3 — First principles: observaciones originales del razonamiento sobre el problema especifico. Las mas valiosas.

El "Eureka moment": entender que hace todo el mundo y POR QUE (L1+L2), aplicar razonamiento de primeros principios a sus assumptions (L3), descubrir por que la convencion esta equivocada. "This is the 11 out of 10."

### 3. User Sovereignty
AI recomienda. El usuario decide. Esta regla overridea todas las demas.

Dos modelos de acuerdo = senal fuerte, no mandato. El usuario siempre tiene contexto que los modelos no: domain knowledge, relaciones de negocio, timing estrategico, gusto personal, planes futuros no compartidos.

Referencias:
- Karpathy: "Iron Man suit" philosophy — AI augmenta, no reemplaza
- Willison: "agents are merchants of complexity" — sin humano en el loop, no sabes que esta pasando
- Anthropic research: usuarios expertos interrumpen Claude MAS seguido, no menos

Patron correcto: generation-verification loop. AI genera, usuario verifica y decide. Nunca saltear verificacion por confianza.

### Como trabajan juntos
- Search Before Building dice: sabe que existe antes de decidir que construir
- Boil the Lake dice: hace la version completa
- Juntos: buscar primero, luego construir la version completa de lo correcto
- Peor outcome: construir version completa de algo que ya existe como one-liner
- Mejor outcome: construir version completa de algo que nadie penso — porque buscaste, entendiste el landscape, y viste lo que todos se perdieron

## Sprint Structure

Think → Plan → Build → Review → Test → Ship → Reflect

### Skills por fase (23 total)

Planning & Strategy:
- /office-hours — interrogacion de producto con 6 forcing questions
- /plan-ceo-review — rethink estrategico con 4 scope modes
- /plan-eng-review — blueprint de arquitectura + testing
- /plan-design-review — auditoria de diseno (ratings 0-10)
- /plan-devex-review — analisis de developer experience (20-45 forcing questions)
- /autoplan — plan completo revieweado en un comando

Design:
- /design-consultation — design system from scratch
- /design-shotgun — exploracion de mockups visuales con comparison board
- /design-html — HTML de produccion desde mockups (framework-aware, 30KB)
- /design-review — auditoria de diseno + fixes con atomic commits

Implementation & Review:
- /review — code review de staff engineer (auto-fix de issues obvios)
- /investigate — debugging sistematico de root cause
- /codex — segunda opinion via OpenAI Codex CLI
- /ship — sync, test, audit coverage, push PR

QA:
- /qa — testing en browser real con fixes y regression tests
- /qa-only — bug report sin cambios de codigo
- /devex-review — auditoria live de DX (onboarding, TTHW, errors)

Deploy & Monitoring:
- /land-and-deploy — merge → CI → deploy → verify production
- /canary — monitoreo post-deploy (console errors, perf, failures)
- /benchmark — Core Web Vitals y baseline de performance

Security & Utilities:
- /cso — Chief Security Officer (OWASP Top 10 + STRIDE)
- /document-release — auto-update de docs del proyecto
- /retro — retrospectiva semanal de ingenieria

Safety:
- /careful — warnings de comandos destructivos
- /freeze — restringir edits a un directorio
- /guard — /careful + /freeze combinados

## Arquitectura tecnica

### Browser persistente
- Chromium daemon de larga vida comunicandose con CLI compilado via localhost HTTP
- Primera llamada ~3s, subsecuentes 100-200ms
- Puerto aleatorio (10000-60000) para evitar conflictos
- Auto-shutdown a 30 min idle
- Login persistence entre comandos

### Bun runtime (elegido sobre Node.js)
- Binarios compilados (~58MB) eliminan dependencias de runtime
- SQLite nativo para cookies de Chromium
- TypeScript nativo sin transpilacion

### Sistema de refs (@refs)
- Elementos referenciados via accessibility tree (@e1, @e2), no DOM
- Evita conflictos con CSP, framework reconciliation, Shadow DOM
- Deteccion de staleness via async count checks

### Seguridad
- Localhost-only binding
- Bearer token con UUID aleatorio, permisos 0o600
- Cookie DB read-only via copias temporales
- Decryption in-memory (PBKDF2 + AES-128-CBC), nunca en disco
- Paths de browser hardcoded para evitar shell injection

### Testing
- Dos tiers: Gate (safety, deterministic, CI) y Periodic (quality, weekly)
- Diff-based selection via git diff con declaracion de dependencias
- E2E tests spawneados como subprocesos claude -p independientes

## Design system

- Estetica industrial/utilitaria, no SaaS generico
- Display: Satoshi (Black 900/Bold 700) — geometrica con calidez
- Body/UI: DM Sans (400/500/600) — limpia y legible
- Data/Code: JetBrains Mono — la fuente de personalidad
- Amber accent (#F59E0B dark / #D97706 light) — evoca cursor de terminal
- Cool zinc grays para neutrales
- Dark mode default, base near-black (#0C0C0C), cards #141414
- SVG noise overlay (opacity 0.03/0.02) para materialidad
- Motion minimal-funcional: 150ms ease-out, 250ms max
- Grid 12 columnas, max-width 1200px, border-radius 12px cards / 8px inputs

## Multi-model review
/review (Claude) + /codex (OpenAI) = analisis cross-model.
Hallazgos superpuestos (alta confianza) vs unicos (perspectiva complementaria).

## Multi-agent coordination
- GStack Browser: Chromium con anti-bot stealth + sidebar agent
- Pair Agent: multiples agentes compartiendo browser con tab isolation
- Handoff Mode: CAPTCHA/MFA → abre Chrome visible, luego resume
- Parallel sprints via Conductor: 10-15 sesiones Claude Code simultaneas
