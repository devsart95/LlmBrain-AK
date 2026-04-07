---
title: Claude Code — Agent Teams
type: concept
tags: [claude-code, agent-teams, paralelismo, multi-agente, experimental]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Agent Teams

> Sistema experimental de múltiples instancias de Claude que se coordinan directamente entre sí via shared task list y mailbox, a diferencia de subagentes que solo reportan al agente principal.

---

## Contexto

Agent teams es la evolución del modelo de subagentes hacia coordinación horizontal. En vez de un agente principal que orquesta N subagentes, los teammates tienen visibilidad del trabajo total, pueden tomar tareas del pool, y enviarse mensajes directamente. Es potente y complejo — está marcado como experimental.

Requiere `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

## Detalle

### Habilitar

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

O en `settings.json`:
```json
{
  "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
}
```

### Arquitectura de un team

```
Team Lead (sesión principal)
├── Task List (compartida, con file locking)
│   ├── Task 1: "Implementar auth middleware" [claiming: teammate-1]
│   ├── Task 2: "Tests de integración" [available]
│   └── Task 3: "Documentar API" [claiming: teammate-2]
├── Mailbox (mensajes directos entre agentes)
│   ├── teammate-1 → lead: "Auth implementado, necesito review del schema"
│   └── lead → teammate-2: "Priorizar docs de /auth endpoints"
├── Teammate 1
└── Teammate 2
```

**Team lead**: crea tareas, aprueba planes de teammates, tiene visibilidad total, decide merges.

**Teammates**: reclaman tareas del pool, ejecutan, reportan completado, se comunican con lead y otros teammates.

### Diferencia clave con subagentes

| Aspecto | Subagentes | Agent Teams |
|---------|-----------|-------------|
| Comunicación | Solo upstream (al principal) | Bidireccional entre cualquier agente |
| Task distribution | Manual (main asigna) | Automática (claiming del pool) |
| Contexto compartido | No | Shared task list visible a todos |
| Coordinación | Centralizada | Distribuida |
| Confiabilidad | Alta (probado) | Media (experimental) |
| Ideal para | Tareas bien definidas | Investigación paralela abierta |
| Costo de tokens | Lineal con uso | Lineal con N teammates |

### Display modes

**In-process** (default): los teammates corren en el mismo proceso, visibles en el REPL con `Shift+Down` para ciclar entre ellos.

**Tmux**: cada teammate en un pane de tmux separado. Visual, permite seguir el progreso de todos en paralelo.

**iTerm2 split panes**: similar a tmux pero en la terminal de macOS.

Configurar en `~/.claude.json`:
```json
{
  "teammateMode": "auto"
}
```

`"auto"` detecta el entorno y elige el mejor modo. `"in-process"` fuerza el modo embebido. `"tmux"` fuerza tmux.

### Plan approval para teammates

Antes de ejecutar, cada teammate presenta su plan al team lead para aprobación. Hasta que el lead aprueba, el teammate está en **read-only mode**: puede explorar y planificar pero no modificar archivos.

Esto previene que teammates vayan en direcciones incorrectas desperdiciando tokens.

```
Teammate 1: "Plan para auth middleware:
  1. Crear src/middleware/auth.ts con verificación JWT
  2. Agregar middleware a todas las rutas protegidas en routes/
  3. Tests en tests/middleware/auth.test.ts
  ¿Procedo?"

Lead: "Aprobado, pero usa Better Auth en lugar de JWT manual"

Teammate 1: [ejecuta con el cambio indicado]
```

### Task claiming con file locking

El task pool usa file locking para evitar race conditions cuando múltiples teammates intentan tomar la misma tarea simultáneamente:

```
Task pool state:
- auth-middleware: available
- tests: available
- docs: available

Teammate 1 intenta claim auth-middleware → lock adquirido → status: claiming
Teammate 2 intenta claim auth-middleware → lock unavailable → toma siguiente disponible (tests)
```

### Team config storage

```
~/.claude/teams/
└── <team-name>/
    └── config.json
