---
title: Claude Code — Orquestadores
type: overview
tags: [claude-code, orquestadores, multi-agent, automatización]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Orquestadores

> Herramientas que coordinan múltiples instancias de Claude Code o implementan loops autónomos de ejecución.

## Contexto

Los orquestadores resuelven el problema de tasks que superan el context window o requieren paralelismo. Van desde scripts bash simples hasta frameworks completos con UI, task queues y multi-agent coordination.

## Detalle

### Taxonomía de orquestadores

```
Complejidad
    ▲
    │  Ruflo          ← swarms, vector memory, self-learning
    │  Auto-Claude    ← UI kanban, SDLC completo
    │  Claude Swarm   ← swarm de agents conectados
    │  Claude Squad   ← múltiples instances con workspaces
    │  Claude Flow    ← recursive cycles
    │  TSK            ← Docker sandboxes, branches
    │  Ralph          ← loop bash hasta done
    ▼
```

---

### Ralph Wiggum Loop

Ver [[ralph-wiggum-technique]] para la descripción completa.

El patrón base sobre el que muchos orquestadores están construidos.

---

### Claude Squad (smtg-ai)

Terminal app para múltiples agentes en workspaces paralelos:

```
claude-squad
├── session-1 (feature/auth)     → WORKING
├── session-2 (bugfix/login)     → DONE
└── session-3 (refactor/api)     → WAITING INPUT
```

- Soporta Claude Code, Codex, Aider
- Cada session tiene su propio directorio de trabajo
- Switching rápido entre sessions
- Para workflows donde se quieren explorar múltiples approaches en paralelo

---

### Claude Swarm (parruda)

Conecta una sesión de Claude Code con un swarm de agentes:

```bash
claude-swarm start --config swarm.yml

# swarm.yml
agents:
  - name: architect
    model: claude-opus-4-5
    role: "Diseña la solución"
  - name: implementer
    model: claude-sonnet-4-5
    role: "Implementa código"
    tools: [bash, text_editor]
  - name: tester
    model: claude-sonnet-4-5
    role: "Escribe y corre tests"
    tools: [bash]
```

Los agentes se comunican entre sí. La sesión principal actúa como entrada/salida al swarm.

---

### Auto-Claude (AndyMik90)

Framework multi-agente que integra el SDLC completo:

**Features:**
- UI kanban-style para visualizar el pipeline
- Basado en el Claude Agent SDK
- Planifica → Implementa → Valida en ciclos
- Strict protocols para prevenir que el AI "se vaya por las ramas"
- Task queue con prioridades

**Arquitectura interna:**
```
Task Queue
    ↓
Planner Agent (crea subtasks)
    ↓
Implementer Agent (ejecuta subtasks en worktrees)
    ↓
Validator Agent (verifica criterios de done)
    ↓
Reporter Agent (actualiza kanban + notifica)
```

---

### Claude Code Flow (ruvnet)

Layer de orquestación code-first:
- Claude escribe, edita, testea y optimiza código autónomamente
- Ciclos recursivos de agentes
- Cada ciclo evalúa el progreso y ajusta la estrategia
- Orientado a proyectos de largo plazo

---

### TSK — AI Agent Task Manager (dtormoen)

CLI en Rust con sandboxes Docker:

```bash
tsk run "Implementa el módulo de pagos según la spec en docs/payments.md"

# TSK:
# 1. Crea contenedor Docker con el repo
# 2. Lanza Claude Code dentro del contenedor
# 3. Claude trabaja de forma aislada
# 4. Retorna git branch con los cambios
# 5. Humano hace review y merge
```

**Ventajas del approach Docker:**
- Aislamiento real: si algo sale mal, no afecta el repo principal
- Múltiples agents en paralelo con contenedores separados
- El resultado es siempre una branch limpia para review

---

### Claude Task Master (eyaltoledano)

Sistema de task management para development con AI:
- Diseñado para integrarse con Cursor AI
- Mantiene un task board persistente
- Agents pueden leer y actualizar el estado de tasks
- Compatible con Claude Code y Cursor

---

### Ruflo (ruvnet)

El más ambicioso del ecosistema:

**Features:**
- Multi-agent swarms auto-coordinados
- Vector-based memory en múltiples capas
- Self-learning: aprende de errores anteriores
- Systematic planning con subobjetivos
- Security guardrails integrados
- Autonomous coordination sin human-in-the-loop

```
┌─────────────────────────────────────────┐
│               Ruflo                     │
│                                         │
│  Memory Layer          Agent Swarm      │
│  ├── episodic         ├── planner      │
│  ├── semantic         ├── executor     │
│  └── procedural       ├── reviewer     │
│                       └── learner      │
│                                         │
│  Security Layer                         │
│  ├── guardrails                        │
│  ├── rate limiting                     │
│  └── audit log                         │
└─────────────────────────────────────────┘
```

El autor advierte: YMMV en producción, pero el código enseña patrones valiosos.

---

### Claude Task Runner (grahama1970)

Especializado en **context isolation**:
- Cada task corre en contexto limpio
- Resuelve el problema de context bleed entre tasks relacionadas
- Multi-step projects con memoria selectiva

---

### Sudocode (sudocode-ai)

Orquestación ligera que vive en el repo:

```
repo/
└── .sudocode/
    ├── tasks/
    │   ├── task-001.md
    │   └── task-002.md
    └── config.yml
```

Integra con specification frameworks. "It's giving Jira" — el autor del awesome-list.

---

### Simone (Helmi)

Project management workflow completo:
- No solo commands — un sistema de documentos y procesos
- Guidelines para planning y ejecución
- Facilita proyectos de largo plazo con Claude Code
- Orientado a equipos pequeños

---

### Cuándo usar cada uno

| Si necesitás... | Usar |
|-----------------|------|
| Loop autónomo simple con criterio de done | [[ralph-wiggum-technique]] |
| Múltiples tasks en paralelo con aislamiento | Claude Squad o TSK |
| Swarm de agents especializados | Claude Swarm |
| SDLC completo con UI | Auto-Claude |
| Aislamiento real con Docker | TSK o viwo-cli |
| Task management persistente | Sudocode o Simone |
| Máxima autonomía con auto-learning | Ruflo (experimental) |

## Conexiones
- Relacionado con: [[ralph-wiggum-technique]], [[claude-code-tooling-ecosystem]]
- Base teórica: [[claude-code-subagentes]], [[claude-code-agent-teams]]
- Patterns de orquestación: [[ai-development-workflows]]

## Fuentes
- `https://github.com/hesreallyhim/awesome-claude-code` — sección Orchestrators

---

## Timeline

- 2026-04-07: página creada desde awesome-claude-code
