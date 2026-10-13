# Sesión 10 · Document AI y voz

## Entorno

```bash
uv sync --group docai
uv run jupyter lab
```

## Dónde corre cada notebook

La mayoría se escribió para **Google Colab**: suben archivos con
`files.upload()`, que solo existe ahí.

| Notebook | Dónde | Qué necesita |
|---|---|---|
| `lab-voz/asr_motores_transcripcion.ipynb` | Local | Micrófono. Clave de OpenAI y token de Hugging Face para las secciones que los usan |
| `lab/LAB_Entrevistas.ipynb` | Colab | Clave de OpenAI |
| `lab/LAB_LLM_CV.ipynb` | Colab | Clave de OpenAI |
| `lab/LAB_PDF_TICKET.ipynb` | Colab | Clave de OpenAI |
| `lab-vision-models.ipynb` | Colab con GPU | — |
| `lab-voz/1_extract_text_from_pdfs_with_claude.ipynb` | Colab | Clave de Anthropic |
| `lab-voz/CPU VS GPU.ipynb` | Colab con GPU | TensorFlow (ya viene en Colab) |

`lecture/PDF_OCR_and_Complaint_Extraction_with_Claude_AI_.pdf` son las slides de
la clase.

## Claves

**Nunca escribas una clave dentro de una celda.**

- Los tres notebooks de `lab/` piden la clave de OpenAI con `getpass`: se escribe
  en el cuadro que aparece y no queda guardada.
- `asr_motores_transcripcion.ipynb` lee `OPENAI_API_KEY` y `HUGGINGFACE_TOKEN`
  del archivo `.env` de la raíz del repositorio, que no se sube a GitHub. Sin
  `HUGGINGFACE_TOKEN` se salta la parte de identificar hablantes y sigue. Esa
  parte además pide aceptar las condiciones del modelo
  `pyannote/speaker-diarization-3.1` en Hugging Face.
- `1_extract_text_from_pdfs_with_claude.ipynb` lee la clave de Anthropic desde un
  archivo de texto en Google Drive.

## Datos

No hay nada que descargar a mano. Cada laboratorio trabaja con el archivo que
tú subes (un PDF, un CV, un audio).

Los audios que se graban al correr los notebooks (`*.wav`) no se versionan.
