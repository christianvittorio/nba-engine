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
LOOKBACK = int(os.environ.get("LOOKBACK_DAYS") or (3 if (last_success(store) and os.path.exists("artifacts/player_applied.json")) else 21))
av = None
# Rosters + injury statuses first (best effort, never fails the job): used for the injury-adjusted forecasts and the dashboard.
try:
    from nbaengine.availability import build_availability, save_availability
    from nbaengine.injury import make_injury_fn, make_avail_fn
    from nbaengine.players import PlayerModel
    av = build_availability(EspnFeed(pause_s=0.3), teams=None, player_state_path="artifacts/player_state.json")   # all 30 teams
    save_availability(av, "artifacts/availability.json")
    n_inj = sum(len(t["injuries"]) for t in av["teams"].values())
    print(f"availability: {len(av['teams'])} teams, {n_inj} injury entries, {len(av['unmatched_roster_names'])} roster names "
          f"without history, problems={av['problems'][:3]}")
    eng.injury_fn = make_injury_fn(PlayerModel.load("artifacts/player_state.json"), av)
    eng.avail_fn = make_avail_fn(PlayerModel.load("artifacts/player_state.json"), av)
except Exception as ex:
    print("availability step failed (forecasts unaffected):", type(ex).__name__, ex)
try:        # back-to-back effect fitted from walk-forward projections (scripts/fit_rest.py)
    import json as _json
    eng.rest_coef = _json.load(open("artifacts/rest_fit.json"))
except Exception as ex:
    print("rest fit not loaded (rest-adjusted forecasts skipped):", type(ex).__name__, ex)
feed = EspnFeed()
summary = run_update(eng, feed, today, n_sims=N_SIMS, lookback_days=LOOKBACK)
print(summary)
if summary["ok"]:
    try:      # player history from ESPN box scores: best effort, must never fail the forecast job
        from nbaengine.playerfeed import update_players
        from nbaengine import player_live as PLV
        PLDB = "artifacts/player_live.sqlite"
        print("players:", update_players(feed, "artifacts", sink=lambda season, eid, df: PLV.store_actuals(PLDB, season, eid, df)))
        try:      # raw game data (plays, shot coordinates, quarter scores, officials, odds, team stats) for the new layers
            from nbaengine.gamedata import collect_from_feed
            print("gamedata:", collect_from_feed(feed, "artifacts/gamedata"), "games stored")
        except Exception as ex:
            print("gamedata failed (forecasts unaffected):", type(ex).__name__, ex)
        try:      # player-stat forecasts for today's games that have a stored team forecast and have not started (calibrated later)
            import json as _j, sqlite3 as _sq
            from datetime import datetime as _dt, timezone as _tz
            from nbaengine.players import PlayerModel as _PM
            _c = _sq.connect(DB)
            _res = set(map(tuple, _c.execute("SELECT season, game_id FROM results").fetchall()))
            _g = []
            for _s, _gid, _dj, _mh, _ma in _c.execute("SELECT season, game_id, details_json, mean_home, mean_away FROM forecasts WHERE model_name='sim_mc'").fetchall():
                _d = _j.loads(_dj)
                if _d.get("date") == str(today) and (_s, _gid) not in _res and _d.get("tip_utc") and \
                        _dt.fromisoformat(_d["tip_utc"].replace("Z", "+00:00")) > _dt.now(_tz.utc):
                    _g.append({"season": _s, "game_id": _gid, "home": _d["home"], "away": _d["away"], "seed": 20261021 + _gid * 100,
                               "team_pts": {_d["home"]: _mh, _d["away"]: _ma}})
            _c.close()
            print("player forecasts:", PLV.forecast_slate(PLDB, _PM.load("artifacts/player_state.json"), av, _g,
                                                            n_sims=int(os.environ.get("PLAYER_N_SIMS", 1000))))
        except Exception as ex:
            print("player forecasts failed (team forecasts unaffected):", type(ex).__name__, ex)
    except Exception as ex:
        print("player update failed (forecasts unaffected):", type(ex).__name__, ex)
    eng.save_state(STATE)       # state is only persisted after a fully successful run
    os.makedirs("artifacts/reports", exist_ok=True)
    print(write_report(store, today, f"artifacts/reports/forecasts_{today}.md"))
    try:      # active niche streaks for today's slate (best effort; descriptive, not predictive)
        import importlib.util
        spec = importlib.util.spec_from_file_location("niche_streaks", os.path.join(ROOT, "scripts/niche_streaks.py"))
        ns = importlib.util.module_from_spec(spec); spec.loader.exec_module(ns)
        print("niche streaks written" if ns.build(DB, str(today), f"artifacts/reports/niche_streaks_{today}.md") else f"no forecast games on {today}: no streak report")
    except Exception as ex:
        print("niche streaks failed (forecasts unaffected):", type(ex).__name__, ex)
    try:      # team box-score / advanced-stat report (best effort)
        import importlib.util
        spec = importlib.util.spec_from_file_location("team_stats_report", os.path.join(ROOT, "scripts/team_stats_report.py"))
        tsr = importlib.util.module_from_spec(spec); spec.loader.exec_module(tsr); tsr.build(DB)
    except Exception as ex:
        print("team stats report failed (forecasts unaffected):", type(ex).__name__, ex)
    try:      # calibration of team and player forecasts against results (reports + display constants; changes no stored forecast)
        import importlib.util
        spec = importlib.util.spec_from_file_location("calibration_report", os.path.join(ROOT, "scripts/calibration_report.py"))
        cr = importlib.util.module_from_spec(spec); spec.loader.exec_module(cr); cr.main()
    except Exception as ex:
        print("calibration report failed (forecasts unaffected):", type(ex).__name__, ex)
else:
    sys.exit(1)
