from __future__ import annotations

from typing import Optional, Dict, Any
import yfinance as yf


def get_price(symbol: str) -> Optional[float]:
    """
    Return the latest price for the given symbol using yfinance.
    Falls back to the most recent close if last price is unavailable.
    """
    try:
        t = yf.Ticker(symbol)
        fi = getattr(t, "fast_info", None)
        if fi:
            px = fi.get("last_price") or fi.get("previous_close") or fi.get("last_close")
            if px is not None:
                return float(px)

        hist = t.history(period="1d", interval="1d")
        if not hist.empty:
            return float(hist["Close"].iloc[-1])
    except Exception as e:
        print(f"[get_price] Error for {symbol}: {e}")
        return None
    return None


def get_overview(symbol: str) -> Dict[str, Any]:
    """
    Return a minimal overview similar to alpha.get_overview:
    {
        "MarketCapitalization": float | None,
        "Name": str | None,
        "Exchange": str | None,
        "Symbol": str,
    }
    """
    name: Optional[str] = None
    exchange: Optional[str] = None
    mc: Optional[float] = None

    try:
        t = yf.Ticker(symbol)

        # Fast path
        fi = getattr(t, "fast_info", None)
        if fi:
            try:
                mc_val = fi.get("market_cap")
                mc = float(mc_val) if mc_val is not None else None
            except Exception:
                mc = None
            exchange = fi.get("exchange") or exchange

        # Additional metadata
        try:
            info = t.get_info()
            name = info.get("shortName") or info.get("longName") or info.get("displayName") or name
            exchange = exchange or info.get("exchange") or info.get("fullExchangeName")
            if mc is None:
                mc_val = info.get("marketCap")
                mc = float(mc_val) if mc_val is not None else None
        except Exception as e:
            print(f"[get_overview] get_info error for {symbol}: {e}")
    except Exception as e:
        print(f"[get_overview] Ticker error for {symbol}: {e}")
    
    return {
        "MarketCapitalization": mc,
        "Name": name,
        "Exchange": exchange,
        "Symbol": symbol.upper(),
    }