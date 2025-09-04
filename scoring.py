from collections import defaultdict
from statistics import mean

MIN_PRICE = 2
MIN_MARKET_CAP = 1_000_000_000

def aggregate_features(mapped_headlines: list) -> dict:
    print("Aggregating Features")
    feats = defaultdict(lambda: {"headline_count": 0, "sentiments": [], "urls": set()})
    for h in mapped_headlines:
        for t in h["tickers"]:
            feats[t]["headline_count"] += 1
            feats[t]["sentiments"].append(h["sentiment"])
            feats[t]["urls"].add(h["url"])
    final = {}
    for t, v in feats.items():
        final[t] = {
            "headline_count": v["headline_count"],
            "sentiment_mean": mean(v["sentiments"]) if v["sentiments"] else 0.0,
            "urls": list(v["urls"])[:5],
        }
    return final

def score_row(row: dict) -> float:
    return (
        0.6 * row.get("sentiment_mean", 0) +
        0.4 * min(row.get("headline_count", 0) / 5.0, 1.0)
    )

def pick_winner(features: dict, quotes: dict, overviews: dict) -> tuple[str, dict]:
    print("Picking Winner")
    candidates = []
    for t, row in features.items():
        px = quotes.get(t)
        ov = overviews.get(t, {})
        mc = ov.get("MarketCapitalization")
        if px is None or mc is None:
            continue
        if px < MIN_PRICE or mc < MIN_MARKET_CAP:
            continue
        row_enriched = {**row, "price": px, "market_cap": mc}
        row_enriched["score"] = score_row(row_enriched)
        candidates.append((t, row_enriched))
    if not candidates:
        return None, {}
    candidates.sort(key=lambda x: x[1]["score"], reverse=True)
    return candidates[0]
