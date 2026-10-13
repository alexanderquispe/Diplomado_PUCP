# Sesión 11 · Agentes

## Entorno

```bash
uv sync --group agents
uv run jupyter lab
```

## Contenido

| Archivo | Dónde corre | Qué necesita |
|---|---|---|
| `lecture-crewai.ipynb` | Local o Colab | Clave de OpenAI y clave de Serper (búsqueda web) |
| `lab/LAB_JSON_AGENT.ipynb` | Colab | Clave de OpenAI |
| `lab/PDF_AGENTS.ipynb` | Colab | Clave de OpenAI. Los PDF de `lab/` sirven de ejemplo para subir |
| `lab/Skills_Claude/` | Local | Proyecto con su propio README: servidor MCP del BCRP + dashboard en Streamlit |
| `lab/DatosAbiertos/` | Local | Proyecto con su propio README: servidor MCP de datos abiertos + dashboard |
| `lecture-openclaw/` | — | Slides (`OpenClaw_Lecture.pdf`) y plan de la clase |

Los dos notebooks de `lab/` se escribieron para Google Colab: suben archivos con
`files.upload()`, que solo existe ahí.

### Sobre `Skills_Claude/` y `DatosAbiertos/`

Sus README explican cómo crear un entorno con `setup.ps1` y `pip`. En este
repositorio ese paso no hace falta: el grupo `agents` ya trae `mcp`, `streamlit`
y `requests`. Por ejemplo:

```bash
uv run streamlit run sessions/11-agentes/lab/Skills_Claude/dashboard.py
```

## Claves

Los tres notebooks piden sus claves con `getpass`: se escriben en el cuadro que
aparece al ejecutar la celda y no quedan guardadas. **Nunca escribas una clave
dentro de una celda.**

## Datos

No hay nada que descargar a mano. Los PDF de ejemplo ya están en `lab/`.
