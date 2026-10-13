#  Guía paso a paso para correr el proyecto desde CMD (Windows)

##  Checklist de prerrequisitos

---

## 🪟 PARTE 1 — Abrir CMD y verificar Python

### 1.1 — Abrir CMD

Hay varias formas, usa la que prefieras:


- Pulsa la tecla **Windows**, escribe `cmd` y haz clic en **Símbolo del sistema**.


### 1.2 — Verificar la versión de Python

En la ventana de CMD escribe:

```cmd
python --version
```

Resultado esperado:

```
Python 3.10.x
```

### 1.3 — Verificar pip

```cmd
pip --version
```

Debe responder con la versión de pip y la ruta donde está instalado. Si falla, vuelve al paso anterior.

---

##  PARTE 2 — Preparar la carpeta del proyecto

### 2.1 — Crear una carpeta de trabajo

Vamos a usar `C:\Users\TU_USUARIO\Documents\rag-demo`. Si tu usuario es distinto, ajusta el nombre.

En CMD ejecuta (una línea a la vez):

```cmd
cd %USERPROFILE%\Documents
mkdir rag-demo
cd rag-demo
```

>  `%USERPROFILE%` es una variable que apunta a tu carpeta de usuario, sea cual sea (`C:\Users\Juan`, `C:\Users\Maria`, etc.). **No hace falta cambiarla.**

### 2.2 — Copiar los archivos del proyecto

Copia dentro de `C:\Users\TU_USUARIO\Documents\rag-demo` los archivos que te entregó el profesor:

```
 rag-demo
└──  RAG_documento_demo.ipynb
```

(Si recibiste un `.zip`, click derecho → **Extraer todo…** → selecciona la carpeta `rag-demo`.)

### 2.3 — Verificar que el notebook está ahí

```cmd
dir
```

Debe aparecer en el listado el archivo `RAG_documento_demo.ipynb`.

---

##  PARTE 3 — Crear y activar el entorno virtual

>  **¿Qué es un entorno virtual?** Es un Python aislado solo para este proyecto. Las librerías que instales aquí no afectan a otros proyectos de tu PC.

### 3.1 — Crear el venv

Asegúrate de que el prompt está en la carpeta correcta (debe terminar en `…\rag-demo>`). Ejecuta:

```cmd
python -m venv venv
```

