---
title: Claude Code — CLAUDE.md Ejemplos Reales
type: overview
tags: [claude-code, claude-md, configuración, best-practices]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — CLAUDE.md Ejemplos Reales

> Análisis de CLAUDE.md de proyectos reales: qué incluyen, cómo están estructurados, y qué patrones funcionan.

## Contexto

Los CLAUDE.md de proyectos reales en producción son la mejor fuente para entender qué información realmente ayuda a Claude Code y qué es ruido. La comunidad ha publicado decenas de ejemplos con diferentes approaches.

## Detalle

### El estándar de calidad: pre-commit-hooks (aRustyDev)

El mejor ejemplo del awesome-list. Por qué:
- **Thorough sin ser verbose**: cubre todo lo que Claude necesita sin padding
- **No grita en CAPS**: sin `NUNCA HAGAS X`, sin `SIEMPRE USA Y` en mayúsculas
- **Cada línea tiene propósito**: no hay secciones decorativas
- **Adaptable**: no impone un workflow rígido

Estructura que usa:
```markdown
# Project: pre-commit-hooks

## Commands
- Install: `pip install -e ".[dev]"`
- Test: `pytest tests/ -v`
- Lint: `pre-commit run --all-files`

## Architecture
[Descripción concisa de los componentes]

## Code Conventions
[Solo las que no son obvias del código]

## Testing Requirements
[Lo que el CI verifica y lo que no]
```

**Lección:** Un CLAUDE.md no es un manual de usuario. Es contexto que Claude no puede inferir del código.

---

### CLAUDE.md de proyectos grandes

#### Metabase (metabase)

Para un codebase enorme en Clojure/ClojureScript:
```markdown
## Development Workflow
- REPL-driven: always prefer incremental development over big bang changes
- Start with the smallest possible change that could work
- Test in the REPL before writing to disk
- Step-by-step: never skip steps even when they seem obvious

## Clojure Style
- Use threading macros (-> and ->>) for clarity
- Prefer pure functions; isolate side effects
- No reflection warnings in production code
```

**Lección:** Para stacks inusuales (Clojure), el CLAUDE.md tiene que enseñarle a Claude el paradigma, no solo los comandos.

#### HASH (hashintel)

Codebase grande con Rust + múltiples lenguajes:
```markdown
## Repository Structure
[Mapa detallado de qué está dónde]

## Coding Standards
- Rust: all public functions must have doc comments
- Error handling: use our custom error types, not anyhow in library code
- Testing: table-driven tests preferred

## PR Review Process
1. Self-review checklist before requesting review
2. All CI must pass
3. At least one engineer familiar with the component
```

**Lección:** En repos grandes, el mapa del territorio es tan importante como las convenciones.

#### LangGraphJS (langchain-ai)

Monorepo con yarn workspaces:
```markdown
## Build Commands
- Full build: `yarn build`
- Single package: `cd packages/[name] && yarn build`
- Tests: `yarn test` (all) or `yarn test --filter [package]`

## TypeScript Style
- All exports must be typed explicitly (no `any`)
- Generics preferred over `unknown` casts
- Use `type` for pure type aliases, `interface` for object shapes

## Architecture: Layered Libraries
- Core (no deps): packages/langgraph
- Integrations (with deps): packages/langgraph-[provider]
- Examples: packages/langgraph-examples (no re-export constraints)
```

**Lección:** La arquitectura layered necesita ser explícita — Claude no infiere qué puede depender de qué.

---

### CLAUDE.md por dominio

#### SteadyStart (steadycursor)

Ejemplo de CLAUDE.md para project scaffolding — define el "rol" de Claude:
```markdown
## Claude's Role
You are a senior software architect helping build this project.
Your job: make architectural decisions, write production-quality code,
and challenge requirements that seem suboptimal.

## Communication Style
- Direct and technical
- If a requirement seems wrong, say so once and clearly
- Don't repeat the same question twice

## Permissions
- You may refactor code you're touching if you see clear improvements
- You may not change the tech stack without explicit approval
- You may add tests for code you write

## Documentation
After each session, update CONTEXT.md with what changed and why.
```

**Lección:** Definir el rol, los permisos y el estilo de comunicación reduce fricción y ambigüedad.

#### Pareto Mac (ParetoSecurity)

