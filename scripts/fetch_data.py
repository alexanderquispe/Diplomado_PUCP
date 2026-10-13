"""Descarga los datasets del curso desde Hugging Face.

Uso:
    uv run python scripts/fetch_data.py                # todo
    uv run python scripts/fetch_data.py 03-pandas      # solo una sesion
    uv run python scripts/fetch_data.py 07-raster      # laboratorio de raster

Los datos quedan en data/ y no se versionan.
"""

import shutil
import sys
from pathlib import Path

REPO_ID = "aquiro1994/diplomado-pucp-python"
ROOT = Path(__file__).resolve().parent.parent

# El laboratorio de raster usa datos de otro dataset, donde estan bajo una ruta
# antigua. Sus notebooks los abren por nombre ("Prec_raster.tif"), asi que deben
# quedar en la misma carpeta que el notebook y no en data/.
RASTER_REPO_ID = "aquiro1994/ds-python-up"
RASTER_SOURCE = "Labs/Python_Notebooks/LAB7"
RASTER_TARGET = ROOT / "sessions" / "07-raster" / "lab"
RASTER_FILES = [
    "Prec_raster.tif",
    "tmax_raster.tif",
    "tmin_raster.tif",
    "shape_file/*",
    "Rios_quebradas_ANA_geogpsperu_SuyoPomalia.*",
]


def fetch_raster_lab() -> None:
    from huggingface_hub import snapshot_download

    cache = ROOT / "data" / ".cache" / "ds-python-up"
    snapshot_download(
        repo_id=RASTER_REPO_ID,
        repo_type="dataset",
        local_dir=cache,
        allow_patterns=[f"{RASTER_SOURCE}/{name}" for name in RASTER_FILES],
        ignore_patterns=["*.zip"],
    )
    shutil.copytree(cache / RASTER_SOURCE, RASTER_TARGET, dirs_exist_ok=True)
    print(f"Datos del laboratorio en: {RASTER_TARGET}")


def main(subset: str | None = None) -> None:
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        sys.exit("Falta huggingface_hub:  uv add huggingface-hub")

    if subset == "07-raster":
        fetch_raster_lab()
        return

    patterns = [f"{subset}/**"] if subset else None
    path = snapshot_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        local_dir=ROOT / "data",
        allow_patterns=patterns,
    )
    print(f"Datos en: {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
