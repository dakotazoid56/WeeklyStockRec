import os
from dotenv import load_dotenv
load_dotenv()

from news import fetch_headlines, map_headlines_to_tickers
#from alpha import get_price, get_overview
from yahooFinance import get_price, get_overview
from scoring import aggregate_features, pick_winner
from slack import send_slack
from utils import format_sms




def run_once():
    raw = fetch_headlines()
    mapped = map_headlines_to_tickers(raw)
    if not mapped:
        send_slack("No pick: not enough relevant headlines this week.")
        return
    feats = aggregate_features(mapped)
    quotes = {}
    overviews = {}
    for t in feats.keys():
        quotes[t] = get_price(t)
        overviews[t] = get_overview(t)
    winner, row = pick_winner(feats, quotes, overviews)
    if not winner:
        send_slack("No pick: filters removed all candidates.")
        return
    body = format_sms(winner, row)
    send_slack(body)

if __name__ == "__main__":
    run_once()
