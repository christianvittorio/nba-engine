"""Compare team forecasts built from the roster that plays (player values) against Elo and the stored simulation, on past games, out of sample.
Roster strength for a game = sum over the team's players who played of (trailing minutes / 240) x player value, where player value is the
box-score composite per minute (current season to date plus half of last season, shrunk to the league average) and trailing minutes are known before tip.
Usage: python scripts/roster_forecast_test.py"""
import os, sys, numpy as np, pandas as pd, sqlite3
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
from nbaengine.elo import Elo, EloParams
R = ROOT + "/data/processed/"; S = (2022, 2023, 2024, 2025, 2026)
G = pd.concat([pd.read_csv(R + f"games_cdn_{y}.csv", usecols=["game_id", "home", "away", "home_pts", "away_pts", "date"]).assign(season=y) for y in S]).sort_values(["season", "date", "game_id"]).reset_index(drop=True)
cols = ["game_id", "season", "team", "player_id", "min", "pts", "reb", "oreb", "ast", "stl", "blk", "tov", "fgm", "fga", "ftm", "fta"]
P = pd.concat([pd.read_csv(R + f"player_games_{y}.csv", usecols=cols) for y in S]); P = P[P["min"] > 0].copy()
P["gs"] = P.pts + 0.4 * P.fgm - 0.7 * P.fga - 0.4 * (P.fta - P.ftm) + 0.7 * P.oreb + 0.3 * (P.reb - P.oreb) + P.stl + 0.7 * P.ast + 0.7 * P.blk - P.tov
byg = {k: v for k, v in P.groupby("game_id")}
K_SHRINK, PREV_W = 600.0, 0.5
cum = {}      # player -> [gs, min] this season ; prev -> same for last season ; mins -> trailing minutes list
prev = {}; recent = {}; team_recent = {}
MODE = os.environ.get('MODE', 'played')   # played: players who played this game (injury-report-like); expected: union of the team's last 3 games' players (no knowledge of tonight's absences)
lg_rate = {}
def start_season(s):
    global prev, cum, recent
    prev = {p: v for p, v in cum.items()}; cum = {}; recent = {p: v[-10:] for p, v in recent.items()}
cur = None; rows = []
e = Elo(EloParams(k=20, home_adv=45, carryover=0.7, init=1505, mov_scale=1.0))
for r in G.itertuples():
    if r.season != cur:
        if cur is not None: start_season(r.season)
        cur = r.season
        lg = sum(v[0] for v in prev.values()) / max(sum(v[1] for v in prev.values()), 1.0) if prev else 0.0
    e.new_season(r.season); ed = e.predict(r.home, r.away)["elo_diff"]
    pg = byg.get(r.game_id)
    strength = {}
    if pg is not None and len(cum) + len(prev) > 0:
        for t, side in ((r.home, "h"), (r.away, "a")):
            tp = pg[pg.team == t]; items = []
            plist = list(tp.player_id) if MODE == 'played' else sorted(set().union(*team_recent.get(t, [set()])))
            for p in plist:
                m = recent.get(p)
                w = float(np.mean(m)) if m else (prev.get(p, [0, 0])[1] / 70.0 if prev.get(p) else 10.0)
                gs_c, mn_c = cum.get(p, [0.0, 0.0]); gs_p, mn_p = prev.get(p, [0.0, 0.0])
                rate = (gs_c + PREV_W * gs_p + K_SHRINK * lg) / (mn_c + PREV_W * mn_p + K_SHRINK) if (mn_c + mn_p) >= 0 else lg
                items.append((min(w, 36.0), rate - lg))
            items = sorted(items, key=lambda x: -x[0])[:10]; tot = sum(w for w, _ in items) or 1.0; sc = min(1.0, 240.0 / tot)
            strength[side] = sum(w * sc / 240.0 * v for w, v in items)
    rows.append((ed, strength.get("h", np.nan) - strength.get("a", np.nan)))
    e.update(r.home, r.away, r.home_pts, r.away_pts)
    if pg is not None:
        for p, mn, gs in zip(pg.player_id, pg["min"], pg.gs):
            c = cum.setdefault(p, [0.0, 0.0]); c[0] += gs; c[1] += mn; recent.setdefault(p, []).append(mn); recent[p] = recent[p][-10:]
        for t_ in (r.home, r.away):
            team_recent.setdefault(t_, []).append(set(pg[pg.team == t_].player_id)); team_recent[t_] = team_recent[t_][-3:]
