"""End-to-end demo: load -> validate -> forecast (Elo, baseline, Monte Carlo) -> save -> evaluate."""
import json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import pandas as pd
from nbaengine import MODEL_VERSION
from nbaengine.data import load_pbp_games, validate_games, sha256
from nbaengine.elo import EloParams
from nbaengine.store import Store
from nbaengine.backtest import run_backtest, evaluate, metrics, calibration_table

N_SIMS = int(os.environ.get("N_SIMS", 2000))
DB = os.environ.get("DB", "artifacts/nba_engine.sqlite")
if os.path.exists(DB):
    os.remove(DB)   # fresh demo database (forecast rows are immutable once written)

games, manifest = load_pbp_games("data/raw/pbp_extract", [2021, 2022, 2023, 2024], "data/processed")
rep = validate_games(games)
print("validation:", rep.to_json())
assert rep.ok

ep = json.load(open("artifacts/elo_params.json"))["params"]
store = Store(DB)
store.add_source(name="shufinskiy/nba_data nbastats play-by-play 2021-22..2024-25",
                 url="https://github.com/shufinskiy/nba_data (commit e829d46, git clone)",
                 retrieved_at_utc=open("data/raw/pbp_extract/retrieved_at").read().strip() if os.path.exists("data/raw/pbp_extract/retrieved_at") else "2026-10-17",
                 season_coverage="regular season 2021-22 .. 2024-25 (4 x 1230 games)",
                 sha256=json.dumps(manifest), reliability="derived from stats.nba.com PBP; 27/4920 games fail point reconciliation",
                 limitations="no calendar dates (schedule-order proxy), no injuries/lineups/odds, regular season only")
store.add_source(name="FiveThirtyEight nbaallelo.csv", url="https://github.com/fivethirtyeight/data/tree/master/nba-elo",
                 retrieved_at_utc=open("data/raw/nbaallelo.retrieved_at").read().strip(),
                 season_coverage="1947-2015", sha256=sha256("data/raw/nbaallelo.csv"),
                 reliability="Basketball-Reference derived", limitations="ends 2015; used only for Elo hyper-parameter tuning")

t0 = time.time()
cal = run_backtest(games, store, EloParams(**ep), warmup_seasons=[2022], calib_season=2023,
                   eval_seasons=[2024, 2025], n_sims=N_SIMS)
print(f"backtest wall time {time.time()-t0:.0f}s with {N_SIMS} sims/game")

df = evaluate(store)
m = metrics(df)
pd.set_option("display.width", 200); pd.set_option("display.max_columns", 30)
print(m.round(4).T)
for name in ("sim_mc", "elo"):
    print(f"\ncalibration: {name}"); print(calibration_table(df, name))
m.round(5).to_csv("artifacts/metrics_overall.csv")
df.to_pickle("artifacts/eval_frame.pkl")
print("done")
