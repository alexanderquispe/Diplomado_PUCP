"""Dashboard de dengue y capacidad de respuesta en salud.

Correr en local:
    uv run streamlit run app.py
"""

import geopandas as gpd
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------- configuracion
st.set_page_config(page_title="Dengue en el Perú", page_icon="🦟", layout="wide")


# ------------------------------------------------------------------ carga datos
# @st.cache_data guarda el resultado: sin esto, el archivo se lee otra vez
# cada vez que alguien mueve un filtro y la app va lentísima.
@st.cache_data
def cargar():
    datos = pd.read_csv("datos.csv", dtype={"ubigeo": str})
    formas = gpd.read_file("distritos.geojson")
    return datos, formas


datos, formas = cargar()

# ----------------------------------------------------------------------- filtros
st.sidebar.header("Filtros")

departamentos = sorted(datos["departamento"].unique())
elegidos = st.sidebar.multiselect(
    "Departamento", departamentos, default=departamentos[:5]
)

minimo = st.sidebar.slider(
    "Casos mínimos por distrito", 0, int(datos["casos_dengue"].max()), 0, step=50
)

filtrado = datos[
    datos["departamento"].isin(elegidos) & (datos["casos_dengue"] >= minimo)
]

# ------------------------------------------------------------------------ titulo
st.title("🦟 Dengue y capacidad de respuesta en salud")
st.caption("Casos 2015-2021 por distrito · Fuente: MINSA e INEI")

if filtrado.empty:
    st.warning("No hay distritos que cumplan los filtros. Ajusta la selección.")
    st.stop()

# ---------------------------------------------------------------------- metricas
c1, c2, c3, c4 = st.columns(4)
c1.metric("Distritos", f"{len(filtrado):,}")
c2.metric("Casos totales", f"{int(filtrado['casos_dengue'].sum()):,}")
c3.metric("Establecimientos", f"{int(filtrado['n_establecimientos'].sum()):,}")
c4.metric("Casos por establecimiento", f"{filtrado['casos_dengue'].sum() / max(filtrado['n_establecimientos'].sum(), 1):.1f}")

st.divider()

# ---------------------------------------------------------------------- graficos
izq, der = st.columns(2)

with izq:
    st.subheader("Casos por departamento")
    por_depto = (
        filtrado.groupby("departamento")["casos_dengue"].sum().reset_index()
        .sort_values("casos_dengue")
    )
    fig = px.bar(
        por_depto, x="casos_dengue", y="departamento", orientation="h",
        color="casos_dengue", color_continuous_scale="Reds",
        labels={"casos_dengue": "Casos", "departamento": ""},
    )
    fig.update_layout(coloraxis_showscale=False, template="plotly_white", height=400)
    st.plotly_chart(fig, width="stretch")

with der:
    st.subheader("Casos vs. establecimientos de salud")
    fig = px.scatter(
        filtrado[filtrado["casos_dengue"] > 0],
        x="n_establecimientos", y="casos_dengue",
        color="departamento", hover_name="distrito", log_y=True,
        labels={"n_establecimientos": "Establecimientos", "casos_dengue": "Casos (log)"},
    )
    fig.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig, width="stretch")

# -------------------------------------------------------------------------- mapa
st.subheader("Mapa distrital")

formas_filtradas = formas[formas["ubigeo"].isin(filtrado["ubigeo"])]

fig = px.choropleth_map(
    formas_filtradas,
    geojson=formas_filtradas.geometry,
    locations=formas_filtradas.index,
    color="casos_dengue",
    color_continuous_scale="YlOrRd",
    map_style="carto-positron",
    zoom=4.5,
    center={"lat": -9.2, "lon": -75.0},
    opacity=0.7,
    hover_name="distrito",
    hover_data={"departamento": True, "casos_dengue": True, "n_establecimientos": True},
    height=550,
)
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, width="stretch")

# ------------------------------------------------------------------------- tabla
st.subheader("Distritos con mayor presión sobre el sistema de salud")

tabla = filtrado.copy()
tabla["casos_por_establecimiento"] = (
    tabla["casos_dengue"] / tabla["n_establecimientos"].replace(0, pd.NA)
).round(1)

st.dataframe(
    tabla.sort_values("casos_por_establecimiento", ascending=False)[
        ["departamento", "provincia", "distrito", "casos_dengue",
         "n_establecimientos", "casos_por_establecimiento"]
    ].head(20),
    width="stretch",
    hide_index=True,
)

st.download_button(
    "Descargar datos filtrados (CSV)",
    tabla.to_csv(index=False).encode("utf-8"),
    "dengue_filtrado.csv",
    "text/csv",
)
