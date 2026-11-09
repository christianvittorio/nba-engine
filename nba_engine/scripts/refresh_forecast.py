"""Re-forecast a slate with the CURRENT injury report, whether or not games have started (run from GitHub Actions: ESPN is reachable there).
Players ESPN lists as Out or Doubtful are removed; the team simulation carries the availability shift; players are re-projected with the new
team points, and market ladders (P over x.5 for every stat, 2PM/2PA and combos included) are written. Stored forecasts are never changed:
team rows go to `forecasts` under the model name `sim_mc_refresh`, player rows to the table `player_refresh` (tagged with the run time).
Usage: python scripts/refresh_forecast.py [YYYY-MM-DD US Eastern date; default today]  -> artifacts/reports/refresh_<date>.md"""
import os, sys, json, sqlite3
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
import numpy as np
from nbaengine.feed import EspnFeed
from nbaengine.store import Store
from nbaengine import MODEL_VERSION
from nbaengine.pipeline import Engine, SEED0
from nbaengine.sim import simulate_game, summarize, apply_dispersion
from nbaengine.availability import build_availability, save_availability
from nbaengine.injury import make_avail_fn
from nbaengine.players import PlayerModel, sample_players, summarize_samples
from nbaengine.player_live import _ladders, KEEP
day = sys.argv[1] if len(sys.argv) > 1 else str(datetime.now(ZoneInfo("America/New_York")).date())
now = datetime.now(timezone.utc); stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
store = Store("artifacts/live.sqlite"); eng = Engine.load(store, "artifacts/state.json")
av = build_availability(EspnFeed(pause_s=0.3), teams=None, player_state_path="artifacts/player_state.json")
save_availability(av, "artifacts/availability.json")
pm = PlayerModel.load("artifacts/player_state.json")
if os.path.exists("artifacts/p_play_cal.json"):
    c_ = json.load(open("artifacts/p_play_cal.json")); pm.p.p_play_cal = [float(c_["a"]), float(c_["b"])]
avail_fn = make_avail_fn(pm, av)
def listed(team, words):
    t = (av.get("teams") or {}).get(team, {})
    return [(i.get("nba_id"), i.get("name") or i.get("player") or str(i.get("nba_id")), str(i.get("status", ""))) for i in t.get("injuries", [])
            if any(w in str(i.get("status", "")).lower() for w in words)]
con = sqlite3.connect("artifacts/live.sqlite"); pl = sqlite3.connect("artifacts/player_live.sqlite")
pl.execute("CREATE TABLE IF NOT EXISTS player_refresh(run_utc TEXT, game_id INTEGER, team TEXT, player_id INTEGER, name TEXT, proj_min REAL, p_play REAL, details_json TEXT, PRIMARY KEY(run_utc, game_id, player_id))")
games = []
for gid, season, dj, mh, ma in con.execute("select game_id, season, details_json, mean_home, mean_away from forecasts where model_name='sim_mc'"):
    d = json.loads(dj)
    if d.get("date") == day: games.append((gid, season, d, mh, ma))
games.sort(key=lambda g: g[2].get("tip_utc") or "")
out = [f"# Re-forecast with the current injury report, {day}", f"Run {stamp} UTC. Players ESPN lists as Out or Doubtful are removed (Questionable are kept, listed below). Original forecasts are unchanged; this is a second version. "
       "Games already started are included for review only.", ""]
