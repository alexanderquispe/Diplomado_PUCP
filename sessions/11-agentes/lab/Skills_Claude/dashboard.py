import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Peru Macro Dashboard 2023-2026",
    page_icon="🇵🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data embedded
DATA = {
    "inflation": [
        ("May.2023", 0.31786146413237),
        ("Jun.2023", -0.152769746155551),
        ("Jul.2023", 0.391066276983018),
        ("Ago.2023", 0.376132603479856),
        ("Sep.2023", 0.0164026333286269),
        ("Oct.2023", -0.322447443370826),
        ("Nov.2023", -0.163060842314584),
        ("Dic.2023", 0.405777961086682),
        ("Ene.2024", 0.0192113272793558),
        ("Feb.2024", 0.557510800936321),
        ("Mar.2024", 1.00938516188575),
        ("Abr.2024", -0.0516715997229469),
        ("May.2024", -0.0907064485030323),
        ("Jun.2024", 0.121741927959431),
        ("Jul.2024", 0.236268738691571),
        ("Ago.2024", 0.284170528141876),
        ("Sep.2024", -0.237560474773851),
        ("Oct.2024", -0.0931035230159262),
        ("Nov.2024", 0.0941530377317251),
        ("Dic.2024", 0.105667996950954),
        ("Ene.2025", -0.0933179134509413),
        ("Feb.2025", 0.188012094871704),
        ("Mar.2025", 0.810159321766145),
        ("Abr.2025", 0.31806633832046),
        ("May.2025", -0.0564746187563057),
        ("Jun.2025", 0.128679643778829),
        ("Jul.2025", 0.231431002364371),
        ("Ago.2025", -0.29025398690341),
        ("Sep.2025", 0.0111517897177685),
        ("Oct.2025", -0.0996274056654658),
        ("Nov.2025", 0.110781919406383),
        ("Dic.2025", 0.244108583947482),
        ("Ene.2026", 0.0957671016980487),
        ("Feb.2026", 0.693626297343638),
        ("Mar.2026", 2.37869353004195),
        ("Abr.2026", 0.5206244057768),
    ],
    "exchange_rate": [
        ("May.2023", 3.68870454545455),
        ("Jun.2023", 3.65104761904762),
        ("Jul.2023", 3.6013),
        ("Ago.2023", 3.69634090909091),
        ("Sep.2023", 3.72966666666667),
        ("Oct.2023", 3.84440909090909),
        ("Nov.2023", 3.76188095238095),
        ("Dic.2023", 3.73368421052632),
        ("Ene.2024", 3.73980952380952),
        ("Feb.2024", 3.82730952380952),
        ("Mar.2024", 3.70955263157895),
        ("Abr.2024", 3.71315909090909),
        ("May.2024", 3.73097727272727),
        ("Jun.2024", 3.78463157894737),
        ("Jul.2024", 3.7644),
        ("Ago.2024", 3.741325),
        ("Sep.2024", 3.76821428571429),
        ("Oct.2024", 3.75359090909091),
        ("Nov.2024", 3.77885),
        ("Dic.2024", 3.73489473684211),
        ("Ene.2025", 3.74775),
        ("Feb.2025", 3.6977),
        ("Mar.2025", 3.65259523809524),
        ("Abr.2025", 3.6997),
        ("May.2025", 3.66014285714286),
        ("Jun.2025", 3.60390476190476),
        ("Jul.2025", 3.5562),
        ("Ago.2025", 3.5432),
        ("Sep.2025", 3.50281818181818),
        ("Oct.2025", 3.41409090909091),
        ("Nov.2025", 3.37285),
        ("Dic.2025", 3.36673684210526),
        ("Ene.2026", 3.35675),
        ("Feb.2026", 3.356975),
        ("Mar.2026", 3.44677272727273),
        ("Abr.2026", 3.442675),
    ],
    "gdp": [
        ("May.2023", 174.205884177575),
        ("Jun.2023", 178.389612909719),
        ("Jul.2023", 175.55607284978),
        ("Ago.2023", 177.273544890054),
        ("Sep.2023", 178.226772279038),
        ("Oct.2023", 177.708044328767),
        ("Nov.2023", 179.544540628351),
        ("Dic.2023", 177.94208243702),
        ("Ene.2024", 178.791698564371),
        ("Feb.2024", 178.714605943273),
        ("Mar.2024", 180.331867541023),
        ("Abr.2024", 182.273289709686),
        ("May.2024", 183.960512446356),
        ("Jun.2024", 180.151783846905),
        ("Jul.2024", 183.142003459551),
        ("Ago.2024", 185.173621902032),
        ("Sep.2024", 184.332772760658),
        ("Oct.2024", 184.553940301195),
        ("Nov.2024", 187.895068452118),
        ("Dic.2024", 186.365603465107),
        ("Ene.2025", 186.649010773463),
        ("Feb.2025", 187.186990155126),
        ("Mar.2025", 186.174264324815),
        ("Abr.2025", 187.781277400429),
        ("May.2025", 188.71190559638),
        ("Jun.2025", 188.095716161878),
        ("Jul.2025", 190.23645687057),
        ("Ago.2025", 191.1008183768),
        ("Sep.2025", 191.867834864242),
        ("Oct.2025", 192.028747319219),
        ("Nov.2025", 190.919048081582),
        ("Dic.2025", 193.429031752229),
        ("Ene.2026", 194.060217842914),
        ("Feb.2026", 194.113128875084),
        ("Mar.2026", 191.625714318591),
    ],
    "interest_rate": [
        ("May.2023", 7.746),
        ("Jun.2023", 7.7164),
        ("Jul.2023", 7.7481),
        ("Ago.2023", 7.7452),
        ("Sep.2023", 7.6024),
        ("Oct.2023", 7.2814),
        ("Nov.2023", 7.0889),
        ("Dic.2023", 6.858),
        ("Ene.2024", 6.601),
        ("Feb.2024", 6.3599),
        ("Mar.2024", 6.2368),
        ("Abr.2024", 6.0761),
        ("May.2024", 5.8595),
        ("Jun.2024", 5.7409),
        ("Jul.2024", 5.7126),
        ("Ago.2024", 5.5272),
        ("Sep.2024", 5.3487),
        ("Oct.2024", 5.2319),
        ("Nov.2024", 5.0847),
        ("Dic.2024", 4.946),
        ("Ene.2025", 4.7349),
        ("Feb.2025", 4.7755),
        ("Mar.2025", 4.7203),
        ("Abr.2025", 4.7565),
        ("May.2025", 4.484),
        ("Jun.2025", 4.49889399603857),
        ("Jul.2025", 4.5),
        ("Ago.2025", 4.5079),
        ("Sep.2025", 4.3685),
        ("Oct.2025", 4.25),
        ("Nov.2025", 4.2478),
        ("Dic.2025", 4.2411),
        ("Ene.2026", 4.2276),
        ("Feb.2026", 4.2481),
        ("Mar.2026", 4.2473),
        ("Abr.2026", 4.246),
    ],
    "agricultural": [
        ("May.2023", 53.819229),
        ("Jun.2023", 79.242689),
        ("Jul.2023", 92.943356),
        ("Ago.2023", 70.249502),
        ("Sep.2023", 41.145149),
        ("Oct.2023", 30.883648),
        ("Nov.2023", 31.47137),
        ("Dic.2023", 30.552348),
        ("Ene.2024", 28.3691),
        ("Feb.2024", 32.273789),
        ("Mar.2024", 38.197939),
        ("Abr.2024", 43.780728),
        ("May.2024", 54.14509),
        ("Jun.2024", 76.175647),
        ("Jul.2024", 91.821119),
        ("Ago.2024", 61.94624),
        ("Sep.2024", 39.349489),
        ("Oct.2024", 28.753899),
        ("Nov.2024", 27.72641),
        ("Dic.2024", 27.909188),
        ("Ene.2025", 27.090628),
        ("Feb.2025", 31.219898),
        ("Mar.2025", 38.499157),
        ("Abr.2025", 42.647146),
        ("May.2025", 59.223137),
        ("Jun.2025", 71.912675),
        ("Jul.2025", 91.451297),
        ("Ago.2025", 55.466306),
        ("Sep.2025", 35.057846),
        ("Oct.2025", 27.804407),
        ("Nov.2025", 27.1682),
        ("Dic.2025", 31.313028),
        ("Ene.2026", 27.347146),
        ("Feb.2026", 30.77729),
        ("Mar.2026", 35.564098),
    ],
}

