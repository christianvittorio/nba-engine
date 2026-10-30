"""One-off: advance Elo + team profiles through all history, fit nothing new, and write artifacts/state.json.
Needs the raw/processed game tables (see README). After this, daily_update.py needs only state.json + live.sqlite."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import numpy as np, pandas as pd
from nbaengine import MODEL_VERSION
from nbaengine.data import load_pbp_games
from nbaengine.elo import Elo, EloParams
from nbaengine.sim import TeamProfiles, simulate_game
from nbaengine.backtest import RunningSD
from nbaengine.store import Store
from nbaengine.pipeline import Engine

THROUGH = int(os.environ.get("THROUGH", 2026))          # last season label to include (2026 = 2025-26)
OUT = os.environ.get("STATE", "artifacts/state.json")
DB = os.environ.get("DB", "artifacts/live.sqlite")

pbp, _ = load_pbp_games("data/raw/pbp_extract", [2021, 2022, 2023, 2024], "data/processed")
parts = [pbp]
if THROUGH >= 2026:
    cdn = pd.read_csv("data/processed/games_2025_cdn.csv")
    parts.append(cdn)
g = pd.concat(parts, ignore_index=True)
g = g[g.season <= THROUGH].sort_values(["season", "game_id"]).reset_index(drop=True)

ep = EloParams(**json.load(open("artifacts/elo_params.json"))["params"])
cal = json.load(open("artifacts/nba_engine.sqlite.kappa.json")) if os.path.exists("artifacts/nba_engine.sqlite.kappa.json") else None
if cal is None:
    import sqlite3
    pj = json.loads(sqlite3.connect("artifacts/nba_engine.sqlite").execute(
        "SELECT params_json FROM model_versions WHERE model_name='sim_mc'").fetchone()[0])
    cal = {"kappa_margin": pj["kappa_margin"], "kappa_total": pj["kappa_total"]}
    json.dump(cal, open("artifacts/nba_engine.sqlite.kappa.json", "w"))

elo, prof = Elo(ep), TeamProfiles()
base = {"n": 0.0, "hw": 0.0, "m": 0.0, "t": 0.0}
level_delta, tail_start = 0.0, len(g) - 300
for i, r in enumerate(g.itertuples(index=False)):
    gd = r._asdict()
    elo.new_season(gd["season"]); prof.new_season(gd["season"])
    if i >= tail_start and (i - tail_start) % 3 == 0:     # estimate the current league scoring-level offset
        sim = simulate_game(prof, gd["home"], gd["away"], 400, 1000 + i, 0.0)
        level_delta = 0.9 * level_delta + 0.1 * ((gd["home_pts"] + gd["away_pts"]) - (sim["home_pts"] + sim["away_pts"]).mean()) if level_delta else ((gd["home_pts"] + gd["away_pts"]) - (sim["home_pts"] + sim["away_pts"]).mean())
    elo.update(gd["home"], gd["away"], gd["home_pts"], gd["away_pts"])
    prof.record_pace_residual(prof.expected_poss(gd["home"], gd["away"]), gd)
    prof.update(gd)
    base["n"] += 1; base["hw"] += float(gd["home_pts"] > gd["away_pts"])
    base["m"] += gd["home_pts"] - gd["away_pts"]; base["t"] += gd["home_pts"] + gd["away_pts"]

if os.path.exists(DB): os.remove(DB)
store = Store(DB)
store.add_model_version("sim_mc", MODEL_VERSION, {"bootstrap_through": THROUGH, **cal})
sds = {"elo": RunningSD(13.5), "base_m": RunningSD(13.5), "base_t": RunningSD(18.5)}
eng = Engine(store, elo, prof, cal["kappa_margin"], cal["kappa_total"], level_delta, base, sds, set())
eng.save_state(OUT); store.commit()
top = sorted(elo.ratings.items(), key=lambda kv: -kv[1])[:5]
print(f"bootstrapped through season label {THROUGH}: {len(g)} games, level_delta {level_delta:+.2f}, top Elo {[(t, round(v)) for t, v in top]}")
print("state ->", OUT, os.path.getsize(OUT), "bytes")
