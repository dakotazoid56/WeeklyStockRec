import os
import requests

ALPHA = os.getenv("ALPHAVANTAGE_KEY")

def _get_json(url: str):
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()

def get_price(symbol: str) -> float | None:
    if not ALPHA:
        raise RuntimeError("Missing ALPHAVANTAGE_KEY")
    url = (
        "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
        f"&symbol={symbol}&apikey={ALPHA}"
    )
    data = _get_json(url)
    try:
        return float(data["Global Quote"]["05. price"])
    except Exception:
        return None

def get_overview(symbol: str) -> dict:
    if not ALPHA:
        raise RuntimeError("Missing ALPHAVANTAGE_KEY")
    url = (
        "https://www.alphavantage.co/query?function=OVERVIEW"
        f"&symbol={symbol}&apikey={ALPHA}"
    )
    data = _get_json(url)
    try:
        mc = float(data.get("MarketCapitalization")) if data.get("MarketCapitalization") else None
    except Exception:
        mc = None
    return {
        "MarketCapitalization": mc,
        "Name": data.get("Name"),
        "Exchange": data.get("Exchange"),
        "Symbol": data.get("Symbol", symbol),
    }