def list_to_df(data_list):
    df = pd.DataFrame(data_list, columns=["period", "value"])
    df["date"] = pd.to_datetime(df["period"], format="%b.%Y", errors='coerce')
    df = df.sort_values("date").reset_index(drop=True)
    return df

df_inflation = list_to_df(DATA["inflation"])
df_exchange = list_to_df(DATA["exchange_rate"])
df_gdp = list_to_df(DATA["gdp"])
df_interest = list_to_df(DATA["interest_rate"])
df_agricultural = list_to_df(DATA["agricultural"])

RED = "#C8102E"
NAVY = "#003087"
GREEN = "#2ecc71"
GOLD = "#f39c12"
CHART_HEIGHT = 400

st.sidebar.title("🇵🇪 Peru Macro Intelligence")
st.sidebar.markdown("**Period:** May 2023 – Apr 2026 (3 años)")
st.sidebar.markdown("**Source:** BCRP | Banco Central de Reserva del Perú")

show_trend = st.sidebar.checkbox("Show OLS trend line", value=True)
show_ma = st.sidebar.checkbox("Show 6-month moving average", value=True)

st.title("🇵🇪 Peru Macro Intelligence Dashboard (2023–2026)")
st.markdown("Real-time monitoring of Peru's key macroeconomic indicators")

