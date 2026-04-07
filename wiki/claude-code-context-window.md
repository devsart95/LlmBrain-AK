---
title: Claude Code — Context Window y Compaction
type: concept
tags: [claude-code, contexto, compaction, tokens, performance]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Context Window y Compaction

> La constraint fundamental del sistema: el context window se llena, el rendimiento degrada, y el comportamiento se vuelve impredecible. Las herramientas de compaction y rewind son el manejo activo de esa constraint.

---

## Contexto

No es una limitación a tolerar — es la variable de diseño más importante cuando se trabaja con Claude Code. Cada token que consume el contexto es uno menos disponible para instrucciones, código, y razonamiento. Gestionar el contexto activamente es la diferencia entre sesiones de 2 horas productivas y sesiones que se rompen a los 20 minutos.

## Detalle

### Qué consume tokens al startup

Antes de que el usuario escriba la primera línea, el context window ya tiene contenido:

| Fuente | Tokens aproximados |
|--------|-------------------|
| System prompt de Claude Code | ~2000-4000 |
| CLAUDE.md global (`~/.claude/`) | Variable (objetivo: <200 líneas → ~2000 tokens) |
| CLAUDE.md del proyecto | Variable |
| `.claude/rules/*.md` | Por cada archivo activo |
| Auto-memory (`MEMORY.md`) | Hasta 200 líneas (~3000 tokens) |
| Skill descriptions | ~1% del context window budget total |
| MCP tool schemas | Por cada servidor MCP activo |

Un proyecto con CLAUDE.md bien dimensionado usa ~8000-15000 tokens en startup. Uno mal configurado puede llegar a 30000+.

### Degradación de performance

Cuando el context window llega a ~70-80% de capacidad:
1. **Instrucciones del inicio se "olvidan"**: CLAUDE.md deja de respetarse
2. **Errores aumentan**: Claude pierde track de qué se hizo y qué falta
3. **Regresiones**: Claude rehace trabajo ya hecho
4. **Convenciones olvidadas**: los patrones de código definidos no se siguen

**Señal temprana**: Claude empieza a pedir confirmaciones que normalmente no pide, o hace cosas que explícitamente dijo que no haría.

### Herramientas de compaction y reset

#### `/compact` — compactar manteniendo relevante

```
/compact
```

Claude resume toda la conversación en un extracto denso y lo usa como base para continuar. Decide qué preservar basándose en recencia y relevancia percibida.

**Riesgo**: puede descartar información que parece vieja pero es importante (lista de archivos modificados, decisiones tomadas).

#### `/compact <instrucciones>` — compactar con guidance

```
/compact keep: list of all modified files, current task status, open issues found
/compact preserve: the schema decisions we made for the invoices table
/compact focus on: the auth bug we're debugging, discard the initial exploration
```

La forma correcta de usar compact en sesiones largas. Guiar qué preservar elimina la ambigüedad de qué es "importante".

**En CLAUDE.md** — compact customization persistente:
```markdown
## Compact Instructions
When compacting, always preserve:
- List of files modified in this session
- Current task and subtasks pending
- Decisions made about architecture/naming
- Bugs found but not yet fixed
```

#### `/clear` — reset completo

```
/clear
```

Borra todo el historial. El siguiente mensaje empieza en un context window vacío (solo system prompt + CLAUDE.md + memory).

**Cuándo usar**: entre tareas completamente distintas, cuando el contexto está corrupto por una sesión que fue mal, antes de empezar una tarea nueva importante.

**Costo**: perdes el historial de la sesión. No hay rollback. Para eso está `/rewind`.

#### `Esc+Esc` o `/rewind` — checkpoints

```
Esc+Esc
/rewind
```

Abre un menú de checkpoints. Claude Code crea checkpoints automáticamente antes de cada cambio significativo. Desde el menú se puede restaurar:
- Solo la conversación (sin deshacer cambios de código)
- Solo los cambios de código (sin revertir la conversación)
- Ambos (conversación + código al estado del checkpoint)

**Checkpoints persisten entre sesiones** — si cerrás Claude Code y volvés, los checkpoints siguen disponibles.

#### `/btw` — pregunta fuera del contexto

