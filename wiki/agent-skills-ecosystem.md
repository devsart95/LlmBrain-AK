---
title: Agent Skills Ecosystem
type: overview
tags: [ai, skills, claude-code, herramienta, ecosistema]
sources: 1
created: 2026-04-07
updated: 2026-04-07
---

# Agent Skills Ecosystem

> Archivos markdown (SKILL.md) que dan a un coding agent un rol especializado con instrucciones detalladas, distribuidos como un ecosistema abierto entre plataformas y proveedores.

## Contexto

Los Agent Skills emergen como la nueva capa de integracion entre plataformas y agentes AI. Si antes los servicios publicaban SDKs para que los desarrolladores los consumieran, ahora publican skills para que los agentes los operen directamente. El repositorio central es [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) con 1060+ skills y 14.5k stars.

## Detalle

### Que es un Skill

Un skill es un archivo markdown estructurado (SKILL.md o similar) que define:
- El rol que debe asumir el agente
- El dominio de conocimiento especifico
- Instrucciones de operacion detalladas
- Patrones de uso y ejemplos

### Plataformas soportadas

Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot.

### Proveedores principales

| Proveedor | Skills | Dominio principal |
|-----------|--------|-------------------|
| Anthropic | 17 | Documentos, diseno, testing, MCP |
| Microsoft | 133+ | Azure SDKs (.NET, Java, Python, Rust, TS) |
| Garry Tan (gstack) | 28 | Sprint completo: planning → deploy |
| Trail of Bits | 21 | Security analysis, smart contracts, fuzzing |
| Google Workspace | 17 | Drive, Sheets, Gmail, Calendar, Docs |
| Hugging Face | 13 | ML workflows, model training, datasets |
| Netlify | 12 | Edge functions, deploy, forms, caching |
| HashiCorp | 11 | Terraform providers, modules, testing |
| Expo | 11 | React Native, SwiftUI, Jetpack Compose |
| MiniMax | 10 | Frontend, mobile, shader, documentos |
| Firecrawl | 8 | Web scraping, crawling, search |
| GSAP | 8 | Animaciones, ScrollTrigger, React |
| Better Auth | 7 | Auth: email, 2FA, organization |
| Vercel | 7 | React, Next.js, diseno web |
| Cloudflare | 6 | Workers, MCP servers, Durable Objects |
| Google Stitch | 6 | DESIGN.md, design-to-code loop |
| DuckDB | 6 | SQL queries, file reading, memory |
| Resend | 5 | Email: envio, templates, inbox |

### Insight clave

La tendencia es que cada plataforma/servicio publica sus propios skills oficiales. El AI agent se convierte en la nueva superficie de integracion — como fueron los SDKs antes, pero orientados a que el agente opere el servicio en lugar de que el desarrollador lo integre manualmente.

## Conexiones
- Relacionado con: [[gstack-overview]], [[context-engineering-patterns]], [[ai-security-skills]], [[product-management-ai]], [[uipro-design-skills]]
- Contrasta con: [[ejemplo-rag-vs-llm-wiki]] (RAG no tiene estado acumulado; los skills sí tienen roles especializados)
- Parte de: [[ai-development-workflows]]
- Ver también: [[sprint-structure-ai]] (gstack como caso de uso de skills por fase), [[design-md-format]] (Google Stitch skills)

## Fuentes
- `sources/awesome-agent-skills.md` — catalogo de skills por proveedor con conteos, dominios y descripcion del ecosistema

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-07: creacion inicial desde `sources/awesome-agent-skills.md`
