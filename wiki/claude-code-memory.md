---
title: Claude Code — Memory y CLAUDE.md
type: concept
tags: [claude-code, memory, claude-md, contexto, configuracion]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Memory y CLAUDE.md

> Dos sistemas complementarios: CLAUDE.md (instrucciones que vos escribís) y auto-memory (notas que Claude escribe automáticamente). Juntos persisten conocimiento entre sesiones.

---

## Contexto

El context window se vacía con cada sesión nueva. CLAUDE.md es la solución manual: instrucciones permanentes que Claude lee al inicio. Auto-memory es la solución automática: Claude toma notas mientras trabaja y las recarga la próxima sesión. Entender cuándo usar cada uno y cómo estructurarlos es fundamental para sesiones efectivas.

## Detalle

### Los dos sistemas

| Sistema | Quién escribe | Cuándo se carga | Cuándo usar |
|---------|---------------|-----------------|-------------|
| `CLAUDE.md` | Vos | Inicio de sesión, siempre | Convenciones estables, comandos, reglas del proyecto |
| Auto-memory `MEMORY.md` | Claude | Inicio de sesión (últimas 200 líneas) | Hechos descubiertos, decisiones tomadas, bugs encontrados |

### CLAUDE.md — locations por scope

```
~/.claude/CLAUDE.md                    # global — aplica a todos los proyectos
./CLAUDE.md                            # proyecto — versionado con git
./CLAUDE.local.md                      # local — no versionado (overrides personales)
```

**Managed policy** (organizaciones): deployado via MDM/Ansible, sobreescribe todos los demás scopes para políticas corporativas.

Orden de carga: managed → global → proyecto → local. El contenido se acumula (no se sobreescribe entre scopes).

### `.claude/rules/` — reglas modulares

Directorio opcional para organizar reglas por tema:

```
.claude/rules/
├── api.md           # convenciones de API
├── database.md      # patrones de DB
├── security.md      # checklist de seguridad
└── frontend.md      # reglas de UI
```

Cada archivo en `.claude/rules/` se carga automáticamente. El campo `paths` en frontmatter limita el scope:

```yaml
---
paths: ["src/api/**/*.ts", "src/routes/**/*.ts"]
---

# API Rules
- Siempre validar con zod en el boundary
- Rate limit en endpoints de auth
```

Solo se carga cuando Claude trabaja con archivos que matcheen el glob. En proyectos grandes, esto evita cargar reglas irrelevantes y optimiza el context window.

### `@path/to/import` — imports en CLAUDE.md

```markdown
# Mi proyecto

@.claude/rules/api.md
@.claude/rules/database.md
@docs/architecture.md

## Comandos de desarrollo
- `npm run dev` — servidor en puerto 3000
```

Permite modularizar CLAUDE.md sin duplicar contenido. Las reglas globales usan este mecanismo para importar reglas específicas de proyecto.

### Auto-memory (v2.1.59+)

Habilitado por default. Claude escribe notas automáticamente cuando descubre algo útil:

- Patrones del codebase
- Bugs recurrentes y sus soluciones
- Convenciones no documentadas
- Decisiones de arquitectura tomadas en sesión
- Preferencias del usuario observadas

**Activar/desactivar:**
- `/memory` en el REPL — toggle interactivo y lista de archivos cargados
- `autoMemoryEnabled: false` en `settings.json` — deshabilitar globalmente

**Storage location:**
```
~/.claude/projects/<project-hash>/memory/
├── MEMORY.md              # índice principal (máx 200 líneas / 25KB)
├── debugging.md           # tema específico
├── patterns.md            # tema específico
└── architecture.md        # tema específico
```

### Límite de auto-memory

Solo las **primeras 200 líneas o 25KB** de `MEMORY.md` se cargan por sesión. Por eso `MEMORY.md` funciona como índice — el detalle va en topic files:

