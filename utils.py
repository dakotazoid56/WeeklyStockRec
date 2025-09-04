import os
from datetime import datetime
import pytz

TZ = pytz.timezone(os.getenv("TIMEZONE", "America/Los_Angeles"))

def now_local_str():
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M %Z")

def format_sms(ticker: str, row: dict) -> str:
    print("Formatting SMS")
    why = (
        f"headline_count={row.get('headline_count')} sentiment={row.get('sentiment_mean'):.2f}"
    )
    refs = " ".join([f"[{i+1}] {u}" for i, u in enumerate(row.get("urls", [])[:3])])
    return (
        f"This week’s $10 pick: {ticker} (score {row.get('score'):.2f}, price ${row.get('price'):.2f})\n"
        f"Why: {why}\n"
        f"Refs: {refs}\n"
        f"{now_local_str()}"
    )
