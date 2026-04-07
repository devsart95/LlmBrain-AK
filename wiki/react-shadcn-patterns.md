---
title: React + shadcn/ui — Patrones y Convenciones
type: concept
tags: [react, shadcn, typescript, componentes, ui]
sources: 1
created: 2026-04-04
updated: 2026-04-04
---

# React + shadcn/ui — Patrones y Convenciones

> Uso correcto de shadcn/ui y patrones React para proyectos productivos. shadcn = componentes copiados, no dependencia — eso cambia cómo se extienden.

## Setup

```bash
# Inicializar primero (genera components.json y globals.css)
npx shadcn@latest init

# Agregar componentes
npx shadcn@latest add button dialog form table
```

**Nunca** copiar manualmente el código de la docs — el CLI configura paths, aliases y CSS variables correctamente.

## Theming — CSS Variables

```css
/* globals.css — sistema de colores */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  /* ... */
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... */
}
```

Usar siempre `bg-primary text-primary-foreground` — nunca hardcodear `bg-blue-500`.

## Formularios — patrón completo

```tsx
// Patrón correcto: react-hook-form + zod + shadcn Form
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form'

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
})

export function UserForm() {
  const form = useForm({ resolver: zodResolver(schema) })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" autoComplete="email" {...field} />
              </FormControl>
              <FormMessage />   {/* Error inline automático */}
            </FormItem>
          )}
        />
      </form>
    </Form>
  )
}
```

## Componentes clave — cuándo usar cuál

| Componente | Cuándo | No usar para |
|-----------|--------|-------------|
| `Dialog` | Modales, confirmaciones, forms en overlay | Navegación lateral |
| `Sheet` | Paneles laterales, filtros, settings | Modales centrales |
| `Popover` | Dropdowns flotantes, pickers de fecha | Listas de acciones |
| `DropdownMenu` | Menús de acciones, menú de usuario | Content flotante complejo |
| `Command` | Command palette, búsquedas con filtro | Selects simples |
| `Select` | Selección de opción de lista | Búsquedas complejas |
| `Tabs` | Secciones de contenido relacionado | Navegación de páginas |
| `Accordion` | FAQ, configuraciones colapsables | Tabs |
| `Tooltip` | Hints en botones icon-only, texto truncado | Info crítica |
| `Table` | Datos tabulares | Layout grid |
| `DataTable` | Tablas con sort/filter/pagination | Listas simples |

## Dialog — estructura correcta

```tsx
<Dialog open={open} onOpenChange={setOpen}>
  <DialogTrigger asChild>
    <Button>Abrir</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Título obligatorio</DialogTitle>
      <DialogDescription>Descripción para accesibilidad</DialogDescription>
    </DialogHeader>
    {/* contenido */}
  </DialogContent>
</Dialog>
```

## Toasts — Sonner

```tsx
// layout.tsx — una vez en root
import { Toaster } from '@/components/ui/sonner'
export default function Layout({ children }) {
  return <>{children}<Toaster /></>
}

// En cualquier componente
import { toast } from 'sonner'
toast.success("Guardado correctamente")
toast.error("No se pudo guardar")
toast.loading("Procesando...")
```

## Tooltip — setup

```tsx
// Wrap en root con TooltipProvider
<TooltipProvider>
  <App />
</TooltipProvider>

// Uso
<Tooltip>
  <TooltipTrigger asChild>
    <Button size="icon" aria-label="Eliminar">
      <Trash2 className="h-4 w-4" aria-hidden="true" />
    </Button>
  </TooltipTrigger>
  <TooltipContent>Eliminar registro</TooltipContent>
</Tooltip>
```

## DataTable — TanStack Table

```tsx
// Para tablas con sort/filter/pagination
import { useReactTable, getCoreRowModel } from '@tanstack/react-table'

const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  // getSortedRowModel, getFilteredRowModel según necesidad
})
```

## Extensión de componentes

```tsx
// Correcto: className para one-off customizations
<Button className="w-full">Submit</Button>

// Correcto: variant para variantes definidas
<Button variant="destructive" size="sm">Eliminar</Button>

// Incorrecto: modificar button.tsx para casos específicos
// Los componentes de /components/ui/ son primitivos — no tocarlos
```

## Conexiones
- Relacionado con: [[nextjs-best-practices]], [[patron-estados-ui]], [[ux-guidelines-formularios-accesibilidad]], [[performance-react-ui]]
- Contrasta con: [[uipro-design-skills]] (uipro extiende shadcn con tokens y brand; shadcn es la capa base)
- Ver también: [[design-tokens-comparativa]] (CSS variables = token architecture en shadcn), [[sistema-colores-por-dominio]] (theming con CSS vars), [[ux-guidelines-mobile-touch]] (touch targets en componentes)

## Fuentes
- `sources/uipro-skill/stack-shadcn.csv` — 39 convenciones shadcn con ejemplos
- `sources/uipro-skill/stack-react.csv` — patrones React generales

---

## Timeline

> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-04: creación inicial desde uipro-skill v2.5.0
