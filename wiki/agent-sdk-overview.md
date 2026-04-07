---
title: Claude Agent SDK — Overview
type: concept
tags: [claude, agent-sdk, python, typescript, ai]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Agent SDK — Overview

> SDK oficial de Anthropic para construir agentes de IA sobre Claude. Antes llamado Claude Code SDK.

## Contexto

El Agent SDK permite invocar Claude programáticamente con capacidades agentivas: uso de herramientas, subagentes, sesiones persistentes y MCP. Es la base técnica de Claude Code como producto.

## Detalle

### Función principal: `query()`

```python
import anthropic

client = anthropic.Anthropic()

# Python
messages = client.query(
    prompt="Analiza este código",
    tools=["computer", "bash", "text_editor"],
    session_id="session-abc123"
)
```

```typescript
// TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const messages = await client.beta.messages.create({...});
```

La función `query()` es el entry point principal. Devuelve un stream de eventos o mensajes.

### Herramientas built-in

| Tool | Descripción |
|------|-------------|
| `computer` | Control de interfaz gráfica (screenshots, clicks, teclado) |
| `bash` | Ejecutar comandos shell |
| `text_editor` | Leer/escribir archivos con diffs |

### Hooks callbacks

El SDK expone hooks del ciclo de vida para interceptar eventos:

```python
def on_pre_tool_use(event):
    # Antes de ejecutar cualquier tool
    if event.tool_name == "bash":
        print(f"Comando: {event.input['command']}")

def on_post_tool_use(event):
    # Después de ejecutar el tool
    pass

def on_stop(event):
    # Agente terminó
    pass
```

Ver [[claude-code-hooks]] para referencia completa de hooks disponibles.

### Subagentes

Un agente puede lanzar subagentes para paralelizar trabajo:

```python
# El agente padre puede invocar sub-sesiones independientes
result = await client.query(
    prompt="Analiza en paralelo estos 3 archivos",
    subagent_config={
        "isolation": "worktree",  # copia git aislada
        "model": "claude-sonnet-4-5"
    }
)
```

Ver [[claude-code-subagentes]] para patterns avanzados.

### Integración MCP

```python
client = anthropic.Anthropic()
# MCP servers declarados en .mcp.json o inline
messages = client.query(
    prompt="...",
    mcp_servers=[{
        "name": "filesystem",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    }]
)
```

### Sesiones y continuidad

```python
# Iniciar sesión
result = client.query(prompt="Paso 1")
session_id = result.session_id

# Continuar en la misma sesión
result2 = client.query(
    prompt="Paso 2 — recuerda el contexto",
    session_id=session_id
)

# Fork: nueva rama desde un punto
result3 = client.query(
    prompt="Explorar alternativa",
    resume_session_id=session_id,
    fork=True
)
```

Ver [[agent-sdk-sessions]] para detalles de continue/resume/fork.

## Conexiones
- Relacionado con: [[claude-code-hooks]], [[claude-code-subagentes]], [[agent-sdk-sessions]], [[agent-sdk-hooks]]
- Construido sobre: [[mcp-arquitectura]]
- Usado en: [[claude-code-workflow-patterns]]
- Alternativa: [[vercel-ai-sdk-overview]] para proyectos Next.js/web

## Fuentes
- Documentación oficial Claude Agent SDK

---

## Timeline

- 2026-04-07: página creada desde docs oficiales del Agent SDK
