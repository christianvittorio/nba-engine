"""Build the modern-era Elo (home advantage 45, K 20, carryover 0.7) from stored history and add it to artifacts/state.json as `elo2`.
Replays the 2022-2026 results and then the live-season results in order. Safe to rerun (rebuilds from scratch)."""
import os, sys, json, sqlite3
import pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.elo import Elo, EloParams
prm = EloParams(k=20, home_adv=45, carryover=0.7, init=1505.0, mov_scale=1.0)
fr = []
for y in (2022, 2023, 2024, 2025, 2026):
    d = pd.read_csv(f"data/processed/games_cdn_{y}.csv", usecols=["game_id", "home", "away", "home_pts", "away_pts", "date"]); d["season"] = y; fr.append(d)
g = pd.concat(fr).sort_values(["season", "date", "game_id"])
e = Elo(prm)
for r in g.itertuples(): e.new_season(r.season); e.update(r.home, r.away, r.home_pts, r.away_pts)
c = sqlite3.connect("artifacts/live.sqlite")
for s, h, a, hp, ap in c.execute("select g.season,g.home,g.away,r.home_pts,r.away_pts from games g join results r on r.game_id=g.game_id and r.season=g.season order by g.season,g.seq"):
    e.new_season(s); e.update(h, a, hp, ap)
st = json.load(open("artifacts/state.json")); st["elo2"] = {"params": vars(prm), "ratings": e.ratings, "season": e.season}
json.dump(st, open("artifacts/state.json", "w")); print("elo2 ratings", len(e.ratings), "season", e.season, "top", sorted(e.ratings.items(), key=lambda x: -x[1])[:3])
