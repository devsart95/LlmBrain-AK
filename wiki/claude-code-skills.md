---
title: Claude Code — Skills
type: concept
tags: [claude-code, skills, slash-commands, workflow]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Skills

> Archivos SKILL.md que definen comandos slash personalizados con control fino sobre invocación, contexto, modelo y permisos.

---

## Contexto

Los skills reemplazaron y extendieron el sistema de commands de Claude Code. A diferencia de un simple archivo de instrucciones, un skill puede controlar si Claude lo invoca automáticamente, si requiere aprobación del usuario, qué tools tiene disponibles, en qué modelo corre, y si opera en un subagente aislado. Son la unidad de composición del comportamiento de Claude Code.

Directorio: `.claude/skills/<name>/SKILL.md`

## Detalle

### Frontmatter fields

```yaml
---
name: deploy
description: "Deploy to production via Docker Compose. Runs tests, builds image, pushes to registry, applies to server."
disable-model-invocation: true     # solo usuario puede invocar
user-invocable: false              # solo Claude puede invocar (background knowledge)
allowed-tools: [Bash, Read]        # allowlist de tools disponibles
disallowed-tools: [Write, Edit]    # blocklist de tools
model: claude-opus-4               # modelo específico para este skill
effort: high                       # nivel de esfuerzo (low/medium/high)
context: fork                      # aislar en subagente
agent: Explore                     # tipo de agente (Explore/Plan/general-purpose)
hooks:                             # hooks locales al skill
  - event: Stop
    hook: { type: command, command: "notify-team.sh" }
paths: ["src/api/**/*.ts"]         # skill se activa solo para estos archivos
shell: bash                        # shell para bloques de código
argument-hint: "<environment>"     # hint para el usuario sobre qué argumento pasar
---
```

### String substitutions

| Placeholder | Descripción |
|-------------|-------------|
| `$ARGUMENTS` | Todos los argumentos pasados al skill |
| `$ARGUMENTS[N]` | Argumento N (base 0) |
| `$N` | Shorthand para `$ARGUMENTS[N]` |
| `${CLAUDE_SESSION_ID}` | ID de la sesión actual |
| `${CLAUDE_SKILL_DIR}` | Directorio del skill (para referencias relativas) |

Ejemplo:
```markdown
Deploy `$ARGUMENTS[0]` to `$ARGUMENTS[1]` environment.
Session: ${CLAUDE_SESSION_ID}
```

### `disable-model-invocation: true`

El skill **no puede ser invocado automáticamente por Claude**. Solo el usuario puede llamarlo con `/skill-name`. Usar para:
- Deploy a producción
- Commits y pushes
- Envíos de email/SMS
- Cualquier acción irreversible con side effects externos

```yaml
---
name: deploy-prod
description: "Deploy to production. User-invocable only."
disable-model-invocation: true
allowed-tools: [Bash]
---
```

### `user-invocable: false`

El skill es **invisible para el usuario** en el menú slash. Solo Claude puede invocarlo internamente. Usar para:
- Knowledge bases especializadas
- Contexto de dominio que Claude consulta cuando necesita
- Lógica de preprocessing interna

```yaml
---
name: project-patterns
description: "Internal patterns for this codebase. Reference when implementing new features."
user-invocable: false
---

## Architecture Patterns
- Services in src/services/, always extend BaseService
- Repository pattern for DB access
- Zod schemas in src/schemas/
```

### `context: fork` con `agent`

Corre el skill en un subagente completamente aislado. El contexto del subagente no contamina el contexto principal.

```yaml
---
name: security-audit
context: fork
agent: Explore
model: claude-opus-4
description: "Run security audit on the codebase. Isolated context."
---
```

Tipos de agente:
- `Explore` — solo lectura, optimizado para búsqueda en codebase
- `Plan` — genera plan sin ejecutar
- `general-purpose` — agente completo con todos los tools

### Sintaxis `!`command`` — preprocessing shell

Ejecuta un comando shell **antes** de enviar el contenido a Claude. El output reemplaza el bloque:

```markdown
# PR Review Skill

Context del PR actual:
!`gh pr diff HEAD`

Archivos modificados:
!`git diff --name-only main...HEAD`

Revisa los cambios anteriores buscando:
- Security issues
- Performance regressions
- Missing tests
```

