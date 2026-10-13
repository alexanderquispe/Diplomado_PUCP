from mcp.server.fastmcp import FastMCP
import requests
from datetime import datetime

mcp = FastMCP("bcrp")

BASE_URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"

SERIES = {
    "inflation":     "PN01271PM",  # IPC variación mensual
    "exchange_rate": "PN01234PM",  # Tipo de cambio promedio mensual USD/PEN
    "gdp":           "PN01773AM",  # PBI desestacionalizado
    "interest_rate": "PN07819NM",  # Tasa de interés referencial BCRP
    "trade_balance": "PN01781AM",  # Exportaciones acumuladas (millones USD)
    "reserves":      "PN01265GM",  # Reservas internacionales netas
}


def fetch_series(series_code: str, start: str, end: str) -> dict:
    url = f"{BASE_URL}/{series_code}/json/{start}/{end}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "series": series_code}


@mcp.tool()
def get_inflation(start: str, end: str) -> dict:
    """
    Get monthly CPI inflation rate for Peru (IPC variación mensual).
    start/end format: YYYY-MM  e.g. '2024-01'
    Returns monthly percentage variation.
    """
    return fetch_series(SERIES["inflation"], start, end)


@mcp.tool()
def get_exchange_rate(start: str, end: str) -> dict:
    """
    Get daily USD/PEN exchange rate (tipo de cambio bancario venta).
    start/end format: YYYY-MM-DD  e.g. '2024-01-01'
    Returns soles per USD.
    """
    return fetch_series(SERIES["exchange_rate"], start, end)


@mcp.tool()
def get_gdp(start: str, end: str) -> dict:
    """
    Get seasonally adjusted monthly GDP index for Peru (PBI desestacionalizado).
    start/end format: YYYY-MM  e.g. '2024-01'
    """
    return fetch_series(SERIES["gdp"], start, end)


@mcp.tool()
def get_interest_rate(start: str, end: str) -> dict:
    """
    Get BCRP reference interest rate (tasa de política monetaria).
    start/end format: YYYY-MM  e.g. '2024-01'
    Returns annual percentage rate.
    """
    return fetch_series(SERIES["interest_rate"], start, end)


@mcp.tool()
def get_trade_balance(start: str, end: str) -> dict:
    """
    Get Peru monthly trade balance in millions of USD (balanza comercial).
    Positive = surplus, negative = deficit.
    start/end format: YYYY-MM  e.g. '2024-01'
    """
    return fetch_series(SERIES["trade_balance"], start, end)


@mcp.tool()
def get_macro_snapshot(months: int = 12) -> dict:
    """
    Get all key macro indicators for the last N months in one call.
    Use this when building or updating the complete dashboard.
    Returns inflation, GDP, exchange rate, interest rate, and trade balance.
    months: number of months to fetch (default 12, max 24)
    """
    now = datetime.now()
    end = now.strftime("%Y-%m")
    start_year = now.year - 1 if months > 12 else now.year
    start_month = now.month
    start = f"{start_year}-{start_month:02d}"

    return {
        "inflation":     fetch_series(SERIES["inflation"], start, end),
        "gdp":           fetch_series(SERIES["gdp"], start, end),
        "interest_rate": fetch_series(SERIES["interest_rate"], start, end),
        "trade_balance": fetch_series(SERIES["trade_balance"], start, end),
        "exchange_rate": fetch_series(
            SERIES["exchange_rate"],
            f"{start_year}-{start_month:02d}-01",
            now.strftime("%Y-%m-%d"),
        ),
        "fetched_at": now.strftime("%Y-%m-%d %H:%M"),
        "period_months": months,
    }


if __name__ == "__main__":
    mcp.run()
