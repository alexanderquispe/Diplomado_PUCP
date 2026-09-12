# Contexto para agentes de código

Repositorio del curso **Fundamentos de Python para Ciencias Sociales y Gestión
Pública** (Diplomado PUCP 2026). Público: profesionales de todas las carreras,
sin experiencia previa en programación.

## Regla principal

El código de este curso lo van a **leer en voz alta** participantes que recién
empiezan. Prioriza que se entienda por encima de que sea elegante.

- Nada de comprensiones anidadas, `lambda` complicados ni encadenamientos largos.
- Nombres de variables en español y descriptivos: `casos_por_distrito`, no `df2`.
- Una idea por celda. Si una celda necesita tres comentarios, son tres celdas.
- Sin clases ni programación orientada a objetos. Funciones solo cuando algo
  se repite tres veces.
- Comentarios que expliquen **por qué**, no **qué**.

## El hilo del curso

Un solo caso atraviesa las 6 sesiones activas: **dengue en el Perú y capacidad
de respuesta del sistema de salud**. Todo cruza por **ubigeo**.

Cada sesión abre con una pregunta sustantiva y el código es la respuesta. No
se enseña una función porque toca en el temario, sino porque hace falta para
responder la pregunta.

## Entorno

```bash
uv sync --group <scraping|ia|mapas|dashboard>
uv run jupyter lab
uv run python scripts/fetch_data.py <sesion>
```

Python 3.12. Dependencias en `pyproject.toml`, fijadas en `uv.lock`.
**No usar `pip install` ni `conda`.**

## Estructura

```
sessions/NN-tema/    notebook(s) + README.md + assets/
assignments/         enunciados
scripts/             fetch_data.py
data/                datasets (gitignored)
archive/             material 2022-2025 (no tocar)
```

## Al crear o editar notebooks

1. **Ejecútalos.** Un notebook sin outputs no sirve para dar clase.
   ```bash
   uv run jupyter nbconvert --to notebook --execute --inplace <archivo>.ipynb
   ```
2. **Ritmo:** 12 a 15 celdas por hora de clase. Una sesión de 1.5 h son unas
   20 celdas; una de 3 h, unas 40.
3. **Cierra con una tabla resumen** de "qué hicimos" con el código de cada paso.
4. **Los mapas de Folium no se guardan con output** (pesan varios MB). Se
   generan al correr la celda.

## Datos

Los ubigeos son **texto de 6 dígitos**, siempre: `080914`, no `80914`. Leerlos
como número les come el cero de la izquierda y rompe todos los cruces. Es el
error más común del curso y se enseña a propósito.

## Lo que no va en este curso

Programación orientada a objetos, herencia, decoradores, `args`/`kwargs`,
manejo avanzado de excepciones, inferencia causal, NLP clásico, datos raster.
Todo eso vive en `archive/lectures-legacy/` o pasa al curso intermedio.

## Secretos

`ANTHROPIC_API_KEY` va en `.env` (gitignored). Nunca escrita dentro de un
notebook. Ver `.env.example`.
