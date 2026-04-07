---
title: Persistent Browser Pattern
type: concept
tags: [arquitectura, testing, browser, performance]
sources: 1
created: 2026-04-06
updated: 2026-04-06
---

# Persistent Browser Pattern

> Patron de arquitectura de gstack: un daemon de Chromium de larga vida reemplaza el modelo de spawn-per-command, reduciendo latencia de 3-5s a 100-200ms por operacion.

## Contexto
El flujo estandar de automatizacion de browser es stateless: cada comando lanza un browser, ejecuta la accion, y lo cierra. Para tareas individuales es aceptable. Para un workflow de QA con 20 comandos, el overhead es 40-100 segundos solo en launches. En gstack, donde la IA ejecuta ciclos de inspeccion y verificacion frecuentes, ese overhead destruye la cadencia de trabajo.

## Detalle

### El problema
Lanzar un browser fresco por cada comando cuesta 3-5 segundos. Es tiempo de startup de Chromium: inicializar proceso, cargar perfil, establecer contexto. Multiplicado por la cantidad de operaciones de QA en un sprint, el overhead es mayor que el trabajo util.

### La solucion
Un daemon de Chromium que vive entre comandos:
- **Primera llamada:** ~3s (startup normal)
- **Llamadas subsecuentes:** 100-200ms (reutiliza proceso existente)

### Configuracion del daemon
- **Puerto aleatorio** en rango 10000-60000 — permite multiples workspaces sin conflicto
- **Auto-shutdown** a los 30 minutos de idle — no se quedan procesos zombies
- **Login persistence** — sesion autenticada entre comandos, no hay que re-loguear por cada operacion

### Refs via accessibility tree
En lugar de selectors CSS o XPath, el daemon referencia elementos via accessibility tree (`@e1`, `@e2`, etc.). Beneficios:
- Evita problemas de CSP (Content Security Policy)
- No se rompe por framework reconciliation (React re-renders, etc.)
- Funciona a traves de Shadow DOM donde los selectors CSS fallan
- Mas estable que DOM queries en aplicaciones SPA

### Seguridad
El daemon maneja sesiones autenticadas, lo que requiere precauciones explicitas:
- **localhost-only** — no expone puerto a red externa
- **Bearer token UUID** — autenticacion por request al daemon
- **Permisos 0o600** en archivos de configuracion — solo el usuario propietario puede leer
- **Cookie DB read-only** — accede a cookies del browser sin posibilidad de escritura accidental
- **Decryption in-memory** — credenciales nunca en disco en texto plano

## Conexiones
- Relacionado con: [[gstack-overview]], [[sprint-structure-ai]], [[ai-development-workflows]]
- Contrasta con: spawn-per-command (el anti-patron que este patron reemplaza)
- Parte de: [[gstack-overview]]
- Ver también: [[agent-skills-ecosystem]] (patron aplicable a cualquier skill de browser), [[performance-react-ui]] (latencia de operaciones de UI)

## Fuentes
- `sources/gstack-garry-tan.md` — arquitectura del browser daemon de gstack, incluyendo metricas de latencia y mecanismos de seguridad

---

## Timeline
> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-06: creacion inicial desde `sources/gstack-garry-tan.md`
