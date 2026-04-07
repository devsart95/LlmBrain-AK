---
title: AI Security Skills
type: reference
tags: [seguridad, ai, skills, owasp, testing]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# AI Security Skills

> Catalogo de skills de seguridad disponibles para AI agents, desde static analysis hasta threat modeling y smart contracts.

## Contexto

El ecosistema de agent skills tiene una cobertura significativa en seguridad. Trail of Bits lidera con 21 skills especializados; gstack aporta el workflow CSO ya integrado en DevSar. La comunidad agrega capas complementarias para escenarios especificos (mobile, secrets, bug hunting).

## Detalle

### Trail of Bits — 21 skills (el mas completo)

| Categoria | Skills | Que hacen |
|-----------|--------|-----------|
| Smart Contracts | building-secure-contracts, entry-point-analyzer, spec-to-code-compliance | Seguridad para 6 blockchains |
| Static Analysis | static-analysis (CodeQL/Semgrep/SARIF), semgrep-rule-creator, variant-analysis | Deteccion automatizada |
| Testing | property-based-testing (multi-lenguaje), testing-handbook-skills (fuzzers, sanitizers) | Testing avanzado |
| Code Review | differential-review, audit-context-building | Review security-focused |
| Crypto | constant-time-analysis | Timing side-channels |
| Mobile | firebase-apk-scanner | Android misconfigs |
| Config | insecure-defaults, sharp-edges | APIs peligrosas, defaults inseguros |

### gstack /cso — Chief Security Officer

- OWASP Top 10 + STRIDE threat model
- Zero false-positive exclusions
- Gate de confianza: 8/10+ antes de reportar
- Ya integrado en DevSar via `/review-security --owasp`
- Ver [[sprint-structure-ai]] para detalles del workflow

### Comunidad

| Skill / Autor | Enfoque |
|---------------|---------|
| clawsec (Prompt Security) | Drift detection, audits automatizados, skill integrity verification |
| vibesec | Prevencion IDOR, XSS, SQL injection, SSRF desde perspectiva de bug hunter |
| security-bluebook-builder | Builds de seguridad para apps sensibles |
| defense-in-depth | Seguridad multi-capa |
| cybersecurity-skills (mukul975) | 753 skills en 38 dominios con MITRE ATT&CK mapping |
| varlock | Gestion segura de env vars, previene exposicion de secrets |

### Relevancia para DevSar

Trail of Bits y gstack /cso complementan el workflow `/review-security --owasp` del CLAUDE.md global. `insecure-defaults` y `sharp-edges` son directamente aplicables a cualquier proyecto que toque configuracion de infraestructura o APIs externas. `varlock` refuerza la regla de secrets-en-env-vars.

## Conexiones

- Relacionado con: [[sprint-structure-ai]], [[gstack-overview]], [[agent-skills-ecosystem]], [[ai-development-workflows]], [[multi-model-review]]
- Contrasta con: [[product-management-ai]] (skills de descubrimiento vs seguridad)
- Parte de: [[agent-skills-ecosystem]]
- Ver también: [[generation-verification-loop]] (checkpoints de seguridad en el loop), [[context-engineering-patterns]] (context poisoning como vector de riesgo)

## Fuentes

- `sources/awesome-agent-skills.md` — catalogo curado de skills de seguridad para AI agents

---

## Timeline

> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-07: creacion inicial desde `sources/awesome-agent-skills.md`