```

```json
{
  "name": "feature-team",
  "teammates": [
    { "name": "backend-dev", "model": "claude-sonnet-4-5", "skills": ["api-patterns"] },
    { "name": "test-writer", "model": "claude-haiku-4", "skills": ["testing-patterns"] }
  ],
  "maxConcurrentTasks": 3
}
```

### Casos de uso ideales

**Investigación paralela** — cuando el espacio del problema es amplio:
```
Lead crea tasks:
- "Investigar autenticación: OAuth2 vs Better Auth vs Lucia"
- "Investigar DB: PostgreSQL vs PlanetScale para este caso de uso"
- "Investigar hosting: Vercel vs Railway vs VPS para los reqs dados"

3 teammates en paralelo → reportan → Lead sintetiza decisión
```

**Nuevos módulos independientes:**
```
Feature: sistema de facturación
Tasks:
- "Implementar modelo de datos: Invoice, LineItem, Payment"
- "Implementar API REST: CRUD de facturas"
- "Implementar integración con Stripe"
- "Implementar PDF generation"

4 teammates en paralelo (módulos sin dependencias entre sí)
```

**Debugging con hipótesis competidoras:**
```
Bug: memory leak en producción (causa desconocida)
Tasks (hipótesis):
- "Investigar memory leak por event listeners no removidos"
- "Investigar memory leak por cache sin límite en Redis client"
- "Investigar memory leak por closures en worker pool"

3 teammates prueban las 3 hipótesis en paralelo
```

**Parallel code review:**
```
PR grande con cambios en auth, API, y frontend
Tasks:
- "Revisar cambios de seguridad en auth/ (OWASP checklist)"
- "Revisar performance de queries en src/db/"
- "Revisar cobertura de tests para los nuevos endpoints"
```

### Hooks para quality gates en teams

```json
{
  "hooks": [
    {
      "event": "TaskCompleted",
      "hook": {
        "type": "command",
        "command": "npm test -- --testPathPattern=$CLAUDE_TASK_AFFECTED_FILES 2>&1"
      }
    },
    {
      "event": "TeammateIdle",
      "hook": {
        "type": "command",
        "command": "echo \"Teammate $CLAUDE_TEAMMATE_NAME idle — asignar nueva tarea si disponible\""
      }
    }
  ]
}
```

### Recomendaciones prácticas

- **3-5 teammates** es el sweet spot — más es overhead de coordinación
- **5-6 tasks por teammate** como máximo para evitar contexto demasiado fragmentado
- **Tasks atómicas e independientes** — si una task depende de otra, modelar la dependencia explícitamente en la descripción
- **Evitar en**: tareas donde el orden importa mucho, cambios que se solapan en los mismos archivos, debugging donde la hipótesis es clara

### Limitaciones actuales

- **No session resumption** con in-process teammates — si se cierra Claude Code, el team no se puede reanudar
- **Task status puede lagear** — el display de progreso no es siempre en tiempo real
- **No nested teams** — un teammate no puede crear su propio team
- **Experimental** — API puede cambiar entre versiones

### Costo de tokens

Los tokens escalan linealmente con el número de teammates activos. Un team de 4 con un modelo expensive (Opus) puede consumir 4x el costo de una sesión simple. Estrategia de ahorro:

```json
{
  "teammates": [
    { "name": "lead", "model": "claude-opus-4" },        // lead en Opus
    { "name": "researcher", "model": "claude-haiku-4" }, // búsqueda en Haiku
    { "name": "coder", "model": "claude-sonnet-4-5" },   // implementación en Sonnet
    { "name": "tester", "model": "claude-haiku-4" }      // tests en Haiku
  ]
}
```

## Conexiones

- Relacionado con: [[claude-code-subagentes]], [[claude-code-hooks]], [[claude-code-settings]]
- Contrasta con: [[claude-code-subagentes]] (coordinación unilateral vs bilateral)
- Parte de: [[claude-code-workflow-patterns]]
- Habilita patrones de: [[ai-development-workflows]], [[context-engineering-patterns]]
- Ver también: [[claude-code-best-practices]] (cuándo usar teams vs subagentes)

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
