# Sesión 03 · Pandas de principio a fin

**3 h · mié 16 set**

## Entorno

```bash
uv sync
uv run jupyter lab
```

## Contenido

Cierra todo pandas en una sesión. Se parte en dos notebooks con una pausa al medio.

**Notebooks**
- `01a_leer_limpiar.ipynb` — leer archivos, inspeccionar, renombrar, tipos, nulos, ubigeo, duplicados, filtros, `loc`/`iloc`, columnas nuevas
- `01b_agrupar_cruzar.ipynb` — `groupby`, `agg`, `pivot_table`, `merge`, `concat`, exportar a Excel

**Pregunta que responde:** ¿qué distritos tienen muchos casos de dengue y pocos establecimientos de salud?

**Genera:** `dengue_limpio.csv`, `tabla_distritos.csv`, `reporte_dengue.xlsx`

**Al cierre:** primera demostración de Claude Code (20 min) y se deja la Tarea 1.

## Datos

```bash
uv run python scripts/fetch_data.py 03-pandas
```