Esto tarda unos 10–15 segundos y crea una carpeta nueva llamada `venv\` dentro del proyecto.

### 3.2 — Activar el venv

```cmd
venv\Scripts\activate
```

Si todo va bien, el prompt cambia a:

```
(venv) C:\Users\TU_USUARIO\Documents\rag-demo>
```

>  **Mientras veas `(venv)` al principio, estás dentro del entorno virtual.**

> 🚨 **Si ves un error de “execution policy”** → eso solo pasa en PowerShell. En **CMD** no debería ocurrir. Verifica que estás efectivamente en el *Símbolo del sistema* y no en PowerShell.

### 3.3 — Desactivar el venv (cuando termines)

Cuando ya no quieras usar el proyecto, basta con:

```cmd
deactivate
```

---

##  PARTE 4 — Instalar las dependencias

Con el `(venv)` activo, instala todas las librerías necesarias:

```cmd
pip install pypdf tiktoken langchain-text-splitters deep-translator google-genai chromadb ipywidgets tqdm python-dotenv notebook
```

 Tarda **3–5 minutos** dependiendo de tu conexión. Verás muchas líneas de descarga.

Al final debe aparecer un mensaje similar a:

```
Successfully installed chromadb-... deep-translator-... google-genai-... notebook-...
```

### 4.1 — Verificar la instalación

```cmd
pip list | findstr /I "chromadb google-genai deep-translator pypdf notebook"
```

Debes ver las cinco librerías listadas con sus versiones. Si falta alguna, repite el `pip install` correspondiente.

---

##  PARTE 5 — Obtener tu API Key de Gemini

### 5.1 — Generar la clave

1. Abre el navegador y ve a 👉 <https://aistudio.google.com/app/apikey>
2. Inicia sesión con tu cuenta de Google.
3. Haz clic en **“Create API key”** (botón azul).
4. Selecciona o crea un proyecto.
5. Copia la cadena que empieza con `AIzaSy…` (39 caracteres aprox.).

>  **Guárdala en un lugar seguro** (un bloc de notas, gestor de contraseñas…). **No la subas a GitHub** y **no la compartas** con nadie.

### 5.2 — ¿Dónde se ingresa la clave?

En este proyecto la clave se pega **directamente al ejecutar la celda del Paso 1 del notebook**. Cuando hagas `Ctrl + Enter` en esa celda, aparecerá un campo donde tendrás que pegar la API Key. **No se guarda en ningún archivo, no queda escrita en pantalla.**

>  
>
> ```
> GEMINI_API_KEY=AIzaSy_tu_clave_real_aqui
> ```
>
> 

---

##  PARTE 6 — Preparar el documento PDF de la demostración

### 6.1 — Elegir un PDF corto

Para esta demo conviene un PDF de **entre 5 y 30 páginas**: un artículo, un capítulo, un manual, una nota técnica… Si es muy largo, la indexación tarda más.

### 6.2 — Copiar el PDF a la carpeta del proyecto

Lo más sencillo es **dejar el PDF dentro de la propia carpeta `rag-demo`** y renombrarlo a `documento_demo.pdf`. Así el notebook lo encuentra sin tener que tocar rutas.

Desde CMD puedes copiarlo con:

```cmd
copy "C:\Users\TU_USUARIO\Downloads\mi_archivo.pdf" "%CD%\documento_demo.pdf"
```

>  `%CD%` es la carpeta actual. Asegúrate de estar en `…\rag-demo>` antes de ejecutar el `copy`.

Verifica que se copió:

```cmd
dir documento_demo.pdf
```

---

##  PARTE 7 — Abrir el notebook desde CMD

Con el `(venv)` activo y dentro de la carpeta del proyecto, lanza Jupyter:

```cmd
jupyter notebook
```

Sucederán dos cosas:

1. En la propia consola CMD verás logs del servidor.
2. **Tu navegador se abrirá automáticamente** mostrando la lista de archivos de la carpeta.

>  **Si el navegador no se abre solo**, busca en la consola una línea parecida a:
> ```
> http://localhost:8888/tree?token=…
> ```
> Cópiala y pégala manualmente en tu navegador.

### 7.1 — Abrir el notebook

En la página del navegador:

1. Haz clic sobre `RAG_documento_demo.ipynb`.
2. El notebook se abrirá en una pestaña nueva.

### 7.2 — Verificar el kernel

En la esquina superior derecha del notebook debería aparecer **“Python 3 (ipykernel)”** o similar. Si dice **“No Kernel”**, haz clic ahí y selecciona **Python 3**.

> ⚠️ **Importante:** No cierres la ventana de CMD mientras uses el notebook. Si la cierras, el servidor de Jupyter se detiene y el notebook deja de funcionar. Para **detener el servidor** (cuando termines), vuelve a CMD y presiona `Ctrl + C` dos veces.

---

## ▶ PARTE 8 — Ejecutar el notebook celda por celda

>  **Atajo clave:** `Shift + Enter` ejecuta la celda actual y avanza a la siguiente. `Ctrl + Enter` la ejecuta sin avanzar.

Vas a recorrer los **11 pasos en orden**, de arriba hacia abajo. Esto es lo que esperar en cada uno:

### Paso 0 — Preparación del entorno
Solo es una celda con un `pip install` comentado. **No la ejecutes** si ya hiciste el `pip install` de la Parte 4.

### Paso 1 — Carga segura de la API Key
**Lo que vas a ver al ejecutar la celda con `Ctrl + Enter`:**

```
 Pega tu API Key de Gemini y presiona Enter (no se mostrará por seguridad):
   GEMINI_API_KEY ➜ █
```

Pega aquí tu clave (no se mostrará en pantalla — es normal). Presiona **Enter**. Resultado:

```
 Clave cargada correctamente — longitud: 39 caracteres.
```

> 🚨 Si dejas el campo vacío y das Enter, te dará `AssertionError`. Vuelve a ejecutar la celda y pega bien la clave.

### Paso 2 — Verificación del traductor
**Lo que ves:**

```
 Traductor operativo.
   Entrada : Knowledge is power.
   Salida  : El conocimiento es poder.
