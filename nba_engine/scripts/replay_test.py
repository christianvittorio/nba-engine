"""Replay the 2025-26 season through the daily loop as if it were live (offline end-to-end test)."""
import json, os, sys, time
from datetime import date, timedelta
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import pandas as pd
from nbaengine.feed import ReplayFeed
from nbaengine.store import Store
from nbaengine.pipeline import Engine, run_update, monitor, last_success
from nbaengine.backtest import evaluate, metrics

N_SIMS = int(os.environ.get("N_SIMS", 2000))
DB, STATE = "artifacts/replay_live.sqlite", "artifacts/replay_state.json"
if os.path.exists(DB): os.remove(DB)
os.system(f"cp artifacts/state_through2025.json {STATE}")
games = pd.read_csv("data/processed/games_2025_cdn.csv")
feed = ReplayFeed(games)

class FlakyFeed:      # raises on one chosen day to prove failures are recorded, not hidden
    def __init__(self, inner, bad): self.inner, self.bad = inner, bad
    def scoreboard(self, d):
        if d == self.bad: raise ConnectionError("simulated outage")
        return self.inner.scoreboard(d)

store = Store(DB)
eng = Engine.load(store, STATE)
d0, d1 = date.fromisoformat(games.date.min()), date.fromisoformat(games.date.max()) + timedelta(days=1)
bad_day = date(2025, 12, 10)
t0, day, n_fail = time.time(), d0, 0
while day <= d1:
    f = FlakyFeed(feed, (bad_day - timedelta(days=0)).strftime("%Y%m%d")) if day == bad_day else feed
    s = run_update(eng, f, day, n_sims=N_SIMS, now_iso=f"{day}T12:00:00Z")
    if not s["ok"]: n_fail += 1; print("run failed (expected once):", day, s["error"])
    eng.save_state(STATE)
    if (day - d0).days % 40 == 39:                      # prove state survives a restart
        store.commit(); eng = Engine.load(Store(DB), STATE); store = eng.store
    day += timedelta(days=1)
print(f"replayed {(d1 - d0).days + 1} days in {time.time() - t0:.0f}s, failed runs: {n_fail}")
store.commit()
df = evaluate(store)
pd.set_option("display.width", 200)
print(metrics(df).round(4).T)
print(monitor(store, window=300))
print("games forecast:", df.game_id.nunique(), "| runs:", store.con.execute("SELECT COUNT(*), SUM(ok) FROM runs").fetchone())
print("last successful refresh:", last_success(store))
# duplicates / immutability
print("duplicate forecast keys:", store.con.execute("SELECT COUNT(*) FROM (SELECT 1 FROM forecasts GROUP BY season,game_id,model_name HAVING COUNT(*)>1)").fetchone()[0])
df.to_pickle("artifacts/replay_eval_frame.pkl")