G[["ed", "rd"]] = rows
G["win"] = (G.home_pts > G.away_pts) * 1.0; G["am"] = G.home_pts - G.away_pts
n_season = G.groupby("season").cumcount(); G["n"] = n_season
# games played by the home/away team so far this season (early-season flag)
gp = {}; g1 = []
for r in G.itertuples():
    k = (r.season, r.home), (r.season, r.away); g1.append((gp.get(k[0], 0) + gp.get(k[1], 0)) / 2); gp[k[0]] = gp.get(k[0], 0) + 1; gp[k[1]] = gp.get(k[1], 0) + 1
G["gpm"] = g1
# stored simulation forecasts (2024, 2025 seasons only)
c = sqlite3.connect(ROOT + "/artifacts/nba_engine.sqlite")
sim = pd.read_sql_query("select season, game_id, p_home sim from forecasts where model_name='sim_mc'", c)
G = G.merge(sim, on=["season", "game_id"], how="left")
H = G[(G.season >= 2023) & G.rd.notna()].copy(); H["lsim"] = np.log(H.sim / (1 - H.sim))
def fit(X, y, l2=1e-3):
    b = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-X @ b)); g = X.T @ (p - y) + l2 * b; W = p * (1 - p); b -= np.linalg.solve((X * W[:, None]).T @ X + l2 * np.eye(len(b)), g)
    return b
def design(d, kind):
    one = np.ones(len(d)); e_ = d.ed.values / 100.0; r_ = d.rd.values; s_ = d.lsim.values
    return {"elo": np.c_[one, e_], "roster": np.c_[one, r_], "elo+roster": np.c_[one, e_, r_], "sim": np.c_[one, s_], "sim+roster": np.c_[one, s_, r_], "sim+elo": np.c_[one, s_, e_], "sim+elo+roster": np.c_[one, s_, e_, r_]}[kind]
def ll_vec(p, y): p = np.clip(p, 1e-4, 1 - 1e-4); return -(y * np.log(p) + (1 - y) * np.log(1 - p))
def evaluate(kinds, splits, subset=None, need_sim=False):
    res = {k: [] for k in kinds}
    for tr, te in splits:
        a = H[H.season.isin(tr)]; b = H[H.season.isin(te)]
        if need_sim: a = a[a.sim.notna()]; b = b[b.sim.notna()]
        if subset is not None: b = b[subset(b)]
        for k in kinds:
            w = fit(design(a, k), a.win.values); p = 1 / (1 + np.exp(-design(b, k) @ w)); res[k].append(ll_vec(p, b.win.values))
    return {k: np.concatenate(v) for k, v in res.items()}
def report(title, kinds, splits, subset=None, need_sim=False, base="elo"):
    L = evaluate(kinds, splits, subset, need_sim); n = len(L[base]); print(f"\n{title} (n={n} games)")
    for k in kinds:
        d = L[k] - L[base]; print(f"  {k:16s} log-loss {L[k].mean():.4f}" + ("" if k == base else f"   vs {base}: {d.mean():+.4f} +/- {d.std() / np.sqrt(n):.4f}"))
SPL = (((2023, 2024), (2025, 2026)), ((2025, 2026), (2023, 2024)), ((2023, 2026), (2024, 2025)))
report("All games, Elo vs roster-built vs both", ["elo", "roster", "elo+roster"], SPL)
report("First 25 games per team", ["elo", "roster", "elo+roster"], SPL, subset=lambda b: b.gpm < 25)
big = H.copy(); first = big[big.gpm < 12]
report("Games 2024-25 only, with the stored simulation", ["sim", "elo", "elo+roster", "sim+elo", "sim+roster", "sim+elo+roster"], (((2024,), (2025,)), ((2025,), (2024,))), need_sim=True, base="sim")
report("Same, first 25 games per team", ["sim", "elo", "elo+roster", "sim+elo", "sim+roster", "sim+elo+roster"], (((2024,), (2025,)), ((2025,), (2024,))), subset=lambda b: b.gpm < 25, need_sim=True, base="sim")
