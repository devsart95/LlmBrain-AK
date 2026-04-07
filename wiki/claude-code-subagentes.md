---
title: Claude Code — Subagentes
type: concept
tags: [claude-code, subagentes, agentes, paralelismo, contexto]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Subagentes

> Agentes especializados con context window propio, system prompt aislado, tools restringidos y permisos independientes, que reportan resultados al agente principal.

---

## Contexto

Los subagentes resuelven el problema de contaminación de contexto en tareas largas de exploración. Cuando Claude necesita entender 50 archivos para tomar una decisión, hacerlo en el contexto principal consume tokens que se necesitan para implementar. Un subagente explora, resume y reporta — dejando el contexto principal libre para el trabajo real.

Son también el mecanismo de especialización: un subagente puede correr en Haiku (barato, rápido) para tareas de búsqueda mientras el agente principal corre en Opus.

## Detalle

### Definición de un subagente

```
.claude/agents/<name>.md          # proyecto
~/.claude/agents/<name>.md        # usuario (global)
```

```yaml
---
name: security-reviewer
description: "Audits code for security issues: OWASP Top 10, injection, secrets exposure, auth flaws."
tools: [Read, Grep, Glob, Bash]   # allowlist — solo estos tools disponibles
model: claude-opus-4               # modelo específico
disallowed-tools: [Write, Edit]    # blocklist adicional
skills: [api-patterns, auth-guide] # skills preloaded en system prompt
mcpServers: [github]               # MCP servers disponibles
---

# Security Reviewer Agent

Eres un especialista en seguridad de aplicaciones. Tu único rol es auditar código.

Cuando el agente principal te invoque:
1. Leer los archivos especificados
2. Buscar patrones de vulnerabilidad OWASP Top 10
3. Reportar hallazgos con severidad (critical/high/medium/low) y ubicación exacta
4. NO modificar ningún archivo

Formato de reporte:
- [SEVERITY] Descripción breve — archivo:línea
```

### Frontmatter fields

| Campo | Descripción |
|-------|-------------|
| `name` | Identificador único (kebab-case) |
| `description` | Cuándo usar este agente (ayuda al agente principal a elegir) |
| `tools` | Allowlist de tools disponibles |
| `disallowed-tools` | Blocklist adicional |
| `model` | Modelo a usar (puede ser más barato que el principal) |
| `skills` | Skills preloaded en el system prompt del subagente |
| `mcpServers` | MCP servers disponibles para el subagente |
| `isolation` | `"worktree"` para aislamiento git |

### Scopes de definición

- **Proyecto** `.claude/agents/` — disponible solo en este proyecto, se versiona con git
- **Usuario** `~/.claude/agents/` — disponible en todos los proyectos
- **Plugin** — provisto por extensiones de terceros
- **CLI** — definido en argumentos de línea de comando

El agente principal descubre automáticamente todos los agentes en scope. La `description` es clave — Claude la usa para decidir cuándo invocar qué subagente.

### `isolation: "worktree"` — aislamiento total

```yaml
---
name: experimental-refactor
isolation: worktree
tools: [Read, Write, Edit, Bash]
---
```

Con `isolation: worktree`:
- Se crea un git worktree temporal en una rama nueva
- El subagente trabaja en ese worktree, completamente aislado del working tree principal
- Al terminar, el agente principal puede revisar los cambios y decidir si mergear
- Si el subagente no hizo cambios, el worktree se limpia automáticamente

Útil para: refactoring experimental, probar arquitecturas alternativas, explorar soluciones sin riesgo.

### Skills preloaded en subagentes

El campo `skills` inyecta el contenido completo del skill en el system prompt del subagente antes de que empiece:

```yaml
---
name: api-builder
skills: [api-patterns, zod-schemas, auth-guide]
---
```

Equivale a que el subagente ya "sabe" todo lo que dice cada skill antes de recibir la tarea. No necesita invocarlos — ya están en contexto.

### Auto-memory por subagente

Cada subagente puede tener su propia `MEMORY.md`. Claude Code la crea automáticamente en:
```
~/.claude/projects/<project>/agents/<agent-name>/memory/MEMORY.md
```

Permite que un subagente "recuerde" patrones descubiertos en sesiones anteriores — por ejemplo, un security-reviewer que acumula conocimiento sobre vulnerabilidades específicas del proyecto.

### Diferencia subagente vs agent team

