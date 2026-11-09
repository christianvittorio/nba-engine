"""Are the player market ladders calibrated?  For every stored forecast with a ladder and a box-score actual (players who played), take the half-lines
around the projection (floor(mean)+0.5 and +/-1, +/-2) and compare the predicted P(over) with how often the stat really went over.
Writes artifacts/reports/player_ladder_calibration.md"""
import os, sys, json, sqlite3
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
from nbaengine.player_live import with_ladder
pl = sqlite3.connect(f"{ROOT}/artifacts/player_live.sqlite")
A = pd.read_sql_query("select * from player_act", pl); A = A[A["min"] > 0].set_index(["game_id", "player_id"])
ACT = {"pts": lambda a: a.pts, "reb": lambda a: a.reb, "ast": lambda a: a.ast, "stl": lambda a: a.stl, "blk": lambda a: a.blk, "tov": lambda a: a.tov, "tpm": lambda a: a.tpm, "tpa": lambda a: a.tpa,
       "fgm": lambda a: a.fgm, "fga": lambda a: a.fga, "ftm": lambda a: a.ftm, "fta": lambda a: a.fta, "pra": lambda a: a.pts + a.reb + a.ast, "pr": lambda a: a.pts + a.reb,
       "pa": lambda a: a.pts + a.ast, "ra": lambda a: a.reb + a.ast, "sb": lambda a: a.stl + a.blk, "fg2m": lambda a: a.fgm - a.tpm, "fg2a": lambda a: a.fga - a.tpa}
rows = []
for gid, pid, dj in pl.execute("select game_id, player_id, details_json from player_fc"):
    if (gid, pid) not in A.index: continue
    d = with_ladder(pl, gid, pid, json.loads(dj)); a = A.loc[(gid, pid)]
    for k, f in ACT.items():
        x = d.get(k)
        if not x or "ov" not in x: continue
        act = float(f(a)); base = int(x["m"])
        for off in (-2, -1, 0, 1, 2):
            ln = base + off + 0.5
            if ln < 0.5: continue
            j = int(ln - 0.5) - x["t0"]; p = 1.0 if j < 0 else (0.01 if j >= len(x["ov"]) else x["ov"][j] / 1000.0)
            rows.append({"game_id": gid, "stat": k, "line": ln, "p": p, "over": float(act > ln)})
R = pd.DataFrame(rows)
if R.empty:
    print("no forecasts with both a ladder and an actual yet"); sys.exit(0)
R["bin"] = pd.cut(R.p, [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0], include_lowest=True)
T = R.groupby("bin", observed=True).agg(n=("p", "size"), predicted=("p", "mean"), actual=("over", "mean")).round(3)
brier = ((R.p - R.over) ** 2).mean(); base = ((R.over.mean() - R.over) ** 2).mean()
by = R.groupby("stat").agg(n=("p", "size"), predicted=("p", "mean"), actual=("over", "mean")).assign(gap=lambda d: (d.actual - d.predicted).round(3)).round(3)
n_games = R.game_id.nunique()
md = [f"# Player market ladders: calibration", f"{n_games} games, {len(R)} (player, stat, line) cases; each case is a half-line within 2 of the projection; players who played only.", "",
      f"Brier score {brier:.4f} (always saying the base rate {R.over.mean():.2f}: {base:.4f}; lower is better).", "",
      "## Predicted P(over) vs how often it went over", "", T.to_markdown(), "", "## By stat", "", by.to_markdown(), ""]
p = f"{ROOT}/artifacts/reports/player_ladder_calibration.md"; open(p, "w").write("\n".join(md)); print("\n".join(md[:14]))
