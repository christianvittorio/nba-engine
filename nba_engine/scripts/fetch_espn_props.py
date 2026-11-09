"""Fetch ESPN's keyless DraftKings player props. Usage: python scripts/fetch_espn_props.py FROM_DATE [TO_DATE] (US Eastern, YYYY-MM-DD; default today).
Takes every game the engine stored for those dates (finished games keep their last pre-tip lines, so history can be backfilled for grading)."""
import os, sys, json, sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.espnprops import fetch_event, store
a = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else str(datetime.now(ZoneInfo("America/New_York")).date()); b = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else a
av = json.load(open("artifacts/availability.json")); roster = {}
for t in av["teams"].values():
    for r in t.get("roster", []):
        if r.get("espn_id") is not None: roster[int(r["espn_id"])] = (r.get("nba_id"), r.get("name"))
live = sqlite3.connect("artifacts/live.sqlite")
gids = [g for g, d in live.execute("select game_id, date from game_dates where date between ? and ? order by date, game_id", (a, b))]
tot = 0
for g in gids:
    try:
        rows = fetch_event(g, roster); n = store("artifacts/player_live.sqlite", g, rows); tot += n
        print(g, n, "lines,", sum(1 for r in rows if r[1] is None), "without a matched player")
    except Exception as ex:
        print(g, "failed:", type(ex).__name__, ex)
print("total", tot)
