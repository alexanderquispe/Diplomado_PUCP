"""MCP server for datosabiertos.gob.pe (CKAN/DKAN API)."""
from __future__ import annotations

import io
import json
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from mcp.server.fastmcp import FastMCP

from catalog_curated import CURATED, MAX_RECORDS_PER_RESOURCE

mcp = FastMCP("datosabiertos")

BASE_URL = "https://www.datosabiertos.gob.pe/api/3/action"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DatosAbiertos-Lab/1.0)",
    "Accept": "application/json",
}
TIMEOUT = 20
MAX_LIMIT = 500


def ckan_get(action: str, params: dict | None = None) -> dict:
    """Call a CKAN action and normalize success/error."""
    url = f"{BASE_URL}/{action}"
    try:
        response = requests.get(url, params=params or {}, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        text = response.content.decode("utf-8-sig").strip()
        if not text.startswith("{"):
            return {"error": "Non-JSON response from CKAN API", "action": action}
        data = json.loads(text)
    except requests.exceptions.RequestException as exc:
        return {"error": str(exc), "action": action}
    except json.JSONDecodeError as exc:
        return {"error": f"Invalid JSON: {exc}", "action": action}

    if not data.get("success"):
        return {"error": data.get("error", "CKAN request failed"), "action": action}
    return {"result": data.get("result")}


def _normalize_package_show(result: Any) -> dict | None:
    if isinstance(result, list):
        return result[0] if result else None
    if isinstance(result, dict):
        return result
    return None


def _records_from_dataframe(df: pd.DataFrame, limit: int) -> tuple[list[dict], list[dict]]:
    df = df.head(limit)
    fields = [{"id": str(c), "type": "text"} for c in df.columns]
    records = json.loads(df.to_json(orient="records", force_ascii=False))
    return records, fields


def _fetch_via_csv(url: str, encoding: str, limit: int) -> dict:
    try:
        response = requests.get(url, headers=HEADERS, timeout=60)
        response.raise_for_status()
        df = pd.read_csv(io.BytesIO(response.content), encoding=encoding, low_memory=False)
        records, fields = _records_from_dataframe(df, min(limit, MAX_LIMIT))
        return {
            "records": records,
            "fields": fields,
            "total": len(df),
            "source": "csv_download",
        }
    except Exception as exc:
        return {"error": str(exc), "source": "csv_download"}


def fetch_resource_data(
    resource_id: str,
    limit: int = 100,
    offset: int = 0,
    filters: dict | None = None,
    q: str | None = None,
    fields: list[str] | None = None,
    sort: str | None = None,
    download_url: str | None = None,
    encoding: str = "utf-8",
) -> dict:
    """Datastore search with CSV fallback for resources not in DataStore."""
    limit = min(max(1, limit), MAX_LIMIT)
    params: dict[str, Any] = {
        "resource_id": resource_id,
        "limit": limit,
        "offset": max(0, offset),
    }
    if filters:
        params["filters"] = json.dumps(filters)
    if q:
        params["q"] = q
    if fields:
        params["fields"] = fields
    if sort:
        params["sort"] = sort

    raw = ckan_get("datastore_search", params)
    if "error" not in raw:
        result = raw.get("result") or {}
        records = result.get("records") or []
        if records:
            return {
                "resource_id": resource_id,
                "records": records[:limit],
                "fields": result.get("fields", []),
                "total": result.get("total", len(records)),
                "source": "datastore",
            }

    if download_url:
        csv_result = _fetch_via_csv(download_url, encoding, limit)
        if "error" not in csv_result:
            csv_result["resource_id"] = resource_id
            csv_result["offset"] = offset
            return csv_result
        return {"error": csv_result["error"], "resource_id": resource_id}

    err = raw.get("error", "No records returned")
    return {"error": err, "resource_id": resource_id}


def _search_via_package_list(q: str, rows: int, start: int) -> dict:
    listed = ckan_get("package_list")
    if "error" in listed:
        return listed
    names = listed.get("result") or []
    q_lower = q.lower()
    tokens = [t for t in q_lower.split() if t]
    matched = [
        n
        for n in names
        if q_lower in n.lower() or all(t in n.lower() for t in tokens)
    ]
    sliced = matched[start : start + rows]
    results = []
    for name in sliced:
        shown = get_dataset(name)
        if "error" not in shown:
            results.append(shown)
    return {
        "count": len(matched),
        "results": results,
        "search_backend": "package_list_filter",
    }


@mcp.tool()
def search_datasets(
    q: str,
    rows: int = 10,
    start: int = 0,
    organization: str | None = None,
) -> dict:
    """
    Search open datasets on datosabiertos.gob.pe.
    Uses package_search when available; falls back to filtering package_list.
    """
    params: dict[str, Any] = {"q": q, "rows": min(rows, 50), "start": start}
    if organization:
        params["fq"] = f"organization:{organization}"

    raw = ckan_get("package_search", params)
    if "error" not in raw:
        return raw.get("result") or {}

    return _search_via_package_list(q, rows, start)


@mcp.tool()
def get_dataset(name_or_id: str) -> dict:
    """Return dataset metadata and resource list (package_show)."""
    raw = ckan_get("package_show", {"id": name_or_id})
    if "error" in raw:
        return raw
    pkg = _normalize_package_show(raw.get("result"))
    if not pkg:
        return {"error": f"Dataset not found: {name_or_id}"}
    resources = [
        {
            "id": r.get("id"),
            "name": r.get("name"),
            "format": r.get("format"),
            "url": r.get("url"),
            "datastore_active": r.get("datastore_active"),
        }
        for r in pkg.get("resources", [])
    ]
    return {
        "id": pkg.get("id"),
        "name": pkg.get("name"),
        "title": pkg.get("title"),
        "organization": (pkg.get("organization") or {}).get("title")
        if isinstance(pkg.get("organization"), dict)
        else pkg.get("organization"),
        "notes": (pkg.get("notes") or "")[:500],
        "resources": resources,
    }


@mcp.tool()
def datastore_search(
    resource_id: str,
    limit: int = 100,
    offset: int = 0,
    filters: dict | None = None,
    q: str | None = None,
    fields: list[str] | None = None,
    sort: str | None = None,
) -> dict:
    """
    Query a DataStore table by resource_id.
    Falls back to CSV download for curated resources when DataStore is empty.
    """
    meta = None
    for entry in CURATED.values():
        if entry["resource_id"] == resource_id:
            meta = entry
            break
    return fetch_resource_data(
        resource_id=resource_id,
        limit=limit,
        offset=offset,
        filters=filters,
        q=q,
        fields=fields,
        sort=sort,
        download_url=meta.get("download_url") if meta else None,
        encoding=meta.get("encoding", "utf-8") if meta else "utf-8",
    )


@mcp.tool()
def list_organizations(rows: int = 50) -> dict:
    """List publisher organizations on the portal."""
    raw = ckan_get("organization_list", {"all_fields": True})
    if "error" in raw:
        return raw
    orgs = raw.get("result") or []
    return {"count": len(orgs), "organizations": orgs[: min(rows, 100)]}


def build_health_edu_snapshot(limit_per_resource: int = 200) -> dict:
    limit_per_resource = min(max(1, limit_per_resource), MAX_RECORDS_PER_RESOURCE)
    out: dict[str, Any] = {
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "datasets": {},
        "errors": {},
    }
    for key, entry in CURATED.items():
        data = fetch_resource_data(
            resource_id=entry["resource_id"],
            limit=limit_per_resource,
            download_url=entry.get("download_url"),
            encoding=entry.get("encoding", "utf-8"),
        )
        if "error" in data:
            out["errors"][key] = data["error"]
        else:
            out["datasets"][key] = {
                "package_id": entry["package_id"],
                "title": entry["title"],
                "description": entry["description"],
                "resource_id": entry["resource_id"],
                "records": data.get("records", []),
                "fields": data.get("fields", []),
                "total": data.get("total", 0),
                "source": data.get("source"),
                "chart_hints": entry.get("chart_hints", {}),
            }
    return out


@mcp.tool()
def get_health_edu_snapshot(limit_per_resource: int = 200) -> dict:
    """
    Fetch curated health (IPRESS) and education (matrícula) datasets in one call.
    Use when building or updating the Streamlit dashboard.
    """
    return build_health_edu_snapshot(limit_per_resource)


if __name__ == "__main__":
    mcp.run()
