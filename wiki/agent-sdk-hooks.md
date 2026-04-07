---
title: Claude Agent SDK — Hooks
type: concept
tags: [claude, agent-sdk, hooks, callbacks, python]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Agent SDK — Hooks

> Sistema de callbacks del ciclo de vida para interceptar, modificar y controlar la ejecución de agentes.

## Contexto

Los hooks del Agent SDK son equivalentes a los hooks de Claude Code CLI pero en forma programática. Permiten auditar, bloquear, modificar inputs/outputs de herramientas y reaccionar a eventos del agente.

## Detalle

### Tipos de hooks principales

| Hook | Cuándo se llama |
|------|-----------------|
| `PreToolUse` | Antes de ejecutar cualquier tool |
| `PostToolUse` | Después de ejecutar cualquier tool |
| `Stop` | Cuando el agente termina |
| `SubagentStart` | Cuando se lanza un subagente |
| `SubagentStop` | Cuando termina un subagente |

### HookMatcher — filtrar por tool

```python
from anthropic.sdk import HookMatcher

# Solo interceptar bash
bash_hook = HookMatcher(tool_name="bash")

# Cualquier tool
any_hook = HookMatcher(tool_name="*")

# Por prefijo
file_hooks = HookMatcher(tool_name="text_editor*")
```

### PreToolUse — interceptar antes

```python
def on_pre_tool_use(event):
    tool = event.tool_name
    input_data = event.input

    # Bloquear comandos peligrosos
    if tool == "bash":
        cmd = input_data.get("command", "")
        if "rm -rf" in cmd:
            return {"permissionDecision": "deny", "reason": "Comando destructivo bloqueado"}

    # Modificar el input antes de ejecutar
    if tool == "text_editor" and "action" in input_data:
        if input_data["action"] == "write":
            # Normalizar contenido antes de escribir
            event.updatedInput = {
                **input_data,
                "content": input_data["content"].strip()
            }

    # Aprobar explícitamente
    return {"permissionDecision": "approve"}
```

### permissionDecision — valores posibles

```python
# Aprobar sin modificar
{"permissionDecision": "approve"}

# Denegar con razón
{"permissionDecision": "deny", "reason": "Explicación para el agente"}

# Aprobar con input modificado
{"permissionDecision": "approve", "updatedInput": {...}}
```

### PostToolUse — reaccionar al resultado

```python
def on_post_tool_use(event):
    tool = event.tool_name
    output = event.output
    duration_ms = event.duration_ms

    # Auditoría
    print(f"[{tool}] completado en {duration_ms}ms")

    # Logging de salida
    if tool == "bash":
        if output.get("exit_code") != 0:
            log_error(f"Bash falló: {output.get('stderr')}")
```

### Stop hook

```python
def on_stop(event):
    reason = event.stop_reason  # "end_turn" | "max_tokens" | "stop_sequence"
    usage = event.usage  # tokens consumidos

    print(f"Agente terminó: {reason}")
    print(f"Tokens: {usage.input_tokens} in, {usage.output_tokens} out")
```

### SubagentStart / SubagentStop

```python
def on_subagent_start(event):
    subagent_id = event.subagent_id
    prompt = event.prompt
    print(f"Subagente {subagent_id} iniciado: {prompt[:50]}...")

def on_subagent_stop(event):
    subagent_id = event.subagent_id
    result = event.result
    print(f"Subagente {subagent_id} terminó")
```

### Hooks asíncronos

```python
import asyncio

async def async_pre_tool_use(event):
    # Puede hacer I/O asíncrono
    await audit_db.log(event.tool_name, event.input)
    return {"permissionDecision": "approve"}
```

### Registrar hooks en el cliente

```python
client = anthropic.Anthropic()

result = client.query(
    prompt="Refactoriza este módulo",
    hooks={
        "preToolUse": on_pre_tool_use,
        "postToolUse": on_post_tool_use,
        "stop": on_stop,
        "subagentStart": on_subagent_start,
        "subagentStop": on_subagent_stop,
    }
)
```

### Webhook HTTP (alternativa)

Para arquitecturas distribuidas, los hooks pueden ser endpoints HTTP:

```python
result = client.query(
    prompt="...",
    webhook_hooks={
        "preToolUse": "https://my-service.com/hooks/pre-tool",
        "postToolUse": "https://my-service.com/hooks/post-tool",
    }
)
```

El SDK hace POST al endpoint con el evento en JSON y espera la respuesta de control.

## Conexiones
- Relacionado con: [[agent-sdk-overview]], [[claude-code-hooks]]
- Diferencia con CLI: [[claude-code-hooks]] opera a nivel shell/proceso, estos hooks son callbacks Python/TS en el mismo proceso
- Usado para: auditoría, seguridad, modificación de comportamiento

## Fuentes
- Documentación oficial Claude Agent SDK — sección Hooks

---

## Timeline

- 2026-04-07: página creada desde docs oficiales del Agent SDK
