---
title: Claude Agent SDK — Sesiones
type: concept
tags: [claude, agent-sdk, sessions, continuidad, python]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Agent SDK — Sesiones

> Sistema de continuidad de contexto: continue, resume y fork de sesiones de agente.

## Contexto

Las sesiones permiten que un agente mantenga contexto a través de múltiples llamadas. Esencial para workflows de larga duración, tasks multietapa y flujos que deben poder pausar/continuar.

## Detalle

### Los tres modos de sesión

| Modo | Descripción | Caso de uso |
|------|-------------|-------------|
| `continue` | Misma sesión, mismo hilo | Conversación continua |
| `resume` | Retomar sesión pausada | Reanudar trabajo interrumpido |
| `fork` | Nueva rama desde sesión existente | Explorar alternativas sin contaminar el original |

### Continue — conversación continua

```python
client = anthropic.Anthropic()

# Primera llamada — crea la sesión
result1 = client.query(prompt="Analiza el archivo main.py")
session_id = result1.session_id  # guardar este ID

# Segunda llamada — continúa el contexto
result2 = client.query(
    prompt="Ahora refactoriza la función más larga que encontraste",
    session_id=session_id
)
# El agente recuerda lo que analizó en la llamada anterior
```

### Resume — reanudar sesión pausada

```python
# Útil cuando la sesión se cortó (timeout, error, interrupción)
result = client.query(
    prompt="Continúa con la tarea donde la dejaste",
    resume_session_id="session-abc123"
)
```

La diferencia con `continue` es que `resume` puede retomar sesiones que terminaron con `stop_reason != "end_turn"` (por ejemplo, interrumpidas por timeout o max_tokens).

### Fork — explorar alternativas

```python
# Sesión base con análisis realizado
base_session = "session-abc123"

# Fork A: implementar solución conservadora
fork_a = client.query(
    prompt="Implementa la solución conservadora que discutimos",
    resume_session_id=base_session,
    fork=True
)
fork_a_id = fork_a.session_id  # nueva sesión, no afecta base

# Fork B: implementar solución agresiva (en paralelo)
fork_b = client.query(
    prompt="Implementa la refactorización más agresiva",
    resume_session_id=base_session,
    fork=True
)
```

Después se puede comparar resultados de fork_a y fork_b sin haber modificado la sesión base.

### ClaudeSDKClient en Python

```python
from anthropic.sdk import ClaudeSDKClient

# Cliente de alto nivel con gestión de sesiones
client = ClaudeSDKClient(
    api_key="...",
    default_model="claude-opus-4-5",
    session_store="redis://localhost:6379"  # persistencia externa
)

# Sesión con nombre semántico
with client.session("refactor-auth-module") as session:
    result1 = await session.query("Revisa la lógica de auth")
    result2 = await session.query("Propón mejoras")
    result3 = await session.query("Implementa los cambios")
# La sesión persiste en Redis, recuperable después
```

### Capturar session_id

```python
# El session_id viene en la respuesta
result = client.query(prompt="...")

# Formas de extraerlo según el tipo de respuesta
session_id = result.session_id           # objeto Response
session_id = result["session_id"]        # dict
session_id = result.metadata.session_id  # streaming
```

### Sesiones cross-host

Con un store externo (Redis, base de datos), una sesión puede continuar en diferentes instancias del servicio:

```python
# Servidor A — inicia
session_id = start_analysis_task(file_path)
queue.publish("session_id", session_id)

# Servidor B — continúa (diferente proceso, diferente máquina)
session_id = queue.receive("session_id")
result = client.query(
    prompt="Termina el análisis e implementa los cambios",
    session_id=session_id
)
```

### Límites y consideraciones

- Las sesiones tienen un límite de tokens de contexto acumulado
- Para tasks muy largas usar `fork` para limpiar contexto sin perder estado
- Los session_ids son UUIDs opacos — almacenar en DB propia si se necesita buscar
- Resume funciona solo si la sesión fue guardada correctamente (no siempre garantizado en errores de red)

## Conexiones
- Relacionado con: [[agent-sdk-overview]], [[agent-sdk-subagentes]]
- Diferencia con subagentes: sesiones son el mismo agente a través del tiempo; subagentes son agentes paralelos/hijo
- Patrón relacionado: [[claude-code-workflow-patterns]]

## Fuentes
- Documentación oficial Claude Agent SDK — sección Sessions

---

## Timeline

- 2026-04-07: página creada desde docs oficiales del Agent SDK
