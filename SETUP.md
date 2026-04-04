# Setup — Inicializar tu propia wiki

Guia para configurar LlmBrain con tu dominio especifico.
Completar antes del primer ingest.

---

## Paso 1 — Definir el dominio

Abrir `CLAUDE.md` y responder mentalmente:

- **Que temas va a cubrir esta wiki?** (3-5 categorias principales)
- **Quien la usa?** (solo yo / equipo)
- **Para que la voy a consultar principalmente?** (consultas rapidas / analisis profundo / generacion de contenido)

---

## Paso 2 — Actualizar CLAUDE.md

En la seccion `index.md — estructura`, reemplazar el comentario de categorias con las tuyas:

```markdown
## Categorias

### Conceptos
### Personas
### Proyectos
### Tecnologias
### [tu categoria]
```

Agregar cualquier convencion especifica del dominio en la seccion `Convenciones`.

---

## Paso 3 — Actualizar index.md

Reemplazar el comentario de categorias en `index.md` con la misma estructura que definiste en el paso 2.

---

## Paso 4 — Primera fuente

Depositar un archivo en `sources/`. Puede ser:
- Un articulo convertido a markdown (usar Obsidian Web Clipper)
- Un PDF con texto copiado a `.md`
- Una nota propia
- Un paper, transcript, o documento de referencia

Luego abrir Claude Code y decir:

```
ingest sources/tu-archivo.md
```

---

## Paso 5 — Primer query

Una vez ingested la primera fuente:

```
que dice la wiki sobre X?
```

Verificar que el agente leyó `index.md` primero y cito paginas de `wiki/`.

---

## Paso 6 — Primer lint

Despues de 5-10 fuentes ingestadas:

```
lint the wiki
```

Revisar el reporte en `log.md`. Las sugerencias de nuevas fuentes son el input mas valioso del lint.

---

## Paso 7 — Co-evolucionar el schema

A medida que uses la wiki, vas a descubrir que el formato de algunas paginas no encaja bien con tu dominio, o que falta una categoria, o que el agente no esta enfatizando lo correcto.

Editar `CLAUDE.md` directamente y decirle al agente que leyo la nueva version.

> *"You and the LLM co-evolve this over time as you figure out what works for your domain."* — Karpathy

---

## Referencia rapida de comandos

| Accion | Comando |
|--------|---------|
| Ingestar fuente | `"ingest sources/archivo.md"` |
| Consultar | `"que dice la wiki sobre X?"` |
| Comparar | `"compara A con B"` |
| Health check | `"lint the wiki"` |
| Overview del dominio | `"genera un mapa de todo lo que sabe la wiki"` |

---

## Privacidad

Si el contenido es sensible, agregar al `.gitignore`:

```gitignore
sources/**/*.md
sources/**/*.pdf
wiki/*.md
!wiki/_template.md
!wiki/.gitkeep
```