for gid, season, d, mh, ma in games:
    h, a = d["home"], d["away"]
    ug = type("UG", (), {"season": season, "game_id": gid, "home": h, "away": a, "date": day})()
    r = avail_fn(ug) if avail_fn else None
    lh, la, det = r if r else (0.0, 0.0, {})
    sim = simulate_game(eng.prof, h, a, 10000, SEED0 + gid, 0.0, track=True, shift_home=lh, shift_away=la)
    sm = summarize(apply_dispersion(sim, eng.kappa_m, eng.kappa_t, eng.level_delta))
    store.save_forecast(season, gid, "sim_mc_refresh", f"{MODEL_VERSION}+r{now.strftime('%m%d%H%M')}", stamp, SEED0 + gid, 10000, sm["p_home"], sm["mean_home"], sm["mean_away"], sm["mean_total"], sm["p_ot"],
                        q_margin=sm["q_margin"], q_total=sm["q_total"], details={**det, "date": day, "home": h, "away": a, "refresh_utc": stamp})
    p0 = con.execute("select p_home from forecasts where game_id=? and model_name='sim_mc' order by forecast_id limit 1", (gid,)).fetchone()
    started = bool(d.get("tip_utc")) and datetime.fromisoformat(d["tip_utc"].replace("Z", "+00:00")) <= now
    out += [f"## {a} at {h} (game {gid}){'  [already started]' if started else ''}", "",
            f"- Team: P(home) {p0[0]:.3f} -> **{sm['p_home']:.3f}**; projected final {h} {sm['mean_home']:.0f} - {a} {sm['mean_away']:.0f} (was {mh:.0f} - {ma:.0f}); total {sm['mean_total']:.1f}.",
            f"- Out/Doubtful removed: {h}: {', '.join(f'{n} ({s})' for _, n, s in listed(h, ('out', 'doubtful'))) or 'none'}; {a}: {', '.join(f'{n} ({s})' for _, n, s in listed(a, ('out', 'doubtful'))) or 'none'}.",
            f"- Questionable (kept in): {h}: {', '.join(n for _, n, s in listed(h, ('question', 'day'))) or 'none'}; {a}: {', '.join(n for _, n, s in listed(a, ('question', 'day'))) or 'none'}.", ""]
    ptsd = {h: sm["mean_home"], a: sm["mean_away"]}
    for ti, team in enumerate((h, a)):
        gone = {i for i, _, _ in listed(team, ("out", "doubtful")) if i is not None}
        roster = [r_["nba_id"] for r_ in av["teams"].get(team, {}).get("roster", []) if r_.get("nba_id") is not None]
        pool = [i for i in roster if i not in gone and i in pm.pl] if roster else [i for i in pm.pool(team) if i not in gone]
        if not pool: continue
        pr = pm.project_team(team, mode="unconfirmed", pool_ids=pool, team_pts=ptsd[team], opp_team=(a if team == h else h))
        pr = pr.sort_values("base_min", ascending=False).head(12).reset_index(drop=True)
        samp = sample_players(pr, pm.p, 4000, 20261021 + gid * 100 + ti, "unconfirmed"); summ = summarize_samples(samp); lad = _ladders(samp)
        out += [f"**{team}**", "", "| Player | Min | P(play) | PTS | REB | AST | PRA | 3PM | 2PM | FTA | STL | BLK | TOV | P+R | P+A | R+A |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for row, dd, L in zip(pr.itertuples(index=False), summ, lad):
            det_ = {k: {"m": round(dd[k]["mean"], 3), "q": [round(x, 2) for x in dd[k]["q"]]} for k in KEEP if k in dd}
            for k, v in L.items(): det_.setdefault(k, {"m": v["m"], "q": v["q"]}).update(t0=v["t0"], ov=v["ov"])
            pl.execute("INSERT OR REPLACE INTO player_refresh VALUES(?,?,?,?,?,?,?,?)", (stamp, gid, team, int(row.player_id), row.name, float(row.proj_min), float(row.p_play), json.dumps(det_)))
            def po(k):
                x = det_[k]; ln = int(x["m"]) + 0.5; j = int(ln - 0.5) - x["t0"]
                return f"{x['m']:.1f} (o{ln:g} {1.0 if j < 0 else (0.01 if j >= len(x['ov']) else x['ov'][j] / 1000):.0%})"
            out.append(f"| {row.name} | {row.proj_min:.0f} | {row.p_play:.2f} | " + " | ".join(po(k) for k in ("pts", "reb", "ast", "pra", "tpm", "fg2m", "fta", "stl", "blk", "tov", "pr", "pa", "ra")) + " |")
        out.append("")
pl.commit(); con.commit()
p = f"artifacts/reports/refresh_{day}.md"; open(p, "w").write("\n".join(out)); print("wrote", p, len(games), "games")
