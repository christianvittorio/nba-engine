"""Over/under leans and parlays from the injury-adjusted player projections (player_refresh table, written by scripts/refresh_forecast.py).
Books' lines are not available here, so a stand-in line is used: the player's last-10-game average rounded to the nearest half (books anchor on recent form).
For each player-stat the side (over or under) with the higher model probability at that line is the lean. Probabilities get the bias correction measured by the
calibration check (scripts/player_ladder_calibration.py: the ladders ran high on overs). Parlay probability = product of leg probabilities (legs from
different players; independence is an approximation). Usage: python scripts/best_picks.py [YYYY-MM-DD]  -> artifacts/reports/best_picks_<date>.md"""
import os, sys, re, json, sqlite3
from itertools import combinations
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.players import PlayerModel
day = sys.argv[1] if len(sys.argv) > 1 else None
pl = sqlite3.connect("artifacts/player_live.sqlite"); live = sqlite3.connect("artifacts/live.sqlite")
run = pl.execute("select max(run_utc) from player_refresh").fetchone()[0]
rows = pl.execute("select game_id,team,player_id,name,proj_min,p_play,details_json from player_refresh where run_utc=?", (run,)).fetchall()
tm = {g: json.loads(d) for g, d in live.execute("select game_id, details_json from forecasts where model_name='sim_mc'")}
pm = PlayerModel.load("artifacts/player_state.json")
GAP = {}
try:
    t = open("artifacts/reports/player_ladder_calibration_player_ladder_cal.md").read().split("## By stat")[1]
    for m in re.finditer(r"\|\s*(\w+)\s*\|\s*\d+\s*\|\s*[\d.]+\s*\|\s*[\d.]+\s*\|\s*(-?[\d.]+)\s*\|", t): GAP[m.group(1)] = float(m.group(2))
except Exception:
    pass
H = {"pts": ("pts",), "reb": ("reb",), "ast": ("ast",), "stl": ("stl",), "blk": ("blk",), "tov": ("tov",), "tpm": ("tpm",), "fta": ("fta",)}
COMBO = {"pra": ("pts", "reb", "ast"), "pr": ("pts", "reb"), "pa": ("pts", "ast"), "ra": ("reb", "ast")}
LABEL = {"pts": "Points", "reb": "Rebounds", "ast": "Assists", "stl": "Steals", "blk": "Blocks", "tov": "Turnovers", "tpm": "3-pointers made", "fta": "Free-throw attempts",
         "pra": "Pts+Reb+Ast", "pr": "Pts+Reb", "pa": "Pts+Ast", "ra": "Reb+Ast", "fg2m": "2-pointers made"}
legs = []
for gid, team, pid, name, pmin, pp, dj in rows:
    if pp < 0.85 or pmin < 18: continue
    base = pm.baseline_means(pid, 10)
    if base is None: continue
    d = json.loads(dj)
    stats = {**{k: base[k] for k in H}, **{k: sum(base[x] for x in v) for k, v in COMBO.items()}, "fg2m": base["fgm"] - base["tpm"]}
    for k, rec in stats.items():
        x = d.get(k)
        if not x or "ov" not in x: continue
        lo = np.floor(rec) + 0.5; ln = float(lo if abs(rec - lo) <= abs(rec - (lo + 1)) else lo + 1)
        if ln < 0.5: continue
        j = int(ln - 0.5) - x["t0"]; po = 1.0 if j < 0 else (0.01 if j >= len(x["ov"]) else x["ov"][j] / 1000.0)
        po = float(np.clip(po + GAP.get(k, 0.0), 0.02, 0.98))               # actual - predicted over-rate measured on past games
        side, p = ("OVER", po) if po >= 0.5 else ("UNDER", 1 - po)
        if p > 0.75: continue                                              # near-certainties are not lines a book prices at anything worth taking, and extreme model confidence is more likely model error
        if abs(x["m"] - rec) / max(rec, 1.0) > 0.30: continue              # the model and recent form disagree by more than 30%: more likely a model miss than an edge
        if k in ("stl", "blk", "tov") and ln < 1.5: continue               # 0.5 lines on rare events are near coin-flips with heavy juice, skip
        legs.append(dict(gid=gid, team=team, name=name, stat=k, line=ln, side=side, p=p, model=x["m"], recent=rec, pp=pp))
