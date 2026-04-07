---
title: Claude Code — Best Practices
type: concept
tags: [claude-code, best-practices, workflow, productividad]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Best Practices

> Patrones validados para maximizar calidad y velocidad con Claude Code, organizados alrededor de la constraint fundamental: el context window se llena y el rendimiento degrada.

---

## Contexto

La mayoría de los problemas con Claude Code vienen del mismo lugar: context window lleno, instrucciones olvidadas, sesiones mezcladas. Las best practices son básicamente estrategias para combatir esa constraint y asegurar que Claude siempre tenga el contexto correcto para la tarea correcta.

## Detalle

### La constraint fundamental

El context window no es infinito. Cuando se llena:
- Claude "olvida" instrucciones del inicio de la sesión
- Los errores aumentan
- Las instrucciones de CLAUDE.md dejan de respetarse
- El output degrada antes de que el usuario lo note

**Señal**: si Claude empieza a ignorar convenciones que definiste al principio de la sesión, el context está demasiado lleno.

### El principio de más alto leverage

> "Give Claude a way to verify its work"

Tests, screenshots, scripts de validación, expected outputs. Esto transforma a Claude de "el que genera" a "el que genera y verifica". Sin verificación, Claude puede quedar atrapado en bucles de corrección.

Formas de verificación:
- Tests automatizados: `npm test -- --watch`
- Scripts bash: `curl http://localhost:3000/health && echo OK`
- Screenshots: Chrome DevTools MCP para UI
- Expected outputs: "el resultado debe ser exactamente este JSON"

### Workflow base: Explore → Plan → Implement → Commit

**1. Explore (Plan Mode)**
```
Ctrl+Shift+P o Shift+Tab — activar Plan Mode
```
Claude solo lee archivos, no modifica nada. Úsalo para entender el codebase antes de cambiar.

**2. Plan**
Claude propone el plan de implementación. Revisarlo antes de ejecutar:
```
Ctrl+G — abrir el plan en editor de texto para editar
```
Editar el plan, agregar restricciones, eliminar pasos innecesarios. Commit el plan antes de implementar.

**3. Implement**
Con el plan aprobado, Claude ejecuta. Si algo va mal, `Esc` interrumpe.

**4. Commit**
Siempre commit al terminar un bloque de trabajo. Checkpoint claro para `/rewind` si algo sale mal después.

### Context management

| Comando/Acción | Cuándo usar |
|----------------|-------------|
| `/clear` | Entre tareas no relacionadas |
| `/compact <instrucciones>` | Cuando el contexto está lleno pero hay que seguir |
| `Esc+Esc` o `/rewind` | Checkpoints — restaurar conversación/código/ambos |
| `/btw` | Pregunta rápida que no debe entrar al contexto |
| Subagente para exploración | Investigar sin contaminar el contexto principal |

**`/compact` con instrucciones:**
```
/compact keep: list of modified files, current task, open bugs found
```
Guía qué preservar cuando Claude compacta. Sin instrucciones, Claude decide — y puede descartar cosas importantes.

**`/btw` — pregunta tangencial:**
```
/btw ¿cuál es la diferencia entre useCallback y useMemo?
```
Corre en un overlay separado. La respuesta no entra al historial de la sesión principal.

### Prompts específicos — tabla Before/After

| Vago (ineficaz) | Específico (efectivo) |
|----------------|----------------------|
| "Fix the bug" | "Fix the login bug in `src/auth/login.ts:45` where JWT expires silently. Expected: error 401 with message" |
| "Add tests" | "Add tests for `UserService.create()` in `tests/services/user.test.ts`. Use existing fixture from `tests/fixtures/user.ts`" |
| "Refactor this" | "Refactor `HotDogWidget` pattern to `src/components/PizzaWidget.tsx` following the same props interface and loading states" |
| "Make it faster" | "Fix N+1 query in `GET /api/users` — use `include: { posts: true }` in the Prisma query at `src/routes/users.ts:23`" |

**Patrones de prompt efectivos:**

1. **Scope task**: archivo + escenario + preferencias de testing
2. **Point to sources**: git history, archivos específicos, ejemplos existentes
3. **Reference existing patterns**: "seguir el patrón de HotDogWidget"
4. **Describe symptom, not solution**: ubicación del archivo + qué es "fixed" (no el cómo)

### Referenciar archivos y datos

