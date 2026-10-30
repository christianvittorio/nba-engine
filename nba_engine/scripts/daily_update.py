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
LOOKBACK = int(os.environ.get("LOOKBACK_DAYS", 3 if last_success(store) else 21))
summary = run_update(eng, EspnFeed(), today, n_sims=N_SIMS, lookback_days=LOOKBACK)
print(summary)
if summary["ok"]:
    eng.save_state(STATE)       # state is only persisted after a fully successful run
    os.makedirs("artifacts/reports", exist_ok=True)
    print(write_report(store, today, f"artifacts/reports/forecasts_{today}.md"))
else:
    sys.exit(1)
