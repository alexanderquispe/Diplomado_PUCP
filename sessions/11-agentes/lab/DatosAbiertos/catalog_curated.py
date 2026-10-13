"""Curated datasets for the health + education lab snapshot."""

CURATED = {
    "health_establishments": {
        "package_id": "minsa-ipress",
        "resource_id": "7cf96151-5ddf-4281-90ba-b2b0407447ab",
        "title": "MINSA - IPRESS",
        "description": "Establecimientos de salud (RENIPRESS / IPRESS)",
        "download_url": "https://www.datosabiertos.gob.pe/sites/default/files/recursos/2017/09/IPRESS.csv",
        "encoding": "latin-1",
        "chart_hints": {
            "group_by": ["Departamento", "DEPARTAMENTO", "departamento"],
            "category": ["Tipo", "TIPO", "tipo", "Clasificación", "Clasificacion"],
        },
    },
    "education_enrollment": {
        "package_id": "alumnos-matriculados",
        "resource_id": "e276da3f-a009-4547-9e76-c814e14fc574",
        "title": "Alumnos matriculados",
        "description": "Matrícula escolar 2016-2022 (MINEDU / portal nacional)",
        "download_url": "https://www.datosabiertos.gob.pe/sites/default/files/Matriculados_2016_al_2022.csv",
        "encoding": "utf-8",
        "chart_hints": {
            "year": ["Año Matrícula", "Ano Matricula", "AÑO MATRÍCULA"],
            "region": [
                "Departamento\nColegio",
                "Departamento Colegio",
                "DEPARTAMENTO COLEGIO",
            ],
            "gender": ["Género", "Genero", "GÉNERO"],
        },
    },
}

MAX_RECORDS_PER_RESOURCE = 500
