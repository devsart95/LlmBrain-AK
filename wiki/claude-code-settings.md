---
title: Claude Code — Settings y Configuración
type: concept
tags: [claude-code, settings, configuracion, permisos]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Settings y Configuración

> Sistema de configuración con 4 scopes jerárquicos que controlan permisos, hooks, modelos, MCP servers y comportamiento general de Claude Code.

---

## Contexto

Settings en Claude Code no es un solo archivo — es una jerarquía de 4 niveles donde cada nivel puede ser gestionado por distintos actores (IT, usuario, proyecto, developer local). Los arrays hacen merge entre niveles; los valores escalares tienen prioridad por nivel (el más específico gana).

## Detalle

### Scopes jerárquicos

```
managed (IT/Ansible/MDM)              # política corporativa — no editable por usuario
~/.claude/settings.json               # usuario — aplica a todos los proyectos
.claude/settings.json                 # proyecto — versionado con git
.claude/settings.local.json           # local — no versionado, overrides personales
```

**Merge behavior:**
- Arrays (`hooks`, `permissions.allow`, `permissions.deny`, `env`): se acumulan entre scopes
- Escalares (`model`, `autoMemoryEnabled`): el scope más específico gana
- Managed tiene prioridad absoluta sobre todo

### Estructura completa de `settings.json`

```json
{
  "model": "claude-opus-4",
  "autoMemoryEnabled": true,
  "autoMemoryDirectory": ".claude/memory",
  "disableAllHooks": false,
  "claudeMdExcludes": ["packages/legacy/**"],

  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm *)",
      "Edit(*.ts)",
      "Edit(*.tsx)",
      "Skill(review)",
      "mcp__github__*"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Edit(.env*)",
      "Skill(deploy-prod)"
    ]
  },

  "hooks": [
    {
      "event": "PostToolUse",
      "if": "Edit|Write",
      "hook": {
        "type": "command",
        "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\" 2>/dev/null || true"
      }
    }
  ],

  "env": {
    "NODE_ENV": "development",
    "DATABASE_URL": "$DATABASE_URL"
  },

  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "$GITHUB_TOKEN" }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "$DATABASE_URL"]
    }
  },

  "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
}
```

### `~/.claude.json` — global config

Archivo separado para configuración global que no es por proyecto:

```json
{
  "teammateMode": "auto",
  "theme": "dark",
  "defaultModel": "claude-sonnet-4-5"
}
```

Valores de `teammateMode`: `"auto"`, `"in-process"`, `"tmux"`.

### Permission rules — sintaxis completa

```
Bash(<command-pattern>)   — comandos shell
Edit(<file-pattern>)      — edición de archivos
Write(<file-pattern>)     — escritura de archivos
Read(<file-pattern>)      — lectura de archivos
Skill(<skill-name>)       — invocación de skills
mcp__<server>__<tool>     — tools de MCP servers
mcp__<server>__*          — todos los tools de un server
WebFetch                  — requests HTTP
Task                      — crear subagentes/tareas
```

**Glob en patterns:**
```json
"allow": [
  "Bash(git *)",              // git seguido de cualquier cosa
  "Edit(src/**/*.ts)",        // .ts en src/ y subdirectorios
  "Edit(*.{ts,tsx,js,jsx})"  // múltiples extensiones
]
```

**Allow vs Deny:**
- `allow` — skip del diálogo de permiso (Claude ejecuta sin pedir)
- `deny` — bloquear siempre, sin excepción (ni aunque el usuario lo pida)
- Un deny siempre gana sobre un allow

### `/config` — UI interactivo

En el REPL:
```
/config
```

Abre una UI de texto para ver y modificar settings sin editar JSON manualmente. Muestra el scope de cada setting y permite cambiar valores.

### `/permissions` — gestión interactiva de permisos

```
/permissions
```

Lista todas las reglas de allow/deny activas, su scope, y permite agregar/remover reglas interactivamente.

### `disableAllHooks: true`

Útil para debugging cuando un hook está causando comportamiento inesperado:

```json
{
  "disableAllHooks": true
}
```

Deshabilita todos los hooks de todos los scopes. Flag de emergencia.

### Managed settings — organizaciones

Para equipos corporativos, se puede deployar un `server-managed-settings.json` via MDM/Ansible:

```json
{
  "permissions": {
    "deny": [
      "WebFetch(*://internal.company.com/*)",
      "Bash(curl * internal.*)"
    ]
  },
  "claudeMdExcludes": ["**/secrets/**"],
  "disableAllHooks": false
}
```

El archivo se coloca en una ubicación específica del sistema que Claude Code lee con prioridad sobre todos los demás scopes.

### `env` — variables de entorno

```json
{
  "env": {
    "NODE_ENV": "development",
    "API_URL": "http://localhost:3000",
    "REDIS_URL": "$REDIS_URL"
  }
}
```

Las variables definidas aquí están disponibles en todos los tools (Bash, hooks, skills). `$VARIABLE` expande desde el entorno del shell donde se lanzó Claude Code.

### Settings relevantes por caso de uso

**Proyecto con deploy frecuente:**
```json
{
  "permissions": {
    "allow": ["Bash(docker *)", "Bash(git push *)", "Bash(npm run build)"]
  }
}
```

**Proyecto con DB sensible:**
```json
{
  "permissions": {
    "deny": ["Bash(psql * --command *DROP*)", "Bash(psql * --command *TRUNCATE*)"]
  }
}
```

**CI/CD non-interactive:**
```json
{
  "permissions": {
    "allow": ["Bash(*)", "Edit(*)", "Write(*)"]
  }
}
```

**Monorepo con múltiples apps:**
```json
{
  "claudeMdExcludes": [
    "apps/legacy-php/**",
    "packages/deprecated/**"
  ]
}
```

### Relación entre scopes — ejemplo real

```
~/.claude/settings.json (usuario):
  permissions.allow: ["Bash(git *)", "Bash(npm *)"]
  hooks: [notificación desktop en Stop]

.claude/settings.json (proyecto):
  permissions.allow: ["Bash(docker compose *)", "Edit(*.ts)"]
  permissions.deny: ["Edit(.env*)"]
  hooks: [Prettier en PostToolUse]

.claude/settings.local.json (local):
  env: { DATABASE_URL: "postgres://localhost/myapp_dev" }

Resultado efectivo:
  allow: ["Bash(git *)", "Bash(npm *)", "Bash(docker compose *)", "Edit(*.ts)"]
  deny: ["Edit(.env*)"]
  hooks: [notificación desktop, Prettier]
  env: { DATABASE_URL: "postgres://localhost/myapp_dev" }
```

## Conexiones

- Relacionado con: [[claude-code-permisos]], [[claude-code-hooks]], [[claude-code-memory]]
- Parte de: [[claude-code-workflow-patterns]], [[claude-code-mcp]]
- Habilita: [[claude-code-agent-teams]] (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS), [[claude-code-subagentes]] (scopes de agentes)
- Ver también: [[claude-code-cli-referencia]] (flags que sobreescriben settings)

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
