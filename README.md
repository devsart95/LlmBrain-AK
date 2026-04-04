# WikiJRS

**A personal knowledge base maintained by an LLM — not a chatbot, a persistent second brain.**

> Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

---

## The idea

Most people use LLMs like search engines: ask, get answer, forget. Karpathy proposes something different — make the LLM **incrementally build and maintain a wiki** that compounds over time.

> *"The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping."*
> — Andrej Karpathy

The insight: every time you feed the LLM a new source, it doesn't just answer a question. It updates 10–15 related pages, resolves contradictions, fills gaps, and cross-references everything. The wiki grows smarter with each ingest.

Traditional RAG rediscovers knowledge on every query. This approach **compiles it once and maintains it continuously**.

---

## Architecture

Three layers, clean separation:

```
WikiJRS/
├── sources/          # Raw inputs — immutable, source of truth
│   └── article.md    # PDFs, papers, notes, transcripts, clips
│
├── wiki/             # LLM-generated pages — Claude owns this layer
│   ├── concept-a.md  # One file per entity, concept, or topic
│   └── person-b.md
│
├── schema/           # Design decisions & changelog
│   └── decisiones.md
│
├── index.md          # Content catalog — updated on every ingest
├── log.md            # Append-only activity log
└── CLAUDE.md         # Schema & operating instructions for Claude
```

---

## Three operations

### `INGEST` — add a new source
Drop a file in `sources/`. Tell Claude: *"ingest sources/article.md"*

Claude reads the source, identifies entities and concepts, creates or updates 5–15 wiki pages, updates the index, and logs everything.

### `QUERY` — ask the wiki
Ask a question. Claude searches wiki pages, synthesizes an answer with citations, and optionally saves valuable answers as new wiki pages.

### `LINT` — health check
Tell Claude: *"lint the wiki"*

Claude scans for orphan pages, contradictions between entries, stale claims, and gaps — concepts referenced but never defined. Generates a report in `log.md`.

---

## How to use this

**Requirements:** [Claude Code](https://claude.ai/code) with Opus model for ingest/lint, Sonnet for search/read.

```bash
# 1. Clone or fork this repo
git clone https://github.com/devsart95/WikiJRS
cd WikiJRS

# 2. Open with Claude Code
claude .

# 3. Switch to Opus for deep operations
/model opus

# 4. Start adding knowledge
# Drop a file in sources/, then:
# "ingest sources/my-article.md"

# 5. Query your wiki
# "what does the wiki say about X?"

# 6. Periodic maintenance
# "lint the wiki"
```

The `CLAUDE.md` file is the schema — it tells Claude exactly how to operate, what format to use, and what decisions have been made. Edit it to evolve the system with your needs.

---

## Model assignment

| Operation | Model | Why |
|-----------|-------|-----|
| Ingest / Lint | **Opus** | Deep reasoning, cross-referencing, contradiction detection |
| Query | **Opus** | Multi-source synthesis |
| Search / Read | **Sonnet** | Fast, efficient file retrieval |

---

## Optional tooling

Once the wiki grows past ~100 pages:

- **[qmd](https://github.com/qmd-app/qmd)** — local BM25/vector search with MCP server, integrates directly with Claude
- **[Obsidian](https://obsidian.md)** — graph view to visualize connections between pages, renders `[[wiki-links]]`
- **[Obsidian Web Clipper](https://obsidian.md/clipper)** — clip web articles to markdown before ingesting

No code required until scale demands it.

---

## Privacy

The `sources/` and `wiki/` directories contain your personal knowledge. If the content is sensitive, add these lines to your `.gitignore`:

```gitignore
sources/**/*.pdf
sources/**/*.md
wiki/*.md
!wiki/.gitkeep
```

The framework files (`CLAUDE.md`, `index.md`, `log.md`, `cuestionario.md`) are safe to keep public as they contain no personal data.

---

## Credits

Pattern by [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
Implementation by [devsart95](https://github.com/devsart95) — Paraguay 🇵🇾