El shell se ejecuta en tiempo de invocación. Permite inyectar contexto dinámico sin que Claude tenga que correr comandos.

### `paths` — activación condicional por archivo

El skill solo se carga en el contexto cuando Claude está trabajando con archivos que matcheen el glob:

```yaml
---
name: api-patterns
paths: ["src/api/**/*.ts", "src/routes/**/*.ts"]
user-invocable: false
description: "API conventions for this project"
---

## API Conventions
- Always use zod validation middleware
- Return { data, error } structure
- Rate limit with express-rate-limit on auth routes
```

Útil en monorepos para tener skills específicos por servicio o capa.

### Supporting files

Un skill puede tener archivos adicionales en su directorio:

```
.claude/skills/deploy/
├── SKILL.md           # definición principal
├── reference.md       # documentación de referencia
├── examples/          # ejemplos de uso
│   ├── simple.md
│   └── rollback.md
└── scripts/
    └── health-check.sh
```

Referenciar con `${CLAUDE_SKILL_DIR}`:
```markdown
Ver referencia: ${CLAUDE_SKILL_DIR}/reference.md
```

### Bundled skills del sistema

| Skill | Descripción |
|-------|-------------|
| `/batch` | Orquesta migraciones masivas en paralelo con worktrees |
| `/claude-api` | Integración con Anthropic SDK |
| `/debug` | Debugging con root cause analysis |
| `/loop` | Ejecuta skills en intervalo recurrente |
| `/simplify` | Revisa código para reuso y calidad |

### Reglas de permission para skills

En `settings.json`:
```json
{
  "permissions": {
    "allow": ["Skill(review)"],
    "deny": ["Skill(deploy *)"]
  }
}
```

Sintaxis: `Skill(name)` o `Skill(name *)` para skills con argumentos.

### Ejemplo completo — deploy skill

```markdown
---
name: deploy
description: "Deploy app to production. Runs tests, builds Docker image, pushes to registry, applies docker-compose."
disable-model-invocation: true
allowed-tools: [Bash]
argument-hint: "<service-name>"
---

# Deploy $ARGUMENTS[0] to Production

Pre-flight checks:
!`npm test -- --passWithNoTests 2>&1 | tail -5`
!`docker info > /dev/null 2>&1 && echo "Docker OK" || echo "Docker NOT running"`

Sigue estos pasos en orden:
1. Correr tests: `npm test`
2. Build: `docker build -t registry.example.com/$ARGUMENTS[0]:latest .`
3. Push: `docker push registry.example.com/$ARGUMENTS[0]:latest`
4. Deploy: `ssh deploy@prod 'docker compose pull $ARGUMENTS[0] && docker compose up -d $ARGUMENTS[0]'`
5. Health check: `curl -f https://app.example.com/health`

Si algún paso falla, reportar el error y NO continuar.
```

### Ejemplo — skill con visual output

```markdown
---
name: metrics-report
description: "Generate visual metrics report from logs"
allowed-tools: [Bash, Read]
---

Genera un reporte HTML de las métricas del proyecto:
!`cat logs/metrics.json`

Usa Python para generar un HTML con charts. Guarda en /tmp/report.html y abrelo con `open /tmp/report.html`.
```

### Descripción efectiva

- Máximo 250 caracteres (límite de discovery)
- Front-load el caso de uso principal
- Mencionar cuándo usar vs cuándo NO usar

```yaml
# Mal
description: "Tool for various deployment tasks"

# Bien
description: "Deploy to production via Docker Compose. Runs tests first. Use only for production; for staging use /deploy-staging."
```

### Skill discovery en monorepos

Claude busca skills en subdirectorios automáticamente. En un monorepo:
```
apps/
  api/.claude/skills/
  web/.claude/skills/
packages/
  shared/.claude/skills/
.claude/skills/            # root — disponible en todo el monorepo
```

## Conexiones

- Relacionado con: [[claude-code-hooks]], [[claude-code-subagentes]], [[claude-code-permisos]]
- Parte de: [[claude-code-workflow-patterns]], [[claude-code-settings]]
- Habilita patrones de: [[ai-development-workflows]], [[agent-skills-ecosystem]]
- Ver también: [[claude-code-agent-teams]] (skills preloaded en teammates), [[claude-code-memory]] (skills como knowledge bases)

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
