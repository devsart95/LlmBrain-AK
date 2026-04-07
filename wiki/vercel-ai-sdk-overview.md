---
title: Vercel AI SDK — Overview
type: concept
tags: [vercel, ai-sdk, typescript, streaming, react]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Vercel AI SDK — Overview

> SDK TypeScript/JavaScript de Vercel para integrar LLMs en aplicaciones web. Capa de abstracción sobre múltiples proveedores de AI.

## Contexto

El Vercel AI SDK resuelve la integración de LLMs en aplicaciones Next.js y React con soporte nativo para streaming, tool calling y múltiples proveedores (Anthropic, OpenAI, Google, etc.) con una API unificada.

## Detalle

### Arquitectura del SDK

```
@ai-sdk/core          # lógica principal, agnóstico de provider
@ai-sdk/anthropic     # provider Anthropic
@ai-sdk/openai        # provider OpenAI
@ai-sdk/react         # hooks React (useChat, useCompletion)
ai                    # re-exports + utilities
```

### Instalación

```bash
npm install ai @ai-sdk/anthropic
```

### Funciones principales

#### generateText — respuesta completa

```typescript
import { generateText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

const { text } = await generateText({
  model: anthropic("claude-sonnet-4-5"),
  prompt: "Explica qué es MCP en 3 líneas",
});
```

#### streamText — respuesta en stream

```typescript
import { streamText } from "ai";

const result = streamText({
  model: anthropic("claude-opus-4-5"),
  messages: [
    { role: "user", content: "Analiza este código..." }
  ],
  system: "Eres un expert en TypeScript.",
});

// En API route de Next.js
return result.toDataStreamResponse();

// O iterar manualmente
for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
```

#### generateObject — salida estructurada

```typescript
import { generateObject } from "ai";
import { z } from "zod";

const { object } = await generateObject({
  model: anthropic("claude-sonnet-4-5"),
  schema: z.object({
    bugs: z.array(z.object({
      severity: z.enum(["low", "medium", "high"]),
      description: z.string(),
      line: z.number().optional()
    }))
  }),
  prompt: "Analiza este código y lista los bugs"
});

// object.bugs está completamente tipado
```

### Provider Anthropic

```typescript
import { anthropic } from "@ai-sdk/anthropic";

// Modelos disponibles
const opus = anthropic("claude-opus-4-5");
const sonnet = anthropic("claude-sonnet-4-5");
const haiku = anthropic("claude-haiku-4-5-20251001");

// Con configuración
const modelWithConfig = anthropic("claude-sonnet-4-5", {
  cacheControl: true,  // prompt caching
});
```

### React hooks

```tsx
import { useChat } from "@ai-sdk/react";

function ChatComponent() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat",
  });

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>{m.content}</div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button disabled={isLoading}>Enviar</button>
      </form>
    </div>
  );
}
```

```tsx
// Backend (API route)
import { streamText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: anthropic("claude-sonnet-4-5"),
    messages,
  });

  return result.toDataStreamResponse();
}
```

### Tool calling

```typescript
import { streamText, tool } from "ai";
import { z } from "zod";

const result = streamText({
  model: anthropic("claude-sonnet-4-5"),
  tools: {
    get_weather: tool({
      description: "Obtiene el clima de una ciudad",
      parameters: z.object({
        city: z.string()
      }),
      execute: async ({ city }) => {
        return await fetchWeather(city);
      }
    })
  },
  maxSteps: 5,  // permite múltiples rondas tool call → resultado
  prompt: "¿Cómo está el clima en Asunción?"
});
```

Ver [[vercel-ai-sdk-tools]] para tool calling avanzado.

### Streaming en Next.js 15

```typescript
// app/api/chat/route.ts
import { streamText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: anthropic("claude-sonnet-4-5"),
    messages,
    system: "...",
    onChunk({ chunk }) {
      if (chunk.type === "tool-call") {
        console.log("Tool call:", chunk.toolName);
      }
    }
  });

  return result.toDataStreamResponse();
}
```

Ver [[vercel-ai-sdk-streaming]] para patrones de streaming avanzados.

### vs fetch directo a la API

| | Vercel AI SDK | Fetch directo |
|--|--------------|---------------|
| Boilerplate | Mínimo | Alto |
| Streaming | `toDataStreamResponse()` | Manual |
| Tool calling | Automático con Zod | Manual JSON |
| React hooks | `useChat`, `useCompletion` | Manual |
| Multi-provider | Un API, muchos providers | Cada provider diferente |
| Type safety | Total con Zod | Manual |

## Conexiones
- Relacionado con: [[vercel-ai-sdk-tools]], [[vercel-ai-sdk-streaming]], [[vercel-ai-sdk-agentes]]
- Usado en: wikijrs web app (`web/src/lib/llm.ts`, `ingest.ts`, `query.ts`)
- Alternativa SDK: [[agent-sdk-overview]] (para agents Python/CLI)
- Provider principal: [[claude-sonnet]] y [[claude-opus]]

## Fuentes
- Documentación oficial Vercel AI SDK

---

## Timeline

- 2026-04-07: página creada desde docs oficiales del Vercel AI SDK
