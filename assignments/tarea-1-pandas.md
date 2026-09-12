# Tarea 1 · Pandas

**Se deja:** miércoles 16 de setiembre · **Vence:** lunes 22 de setiembre, 11:59 pm
**Peso:** 33.3%

## Qué se entrega

Un notebook `tarea1_<apellido>.ipynb` subido a tu repositorio de GitHub.

## El trabajo

Elige **un dataset de tu propia área** (salud, educación, presupuesto,
justicia, ambiente, lo que corresponda a tu trabajo). Debe tener al menos
500 filas y 5 columnas. Fuentes posibles: [datosabiertos.gob.pe](https://www.datosabiertos.gob.pe),
INEI, el portal de tu institución.

Si no encuentras uno, usa el de dengue de la sesión 3 pero **con otra pregunta**
que la que vimos en clase.

### 1. Cargar y describir (4 puntos)

- Carga el archivo y muestra sus dimensiones
- Explica en dos líneas qué es cada fila del dataset
- Muestra tipos de datos y cuenta los nulos

### 2. Limpiar (5 puntos)

Documenta y resuelve al menos **tres** problemas reales de tus datos. Por ejemplo:

- columnas con nombres impracticables
- números guardados como texto
- nulos que significan cero, o nulos que significan "no sabemos"
- códigos que perdieron el cero de la izquierda
- categorías escritas de varias formas (`LIMA`, `Lima`, `lima `)
- duplicados

Por cada uno: **muestra el problema**, arréglalo, **muestra que quedó arreglado**.

### 3. Preguntar (5 puntos)

Formula **tres preguntas** que se puedan responder con tus datos y respóndelas
con `groupby`, `pivot_table` o filtros. Cada respuesta es una tabla.

Las preguntas deben ser sustantivas ("¿qué distritos concentran el gasto?"),
no técnicas ("¿cuál es el promedio de la columna 3?").

### 4. Cruzar (4 puntos)

Trae una **segunda fuente** y crúzala con la primera.

- Explica cuál es la llave del cruce
- **Reporta cuántas filas no cruzaron y por qué**
- Produce una tabla que solo sea posible con las dos fuentes juntas

### 5. Exportar (2 puntos)

Un archivo Excel con tus tres tablas de resultados en hojas separadas.

## Uso de agentes de código

**Permitido.** Claude Code, Copilot, ChatGPT: úsalos.

**Obligatorio:** debajo de cada bloque de código, una celda de texto que explique
en tus palabras qué hace y por qué elegiste ese camino. Bloque sin explicación,
o explicación que no corresponde al código, **vale cero**.

## Cómo se califica

| | |
|---|---|
| Las secciones 1 a 5 | 20 puntos |
| Las explicaciones corresponden al código | requisito, no puntaje |
| El notebook corre de principio a fin sin errores | requisito |

Antes de entregar: *Kernel → Restart & Run All*. Si se cae, no está listo.
