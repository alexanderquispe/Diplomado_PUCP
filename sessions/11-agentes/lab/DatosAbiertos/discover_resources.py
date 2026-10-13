"""Discover CKAN package/resource IDs for catalog_curated.py."""
import json
import sys

import requests

BASE = "https://www.datosabiertos.gob.pe/api/3/action"
TIMEOUT = 20
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DatosAbiertos-Lab/1.0)",
    "Accept": "application/json",
}

from catalog_curated import CURATED

SEARCHES = [
    ("health", "ipress minsa", None),
    ("education", "alumnos matriculados", None),
]


def ckan(action: str, **params):
    r = requests.get(f"{BASE}/{action}", params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if not data.get("success"):
        raise RuntimeError(data.get("error", data))
    return data["result"]


def pick_datastore_resource(package_id: str) -> dict | None:
    pkg = ckan("package_show", id=package_id)
    for res in pkg.get("resources", []):
        fmt = (res.get("format") or "").upper()
        if res.get("datastore_active") or fmt in ("CSV", "JSON"):
            return {
                "package_id": package_id,
                "package_title": pkg.get("title"),
                "resource_id": res["id"],
                "name": res.get("name"),
                "format": res.get("format"),
                "datastore_active": res.get("datastore_active"),
            }
    return None


def search_best(q: str, organization: str | None = None) -> list[dict]:
    params = {"q": q, "rows": 8}
    if organization:
        params["fq"] = f'organization:{organization}'
    result = ckan("package_search", **params)
    out = []
    for ds in result.get("results", []):
        pid = ds["name"]
        picked = pick_datastore_resource(pid)
        if picked:
            out.append(picked)
    return out


def main():
    print("=== CKAN resource discovery (datosabiertos.gob.pe) ===\n")
    all_hits = {}
    for key, q, org in SEARCHES:
        print(f"--- {key}: q={q!r} org={org} ---")
        try:
            hits = search_best(q, org)
        except Exception as e:
            print(f"  ERROR: {e}")
            hits = []
        for h in hits[:3]:
            print(f"  package={h['package_id']}")
            print(f"    resource_id={h['resource_id']}  format={h['format']}  datastore={h['datastore_active']}")
        all_hits[key] = hits
        print()

    print("\n--- catalog_curated.py (configured) ---")
    for key, entry in CURATED.items():
        picked = pick_datastore_resource(entry["package_id"])
        rid = entry["resource_id"]
        ok = picked and picked["resource_id"] == rid
        print(f"  {key}: package={entry['package_id']} resource={rid[:8]}... ok={ok}")

    print("\n=== Suggested CURATED entries (copy to catalog_curated.py) ===")
    health = (all_hits.get("health") or [None])[0]
    edu = (all_hits.get("education") or [None])[0]
    if health:
        print(json.dumps({"health_establishments": health}, indent=2, ensure_ascii=False))
    if edu:
        print(json.dumps({"education_enrollment": edu}, indent=2, ensure_ascii=False))
    if not health or not edu:
        print("WARNING: missing health or education resource — fix catalog manually.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