```

>  

### Paso 3 — Lectura del documento PDF
⏱️ ~5 segundos para un PDF corto.

**Lo que ves:**

```
📄 Páginas detectadas: 18
📊 Caracteres totales : 42,150
📊 Palabras aprox.    : 6,820
🔍 Vista previa (primeros 400 caracteres):
------------------------------------------------------------
[texto del documento]
------------------------------------------------------------
```



### Paso 4 — Conteo de tokens
**Lo que ves:**

```
🔢 Tokens del documento : 9,420
📏 Límite por petición  : 8 192 tokens (gemini-embedding-001)
➡️  Por eso lo dividiremos en fragmentos en el siguiente paso.
```

### Paso 5 — Segmentación en fragmentos
⏱️ ~2 segundos.

**Lo que ves:**

```
  Fragmentos generados : 48
 Tamaño objetivo       : 200 tokens (con 25 de solapamiento)

 Ejemplo — fragmento #3 (texto original):
------------------------------------------------------------
[fragmento de texto en inglés u original]
------------------------------------------------------------
```
### Paso 6 — Traducción al español 
⏱ Para un documento corto: **30 segundos – 2 minutos**.

**Lo que ves:** una barra de progreso `tqdm`:

```
 Traduciendo EN→ES: 100%|████████| 48/48 [00:45<00:00]
 48 traducciones guardadas en 'segments_cache.pkl'.
```

>  Se guarda automáticamente en `segments_cache.pkl`. **Si repites la demo después, este paso será instantáneo** (la próxima vez detecta la caché y no traduce de nuevo).
>
>  Si Google Translate frena con muchos errores: detén la celda con el botón cuadrado ⏹️, espera 2–3 minutos y vuelve a ejecutar. Continuará desde donde se quedó.

### Paso 7 — Configuración de embeddings
 Inmediato.

**Lo que ves:**

```
 Embeddings listos.
   • Modelo       : gemini-embedding-001
   • Dimensiones  : 768
   • Throttling   : 1 petición cada 1.1s (~54 por minuto)
```

### Paso 8 — Base vectorial ChromaDB
 ~2 segundos.

**Lo que ves:**

```
 olección activa : 'rag_demo_collection'
 Persistencia en  : ./chroma_storage
 Documentos hoy   : 0
```

### Paso 9 — Indexación con embeddings 📥
 Para un documento corto: **1–2 minutos** (depende del número de fragmentos).

**Lo que ves:**

```
 Se indexarán 48 fragmentos nuevos.
   Tiempo estimado: ~0.9 minutos.

 Indexando: 100%|████████| 5/5 [00:53<00:00]

 Indexado completo. Total en colección: 48
```

>  **Si vuelves a ejecutar esta celda después**, detectará que ya están indexados y no repetirá el trabajo: `♻️  La colección ya contiene 48 fragmentos. No se reindexa.`
>
>  Si te da error `RESOURCE_EXHAUSTED` o `429`: llegaste al rate limit del free tier. El código tiene reintentos automáticos. Si insiste, espera 1 minuto y vuelve a ejecutar la celda — continuará desde donde quedó.

### Paso 10 — Prueba del pipeline RAG
 ~5 segundos.

**Lo que ves:**

```
 Prueba rápida del pipeline RAG

 RESPUESTA:
[respuesta generada por Gemini sobre el contenido del documento]

 FUENTES (top 3):
   1. distancia=0.3520 → [fragmento del documento]…
   2. distancia=0.4108 → [fragmento del documento]…
   3. distancia=0.4633 → [fragmento del documento]…
```

### Paso 11 — Interfaz interactiva 
**Lo que ves:** una caja morada con el título *“Asistente RAG sobre tu documento”*, un campo de texto, un slider de fragmentos, y dos botones (🚀 Preguntar y 🧹 Limpiar).


---

##  PARTE 9 — Hacer preguntas al documento

Una vez veas la caja morada del Paso 11:

1. **Click** dentro del campo de texto.
2. **Escribe** tu pregunta. Algunas ideas:
   - *¿De qué trata este documento?*
   - *¿Cuáles son las ideas principales?*
   - *Resume el apartado sobre [tema X].*
   - *¿Qué conclusiones plantea el autor?*
3. **Ajusta el slider** “Fragmentos a recuperar” (4 está bien para empezar).
4. Haz click en ** Preguntar**.
5. Espera 2–3 segundos.
6. Verás:
   - Tu pregunta
   - La respuesta generada por Gemini, basada solo en el documento
   - Los fragmentos que se consultaron (haz click en cada uno para expandirlo)

>  **Las preguntas son ilimitadas** una vez indexado el documento. Cada pregunta cuesta ~2 peticiones de Gemini (búsqueda + generación), bien dentro del free tier.

---


>  Solo deberás volver a pegar la API Key en el Paso 1 (no se guarda).

---
