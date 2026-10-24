# Sesión 04 · De la web al DataFrame

**1.5 h · sáb 19 set**

## Entorno

Con `uv` (lo que usa el resto del curso):

```bash
uv sync --group scraping
uv run jupyter lab
```

Con Anaconda, `pip` o cualquier otro entorno:

```bash
pip install -r requirements.txt
```

El notebook de Selenium también trae una celda `%pip install` al inicio, por si
lo abres en un entorno suelto (Colab, Anaconda base) y no quieres instalar nada
desde la terminal.

**Requisito:** tener **Google Chrome instalado**. El driver lo descarga y
actualiza Selenium solo — no hay que bajar `chromedriver` a mano.

## Contenido

Los notebooks, en este orden.

### `02_web_al_dataframe.ipynb` — la página ya trae el dato

`requests`, códigos de estado, `pd.read_html`, limpieza de tablas web,
`BeautifulSoup` (`find`, `find_all`, `select`).

**Pregunta que responde:** ajustado por población, ¿qué departamento tiene la
mayor incidencia de dengue? (Cambia la respuesta: no es Piura, es Madre de Dios.)

**Genera:** `tasas_departamento.csv`

### `03_selenium_bumeran.ipynb` — la página se arma sola

Caso real sobre [bumeran.com.pe](https://www.bumeran.com.pe): un sitio donde
`requests` devuelve el HTML **vacío de ofertas**, porque las dibuja JavaScript.

Cubre: comprobar que Selenium hace falta, leer el `robots.txt`, abrir Chrome
desde Python, `WebDriverWait` frente a `time.sleep`, por qué no usar clases CSS
generadas, paginación, pausas entre pedidos, y `try / finally` para cerrar el
navegador siempre.

**Pregunta que responde:** ¿qué empleos se ofrecen hoy en el Perú, dónde, y
cuántos son remotos? (Al correrlo: de 60 ofertas de analista de datos, **44 son
presenciales y solo 1 remota**.)

**Genera:** `empleos_bumeran.csv`, `empleos_comparacion.csv`

### `04_selenium_paso_a_paso.ipynb` — la versión lenta

El notebook anterior extrae 60 ofertas en una celda: muestra el resultado, pero
va rápido. Este hace lo contrario — **saca un dato a la vez** y muestra qué
devuelve cada instrucción, hasta armar la función al final.

Mismo sitio, mismo objetivo, otro ritmo. Sirve para la parte de la clase en que
hay que entender *cómo* se extrae, no solo *que* se extrae.

Recorrido: `find_element` frente a `find_elements` · las formas de `By` ·
qué es un WebElement · radiografía de una tarjeta · sacar el puesto, la fecha,
la empresa, la ubicación, la modalidad y el enlace **uno por uno** · armar el
diccionario a mano · repetirlo con la segunda tarjeta · y recién entonces la
función y el bucle.

**El momento importante:** los `<h3>` parecen estar siempre en el mismo orden,
pero 7 de 20 tarjetas traen uno extra con la calificación de la empresa, así que
`h3[2]` unas veces es la ubicación y otras un `3.1`. El notebook lo descubre
comparando seis tarjetas y enseña la regla: **buscar por contenido cuando la
posición puede moverse**. Un índice equivocado no da error — guarda el dato
incorrecto en silencio.

Abre el navegador **visible** por defecto.

### `06_empleos_analista_datos.ipynb` — la base de datos de analistas

Recorre 4 búsquedas (*analista de datos*, *data analyst*, *analista bi*,
*business intelligence*) y lee **cada tarjeta del listado**: no entra a cada
aviso, porque la tarjeta ya trae la descripción completa. Arma una base con
**una fila por aviso**: puesto, empresa, calificación, modalidad, distrito,
departamento, antigüedad, descripción y qué herramientas pide (SQL, Python,
Power BI…).

**Pregunta que responde:** ¿dónde están hoy los empleos de analista de datos
en el Perú, en qué modalidad, y qué herramientas piden?

Cubre: reintentar cuando Bumeran devuelve la página vacía, leer cada dato por
el **nombre de su ícono** (`following::h3[1]`) en vez de por su posición, y
detectar herramientas en el texto con expresiones regulares.

**Genera:** `empleos_analista_datos_<fecha>.csv`. Toma **un par de minutos**.

> Los resultados cambian cada vez que se corre: son avisos de empleo reales,
> publicados hoy. Eso es parte de la gracia — y la razón por la que el notebook
> insiste en guardar apenas se extrae.

## Para dar la clase

Pon `HEADLESS = False` en la celda de configuración para que los participantes
**vean la ventana de Chrome navegando sola**. Es el momento que engancha.
Déjalo en `True` cuando corras muchas páginas.
