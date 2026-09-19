# Sesión 04 · De la web al DataFrame

**1.5 h · sáb 19 set**

## Entorno

```bash
uv sync --group scraping
uv run jupyter lab
```

Para el notebook de Selenium hace falta tener **Google Chrome instalado**.
El driver lo gestiona Selenium solo, no hay que descargar nada.

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
