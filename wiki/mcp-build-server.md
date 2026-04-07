---
title: MCP — Construir un Server
type: concept
tags: [mcp, server, typescript, python, desarrollo]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# MCP — Construir un Server

> Tutorial práctico para construir un MCP server desde cero, en TypeScript o Python.

## Contexto

Construir un MCP server permite exponer cualquier API, base de datos, o herramienta al ecosistema de LLMs compatibles con MCP (Claude Code, Claude Desktop, Cursor, etc).

## Detalle

### TypeScript — setup básico

```bash
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node tsx
```

```typescript
// src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "mi-server",
  version: "1.0.0",
});

// Registrar un tool
server.tool(
  "get_weather",
  "Obtiene el clima actual de una ciudad",
  {
    city: z.string().describe("Nombre de la ciudad"),
    units: z.enum(["celsius", "fahrenheit"]).default("celsius")
  },
  async ({ city, units }) => {
    const data = await fetchWeather(city, units);
    return {
      content: [{
        type: "text",
        text: JSON.stringify(data, null, 2)
      }]
    };
  }
);

// Iniciar con stdio transport
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python — equivalente

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json

server = Server("mi-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="Obtiene el clima actual",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["city"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather":
        city = arguments["city"]
        data = await fetch_weather(city)
        return [TextContent(type="text", text=json.dumps(data))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())
```

### Registrar Resources

```typescript
// Resource estático
server.resource(
  "config",
  "config://app",
  async (uri) => ({
    contents: [{
      uri: uri.href,
      mimeType: "application/json",
      text: JSON.stringify(appConfig)
    }]
  })
);

// Resource dinámico con template
server.resource(
  "user-profile",
  new ResourceTemplate("users://{userId}/profile", { list: undefined }),
  async (uri, { userId }) => {
    const user = await db.users.findById(userId);
    return {
      contents: [{
        uri: uri.href,
        mimeType: "application/json",
        text: JSON.stringify(user)
      }]
    };
  }
);
```

### Registrar Prompts

```typescript
server.prompt(
  "code_review",
  "Template para code review estructurado",
  {
    language: z.string(),
    code: z.string(),
    focus: z.enum(["security", "performance", "readability"]).optional()
  },
  ({ language, code, focus }) => ({
    messages: [{
      role: "user",
      content: {
        type: "text",
        text: `Haz un code review de este código ${language}${focus ? ` con foco en ${focus}` : ''}:\n\n${code}`
      }
    }]
  })
);
```

### HTTP transport (deploy remoto)

```typescript
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";

const app = express();
app.use(express.json());

// Manejar todas las peticiones MCP
app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

app.listen(3000);
```

### Testing del server

```bash
# Instalar inspector oficial
npx @modelcontextprotocol/inspector

# Con stdio server
npx @modelcontextprotocol/inspector npx tsx src/index.ts

# Con HTTP server (en otra terminal)
npx @modelcontextprotocol/inspector --url http://localhost:3000/mcp
```

El inspector es una UI web para probar tools, resources y prompts interactivamente.

### Configurar en Claude Code

```json
// .mcp.json en el proyecto
{
  "mcpServers": {
    "mi-server": {
      "command": "npx",
      "args": ["tsx", "src/index.ts"]
    }
  }
}

// o con HTTP
{
  "mcpServers": {
    "mi-server-remoto": {
      "url": "https://mi-api.com/mcp",
      "headers": {
        "Authorization": "Bearer ${MI_API_TOKEN}"
      }
    }
  }
}
```

### Patrones de respuesta de tools

```typescript
// Éxito simple
return {
  content: [{ type: "text", text: "resultado" }]
};

// Con datos estructurados
return {
  content: [{ type: "text", text: JSON.stringify(data) }]
};

// Con imagen
return {
  content: [{
    type: "image",
    data: base64ImageData,
    mimeType: "image/png"
  }]
};

// Error (el LLM entiende que falló)
return {
  content: [{ type: "text", text: "Error: recurso no encontrado" }],
  isError: true
};
```

## Conexiones
- Relacionado con: [[mcp-arquitectura]], [[claude-code-mcp]], [[mcp-seguridad]]
- Wikijrs usa esto: `.mcp.json` con `wikisearch` server
- Alternativa para tools web: [[vercel-ai-sdk-tools]]

## Fuentes
- Documentación oficial MCP — Build a Server tutorial

---

## Timeline

- 2026-04-07: página creada desde docs oficiales de MCP
