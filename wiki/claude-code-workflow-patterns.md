---
title: Claude Code — Patrones de Workflow
type: concept
tags: [claude-code, workflow, patrones, productividad, automatizacion]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Patrones de Workflow

> Patrones probados para organizar el trabajo con Claude Code: desde el ciclo base de desarrollo hasta automatización masiva y sesiones paralelas.

---

## Contexto

Claude Code no es un chat con acceso a archivos — es un sistema orquestable con modos distintos para distintas fases del trabajo. El workflow que usás determina la calidad del output más que cualquier otra variable. Un prompt perfecto en el workflow equivocado produce resultados mediocres.

## Detalle

### El ciclo base: Explore → Plan → Implement → Commit

**Explore** — entender antes de tocar:
```
Ctrl+Shift+P  o  Shift+Tab  — activar Plan Mode
```
En Plan Mode, Claude lee archivos y puede hacer preguntas, pero no puede modificar nada. Es el modo de reconocimiento. Úsalo siempre antes de implementar en código desconocido.

**Plan** — definir el camino:
Una vez que Claude tiene contexto, propone un plan detallado. Antes de aprobarlo:
```
Ctrl+G — abrir el plan en editor de texto
```
Editar el plan: agregar constraints, cambiar el approach, eliminar pasos. El plan es un contrato — Claude lo va a seguir.

**Implement** — ejecutar el plan:
Claude ejecuta paso a paso. `Esc` interrumpe en cualquier momento. Si algo va mal, `/rewind` vuelve al estado pre-implementación.

**Commit** — persistir el progreso:
Siempre commit al terminar un bloque lógico. Los commits son checkpoints del código; `/rewind` son checkpoints de la conversación. Ambos son necesarios.

### Plan Mode en detalle

```
Ctrl+Shift+P  — toggle Plan Mode
Shift+Tab     — ciclar entre modos
```

Mientras está activo, Claude puede:
- Leer archivos (Read, Glob, Grep)
- Hacer preguntas de clarificación
- Proponer planes
- Estimar complejidad y riesgos

Claude NO puede:
- Editar o crear archivos (Write, Edit bloqueados)
- Ejecutar comandos Bash
- Invocar subagentes que modifiquen

**Cuándo usar Plan Mode:**
- Primera vez que trabajás en un módulo desconocido
- Antes de refactorings grandes
- Cuando el feature spec es ambiguo y necesitás explorar opciones
- Para estimar effort antes de comprometerte

### Non-interactive mode

Para scripts, CI/CD, automatización:

```bash
# Ejecución simple
claude -p "auditar el directorio src/ buscando N+1 queries"

# Con output estructurado
claude -p "analizar src/auth.ts" --output-format json

# Output streaming para procesamiento en tiempo real
claude -p "describir la arquitectura" --output-format stream-json

# Con tools específicos
claude -p "buscar todos los TODO en el código" \
  --allowedTools "Grep,Glob,Read" \
  --output-format json
```

Output formats:
- `text` — texto plano (default)
- `json` — JSON con metadata (tokens, model, etc.)
- `stream-json` — chunks JSON en streaming, útil para procesamiento incremental

### Fan-out pattern — migraciones masivas

```bash
#!/bin/bash
# migrate-to-typescript.sh
# Migrar todos los .js a .ts en paralelo

CONCURRENCY=5
FILES=$(find src/ -name "*.js" -not -path "*/node_modules/*")

echo "$FILES" | xargs -P $CONCURRENCY -I{} bash -c '
  FILE="{}"
  OUTPUT="${FILE%.js}.ts"
  claude -p "
    Migrar $FILE a TypeScript estricto.
    - No usar '\''any'\''
    - Inferir tipos desde el uso
    - Preservar lógica exactamente
    Guardar como $OUTPUT
  " --allowedTools "Read,Write,Edit" 2>&1 | tail -1
  echo "Migrado: $FILE → $OUTPUT"
'
```

Cada instancia de `claude -p` tiene su propio contexto aislado. No comparten estado. Ideal para transformaciones file-by-file sin dependencias cruzadas.

### Writer/Reviewer pattern

```bash
# Sesión 1: implementa (con contexto de la tarea)
claude

# Sesión 2: revisar con ojos frescos (SIN contexto de implementación)
# No usar --continue ni --resume de la sesión anterior
claude -p "Hacer code review de los cambios en src/auth/. Checklist: seguridad, tests, edge cases, naming" \
  --allowedTools "Read,Grep,Glob"
```

