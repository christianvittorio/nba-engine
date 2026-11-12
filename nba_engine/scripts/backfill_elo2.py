"""Add `elo_v2` and `blend_v2` for games that already have a sim_mc forecast but no elo_v2 yet (games forecast before elo2 existed).
Uses the stored sim_mc forecast and the current elo2 ratings; sim_mc and every other stored forecast are untouched. Usage: python scripts/backfill_elo2.py [YYYY-MM-DD]"""
import os, sys, json, types
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.store import Store
from nbaengine.pipeline import Engine, MODEL_VERSION
store = Store("artifacts/live.sqlite"); eng = Engine.load(store, "artifacts/state.json")
if not eng.elo2: sys.exit("no elo2 in state; run scripts/init_elo2.py")
day = sys.argv[1] if len(sys.argv) > 1 else None
q = """select f.season, f.game_id, f.p_home, f.mean_home, f.mean_away, f.mean_total, f.details_json from forecasts f
       where f.model_name='sim_mc' and not exists (select 1 from forecasts x where x.season=f.season and x.game_id=f.game_id and x.model_name='elo_v2')
       and not exists (select 1 from results r where r.season=f.season and r.game_id=f.game_id)"""
n = 0
for s, gid, ph, mh, ma, mt, dj in store.con.execute(q).fetchall():
    d = json.loads(dj)
    if day and d.get("date") != day: continue
    ug = types.SimpleNamespace(season=s, game_id=gid, home=d["home"], away=d["away"], date=d.get("date"))
    eng.elo2.new_season(s)
    eng._forecast_elo2(ug, {"p_home": ph, "mean_home": mh, "mean_away": ma, "mean_total": mt}, mt, 0, 0, __import__("datetime").datetime.utcnow().isoformat() + "Z")
    n += 1
store.con.commit(); print("elo_v2/blend_v2 added for", n, "games")
