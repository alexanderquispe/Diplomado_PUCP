# Proyecto: Web Scrapping - Parte 1 (API de Reddit)

## 🎯 Objetivo
Recopilar datos de publicaciones y comentarios de subreddits políticos utilizando la API de Reddit (PRAW), identificar las publicaciones más comunes y sus comentarios.

---

## 📌 Parte 1: Configuración de la API de Reddit y recopilación de datos

### 1) Credenciales de la API de Reddit: Cuenta de desarrollador
- Ingresé a [https://www.reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/).
- Creé una aplicación con los siguientes datos:
  - **Nombre**: `webscrapping_group4`
  - **Tipo**: `script`
  - **About URL**: `http://localhost`
  - **Redirect URI**: `http://localhost:8080`
- Esto generó mis credenciales:
  - `client_id`
  - `client_secret`
- Las guardé en un archivo oculto **.env** para mantenerlas seguras:
  ```env
  REDDIT_CLIENT_ID=xxxxxxxx
  REDDIT_CLIENT_SECRET=xxxxxxxx
  REDDIT_USER_AGENT=python:webscrappingProject:v1.0 (by /u/CranberryEqual8083)
  ```


### 2) Configuración del entorno
- Activé mi entorno de conda:
```bash
conda activate envseleniumvivi
```
- Instalé las librerías necesarias:
```bash
pip install praw python-dotenv pandas
```
- Verifiqué que el archivo .env cargaba correctamente con:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); \
print('ID:', os.getenv('REDDIT_CLIENT_ID')); \
print('SEC:', (os.getenv('REDDIT_CLIENT_SECRET') or '')[:5]+'...'); \
print('UA:', os.getenv('REDDIT_USER_AGENT'))"
```

✅ Resultado esperado: se muestran los valores de client_id, un fragmento de client_secret y el user_agent.



### 3) Conexión API (PRAW)
- Creé el archivo code/api_reddit.py con el siguiente código base:
```python
import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
)

print("✅ Conexión exitosa. Autenticado como:", reddit.user.me())
```
- Probé la conexión ejecutando en terminal:
```bash
python code/api_reddit.py
```
- ✅ Resultado esperado:
```yaml
✅ Conexión exitosa. Autenticado como: CranberryEqual8083
```
- Luego ejecuté consultas para distintos subreddits, por ejemplo:
```bash
python code/api_reddit.py --subreddit peru --query "economia" --limit 10 --comments --max_comments 5
```
- Los resultados se guardaron en la carpeta ./salida/ como:
  - reddit_posts.csv
  - reddit_comments.csv

- ✅ Ejemplo de salida:
```bash
✅ Posts guardados en: ./salida/reddit_posts.csv  (10 filas)
✅ Comentarios guardados en: ./salida/reddit_comments.csv  (38 filas)
```


## 📊 Parte 2: Recopilación de datos y almacenamiento

### 4) Recopilar publicaciones de subreddits
- **Subreddits de destino**:
  - `r/politics`
  - `r/PoliticalDiscussion`
  - `r/worldnews`

- **Tarea**: para cada uno de los tres subreddits, recopilé **20 publicaciones** en modo “top” (principales).

- **Extracción (por cada publicación)**:
  - `title` (título)
  - `score` (votos positivos)
  - `num_comments` (número de comentarios)
  - `id` (identificador único)
  - `url`

- **Almacenamiento**: los datos se guardaron en archivos CSV dentro de la carpeta `./salida/`.

### 5) Recopilar comentarios
- **Tarea**: para cada publicación recopilada, obtuve hasta **5 comentarios**.

- **Extracción (por cada comentario)**:
  - `body` (texto del comentario)
  - `score` (votos positivos del comentario)
  - `post_id` (para enlazar a la publicación original)

- **Almacenamiento**: los comentarios se guardaron en archivos CSV dentro de la carpeta `./salida/`.

### 6) Ejecución en Windows CMD
Desde el directorio del proyecto ejecuté en **CMD**:

```bat
python code\api_reddit.py --batch_subs politics,PoliticalDiscussion,worldnews --batch_mode top --batch_limit 20 --batch_max_comments 5
```

✅ Resultados esperados

- Para cada subreddit:

  - Se genera un archivo *_posts.csv con 20 publicaciones.

  - Se genera un archivo *_comments.csv con 100 comentarios (20 publicaciones × 5 comentarios c/u).

- Ejemplo de salida:

  - ./salida/politics_posts.csv → 20 filas

  - ./salida/politics_comments.csv → 100 filas

  - ./salida/PoliticalDiscussion_posts.csv → 20 filas

  - ./salida/PoliticalDiscussion_comments.csv → 100 filas

  - ./salida/worldnews_posts.csv → 20 filas

  - ./salida/worldnews_comments.csv → 100 filas

🔍 Validación rápida con Python (en Windows CMD)
  - Para confirmar que los CSV se generaron correctamente, corrí este bloque en CMD:
  ```bat
  python
  ```

```python
import pandas as pd, glob

for f in sorted(glob.glob("./salida/*_posts.csv")):
    df = pd.read_csv(f)
    print(f, len(df))

for f in sorted(glob.glob("./salida/*_comments.csv")):
    df = pd.read_csv(f)
    print(f, len(df))
```

- Salida esperada:
```bash
./salida/politics_posts.csv 20
./salida/politics_comments.csv 100
./salida/PoliticalDiscussion_posts.csv 20
./salida/PoliticalDiscussion_comments.csv 100
./salida/worldnews_posts.csv 20
./salida/worldnews_comments.csv 100
```

```yaml
---
👉 Con esto, tu README ya documenta **lo que hiciste en la Parte 2 paso a paso**, incluyendo la validación.  
```
