"""Can a fitted team-vs-team regression beat the rate-by-rate sim? Walk-forward on 2025 (fit only on earlier games).
Target: actual home margin. Baseline: sim margin (profile-only sim). Features: four-factor/pace matchup differentials."""
import os, sys, numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = pd.concat([pd.read_csv(f"{ROOT}/data/processed/games_cdn_{s}.csv") for s in (2022, 2023, 2024, 2025)]).sort_values("game_id").reset_index(drop=True)
S = pd.read_csv(f"{ROOT}/data/processed/team_stats_bt_2025_all.csv")[["game_id", "all_home_pts_reg", "all_away_pts_reg"]]
def fac(g, s, o):
    poss = g[f"{s}_fga"] + .44 * g[f"{s}_fta"] - g[f"{s}_oreb"] + g[f"{s}_tov"]
    return dict(efg=(g[f"{s}_fgm"] + .5 * g[f"{s}_3pm"]) / g[f"{s}_fga"], tov=g[f"{s}_tov"] / poss,
                orb=g[f"{s}_oreb"] / (g[f"{s}_oreb"] + g[f"{o}_dreb"]), ftr=g[f"{s}_fta"] / g[f"{s}_fga"],
                ft=g[f"{s}_ftm"] / max(g[f"{s}_fta"], 1), p3r=g[f"{s}_3pa"] / g[f"{s}_fga"], pace=poss)
HL = float(os.environ.get("HL", 25)); lam = .5 ** (1 / HL)
st = {}; rows = []
for _, g in G.iterrows():
    h, a = g.home, g.away
    fh, fa = fac(g, "home", "away"), fac(g, "away", "home")
    def get(t): return st.get(t)
    if g.season == 2025 and get(h) and get(a) and get(h)["n"] > 8 and get(a)["n"] > 8:
        H, A = get(h), get(a); r = {"game_id": g.game_id, "y": g.home_pts - g.away_pts}
        for k in fh:
            r["m_" + k] = (H["o"][k] - A["d"][k]) - (A["o"][k] - H["d"][k]) if k != "pace" else (H["o"][k] + H["d"][k] - A["o"][k] - A["d"][k])
        rows.append(r)
    for t, o, d in ((h, fh, fa), (a, fa, fh)):
        s = st.setdefault(t, {"o": {k: 0.0 for k in o}, "d": {k: 0.0 for k in o}, "w": 0.0, "n": 0})
        for k in o:
            s["o"][k] = (s["o"][k] * lam * s["w"] + o[k]) / (s["w"] * lam + 1); s["d"][k] = (s["d"][k] * lam * s["w"] + d[k]) / (s["w"] * lam + 1)
        s["w"] = s["w"] * lam + 1; s["n"] += 1
D = pd.DataFrame(rows).merge(S, on="game_id"); D["sim"] = D.all_home_pts_reg - D.all_away_pts_reg
F = [c for c in D if c.startswith("m_")]
for c in F: D[c] = (D[c] - D[c].mean()) / D[c].std()
D = D.reset_index(drop=True); pred = np.full(len(D), np.nan); pred_s = pred.copy()
for i in range(250, len(D)):
    tr = D.iloc[:i]
    for cols, out in ((F + ["sim"], pred), (["sim"], pred_s)):
        X = np.c_[np.ones(len(tr)), tr[cols].values]; lamr = 30 * np.eye(X.shape[1]); lamr[0, 0] = 0
        b = np.linalg.solve(X.T @ X + lamr, X.T @ tr.y.values); out[i] = np.r_[1, D.loc[i, cols].values.astype(float)] @ b
T = D.iloc[250:]; e = lambda p: (T.y - p[250:]).abs().mean()
print(len(T), "games | sim as-is MAE %.3f | sim recalibrated %.3f | sim + all matchup stats (ridge, walk-forward) %.3f" % ((T.y - T.sim).abs().mean(), e(pred_s), e(pred)))
X = np.c_[np.ones(len(D)), D[F + ["sim"]].values]; b = np.linalg.lstsq(X, D.y.values, rcond=None)[0]
res = D.y.values - X @ b; se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * res.var())
for n, c, s_ in zip(["const"] + F + ["sim"], b, se): print(f"{n:8s} {c:7.2f} (t={c / s_:5.1f})")
