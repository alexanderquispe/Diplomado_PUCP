# Sesión 08 · LLMs: instrucciones, salidas estructuradas y RAG

## Entorno

```bash
uv sync --group llm
uv run jupyter lab
```

No hace falta API key para la clase: todo corre local.

## Contenido

| Archivo | Qué es |
|---|---|
| `assets/Intro_LLMs_Slides.pdf` | Slides de introducción: tokens, siguiente token, embeddings, producto punto |
| **`lecture/llms_a_prueba.ipynb`** | **Clase práctica.** Comprueba una por una las afirmaciones de las slides con un modelo real y termina en un buscador RAG sobre el sílabo |
| `assets/Silabo_DS_Python_UP_2026_II.tex` | El sílabo que usa la sección 6 de la clase como documento de prueba |
| `lab/`, `lab9.ipynb` | Laboratorios con APIs y RAG con ChromaDB — requieren API key (ver abajo) |

## `llms_a_prueba.ipynb`

Modelos: `Qwen/Qwen2.5-0.5B-Instruct` (generación) e `intfloat/multilingual-e5-small`
(embeddings). ~1,5 GB la primera vez; corre en CPU.

1. **Tokens** — reproduce los 32 IDs de la slide 14 (`o200k_base`); por qué un LLM no cuenta letras; el español usa ~25 % más tokens
2. **Siguiente token** — la distribución sobre 151 936 tokens; el bucle de generación escrito a mano; temperatura
3. **$W_E$** — la matriz de embeddings real: 151 936 × 896, el 28 % del modelo
4. **Producto punto** — signo, trampa de la magnitud, vecinos semánticos
5. **Analogías** — king − man + woman → queen funciona; «ceviche» falla porque no es un token
6. **Pregúntale al sílabo** — troceo, búsqueda semántica, evaluación con hit@k y RAG en miniatura

Resultados que produce: embeddings aciertan 7/10 preguntas parafraseadas (hit@3) frente a
3/10 por palabras clave; el RAG muestra dos tipos de falla (recuperación y generación) y
que no existe un `k` único que funcione para todas las preguntas.

## Laboratorios

Todos piden la clave al ejecutarse, con `getpass`: se escribe en el cuadro que
aparece y no queda guardada en el notebook. **Nunca pegues una clave dentro de
una celda.**

| Notebook | Clave que pide | Archivo que usa |
|---|---|---|
| `lab/LLM_GPT.ipynb` | OpenAI | — |
| `lab/LAB_LLM_DeepSeeK.ipynb` | DeepSeek | — |
| `lab/LLM_basics.ipynb` | OpenAI | `bdg_2022.pdf` (lo descarga el notebook) |
| `lab9.ipynb` | OpenAI | `bdg_2022.pdf` (lo descarga el notebook) |
| `lab/RAG_clinico_sintomas.ipynb` | OpenAI y Anthropic | `lab/knowledge_base.json` |
| `lab/RAG_documento_demo.ipynb` | Gemini | `lab/Artificial_intelligence_applications_Latin.pdf` |

Algunos notebooks traen una celda `!pip install ...`. Con el grupo `llm` ya
instalado esa celda no hace nada nuevo: se puede saltar.

`lab/guia_alumnos_demo.md` es la guía original para Windows con `pip` y `venv`.
En este repositorio no hace falta seguirla: `uv sync --group llm` la reemplaza.
