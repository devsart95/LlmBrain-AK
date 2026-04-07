# awesome-agent-skills — VoltAgent

> Fuente: https://github.com/VoltAgent/awesome-agent-skills
> Fecha de captura: 2026-04-07
> 1060+ agent skills curados para Claude Code, Codex, Gemini CLI, Cursor, etc.
> 14.5k stars, 293 commits, comunidad activa

## Que es

Coleccion curada de Agent Skills (archivos SKILL.md) de equipos oficiales y la comunidad. Enfasis en skills reales usados por equipos de ingenieria, no generados masivamente con AI.

## Plataformas compatibles
Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, Antigravity, y otros AI coding environments.

## Proveedores oficiales principales

### Anthropic (17 skills)
- docx, doc-coauthoring, pptx, xlsx, pdf — documentos
- algorithmic-art, canvas-design, frontend-design — diseno
- slack-gif-creator, theme-factory, web-artifacts-builder — creacion
- mcp-builder — integracion MCP
- webapp-testing — testing con Playwright
- brand-guidelines, internal-comms — marca y comunicacion
- skill-creator, template — meta-skills

### Vercel (7 skills)
- react-best-practices, composition-patterns — React
- next-best-practices, next-cache-components, next-upgrade — Next.js
- web-design-guidelines — diseno web
- react-native-skills — mobile

### Cloudflare (6 skills)
- agents-sdk, building-ai-agent-on-cloudflare — agentes AI
- building-mcp-server-on-cloudflare — MCP servers
- durable-objects — estado persistente
- web-perf — Core Web Vitals
- wrangler — deploy Workers, KV, R2, D1

### Google Labs / Stitch (6 skills)
- design-md — crear DESIGN.md
- enhance-prompt — mejorar prompts con specs de diseno
- react-components, shadcn-ui — conversion a React
- remotion — videos walkthrough
- stitch-loop — feedback loop design-to-code

### Google Workspace CLI (17 skills)
- Drive, Sheets, Gmail, Calendar, Docs, Slides, Tasks, People, Chat, Classroom, Forms, Keep, Events, ModelArmor, Workflow

### Stripe (2 skills)
- stripe-best-practices, upgrade-stripe

### Better Auth (7 skills)
- best-practices, explain-error, providers, create-auth, emailAndPassword, organization, twoFactor

### HashiCorp / Terraform (11 skills)
- azure-verified-modules, new-terraform-provider, provider-resources, provider-test-patterns, provider-actions, run-acceptance-tests, refactor-module, terraform-search-import, terraform-style-guide, terraform-stacks, terraform-test

### Expo (11 skills)
- building-native-ui, api-routes, cicd-workflows, deployment, dev-client, tailwind-setup, ui-jetpack-compose, ui-swift-ui, native-data-fetching, upgrading-expo, use-dom

### Hugging Face (13 skills)
- hf-cli, datasets, dataset-viewer, evaluation, jobs, model-trainer, paper-pages, paper-publisher, tool-builder, trackio, vision-trainer, gradio, transformers.js

### Trail of Bits — Security (21 skills)
- ask-questions-if-underspecified, audit-context-building — proceso
- building-secure-contracts — smart contracts para 6 blockchains
- burpsuite-project-parser — analisis Burp Suite
- constant-time-analysis — timing side-channels en crypto
- differential-review — security-focused diff review
- entry-point-analyzer — smart contracts
- firebase-apk-scanner — Android security
- insecure-defaults — configuraciones inseguras
- modern-python — uv, ruff, ty, pytest
- property-based-testing — multi-lenguaje + smart contracts
- semgrep-rule-creator, semgrep-rule-variant-creator — deteccion vulnerabilidades
- sharp-edges — APIs peligrosas
- spec-to-code-compliance — compliance blockchain
- static-analysis — CodeQL, Semgrep, SARIF
- testing-handbook-skills — fuzzers, sanitizers
- variant-analysis — vulnerabilidades similares

