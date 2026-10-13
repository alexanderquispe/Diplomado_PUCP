"""Offline helper: fetch curated snapshot and save to JSON."""
import json

from mcp_datosabiertos_server import build_health_edu_snapshot

OUT = "datosabiertos_snapshot.json"


def main():
    snap = build_health_edu_snapshot(limit_per_resource=200)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    print(f"Saved {OUT}")
    for key, ds in snap.get("datasets", {}).items():
        print(f"  {key}: {len(ds.get('records', []))} records (total={ds.get('total')})")
    if snap.get("errors"):
        print("Errors:", snap["errors"])


if __name__ == "__main__":
    main()
