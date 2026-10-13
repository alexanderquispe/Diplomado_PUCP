# Sesión 09 · Hugging Face y fine-tuning

## Entorno

```bash
uv sync --group hf
uv run jupyter lab
```

## Dónde corre cada notebook

Casi todo el material de esta sesión se escribió para **Google Colab con GPU**.
Afinar un modelo en una laptop sin GPU puede tomar horas; en Colab, minutos.

| Notebook | Dónde | Qué necesita |
|---|---|---|
| `lecture-modernbert.ipynb` | Local o Colab | Token de Hugging Face. GPU recomendada |
| `lecture-os-models.ipynb` | Colab | Varias celdas usan las clases `TFAuto...` de TensorFlow |
| `lecture-finetuning.ipynb` | Colab con GPU | Clave de OpenAI. Algunas celdas usan TensorFlow |
| `lab-hf/LAB_HUGGING_FACE.ipynb` | Colab | Token de la API de X (Twitter); instala `geoai` |
| `lab-hf/Lab_Roberta.ipynb` | Colab | — |
| `lab-finetune/fine_tune_modernbert_classifier.ipynb` | Colab con GPU | Token de Hugging Face |
| `assets/modernbert_v3.ipynb` | Colab con GPU | Token de Hugging Face |

### Por qué TensorFlow solo en Colab

El grupo `hf` instala `transformers` 5, que trabaja con PyTorch y ya no incluye
las clases de TensorFlow (`TFAutoModelFor...`). Las celdas que las usan fallan en
el entorno local: necesitan TensorFlow y una versión de `transformers` anterior
a la 5.

## Tokens y claves

El token de Hugging Face se crea en <https://huggingface.co/settings/tokens>.

- **En local**, inicia sesión una sola vez desde la terminal. El token queda
  guardado fuera del repositorio y los notebooks lo encuentran solos:
  ```bash
  uv run hf auth login
  ```
- **En Colab**, pégalo en el cuadro que abre `notebook_login()`.
- La clave de OpenAI de `lecture-finetuning.ipynb` se pide con `getpass` al
  ejecutar la celda.

**Nunca escribas un token dentro de una celda**, aunque el notebook traiga una
línea comentada `login(token="hf_...")`. Un token subido a GitHub queda expuesto
aunque después se borre.

## Datos

No hay nada que descargar a mano: los notebooks bajan sus datasets y modelos
desde Hugging Face con `load_dataset(...)` y `from_pretrained(...)`.

Los modelos afinados (`ModernBERT-*/`, `checkpoint-*/`) pesan más de 1 GB y no se
versionan.
