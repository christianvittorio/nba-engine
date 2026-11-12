"""`final_v2`: the headline forecast going forward = 30% simulation + 70% Elo (modern home advantage 45), both adjusted for rest, injuries and rest-day risk.
Built only from forecasts already stored for the game (sim_mc_all, elo_v2); never edits them. Games without the adjusted variants fall back to blend_v2.
Backtest basis (see artifacts/reports/roster_forecast_comparison.md and miss_analysis): corrected Elo beats the simulation; the blend scores best. Usage: python scripts/make_final.py"""
import os, sys, json, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.store import Store
from nbaengine.pipeline import MODEL_VERSION
from nbaengine.elo import ELO_PER_POINT
W_SIM = 0.30
store = Store("artifacts/live.sqlite"); con = store.con
rows = con.execute("""select s.season, s.game_id, s.p_home, s.mean_home, s.mean_away, s.q_margin_json, s.details_json, e.details_json
    from forecasts s join forecasts e on e.season=s.season and e.game_id=s.game_id and e.model_name='elo_v2'
    where s.model_name='sim_mc_all'
      and not exists (select 1 from forecasts x where x.season=s.season and x.game_id=s.game_id and x.model_name='final_v2')
      and not exists (select 1 from results r where r.season=s.season and r.game_id=s.game_id)""").fetchall()
rows2 = con.execute("""select b.season, b.game_id, b.p_home, b.mean_home, b.mean_away, b.q_margin_json, b.details_json, b.details_json
    from forecasts b where b.model_name='blend_v2'
      and not exists (select 1 from forecasts x where x.season=b.season and x.game_id=b.game_id and x.model_name='final_v2')
      and not exists (select 1 from forecasts a where a.season=b.season and a.game_id=b.game_id and a.model_name='sim_mc_all')
      and not exists (select 1 from results r where r.season=b.season and r.game_id=b.game_id)""").fetchall()
now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"); n = 0
for s, gid, p_sim, mh, ma, qj, sj, ej in rows:
    sd, ed = json.loads(sj), json.loads(ej); shift = float(sd.get("shift", 0.0))
    d2 = ed["elo_diff"] + ELO_PER_POINT * shift; p_elo = 1.0 / (1.0 + 10.0 ** (-d2 / 400.0)); m_elo = d2 / ELO_PER_POINT
    ph = W_SIM * p_sim + (1 - W_SIM) * p_elo; m_sim = mh - ma; mm = W_SIM * m_sim + (1 - W_SIM) * m_elo; tot = mh + ma
    q = json.loads(qj) if qj else None
    if q: q = {k: v + (mm - m_sim) for k, v in q.items()}
    store.save_forecast(s, gid, "final_v2", MODEL_VERSION, now, None, None, ph, (tot + mm) / 2, (tot - mm) / 2, tot, None, q_margin=q,
                        details={"date": sd.get("date"), "home": sd.get("home"), "away": sd.get("away"), "w_sim": W_SIM, "shift": shift, "p_sim_adj": p_sim, "p_elo_adj": p_elo, "basis": "sim_mc_all + elo_v2 + rest/injury shifts"})
    n += 1
for s, gid, p, mh, ma, qj, sj, _ in rows2:
    sd = json.loads(sj); q = json.loads(qj) if qj else None
    store.save_forecast(s, gid, "final_v2", MODEL_VERSION, now, None, None, p, mh, ma, mh + ma, None, q_margin=q,
                        details={"date": sd.get("date"), "home": sd.get("home"), "away": sd.get("away"), "w_sim": W_SIM, "shift": 0.0, "basis": "blend_v2 (no adjusted variants available)"})
    n += 1
con.commit(); print("final_v2 added for", n, "games")
