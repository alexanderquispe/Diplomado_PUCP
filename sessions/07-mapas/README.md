# Sesión 07 · Mapas del Perú

**2 h · mié 30 set**

## Entorno

```bash
uv sync --group mapas
uv run jupyter lab
```

## Contenido

El paso difícil no es dibujar: es cruzar los datos con las fronteras por ubigeo.

**Notebook:** `05_mapas.ipynb`

`geopandas`, CRS, coropletas estáticas con cortes por cuantiles, `folium` (mapa base, marcadores, `Choropleth`, `GeoJsonTooltip`, `MarkerCluster`, `HeatMap`).

**Genera:** `mapa_dengue_norte.html`, `distritos_con_datos.csv`

> Los mapas de Folium están guardados sin output porque pesan varios MB.
> Se generan al correr la celda.

Se deja la Tarea 3 (trabajo final).

## Datos

```bash
uv run python scripts/fetch_data.py 07-mapas
```
