---
title: Claude Code — CLI Referencia
type: concept
tags: [claude-code, cli, comandos, referencia]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — CLI Referencia

> Referencia completa de flags de línea de comando, comandos REPL, y keybindings de Claude Code.

---

## Contexto

Claude Code tiene dos interfaces: la CLI (para lanzar sesiones, scripts, CI) y el REPL (los comandos `/` dentro de una sesión activa). Conocer los flags correctos evita configurar cosas que ya se pueden hacer desde la línea de comando.

## Detalle

### Flags de la CLI

#### Modo de sesión

```bash
claude                          # sesión interactiva nueva
claude -p "prompt"              # non-interactive, ejecuta y sale
claude --continue               # retomar la sesión más reciente
claude --resume                 # elegir sesión de una lista
```

#### Output format (non-interactive)

```bash
claude -p "..." --output-format text        # texto plano (default)
claude -p "..." --output-format json        # JSON con metadata completa
claude -p "..." --output-format stream-json # chunks JSON en streaming
```

**JSON output incluye:**
```json
{
  "response": "...",
  "model": "claude-opus-4",
  "usage": {
    "input_tokens": 1234,
    "output_tokens": 567
  },
  "session_id": "...",
  "stop_reason": "end_turn"
}
```

#### Permisos

```bash
# Modo de operación
claude --permission-mode default        # pregunta todo (default)
claude --permission-mode acceptEdits    # acepta edits, pregunta Bash
claude --permission-mode auto           # clasificador ML
claude --permission-mode bypassPermissions  # sin restricciones

# Sin sistema de permisos (CI/aislado)
claude --dangerously-skip-permissions

# Tools específicos
claude --allowedTools "Read,Grep,Glob"
claude --allowedTools "Bash(git *),Edit(*.ts)"
claude --disallowedTools "Write,Edit"

# Directorios adicionales con acceso
claude --add-dir /home/user/shared-libs
claude --add-dir /tmp/artifacts
```

#### Modelo

```bash
claude --model claude-opus-4
claude --model claude-sonnet-4-5
claude --model claude-haiku-4
```

El modelo también se puede setear en `settings.json` para que sea el default de todas las sesiones.

#### Contexto adicional

```bash
# Agregar al system prompt
claude --append-system-prompt "Siempre responder en español. Usar TypeScript estricto."

# Directorio de trabajo específico
claude --cwd /path/to/project
```

#### Debug

```bash
claude --debug          # traces completos de tools, hooks, permisos
claude --verbose        # output más detallado (similar a Ctrl+O)
```

#### Subcomandos MCP

```bash
claude mcp add <name> -- <command> [args...]
claude mcp add <name> --url <http-url>
claude mcp add <name> --scope project -- <command>
claude mcp list
claude mcp get <name>
claude mcp remove <name>
claude mcp tools <name>         # listar tools del servidor
```

### Comandos REPL (slash commands)

#### Gestión de sesión y contexto

| Comando | Descripción |
|---------|-------------|
| `/clear` | Limpiar historial completo de la sesión |
| `/compact` | Compactar conversación (Claude decide qué preservar) |
| `/compact <instrucciones>` | Compactar con guidance de qué mantener |
| `/rewind` | Menú de checkpoints (restaurar conversación/código/ambos) |
| `/btw <pregunta>` | Pregunta en overlay separado, no entra al contexto |
| `/rename <nombre>` | Renombrar la sesión actual |

#### Configuración

| Comando | Descripción |
|---------|-------------|
| `/config` | UI interactivo de settings |
| `/permissions` | Gestionar allow/deny rules interactivamente |
| `/hooks` | Ver hooks activos y sus configuraciones |
| `/memory` | Ver archivos CLAUDE.md y MEMORY.md cargados |
| `/init` | Generar CLAUDE.md base desde el codebase |

#### Skills y herramientas

| Comando | Descripción |
|---------|-------------|
| `/batch <tarea>` | Orquestar migración masiva en paralelo con worktrees |
| `/debug` | Root cause debugging interactivo |
| `/loop <intervalo> <comando>` | Ejecutar comando repetidamente |
| `/simplify` | Revisar código cambiado para reuso y calidad |
| `/<nombre-skill>` | Invocar skill personalizado |

