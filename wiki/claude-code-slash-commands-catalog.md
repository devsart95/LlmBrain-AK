---
title: Claude Code — Slash Commands Catalog
type: overview
tags: [claude-code, slash-commands, workflows, git, testing]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Slash Commands Catalog

> Catálogo de slash commands notables de la comunidad Claude Code, organizados por categoría de uso.

## Contexto

Los slash commands son prompts refinados que controlan el comportamiento de Claude en una tarea específica. La comunidad ha convergido en patterns estables para las tareas más comunes del SDLC.

## Detalle

### Version Control & Git

#### `/commit` (evmts/tevm-monorepo)
Crea commits en conventional commit format con emojis apropiados:
- Analiza los cambios staged
- Selecciona el tipo correcto (feat/fix/refactor/docs/...)
- Genera mensaje descriptivo que explica el *por qué*
- Sigue los estándares del proyecto

#### `/commit-fast` (steadycursor)
Versión rápida de `/commit`:
- Usa el primer mensaje sugerido sin confirmación manual
- Skipa el footer de Co-Authorship
- Para workflows donde cada segundo cuenta

#### `/create-pr` (toyamarinyon/giselle)
Workflow completo de PR:
1. Crea branch nueva
2. Commitea cambios
3. Formatea con Biome
4. Abre el PR con descripción estructurada

#### `/create-pull-request` (liam-hq)
Versión con enforcement de convenciones:
- Valida el título del PR contra conventions del proyecto
- Llena el template del PR
- Ejemplos concretos de comandos gh
- Best practices inline

#### `/fix-pr` (metabase)
**Muy útil** — fetcha comentarios sin resolver de un PR y los arregla:
```
/fix-pr 1234
→ Descarga todos los review comments del PR
→ Lee cada thread sin resolver
→ Implementa los cambios sugeridos
→ Comitea con referencia al comentario
```

#### `/fix-github-issue` (jeremymailen)
Resolución completa de issues:
1. Descarga detalles del issue via `gh`
2. Analiza el contexto y reproduce el problema
3. Implementa la solución
4. Corre tests
5. Commitea con `Closes #N` en el mensaje

#### `/create-worktrees` (evmts)
Crea git worktrees para todos los PRs abiertos o branches específicas:
- Maneja branches con slashes en el nombre
- Limpia worktrees obsoletos automáticamente
- Permite trabajar en múltiples PRs simultáneamente sin stash

---

### Code Analysis & Testing

#### `/tdd` (zscott/pane)
Guía el desarrollo con TDD estricto:
- Enforcea Red → Green → Refactor
- Integración con git workflow
- Crea el PR al finalizar

#### `/tdd-implement` (jerseycheese)
Para implementar una feature específica via TDD:
1. Analiza los requirements de la feature
2. Escribe tests primero (RED)
3. Implementa el mínimo código que pasa (GREEN)
4. Refactoriza sin romper tests

#### `/check` (rygwdn)
Auditoría comprehensive de código:
- Static analysis integration
- Security vulnerability scanning
- Code style enforcement
- Reporte detallado con prioridades

#### `/code_analysis` (kingler)
Menú de comandos de análisis avanzado:
- Knowledge graph generation del codebase
- Optimization suggestions con datos
- Quality evaluation con métricas

#### `/repro-issue` (rzykov)
Crea test cases reproducibles para issues:
- El test falla de forma confiable
- Documenta pasos de reproducción claros
- Resultado: issue está "pinned" en el test suite

#### `/optimize` (to4iki)
Análisis de performance con implementación:
- Identifica bottlenecks con profiling
- Propone optimizaciones concretas
- Implementación con guidance paso a paso

---

### Context Loading & Priming

#### `/context-prime` (elizaOS)
Priming comprehensivo con contexto del proyecto:
```
/context-prime
→ Lee estructura del repo
→ Carga documentación clave
→ Establece goals del proyecto
→ Define parámetros de colaboración
```
Para empezar sesiones en proyectos complejos con contexto completo desde el inicio.

#### `/prime` (yzyydev)
Versión ligera:
- Lee estructura de directorios
- Carga archivos clave (CLAUDE.md, README, configuraciones)
- Contexto standarizado rápido

#### `/common-ground` (jeffallan)
**El más ingenioso** — hace que Claude explicite sus suposiciones ocultas:
```
/common-ground
→ Claude lista TODAS sus suposiciones sobre el proyecto
→ Stack asumido, patterns asumidos, convenciones asumidas
→ Humano confirma o corrige
→ Resultado: colaboración sin malentendidos implícitos
```
Resuelve el problema de Claude asumiendo Rails cuando usas Django, o Tailwind cuando usas CSS modules.

