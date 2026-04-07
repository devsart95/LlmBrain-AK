---
title: Vercel AI SDK — Tool Calling
type: concept
tags: [vercel, ai-sdk, tools, function-calling, zod]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Vercel AI SDK — Tool Calling

> Sistema de tool calling del Vercel AI SDK: definición con Zod, ejecución automática, multi-step loops y approval flows.

## Contexto

Tool calling (function calling) permite al LLM invocar funciones definidas por el desarrollador. El AI SDK maneja el loop completo: LLM decide llamar → ejecuta la función → resultado vuelve al LLM → LLM responde.

## Detalle

### Definir un tool

```typescript
import { tool } from "ai";
import { z } from "zod";

const weatherTool = tool({
  description: "Obtiene el clima actual de una ciudad",
  parameters: z.object({
    city: z.string().describe("Nombre de la ciudad"),
    units: z.enum(["celsius", "fahrenheit"]).default("celsius").optional()
  }),
  execute: async ({ city, units = "celsius" }) => {
    const data = await fetchWeatherAPI(city);
    return {
      temperature: data.temp,
      condition: data.condition,
      units
    };
  }
});
```

### Usar tools en generateText / streamText

```typescript
import { generateText, tool } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

const { text, toolCalls, toolResults } = await generateText({
  model: anthropic("claude-sonnet-4-5"),
  tools: {
    get_weather: weatherTool,
    search_web: searchTool,
  },
  maxSteps: 10,  // loops automáticos hasta respuesta final
  prompt: "¿Necesito paraguas en Asunción hoy?"
});
```

Con `maxSteps > 1`, el SDK maneja el loop automáticamente:
1. LLM decide llamar `get_weather`
2. SDK ejecuta `execute()`
3. Resultado vuelve al LLM
4. LLM responde con el texto final

### stopWhen — terminar el loop

```typescript
import { generateText, stopWhen } from "ai";

const result = await generateText({
  model: anthropic("claude-opus-4-5"),
  tools: { /* ... */ },
  maxSteps: 20,
  stopWhen: stopWhen.toolCallCount(5),  // máximo 5 tool calls
  // o
  stopWhen: (state) => state.toolCallCount > 5 || state.hasError,
});
```

### Human-in-the-loop: needsApproval

```typescript
const dangerousTool = tool({
  description: "Elimina archivos del sistema",
  parameters: z.object({ path: z.string() }),
  needsApproval: async ({ path }) => {
    // Lógica para decidir si necesita aprobación
    return path.includes("important") || path.startsWith("/");
  },
  execute: async ({ path }) => {
    await fs.rm(path);
    return { deleted: path };
  }
});
```

Cuando `needsApproval` retorna `true`, el SDK pausa y espera confirmación del usuario antes de ejecutar.

### Tool-only mode

```typescript
// Forzar que el LLM SIEMPRE use tools
const result = await generateText({
  model: anthropic("claude-sonnet-4-5"),
  tools: { analyze_code: analysisTool },
  toolChoice: "required",  // el LLM debe llamar al menos un tool
  prompt: "Analiza este código"
});

// Forzar tool específico
const result2 = await generateText({
  model: anthropic("claude-sonnet-4-5"),
  tools: { analyze_code: analysisTool },
  toolChoice: { type: "tool", toolName: "analyze_code" },
  prompt: "Analiza este código"
});
```

### Tools con estado (closures)

```typescript
function createDbTools(db: Database) {
  return {
    query_users: tool({
      description: "Consulta usuarios",
      parameters: z.object({ filter: z.string().optional() }),
      execute: async ({ filter }) => {
        // `db` viene del closure
        return await db.users.findMany({ where: filter ? { name: { contains: filter } } : {} });
      }
    }),
    create_user: tool({
      description: "Crea un usuario",
      parameters: z.object({ name: z.string(), email: z.string().email() }),
      execute: async ({ name, email }) => {
        return await db.users.create({ data: { name, email } });
      }
    })
  };
}

// Usar en la llamada
const tools = createDbTools(prisma);
const result = await generateText({ model, tools, prompt });
```

### Tipos de retorno de execute

```typescript
execute: async (args) => {
  // String simple
  return "resultado en texto";

  // Objeto (se serializa como JSON)
  return { success: true, data: [...] };

  // Mensaje de error (el LLM sabrá que falló)
  return { error: "Recurso no encontrado", code: "NOT_FOUND" };
}
```

### Multi-tool: varios tools en paralelo

El LLM puede llamar múltiples tools simultáneamente en una ronda:

```typescript
const result = await generateText({
  model: anthropic("claude-sonnet-4-5"),
  tools: {
    get_weather: weatherTool,
    get_news: newsTool,
    get_stocks: stocksTool,
  },
  prompt: "Dame el clima, noticias y mercados de hoy"
});

// El LLM puede llamar los 3 tools en paralelo
// El SDK ejecuta execute() para cada uno y retorna todos al LLM
```

### onToolCall callback

```typescript
const result = streamText({
  model: anthropic("claude-opus-4-5"),
  tools: { /* ... */ },
  onChunk: ({ chunk }) => {
    if (chunk.type === "tool-call") {
      console.log(`Llamando ${chunk.toolName} con:`, chunk.args);
    }
    if (chunk.type === "tool-result") {
      console.log(`Resultado de ${chunk.toolName}:`, chunk.result);
    }
  }
});
```

## Conexiones
- Relacionado con: [[vercel-ai-sdk-overview]], [[vercel-ai-sdk-agentes]]
- Equivalente MCP: [[mcp-build-server]] (tools en el protocolo MCP)
- Diferencia: tools del AI SDK son server-side en tu app; MCP tools son en proceso externo
- Usado en wikijrs: `web/src/lib/ingest.ts`, `web/src/lib/query.ts`

## Fuentes
- Documentación oficial Vercel AI SDK — sección Tool Calling

---

## Timeline

- 2026-04-07: página creada desde docs oficiales del Vercel AI SDK
