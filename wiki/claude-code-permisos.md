---
title: Claude Code — Sistema de Permisos
type: concept
tags: [claude-code, permisos, seguridad, configuracion]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Sistema de Permisos

> Sistema de control de acceso multi-capa que determina qué acciones puede ejecutar Claude Code, desde reglas declarativas en JSON hasta hooks programáticos y modos de operación predefinidos.

---

## Contexto

Claude Code ejecuta código en tu sistema. El sistema de permisos es la barrera entre "Claude puede hacer todo" y "Claude puede hacer exactamente lo que necesita para esta tarea". Entenderlo permite calibrar el balance entre autonomía y control según el contexto: desarrollo local, CI/CD, producción.

## Detalle

### Modos de operación

| Modo | Comportamiento | Uso |
|------|---------------|-----|
| `default` | Pregunta antes de cada acción no permitida explícitamente | Desarrollo interactivo |
| `acceptEdits` | Acepta edits automáticamente, pregunta para Bash y otros | Balance autonomía/control |
| `auto` | Clasificador ML decide automáticamente | Operación con supervisión mínima |
| `bypassPermissions` | Sin restricciones de permisos | CI/scripts — PELIGROSO en entornos no aislados |

Activar desde CLI:
```bash
claude --permission-mode auto
claude --permission-mode bypassPermissions  # solo en CI con aislamiento
```

### Modo `auto` — clasificador ML

No es "sin restricciones". Es un clasificador de modelo separado que evalúa cada acción y bloquea automáticamente:

- **Scope escalation**: Claude pide permisos para algo mayor a lo que debería necesitar
- **Infra desconocida**: comandos que tocan infraestructura no mencionada en el contexto
- **Hostile content**: inyección de instrucciones via contenido del archivo (prompt injection)
- **Destructive operations**: `rm -rf`, drops de DB, overwrite de backups

El clasificador tiene sus propios false positives — en algunos casos puede ser más restrictivo de lo esperado.

### Permission rules — sintaxis

```
Bash(<pattern>)           — comandos shell
Edit(<file-pattern>)      — edición de archivos existentes
Write(<file-pattern>)     — creación de archivos nuevos
Read(<file-pattern>)      — lectura de archivos
Skill(<skill-name>)       — invocación de skills
mcp__<server>__<tool>     — tools de MCP servers
mcp__<server>__*          — todos los tools de un MCP server
WebFetch                  — cualquier request HTTP
WebFetch(<url-pattern>)   — request a URL específica
Task                      — crear subagentes/tareas
```

**Glob patterns disponibles:**
```
*         — cualquier cosa (no incluye /)
**        — cualquier cosa incluyendo /
?         — cualquier carácter
{a,b}     — alternativas
```

### Allow rules — skip del diálogo

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm run *)",
      "Bash(docker compose *)",
      "Edit(src/**/*.{ts,tsx})",
      "Write(src/**/*.{ts,tsx})",
      "Read(**)",
      "mcp__github__list_*",
      "mcp__github__get_*"
    ]
  }
}
```

Claude ejecuta sin pedir confirmación. El diálogo no aparece para estas acciones.

### Deny rules — bloqueo absoluto

```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf *)",
      "Bash(DROP *)",
      "Edit(.env*)",
      "Edit(**/secrets/**)",
      "Write(**/prod/**)",
      "mcp__github__delete_*",
      "mcp__postgres__execute"
    ]
  }
}
```

**Deny siempre gana sobre allow**. Incluso si el usuario dice "hazlo de todas formas", una deny rule no se puede sobreescribir desde el REPL. Solo modificando `settings.json`.

### `/permissions` — gestión interactiva

```
/permissions
```

UI de texto en el REPL que muestra:
- Todas las reglas activas y su scope
- Acciones pendientes de aprobación
- Historial de permisos otorgados/negados en la sesión

Permite agregar/remover reglas sin editar JSON manualmente.

### Hooks y permisos — interacción

Los hooks pueden **tighten** (endurecer) permisos pero **no pueden loosenen** (relajar) restricciones:

```json
{
  "hooks": [{
    "event": "PreToolUse",
    "if": "Edit",
    "hook": {
      "type": "command",
      "command": "bash .claude/check-protected-files.sh"
    }
  }]
}
```

Si el script sale con código 2, bloquea la acción incluso si hay una allow rule.

**Hook allow no bypasea deny rules.** Si `Edit(.env*)` está en deny, un hook que retorne `permissionDecision: "allow"` no sirve de nada.

```json
// Esto NO funciona si hay una deny rule para Edit(.env*)
{
  "hookSpecificOutput": {
    "permissionDecision": "allow"   // ignorado — deny rule tiene prioridad
  }
}
```

### PreToolUse + exit 2 — el bloqueador más fuerte

Un PreToolUse hook con exit 2 bloquea **incluso en bypassPermissions mode**:

```bash
#!/bin/bash
# protect-production.sh
if [[ "$CLAUDE_TOOL_INPUT_COMMAND" == *"--env production"* ]]; then
  echo "Comandos con --env production están bloqueados en esta sesión" >&2
  exit 2
