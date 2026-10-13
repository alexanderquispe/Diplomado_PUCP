---
name: datosabiertos-dashboard
description: >-
  Builds and launches the Peru open-data Streamlit dashboard (health IPRESS +
  education enrollment) from datosabiertos.gob.pe via MCP. Use when the user asks
  for datosabiertos dashboard, panel datos abiertos, CKAN salud educación, or
  datosabiertos-dashboard skill.
disable-model-invocation: true
---

# datosabiertos-dashboard — Panel Salud y Educación

Fetch live data from the **datosabiertos** MCP server, embed parsed data in `dashboard.py`, and launch Streamlit.

## Steps

1. **Fetch data** — call `get_health_edu_snapshot(200)` on MCP server `datosabiertos`.
   Returns `health_establishments` and `education_enrollment` with `records`, `fields`, `total`, `chart_hints`.

2. **Parse records** — each dataset has `records: [{col: val, ...}, ...]`.
   - Skip rows where key grouping fields are null/empty.
   - Use `chart_hints` and inspect `fields` to find columns:
     - Health: `Departamento`, `Tipo` / `Clasificación`
     - Education: `Año Matrícula`, `Departamento\nColegio`, `Género`
   - For charts, aggregate with `Counter` or pandas `value_counts` (top 12–15 categories).

3. **Overwrite `dashboard.py`** — full file rewrite with:
   - Embedded `HEALTH_RECORDS`, `EDU_RECORDS` as Python lists of dicts (from snapshot, max 200 rows each).
   - Embedded `FETCHED_AT`, `HEALTH_META`, `EDU_META` dicts.
   - **No** runtime API or MCP calls in Streamlit.
   - Layout:
     - Title: `Panel Datos Abiertos — Salud y Educación (Perú)`
     - Subtitle: `Fuente: datosabiertos.gob.pe | Actualizado: <fetched_at>`
     - Row 1: barras por departamento (salud) | barras por tipo (salud)
     - Row 2: línea/barras matrícula por año | barras por departamento colegio
     - Row 3: markdown con enlaces a datasets + expanders con preview tabular
     - Footer metrics: totales muestra y totales portal
   - Colors: `#C8102E` (red), `#003087` (navy); `st.set_page_config(layout="wide")`; Spanish labels; x-axis 45°.

4. **Launch Streamlit** (background):

```powershell
.\.venv\Scripts\streamlit run dashboard.py
```

5. **Report** — tell the user: `Dashboard actualizado y lanzado en http://localhost:8501`

## Error handling

- If a dataset has `errors[key]` or empty `records`, show `st.warning("No disponible: <name>")` in that panel.
- If **all** datasets fail, write `dashboard.py` with only `st.error()` explaining the API is unreachable; still launch Streamlit.

## MCP tools reference

| Tool | Use |
|------|-----|
| `get_health_edu_snapshot(limit)` | Preferred for this skill |
| `datastore_search(resource_id, limit)` | Single resource query |
| `search_datasets(q)` | Discovery (falls back to package_list filter) |
| `get_dataset(name)` | Metadata and resource IDs |
| `list_organizations()` | Browse publishers |

## Notes

- DataStore API may return HTML errors; MCP falls back to CSV download for curated resources.
- Workspace root must be `DatosAbiertos/` so `.cursor/mcp.json` resolves paths.
