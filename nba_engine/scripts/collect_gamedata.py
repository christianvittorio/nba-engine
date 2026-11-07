"""Fetch ESPN game summaries for a date range and store the raw game data (plays, shot coordinates, quarter scores, officials, odds, team stats).
Usage: python scripts/collect_gamedata.py FROM TO [pause_s]     (dates YYYY-MM-DD, US Eastern game dates; run from GitHub Actions, ESPN is blocked elsewhere)"""
import os, sys
from datetime import date, timedelta
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.feed import EspnFeed
from nbaengine.gamedata import collect_from_feed

a, b = date.fromisoformat(sys.argv[1]), date.fromisoformat(sys.argv[2])
feed = EspnFeed(pause_s=float(sys.argv[3]) if len(sys.argv) > 3 else 0.6)
d, n = a, 0
while d <= b:
    feed.summaries.clear()
    try:
        feed.scoreboard(d.strftime("%Y%m%d"))
        k = collect_from_feed(feed)
        n += k
        print(d, k, "games", flush=True)
    except Exception as ex:
        print(d, "failed:", type(ex).__name__, ex, flush=True)
    d += timedelta(days=1)
print("done", n, "games")
