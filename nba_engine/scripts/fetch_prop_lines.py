"""Fetch sportsbook player-prop lines for a slate's games that have not started. Usage: python scripts/fetch_prop_lines.py [YYYY-MM-DD US Eastern]
Env: ODDS_API_KEY (required), PROP_MARKETS (comma list, default 5 core markets), PROP_BOOKS (default draftkings,fanduel), ODDS_RESERVE (default 40 credits)."""
import os, sys, json, sqlite3
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.props import fetch_slate
day = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else str(datetime.now(ZoneInfo("America/New_York")).date())
live = sqlite3.connect("artifacts/live.sqlite"); now = datetime.now(timezone.utc); games = []
for gid, dj in live.execute("select game_id, details_json from forecasts where model_name='sim_mc'"):
    d = json.loads(dj)
    if d.get("date") != day: continue
    tip = d.get("tip_utc")
    if tip and datetime.fromisoformat(tip.replace("Z", "+00:00")) <= now: continue          # started: the pre-game line is gone, do not spend credits
    games.append({"game_id": gid, "home": d["home"], "away": d["away"]})
print(f"{day}: {len(games)} games not started")
try:
    res = fetch_slate("artifacts/player_live.sqlite", games, os.environ.get("PROP_MARKETS") or "player_points,player_rebounds,player_assists,player_threes,player_points_rebounds_assists",
                      os.environ.get("PROP_BOOKS") or "draftkings,fanduel", int(os.environ.get("ODDS_RESERVE") or 40))
except Exception as ex:          # never fails the job: the picks fall back to stand-in lines
    res = {"failed": f"{type(ex).__name__}: {ex}"}
print(res)
