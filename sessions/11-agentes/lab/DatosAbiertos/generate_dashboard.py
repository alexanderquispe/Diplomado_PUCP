"""Generate dashboard.py with embedded data (skill datosabiertos-dashboard)."""
from __future__ import annotations

import io
import json
import pprint
from datetime import datetime

import pandas as pd
import requests

from catalog_curated import CURATED
from mcp_datosabiertos_server import build_health_edu_snapshot

PERIOD_YEARS = 3
MAX_EDU_SAMPLE = 500


def fetch_education_last_years(years: int = PERIOD_YEARS) -> tuple[list[dict], dict, list[int]]:
    entry = CURATED["education_enrollment"]
    response = requests.get(
        entry["download_url"],
        headers={"User-Agent": "Mozilla/5.0 (compatible; DatosAbiertos-Lab/1.0)"},
        timeout=120,
    )
    response.raise_for_status()
    df = pd.read_csv(io.BytesIO(response.content), encoding=entry["encoding"], low_memory=False)
    year_col = next(c for c in df.columns if "Matr" in c)
    selected_years = sorted(df[year_col].dropna().unique())[-years:]
    filtered = df[df[year_col].isin(selected_years)].copy()
    per_year = max(1, MAX_EDU_SAMPLE // len(selected_years))
    parts = []
    for year in selected_years:
        subset = filtered[filtered[year_col] == year]
        n = min(len(subset), per_year)
        parts.append(subset.sample(n=n, random_state=42) if len(subset) > n else subset)
    sample = pd.concat(parts).head(MAX_EDU_SAMPLE)
    records = json.loads(sample.to_json(orient="records", force_ascii=False))
    meta = {
        "package_id": entry["package_id"],
        "title": entry["title"],
        "total": len(filtered),
        "year_range": f"{int(selected_years[0])}-{int(selected_years[-1])}",
        "years": [int(y) for y in selected_years],
    }
    return records, meta, [int(y) for y in selected_years]


def main() -> None:
    snap = build_health_edu_snapshot(limit_per_resource=500)
    health_ds = snap["datasets"]["health_establishments"]
    health_records = health_ds["records"]
    edu_records, edu_meta, years = fetch_education_last_years(PERIOD_YEARS)

    fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    year_label = edu_meta["year_range"]

    snap_out = {
        "fetched_at": fetched_at,
        "period_years": PERIOD_YEARS,
        "year_range": year_label,
        "datasets": {
            "health_establishments": health_ds,
            "education_enrollment": {
                "package_id": CURATED["education_enrollment"]["package_id"],
                "title": CURATED["education_enrollment"]["title"],
                "description": CURATED["education_enrollment"]["description"],
                "resource_id": CURATED["education_enrollment"]["resource_id"],
                "records": edu_records,
                "total": edu_meta["total"],
                "source": "csv_download_filtered_3y",
                "year_filter": years,
            },
        },
        "errors": snap.get("errors", {}),
    }
    with open("datosabiertos_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(snap_out, f, ensure_ascii=False, indent=2)

    health_meta = {
        "package_id": health_ds["package_id"],
        "title": health_ds["title"],
        "total": health_ds["total"],
    }

    dashboard = f'''"""
Panel Datos Abiertos — Salud y Educación (Perú)
Fuente: datosabiertos.gob.pe | Generado por skill datosabiertos-dashboard
Período educación: últimos {PERIOD_YEARS} años ({year_label})
"""
from collections import Counter

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Panel Datos Abiertos — Perú",
    page_icon="🇵🇪",
    layout="wide",
)

BCRP_RED = "#C8102E"
BCRP_NAVY = "#003087"

FETCHED_AT = {json.dumps(fetched_at)}
PERIOD_LABEL = {json.dumps(f"{year_label} ({PERIOD_YEARS} años)")}
HEALTH_RECORDS: list[dict] = {pprint.pformat(health_records, sort_dicts=False, width=100)}
EDU_RECORDS: list[dict] = {pprint.pformat(edu_records, sort_dicts=False, width=100)}
HEALTH_META = {pprint.pformat(health_meta, sort_dicts=False, width=100)}
EDU_META = {pprint.pformat(edu_meta, sort_dicts=False, width=100)}


def _pick_column(columns: list[str], candidates: list[str]) -> str | None:
    norm = {{c.lower().replace("\\n", " "): c for c in columns}}
    for cand in candidates:
        key = cand.lower().replace("\\n", " ")
        if key in norm:
            return norm[key]
    for col in columns:
        cl = col.lower()
        for cand in candidates:
            if cand.lower() in cl:
                return col
    return None


def _count_by(records: list[dict], col: str | None, top_n: int = 15) -> tuple[list, list]:
    if not col or not records:
        return [], []
    ctr = Counter(str(r.get(col, "")).strip() for r in records if r.get(col))
    ctr.pop("", None)
    items = ctr.most_common(top_n)
    return [k for k, _ in items], [v for _, v in items]


st.title("🇵🇪 Panel Datos Abiertos — Salud y Educación (Perú)")
st.caption(
    f"Fuente: datosabiertos.gob.pe · Actualizado: {{FETCHED_AT}} · Matrícula: {{PERIOD_LABEL}}"
)
st.divider()

if not HEALTH_RECORDS and not EDU_RECORDS:
    st.error(
        "No hay datos cargados. Ejecute el skill datosabiertos-dashboard o "
        "python fetch_snapshot.py para generar datosabiertos_snapshot.json."
    )
    st.stop()

hcols = list(HEALTH_RECORDS[0].keys()) if HEALTH_RECORDS else []
ecols = list(EDU_RECORDS[0].keys()) if EDU_RECORDS else []
dept_col = _pick_column(hcols, ["Departamento", "DEPARTAMENTO"])
tipo_col = _pick_column(hcols, ["Tipo", "TIPO", "Clasificación", "Clasificacion"])
year_col = _pick_column(ecols, ["Año Matrícula", "Ano Matricula"])
region_col = _pick_column(ecols, ["Departamento\\nColegio", "Departamento Colegio"])
gender_col = _pick_column(ecols, ["Género", "Genero"])

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Establecimientos (muestra)", len(HEALTH_RECORDS))
c2.metric("Total IPRESS (portal)", f"{{HEALTH_META.get('total', 0):,}}")
depts_h = len({{r.get(dept_col) for r in HEALTH_RECORDS if dept_col and r.get(dept_col)}})
c3.metric("Departamentos (muestra)", depts_h)
c4.metric("Registros educación (muestra)", len(EDU_RECORDS))
c5.metric("Total matrícula (3 años)", f"{{EDU_META.get('total', 0):,}}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Establecimientos de salud por departamento")
    if HEALTH_RECORDS and dept_col:
        labels, values = _count_by(HEALTH_RECORDS, dept_col, 15)
        fig = go.Figure(go.Bar(x=labels, y=values, marker_color=BCRP_NAVY))
        fig.update_layout(
            yaxis_title="Cantidad",
            xaxis_tickangle=-45,
            plot_bgcolor="white",
            height=380,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No disponible: establecimientos por departamento")

with col2:
    st.subheader("Establecimientos por tipo")
    if HEALTH_RECORDS and tipo_col:
        labels, values = _count_by(HEALTH_RECORDS, tipo_col, 12)
        fig2 = go.Figure(go.Bar(x=labels, y=values, marker_color=BCRP_RED))
        fig2.update_layout(
            yaxis_title="Cantidad",
            xaxis_tickangle=-45,
            plot_bgcolor="white",
            height=380,
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No disponible: establecimientos por tipo")

col3, col4 = st.columns(2)

with col3:
    st.subheader(f"Matrícula por año ({{PERIOD_LABEL}})")
    if EDU_RECORDS and year_col:
        labels, values = _count_by(EDU_RECORDS, year_col, 20)
        labels_sorted = sorted(labels, key=lambda x: str(x))
        values_sorted = [values[labels.index(l)] for l in labels_sorted]
        fig3 = go.Figure(
            go.Scatter(
                x=labels_sorted,
                y=values_sorted,
                mode="lines+markers",
                line=dict(color=BCRP_NAVY, width=2),
            )
        )
        fig3.update_layout(
            yaxis_title="Registros (muestra)",
            xaxis_tickangle=-45,
            plot_bgcolor="white",
            height=380,
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("No disponible: matrícula por año")

with col4:
    st.subheader("Matrícula por departamento (colegio)")
    if EDU_RECORDS and region_col:
        labels, values = _count_by(EDU_RECORDS, region_col, 12)
        fig4 = go.Figure(go.Bar(x=labels, y=values, marker_color=BCRP_NAVY))
        fig4.update_layout(
            yaxis_title="Registros (muestra)",
            xaxis_tickangle=-45,
            plot_bgcolor="white",
            height=380,
            showlegend=False,
        )
        st.plotly_chart(fig4, use_container_width=True)
        if gender_col:
            g_labels, g_vals = _count_by(EDU_RECORDS, gender_col, 5)
            parts = [f"{{a}}: {{b}}" for a, b in zip(g_labels, g_vals)]
            st.caption("Género (muestra): " + ", ".join(parts))
    else:
        st.warning("No disponible: matrícula por departamento")

st.subheader("Fuentes institucionales")
st.markdown(
    f"- **Salud:** [{{HEALTH_META.get('title', 'IPRESS')}}](https://www.datosabiertos.gob.pe/dataset/{{HEALTH_META.get('package_id', '')}}) "
    f"(`{{HEALTH_META.get('package_id', '')}}`) — {{HEALTH_META.get('total', 0):,}} registros en el portal.\\n"
    f"- **Educación:** [{{EDU_META.get('title', 'Matrícula')}}](https://www.datosabiertos.gob.pe/dataset/{{EDU_META.get('package_id', '')}}) "
    f"(`{{EDU_META.get('package_id', '')}}`) — {{EDU_META.get('total', 0):,}} registros en el período {{PERIOD_LABEL}}."
)

if HEALTH_RECORDS:
    with st.expander("Vista previa — salud (5 filas)"):
        st.dataframe(pd.DataFrame(HEALTH_RECORDS).head(), use_container_width=True)
if EDU_RECORDS:
    with st.expander("Vista previa — educación (5 filas)"):
        st.dataframe(pd.DataFrame(EDU_RECORDS).head(), use_container_width=True)

st.divider()
st.caption(
    "Recursos: IPRESS 7cf96151-5ddf-4281-90ba-b2b0407447ab · "
    "Matrícula e276da3f-a009-4547-9e76-c814e14fc574 · Período matrícula: 3 años"
)
'''

    with open("dashboard.py", "w", encoding="utf-8") as f:
        f.write(dashboard)

    print("Generated dashboard.py")
    print(f"Health records: {len(health_records)} (portal total: {health_ds['total']})")
    print(f"Edu records: {len(edu_records)} (3-year total: {edu_meta['total']}, years: {years})")
    print(f"Fetched: {fetched_at}")


if __name__ == "__main__":
    main()
