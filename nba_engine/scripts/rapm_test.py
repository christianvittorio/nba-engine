"""Does a roster-aware strength rating (ridge RAPM from lineup stints) add to the sim's margin?  Walk-forward on one season.
Rating fitted only on games BEFORE each test month (all earlier stints, ridge). Game strength = sum_i rating_i * minutes_i/48 (home - away),
using the minutes players actually played (an upper bound: it knows who played). Compare residual of actual margin vs the sim margin."""
import os, sys, pickle, numpy as np, pandas as pd
from scipy import sparse
from sklearn.linear_model import Ridge
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
from nbaengine.gamedata import load_all
from nbaengine.layers import stints, home_away
from nbaengine.feed import ESPN_TO_NBA
CACHE = os.environ.get("CACHE", "/tmp/rapm_stints.pkl")
TEST = int(os.environ.get("TEST", 2025)); ALPHA = float(os.environ.get("ALPHA", 2500))
if os.path.exists(CACHE):
    S, M = pickle.load(open(CACHE, "rb"))
else:
    recs = [r for r in load_all(f"{ROOT}/artifacts/gamedata")]
    S = stints(recs)
    M = {}   # espn game id -> (date, home abbr)
    for r in recs:
        h, a = home_away(r)
        if h: ab = r["teams"][h]["abbr"]; M[r["game_id"]] = (r["date"], ESPN_TO_NBA.get(ab, ab))
    pickle.dump((S, M), open(CACHE, "wb"))
S = S[S.sec > 0].copy(); S["net48"] = (S.pf - S.pa) * 2880 / S.sec
H = S[S.is_home]; A = S[~S.is_home].set_index(["game_id", "date", "period"])  # not used; build per-game home-perspective rows below
home = S[S.is_home].reset_index(drop=True)
opp = S[~S.is_home].reset_index(drop=True)
assert len(home) == len(opp)
# rows are aligned per (game, stint boundary) only if same flush; verify by game/sec
assert (home.game_id.values == opp.game_id.values).all() and np.allclose(home.sec.values, opp.sec.values)
D = pd.DataFrame({"game_id": home.game_id, "date": home.date, "sec": home.sec, "net": (home.pf - home.pa), "hl": home.lineup, "al": opp.lineup})
ids = sorted({i for lu in D.hl for i in lu} | {i for lu in D.al for i in lu}); ix = {p: k for k, p in enumerate(ids)}
rows, cols, vals = [], [], []
for r, (hl, al) in enumerate(zip(D.hl, D.al)):
    for p in hl: rows.append(r); cols.append(ix[p]); vals.append(1.0)
    for p in al: rows.append(r); cols.append(ix[p]); vals.append(-1.0)
X = sparse.csr_matrix((vals, (rows, cols)), shape=(len(D), len(ids)))
y = (D.net / D.sec * 2880).values; w = D.sec.values / 60.0
# per game per player minutes (home +, away -) for the strength sum
mins = {}
for g, lu_h, lu_a, sec in zip(D.game_id, D.hl, D.al, D.sec):
    d = mins.setdefault(g, {})
    for p in lu_h: d[p] = d.get(p, 0) + sec / 60
    for p in lu_a: d[p] = d.get(p, 0) - sec / 60
