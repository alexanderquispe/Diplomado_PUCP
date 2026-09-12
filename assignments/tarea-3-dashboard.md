# Tarea 3 · Dashboard público (trabajo final)

**Se deja:** miércoles 30 de setiembre · **Vence:** martes 13 de octubre, 11:59 pm
**Peso:** 33.3%

## Qué se entrega

**Una URL.** Un dashboard funcionando en Streamlit Cloud, más el enlace al
repositorio de GitHub que lo alimenta.

No se entrega un archivo. Si el enlace no abre, no hay entrega.

## El trabajo

Construye un dashboard sobre tus datos —los de las tareas 1 y 2, o unos nuevos
de tu área.

### Requisitos mínimos

| # | Requisito | Puntos |
|---|---|---|
| 1 | **Al menos 2 filtros** que cambien de verdad lo que se muestra (`selectbox`, `multiselect`, `slider`) | 3 |
| 2 | **Una fila de métricas** (`st.metric`) que se actualicen con los filtros | 2 |
| 3 | **Tres gráficos** de distinto tipo, hechos con Plotly | 5 |
| 4 | **Un mapa** del Perú con tus datos | 4 |
| 5 | **Una tabla** con los datos filtrados y botón de descarga | 2 |
| 6 | **Desplegado y accesible** desde cualquier navegador | 4 |

### Requisitos de forma

- Los datos viven **dentro del repositorio** (una ruta `../../data/` funciona en
  tu máquina y falla en la nube)
- `requirements.txt` con todo lo que la app importa
- `@st.cache_data` en la carga de datos
- Cada gráfico con título que diga la conclusión, ejes con nombre y fuente citada
- El repositorio tiene que ser **público**

### El README del repositorio

Media página que responda:

1. ¿Qué pregunta responde este dashboard?
2. ¿De dónde vienen los datos y de cuándo son?
3. ¿Qué encontraste? Dos o tres hallazgos concretos.
4. ¿Qué limitaciones tiene lo que hiciste?

## Uso de agentes de código

Permitido, y para esta tarea es lo esperado: el `app.py` es largo y repetitivo.

**Pero:** en la sesión de cierre vas a mostrar tu dashboard y explicar una parte
del código que te señale. Si no puedes explicar lo que muestras, la nota baja
independientemente de que la app funcione.

## Cómo se califica

| | |
|---|---|
| Requisitos 1 a 6 | 20 puntos |
| Explicación en la presentación | condiciona la nota |
| El enlace no abre | sin entrega |

## Si te trabas

| Error | Qué revisar |
|---|---|
| `ModuleNotFoundError` | falta la librería en `requirements.txt` |
| `FileNotFoundError` | el CSV no está en el repo, o `.gitignore` lo bloqueó |
| La app se queda cargando | archivo muy pesado, o falta `@st.cache_data` |
| El mapa sale en blanco | el ubigeo no es texto de 6 dígitos en ambas tablas |
