"""Does the model beat real DraftKings prop lines (ESPN feed) on FINISHED games? Uses the stored pre-game ladders (player_ladder_cal: re-simulated from the
pre-game state with the live play-probability recalibration) against the line on the board, graded with box scores. Flat 1-unit stakes on every
over/under where the model's win probability exceeds the book's no-vig probability by an edge threshold. Writes artifacts/reports/props_backtest.md.
NOTE: the ladders are re-simulations of the stored forecasts (no same-day injury news), so this tests the model, not the refresh."""
import os, sys, json, sqlite3
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
TABLE = os.environ.get("LADDER_TABLE", "player_ladder_cal")
pl = sqlite3.connect("artifacts/player_live.sqlite")
P = pd.read_sql_query("select * from espn_props", pl).sort_values("fetched_utc").drop_duplicates(["game_id", "espn_athlete", "stat", "line"], keep="last")
A = pd.read_sql_query("select game_id, player_id as nba_id, pts, reb, ast, tpm, stl, blk, min from player_act", pl)
L = {(g, p): json.loads(j) for g, p, j in pl.execute(f"select game_id, player_id, ladder_json from {TABLE}")}
dec = lambda a: 1 + a / 100 if a > 0 else 1 + 100 / abs(a)
pge = lambda x, k: 1.0 if k - 1 < x["t0"] else (0.005 if k - 1 - x["t0"] >= len(x["ov"]) else x["ov"][k - 1 - x["t0"]] / 1000.0)
rows = []
act = A.set_index(["game_id", "nba_id"])
for r in P.itertuples(index=False):
    if r.nba_id is None or pd.isna(r.nba_id): continue
    k = (r.game_id, int(r.nba_id)); lad = L.get(k)
    if lad is None or r.stat not in lad or k not in act.index: continue
    a = act.loc[k]
    if a["min"] <= 0: continue                                     # voided
    x = lad[r.stat]; line = r.line
    if line == int(line): p_over = pge(x, int(line) + 1); p_push = pge(x, int(line)) - p_over
    else: p_over = pge(x, int(np.ceil(line))); p_push = 0.0
    d_o, d_u = dec(r.price_a), dec(r.price_b); fair_o = (1 / d_o) / (1 / d_o + 1 / d_u); val = float(a[r.stat])
    if val == line: continue
    for side, p, d, fair, won in (("OVER", p_over, d_o, fair_o, val > line), ("UNDER", max(0.0, 1 - p_over - p_push), d_u, 1 - fair_o, val < line)):
        rows.append(dict(game_id=r.game_id, name=r.name, stat=r.stat, line=line, side=side, p=p, fair=fair, edge=p - fair, dec=d, won=float(won), profit=(d - 1) if won else -1.0, model=x["m"]))
R = pd.DataFrame(rows)
if R.empty: print("nothing to test"); sys.exit(0)
md = ["# Model vs real DraftKings prop lines (finished games)", f"{R.game_id.nunique()} games, {len(R) // 2} prop lines with a pre-game ladder, a line and a box score.", "",
      "Flat 1-unit stakes on every side where (model win prob - book no-vig prob) exceeds the threshold; 'book' rows show what betting everything blindly returns (the vig).", ""]
def line(lbl, d): return f"| {lbl} | {len(d)} | {d.p.mean():.3f} | {d.fair.mean():.3f} | {d.won.mean():.3f} | {d.profit.sum():+.1f} | {d.profit.mean():+.3f} |" if len(d) else f"| {lbl} | 0 | | | | | |"
tab = ["| Selection | Bets | Model p | Book fair p | Hit rate | Units | ROI |", "|---|---|---|---|---|---|---|", line("every side (blind)", R)]
for th in (0.03, 0.05, 0.08, 0.12):
    tab.append(line(f"edge > {th:.0%}", R[R.edge > th])); tab.append(line(f"edge > {th:.0%}, 52-75% sure", R[(R.edge > th) & (R.p >= .52) & (R.p <= .75)]))
for s in ("OVER", "UNDER"): tab.append(line(f"edge > 5%, {s} only", R[(R.edge > .05) & (R.side == s)]))
md += tab + ["", "By stat (edge > 5%):", "", "| Stat | Bets | Model p | Book fair p | Hit rate | Units | ROI |", "|---|---|---|---|---|---|---|"] + [line(st, d) for st, d in R[R.edge > .05].groupby("stat")]
# is the model's probability or the book's the better predictor? (log loss on all sides, vs outcomes)
ll = lambda p, y: float(-np.mean(y * np.log(np.clip(p, 1e-3, 1)) + (1 - y) * np.log(np.clip(1 - p, 1e-3, 1))))
O = R[R.side == "OVER"]; md += ["", f"Log-loss on over outcomes: model {ll(O.p, O.won):.4f}, book no-vig {ll(O.fair, O.won):.4f} (lower is better)."]
x_ = (O.p - O.fair).values; y_ = (O.won - O.fair).values; w_ = float((x_ * y_).sum() / (x_ * x_).sum()); se_ = float(np.sqrt(((y_ - w_ * x_) ** 2).sum() / (len(x_) - 1) / (x_ * x_).sum()))
md += [f"Weight the model earns against the book (0 = trust the book, 1 = trust the model): {w_:.2f} +- {se_:.2f} on {len(O)} over-lines. Picks use max(0, this) as their blend weight."]
json.dump({"w": w_, "se": se_, "n": int(len(O)), "games": int(R.game_id.nunique())}, open("artifacts/props_blend.json", "w"))
open("artifacts/reports/props_backtest.md", "w").write("\n".join(md)); print("\n".join(md))
