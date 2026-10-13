# Sesión 07 · Datos raster

## Entorno

```bash
uv sync --group raster
uv run jupyter lab
```

El grupo `raster` ya trae todo lo de `mapas` (geopandas, folium, matplotlib), así
que basta con ese.

## Contenido

### Clase

| Notebook | Enfoque |
|---|---|
| **`lecture/raster_aplicado.ipynb`** | **Recomendado.** Aplicado: luces nocturnas como proxy de actividad económica distrital, cruzadas con áreas mineras. Corre de punta a punta. |
| `lecture/GIS_v2.ipynb`, `lecture/GIS.ipynb` | Versión anterior, orientada a conceptos (CRS, formatos, geowombat). Escritos para Google Colab: usan rutas `/content/` y la librería `geowombat`, que no viene en el grupo `raster`. |
| `lecture/Tutorial.ipynb` | Material de apoyo. Tiene rutas de una computadora personal: hay que cambiarlas antes de correrlo. |

### Laboratorio

| Notebook | Estado |
|---|---|
| **`lab/RASTER_LAB.ipynb`** | **Recomendado.** Riesgo climático agrícola por distrito: sequía (temperatura máxima alta con poca lluvia) y heladas (temperatura mínima baja). Corre de punta a punta. |
| `lab/RASTER.ipynb` | Versión anterior. Cuatro celdas fallan: usan variables que el notebook nunca define (`out_meta`, `dept_stats`) y un raster que no está publicado (`peru_coverage_2022.tif`). |

Los `.png` de `lab/` son gráficos de referencia del laboratorio de precipitación.

## De qué trata `raster_aplicado.ipynb`

Construye una medida de actividad económica distrital desde imágenes satelitales,
porque en el Perú no existe PBI a nivel de distrito.

1. Abrir el raster VIIRS de luces nocturnas (2021, ~1 km)
2. Detectar los problemas del dato: 27 % de `NaN`, 98 % de píxeles en cero
3. **Zonal statistics**: pasar de píxeles a una fila por distrito
4. Validar el ranking contra lo que sabemos del país
5. Cruzar con un segundo raster de áreas mineras
6. Estimar si los distritos mineros concentran más actividad

Resultados que produce al ejecutarse:

- Los distritos más luminosos por km² son San Borja, Surquillo, Lince y San Isidro
- Las áreas mineras detectadas corresponden a Antapaccay, Toquepala, Cuajone,
  Cerro Verde, Antamina, Yanacocha y Las Bambas
- Los distritos mineros tienen ~1.3 log-puntos más luminosidad total, robusto a
  controles por área, precipitación y efectos fijos de departamento (t = 8.2)

Conceptos que quedan: `nodata`, `all_touched`, `mean` frente a `sum`, y por qué
las áreas no se calculan en EPSG:4326.

## Datos

**Clase.** `raster_aplicado.ipynb` descarga solo lo que necesita desde Hugging
Face (`hf_hub_download`). No hay paso previo.

**Laboratorio.** Los notebooks abren sus archivos por nombre (`Prec_raster.tif`),
así que tienen que estar en la carpeta `lab/`. Este comando los deja ahí:

```bash
uv run python scripts/fetch_data.py 07-raster
```

Son unos 43 MB: tres rasters (precipitación, temperatura máxima y mínima), el
shapefile de distritos y el de ríos. No se versionan.
