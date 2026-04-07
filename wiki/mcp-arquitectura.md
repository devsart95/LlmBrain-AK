---
title: MCP — Arquitectura
type: concept
tags: [mcp, protocolo, arquitectura, ai, tools]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# MCP — Arquitectura

> Model Context Protocol: protocolo abierto de Anthropic para conectar LLMs con herramientas y datos externos de forma estandarizada.

## Contexto

MCP resuelve el problema de integración M×N: sin él, cada LLM necesita integrarse con cada herramienta por separado. Con MCP, cualquier LLM compatible se conecta con cualquier MCP server sin código adicional.

## Detalle

### Componentes del sistema

```
┌─────────────────────────────────────┐
│            MCP Host                 │
│  (Claude Code, Claude Desktop,      │
│   tu propia app)                    │
│                                     │
│  ┌─────────────┐                    │
│  │  MCP Client │◄──────────────────┐│
│  └──────┬──────┘                   ││
└─────────┼───────────────────────────┘
          │ JSON-RPC 2.0
          ▼
┌─────────────────┐   ┌──────────────────┐
│   MCP Server A  │   │   MCP Server B   │
│  (filesystem)   │   │  (github API)    │
│                 │   │                  │
│  Tools          │   │  Tools           │
│  Resources      │   │  Resources       │
│  Prompts        │   │  Prompts         │
└─────────────────┘   └──────────────────┘
```

- **Host**: la aplicación LLM (Claude Code, Claude Desktop, tu app)
- **Client**: componente dentro del host que gestiona conexiones MCP
- **Server**: proceso externo que expone tools/resources/prompts

### Los tres primitivos

#### Tools (el más importante)
Funciones que el LLM puede invocar. Equivalente a function calling:

```json
{
  "name": "read_file",
  "description": "Lee el contenido de un archivo",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {"type": "string", "description": "Ruta del archivo"}
    },
    "required": ["path"]
  }
}
```

#### Resources
Datos que el LLM puede leer (archivos, bases de datos, APIs). Similares a GET endpoints:

```
resource://filesystem/path/to/file.txt
resource://database/users/123
resource://api/weather/current
```

#### Prompts
Templates de prompts reutilizables que el server puede exponer:

```json
{
  "name": "code_review",
  "description": "Template para code review",
  "arguments": [
    {"name": "language", "required": true},
    {"name": "code", "required": true}
  ]
}
```

### Transportes

#### stdio (local)
El más común para tools locales:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"],
      "env": {}
    }
  }
}
```

Host lanza el proceso hijo, comunica por stdin/stdout. Simple, seguro, sin red.

#### Streamable HTTP (remoto)
Para servers accesibles por red:

```json
{
  "mcpServers": {
    "mi-api": {
      "url": "https://api.ejemplo.com/mcp",
      "headers": {
        "Authorization": "Bearer TOKEN"
      }
    }
  }
}
```

Reemplazó SSE+HTTP como transporte estándar para deploys remotos.

### Protocolo JSON-RPC 2.0

```
Cliente → Servidor: initialize (negociación de capacidades)
Servidor → Cliente: initialized
Cliente → Servidor: tools/list
Servidor → Cliente: [lista de tools]
...
Cliente → Servidor: tools/call {name, arguments}
Servidor → Cliente: resultado
```

### Lifecycle y capabilities

```json
// initialize request
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": {"listChanged": true},
      "sampling": {}
    }
  }
}

// initialized response
{
  "capabilities": {
    "tools": {"listChanged": true},
    "resources": {"subscribe": true, "listChanged": true},
    "prompts": {"listChanged": true},
    "logging": {}
  },
  "serverInfo": {"name": "mi-server", "version": "1.0.0"}
}
```

La negociación de capabilities permite que client y server sepan qué features mutuamente soportan.

### Notifications (push)

El server puede notificar al client sin que este pregunte:

```json
// Server notifica que cambió la lista de tools
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/listChanged"
}
```

Útil para servers que exponen herramientas dinámicas.

## Conexiones
- Relacionado con: [[claude-code-mcp]], [[mcp-build-server]], [[mcp-seguridad]]
- Usado por: [[agent-sdk-overview]], [[claude-code-mcp]]
- Tools se mapean a: [[claude-code-hooks]] (el host intercepta tool calls)

## Fuentes
- Documentación oficial MCP — sección Architecture

---

## Timeline

- 2026-04-07: página creada desde docs oficiales de MCP
