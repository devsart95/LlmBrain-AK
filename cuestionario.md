# Cuestionario de configuracion — WikiJRS

Responde estas preguntas para que Claude pueda configurar el schema, las categorias y el workflow optimo para tu wiki personal.

---

## 1. Proposito y alcance

**¿Para que es esta wiki?**
- [ ] Base de conocimiento personal (aprendizaje, investigacion)
- [ ] Referencia operativa de un proyecto/producto
- [ ] Memoria institucional de un equipo
- [ ] Combinacion → especifica:

> Tu respuesta:

**¿Quien va a usarla?**
- [ ] Solo yo
- [ ] Yo + equipo pequeno (2-5 personas)
- [ ] Referencia publica

> Tu respuesta:

---

## 2. Dominio de conocimiento

**¿Cuales son los 3-5 temas principales que esta wiki va a cubrir?**

Ejemplos: desarrollo de software, inteligencia artificial, finanzas, medicina, historia, etc.

> Tu respuesta:
> 1.
> 2.
> 3.
> 4.
> 5.

**¿Hay un dominio central o son temas desconectados?**

> Tu respuesta:

---

## 3. Fuentes de entrada

**¿Que tipo de documentos van a entrar como fuentes? (marca todos los que apliquen)**
- [ ] Articulos web / links
- [ ] PDFs (papers, libros, manuales)
- [ ] Notas personales (.txt, .md)
- [ ] Transcripciones de reuniones / llamadas
- [ ] Videos / podcasts (con transcripcion)
- [ ] Codigo fuente / documentacion tecnica
- [ ] Correos o mensajes
- [ ] Otro:

**¿Con que frecuencia vas a agregar nuevas fuentes?**
- [ ] Diario (multiple fuentes por dia)
- [ ] Semanal (5-10 fuentes por semana)
- [ ] Mensual (batch de documentos)
- [ ] Irregular / segun necesidad

> Tu respuesta:

---

## 4. Modelo de consulta

**¿Como vas a usar la wiki principalmente?**
- [ ] Consultas rapidas: "¿que decia X sobre Y?"
- [ ] Analisis profundo: conectar ideas entre fuentes
- [ ] Generacion de contenido nuevo basado en lo conocido
- [ ] Toma de decisiones informada
- [ ] Combinacion

> Tu respuesta:

**¿Que formato de respuesta prefieres?**
- [ ] Respuesta directa + citas
- [ ] Resumen ejecutivo + detalle
- [ ] Lista de puntos clave
- [ ] Segun el tipo de consulta

> Tu respuesta:

---

## 5. Idioma y estilo

**¿En que idioma van a estar las fuentes principalmente?**
- [ ] Espanol
- [ ] Ingles
- [ ] Mixto (ambos)

**¿En que idioma quieres la wiki (paginas generadas)?**
- [ ] Espanol
- [ ] Ingles
- [ ] En el idioma de la fuente original

> Tu respuesta:

---

## 6. Estructura y categorias

**¿Tienes categorias en mente para organizar el conocimiento?**

Ejemplos: Personas, Conceptos, Proyectos, Tecnologias, Procesos, Eventos, etc.

> Tu respuesta:

**¿Prefieres una organizacion plana o jerarquica?**
- [ ] Plana: todos los articulos al mismo nivel, navegacion por links
- [ ] Jerarquica: carpetas/subcarpetas por categoria
- [ ] Mixta: carpetas de alto nivel, links internos para detalle

> Tu respuesta:

---

## 7. Escala y horizonte

**¿Cuantas paginas wiki estimas a largo plazo?**
- [ ] Pequeña (<50 paginas): tema especifico o proyecto acotado
- [ ] Mediana (50-200 paginas): dominio completo
- [ ] Grande (200+ paginas): base de conocimiento amplia

**¿Horizonte de uso?**
- [ ] Corto plazo (proyecto / periodo especifico)
- [ ] Largo plazo (referencia permanente y creciente)

> Tu respuesta:

---

## 8. Operaciones automaticas

**¿Que operaciones quieres que Claude ejecute sin que se lo pidas?**
- [ ] Al ingresar una fuente: generar resumen + actualizar paginas relacionadas
- [ ] Lint periodico: detectar contradicciones, paginas huerfanas, afirmaciones desactualizadas
- [ ] Sugerir conexiones entre fuentes nuevas y conocimiento existente
- [ ] Generar reporte semanal de lo aprendido
- [ ] Nada automatico — solo cuando lo pida

> Tu respuesta:

---

## 9. Contexto adicional

**¿Hay algo especifico de tu dominio que Claude deba saber para indexar bien el conocimiento?**

Ejemplo: terminologia propia, personas clave, proyectos de referencia, convenciones de nombres.

> Tu respuesta:

**¿Existe ya algun sistema de notas que quieras migrar o conectar?**
(Notion, Obsidian, Roam, carpetas de markdown, etc.)

> Tu respuesta:

---

## Siguiente paso

Con tus respuestas, Claude va a:
1. Generar el `CLAUDE.md` definitivo (schema completo)
2. Crear las categorias base en `wiki/`
3. Definir los workflows de ingest / query / lint
4. Evaluar si se necesita codigo o alcanza con Claude Code + Opus
