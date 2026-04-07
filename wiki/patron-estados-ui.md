---
title: Patrón — Estados UI (Loading, Empty, Error, Success)
type: concept
tags: [ux, ui, estados, loading, empty-state, error-state, feedback]
sources: 1
created: 2026-04-04
updated: 2026-04-04
---

# Patrón — Estados UI

> Un componente que carga datos sin los cuatro estados (loading, empty, error, success) no está terminado. Regla de oro DevSar.

## Los cuatro estados obligatorios

```
Componente con datos async
├── Loading state  → skeleton o spinner mientras carga
├── Empty state    → mensaje + acción cuando no hay datos
├── Error state    → mensaje + retry cuando falla
└── Success state  → datos renderizados
```

## Loading State

**Cuándo:** operación async >300ms

| Tipo | Cuándo usar |
|------|------------|
| Skeleton screen | Listas, cards, tablas — el usuario ve la estructura antes del contenido |
| Spinner | Modales, botones, acciones puntuales |
| Progress bar | Uploads, procesos con progreso medible |

```tsx
// Skeleton — preferido para listas/tablas
<div className="animate-pulse space-y-3">
  <div className="h-4 bg-slate-200 rounded w-3/4" />
  <div className="h-4 bg-slate-200 rounded w-1/2" />
  <div className="h-4 bg-slate-200 rounded w-5/6" />
</div>

// Spinner — para acciones puntuales
<div className="flex items-center justify-center p-8">
  <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
</div>
```

## Empty State

**Cuándo:** la query retorna vacío, primera vez del usuario

Estructura obligatoria: mensaje explicativo + acción sugerida.

```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <InboxIcon className="h-12 w-12 text-slate-300 mb-4" aria-hidden="true" />
  <h3 className="text-sm font-semibold text-slate-900">No hay registros</h3>
  <p className="mt-1 text-sm text-slate-500">
    Empezá creando tu primer registro.
  </p>
  <Button className="mt-4" onClick={onCreate}>
    Crear registro
  </Button>
</div>
```

**No hacer:** pantalla en blanco, "0 resultados" sin contexto, spinner infinito.

## Error State

**Cuándo:** falla de red, error de API, timeout

Estructura: mensaje user-friendly (no el stack trace) + opción de retry.

```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <AlertCircle className="h-12 w-12 text-red-400 mb-4" aria-hidden="true" />
  <h3 className="text-sm font-semibold text-slate-900">
    No se pudo cargar
  </h3>
  <p className="mt-1 text-sm text-slate-500">
    Ocurrió un error al obtener los datos.
  </p>
  <Button variant="outline" className="mt-4" onClick={onRetry}>
    Intentar de nuevo
  </Button>
</div>
```

## Success / Feedback de mutaciones

**Toasts:** transitorios, se auto-cierran en 3-5 segundos.

```tsx
// Toast success
toast.success("Guardado correctamente")

// Toast error
toast.error("No se pudo guardar. Intentá de nuevo.")
```

**Reglas de toast:**
- Auto-dismiss en 3-5 segundos
- No para información crítica que el usuario debe leer detenidamente
- No apilar más de 3 simultáneos

## Botón de Submit — estados

```tsx
<Button type="submit" disabled={isPending}>
  {isPending ? (
    <>
      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      Guardando...
    </>
  ) : (
    "Guardar"
  )}
</Button>
```

**Regla:** mantener habilitado con spinner, no deshabilitar sin feedback visual.

## Confirmación de acciones destructivas

Cualquier acción irreversible (eliminar, resetear, cancelar) necesita confirmación.

```tsx
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Eliminar</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogTitle>¿Estás seguro?</AlertDialogTitle>
    <AlertDialogDescription>
      Esta acción no se puede deshacer.
    </AlertDialogDescription>
    <AlertDialogCancel>Cancelar</AlertDialogCancel>
    <AlertDialogAction onClick={onDelete}>Eliminar</AlertDialogAction>
  </AlertDialogContent>
</AlertDialog>
```

## Progress de multi-paso

```tsx
// Indicador de paso
<div className="flex items-center gap-2 text-sm text-slate-500">
  <span className="font-medium text-slate-900">Paso 2</span>
  <span>de 4</span>
</div>
```

## Conexiones
- Relacionado con: [[ux-guidelines-formularios-accesibilidad]], [[react-shadcn-patterns]], [[ux-guidelines-navegacion-animacion]]
- Contrasta con: [[estilos-ui-por-tipo-producto]] (el estilo varia por dominio; los estados son universales)
- Parte de: [[ux-guidelines-navegacion-animacion]]
- Ver también: [[nextjs-best-practices]] (loading.tsx, error.tsx en App Router), [[uipro-design-skills]] (ui-styling skill incluye states), [[sistema-colores-por-dominio]] (paleta de estados)

## Fuentes
- `sources/uipro-skill/ux-guidelines.csv` — filas 78-83 (Feedback), 32-35 (Interaction)
- `sources/uipro-skill/SKILL.md` — sección completitud de componentes

---

## Timeline

> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-04: creación inicial desde uipro-skill v2.5.0