#### `/load-llms-txt` (ethpandaops)
Carga archivos `llms.txt` al contexto:
- Terminología específica del dominio
- Configuraciones de modelos
- Baseline vocabulary para discusiones de AI

#### `/rsi` (ddisisto)
Lee todos los commands disponibles y archivos clave del proyecto:
- Optimiza el workflow de AI-assisted development
- Un único comando de orientación al inicio de sesión

---

### Documentation & Changelogs

#### `/create-docs` (jerseycheese)
Genera documentación comprehensiva:
- Analiza estructura del código y su propósito
- Documenta inputs/outputs y comportamiento
- Cubre edge cases y error handling
- User interaction flows

#### `/add-to-changelog` (berrydev-ai)
Mantiene el changelog con formato consistente:
- Agrega entradas nuevas sin romper el formato
- Sigue el estándar del proyecto automáticamente

#### `/explain-issue-fix` (hackdays-io)
Documenta el approach de solución para un issue:
- Por qué esta solución y no otra
- Desafíos técnicos superados
- Contexto para revisores del PR

#### `/update-docs` (Consiliency)
Actualiza documentación de implementación:
- Verifica status actual de docs vs código
- Actualiza progress y fases del proyecto
- Mantiene consistencia entre documentos

---

### CI / Deployment

#### `/release` (kelp)
Gestión de releases:
- Actualiza CHANGELOG
- Evalúa el tipo de version bump (major/minor/patch)
- Revisa README para cambios necesarios
- Documenta los cambios del release

#### `/run-ci` (hackdays-io)
Corre CI localmente:
- Activa virtual environments
- Ejecuta scripts de CI
- Itera arreglando errores hasta que todos los tests pasan

---

### Project & Task Management

#### `/create-command` (scopecraft)
Meta-command: crea nuevos slash commands:
- Analiza el requirement del nuevo command
- Usa el template apropiado según la categoría
- Enforcea el estándar de commands
- Genera documentación del command

#### `/create-prp` (Wirasm)
Genera Product Requirement Plans:
- Lee metodología PRP
- Sigue el template estándar
- Crea requirements comprehensivos

#### `/prd-generator` (dredozubov)
Genera PRDs completos desde conversación:
```
/create-prd
→ Executive Summary
→ User Stories
→ MVP Scope
→ Architecture
→ Success Criteria
→ Implementation Phases
```
Invocar después de discutir requirements en chat.

#### `/do-issue` (jerseycheese)
Implementa un GitHub issue con review points manuales:
- Modo manual (con checkpoints de revisión)
- Modo automático (para issues bien especificados)

#### `/todo` (chrisleyva)
Task management dentro de Claude Code:
- Due dates
- Sorting y priorización
- Gestión completa sin salir de la interfaz

---

### Patterns de uso avanzados

#### Argumentos en commands

```markdown
<!-- .claude/commands/fix-issue.md -->
Arregla el issue #$ARGUMENTS en este repo:
1. Descarga el issue con `gh issue view $ARGUMENTS`
2. Analiza el contexto
3. Implementa la solución
4. Corre los tests relevantes
```

```bash
/fix-issue 1234   # $ARGUMENTS = "1234"
```

#### Commands con preprocessing

```markdown
<!-- .claude/commands/analyze.md -->
---
allowed-tools: [bash, text_editor]
---

!find . -name "*.ts" | head -20

Analiza la estructura TypeScript de este proyecto...
```

La línea `!find...` corre el comando antes de que Claude lo vea. El output se inyecta en el prompt.

#### context:fork para commands costosos

```markdown
<!-- .claude/commands/audit.md -->
---
context: fork
---

Haz una auditoría completa de seguridad...
```

`context: fork` abre el command en un subagente con contexto aislado. El contexto de la sesión principal no se consume.

## Conexiones
- Relacionado con: [[claude-code-skills]], [[claude-code-workflow-patterns]]
- Para crear hooks en lugar de commands: [[claude-code-hooks-ecosystem]]
- Pattern de context:fork explicado en: [[claude-code-skills]]

## Fuentes
- `https://github.com/hesreallyhim/awesome-claude-code` — sección Slash Commands

---

## Timeline

- 2026-04-07: página creada desde awesome-claude-code
