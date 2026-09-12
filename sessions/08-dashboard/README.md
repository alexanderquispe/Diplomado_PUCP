# Sesión 08 · Del notebook a una página pública

**1.5 h · sáb 3 oct**

## Entorno

```bash
uv sync --group dashboard
uv run jupyter lab
```

## Contenido

Los participantes salen con una URL viva.

**Archivos**
- `06_dashboard.ipynb` — las piezas de Streamlit y los pasos de despliegue
- `app.py` — el dashboard completo y funcional
- `datos.csv`, `distritos.geojson` — datos versionados (deben estar en el repo para desplegar)
- `requirements.txt` — para Streamlit Cloud

**Correr en local**

```bash
cd sessions/08-dashboard
uv run streamlit run app.py
```

**Publicar:** [share.streamlit.io](https://share.streamlit.io) → Sign in with GitHub → New app.
