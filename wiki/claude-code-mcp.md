---
title: Claude Code — MCP (Model Context Protocol)
type: concept
tags: [claude-code, mcp, tools, integraciones, protocolo]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — MCP (Model Context Protocol)

> Protocolo abierto que permite conectar Claude con herramientas y servicios externos, exponiendo tools que Claude puede invocar como si fueran capacidades nativas.

---

## Contexto

Claude Code incluye tools built-in (Read, Write, Bash, Grep...), pero el mundo real tiene APIs, bases de datos, servicios externos. MCP es el protocolo que permite extender Claude con cualquier herramienta: GitHub, PostgreSQL, Slack, Figma, o tools propios del proyecto. Una vez conectado, Claude puede invocar esas tools directamente sin copy-paste de output.

## Detalle

### Agregar un servidor MCP desde CLI

```bash
# Servidor local (stdio)
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Servidor remoto (HTTP/SSE)
claude mcp add my-api --url https://api.example.com/mcp

# Con variables de entorno
claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres $DATABASE_URL

# En scope de proyecto (compartido con el equipo)
claude mcp add --scope project github -- npx -y @modelcontextprotocol/server-github
```

### Tipos de servidores

**Local (stdio)**:
- Proceso que corre localmente, Claude se comunica via stdin/stdout
- Ideal para: herramientas de filesystem, CLIs, scripts propios
- Latencia: baja (mismo proceso o loopback)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    }
  }
}
```

**Remoto (HTTP/SSE)**:
- Servidor HTTP externo que implementa el protocolo MCP
- Ideal para: SaaS APIs, servicios compartidos, microservicios
- Soporta OAuth para autenticación

```json
{
  "mcpServers": {
    "my-internal-api": {
      "url": "https://mcp.company.com/api",
      "headers": {
        "Authorization": "Bearer $MCP_API_TOKEN"
      }
    }
  }
}
```

### Configuración en settings.json

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "$GITHUB_TOKEN",
        "GITHUB_TOOLSETS": "repos,issues,pull_requests"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "$DATABASE_URL"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "$BRAVE_API_KEY"
      }
    },
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-mcp-server"],
      "env": {
        "FIGMA_TOKEN": "$FIGMA_TOKEN"
      }
    }
  }
}
```

### Registry oficial

```
https://api.anthropic.com/mcp-registry/v0/servers
```

Lista de servidores MCP verificados por Anthropic. Búsqueda y discovery de servidores disponibles.

### Servidores oficiales de alto valor

| Server | Caso de uso |
|--------|-------------|
| `@modelcontextprotocol/server-github` | PRs, issues, code review, commits |
| `@modelcontextprotocol/server-postgres` | Queries SQL directas a la DB |
| `@modelcontextprotocol/server-filesystem` | Acceso a directorios fuera del cwd |
| `@modelcontextprotocol/server-brave-search` | Web search en tiempo real |
| `@modelcontextprotocol/server-slack` | Leer canales, enviar mensajes |
| `@modelcontextprotocol/server-google-drive` | Leer documentos de Drive |
| `figma-mcp-server` | Leer diseños de Figma, exportar specs |

### Naming convention para tools MCP

Claude Code prefija los tools de MCP con `mcp__<server>__<tool>`:

```
mcp__github__list_pull_requests
mcp__github__create_issue
mcp__postgres__query
mcp__brave-search__web_search
```

Importante para:
- Permission rules: `"allow": ["mcp__github__*"]`
- Hook matchers: `"if": "mcp__github__.*"`
- Logs y auditoría

### Permission rules para MCP

```json
{
  "permissions": {
    "allow": [
      "mcp__github__list_*",
      "mcp__github__get_*",
      "mcp__postgres__query"
    ],
    "deny": [
      "mcp__github__delete_*",
      "mcp__postgres__execute"
    ]
  }
}
```

Patrón recomendado: allow explícito para reads, deny explícito para destructivos.