st.subheader("📊 Current Snapshot")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    latest_infl = df_inflation["value"].iloc[-1]
    prev_12_infl = df_inflation["value"].iloc[-13] if len(df_inflation) > 12 else None
    delta_infl = latest_infl - (prev_12_infl if prev_12_infl else 0)
    st.metric("🔴 Inflation (IPC)", f"{latest_infl:.2f}%",
              delta=f"{delta_infl:+.2f}pp" if prev_12_infl else None)
    if latest_infl > 3:
        st.warning("⚠ Above BCRP target (1-3%)")

with col2:
    latest_exch = df_exchange["value"].iloc[-1]
    prev_exch = df_exchange["value"].iloc[-7] if len(df_exchange) > 6 else None
    delta_exch = latest_exch - (prev_exch if prev_exch else 0)
    st.metric("💱 Exchange Rate", f"S/ {latest_exch:.3f}",
              delta=f"{delta_exch:+.3f}" if prev_exch else None)

with col3:
    latest_gdp = df_gdp["value"].iloc[-1]
    prev_gdp = df_gdp["value"].iloc[-12] if len(df_gdp) > 11 else None
    delta_gdp = latest_gdp - (prev_gdp if prev_gdp else 0)
    st.metric("📈 GDP Index", f"{latest_gdp:.1f}",
              delta=f"{delta_gdp:+.1f}" if prev_gdp else None)

with col4:
    latest_rate = df_interest["value"].iloc[-1]
    prev_rate = df_interest["value"].iloc[-12] if len(df_interest) > 11 else None
    delta_rate = latest_rate - (prev_rate if prev_rate else 0)
    st.metric("🏦 Interest Rate", f"{latest_rate:.2f}%",
              delta=f"{delta_rate:+.2f}pp" if prev_rate else None,
              delta_color="inverse" if delta_rate > 0 else "normal")

with col5:
    latest_agr = df_agricultural["value"].iloc[-1]
    prev_agr = df_agricultural["value"].iloc[-12] if len(df_agricultural) > 11 else None
    delta_agr = latest_agr - (prev_agr if prev_agr else 0)
    st.metric("🍊 Agr. Production", f"{latest_agr:.0f}k tons",
              delta=f"{delta_agr:+.0f}" if prev_agr else None)

st.subheader("🔴 Inflation Analysis (Monthly IPC % Variation)")

colors_infl = [RED if x > 3 else (RED if x < 0 else GREEN) for x in df_inflation["value"]]
fig_infl = go.Figure()