#### Modos

| Comando | Descripción |
|---------|-------------|
| `Ctrl+Shift+P` / `Shift+Tab` | Toggle Plan Mode (solo lectura) |

### Keybindings del REPL

| Keybinding | Acción |
|-----------|--------|
| `Ctrl+G` | Abrir plan actual en editor de texto para editar |
| `Ctrl+O` | Toggle verbose mode (ver tools ejecutándose) |
| `Ctrl+T` | Ver task list de agent teams |
| `Shift+Down` | Ciclar entre teammates (agent teams) |
| `Esc` | Interrumpir operación en curso |
| `Esc+Esc` | Menú de checkpoints (equivale a `/rewind`) |
| `Ctrl+C` | Salir del REPL |

### Patrones de uso frecuente

**CI/CD básico:**
```bash
claude -p "correr audit de seguridad en src/ y reportar hallazgos críticos" \
  --allowedTools "Read,Grep,Glob,Bash(npm audit)" \
  --output-format json \
  --dangerously-skip-permissions
```

**Análisis de PR:**
```bash
git diff main...HEAD | claude -p "revisar estos cambios: seguridad, tests faltantes, N+1 queries" \
  --allowedTools "Read,Grep,Glob" \
  --output-format text
```

**Migración masiva:**
```bash
find src/ -name "*.js" | while read f; do
  claude -p "convertir $f a TypeScript estricto. Output: ${f%.js}.ts" \
    --allowedTools "Read,Write" &
done
wait
```

**Debug con contexto de logs:**
```bash
tail -100 logs/app.log | claude -p "identificar el error y su causa raíz"
```

**Investigación antes de implementar:**
```bash
claude --permission-mode acceptEdits
# Activar Plan Mode: Shift+Tab
# Explorar, entender, planear
# Desactivar Plan Mode: Shift+Tab
# Implementar
```

### Variables de entorno de la CLI

| Variable | Descripción |
|----------|-------------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `1` para habilitar agent teams |
| `CLAUDE_CODE_NEW_INIT` | `1` para `/init` interactivo multi-fase |
| `ANTHROPIC_API_KEY` | API key (requerida) |
| `CLAUDE_MODEL` | Modelo default (alternativa a `--model`) |

### Stdin y pipes

Claude Code puede recibir contexto vía stdin:

```bash
# Desde pipe
cat archivo.log | claude -p "analizar errores"

# Desde process substitution
claude -p "comparar estos dos outputs" \
  <(npm test 2>&1) \
  <(npm test -- --watch=false 2>&1)

# JSON desde API
curl -s https://api.example.com/data | claude -p "resumir estos datos"
```

### `--append-system-prompt` — inyectar instrucciones

```bash
# Para sesiones específicas sin modificar CLAUDE.md
claude --append-system-prompt "
Contexto: estoy haciendo un audit de seguridad.
Enfocarse en: injection, secrets exposure, auth issues.
Formato: bullet points con severidad [CRITICAL/HIGH/MEDIUM/LOW].
"
```

Útil para sesiones especializadas temporales sin contaminar la configuración permanente del proyecto.

### Salida de `--output-format json` completa

```json
{
  "type": "result",
  "subtype": "success",
  "response": "El análisis muestra...",
  "model": "claude-opus-4",
  "session_id": "sess_01abc...",
  "cost_usd": 0.0042,
  "usage": {
    "input_tokens": 2341,
    "output_tokens": 897,
    "cache_read_input_tokens": 1200,
    "cache_creation_input_tokens": 0
  },
  "duration_ms": 3421,
  "stop_reason": "end_turn",
  "tools_used": ["Read", "Grep", "Glob"],
  "files_modified": []
}
```

Útil para: auditoría de costos, métricas de CI, procesamiento programático del resultado.

## Conexiones

- Relacionado con: [[claude-code-workflow-patterns]], [[claude-code-permisos]], [[claude-code-settings]]
- Parte de: [[claude-code-best-practices]]
- Habilita: [[claude-code-mcp]] (subcomandos `claude mcp`), [[claude-code-agent-teams]] (variable de entorno)
- Ver también: [[ai-development-workflows]] (patrones de non-interactive mode), [[context-engineering-patterns]]

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