### Hooks para tools MCP

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "if": "mcp__github__create_.*",
      "hook": {
        "type": "command",
        "command": "echo \"[$(date)] GitHub create operation: $CLAUDE_TOOL_NAME\" >> .claude/github-audit.log"
      }
    },
    {
      "event": "PreToolUse",
      "if": "mcp__postgres__.*",
      "hook": {
        "type": "command",
        "command": "echo \"[$(date)] DB query: $CLAUDE_TOOL_INPUT_QUERY\" >> .claude/db-audit.log"
      }
    }
  ]
}
```

### Gestión desde CLI

```bash
# Listar servidores configurados
claude mcp list

# Ver detalles de un servidor
claude mcp get github

# Remover un servidor
claude mcp remove github

# Ver tools disponibles de un servidor
claude mcp tools github
```

### OAuth para servidores remotos

Servidores MCP remotos pueden requerir OAuth. Claude Code maneja el flujo completo:

1. Claude intenta usar el tool
2. Server responde que requiere auth
3. Claude Code abre el browser para el flow OAuth
4. Token se almacena localmente para sesiones futuras

```json
{
  "mcpServers": {
    "linear": {
      "url": "https://mcp.linear.app",
      "oauth": {
        "clientId": "$LINEAR_CLIENT_ID",
        "scopes": ["issues:read", "issues:write"]
      }
    }
  }
}
```

### Scopes de config MCP

Los `mcpServers` en settings.json respetan el mismo sistema de scopes:
- `~/.claude/settings.json` — servidores disponibles globalmente (GitHub, Slack personal)
- `.claude/settings.json` — servidores del proyecto (PostgreSQL del proyecto, API interna)
- `.claude/settings.local.json` — overrides locales (credenciales dev, endpoints locales)

### Elicitation — MCP pide input al usuario

Un servidor MCP puede pausar su ejecución y pedir datos al usuario a través de Claude Code:

```
Ejemplo: mcp__payments__charge_card necesita confirmación con el monto exacto
→ Servidor envía Elicitation request
→ Claude Code muestra diálogo al usuario
→ Usuario confirma/cancela
→ Servidor recibe respuesta y continúa o aborta
```

Hook para interceptar:
```json
{
  "event": "Elicitation",
  "hook": {
    "type": "command",
    "command": "echo \"Elicitation de $CLAUDE_MCP_SERVER: $CLAUDE_ELICITATION_PROMPT\""
  }
}
```

### Scopes de disponibilidad en subagentes

Los subagentes solo tienen acceso a los MCP servers explícitamente listados en su frontmatter:

```yaml
---
name: github-reviewer
tools: [Read, Grep]
mcpServers: [github]   # solo este servidor MCP
---
```

Sin el campo `mcpServers`, el subagente no tiene acceso a ningún servidor MCP aunque estén configurados globalmente.

### chrome-devtools-mcp (instalado globalmente en DevSar)

```bash
# Chrome debe correr con remote debugging
chrome --remote-debugging-port=9222

# Tools disponibles
mcp__chrome-devtools__take_screenshot
mcp__chrome-devtools__evaluate_script
mcp__chrome-devtools__lighthouse_audit
mcp__chrome-devtools__navigate
mcp__chrome-devtools__list_console_messages
```

Disponible en todas las sesiones. Permite a Claude ver la UI, auditar performance, y debuggear frontend sin salir del flujo de trabajo.

## Conexiones

- Relacionado con: [[claude-code-settings]], [[claude-code-permisos]], [[claude-code-hooks]]
- Parte de: [[claude-code-workflow-patterns]], [[claude-code-subagentes]]
- Habilita: integración de tools externos, web search, acceso a DB desde Claude
- Ver también: [[agent-skills-ecosystem]] (skills de MCP en el ecosistema), [[claude-code-cli-referencia]] (comandos `claude mcp`)

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