fig_infl.add_trace(go.Bar(x=df_inflation["date"], y=df_inflation["value"],
                          marker=dict(color=colors_infl), name="IPC Monthly %"))

fig_infl.add_hline(y=3, line_dash="dash", line_color="red", annotation_text="BCRP Target Band")
fig_infl.add_hline(y=1, line_dash="dash", line_color="red")
fig_infl.add_hrect(y0=1, y1=3, fillcolor=GREEN, opacity=0.1, layer="below")

if show_ma:
    ma_6 = df_inflation["value"].rolling(window=6, center=True).mean()
    fig_infl.add_trace(go.Scatter(x=df_inflation["date"], y=ma_6,
                                   mode='lines', name='6m MA',
                                   line=dict(color='blue', width=2)))

if show_trend:
    z = np.polyfit(np.arange(len(df_inflation)), df_inflation["value"], 1)
    p = np.poly1d(z)
    fig_infl.add_trace(go.Scatter(x=df_inflation["date"], y=p(np.arange(len(df_inflation))),
                                   mode='lines', name='OLS Trend',
                                   line=dict(color='orange', width=2, dash='dot')))

max_idx = df_inflation["value"].idxmax()
fig_infl.add_annotation(x=df_inflation["date"].iloc[max_idx],
                        y=df_inflation["value"].iloc[max_idx],
                        text=f"Peak: {df_inflation['value'].iloc[max_idx]:.2f}%",
                        showarrow=True)

fig_infl.update_layout(title="Monthly Inflation Rate (2023–2026)",
                       xaxis_title="Date", yaxis_title="% Change",
                       hovermode="x unified", height=CHART_HEIGHT,
                       template="plotly_white")
st.plotly_chart(fig_infl, use_container_width=True)

st.subheader("💱 Exchange Rate & Interest Rate")

col_left, col_right = st.columns(2)

with col_left:
    fig_exch = go.Figure()
    fig_exch.add_trace(go.Scatter(x=df_exchange["date"], y=df_exchange["value"],
                                   fill='tozeroy', name="USD/PEN",
                                   line=dict(color='#1f77b4', width=2)))

    if show_ma:
        ma_6_exch = df_exchange["value"].rolling(window=6, center=True).mean()
        fig_exch.add_trace(go.Scatter(x=df_exchange["date"], y=ma_6_exch,
                                       mode='lines', name='6m MA',
                                       line=dict(color='green', width=2)))

    max_exch_idx = df_exchange["value"].idxmax()
    min_exch_idx = df_exchange["value"].idxmin()
    fig_exch.add_annotation(x=df_exchange["date"].iloc[max_exch_idx],
                            y=df_exchange["value"].iloc[max_exch_idx],
                            text=f"Max: {df_exchange['value'].iloc[max_exch_idx]:.3f}",
                            showarrow=True)
    fig_exch.add_annotation(x=df_exchange["date"].iloc[min_exch_idx],
                            y=df_exchange["value"].iloc[min_exch_idx],
                            text=f"Min: {df_exchange['value'].iloc[min_exch_idx]:.3f}",
                            showarrow=True)

    fig_exch.update_layout(title="Tipo de Cambio USD/PEN",
                           xaxis_title="Date", yaxis_title="S/ per USD",
                           hovermode="x unified", height=CHART_HEIGHT,
                           template="plotly_white")
    st.plotly_chart(fig_exch, use_container_width=True)

with col_right:
    fig_rate = go.Figure()
    fig_rate.add_trace(go.Scatter(x=df_interest["date"], y=df_interest["value"],
                                   mode='lines', fill='tozeroy', name="BCRP Rate",
                                   line=dict(color=RED, width=3)))

    current_rate = df_interest["value"].iloc[-1]
    fig_rate.add_hline(y=current_rate, line_dash="dash", line_color="gray",
                       annotation_text=f"Current: {current_rate:.2f}%")

    fig_rate.add_annotation(x=df_interest["date"].iloc[0], y=df_interest["value"].iloc[0],
                            text="Rate cutting cycle", showarrow=True)

    fig_rate.update_layout(title="BCRP Reference Rate (Tasa Referencial)",
                           xaxis_title="Date", yaxis_title="% Annual",
                           hovermode="x unified", height=CHART_HEIGHT,
                           template="plotly_white")
    st.plotly_chart(fig_rate, use_container_width=True)