### Sentry (7 skills)
- agents-md, claude-settings-audit, code-review, commit, create-pr, find-bugs, iterate-pr

### Microsoft (133+ skills)
- 9 core skills (cloud-solution-architect, copilot-sdk, mcp-builder, etc.)
- .NET (28), Java (25), Python (39), Rust (7), TypeScript (25)
- Foco: Azure SDKs para cada servicio

### Garry Tan / gstack (28 skills)
- Ya documentados en wiki/gstack-overview.md y wiki/sprint-structure-ai.md

### Notion (4 skills)
- knowledge-capture, meeting-intelligence, research-documentation, spec-to-implementation

### Otros oficiales
- Supabase: postgres-best-practices
- Neon: neon-postgres, claimable-postgres, egress-optimizer
- ClickHouse: clickhouse-best-practices
- Remotion: video creation con React
- Replicate: AI models API
- Typefully: social media scheduling
- DuckDB: 6 skills (query, read-file, docs, memories, install)
- GSAP/GreenSock: 8 skills (core, timeline, scrolltrigger, plugins, utils, react, performance, frameworks)
- Firecrawl: 8 skills (cli, agent, browser, crawl, download, map, scrape, search)
- Sanity: 4 skills (best-practices, content-modeling, seo-aeo, experimentation)
- Tinybird: 4 skills (best-practices, cli, python-sdk, typescript-sdk)
- Courier: multi-channel notifications
- CallStack: react-native-best-practices, github, upgrading-react-native
- Netlify: 12 skills (functions, edge-functions, blobs, db, image-cdn, forms, frameworks, caching, config, cli-deploy, deploy, ai-gateway)
- Resend: 5 skills (resend, react-email, email-best-practices, agent-email-inbox, resend-cli)
- MiniMax: 10 skills (frontend, fullstack, mobile, shader, gif, pdf, pptx, xlsx, docx)

### Product Management — Pawel Huryn (40+ skills)
- Marketing & Growth: marketing-ideas, north-star-metric, positioning, product-name, value-props
- Product Discovery: analyze-feature-requests, brainstorm-experiments, identify-assumptions, interview-script, metrics-dashboard, opportunity-solution-tree, prioritize-features
- Product Strategy: ansoff-matrix, business-model, lean-canvas, monetization, pestle, porters-five-forces, pricing, product-strategy, product-vision, startup-canvas, swot, value-proposition
- Toolkit: draft-nda, grammar-check, privacy-policy, review-resume

## Comunidad — highlights relevantes

### Context Engineering
- context-fundamentals, context-degradation, context-compression, context-optimization
- multi-agent-patterns, memory-systems, tool-design, evaluation
- data-structure-protocol — graph-based long-term memory
- prompt-engineering — techniques incluyendo Anthropic best practices

### Development Workflows (NeoLab)
- code-review — 6 specialized agents (bug-hunter, security-auditor, quality, contracts, historical-context, test-coverage)
- reflexion — self-refinement loop
- sdd — spec-driven development
- ddd — domain-driven + clean architecture + SOLID
- sadd — subagent-dispatched development
- kaizen — continuous improvement (Kaizen + Lean)
- write-concisely — Elements of Style aplicado

### Testing & Quality (obra/superpowers)
- test-driven-development, subagent-driven-development
- systematic-debugging, root-cause-tracing
- testing-anti-patterns, verification-before-completion
- dispatching-parallel-agents

### Security
- clawsec (Prompt Security) — drift detection, automated audits
- vibesec — prevencion IDOR, XSS, SQL injection, SSRF desde perspectiva bug hunter
- security-bluebook-builder, defense-in-depth

### LLM Evaluation (hamelsmu)
- eval-audit, error-analysis, generate-synthetic-data
- write-judge-prompt, validate-evaluator, evaluate-rag
- build-review-interface

### Skill Quality Standards (del repo)
- Formato: SKILL.md con metadata, descripcion, instrucciones
- Emphasis: real-world usage over AI-generated bulk
- Community contributions via issues y PRs
