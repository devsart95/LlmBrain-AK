---
title: Claude Code — Hooks Ecosystem
type: overview
tags: [claude-code, hooks, seguridad, calidad, automatización]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Hooks Ecosystem

> Librerías, SDKs y herramientas construidas sobre el sistema de hooks de Claude Code.

## Contexto

El sistema de hooks de Claude Code tiene una comunidad activa construyendo abstracciones por encima. Hay SDKs en múltiples lenguajes, herramientas de seguridad específicas y patterns de calidad de código probados en producción.

## Detalle

### SDKs por lenguaje

#### TypeScript — claude-hooks (johnlindquist)

```typescript
import { createHook } from "@johnlindquist/claude-hooks";

const hook = createHook({
  event: "PreToolUse",
  match: { tool: "bash" },
  handler: async (event) => {
    const cmd = event.input.command;
    if (isDestructive(cmd)) {
      return { permissionDecision: "deny", reason: "Comando destructivo" };
    }
    return { permissionDecision: "approve" };
  }
});

hook.start();
```

Interface TypeScript con type safety completo sobre el JSON de hooks.

#### Python — cchooks (GowayLee)

```python
from cchooks import ClaudeHook, ToolEvent

@ClaudeHook.pre_tool_use(tool="text_editor")
async def on_file_write(event: ToolEvent):
    # Interceptar escrituras de archivos
    path = event.input.get("path", "")
    if path.endswith(".env"):
        return event.deny("No escribir archivos .env directamente")
    return event.approve()

ClaudeHook.run()
```

API limpia con decorators. Abstrae el JSON de configuración de hooks.

#### PHP — claude-code-hooks-sdk (beyondcode)

```php
use BeyondCode\ClaudeHooks\HookResponse;

$response = HookResponse::make()
    ->approve()
    ->withUpdatedInput(['command' => $sanitizedCommand]);

return $response->toJson();
```

Fluent API al estilo Laravel. Para equipos PHP que necesitan hooks en sus pipelines.

#### Go — cc-tools (Veraticus)

```go
// Alta performance con mínimo overhead
hook := cctool.NewHook(cctool.PreToolUse)
hook.OnBash(func(cmd string) cctool.Decision {
    if strings.Contains(cmd, "rm -rf") {
        return cctool.Deny("Comando peligroso")
    }
    return cctool.Approve()
})
```

Ideal para hooks que necesitan correr en <5ms (linting, validación inline).

---

### Seguridad

#### parry (vaporif)

Scanner de prompt injection para hooks:

```bash
# Configura parry como PostToolUse hook
# Escanea outputs de tools antes de que lleguen al LLM

{
  "hooks": {
    "PostToolUse": [{
      "matcher": {"tool": "*"},
      "hooks": [{"type": "command", "command": "parry scan --stdin"}]
    }]
  }
}
```

Detecta:
- Prompt injection en outputs de tools
- Secrets/tokens en respuestas de APIs externas
- Intentos de data exfiltration
- Patrones sospechosos de tool manipulation

Estado: early development, pero el approach es sólido para producción.

#### Dippy (ldayton) — como hook de permisos

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": {"tool": "bash"},
      "hooks": [{
        "type": "command",
        "command": "dippy check --command \"${CLAUDE_TOOL_INPUT}\""
      }]
    }]
  }
}
```

Usa AST parsing para clasificar comandos bash como seguros o peligrosos. Resuelve permission fatigue sin deshabilitar protecciones.

---

### Calidad de Código

#### TDD Guard (nizos)

Hook que enforcea TDD en tiempo real:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": {"tool": "text_editor", "action": "write"},
      "hooks": [{"type": "command", "command": "tdd-guard check"}]
    }]
  }
}
```

Comportamiento:
1. Cada vez que Claude escribe un archivo de código, TDD Guard verifica
2. Si hay código de producción nuevo sin test correspondiente → bloquea
3. Si el test falla (red) → permite seguir
4. Si el test pasa pero el código está incompleto → bloquea
5. Enforcea el ciclo Red → Green → Refactor