Para una app de seguridad macOS:
```markdown
## Build
- macOS only: `xcodebuild`
- Tests: `xcodebuild test -scheme ParetoSecurity`

## Security Checks Implementation
Each check must:
1. Be deterministic (same result on same system state)
2. Have a clear remediation message
3. Never collect or transmit data
4. Run in <100ms

## Code Style
- No force unwraps (!): use guard let or if let
- All async code uses async/await, not callbacks
- Log levels: os.log for debug, never print()
```

**Lección:** Restricciones de dominio (seguridad, performance) van explícitamente. No asumir que Claude las infiere.

#### AVS Vibe Developer Guide (Layr-Labs)

Para blockchain/EigenLayer:
```markdown
## Domain Terminology
- AVS = Actively Validated Service
- Operator = entity running the AVS
- Restaker = ETH staker delegating to an operator
[...20 más términos con definiciones]

## Naming Conventions
- Files: kebab-case for everything
- Variables: camelCase, with domain terms spelled correctly (restaker not re_staker)

## Prompt File Naming
PRD files: [feature]-prd.md
Spec files: [component]-spec.md
```

**Lección:** En dominios técnicos especializados, el glosario es esencial. Claude puede asumir términos incorrectamente.

---

### CLAUDE.md con MCP y Scaffolding

#### Basic Memory (basicmachines-co)

Framework innovador con MCP para comunicación LLM-markdown bidireccional:
```markdown
## Memory Architecture
This project uses MCP for persistent memory:
- Read: `memory://read/{topic}` → retorna markdown con contexto
- Write: `memory://write/{topic}` → persiste decisiones de diseño
- Search: `memory://search?q={query}` → busca en toda la base de conocimiento

## How to Use Memory
Before starting any task:
1. Search memory for related context: `memory://search?q=[topic]`
2. Read relevant entries
3. After completing: write key decisions to memory
```

**Lección:** Si el proyecto usa MCP servers, el CLAUDE.md debe documentar cómo y cuándo usarlos.

#### claude-code-mcp-enhanced (grahama1970)

CLAUDE.md con enforcement explícito:
```markdown
## CRITICAL: Testing Requirements
- Every function must have tests BEFORE implementation
- Run tests after EVERY change: `npm test`
- If tests fail: fix them before proceeding to the next task
- Zero tolerance for `any` in TypeScript

## Code Examples
[Includes actual code examples of the patterns expected]

## Compliance Checks
Before committing, verify:
[ ] TypeScript compiles without errors
[ ] All tests pass
[ ] No `console.log` in production code
[ ] No commented-out code
```

**Lección:** Los checklists de compliance en el CLAUDE.md funcionan mejor que instrucciones en prosa.

---

### Patterns que funcionan vs los que no

**Funcionan:**
- Comandos exactos para build/test/lint
- Mapa de estructura del repo para proyectos grandes
- Glosario de términos del dominio
- Ejemplos de código de los patterns esperados
- Checklists de compliance binarios
- Definición del rol y permisos de Claude

**No funcionan bien:**
- Instrucciones en ALL CAPS (no asusta a Claude)
- Reglas que se contradicen con el código actual
- Listas exhaustivas de "nunca hagas X" para casos obvios
- Historia del proyecto (es para git log, no para Claude)
- Información deducible del código o del stack

**Señal de que el CLAUDE.md necesita actualización:**
- Claude ignora instrucciones repetidamente → es confuso o contradice el código
- Claude pregunta las mismas cosas de nuevo → falta información no deducible
- El CLAUDE.md tiene >200 líneas → probablemente hay ruido

---

### Estructura recomendada

```markdown
# [Project Name]

## Commands
[Build, test, lint — con comandos exactos]

## Architecture
[Solo lo que no se puede inferir del código]

## Code Conventions
[Solo las no-obvias o que difieren del standard del lenguaje]

## Domain Context
[Glosario, restricciones de dominio, decisiones de diseño]

## Claude's Role
[Permisos, qué puede cambiar, qué debe preguntar]
```

## Conexiones
- Relacionado con: [[claude-code-memory]], [[claude-code-settings]]
- Para el CLAUDE.md global de un dev: ver CLAUDE.md en `~/.claude/`
- Archivos complementarios: [[context-engineering-patterns]]

## Fuentes
- `https://github.com/hesreallyhim/awesome-claude-code` — sección CLAUDE.md Files

---

## Timeline

- 2026-04-07: página creada desde awesome-claude-code
