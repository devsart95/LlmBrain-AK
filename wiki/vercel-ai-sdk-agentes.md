---
title: Vercel AI SDK — Agentes
type: concept
tags: [vercel, ai-sdk, agentes, tool-loop, typescript]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Vercel AI SDK — Agentes

> Construir agentes autónomos con el Vercel AI SDK: tool loops, patrones de orquestación y control de flujo.

## Contexto

Un agente en el contexto del AI SDK es un LLM con tools que puede ejecutar múltiples pasos de forma autónoma hasta completar una tarea. El SDK maneja el loop automáticamente con `maxSteps`.

## Detalle

### El patrón fundamental: ToolLoopAgent

```typescript
import { generateText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import { tool } from "ai";
import { z } from "zod";

// Definir los tools del agente
const agentTools = {
  read_file: tool({
    description: "Lee el contenido de un archivo",
    parameters: z.object({ path: z.string() }),
    execute: async ({ path }) => await fs.readFile(path, "utf-8")
  }),

  write_file: tool({
    description: "Escribe contenido a un archivo",
    parameters: z.object({ path: z.string(), content: z.string() }),
    execute: async ({ path, content }) => {
      await fs.writeFile(path, content);
      return `Archivo ${path} escrito correctamente`;
    }
  }),

  run_tests: tool({
    description: "Ejecuta los tests del proyecto",
    parameters: z.object({ pattern: z.string().optional() }),
    execute: async ({ pattern }) => {
      const { stdout, stderr } = await exec(`npm test ${pattern || ""}`);
      return { stdout, stderr };
    }
  }),
};

// El agente ejecuta hasta completar la tarea
const { text, steps } = await generateText({
  model: anthropic("claude-opus-4-5"),
  system: `Eres un agente de software. Tienes acceso a herramientas para leer/escribir archivos
           y ejecutar tests. Completa la tarea paso a paso.`,
  prompt: "Refactoriza la función getUserById para usar async/await y asegúrate que los tests pasen",
  tools: agentTools,
  maxSteps: 20,  // el agente puede hacer hasta 20 iteraciones
});

console.log(`Completado en ${steps.length} pasos`);
```

### Observar los pasos del agente

```typescript
const result = await generateText({
  model: anthropic("claude-opus-4-5"),
  tools: agentTools,
  maxSteps: 20,
  prompt: "...",
  onStepFinish: ({ stepType, toolCalls, toolResults, text, finishReason }) => {
    if (stepType === "tool-result") {
      console.log(`Tool: ${toolCalls[0]?.toolName}`);
      console.log(`Resultado: ${JSON.stringify(toolResults[0]?.result).slice(0, 100)}`);
    }
  }
});

// Acceder a todos los pasos después
for (const step of result.steps) {
  console.log(`Paso ${step.stepType}:`, step.text || step.toolCalls);
}
```

### Agente con memoria (estado persistente)

```typescript
class PersistentAgent {
  private conversationHistory: Message[] = [];

  async run(task: string): Promise<string> {
    this.conversationHistory.push({
      role: "user",
      content: task
    });

    const result = await generateText({
      model: anthropic("claude-opus-4-5"),
      messages: this.conversationHistory,
      tools: agentTools,
      maxSteps: 15,
      system: "Recuerdas el contexto de tareas anteriores."
    });

    // Guardar en el historial
    this.conversationHistory.push({
      role: "assistant",
      content: result.text
    });

    return result.text;
  }
}

const agent = new PersistentAgent();
await agent.run("Analiza el módulo auth");
await agent.run("Ahora mejora el rendimiento del módulo que analizaste");
// El segundo task recuerda el análisis anterior
```

### Multi-agente: orquestador + especialistas

```typescript
async function orchestrateTask(task: string) {
  // Agente orquestador decide cómo dividir el trabajo
  const { object: plan } = await generateObject({
    model: anthropic("claude-opus-4-5"),
    schema: z.object({
      subtasks: z.array(z.object({
        id: z.string(),
        description: z.string(),
        specialist: z.enum(["security", "performance", "refactor"])
      }))
    }),
    prompt: `Divide esta tarea en subtasks: ${task}`
  });

  // Ejecutar subtasks en paralelo con agentes especializados
  const results = await Promise.all(
    plan.subtasks.map(subtask =>
      generateText({
        model: anthropic("claude-sonnet-4-5"),
        system: getSystemPrompt(subtask.specialist),
        tools: getToolsForSpecialist(subtask.specialist),
        prompt: subtask.description,
        maxSteps: 10,
      })
    )
  );

  // Agente sintetizador consolida resultados
  const { text: finalReport } = await generateText({
    model: anthropic("claude-opus-4-5"),
    prompt: `Consolida estos ${results.length} reportes:\n${results.map(r => r.text).join("\n\n")}`,
  });

  return finalReport;
}
```

### Agente con streaming (UI en tiempo real)

```typescript
// API route con agente streaming
export async function POST(req: Request) {
  const { task } = await req.json();

  const result = streamText({
    model: anthropic("claude-opus-4-5"),
    system: "Eres un agente que resuelve tareas paso a paso.",
    prompt: task,
    tools: agentTools,
    maxSteps: 15,
    onChunk: ({ chunk }) => {
      if (chunk.type === "tool-call") {
        // El cliente puede mostrar "Ejecutando: read_file..."
      }
    }
  });

  return result.toDataStreamResponse();
}
```

```tsx
// Frontend con useChat para el agente
const { messages, isLoading } = useChat({
  api: "/api/agent",
  initialMessages: []
});

// messages incluye tool calls y results visibles en m.toolInvocations
```

### Control de bucle: cuándo parar

```typescript
import { generateText, stopWhen } from "ai";

const result = await generateText({
  model: anthropic("claude-sonnet-4-5"),
  tools: agentTools,
  maxSteps: 50,
  // Parar cuando se alcanza un límite de tool calls
  stopWhen: stopWhen.toolCallCount(10),
  prompt: "..."
});

// O con lógica custom
stopWhen: (state) => {
  const bashCalls = state.steps
    .flatMap(s => s.toolCalls)
    .filter(tc => tc.toolName === "bash").length;
  return bashCalls > 5;  // máximo 5 llamadas bash
},
```

### Error handling en agentes

```typescript
const result = await generateText({
  model: anthropic("claude-opus-4-5"),
  tools: {
    risky_operation: tool({
      description: "Operación que puede fallar",
      parameters: z.object({ id: z.string() }),
      execute: async ({ id }) => {
        try {
          return await performRiskyOp(id);
        } catch (error) {
          // El agente recibe el error y puede decidir qué hacer
          return { error: error.message, recovered: false };
        }
      }
    })
  },
  maxSteps: 10,
  prompt: "Intenta la operación, y si falla, busca una alternativa"
});
```

## Conexiones
- Relacionado con: [[vercel-ai-sdk-overview]], [[vercel-ai-sdk-tools]], [[vercel-ai-sdk-streaming]]
- Contrasta con: [[agent-sdk-overview]] (Python, CLI-focused vs web-focused)
- Pattern similar: [[claude-code-subagentes]] (subagentes en el CLI)
- Para producción: considerar [[claude-code-workflow-patterns]]

## Fuentes
- Documentación oficial Vercel AI SDK — sección Agents

---

## Timeline

- 2026-04-07: página creada desde docs oficiales del Vercel AI SDK
