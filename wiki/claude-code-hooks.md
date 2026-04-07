---
title: Claude Code — Hooks
type: concept
tags: [claude-code, hooks, automatizacion, workflow]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Hooks

> Puntos de extensión del lifecycle de Claude Code que permiten ejecutar comandos, prompts o agentes en respuesta a eventos del sistema.

---

## Contexto

Los hooks son el mecanismo de automatización más potente de Claude Code. Permiten encadenar comportamientos al ciclo de vida de la sesión sin tocar el código del agente. Desde notificaciones desktop hasta quality gates automáticos, los hooks convierten a Claude Code en un sistema orquestable.

Disponibles desde v2.x. El campo `if` para filtrar por tool+args requiere v2.1.85+. Auto-memory requiere v2.1.59+.

## Detalle

### Eventos del lifecycle (25+)

| Evento | Cuándo se dispara |
|--------|------------------|
| `SessionStart` | Inicio de sesión (incluye post-compact) |
| `SessionEnd` | Fin de sesión |
| `PreToolUse` | Antes de ejecutar cualquier tool |
| `PostToolUse` | Después de ejecutar cualquier tool |
| `PostToolUseFailure` | Cuando un tool falla |
| `PermissionRequest` | Claude pide permiso para una acción |
| `PermissionDenied` | Permiso rechazado por el sistema |
| `Stop` | Claude termina de responder |
| `StopFailure` | Claude no pudo completar la tarea |
| `Notification` | Claude envía una notificación |
| `SubagentStart` | Inicia un subagente |
| `SubagentStop` | Termina un subagente |
| `TaskCreated` | Nueva tarea creada en agent teams |
| `TaskCompleted` | Tarea completada en agent teams |
| `CwdChanged` | Cambio de directorio de trabajo |
| `FileChanged` | Archivo modificado en el filesystem |
| `ConfigChange` | Cambio en configuración |
| `PreCompact` | Antes de compactar el contexto |
| `PostCompact` | Después de compactar el contexto |
| `InstructionsLoaded` | CLAUDE.md cargado en sesión |
| `WorktreeCreate` | Git worktree creado |
| `WorktreeRemove` | Git worktree eliminado |
| `Elicitation` | MCP server pide input al usuario |
| `TeammateIdle` | Teammate sin tareas en agent team |
| `UserPromptSubmit` | Usuario envía un prompt |

### Tipos de hooks

**`command`** — shell script, el más común:
```json
{
  "event": "PostToolUse",
  "if": "Edit|Write",
  "hook": {
    "type": "command",
    "command": "npx prettier --write $CLAUDE_TOOL_INPUT_FILE_PATH"
  }
}
```

**`prompt`** — LLM single-turn, para análisis/validación:
```json
{
  "event": "PreToolUse",
  "if": "Bash",
  "hook": {
    "type": "prompt",
    "prompt": "Analiza si este comando bash es seguro. Si contiene rm -rf, responde con exit code 2."
  }
}
```

**`agent`** — LLM multi-turn con tools, para verificación compleja:
```json
{
  "event": "Stop",
  "hook": {
    "type": "agent",
    "agent": "test-verifier",
    "prompt": "Verifica que los tests pasen antes de reportar éxito."
  }
}
```

**`http`** — POST a endpoint externo:
```json
{
  "event": "PostToolUse",
  "hook": {
    "type": "http",
    "url": "https://webhooks.example.com/claude-activity",
    "headers": { "Authorization": "Bearer $WEBHOOK_TOKEN" }
  }
}
```

### Exit codes

| Código | Comportamiento |
|--------|---------------|
| `0` | Proceder normalmente |
| `2` | Bloquear acción, pasar stderr a Claude como feedback |
| Otro | Proceder silenciosamente (error ignorado) |

### Structured JSON output

Para hooks de tipo `command` o `prompt` que necesitan control fino:

```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow",
    "permissionDecisionReason": "Verificado: comando seguro"
  }
}
```

Valores de `permissionDecision`: `"allow"`, `"deny"`, `"ask"`, `"defer"`.

### Field `if` — filtrado por tool+args (v2.1.85+)

Filtra en qué tools se activa el hook. Soporta patrones tipo glob y regex:

```json
{ "if": "Edit|Write" }
{ "if": "Bash(git *)" }
{ "if": "mcp__github__.*" }
{ "if": "Bash(rm *)" }
```

Sin `if`, el hook se dispara en todos los eventos del tipo especificado.

### Scopes de configuración

Los hooks se definen en `settings.json` bajo la clave `hooks`:

- **Global** `~/.claude/settings.json` — aplica a todas las sesiones
- **Proyecto** `.claude/settings.json` — aplica al proyecto, se versiona con git
- **Local** `.claude/settings.local.json` — proyecto pero no versionado (secrets locales)

Los arrays de hooks hacen merge entre scopes. Si global define un hook de notificación y proyecto define uno de formato, ambos se ejecutan.

