# Handoff — DatosAbiertos LAB11

**Date:** 2026-05-26  
**Location:** `Labs/Python_Notebooks/LAB11/DatosAbiertos/`  
**Status:** Implementation complete per plan; Streamlit **stopped** (was running on port 8501).

---

## What was delivered

A **Cursor-only** lab (parallel to `Skills_Claude/` BCRP) that uses **datosabiertos.gob.pe** (CKAN/DKAN) via a local MCP server and a Cursor skill to build a health + education Streamlit dashboard.

| Item | Path | Notes |
|------|------|--------|
| MCP server | `mcp_datosabiertos_server.py` | FastMCP name: `datosabiertos` |
| Curated catalog | `catalog_curated.py` | Two datasets with real resource UUIDs |
| Cursor MCP config | `.cursor/mcp.json` | stdio → `.venv/Scripts/python.exe` |
| Cursor skill | `.cursor/skills/datosabiertos-dashboard/SKILL.md` | `disable-model-invocation: true` |
| Dashboard | `dashboard.py` | Loads `datosabiertos_snapshot.json` if embedded data empty |
| Offline fetch | `fetch_snapshot.py` | Writes gitignored `datosabiertos_snapshot.json` |
| Discovery helper | `discover_resources.py` | Validates catalog against live API |
| Setup | `setup.ps1`, `requirements.txt`, `.gitignore` | venv created and deps installed |
| Docs | `README.md` | Student-facing setup and troubleshooting |

**Not created (by design):** `.claude/` — this lab is Cursor-only.

---

## Where things were left

### Completed and verified

1. **Virtual environment** — `.venv/` exists; dependencies installed (`mcp`, `requests`, `pandas`, `streamlit`, `plotly`).
2. **MCP tools** — All five tools implemented and smoke-tested:
   - `search_datasets`, `get_dataset`, `datastore_search`, `list_organizations`, `get_health_edu_snapshot`
3. **Snapshot fetch** — `fetch_snapshot.py` succeeded:
   - `health_establishments`: 200 records (portal total 20,819)
   - `education_enrollment`: 200 records (portal total 163,199)
4. **Local cache** — `datosabiertos_snapshot.json` generated (gitignored).
5. **Dashboard** — `dashboard.py` runs; tested with snapshot fallback.
6. **Streamlit** — Was started in background at **http://localhost:8501**; **stopped on request** (PID 4084). Port 8501 should be free now.

### Curated datasets (final IDs)

| Key | Package | Resource ID | Source |
|-----|---------|-------------|--------|
| `health_establishments` | `minsa-ipress` | `7cf96151-5ddf-4281-90ba-b2b0407447ab` | CSV on datosabiertos.gob.pe (IPRESS.csv) |
| `education_enrollment` | `alumnos-matriculados` | `e276da3f-a009-4547-9e76-c814e14fc574` | CSV (Matriculados_2016_al_2022.csv) |

Original plan mentioned `establecimientos-de-salud`; that package name was **not** in `package_list`. **`minsa-ipress`** was used instead (MINSA IPRESS, same theme).

### API behavior discovered (important for next dev)

| Endpoint | Behavior |
|----------|----------|
| `package_list` | Works with `User-Agent` header |
| `package_show` | Works; `result` is often a **list** with one package dict |
| `package_search` | Returns **404** on this portal — MCP falls back to filtering `package_list` |
| `datastore_search` | Often returns HTML/500 — MCP **falls back to CSV download** from `catalog_curated.download_url` |

All HTTP calls use:

```python
User-Agent: Mozilla/5.0 (compatible; DatosAbiertos-Lab/1.0)
```

### Dashboard vs skill spec (small gap)

- **Skill spec:** Agent should **overwrite `dashboard.py`** with **embedded** Python lists (no runtime file load).
- **Current `dashboard.py`:** Template with empty embedded lists + **fallback** to `datosabiertos_snapshot.json` for local dev.
- **Next step for a full skill run:** Invoke skill in Cursor Agent so it embeds live data and launches Streamlit (that flow was not executed end-to-end in Agent mode—only manual/offline tests).

### Not committed to git (expected)

- `.venv/`
- `datosabiertos_snapshot.json`
- `__pycache__/`

---

## How to resume

```powershell
cd "C:\Users\Jean Pool\Documents\GitHub\Data-Science-Python\Labs\Python_Notebooks\LAB11\DatosAbiertos"

# If venv missing:
.\setup.ps1

# Refresh local data cache:
.\.venv\Scripts\python fetch_snapshot.py

# Run dashboard manually:
.\.venv\Scripts\streamlit run dashboard.py
# → http://localhost:8501

# Validate catalog:
.\.venv\Scripts\python discover_resources.py
```

**In Cursor:**

1. Open **`DatosAbiertos/`** as workspace root.
2. Enable MCP **`datosabiertos`** (Settings → MCP).
3. Agent chat: **“Use the datosabiertos-dashboard skill”**.

---

## Optional follow-ups (not done)

- [ ] Run full **Agent skill** once to regenerate `dashboard.py` with embedded records (no JSON fallback).
- [ ] Replace `use_container_width` with `width='stretch'` in `dashboard.py` (Streamlit deprecation warning).
- [ ] Add `datastore_search_sql` if portal exposes it (v1.1 in plan).
- [ ] Git commit of `DatosAbiertos/` source files (excluding `.venv` and snapshot JSON).

---

## Related project

| Lab | Folder | Data source | Agent |
|-----|--------|-------------|--------|
| BCRP macro | `Skills_Claude/` | estadisticas.bcrp.gob.pe | Claude Code + optional Cursor |
| Datos abiertos | `DatosAbiertos/` | datosabiertos.gob.pe | **Cursor only** |

---

## Plan file

Implementation followed `.cursor/plans/datosabiertos_mcp_lab_99f4e247.plan.md`. **Do not edit the plan file** unless updating the plan itself; this handoff is the living status doc for the folder.
