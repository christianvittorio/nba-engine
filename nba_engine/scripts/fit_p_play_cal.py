"""Recalibrate the unconfirmed play probability for the LIVE pool (players ESPN does not list as Out). Logistic recalibration
played ~ sigmoid(a + b*logit(p_play)) fitted on stored live forecasts vs box scores. Leave-one-date-out cross-validation of log-loss and Brier.
Prints a, b; writes artifacts/p_play_cal.json."""
import os, sys, json, sqlite3
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pl = sqlite3.connect(f"{ROOT}/artifacts/player_live.sqlite"); live = sqlite3.connect(f"{ROOT}/artifacts/live.sqlite")
F = pd.read_sql_query("select game_id,player_id,p_play,proj_min from player_fc", pl); A = pd.read_sql_query("select game_id,player_id,min from player_act", pl)
D = pd.read_sql_query("select game_id,date from game_dates", live)
F = F[F.game_id.isin(set(A.game_id))].merge(A, on=["game_id", "player_id"], how="left").merge(D, on="game_id")
F["y"] = (F["min"].fillna(0) > 0).astype(int); p = F.p_play.clip(0.02, 0.98); F["x"] = np.log(p / (1 - p))
def fit(d):
    m = LogisticRegression(C=1e6).fit(d[["x"]], d.y); return float(m.intercept_[0]), float(m.coef_[0][0])
def pred(ab, x): return 1 / (1 + np.exp(-(ab[0] + ab[1] * x)))
ll = lambda y, q: float(-(y * np.log(np.clip(q, 1e-4, 1 - 1e-4)) + (1 - y) * np.log(np.clip(1 - q, 1e-4, 1 - 1e-4))).mean())
br = lambda y, q: float(((y - q) ** 2).mean())
out_p = np.zeros(len(F)); 
for dt in F.date.unique():
    tr, te = F[F.date != dt], F[F.date == dt]; out_p[(F.date == dt).values] = pred(fit(tr), te.x)
ab = fit(F)
print(f"{len(F)} rows, {F.game_id.nunique()} games, {F.date.nunique()} dates | fitted a={ab[0]:.3f} b={ab[1]:.3f}")
print("                   log-loss  Brier   mean pred  actual")
print(f"as stored (pow1.2)  {ll(F.y, p):.4f}   {br(F.y, p):.4f}   {p.mean():.3f}     {F.y.mean():.3f}")
print(f"recalibrated (CV)   {ll(F.y, out_p):.4f}   {br(F.y, out_p):.4f}   {out_p.mean():.3f}     {F.y.mean():.3f}")
F["q"] = out_p; F["b"] = pd.cut(F.p_play, [0, .3, .5, .7, .9, .97, 1])
print(F.groupby("b", observed=True).agg(n=("y", "size"), stored=("p_play", "mean"), recal=("q", "mean"), actual=("y", "mean")).round(3))
if "--write" in sys.argv:
    json.dump({"a": ab[0], "b": ab[1], "n_rows": len(F), "n_games": int(F.game_id.nunique())}, open(f"{ROOT}/artifacts/p_play_cal.json", "w")); print("wrote artifacts/p_play_cal.json")
