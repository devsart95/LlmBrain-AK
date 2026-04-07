---
title: Next.js 15 — Best Practices
type: concept
tags: [nextjs, react, performance, typescript, web]
sources: 1
created: 2026-04-04
updated: 2026-04-04
---

# Next.js 15 — Best Practices

> Reglas para Next.js 15+ con App Router. Cambios breaking vs versiones anteriores marcados explícitamente.

## Routing

| Regla | Do | Don't | Severidad |
|-------|----|-------|-----------|
| App Router | `app/` directory con `page.tsx` | `pages/` en proyectos nuevos | Medium |
| Loading States | `loading.tsx` por route | `useState` para loading en page | Medium |
| Error Handling | `error.tsx` con función `reset` | `try/catch` en cada componente | **High** |
| Route Groups | `(marketing)/about/page.tsx` para organizar sin afectar URL | Carpetas anidadas que modifican URL | Low |

## Rendering

| Regla | Do | Don't | Severidad |
|-------|----|-------|-----------|
| Server Components default | Mantener server por default | `'use client'` innecesario | **High** |
| Push Client Components down | Client wrapper solo para partes interactivas | Marcar `page.tsx` como client | **High** |
| Streaming | `<Suspense>` para fetches lentos | Esperar todos los datos antes de renderizar | Medium |

```tsx
// Correcto — Client Component solo donde hay interactividad
// page.tsx (Server Component)
export default async function DashboardPage() {
  const data = await fetchData()
  return (
    <div>
      <StaticHeader data={data} />      {/* Server */}
      <InteractiveFilters />            {/* Client — 'use client' adentro */}
      <Suspense fallback={<Skeleton />}>
        <SlowDataComponent />           {/* Server con streaming */}
      </Suspense>
    </div>
  )
}
```

## Data Fetching

> **Breaking Change en Next.js 15:** `fetch()` ya no cachea por default. Ahora es `no-store` por default.

```tsx
// Next.js 15 — Explicit caching requerido
fetch(url, { cache: 'force-cache' })      // SSG — cachea
fetch(url, { next: { revalidate: 3600 }}) // ISR — revalida cada hora
fetch(url)                                 // Sin cache (default en v15)

// Server Actions para mutations
async function createPost(formData: FormData) {
  'use server'
  await db.post.create({ ... })
  revalidatePath('/posts')
}
```

## Images

```tsx
// Siempre <Image> de next/image
import Image from 'next/image'

// Con dimensiones (previene layout shift)
<Image src="/hero.jpg" alt="..." width={800} height={400} />

// Responsive con fill
<div className="relative aspect-video">
  <Image src="/hero.jpg" alt="..." fill className="object-cover" />
</div>

// LCP images — priority
<Image src="/hero.jpg" alt="..." width={800} height={400} priority />
```

## Fonts

```tsx
// next/font — siempre, nunca <link> externo
import { Inter, IBM_Plex_Sans } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

// En layout.tsx
export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

## Metadata

```tsx
// Metadata estática
export const metadata: Metadata = {
  title: 'Mi App',
  description: '...',
  openGraph: { images: ['/og.png'] },
}

// Metadata dinámica
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await fetchPost(params.slug)
  return { title: post.title }
}
```

## API Routes

```ts
// app/api/users/route.ts
import { NextResponse } from 'next/server'
import { z } from 'zod'

const schema = z.object({ name: z.string() })

export async function POST(request: Request) {
  const body = schema.parse(await request.json())  // Validar siempre
  const user = await db.user.create({ data: body })
  return NextResponse.json(user)
}
```

## Middleware

```ts
// middleware.ts — solo código Edge-compatible
import { NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  // Auth check, headers, redirects
  const session = request.cookies.get('session')
  if (!session) return NextResponse.redirect(new URL('/login', request.url))
  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
}
```

**Prohibido en middleware:** `fs`, `path`, Node.js APIs — solo Edge runtime.

## Environment Variables

```ts
// NEXT_PUBLIC_ para variables accesibles en client
NEXT_PUBLIC_API_URL=https://api.example.com

// Sin prefijo para server-only
DATABASE_URL=postgresql://...

// Validar en startup — nunca undefined en runtime
if (!process.env.DATABASE_URL) throw new Error('DATABASE_URL required')
```

## Performance

| Regla | Do | Don't | Severidad |
|-------|----|-------|-----------|
| Bundle analyzer | `ANALYZE=true npm run build` periódicamente | Ignorar crecimiento del bundle | Medium |
| Dynamic imports | `dynamic(() => import('./Heavy'), { ssr: false })` | Importar componentes pesados al top | Medium |
| Bundle analyzer | `@next/bundle-analyzer` | Blind shipping |  Medium |

## Conexiones
- Relacionado con: [[performance-react-ui]], [[react-shadcn-patterns]], [[patron-estados-ui]]
- Parte de: [[ux-guidelines-formularios-accesibilidad]] — error handling patterns
- Ver también: [[tipografia-pairings]] (next/font para Inter y IBM Plex Sans), [[design-patterns-dark-mode]] (CSS variables en globals.css), [[ai-development-workflows]] (Next.js como plataforma target del SDD)

## Fuentes
- `sources/uipro-skill/stack-nextjs.csv` — 39 reglas Next.js 15+ con ejemplos

---

## Timeline

> Evidencia cronologica append-only. Cada entrada registra cuando y de donde llego la informacion.
> El contenido de arriba (Compiled Truth) se actualiza; el timeline solo crece.

- 2026-04-04: creación inicial desde uipro-skill v2.5.0
