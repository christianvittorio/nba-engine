"""One-off: restart the online scoring-level correction for the live season under the current rule (reset at season start, faster
tracker for the first 60 games) by replaying the live games that have stored raw simulator totals and results. Idempotent.
Reason: the level learned at the end of 2025-26 (+6 points) was carried into 2026-27, where scoring is running about 5-8 points lower."""
import json, os, sqlite3, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import pandas as pd
from nbaengine.pipeline import ALPHA_EARLY, ALPHA_LATE, N_EARLY

st_path, db = os.path.join(ROOT, "artifacts/state.json"), os.path.join(ROOT, "artifacts/live.sqlite")
st = json.load(open(st_path))
c = sqlite3.connect(db)
x = pd.read_sql_query("""SELECT f.season, f.game_id, f.mean_total raw_total, r.home_pts + r.away_pts tot, d.date FROM forecasts f
                         JOIN results r USING(season, game_id) LEFT JOIN game_dates d USING(season, game_id)
                         WHERE f.model_name='sim_mc_raw' ORDER BY d.date, f.game_id""", c)
c.close()
season = int(x.season.max())
x = x[x.season == season]
level, n = 0.0, 0
for r, t in zip(x.raw_total, x.tot):
    a = ALPHA_EARLY if n < N_EARLY else ALPHA_LATE
    level = (1 - a) * level + a * (t - r); n += 1
print(f"season {season}: replayed {n} games; level {st['level_delta']:.2f} -> {level:.2f}")
st["level_delta"], st["level_n"], st["level_season"] = level, n, season
json.dump(st, open(st_path, "w"))
