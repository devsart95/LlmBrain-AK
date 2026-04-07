---
title: Claude Code — Agent Skills Catalog
type: overview
tags: [claude-code, skills, agentes, catálogo, comunidad]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Claude Code — Agent Skills Catalog

> Colecciones de skills de la comunidad para Claude Code, organizadas por dominio y nivel de calidad.

## Contexto

Los Agent Skills son configuraciones controladas por el modelo (archivos SKILL.md, scripts, recursos) que habilitan a Claude Code para tareas especializadas. La comunidad ha producido colecciones para casi todos los dominios del desarrollo de software.

## Detalle

### Tier S — Las colecciones más citadas

#### Trail of Bits Security Skills
**Quién:** Trail of Bits — firma de seguridad de elite
**Qué:** 21+ skills de auditoría y detección de vulnerabilidades
- Static analysis con CodeQL y Semgrep
- Variant analysis (busca patrones de vulnerabilidad en todo el codebase)
- Fix verification (verifica que los patches realmente resuelven el CVE)
- Differential code review (compara antes/después en security terms)

Para quienes hacen auditorías de seguridad o necesitan code review automatizado con profundidad real. Ver también [[ai-security-skills]] para el contexto completo.

#### Claude Scientific Skills (K-Dense)
**Quién:** K-Dense AI
**Qué:** Skills para ciencia, ingeniería, finanzas, análisis y escritura académica
- Nivel de profundidad comparable a un PhD en cada área
- El curator del awesome-list dice: "si pensabas hacer un PhD, leé estos documentos"
- Incluye un agente que opera de forma autónoma

Valor particular: si el dominio es científico/ingenieril, esta colección tiene contexto que no está en el modelo base.

#### Everything Claude Code (affaan-m)
**Quién:** Affaan Mustafa
**Qué:** Cubre prácticamente cada feature de Claude Code con valor standalone

Lo que lo hace especial:
- Cada recurso funciona independientemente (no es un framework cerrado)
- Podés adoptar el workflow del autor o usar los recursos individualmente
- Cobertura: casi todos los features de Claude Code
- Calidad: "top-notch, well-written" según el curator

#### Fullstack Dev Skills (jeffallan)
**Quién:** jeffallan
**Qué:** 65 skills especializados para full-stack development
- Cubre amplio rango de frameworks específicos
- 9 comandos de project workflow con integración Jira/Confluence
- `/common-ground` — el command más innovador: saca las suposiciones ocultas de Claude a la superficie

---

### Tier A — Muy sólidos para casos específicos

#### cc-devops-skills (akin-ozer)
Skills para DevOps / Infrastructure as Code:
- IaC para "cualquier plataforma con la que hayas sufrido"
- Validaciones, generadores, scripts shell
- El curator lo recomienda incluso solo como documentación

#### AgentSys (avifenesh)
Sistema de automatización de workflows con plugins:
- Task-to-production workflows
- PR management automático
- Code cleanup
- Performance investigation
- Drift detection
- Multi-agent code review
- Miles de líneas con miles de tests
- Incluye `agnix` para linting de configuraciones de agents

#### Superpowers (Jesse Vincent)
Bundle de competencias core para software engineering:
- Cubre gran parte del SDLC
- Planning, reviewing, testing, debugging
- Bien escrito y organizado
- "Best practices de engineering que a veces se sienten como superpowers con Claude Code"

#### Claude Codex Settings (fatih akyon)
Plugins para actividades core del developer:
- GitHub, Azure, MongoDB
- Tavily, Playwright
- Clear, no sobreopinionated
- Compatible con múltiples providers

#### Context Engineering Kit (NeoLabHQ)
Técnicas avanzadas de context engineering:
- Mínimo footprint de tokens
- Foco en mejorar calidad de resultados del agente
- Patrones no documentados en docs oficiales
- Directamente relevante a la eficiencia de sesiones largas

---