```
/btw ¿cuál es la diferencia entre Promise.all y Promise.allSettled?
/btw rápido: ¿cómo se hace un git cherry-pick?
```

Corre la pregunta en un overlay separado. La respuesta **no entra al historial** de la sesión principal. Para preguntas tangenciales que no tienen que ver con la tarea actual.

### `PreCompact` y `PostCompact` hooks

```json
{
  "hooks": [
    {
      "event": "PreCompact",
      "hook": {
        "type": "command",
        "command": "git diff --name-only HEAD > /tmp/modified-files-snapshot.txt && echo 'Snapshot guardado'"
      }
    },
    {
      "event": "PostCompact",
      "hook": {
        "type": "command",
        "command": "echo 'Contexto compactado. Archivos modificados:' && cat /tmp/modified-files-snapshot.txt"
      }
    }
  ]
}
```

`PreCompact`: guardar estado antes de compactar (archivos modificados, estado de tests, etc.)
`PostCompact`: re-inyectar contexto que sabes que compact no preserva

### Re-inyección post-compact con SessionStart

```json
{
  "hooks": [{
    "event": "SessionStart",
    "if": "compact",
    "hook": {
      "type": "command",
      "command": "echo '=== CONTEXTO POST-COMPACT ===' && cat .claude/context-snapshot.md"
    }
  }]
}
```

El matcher `"if": "compact"` hace que este hook solo corra cuando la sesión fue iniciada después de una compaction (no en cada SessionStart normal).

### Skill descriptions y context budget

Las descriptions de skills consumen del context window:
- Budget total para skill descriptions: ~1% del context window
- Fallback si se excede: 8000 caracteres total entre todas las descriptions
- Máximo recomendado por skill: 250 caracteres

Con muchos skills activos, las descriptions se truncan automáticamente. Por eso el límite de 250 chars es una restricción real, no solo una recomendación.

### Subagentes para preservar contexto principal

El patrón más efectivo para sesiones largas:

```
Tarea: "Entender el sistema de autenticación y agregar 2FA"

❌ Sin subagentes:
  → Claude lee 40 archivos en el contexto principal
  → Contexto lleno antes de empezar a implementar
  → Performance degrada mientras implementa

✅ Con subagente:
  → Subagente Explore lee los 40 archivos, produce resumen de 500 palabras
  → Contexto principal recibe solo el resumen
  → Contexto principal limpio para implementar con toda la capacidad disponible
```

### Status line — monitorear context usage

Se puede agregar a CLAUDE.md o configurar en el terminal para mostrar el porcentaje de uso del context window en tiempo real. Claude Code expone esta métrica en el status line cuando el REPL está activo.

### Overhead de MCP servers

Cada MCP server activo agrega sus tool schemas al context window en startup. Un server con 20 tools puede agregar 2000-5000 tokens. Mitigación:

```json
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_TOOLSETS": "repos,pull_requests"  // solo subset de tools
      }
    }
  }
}
```

Activar solo los toolsets necesarios reduce el overhead de schemas.

### Resumen de comandos de context management

| Comando | Efecto | Reversible |
|---------|--------|------------|
| `/compact` | Resume conversación, descarta detalle | No (solo via /rewind) |
| `/compact <instr>` | Resume con guidance sobre qué preservar | No |
| `/clear` | Borra todo el historial | No (solo via /rewind) |
| `/rewind` | Menú de checkpoints históricos | Si (elige el checkpoint) |
| `Esc+Esc` | Shorthand de /rewind | Si |
| `/btw <pregunta>` | Overlay separado, no entra al contexto | N/A (nunca entró) |
| Subagente | Exploración en contexto aislado | N/A (contexto aislado) |

## Conexiones

- Relacionado con: [[claude-code-best-practices]], [[claude-code-hooks]], [[claude-code-memory]]
- Parte de: [[claude-code-workflow-patterns]]
- Relacionado con conceptos de: [[context-engineering-patterns]] (degradation, compression)
- Ver también: [[claude-code-subagentes]] (preservar contexto principal), [[claude-code-skills]] (skill descriptions y budget), [[claude-code-mcp]] (overhead de MCP schemas)

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
