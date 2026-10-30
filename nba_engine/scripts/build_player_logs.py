"""Build player game logs for seasons (labels 2022..2026) from cdn play-by-play; validate against team-level scores."""
import json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import pandas as pd
from nbaengine.feed import build_games_from_cdn
from nbaengine.players_data import build_player_logs, validate_player_logs

years = [int(y) for y in sys.argv[1:]] or [2021, 2022, 2023, 2024, 2025]
os.makedirs("data/processed", exist_ok=True)
report = {}
for y in years:
    t0 = time.time()
    csv = f"data/raw/cdn{y}/cdnnba_{y}.csv"
    label = y + 1
    games = build_games_from_cdn(csv, label)
    games.to_csv(f"data/processed/games_cdn_{label}.csv", index=False)
    pg = build_player_logs(csv, label)
    home = games.set_index("game_id")
    pg = pg.merge(games[["game_id", "date", "home", "away"]], on="game_id", how="left")
    pg["is_home"] = (pg["team"] == pg["home"]).astype(int)
    pg["opp"] = pg["away"].where(pg["is_home"] == 1, pg["home"])
    pg = pg.drop(columns=["home", "away"])
    pg.to_csv(f"data/processed/player_games_{label}.csv", index=False)
    rep, tm = validate_player_logs(pg, games)
    report[label] = rep
    print(label, f"{time.time()-t0:.0f}s", len(pg), "rows", json.dumps({k: round(v, 4) if isinstance(v, float) else v for k, v in rep.items()}))
json.dump(report, open("artifacts/player_logs_validation.json", "w"), indent=2)
