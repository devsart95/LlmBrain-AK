---
title: Ralph Wiggum Technique
type: concept
tags: [claude-code, autonomous, loop, workflow, agentic]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Ralph Wiggum Technique

> Patrón agentic de loop autónomo: Claude Code corre iterativamente contra una especificación hasta que la task está marcada como completada o se alcanzan los límites.

## Contexto

El nombre viene del personaje de Los Simpsons que sigue instrucciones literalmente hasta cumplirlas. Es el patrón emergente más discutido en la comunidad Claude Code en 2025-2026 para tasks autónomas de largo plazo. Múltiples implementaciones independientes convergieron en el mismo approach.

## Detalle

### El patrón fundamental

```
1. Escribir especificación en PROMPT.md (o similar)
2. Loop:
   a. Claude Code lee la spec
   b. Trabaja en implementarla (usa tools, edita archivos, corre tests)
   c. Evalúa si la task está completa
   d. Si completa: marca como done, sale
   e. Si no: ajusta, continúa al siguiente ciclo
3. Humano revisa el resultado
```

La clave: **el LLM decide cuándo terminó**, no el humano. El humano define la spec y el criterio de done.

### Implementaciones principales

#### ralph-orchestrator (mikeyobrien)

La implementación más citada en la documentación de Anthropic:

```bash
# Estructura básica
echo "Implementar autenticación JWT con refresh tokens" > PROMPT.md
echo "DONE: false" >> PROMPT.md

./ralph-orchestrator.sh PROMPT.md --max-iterations 20 --timeout 300
```

El orchestrator:
1. Lanza Claude Code con la spec
2. Detecta si Claude marcó `DONE: true` en el archivo
3. Si no: relanza con contexto del estado actual
4. Rate limiting y circuit breaker para evitar loops infinitos

#### ralph-wiggum-bdd (marcindulak)

Bash standalone que implementa BDD (Behavior-Driven Development) con el loop:

```bash
#!/bin/bash
# ralph-wiggum-bdd.sh
SPEC_FILE="$1"
MAX_ATTEMPTS="${2:-10}"

for i in $(seq 1 $MAX_ATTEMPTS); do
  echo "--- Iteración $i ---"

  # Claude Code trabaja en la spec
  claude --print "Lee $SPEC_FILE y avanza hacia el objetivo. Si completaste todo, escribe DONE en el archivo."

  # Verificar si terminó
  if grep -q "DONE" "$SPEC_FILE"; then
    echo "Completado en $i iteraciones"
    exit 0
  fi
done

echo "Límite alcanzado sin completar"
exit 1
```

Soporta modo interactivo y modo unattended. El autor nota que en práctica necesita supervisión humana.

#### Ralph Playbook (Clayton Farr)

El recurso más completo para entender la teoría detrás:

**Principios:**
- La spec debe ser **observable**: Claude puede verificar si cumplió cada criterio
- Los criterios de done deben ser **binarios**: pasa o no pasa (tests, linting, tipos)
- El loop necesita **circuit breakers**: máximo de iteraciones, timeout, detección de ciclos
- Incluir en la spec: contexto, herramientas disponibles, criterio de done explícito

**Anatomía de una buena spec para Ralph:**

```markdown
# Task: Migrar autenticación a Better Auth

## Contexto
- Stack: Next.js 15, Prisma, PostgreSQL
- Auth actual: JWT casero en /lib/auth.ts
- Target: Better Auth con sessions en DB

## Herramientas disponibles
- bash, text_editor, filesystem
- npm install para nuevas deps

## Criterio de done (TODOS deben cumplirse)
- [ ] `npm run typecheck` pasa sin errores
- [ ] `npm test` pasa todos los tests de auth
- [ ] Ningún import de /lib/auth.ts en el codebase
- [ ] .env.example actualizado con nuevas variables

## DONE: false
```

#### Auto-Claude (AndyMik90)

Implementación más sofisticada con UI kanban:

```
┌─────────────────────────────────────┐
│  Auto-Claude — Task Board           │
├──────────┬──────────┬───────────────┤
│ Backlog  │ In Prog  │  Done         │
├──────────┼──────────┼───────────────┤
│ Task C   │ Task B   │  Task A ✓     │
│ Task D   │ (iter 3) │               │
└──────────┴──────────┴───────────────┘
```

Integra el loop con el full SDLC: planifica → implementa → valida → repite.

### Guardrails — lo que no puede faltar

Sin guardrails, Ralph puede:
- Loop infinito (gastar créditos sin terminar)
- Hacer cambios destructivos sin parar
- Romper algo arreglando otra cosa

**Guardrails mínimos:**

```bash
# 1. Máximo de iteraciones
MAX_ITER=15

# 2. Timeout por iteración
ITER_TIMEOUT=180s

# 3. Circuit breaker: si los últimos N outputs son iguales, parar
check_cycle() {
  # Comparar hash de los últimos 3 estados
  local hash1=$(md5 state_n-1.txt)
  local hash2=$(md5 state_n-2.txt)
  if [ "$hash1" = "$hash2" ]; then
    echo "CICLO DETECTADO — abortando"
    exit 2
  fi
}

# 4. Preservar trabajo: commit en cada iteración exitosa
git add -A && git commit -m "ralph: iteración $i"

# 5. Rate limiting: pausa entre iteraciones
sleep 10
```

### Casos de uso óptimos

**Funciona bien:**
- Refactorizaciones con criterio de done medible (tests pasan)
- Migraciones con checklist explícito
- Tareas con feedback loop automático (linting, typecheck, tests)
- Implementación de specs bien definidas

**No funciona bien:**
- Tasks ambiguas sin criterio binario de done
- Work que requiere decisiones de diseño en el camino
- Dependencias externas (APIs que pueden flaquear)
- Tareas que requieren juicio humano en puntos intermedios

### Variante: Ralph para marketing (ralph-wiggum-marketer)

Aplica el mismo patrón a copywriting:
1. Agentes de investigación recopilan datos del mercado
2. Ralph escribe copy iterativamente
3. Criterio de done: pasa checklist de brand guidelines

Muestra que el patrón es agnóstico del dominio — funciona en cualquier tarea con spec observable.

## Conexiones
- Relacionado con: [[claude-code-workflow-patterns]], [[claude-code-agent-teams]], [[claude-code-subagentes]]
- Implementado en: [[claude-code-orquestadores]]
- Requiere buenas specs: similar a [[context-engineering-patterns]]
- Usado con: [[claude-code-hooks]] para safety guardrails

## Fuentes
- `https://github.com/hesreallyhim/awesome-claude-code` — sección Ralph Wiggum

---

## Timeline

- 2026-04-07: página creada desde awesome-claude-code
