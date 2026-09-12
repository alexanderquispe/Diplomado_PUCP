# Tarea 2 · Extraer datos

**Se deja:** miércoles 23 de setiembre · **Vence:** lunes 29 de setiembre, 11:59 pm
**Peso:** 33.3%

## Qué se entrega

Un notebook `tarea2_<apellido>.ipynb` en tu repositorio.

## El trabajo

Consigue datos que **no te dio nadie**: sácalos de la web o de una API.

### 1. Traer datos de afuera (8 puntos)

Elige **uno** de los dos caminos:

**Camino A — una página web.** Extrae una tabla con `pd.read_html` o
`BeautifulSoup`. Al menos 30 filas.

**Camino B — una API pública.** Banco Mundial, INEI, MINSA, Reniec, BCRP,
o cualquier API abierta. Al menos 30 registros.

Documenta:
- la URL y qué información contiene
- el código de estado de la respuesta
- cómo identificaste dónde estaba el dato (si es scraping, qué viste al inspeccionar)

**Guarda lo extraído en un CSV** apenas lo obtengas.

### 2. Limpiar lo extraído (4 puntos)

Lo que viene de la web siempre llega sucio: números con separadores raros,
encabezados en varios niveles, filas de totales, espacios invisibles.
Muestra el antes y el después.

### 3. Cruzarlo con algo tuyo (4 puntos)

Únelo con el dataset de tu Tarea 1 y produce un indicador que antes no existía
—una tasa, un per cápita, una razón entre dos fuentes.

Reporta qué no cruzó y por qué.

### 4. Una columna generada con IA (4 puntos)

Toma una columna de **texto libre** (una descripción, un nombre de proyecto, un
comentario, una dirección) y usa la API de Claude para convertirla en datos:
clasifícala en categorías, o extrae campos en JSON.

- Prueba primero con 3 filas y muestra ese resultado
- Corre luego sobre al menos 20 filas
- **Revisa a mano 5 resultados y di si el modelo acertó**

Si no tienes texto libre en tus datos, usa `reclamos_salud.csv` de la sesión 5.

> La clave va en `.env`, nunca dentro del notebook. Si subes tu clave a GitHub,
> la tarea se califica sobre cero: es un error de seguridad, no de código.

## Uso de agentes de código

Permitido, con la misma regla de siempre: **cada bloque lleva su celda de
explicación**. Sin ella, no se califica.

## Cómo se califica

| | |
|---|---|
| Secciones 1 a 4 | 20 puntos |
| Clave de API expuesta en el repositorio | anula la tarea |
| El notebook corre de principio a fin | requisito |
