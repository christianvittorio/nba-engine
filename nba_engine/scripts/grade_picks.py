"""Grade logged over/under leans against box scores: hit rate by side and probability band, and parlay results. Writes artifacts/reports/picks_grade.md"""
import os, sys, sqlite3
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
pl = sqlite3.connect("artifacts/player_live.sqlite")
L = pd.read_sql_query("select * from picks_log", pl)
A = pd.read_sql_query("select * from player_act", pl)
names = pd.read_sql_query("select distinct game_id, name, player_id from player_refresh", pl)
L = L.drop(columns=["player_id"]).merge(names, on=["game_id", "name"], how="left").merge(A, on=["game_id", "player_id"], how="left", suffixes=("", "_a"))
f = {"pts": L.pts, "reb": L.reb, "ast": L.ast, "stl": L.stl, "blk": L.blk, "tov": L.tov, "tpm": L.tpm, "fta": L.fta, "pra": L.pts + L.reb + L.ast, "pr": L.pts + L.reb, "pa": L.pts + L.ast, "ra": L.reb + L.ast, "fg2m": L.fgm - L.tpm}
L["act"] = [f[s][i] for i, s in zip(L.index, L.stat)]; L = L[L["min"].fillna(0) > 0].copy()          # leg voids if he did not play
if L.empty:
    print("nothing to grade yet"); sys.exit(0)
L["hit"] = np.where(L.side == "OVER", L.act > L.line, L.act < L.line); L["push"] = L.act == L.line; G = L[~L.push]
md = ["# Graded over/under leans", f"{len(G)} graded legs from {G.run_utc.nunique()} run(s); pushes and did-not-play legs excluded.", "",
      "Model said / actual hit rate:", "", G.groupby("side").agg(n=("hit", "size"), model_p=("p", "mean"), hit=("hit", "mean")).round(3).to_markdown(), "",
      G.assign(band=pd.cut(G.p, [0.5, .6, .7, .76])).groupby("band", observed=True).agg(n=("hit", "size"), model_p=("p", "mean"), hit=("hit", "mean")).round(3).to_markdown(), ""]
if "price" in G and G.price.notna().any():
    R_ = G[G.price.notna()].copy(); dec = np.where(R_.price > 0, 1 + R_.price / 100, 1 + 100 / R_.price.abs())
    R_["profit"] = np.where(R_.hit, dec - 1, -1.0); R_["ev_model"] = R_.p * (dec - 1) - (1 - R_.p)
    md += [f"Picks with a real book price: {len(R_)}; flat 1-unit staking returned {R_.profit.sum():+.2f} units (model expected {R_.ev_model.sum():+.2f}); hit {R_.hit.mean():.1%} vs model {R_.p.mean():.1%}.", ""]
P = G[G.in_parlay == 1]
if len(P): md += [f"Legs that were in a suggested parlay: {len(P)}, hit {P.hit.mean():.1%} (model {P.p.mean():.1%}).", ""]
open("artifacts/reports/picks_grade.md", "w").write("\n".join(md)); print("\n".join(md))
