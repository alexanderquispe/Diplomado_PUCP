import requests, json

BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"

def fetch(code, start, end):
    url = f"{BASE}/{code}/json/{start}/{end}"
    r = requests.get(url, timeout=15)
    raw = r.content.decode("utf-8-sig")
    try:
        return json.loads(raw)
    except Exception as e:
        return {"error": str(e), "periods": []}

results = {
    "inflation":     fetch("PN01271PM", "2021-01", "2026-05"),
    "gdp":           fetch("PN01773AM", "2021-01", "2026-05"),
    "interest_rate": fetch("PN07819NM", "2021-01", "2026-05"),
    "exchange_rate": fetch("PN01234PM", "2021-01", "2026-05"),
    "trade_balance": fetch("PN01781AM", "2021-01", "2026-05"),
}

for k, v in results.items():
    p = v.get("periods", [])
    first = p[0] if p else "NONE"
    last  = p[-1] if p else "NONE"
    print(f"{k}: {len(p)} periods | first={first} | last={last}")

with open("bcrp_data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False)

print("\nbcrp_data.json saved OK")
