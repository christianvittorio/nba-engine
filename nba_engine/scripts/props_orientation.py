"""Which of the two prices in each ESPN prop pair is the OVER?  Uses finished games with known results: under hypothesis A (first = over) and B (second = over),
the average log-likelihood of what actually happened, using the book's own no-vig probabilities, is compared. The right orientation scores clearly higher.
Also reports how often the line is hit, for the book's calibration. Writes artifacts/reports/props_orientation.md"""
import os, sys, sqlite3
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
pl = sqlite3.connect("artifacts/player_live.sqlite")
P = pd.read_sql_query("select * from espn_props", pl); A = pd.read_sql_query("select game_id, player_id as nba_id, pts, reb, ast, tpm, stl, blk, min from player_act", pl)
P = P.sort_values("fetched_utc").drop_duplicates(["game_id", "espn_athlete", "stat", "line"], keep="last").merge(A, on=["game_id", "nba_id"], how="inner")
P = P[P["min"] > 0]; P["act"] = [r[s] for r, s in zip(P.to_dict("records"), P.stat)]; P = P[P.act != P.line]; P["over"] = (P.act > P.line).astype(float)
dec = lambda a: np.where(a > 0, 1 + a / 100, 1 + 100 / np.abs(a))
qa, qb = 1 / dec(P.price_a.values), 1 / dec(P.price_b.values); fa = qa / (qa + qb)          # no-vig prob of the FIRST item
ll = lambda p, y: float(np.mean(y * np.log(np.clip(p, 1e-3, 1)) + (1 - y) * np.log(np.clip(1 - p, 1e-3, 1))))
A_, B_ = ll(fa, P.over.values), ll(1 - fa, P.over.values)
tilt = P[np.abs(fa - 0.5) > 0.04]                                                          # pairs where the prices clearly favour one side
fav_first_over = float(((tilt.over == 1) == (tilt.price_a < tilt.price_b)).mean()) if len(tilt) else float("nan")
md = ["# ESPN prop pair orientation", f"{len(P)} graded lines from {P.game_id.nunique()} finished games.", "",
      f"Mean log-likelihood if the FIRST price is the over: {A_:.4f}; if the SECOND is: {B_:.4f} (higher is right).",
      f"Of the {len(tilt)} pairs where the prices clearly favour one item, the more-favoured item won {fav_first_over:.1%} of the time when read as 'first = over'.",
      f"Share of lines where the stat went over: {P.over.mean():.3f}.", ""]
verdict = "first=over" if A_ > B_ + 0.003 else ("second=over" if B_ > A_ + 0.003 else "undecided")
md.append(f"**Verdict: {verdict}.**"); open("artifacts/reports/props_orientation.md", "w").write("\n".join(md)); print("\n".join(md))