def fmt(l): return f"{l['name']} ({l['team']}) {l['side']} {l['line']:g} {LABEL[l['stat']]}"
def best_parlay(L, n, max_per_game=9):
    L = sorted(L, key=lambda l: -l["p"]); pick, used, per = [], set(), {}
    for l in L:
        if l["name"] in used or per.get(l["gid"], 0) >= max_per_game: continue
        pick.append(l); used.add(l["name"]); per[l["gid"]] = per.get(l["gid"], 0) + 1
        if len(pick) == n: break
    return pick
prob = lambda P: float(np.prod([l["p"] for l in P]))
out = [f"# Best over/under leans and parlays (injury-adjusted projections, run {run} UTC)", "",
       "**Read this first.** I do not have sportsbook prop lines, so the line used for each leg is a stand-in: the player's last-10-game average rounded to the nearest half. "
       "Books price off recent form too, so a lean means the model, with the injuries and the opponent, disagrees with recent form. It does not mean there is a +EV bet: "
       "the real line and price may differ, and the model is not proven to beat the market (the market's closing line beat it on team margins). "
       "Check real lines with `python scripts/prop_price.py \"<player>\" <stat> <line>`. Probabilities are shifted by the calibration bias measured so far (the ladders ran high on overs). "
       "A parlay's probability multiplies its legs, treating players as independent; real legs in one game are usually positively linked, so treat it as approximate. "
       "Legs are skipped when the model and recent form differ by more than 30% (more likely a model miss), when the model is more than 75% sure, and for 0.5 steal/block lines. Legs void if the player does not play; only players with P(play) of at least 0.85 and 18+ projected minutes are used.", ""]
games = sorted({l["gid"] for l in legs})
S = best_parlay(legs, 4, 1)
out += ["## Best parlay across the whole slate (4 legs, one per game)", "", "| Leg | Model proj | Recent avg | Win prob |", "|---|---|---|---|"] + \
       [f"| {fmt(l)} | {l['model']:.1f} | {l['recent']:.1f} | {l['p']:.0%} |" for l in S] + ["", f"**Combined probability {prob(S):.1%}** (fair odds about {1 / prob(S):.1f} to 1; a book's payout must beat that for it to be worth anything).", ""]
S3 = best_parlay(legs, 3, 1)
out += ["Safest 3-leg slate parlay: " + "; ".join(fmt(l) + f" ({l['p']:.0%})" for l in S3) + f" -> combined {prob(S3):.1%}.", ""]
for gid in games:
    d = tm.get(gid, {}); L = [l for l in legs if l["gid"] == gid]
    P = best_parlay(L, 3)
    out += [f"## {d.get('away', '?')} at {d.get('home', '?')} (game {gid})", "", "**Best 3-leg parlay for this game:**", "", "| Leg | Model proj | Recent avg | Win prob |", "|---|---|---|---|"] + \
           [f"| {fmt(l)} | {l['model']:.1f} | {l['recent']:.1f} | {l['p']:.0%} |" for l in P] + ["", f"Combined {prob(P):.1%}.", "",
           "Top single leans (over or under, whichever the model prefers):", ""] + \
           [f"- {fmt(l)}: {l['p']:.0%} (model {l['model']:.1f} vs recent {l['recent']:.1f})" for l in sorted(L, key=lambda l: -l["p"])[:8]] + [""]
pl.execute("CREATE TABLE IF NOT EXISTS picks_log(run_utc TEXT, game_id INTEGER, player_id INTEGER, name TEXT, stat TEXT, line REAL, side TEXT, p REAL, model REAL, recent REAL, in_parlay INTEGER, PRIMARY KEY(run_utc, game_id, name, stat))")
inpar = {(l["gid"], l["name"], l["stat"]) for g in games for l in best_parlay([x for x in legs if x["gid"] == g], 3)} | {(l["gid"], l["name"], l["stat"]) for l in S}
for l in legs:      # every lean is logged before the games finish so it can be graded honestly later (scripts/grade_picks.py)
    pl.execute("INSERT OR IGNORE INTO picks_log VALUES(?,?,?,?,?,?,?,?,?,?,?)", (run, l["gid"], 0, l["name"], l["stat"], l["line"], l["side"], l["p"], l["model"], l["recent"], int((l["gid"], l["name"], l["stat"]) in inpar)))
pl.commit()
p = f"artifacts/reports/best_picks_{day or 'latest'}.md"; open(p, "w").write("\n".join(out)); print("wrote", p, len(legs), "legs", len(games), "games"); print("\n".join(out[7:20]))
