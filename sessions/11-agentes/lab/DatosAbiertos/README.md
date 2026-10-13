# DatosAbiertos — CKAN MCP + Cursor Skill (LAB11)

Cursor-only lab that connects **datosabiertos.gob.pe** (Plataforma Nacional de Datos Abiertos, CKAN/DKAN) to a Streamlit dashboard through a local MCP server and the **datosabiertos-dashboard** skill.

## Project structure

```
DatosAbiertos/
├── .cursor/
│   ├── mcp.json
│   └── skills/datosabiertos-dashboard/SKILL.md
├── catalog_curated.py          # Curated package + resource IDs
├── mcp_datosabiertos_server.py # FastMCP server
├── discover_resources.py       # Validate / find resource IDs
├── fetch_snapshot.py           # Offline snapshot → datosabiertos_snapshot.json
├── dashboard.py                # Streamlit app (skill overwrites embedded data)
├── requirements.txt
├── setup.ps1
└── .gitignore
```

## One-time setup

```powershell
cd Labs\Python_Notebooks\LAB11\DatosAbiertos
.\setup.ps1
.\.venv\Scripts\python discover_resources.py   # optional: verify catalog
.\.venv\Scripts\python fetch_snapshot.py       # optional: local JSON cache
```

## Daily usage (Cursor)

1. Open **`DatosAbiertos/`** as the workspace root (not the whole repo).
2. **Settings → MCP** → enable **`datosabiertos`**.
3. In Agent chat: **“Use the datosabiertos-dashboard skill”**.
4. Dashboard: http://localhost:8501

Manual Streamlit (uses `datosabiertos_snapshot.json` if present):

```powershell
.\.venv\Scripts\streamlit run dashboard.py
```

## How it works

```
User invokes datosabiertos-dashboard skill
        → Agent calls get_health_edu_snapshot(200) via MCP
        → mcp_datosabiertos_server.py → CKAN API + CSV fallback
        → Agent embeds records in dashboard.py
        → streamlit run dashboard.py (background)
```

## MCP tools

| Tool | Description |
|------|-------------|
| `search_datasets(q, rows, start, organization)` | Find datasets (`package_search` or `package_list` filter) |
| `get_dataset(name_or_id)` | Package metadata + resources |
| `datastore_search(resource_id, limit, ...)` | Query DataStore; CSV fallback for curated IDs |
| `list_organizations(rows)` | Publisher list |
| `get_health_edu_snapshot(limit)` | IPRESS + matrícula in one call |

## Curated datasets (health + education)

| Key | Package | Resource ID |
|-----|---------|-------------|
| health_establishments | `minsa-ipress` | `7cf96151-5ddf-4281-90ba-b2b0407447ab` |
| education_enrollment | `alumnos-matriculados` | `e276da3f-a009-4547-9e76-c814e14fc574` |

## CKAN API cheat sheet

Base: `https://www.datosabiertos.gob.pe/api/3/action/`

```
package_list
package_show?id=<package_name>
datastore/search.json?resource_id=<uuid>&limit=100
```

Universal DataStore pattern:

```
GET .../datastore_search?resource_id={uuid}&limit={n}&offset={n}
```

**Note:** Many resources are not loaded into DataStore; this lab uses **CSV download fallback** from `download_url` in `catalog_curated.py` when DataStore returns empty/HTML.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| MCP not listed | Open `DatosAbiertos/` as workspace; check `.cursor/mcp.json` |
| MCP connection failed | Output panel → **MCP Logs**; run `.\.venv\Scripts\python mcp_datosabiertos_server.py` |
| 418 / HTML from API | Server sends `User-Agent`; retry later |
| Empty dashboard | Run `fetch_snapshot.py` or invoke skill to refresh data |
| `package_search` 404 | Expected on this portal; search uses `package_list` filter |

## Dependencies

```
mcp[cli]>=1.0
requests>=2.31
pandas>=2.0
streamlit>=1.35
plotly>=5.20
```
