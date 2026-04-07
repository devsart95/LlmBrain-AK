---
title: Claude Agent SDK — Subagentes
type: concept
tags: [claude, agent-sdk, subagentes, parallelism, python]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Agent SDK — Subagentes

> Capacidad de un agente para lanzar agentes hijo independientes, paralelos o con aislamiento de entorno.

## Contexto

Los subagentes del SDK permiten construir sistemas multi-agente donde un agente orquestador delega trabajo a agentes especializados. Diferente a las sesiones (continuidad temporal), los subagentes son paralelos o jerarquicos.

## Detalle

### Concepto fundamental

```
Agente Principal (Orquestador)
├── Subagente A: analiza módulo auth
├── Subagente B: analiza módulo payments
└── Subagente C: analiza módulo API
    └── Sub-subagente: analiza endpoint específico
```

Cada subagente tiene su propio contexto, tools y ciclo de vida.

### Lanzar subagentes desde Python

```python
import asyncio
from anthropic.sdk import ClaudeSDKClient

client = ClaudeSDKClient()

async def run_parallel_analysis(files: list[str]):
    # Lanzar subagentes en paralelo
    tasks = [
        client.query_async(
            prompt=f"Analiza {file} y reporta problemas de seguridad",
            tools=["text_editor", "bash"],
            model="claude-sonnet-4-5"  # modelo más rápido para subtasks
        )
        for file in files
    ]

    results = await asyncio.gather(*tasks)

    # Sintetizar resultados en el agente principal
    synthesis = await client.query_async(
        prompt=f"Aquí los reportes de {len(files)} archivos: {results}. Prioriza los hallazgos."
    )
    return synthesis
```

### Aislamiento con worktree

Para subagentes que modifican archivos, `isolation: "worktree"` crea una copia git aislada:

```python
result = client.query(
    prompt="Implementa la nueva feature en este worktree",
    subagent_config={
        "isolation": "worktree",  # copia temporal del repo
        "branch": "feature/nuevo-modulo",
        "auto_cleanup": True  # eliminar si no hay cambios
    }
)

# El subagente trabaja en su propia copia
# Si hace cambios, se retorna el path del worktree y la rama
worktree_path = result.worktree_path
branch = result.branch
```

### Hooks en subagentes

```python
def on_subagent_start(event):
    print(f"Subagente iniciado: {event.subagent_id}")
    print(f"Task: {event.prompt[:100]}")
    print(f"Modelo: {event.model}")

def on_subagent_stop(event):
    print(f"Subagente {event.subagent_id} terminó")
    print(f"Éxito: {event.success}")
    print(f"Resultado: {event.result[:200]}")

client.query(
    prompt="Orquesta el análisis completo del repo",
    hooks={
        "subagentStart": on_subagent_start,
        "subagentStop": on_subagent_stop,
    }
)
```

### Agent Teams (experimental)

Para equipos de agentes que se comunican entre sí:

```python
from anthropic.sdk.teams import AgentTeam

team = AgentTeam(
    agents={
        "architect": AgentConfig(
            model="claude-opus-4-5",
            system="Eres el arquitecto. Diseñas la solución.",
            tools=["text_editor"]
        ),
        "implementer": AgentConfig(
            model="claude-sonnet-4-5",
            system="Eres el implementador. Escribes código.",
            tools=["bash", "text_editor"]
        ),
        "reviewer": AgentConfig(
            model="claude-sonnet-4-5",
            system="Eres el reviewer. Verificas calidad.",
            tools=["bash", "text_editor"]
        )
    },
    shared_task_list=True,  # todos ven el mismo task list
    mailbox=True            # pueden enviarse mensajes
)

result = team.run("Construye el módulo de autenticación")
```

Ver [[claude-code-agent-teams]] para el estado actual de esta feature.

### Diferencias clave: Subagente vs Sesión

| | Subagente | Sesión |
|--|-----------|--------|
| **Relación** | Padre-hijo / paralelo | Misma entidad en el tiempo |
| **Contexto** | Separado, independiente | Acumulativo |
| **Paralelismo** | Sí, nativamente | No (secuencial) |
| **Caso de uso** | Dividir trabajo | Conversación larga |
| **Aislamiento** | Opcional (worktree) | Compartido |

### Patterns recomendados

**Map-Reduce:**
```python
# Map: subagentes paralelos
chunk_results = await asyncio.gather(*[
    client.query_async(prompt=f"Procesa chunk {i}", ...)
    for i in chunks
])

# Reduce: agente principal sintetiza
final = await client.query_async(
    prompt=f"Sintetiza estos {len(chunk_results)} resultados: ..."
)
```

**Especialización:**
```python
# Agente especialista para cada dominio
security_agent = client.query(
    prompt=task,
    system="Eres experto en seguridad. Solo reportas vulnerabilidades.",
    model="claude-opus-4-5"
)
perf_agent = client.query(
    prompt=task,
    system="Eres experto en performance. Solo reportas bottlenecks.",
    model="claude-sonnet-4-5"
)
```

## Conexiones
- Relacionado con: [[agent-sdk-overview]], [[agent-sdk-sessions]], [[claude-code-subagentes]], [[claude-code-agent-teams]]
- Pattern similar en: [[claude-code-workflow-patterns]]
- Contrasta con: [[agent-sdk-sessions]] (tiempo vs espacio)

## Fuentes
- Documentación oficial Claude Agent SDK — sección Subagentes y Agent Teams

---

## Timeline

- 2026-04-07: página creada desde docs oficiales del Agent SDK