```markdown
# MEMORY.md (índice)

## Patrones clave
- [Ver patterns.md](patterns.md) — Repository pattern, BaseService, zod schemas
- [Ver debugging.md](debugging.md) — Memory leak en worker pool, N+1 en /api/users

## Decisiones recientes
- 2026-04-07: Migrado de JWT a session cookies (Better Auth)
- 2026-04-06: PostgreSQL connection pooling con PgBouncer a 20 conexiones
```

Claude lee el índice y puede leer topic files cuando necesita detalle específico.

### `autoMemoryDirectory` — cambiar ubicación

```json
{
  "autoMemoryDirectory": ".claude/memory"
}
```

Para versionarlo con el proyecto en lugar de guardarlo por usuario.

### CLAUDE.md efectivo — qué incluir y qué no

**Incluir:**
- Comandos de desarrollo no obvios: `npm run db:reset && npm run db:seed`
- Reglas de estilo que difieren del default: `usar tabs, no spaces`
- Testing instructions: cómo correr tests específicos, fixtures necesarios
- Quirks del entorno: puertos, variables de entorno, dependencias de sistema
- Gotchas: "No usar `prisma db push` en producción, siempre migrations"
- Stack específico: versiones, decisiones de arquitectura clave

**No incluir:**
- Lo que Claude ya sabe (React tiene hooks, TypeScript tiene tipos...)
- Convenciones estándar del lenguaje
- Información que cambia frecuentemente (mejor en auto-memory)
- Documentación de negocio extensa (mejor en topic files importados con @)
- Historial de cambios (eso es git history)

### CLAUDE.md: límite práctico

Objetivo: **menos de 200 líneas**. Cada línea consume context window. Reglas:
1. Si se puede deducir del código, no documentarlo
2. Si es obvio para cualquier dev de ese stack, no documentarlo
3. Si cambió hace más de 3 meses y no es relevante, eliminarlo
4. Ejecutar `/init` para generar base automática desde el codebase existente

### `claudeMdExcludes` — monorepos

```json
{
  "claudeMdExcludes": ["packages/legacy/**", "apps/deprecated/**"]
}
```

Excluye directorios del discovery de CLAUDE.md. En monorepos con muchos paquetes, evita cargar reglas de paquetes no relevantes para la tarea actual.

### `CLAUDE_CODE_NEW_INIT=1` — init interactivo

```bash
CLAUDE_CODE_NEW_INIT=1 claude
```

Activa `/init` en modo multi-fase interactivo. Claude te entrevista sobre el proyecto antes de generar el CLAUDE.md — produce un resultado más preciso que el auto-generado.

### InstructionsLoaded hook — debug

Para ver qué archivos CLAUDE.md se cargaron y en qué orden:

```json
{
  "hooks": [{
    "event": "InstructionsLoaded",
    "hook": {
      "type": "command",
      "command": "echo \"Cargado: $CLAUDE_INSTRUCTIONS_FILE\" >> /tmp/instructions-debug.log"
    }
  }]
}
```

### `/memory` command

Muestra todos los archivos CLAUDE.md y MEMORY.md cargados en la sesión actual, con sus scopes y tamaños. Útil para debuggear por qué Claude "olvidó" algo.

### AGENTS.md — compatibilidad multi-agente

```markdown
# AGENTS.md

@CLAUDE.md

## Additional rules for non-Claude agents
- Always use English for code comments
- Follow OpenAPI 3.0 for API specs
```

Si el proyecto usa múltiples agentes (Claude Code, Codex, Gemini CLI), mantener un `AGENTS.md` importando `CLAUDE.md` y agregando instrucciones neutrales. Los agentes que entienden `AGENTS.md` lo leen; Claude Code lee `CLAUDE.md`.

## Conexiones

- Relacionado con: [[claude-code-settings]], [[claude-code-context-window]], [[claude-code-skills]]
- Parte de: [[claude-code-workflow-patterns]], [[claude-code-best-practices]]
- Habilita patrones de: [[context-engineering-patterns]], [[ai-development-workflows]]
- Ver también: [[claude-code-hooks]] (InstructionsLoaded hook), [[claude-code-subagentes]] (auto-memory por subagente)

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
