# wikijrs — Estado actual

> Wiki personal de conocimiento técnico con web app geek/dark.

## Completado

- 37 páginas wiki en `wiki/` con frontmatter YAML (tags, type, sources, dates)
- Crosslinks entre todas las páginas (sección `## Conexiones`)
- `wikisearch` CLI + MCP server (BM25, `uv run wiki search/index/lint/tags`)
- Web app Next.js 15 en `web/` — dashboard, browse, D3 graph, ingest, query, log, Cmd+K
- Tema geek dark (violet + cyan, JetBrains Mono)
- Dev server: `cd web && npm run dev -- --port 3099`

## Pendiente

### Deploy web — wikijrs.vercel.app

**Objetivo:** alimentar la wiki desde la web (ingest + query funcionales en producción).

**Por qué no GitHub Pages:** es hosting estático — las rutas API (ingest, query, search) requieren Node.js en servidor.

**Arquitectura correcta:**
1. Crear repo `devsart95/wikijrs` en GitHub y pushear todo
2. Modificar `web/src/app/api/ingest/route.ts` — en vez de escribir al filesystem local, hacer commit al repo via GitHub API (`octokit`)
3. Conectar Vercel al repo → redeploy automático en cada push
4. Variables de entorno en Vercel: `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`, `GITHUB_REPO`
5. Resultado: `wikijrs.vercel.app` con ingest que persiste en git, `git pull` localmente para sincronizar

**Flujo final:**
```
Ingest desde web → GitHub API commit → Vercel redeploy → wiki actualizada
git pull local   → páginas nuevas disponibles en CLI + MCP
```

## Stack

- Python + uv: `wikisearch` CLI y MCP server
- Next.js 15 App Router + TypeScript + Tailwind + shadcn/ui
- Vercel AI SDK + Anthropic (ingest y query)
- D3.js (force graph)
- Remote: `https://github.com/devsart95/LlmBrain-AK.git`
