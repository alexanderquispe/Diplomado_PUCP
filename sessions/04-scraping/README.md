# Sesión 04 · De la web al DataFrame

**1.5 h · sáb 19 set**

## Entorno

```bash
uv sync --group scraping
uv run jupyter lab
```

## Contenido

Extraer datos que no están en ningún CSV.

**Notebook:** `02_web_al_dataframe.ipynb`

`requests`, códigos de estado, `pd.read_html`, limpieza de tablas web, `BeautifulSoup` (`find`, `find_all`, `select`), y cuándo hace falta Selenium.

**Pregunta que responde:** ajustado por población, ¿qué departamento tiene la mayor incidencia de dengue? (Cambia la respuesta: no es Piura, es Madre de Dios.)

**Genera:** `tasas_departamento.csv`
