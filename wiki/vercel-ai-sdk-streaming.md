---
title: Vercel AI SDK — Streaming
type: concept
tags: [vercel, ai-sdk, streaming, react, next.js]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Vercel AI SDK — Streaming

> Patterns de streaming del Vercel AI SDK: text streams, data streams, RSC streaming y custom streams.

## Contexto

El streaming es fundamental en apps de AI — permite al usuario ver la respuesta en tiempo real en lugar de esperar que el LLM termine. El AI SDK proporciona primitivos de alto nivel sobre la API de streaming de Vercel/Edge Runtime.

## Detalle

### TextStream básico

```typescript
// API route: app/api/chat/route.ts
import { streamText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: anthropic("claude-sonnet-4-5"),
    messages,
  });

  // toTextStreamResponse() — solo texto, sin metadata
  return result.toTextStreamResponse();
}
```

### DataStream — texto + metadata

```typescript
export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: anthropic("claude-sonnet-4-5"),
    messages,
    tools: { /* ... */ },
  });

  // toDataStreamResponse() — incluye tool calls, finishReason, usage
  return result.toDataStreamResponse();
}
```

El data stream usa un protocolo de Vercel que incluye:
- `0:` texto del mensaje
- `2:` tool calls
- `3:` tool results
- `d:` datos finales (usage, finishReason)

### useChat con data stream

```tsx
import { useChat } from "@ai-sdk/react";

export default function ChatPage() {
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
    error,
    stop,         // cancelar stream
    reload,       // reintentar último mensaje
  } = useChat({
    api: "/api/chat",
    onFinish: (message) => {
      console.log("Mensaje completo:", message.content);
    },
    onError: (error) => {
      console.error("Error:", error);
    }
  });

  return (
    <div>
      <div className="messages">
        {messages.map((m) => (
          <div key={m.id} data-role={m.role}>
            {m.content}
            {/* Tool calls aparecen en m.toolInvocations */}
            {m.toolInvocations?.map((t) => (
              <div key={t.toolCallId}>
                Llamando: {t.toolName}
              </div>
            ))}
          </div>
        ))}
        {isLoading && <div>...</div>}
      </div>

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button type="submit" disabled={isLoading}>Enviar</button>
        {isLoading && <button type="button" onClick={stop}>Cancelar</button>}
      </form>
    </div>
  );
}
```

### Stream manual (sin useChat)

```tsx
// Para casos donde useChat no encaja
const [output, setOutput] = useState("");

async function fetchStream(prompt: string) {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages: [{ role: "user", content: prompt }] }),
  });

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value, { stream: true });
    // Parsear el formato data stream de Vercel
    const lines = chunk.split("\n").filter(Boolean);
    for (const line of lines) {
      if (line.startsWith("0:")) {
        const text = JSON.parse(line.slice(2));
        setOutput((prev) => prev + text);
      }
    }
  }
}
```

### streamObject — objetos en stream

```typescript
import { streamObject } from "ai";
import { z } from "zod";

const result = streamObject({
  model: anthropic("claude-sonnet-4-5"),
  schema: z.object({
    analysis: z.object({
      summary: z.string(),
      keyPoints: z.array(z.string()),
      sentiment: z.enum(["positive", "neutral", "negative"])
    })
  }),
  prompt: "Analiza este texto..."
});

// Stream parcial del objeto mientras se genera
for await (const partialObject of result.partialObjectStream) {
  // partialObject puede tener campos incompletos mientras fluye
  console.log(partialObject);
}

// Objeto final completo
const { object } = await result;
```

### RSC — React Server Components streaming

```tsx
// app/actions.ts
"use server";

import { streamUI } from "ai/rsc";
import { anthropic } from "@ai-sdk/anthropic";

export async function generateComponent(prompt: string) {
  const result = await streamUI({
    model: anthropic("claude-sonnet-4-5"),
    messages: [{ role: "user", content: prompt }],
    text: ({ content, done }) => (
      <div className={done ? "complete" : "streaming"}>
        {content}
      </div>
    ),
  });
  return result.value;
}
```

```tsx
// app/page.tsx
"use client";
import { useState } from "react";
import { generateComponent } from "./actions";

export default function Page() {
  const [ui, setUi] = useState(null);

  return (
    <div>
      <button onClick={async () => {
        const component = await generateComponent("Explica Next.js");
        setUi(component);
      }}>
        Generar
      </button>
      {ui}
    </div>
  );
}
```

### onChunk — observar el stream

```typescript
const result = streamText({
  model: anthropic("claude-sonnet-4-5"),
  prompt: "...",
  onChunk: ({ chunk }) => {
    switch (chunk.type) {
      case "text-delta":
        // Cada fragmento de texto
        process.stdout.write(chunk.textDelta);
        break;
      case "tool-call":
        console.log("Tool call:", chunk.toolName);
        break;
      case "tool-result":
        console.log("Tool result:", chunk.result);
        break;
      case "finish":
        console.log("Finish reason:", chunk.finishReason);
        console.log("Usage:", chunk.usage);
        break;
    }
  }
});
```

### Cancellation

```typescript
// En el cliente con useChat
const { stop } = useChat({ /* ... */ });
<button onClick={stop}>Cancelar</button>

// En el servidor con AbortSignal
export async function POST(req: Request) {
  const result = streamText({
    model: anthropic("claude-sonnet-4-5"),
    messages: [...],
    abortSignal: req.signal,  // se cancela si el cliente cierra la conexión
  });
  return result.toDataStreamResponse();
}
```

## Conexiones
- Relacionado con: [[vercel-ai-sdk-overview]], [[vercel-ai-sdk-tools]]
- Usado en wikijrs: `web/src/app/api/query/route.ts`
- Para entender el frontend: React hooks de streaming con `useChat`

## Fuentes
- Documentación oficial Vercel AI SDK — sección Streaming

---

## Timeline

- 2026-04-07: página creada desde docs oficiales del Vercel AI SDK
