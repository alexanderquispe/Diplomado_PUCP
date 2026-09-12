# Sesión 05 · APIs, y una API que entiende texto

**2 h · mié 23 set**

## Entorno

```bash
uv sync --group ia
uv run jupyter lab
```

## Contenido

Dos mitades que son la misma mecánica.

**Notebook:** `03_apis_e_ia.ipynb`

- **Hora 1 — APIs.** Endpoints, parámetros, JSON anidado, `raise_for_status`, manejo de errores. API del Banco Mundial.
- **Hora 2 — La API de Claude.** Clasificar reclamos ciudadanos en texto libre y extraer campos estructurados en JSON.

**Genera:** `contexto_peru.csv`, `reclamos_clasificados.csv`

> ⚠️ **Antes de la clase:** las celdas de la segunda mitad necesitan `ANTHROPIC_API_KEY`
> en un archivo `.env`. Están guardadas sin ejecutar a propósito, para correrlas en vivo.
> Ver `.env.example` en la raíz.

Se deja la Tarea 2.

## Datos

```bash
uv run python scripts/fetch_data.py 05-apis-e-ia
```
