---
title: Performance — React y Next.js
type: concept
tags: [performance, react, nextjs, optimizacion, bundle]
sources: 1
created: 2026-04-04
updated: 2026-04-04
---

# Performance — React y Next.js

> Patrones de optimización específicos de React/Next.js. Severidad Critical = impacto directo en tiempo de carga o interacción.

## Async Waterfall — el problema más común

El mayor desperdicio de performance es esperar operaciones async secuencialmente cuando pueden ser paralelas.

```ts
// ❌ Secuencial — 300ms + 200ms = 500ms total
const user = await fetchUser()
const posts = await fetchPosts()

// ✅ Paralelo — max(300ms, 200ms) = 300ms total
const [user, posts] = await Promise.all([fetchUser(), fetchPosts()])
```

```ts
// ❌ API route — await bloquea innecesariamente
const session = await auth()
const config = await fetchConfig()

// ✅ Iniciar promesas temprano, await tarde
const sessionP = auth()
const configP = fetchConfig()
const [session, config] = await Promise.all([sessionP, configP])
```

```ts
// ✅ Dependencias parciales — better-all
await all({
  user() { return fetchUser() },
  config() { return fetchConfig() },
  profile() { return fetchProfile((await this.$.user).id) } // espera solo user
})
```

**Severidad: Critical** — aplica en casi todos los API routes.

## Bundle Size

```ts
// ❌ Barrel import — carga TODA la librería
import { Check, X, Plus } from 'lucide-react'

// ✅ Import directo — solo el ícono necesario
import Check from 'lucide-react/dist/esm/icons/check'
```

```tsx
// ❌ Import pesado al top level
import { MonacoEditor } from './monaco-editor'   // ~2MB

// ✅ Dynamic import — solo cuando se necesita
const Monaco = dynamic(() => import('./monaco-editor'), { ssr: false })
```

```tsx
// ✅ Preload en hover — el bundle carga antes del click
<button onMouseEnter={() => import('./heavy-editor')}>
  Abrir editor
</button>
```

## Server Components — optimizaciones RSC

```tsx
// ✅ Pasar solo los campos que el Client Component usa
// ❌ Serializa 50 campos innecesarios
<Profile user={user} />

// ✅ Solo lo que necesita
<Profile name={user.name} avatar={user.avatar} />
```

```tsx
// ✅ Composición para paralelizar fetches
// Ambos componentes fetchean en paralelo (Server Components)
export default function Dashboard() {
  return (
    <>
      <Header />     {/* fetch interno */}
      <Sidebar />    {/* fetch interno, paralelo al Header */}
    </>
  )
}
```

```ts
// ✅ React.cache para deduplicar en el mismo request
import { cache } from 'react'
export const getUser = cache(async (id: string) => {
  return db.user.findUnique({ where: { id } })
})
// Múltiples componentes llamando getUser(id) → una sola query
```

```ts
// ✅ after() para logging sin bloquear response
import { after } from 'next/server'

export async function POST(req: Request) {
  const result = await processData(req)
  after(async () => {
    await logAction(result)  // no bloquea la respuesta
  })
  return Response.json(result)
}
```

## Re-renders — reducir renders innecesarios

```tsx
// ✅ setState funcional — sin stale closures
setItems(curr => [...curr, newItem])

// ❌ Referencia a state en el closure
setItems([...items, newItem])  // items puede ser stale
```

```tsx
// ✅ Dependencia primitiva en effects
useEffect(() => {
  console.log(user.id)
}, [user.id])    // re-run solo si cambia el id

// ❌ Objeto como dependencia — re-run en cada render
useEffect(() => {
  console.log(user.id)
}, [user])
```

```tsx
// ✅ startTransition para updates no urgentes
startTransition(() => setFilter(value))  // UI no se bloquea

// ❌ Update síncrono que bloquea
setFilter(value)  // bloquea el thread en cada keystroke
```

```tsx
// ✅ Lazy state initialization — no ejecuta en cada render
const [index, setIndex] = useState(() => buildSearchIndex(items))

// ❌ Ejecuta buildSearchIndex en cada render
const [index, setIndex] = useState(buildSearchIndex(items))
```

## JS Performance — micro-optimizaciones

```ts
// ❌ O(n) en cada lookup
const user = users.find(u => u.id === order.userId)  // en un loop

// ✅ O(1) con Map pre-construido
const userById = new Map(users.map(u => [u.id, u]))
const user = userById.get(order.userId)
```

```ts
// ❌ Sort para encontrar max — O(n log n)
const max = arr.sort((a, b) => b - a)[0]

// ✅ Loop — O(n)
let max = arr[0]
for (const x of arr) if (x > max) max = x
```

```ts
// ❌ RegExp recreada en cada render
function validate(input: string) {
  return /^[^@]+@[^@]+$/.test(input)  // nueva RegExp cada vez
}

// ✅ RegExp hoisted a módulo
const EMAIL_RE = /^[^@]+@[^@]+$/
function validate(input: string) {
  return EMAIL_RE.test(input)
}
```

```ts
// ❌ Muta el array original
users.sort((a, b) => a.name.localeCompare(b.name))

// ✅ Inmutable
users.toSorted((a, b) => a.name.localeCompare(b.name))
```

## Rendering — trucos de CSS

```tsx
// ✅ Animar wrapper div, no el SVG
<div className="animate-spin">
  <svg>...</svg>
</div>

// ❌ Animar SVG directo — más costoso
<svg className="animate-spin">...</svg>
```

```css
/* ✅ content-visibility para listas largas */
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;  /* altura estimada */
}
```

```tsx
// ✅ Condicional con ternario — evita render de '0'
{count > 0 ? <Badge>{count}</Badge> : null}

// ❌ && con número — renderiza '0'
{count && <Badge>{count}</Badge>}
```

## Checklist de performance

- [ ] Fetches independientes en `Promise.all()`
- [ ] Dynamic imports para componentes >50KB
- [ ] Barrel imports reemplazados por direct imports en libs grandes (lucide, lodash)
- [ ] `React.cache()` en data fetchers usados en múltiples Server Components
- [ ] Listas >50 items virtualizadas
- [ ] `content-visibility: auto` en listas largas
- [ ] Bundle analyzer corrido antes de cada release

## Conexiones
- Relacionado con: [[nextjs-best-practices]], [[react-shadcn-patterns]]
- Contrasta con: [[ux-guidelines-formularios-accesibilidad]] — performance no justifica saltarse accesibilidad

## Fuentes
- `sources/uipro-skill/react-performance.csv` — 44 patrones con ejemplos (Critical a Low)

## Log de cambios
- 2026-04-04: creación inicial desde uipro-skill v2.5.0
