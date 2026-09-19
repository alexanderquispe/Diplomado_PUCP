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

Dos notebooks, en este orden.

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

> Los resultados cambian cada vez que se corre: son avisos de empleo reales,
> publicados hoy. Eso es parte de la gracia — y la razón por la que el notebook
> insiste en guardar apenas se extrae.

## Para dar la clase

Pon `HEADLESS = False` en la celda de configuración para que los participantes
**vean la ventana de Chrome navegando sola**. Es el momento que engancha.
Déjalo en `True` cuando corras muchas páginas.