Caso de uso real: proyectos donde TDD es obligatorio y no se puede confiar en que Claude lo siga solo.

#### TypeScript Quality Hooks (bartolli)

Hook de calidad para proyectos TypeScript/Node.js:

```bash
# Ejecuta en <5ms gracias a SHA256 caching de la config
typecheck-hook: npm run typecheck → bloquea si falla
eslint-hook: eslint --fix → auto-fix inline
prettier-hook: prettier --write → formato automático
```

Caching SHA256 de la config de TypeScript/ESLint/Prettier: si no cambió la config, no re-compila. Resultado: validación en tiempo real sin ralentizar el workflow.

---

### UX de Desarrollo

#### Claudio (ctoth)

Agrega sonidos nativos del OS a Claude Code:
```json
{
  "hooks": {
    "Stop": [{"type": "command", "command": "claudio play done"}],
    "PreToolUse": [{"type": "command", "command": "claudio play tool-call"}]
  }
}
```
Notificaciones auditivas sin interrumpir el flujo. El autor dice "sparks joy".

#### CC Notify (dazuiba)

Notificaciones de desktop cuando Claude necesita input o termina una task:
- One-click jump de vuelta a VS Code
- Task duration display
- Sin tener que monitorear el terminal

#### HCOM — Hook Communications (aannoo)

Comunicación en tiempo real entre subagentes via hooks:
```
Agente Principal → @agente-b: "terminé el módulo X, tu turno"
Agente B recibe el mensaje → continúa desde el estado correcto
```

Live dashboard de monitoreo. El curator del awesome-list nota: "prometedor y creativo, aunque inestable en el momento de la publicación."

---

### Especialidades

#### Britfix (Talieisin)

Hook para convertir spelling americano a inglés británico automáticamente:
- Context-aware: solo convierte comentarios y docstrings, nunca identifiers o string literals
- Para proyectos UK/Australian donde el spelling afecta compliance o credibilidad profesional

#### /create-hook command (omril321)

Slash command que genera hooks automáticamente:
- Analiza el setup del proyecto (TypeScript, Prettier, ESLint...)
- Genera la configuración JSON correcta
- Sugiere el tipo de hook adecuado para el caso de uso

---

### Patterns comunes de configuración

#### Hook de seguridad mínimo

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": {"tool": "bash"},
      "hooks": [{
        "type": "command",
        "command": "bash -c 'cmd=\"$CLAUDE_TOOL_INPUT_COMMAND\"; echo \"$cmd\" | grep -qE \"rm -rf|DROP TABLE|> /etc\" && echo \\'BLOCKED\\' && exit 2 || exit 0'"
      }]
    }]
  }
}
```

#### Hook de audit log

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": {"tool": "*"},
      "hooks": [{
        "type": "command",
        "command": "bash -c 'echo \"$(date): $CLAUDE_TOOL_NAME\" >> ~/.claude/audit.log'"
      }]
    }]
  }
}
```

#### Hook de commit automático

```json
{
  "hooks": {
    "Stop": [{
      "matcher": {},
      "hooks": [{
        "type": "command",
        "command": "bash -c 'cd \"$CLAUDE_PROJECT_DIR\" && git diff --quiet || git add -A && git commit -m \"auto: checkpoint $(date +%H:%M)\"'"
      }]
    }]
  }
}
```

## Conexiones
- Relacionado con: [[claude-code-hooks]], [[claude-code-permisos]]
- Seguridad de MCP: [[mcp-seguridad]] (mismo concepto de prompt injection)
- Para el SDK Python de hooks: [[agent-sdk-hooks]] (diferencia: estos son shell-level, los del SDK son Python callbacks)

## Fuentes
- `https://github.com/hesreallyhim/awesome-claude-code` — sección Hooks

---

## Timeline

- 2026-04-07: página creada desde awesome-claude-code