st.subheader("📈 Economic Activity & Agricultural Output")

col_left, col_right = st.columns(2)

with col_left:
    fig_gdp = go.Figure()
    fig_gdp.add_trace(go.Scatter(x=df_gdp["date"], y=df_gdp["value"],
                                  mode='lines', fill='tozeroy', name="GDP Index",
                                  line=dict(color=NAVY, width=3)))

    if show_trend:
        z_gdp = np.polyfit(np.arange(len(df_gdp)), df_gdp["value"], 1)
        p_gdp = np.poly1d(z_gdp)
        fig_gdp.add_trace(go.Scatter(x=df_gdp["date"], y=p_gdp(np.arange(len(df_gdp))),
                                      mode='lines', name='OLS Trend',
                                      line=dict(color='orange', width=2, dash='dot')))

    fig_gdp.update_layout(title="PBI Desestacionalizado (Index 2007=100)",
                          xaxis_title="Date", yaxis_title="Index",
                          hovermode="x unified", height=CHART_HEIGHT,
                          template="plotly_white")
    st.plotly_chart(fig_gdp, use_container_width=True)

with col_right:
    fig_agr = go.Figure()
    fig_agr.add_trace(go.Bar(x=df_agricultural["date"], y=df_agricultural["value"],
                             marker=dict(color=GOLD), name="Production"))

    if show_ma:
        ma_agr = df_agricultural["value"].rolling(window=6, center=True).mean()
        fig_agr.add_trace(go.Scatter(x=df_agricultural["date"], y=ma_agr,
                                      mode='lines', name='6m MA',
                                      line=dict(color='red', width=2)))

    fig_agr.update_layout(title="Producción Agrícola - Naranja (miles toneladas)",
                          xaxis_title="Date", yaxis_title="Thousand Tons",
                          hovermode="x unified", height=CHART_HEIGHT,
                          template="plotly_white")
    st.plotly_chart(fig_agr, use_container_width=True)

st.subheader("📊 Statistical Summary (May 2023 – Apr 2026)")

summary_data = {
    "Indicator": ["Inflation (IPC %)", "Exchange Rate (S/ per USD)", "GDP Index",
                  "Interest Rate (%)", "Agricultural Prod. (k tons)"],
    "Average": [
        f"{df_inflation['value'].mean():.2f}",
        f"{df_exchange['value'].mean():.3f}",
        f"{df_gdp['value'].mean():.1f}",
        f"{df_interest['value'].mean():.2f}",
        f"{df_agricultural['value'].mean():.1f}",
    ],
    "Min": [
        f"{df_inflation['value'].min():.2f}",
        f"{df_exchange['value'].min():.3f}",
        f"{df_gdp['value'].min():.1f}",
        f"{df_interest['value'].min():.2f}",
        f"{df_agricultural['value'].min():.1f}",
    ],
    "Max": [
        f"{df_inflation['value'].max():.2f}",
        f"{df_exchange['value'].max():.3f}",
        f"{df_gdp['value'].max():.1f}",
        f"{df_interest['value'].max():.2f}",
        f"{df_agricultural['value'].max():.1f}",
    ],
    "Latest": [
        f"{df_inflation['value'].iloc[-1]:.2f}",
        f"{df_exchange['value'].iloc[-1]:.3f}",
        f"{df_gdp['value'].iloc[-1]:.1f}",
        f"{df_interest['value'].iloc[-1]:.2f}",
        f"{df_agricultural['value'].iloc[-1]:.1f}",
    ],
}

df_summary = pd.DataFrame(summary_data)
st.dataframe(df_summary, use_container_width=True, hide_index=True)

st.divider()
st.caption(f"Source: Banco Central de Reserva del Perú (BCRP) | Data period: May 2023 – Apr 2026")
st.caption(f"Dashboard generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Series: PN01271PM · PN01234PM · PN01773AM · PN07819NM")