```bash
# En el REPL — referenciar archivo específico
@src/services/auth.ts

# Pegar imagen (drag & drop o clipboard)
# Claude puede leer screenshots, wireframes, error screenshots

# Pipe data desde CLI
cat logs/error.log | claude "¿qué está causando este error?"
git diff main...HEAD | claude "resume los cambios de este PR"
```

### CLAUDE.md efectivo

```
/init  — genera CLAUDE.md desde el codebase existente (punto de partida)
```

Después de `/init`, podar agresivamente. Objetivo: menos de 200 líneas.

Señal de CLAUDE.md sobredimensionado: Claude empieza a ignorar las instrucciones → el archivo es demasiado largo para que las instrucciones finales queden en contexto.

Convertir reglas muy específicas a hooks (se ejecutan automáticamente sin consumir contexto).

### Failure patterns y soluciones

| Pattern | Síntoma | Solución |
|---------|---------|----------|
| Kitchen sink session | Claude olvidó instrucciones del inicio | `/clear` entre tareas distintas |
| Correcting over and over | Claude sigue cometiendo el mismo error | `/clear` + reformular el prompt desde cero |
| Over-specified CLAUDE.md | Claude ignora partes del CLAUDE.md | Podar a <200 líneas, convertir reglas a hooks |
| Trust-then-verify gap | Claude implementó pero nadie verificó | Siempre proveer mecanismo de verificación |
| Infinite exploration | Claude lee files indefinidamente sin implementar | Scopear con subagente para exploración, límite explícito de archivos |
| Context pollution | Investigar un bug arruinó el contexto para implementar | Usar subagente para investigación |

### Non-interactive mode

```bash
# Para CI/scripts/automatización
claude -p "correr audit de seguridad en src/" --output-format json

# Con tools específicos
claude -p "buscar N+1 queries" --allowedTools "Grep,Glob,Read"

# Pipe desde stdin
echo "SELECT * FROM users LIMIT 10" | claude -p "explain this query"
```

### Fan-out pattern — migraciones masivas

```bash
#!/bin/bash
# Migrar 50 archivos en paralelo
find src/ -name "*.js" | while read file; do
  claude -p "Migrar $file a TypeScript estricto. No usar 'any'. Guardar como ${file%.js}.ts" &
done
wait
echo "Migración completada"
```

Claude instancias en paralelo, cada una con su propio contexto aislado. Más rápido que hacerlo secuencialmente en una sesión.

### AskUserQuestion tool — feature entrevistas

Para features grandes y ambiguas, dejar que Claude te entreviste:

```
"Necesito implementar un sistema de facturación. Antes de empezar, hazme las preguntas necesarias para entender exactamente lo que se necesita."
```

Claude usa `AskUserQuestion` para recopilar specs de manera estructurada. El resultado es mucho más preciso que un brief inicial vago.

### Session management

```bash
# Continuar sesión más reciente
claude --continue

# Elegir sesión específica
claude --resume

# Nombrar la sesión para encontrarla fácilmente
/rename oauth-migration-2026-04-07
```

Cada sesión es como una branch: diferentes workstreams, contextos persistentes. Nombrar sessions descriptivamente permite retomar trabajo exactamente donde quedó.

### `CLAUDE_CODE_NEW_INIT=1` — init interactivo

```bash
CLAUDE_CODE_NEW_INIT=1 claude
```

Claude te entrevista sobre el proyecto antes de generar el CLAUDE.md. Resultado más preciso que el auto-generado.

### Verificación como success criteria explícito

```
"Implementá el endpoint POST /api/invoices.
SUCCESS cuando: `curl -X POST http://localhost:3000/api/invoices -d '{...}' | jq .id` retorna un UUID válido y `npm test` pasa sin errores."
```

Claude optimiza hacia el success criteria dado. Con criterio explícito, los bucles de corrección son más cortos.

## Conexiones

- Relacionado con: [[claude-code-workflow-patterns]], [[claude-code-memory]], [[claude-code-context-window]]
- Parte de: [[claude-code-subagentes]], [[claude-code-agent-teams]]
- Conecta con filosofía: [[generation-verification-loop]], [[boil-the-lake]], [[search-before-building]]
- Ver también: [[claude-code-cli-referencia]] (flags de non-interactive mode), [[ai-development-workflows]]

## Fuentes

- Claude Code Docs — https://code.claude.com/docs

---

## Timeline

- 2026-04-07: creación inicial desde docs oficiales Claude Code