fi
```

```json
{
  "hooks": [{
    "event": "PreToolUse",
    "if": "Bash",
    "hook": { "type": "command", "command": "bash .claude/protect-production.sh" }
  }]
}
```

Útil para: proteger entornos específicos, prevenir operaciones accidentales, quality gates.

### `--dangerously-skip-permissions`

```bash
claude --dangerously-skip-permissions -p "correr audit completo"
```

Deshabilita el sistema de permisos completamente. **Solo para**:
- CI/CD en contenedores aislados (sin acceso a producción)
- Scripts de migración en entornos efímeros
- Automatización donde el aislamiento es a nivel de infra

**Jamás usar** en:
- Máquina de desarrollo con acceso a producción
- Entornos con credenciales reales activas
- Sesiones interactivas donde el output puede incluir contenido externo (prompt injection risk)

### Sandboxing — aislamiento OS

```bash
# Activar sandboxing
claude --sandbox

# O en settings.json
{ "sandbox": true }
```

Con sandboxing activo:
- **Filesystem**: acceso limitado al directorio de trabajo y directorios explícitamente permitidos
- **Network**: solo loopback + hosts explícitamente permitidos
- **System calls**: restringidos a operaciones necesarias

Ideal para analizar código desconocido o ejecutar snippets de fuentes externas.

### `--add-dir` — directorios adicionales

```bash
# Permitir acceso a directorio adicional
claude --add-dir /home/user/shared-libs

# Múltiples directorios
claude --add-dir /tmp/artifacts --add-dir ~/dotfiles
```

**Importante**: `--add-dir` otorga acceso a archivos, **no descubre CLAUDE.md** en ese directorio. Solo el directorio de trabajo principal (cwd) triggerea CLAUDE.md discovery.

### Flujo de decisión de un tool

```
Claude quiere ejecutar Edit(src/config/.env.production)
    ↓
¿Hay una deny rule que matchee? → SÍ → BLOQUEAR (con mensaje)
    ↓ NO
¿Hay un PreToolUse hook? → hook retorna exit 2 → BLOQUEAR (stderr → Claude)
    ↓ hook OK
¿Hay una allow rule que matchee? → SÍ → EJECUTAR
    ↓ NO
¿Modo bypassPermissions? → SÍ → EJECUTAR
    ↓ NO
¿Modo acceptEdits y es Edit/Write? → SÍ → EJECUTAR
    ↓ NO
¿Modo auto? → clasificador → EJECUTAR o BLOQUEAR
    ↓ no auto
PREGUNTAR AL USUARIO → usuario allow/deny → EJECUTAR o BLOQUEAR
```

### Configuración por entorno

**Desarrollo local (máxima autonomía):**
```json
{
  "permissions": {
    "allow": ["Bash(*)", "Edit(src/**)", "Write(src/**)", "Read(**)"],
    "deny": ["Edit(.env.production*)", "Bash(* --env prod *)"]
  }
}
```

**CI/CD (non-interactive, aislado):**
```bash
claude --permission-mode bypassPermissions --dangerously-skip-permissions -p "..."
```

**Auditoría de codebase externo (read-only):**
```json
{
  "permissions": {
    "allow": ["Read(**)"],
    "deny": ["Edit(*)", "Write(*)", "Bash(*)", "WebFetch"]
  }
}
```

### Auditoria de permisos

```bash
# Ver todas las acciones permitidas/denegadas en la sesión
claude --debug 2>&1 | grep -E "ALLOW|DENY|BLOCK"

# Log via hook
{
  "hooks": [{
    "event": "PreToolUse",
    "hook": {
      "type": "command",
      "command": "echo \"[$(date)] $CLAUDE_TOOL_NAME: $CLAUDE_TOOL_INPUT_*\" >> .claude/audit.log"
    }
  }]
}
```

## Conexiones

- Relacionado con: [[claude-code-settings]], [[claude-code-hooks]], [[claude-code-mcp]]
- Parte de: [[claude-code-workflow-patterns]], [[claude-code-best-practices]]
- Contrasta con: [[claude-code-agent-teams]] (coordinación sin restricciones adicionales)
- Ver también: [[claude-code-cli-referencia]] (`--permission-mode`, `--dangerously-skip-permissions`, `--add-dir`), [[ai-security-skills]]

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