| Aspecto | Subagente | Agent Team (experimental) |
|---------|-----------|--------------------------|
| Comunicación | Solo reporta al principal | Teammates se comunican entre sí |
| Coordinación | Centralizada en principal | Distribuida via task list + mailbox |
| Paralelismo | Manual (main lanza múltiples) | Automático (task claiming) |
| Visibilidad | Principal ve resultado final | Shared task list visible a todos |
| Complejidad | Simple, confiable | Complejo, experimental |
| Costo | Proporcional al uso | Escala con N teammates |

### Casos de uso

**Investigación de codebase** — el caso más común:
```
Principal: "Necesito entender cómo funciona el sistema de autenticación"
→ Lanza subagente Explore con tools: [Read, Grep, Glob]
→ Subagente lee 20 archivos, resume en 500 palabras
→ Principal recibe resumen, contexto limpio, implementa el cambio
```

**Verificación post-implementación:**
```
Principal: "Implementé el feature, verificá que todo esté bien"
→ Lanza subagente con tools: [Bash, Read] para correr tests
→ Subagente reporta test results sin consumir contexto principal
```

**Routing a modelos baratos:**
```yaml
---
name: file-finder
description: "Find files matching a description in the codebase"
tools: [Glob, Grep, Read]
model: claude-haiku-4    # Haiku para búsqueda simple
---
```

**Especialización por capa:**
```
.claude/agents/
├── db-expert.md       # PostgreSQL, índices, queries
├── api-reviewer.md    # REST conventions, zod, rate limiting
├── ui-auditor.md      # Accesibilidad, estados UI, responsive
└── security-reviewer.md  # OWASP, injection, secrets
```

### Patrón Writer/Reviewer

Dos sesiones independientes para calidad máxima:

```bash
# Sesión 1: implementa
claude -p "Implementa el feature de reset de contraseña"

# Sesión 2: revisa (contexto completamente separado, sin sesgos)
claude --agent security-reviewer -p "Revisa la implementación de reset de contraseña en auth/"
```

El reviewer no tiene el contexto del writer — ve el código con ojos frescos, sin anclas cognitivas.

### Paralelización con worktrees

```bash
# Tres subagentes en paralelo, cada uno en su worktree
claude --agent feature-a &
claude --agent feature-b &
claude --agent feature-c &
wait

# Mergear los tres resultados
```

### Hookear SubagentStart/SubagentStop

```json
{
  "hooks": [
    {
      "event": "SubagentStart",
      "hook": {
        "type": "command",
        "command": "echo \"[$(date)] Subagente iniciado: $CLAUDE_SUBAGENT_NAME\" >> .claude/subagent.log"
      }
    },
    {
      "event": "SubagentStop",
      "hook": {
        "type": "command",
        "command": "echo \"[$(date)] Subagente terminado: $CLAUDE_SUBAGENT_NAME\" >> .claude/subagent.log"
      }
    }
  ]
}
```

### Ejemplo completo — security-reviewer

```yaml
---
name: security-reviewer
description: "Audits code for OWASP Top 10, injection, secrets exposure, auth flaws, insecure dependencies. Use after implementing auth, payment, or user-data features."
tools: [Read, Grep, Glob, Bash]
model: claude-opus-4
disallowed-tools: [Write, Edit, WebFetch]
---

# Security Reviewer

Especialista en seguridad de aplicaciones. Solo lees y reportas — nunca modificas.

## Protocolo de auditoría

1. **Reconocimiento:** mapear los archivos relevantes con Glob/Grep
2. **Análisis estático:** buscar patrones de vulnerabilidad
3. **Verificación de dependencias:** `npm audit --json`
4. **Reporte estructurado:** severidad + ubicación + remediación

## Checklist OWASP Top 10
- [ ] A01 Broken Access Control — verificar middleware de auth en rutas
- [ ] A02 Cryptographic Failures — buscar secrets hardcodeados, HTTP sin TLS
- [ ] A03 Injection — SQL raw sin params, eval(), child_process con input usuario
- [ ] A05 Security Misconfiguration — CORS *, headers de seguridad faltantes
- [ ] A07 Auth Failures — session management, rate limiting en auth endpoints
- [ ] A09 Logging Failures — no loguear passwords, tokens, PII

Formato de hallazgo:
`[CRITICAL|HIGH|MEDIUM|LOW] Descripción — archivo:línea — Remediación sugerida`
```

## Conexiones

- Relacionado con: [[claude-code-skills]], [[claude-code-agent-teams]], [[claude-code-context-window]]
- Parte de: [[claude-code-workflow-patterns]], [[claude-code-settings]]
- Habilita patrones de: [[ai-development-workflows]], [[context-engineering-patterns]]
- Ver también: [[claude-code-hooks]] (SubagentStart/SubagentStop), [[claude-code-memory]] (auto-memory por subagente)

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
