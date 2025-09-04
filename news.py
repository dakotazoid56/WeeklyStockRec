import os
import time
import pytz
import requests
from datetime import datetime, timedelta, timezone
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tickers import UNIVERSE

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
MAX_AGE_DAYS = int(os.getenv("MAX_HEADLINE_AGE_DAYS", "7"))
TZ = pytz.timezone(os.getenv("TIMEZONE", "America/Los_Angeles"))

analyzer = SentimentIntensityAnalyzer()

def _since_date_iso(days: int) -> str:
    now = datetime.now(timezone.utc)
    return (now - timedelta(days=days)).isoformat()

def fetch_headlines() -> list:
    print("Fetching Headlines")
    if not NEWSAPI_KEY:
        raise RuntimeError("Missing NEWSAPI_KEY")
    topics = ["business", "technology"]
    all_items = []
    since = _since_date_iso(MAX_AGE_DAYS)
    for topic in topics:
        url = (
            "https://newsapi.org/v2/top-headlines"
            f"?category={topic}&language=en&pageSize=100&apiKey={NEWSAPI_KEY}"
        )
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        for a in data.get("articles", []):
            if not a.get("title") or not a.get("url"):
                continue
            published_at = a.get("publishedAt") or _since_date_iso(MAX_AGE_DAYS)
            all_items.append({
                "title": a["title"],
                "url": a["url"],
                "published_at": published_at,
                "source": (a.get("source") or {}).get("name")
            })
        time.sleep(0.2)
    cutoff = datetime.fromisoformat(since)
    fresh = [x for x in all_items if datetime.fromisoformat(x["published_at"]) >= cutoff]
    seen = set()
    deduped = []
    for x in fresh:
        if x["url"] in seen:
            continue
        seen.add(x["url"])
        deduped.append(x)
    return deduped

def map_headlines_to_tickers(items: list) -> list:
    print("Mapping Headlines to Tickers")
    out = []
    for x in items:
        title_upper = x["title"].upper()
        hits = set()
        for name, ticker in UNIVERSE.items():
            if name in title_upper:
                hits.add(ticker)
        if not hits:
            continue
        sentiment = analyzer.polarity_scores(x["title"])['compound']
        out.append({**x, "tickers": hits, "sentiment": sentiment})
    return out