# mapping to NBA game ids
G = pd.concat([pd.read_csv(f"{ROOT}/data/processed/games_cdn_{s}.csv") for s in (2025, 2026)])
key = {(str(d), h): gid for gid, d, h in zip(G.game_id, G.date, G.home)}
D["nba_id"] = [key.get(M.get(g, (None, None))) for g in D.game_id]
dates = D.groupby("game_id").date.first().sort_values()
sim = pd.read_csv(f"{ROOT}/data/processed/team_stats_bt_{TEST}_all.csv")[["game_id", "date", "all_home_pts_reg", "all_away_pts_reg"]]
sim["sim"] = sim.all_home_pts_reg - sim.all_away_pts_reg
act = G.set_index("game_id"); sim["y"] = (act.loc[sim.game_id, "home_pts"] - act.loc[sim.game_id, "away_pts"]).values
sim["month"] = sim.date.astype(str).str[:7]
esp_by_nba = {v: k for k, v in D.drop_duplicates("game_id").set_index("game_id").nba_id.items()}
# leakage-safe minutes: each player's exponentially weighted minutes from EARLIER games (hl 10), applied to the players who suited up,
# rescaled to 240 per team; actual minutes leak the outcome (garbage time)
USE_EXP = os.environ.get("EXPMIN", "1") == "1"
emin = {}
if USE_EXP:
    ew, lam = {}, 0.5 ** (1 / 10.0)
    gm = D.groupby("game_id").date.first().sort_values().index
    side_of = {}
    for g in gm:
        d = mins[g]; exp = {p: ew.get(p, 8.0) for p in d}
        for sgn in (1, -1):
            ps = [p for p in d if (d[p] > 0) == (sgn > 0)]; tot = sum(exp[p] for p in ps) or 1
            for p in ps: exp[p] = exp[p] * 240.0 / tot * sgn
        emin[g] = exp
        for p, mn in d.items(): ew[p] = lam * ew.get(p, mn) + (1 - lam) * abs(mn)
pred = {}
for mth in sorted(sim.month.unique()):
    start = sim[sim.month == mth].date.astype(str).min()
    tr = (D.date.astype(str) < start).values
    if tr.sum() < 20000: continue
    # shrink toward 0: ridge on unit-per-48 ratings; mild recency not applied
    m = Ridge(alpha=ALPHA, fit_intercept=True).fit(X[tr], y[tr], sample_weight=w[tr]); r = m.coef_
    for gid in sim[sim.month == mth].game_id:
        eg = esp_by_nba.get(gid)
        if eg is None or eg not in mins: continue
        pred[gid] = sum(r[ix[p]] * mn / 48.0 for p, mn in (emin[eg] if USE_EXP else mins[eg]).items()) + 0  # home - away points per game
sim["rapm"] = sim.game_id.map(pred); T = sim.dropna(subset=["rapm"]).reset_index(drop=True)
print(len(T), "test games with a rating; sim MAE %.3f" % (T.y - T.sim).abs().mean())
res = T.y - T.sim
b = np.polyfit(T.rapm, res, 1); print("residual (actual-sim) on roster strength: slope %.3f, corr %.3f, n=%d" % (b[0], np.corrcoef(T.rapm, res)[0, 1], len(T)))
pr = np.full(len(T), np.nan)
for i in range(150, len(T)):
    tr = T.iloc[:i]; Xt = np.c_[np.ones(i), tr.sim, tr.rapm]; bb = np.linalg.solve(Xt.T @ Xt + 20 * np.eye(3), Xt.T @ tr.y); pr[i] = bb @ [1, T.sim[i], T.rapm[i]]
print("walk-forward MAE after adding roster strength: %.3f vs sim %.3f" % ((T.y[150:] - pr[150:]).abs().mean(), (T.y[150:] - T.sim[150:]).abs().mean()))
# does roster strength add beyond the existing availability layer (missing rotation value)?
MV = pd.read_csv(f"{ROOT}/data/processed/missing_value.csv"); MV = MV[MV.season == TEST + 0].set_index("game_id")
T["mv"] = (MV.loc[T.game_id, "mv_away"].values - MV.loc[T.game_id, "mv_home"].values)   # home minus away missing value: more away missing = good for home
for name, cols in (("sim + availability", ["sim", "mv"]), ("sim + availability + roster strength", ["sim", "mv", "rapm"])):
    pr = np.full(len(T), np.nan)
    for i in range(150, len(T)):
        tr = T.iloc[:i]; Xt = np.c_[np.ones(i), tr[cols].values]; bb = np.linalg.solve(Xt.T @ Xt + 20 * np.eye(Xt.shape[1]), Xt.T @ tr.y)
        pr[i] = bb @ np.r_[1, T.loc[i, cols].values.astype(float)]
    print("%-38s walk-forward MAE %.3f" % (name, (T.y[150:] - pr[150:]).abs().mean()))
