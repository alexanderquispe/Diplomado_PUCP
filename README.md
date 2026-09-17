# Fundamentos de Python para Ciencias Sociales y Gestión Pública

**Diplomado PUCP · 2026**

| | |
|---|---|
| **Docente** | Alexander Quispe Rojas — alexander.quispe@pucp.edu.pe |
| **Jefe de práctica** | Edgar Luna — luna.e@pucp.edu.pe |
| **Horas** | 16 |
| **Horario** | Miércoles 7:00–10:00 pm · Sábados 8:00–9:30 am |

---

## De qué se trata

El curso recorre un solo camino: **leer datos → extraer datos → visualizarlos**.

No es un curso de programación. Es un curso de trabajo con datos, donde el
código es el medio. Se trabaja de principio a fin sobre un caso real —el dengue
en el Perú y la capacidad de respuesta del sistema de salud— y cada sesión
agrega una pieza al mismo producto final.

Los notebooks son cortos y aplicados: se corren en clase línea por línea, sin
teoría suelta. La práctica ocurre en las tareas, donde el uso de agentes de
código está permitido.

---

## Montar el entorno

```bash
uv sync                    # base
uv run jupyter lab
```

Cada sesión instala solo lo que necesita:

```bash
uv sync --group scraping    # sesión 4
uv sync --group ia          # sesión 5
uv sync --group mapas       # sesión 7
uv sync --group dashboard   # sesión 8
```

Las versiones exactas están fijadas en `uv.lock`. No hace falta activar nada:
`uv run` se encarga.

## Datos

**Los datos de la sesión 3 ya vienen en el repositorio** (`data/03-pandas/`): al
clonar, el notebook de pandas corre sin ningún paso previo.

El resto se descarga desde Hugging Face:

```bash
uv run python scripts/fetch_data.py              # todo
uv run python scripts/fetch_data.py 07-mapas     # solo una sesión
```

> Si alguna vez borras `data/` por accidente, ese mismo comando la reconstruye.

---

## Sesiones

| # | Fecha | h | Tema | Grupo |
|---|---|---|---|---|
| 01 | mié 9 set | 3 | [Git y GitHub](sessions/01-github) | — |
| 02 | sáb 12 set | 1.5 | [Fundamentos de Python](sessions/02-fundamentos-python) | — |
| 03 | mié 16 set | 3 | [Pandas de principio a fin](sessions/03-pandas) | — |
| 04 | sáb 19 set | 1.5 | [De la web al DataFrame](sessions/04-scraping) | `scraping` |
| 05 | mié 23 set | 2 | [APIs, y una API que entiende texto](sessions/05-apis-e-ia) | `ia` |
| 06 | sáb 26 set | 1.5 | [Gráficos que se entienden](sessions/06-visualizacion) | — |
| 07 | mié 30 set | 2 | [Mapas del Perú](sessions/07-mapas) | `mapas` |
| 08 | sáb 3 oct | 1.5 | [Del notebook a una página pública](sessions/08-dashboard) | `dashboard` |

Las sesiones 3 a 8 encadenan hacia el mismo producto: quien va al día llega a
la sesión 8 con el dashboard casi armado.

---

## Evaluación

| # | Tarea | Se deja | Vence | Peso |
|---|---|---|---|---|
| 1 | [Lists, Tuples, Dictionaries, and NumPy](https://github.com/alexanderquispe/Diplomado_PUCP/issues/1878) | 12 set | **20 set, 11:59 pm** | 33.3% |
| 2 | [Extraer datos](assignments/tarea-2-extraccion.md) | 23 set | 29 set | 33.3% |
| 3 | [Dashboard](assignments/tarea-3-dashboard.md) | 30 set | 13 oct | 33.3% |

### Sobre el uso de agentes de código

**Está permitido y es parte del método.** Claude Code, Copilot, ChatGPT: úsalos.

Lo que no se acepta es entregar código que no sabes explicar. Por eso cada
respuesta lleva debajo una celda de texto explicando **qué hace ese código y
por qué**. Sin esa celda, la pregunta no se califica.

No es un obstáculo burocrático: en el trabajo real, quien firma un informe
responde por sus números.

---

## Participantes

| Grupo | Integrante 1 | Integrante 2 | Integrante 3 | Integrante 4 | Integrante 5 |
|-------|-----------|-----------|-----------|-----------|-----------|
| G1 | Pierre Emerson Calderon Rivera | Fiorella del Rocio Becerril Mercado | Fabricio Luna Palacios | Luis Gabriel Guevara Vega | |
| G2 | Renato Christian Gates Rojas | Rodrigo Andres Norabuena Mascaraqui | Ana Karen Zamalloa Lima | Ina Lizbeth Huaman Malpartida | |
| G3 | Gabriela Sthefany Pozo Bornás | Josselin Andrea Yauri Condor | Isabella Albarran Chavez | Diego Enrique Sime Rendon | |
| G4 | Erika Jeaneth Mamani Paasaca | Valeria Alejandra Vicente Vasquez | Diana Adriana Garces Garcia | Maryorit Valeria Morales Gomez | |
| G5 | Victor Guardia Fiestas | Oscar Andres Chavez Inocente | Alvaro Ruben Carhuamaca Remigio | Oscar Nicolas Romero Asparrin | |
| G6 | Zulema Denisse Pumacahua Huatangari | Frank Pinares Gutierrez | Josue Alonso Soria Vasquez | Jonatan Carlo Amaya Mory | |
| G7 | Karen Macedo Pineda | Vilma Barrios Torre | Mirian de la Cruz Condori | Hideki Diego Harada Oyakawa | |
| G8 | Sandy Patricia Martinez Jara | Noelia Fernanda Leon Ruiz | Melina Rozas Acurio | Andrea Luciana Calderon Abanto | |
| G9 | Victor Eduardo Roman Lazarte | Amanda Valery Gomez Flores | Roddy Edison Huarhua Rojas | Jhanela Luz Carhuaz Fuster | |
| G10 | Estefanny Diana Mejía Lazo | Nicolas Silva Andujar | Luz María Supo Zapata | Marco Antonio Andrés Virú Lucas | |
| G11 | Ivette Carolina Mamani Flores | Luz Eliana Camacho Cardenas | Alessandra Valeria Murga Rimac | Flavia Romero Piedra | |
| G12 | Claudia Andrea Perez Pardo | Ximena Alejandra Pinillos Zegarra | Greicy Dana Rodriguez Coronel | Alexander German Ramos Choque | |
| G13 | Cristian Moises Wong Pagan | Jose Pablo Navarro Nateros | Lory Rosario Acosta Carbajal | Lucia Alejandra Pulido Tarrillo | Fiorella Vanessa Ampuero Cherrez |

---

## Estructura del repositorio

```
.
├── sessions/          una carpeta por clase: notebook + README
├── assignments/       enunciados de las tareas
├── scripts/           fetch_data.py
├── data/              datasets (no versionados, se descargan)
└── archive/           material de años anteriores
    ├── lectures-legacy/       notebooks 2022-2025
    └── entregas-2022-2025/    trabajos de participantes
```

## Continúa en

**Python Intermedio** (7 al 31 de octubre): scraping con Selenium, RAG y
embeddings, MCP, agentes y despliegue.