### Tier B — Especializados y valiosos en su nicho

#### Book Factory (Robert Guss)
Pipeline completo para crear libros de no-ficción:
- Replica infraestructura editorial tradicional
- Skills especializados por fase (research → outline → writing → editing)
- Para content creators que usan Claude como partner de escritura

#### Claude Code Agents (Paul - UndeadList)
E2E development workflow para solo devs:
- Múltiples auditores en paralelo
- Ciclos de fix automatizados con micro-checkpoint protocols
- Browser-based QA
- "Strict protocols to prevent AI going rogue"

#### Compound Engineering Plugin (EveryInc)
Enfocado en aprender de errores:
- Convierte errores pasados en lecciones
- Documentación de decisiones post-implementación
- Para equipos que iteran sobre el mismo codebase

#### TÂCHES CC Resources (glittercowboy)
"Down-to-earth" sin over-engineering:
- Meta-skills: "skill-auditor", hook creation
- Adaptás vos el workflow, no al revés
- Buena base para construir encima

#### Web Assets Generator (alonw0)
Generación de assets web desde Claude Code:
- Favicons, app icons (PWA), social meta images (OG)
- Para Facebook, Twitter, WhatsApp, LinkedIn
- Resizing, text-to-image, emojis

---

### Workflows notables (no skills pero igual de valiosos)

#### AB Method (Ayoub Bensalah)
Spec-driven workflow para problemas complejos:
- Transforma problemas grandes en "missions" pequeñas y enfocadas
- Subagentes especializados por fase del SDLC
- Slash-commands + workflows específicos

#### Agentic Workflow Patterns (ThibautMelen)
Documentación de todos los patterns de Anthropic con diagramas Mermaid:
- Subagent Orchestration
- Progressive Skills
- Parallel Tool Calling
- Master-Clone Architecture
- Wizard Workflows

El más completo para entender los patterns disponibles y cuándo usarlos.

#### RIPER Workflow (Tony Narlock)
5 fases estrictas:
- **R**esearch → solo leer, no proponer
- **I**nnovate → solo generar ideas, no implementar
- **P**lan → solo planificar, no ejecutar
- **E**xecute → solo implementar el plan aprobado
- **R**eview → solo revisar, no cambiar

La separación de fases previene que Claude mezcle análisis con implementación prematura.

#### Claude Code Infrastructure Showcase (diet103)
Técnica innovadora con hooks para selección inteligente de Skills:
- Hooks que analizan el contexto actual
- Claude selecciona automáticamente el Skill adecuado
- Sin tener que invocar manualmente el skill correcto

#### ClaudoPro Directory (JSONbored)
Hooks, slash commands, subagents y más en un solo lugar:
- Selección de calidad (no es dump genérico)
- Range de tasks especializadas

---

### Cómo evaluar una colección de Skills antes de usarla

1. **¿Tiene tests?** AgentSys tiene miles. Un skill sin tests es una caja negra.
2. **¿Standalone o framework?** Preferir standalone si no querés lockout.
3. **¿Está actualizado?** Claude Code cambia rápido. Skills de 2024 pueden estar desactualizados.
4. **¿Las descripciones son evaluativas?** El curator del awesome-list explica por qué vale. Si solo lista features → más precaución.
5. **¿Compatible con otros providers?** Agentic Workflow Patterns, Dippy lo son. Preferir si tu setup es multi-model.

## Conexiones
- Relacionado con: [[agent-skills-ecosystem]], [[claude-code-skills]]
- Skills de seguridad: [[ai-security-skills]]
- Para entender cómo construir skills: [[claude-code-skills]]
- Workflows: [[claude-code-workflow-patterns]], [[ralph-wiggum-technique]]

## Fuentes
- `https://github.com/hesreallyhim/awesome-claude-code` — secciones Agent Skills y Workflows

---

## Timeline

- 2026-04-07: página creada desde awesome-claude-code