### Casos de uso con JSON real

**Notificación desktop macOS:**
```json
{
  "hooks": [{
    "event": "Stop",
    "hook": {
      "type": "command",
      "command": "osascript -e 'display notification \"Claude terminó\" with title \"Claude Code\"'"
    }
  }]
}
```

**Auto-format Prettier en cada escritura:**
```json
{
  "hooks": [{
    "event": "PostToolUse",
    "if": "Edit|Write",
    "hook": {
      "type": "command",
      "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\" 2>/dev/null || true"
    }
  }]
}
```

**Proteger archivos sensibles (bloquea con feedback):**
```bash
#!/bin/bash
# protect-files.sh
FILE="$CLAUDE_TOOL_INPUT_FILE_PATH"
PROTECTED=(".env" "package-lock.json" ".env.local" ".env.production")
for p in "${PROTECTED[@]}"; do
  if [[ "$FILE" == *"$p"* ]]; then
    echo "Archivo protegido: $FILE — edición bloqueada" >&2
    exit 2
  fi
done
```
```json
{
  "hooks": [{
    "event": "PreToolUse",
    "if": "Edit|Write",
    "hook": { "type": "command", "command": "bash .claude/protect-files.sh" }
  }]
}
```

**Re-inyectar contexto post-compact:**
```json
{
  "hooks": [{
    "event": "SessionStart",
    "if": "compact",
    "hook": {
      "type": "command",
      "command": "cat .claude/context-snapshot.md"
    }
  }]
}
```

**Auto-approve ExitPlanMode:**
```json
{
  "hooks": [{
    "event": "PermissionRequest",
    "if": "ExitPlanMode",
    "hook": {
      "type": "command",
      "command": "echo '{\"hookSpecificOutput\":{\"permissionDecision\":\"allow\"}}'"
    }
  }]
}
```

**Reload direnv en CwdChanged:**
```json
{
  "hooks": [{
    "event": "CwdChanged",
    "hook": { "type": "command", "command": "direnv allow . 2>/dev/null || true" }
  }]
}
```

**Log de comandos Bash:**
```json
{
  "hooks": [{
    "event": "PreToolUse",
    "if": "Bash",
    "hook": {
      "type": "command",
      "command": "echo \"[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $CLAUDE_TOOL_INPUT_COMMAND\" >> ~/.claude/bash-history.log"
    }
  }]
}
```

**Stop hook con agente verificador de tests:**
```json
{
  "hooks": [{
    "event": "Stop",
    "hook": {
      "type": "agent",
      "prompt": "Ejecuta los tests del proyecto. Si fallan, reporta cuáles fallaron. Usa Bash para correr npm test.",
      "agent": "general-purpose"
    }
  }]
}
```

### Stop hook — evitar loop infinito

Un Stop hook que a su vez hace que Claude responda puede dispararse infinitamente. Solución: parsear `$CLAUDE_STOP_HOOK_ACTIVE`:

```bash
#!/bin/bash
if [ "$CLAUDE_STOP_HOOK_ACTIVE" = "1" ]; then
  exit 0  # ya estamos en un stop hook, no hacer nada
fi
# lógica del hook aquí
npm test || exit 2
```

### Variables de entorno disponibles en hooks

| Variable | Descripción |
|----------|-------------|
| `$CLAUDE_TOOL_NAME` | Nombre del tool siendo ejecutado |
| `$CLAUDE_TOOL_INPUT_*` | Inputs del tool (varía por tool) |
| `$CLAUDE_SESSION_ID` | ID de la sesión actual |
| `$CLAUDE_STOP_HOOK_ACTIVE` | `1` si estamos dentro de un stop hook |
| `$CLAUDE_CWD` | Directorio de trabajo actual |

### Debugging

- `/hooks` en el REPL — lista hooks activos y sus configuraciones
- `Ctrl+O` — toggle verbose mode, muestra qué hooks se están ejecutando
- `claude --debug` — modo debug completo con trazas de hooks
- Hook no dispara: verificar `if` matcher, scope del settings.json, y que el evento sea correcto

### Hooks en skills y agents

Los hooks se pueden definir en el frontmatter de un skill para que se activen automáticamente cuando el skill está en ejecución:

```yaml
---
name: deploy
hooks:
  - event: Stop
    hook:
      type: command
      command: "echo 'Deploy completado' | slack-notify"
---
```

## Conexiones

- Relacionado con: [[claude-code-skills]], [[claude-code-settings]], [[claude-code-permisos]]
- Parte de: [[claude-code-workflow-patterns]], [[claude-code-agent-teams]]
- Habilita patrones de: [[context-engineering-patterns]], [[ai-development-workflows]]
- Ver también: [[claude-code-subagentes]] (SubagentStart/SubagentStop hooks), [[claude-code-context-window]] (PreCompact/PostCompact)

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
