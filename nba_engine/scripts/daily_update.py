"""Daily self-update: fetch yesterday's results, update state, forecast today's NBA slate, store, report.
Run once a day (see .github/workflows/daily.yml). Exits non-zero if the refresh failed so the failure is visible."""
import os, sys
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.feed import EspnFeed
from nbaengine.store import Store
from nbaengine.pipeline import Engine, run_update, write_report, last_success

STATE, DB = "artifacts/state.json", "artifacts/live.sqlite"
N_SIMS = int(os.environ.get("N_SIMS", 10000))
today = datetime.now(ZoneInfo("America/New_York")).date()
store = Store(DB)
eng = Engine.load(store, STATE)
# First run on a fresh state: catch up on everything since the season opened (ingesting a game twice is a no-op).
LOOKBACK = int(os.environ.get("LOOKBACK_DAYS", 3 if (last_success(store) and os.path.exists("artifacts/player_applied.json")) else 21))
# Rosters + injury statuses first (best effort, never fails the job): used for the injury-adjusted forecasts and the dashboard.
try:
    from nbaengine.availability import build_availability, save_availability
    from nbaengine.injury import make_injury_fn
    from nbaengine.players import PlayerModel
    av = build_availability(EspnFeed(pause_s=0.3), teams=None, player_state_path="artifacts/player_state.json")   # all 30 teams
    save_availability(av, "artifacts/availability.json")
    n_inj = sum(len(t["injuries"]) for t in av["teams"].values())
    print(f"availability: {len(av['teams'])} teams, {n_inj} injury entries, {len(av['unmatched_roster_names'])} roster names "
          f"without history, problems={av['problems'][:3]}")
    eng.injury_fn = make_injury_fn(PlayerModel.load("artifacts/player_state.json"), av)
except Exception as ex:
    print("availability step failed (forecasts unaffected):", type(ex).__name__, ex)
feed = EspnFeed()
summary = run_update(eng, feed, today, n_sims=N_SIMS, lookback_days=LOOKBACK)
print(summary)
if summary["ok"]:
    try:      # player history from ESPN box scores: best effort, must never fail the forecast job
        from nbaengine.playerfeed import update_players
        print("players:", update_players(feed, "artifacts"))
    except Exception as ex:
        print("player update failed (forecasts unaffected):", type(ex).__name__, ex)
    eng.save_state(STATE)       # state is only persisted after a fully successful run
    os.makedirs("artifacts/reports", exist_ok=True)
    print(write_report(store, today, f"artifacts/reports/forecasts_{today}.md"))
else:
    sys.exit(1)