La separación de contexto es el punto: el reviewer no tiene anclaje cognitivo al proceso de escritura. Ve el código como lo vería un reviewer humano que llega frío.

### Git worktrees para sesiones paralelas

```bash
# Crear worktrees para dos features en paralelo
git worktree add ../proyecto-feature-a feature-a
git worktree add ../proyecto-feature-b feature-b

# Sesión 1: feature A
cd ../proyecto-feature-a && claude

# Sesión 2: feature B (terminal separada)
cd ../proyecto-feature-b && claude

# Cada sesión tiene su propio CLAUDE.md context y filesystem state
```

Permite trabajar en dos features simultáneas sin conflictos de filesystem. Claude Code por sesión no interfiere con la otra.

### Session management

```bash
# Continuar sesión más reciente
claude --continue

# Elegir sesión de una lista
claude --resume
```

Dentro del REPL:
```
/rename feature-oauth-migration-2026-04-07
```

Convención recomendada para nombres: `<tipo>-<descripcion>-<fecha>`. Permite encontrar sesiones específicas fácilmente en `--resume`.

### `/batch` skill — orquestación automática

El skill built-in `/batch` automatiza el fan-out pattern con worktrees:

```
/batch migrate all .js files in src/services/ to TypeScript
/batch add JSDoc to all exported functions in src/
/batch add tests for all services in src/services/
```

`/batch` analiza el scope, crea los worktrees, lanza subagentes en paralelo, y mergea los resultados. Más seguro que el loop manual porque maneja errores y conflictos.

### AskUserQuestion tool — interview mode

```
"Voy a implementar un sistema de notificaciones. Antes de empezar, haceme todas las preguntas que necesitás para entender exactamente qué se necesita."
```

Claude usa `AskUserQuestion` para recopilar specs de forma estructurada:
- Tipo de notificaciones (email, push, in-app)
- Prioridades (qué se muestra primero)
- Persistencia (dónde se guardan)
- Read/unread state
- Expiración

El output de la entrevista se convierte en specs que Claude usa para implementar. Más efectivo que un brief inicial porque Claude sabe qué preguntar para este dominio.

### Keybindings del workflow

| Keybinding | Acción |
|-----------|--------|
| `Ctrl+Shift+P` o `Shift+Tab` | Toggle Plan Mode |
| `Ctrl+G` | Editar plan en editor externo |
| `Ctrl+O` | Toggle verbose mode (ver qué tools se ejecutan) |
| `Ctrl+T` | Ver task list (agent teams) |
| `Shift+Down` | Ciclar entre teammates (agent teams) |
| `Esc` | Interrumpir operación en curso |
| `Esc+Esc` | Menú de checkpoints (rewind) |

### Verificación como parte del workflow

```bash
# El workflow NO termina en "Claude dice que está listo"
# Termina en "el artefacto de verificación pasó"

# 1. Implementar
claude -p "implementar endpoint POST /api/invoices"

# 2. Verificar
curl -X POST http://localhost:3000/api/invoices \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000, "currency": "PYG"}' | jq .id

npm test -- --testPathPattern=invoices
```

Definir el criterio de éxito **antes** de implementar. Claude optimiza hacia lo que se puede medir.

### Sesión como branch de trabajo

Cada sesión de Claude Code es análoga a una branch de git:
- Tiene su propio estado de conversación
- Se puede pausar y retomar
- Se puede nombrar descriptivamente
- Se puede "mergear" (tomar decisiones de múltiples sesiones)

Workflow multi-sesión para una feature compleja:
```
sesión "feature-auth-research":   exploración de opciones
sesión "feature-auth-design":     plan arquitectural (sin implementación)
sesión "feature-auth-impl":       implementación
sesión "feature-auth-review":     code review + fixes
```

Cada sesión tiene foco claro y contexto limpio para ese foco.

## Conexiones

- Relacionado con: [[claude-code-best-practices]], [[claude-code-context-window]], [[claude-code-subagentes]]
- Parte de: [[claude-code-agent-teams]], [[claude-code-skills]]
- Conecta con: [[ai-development-workflows]] (SDD, TDD, ciclos de desarrollo)
- Ver también: [[claude-code-cli-referencia]] (flags de non-interactive), [[generation-verification-loop]], [[boil-the-lake]]

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
