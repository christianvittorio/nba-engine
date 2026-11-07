"""Fit how much missing rotation players move each team's OWN points and its opponent's points, so availability can act inside the simulation.

For every 2022-26 game (walk-forward, player model sees only earlier games): missing value of each team =
sum over pool players who did not play of usual_minutes * max(0, quality_per_min - 0.32)   (same definition as nbaengine/injury.py).
Regression, per season intercept:  points - simulator mean  ~  a * own_missing + b * opponent_missing   (home and away stacked, + home flag).
Fitted on 2023-24, checked on 2025-26 without refitting. Writes artifacts/availability_fit.json and data/processed/missing_value.csv."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
import numpy as np, pandas as pd
from nbaengine.injury import missing_value
from nbaengine.players import PlayerModel, PlayerParams
from nbaengine.players_backtest import load_logs, run_pass

tpl = json.load(open("artifacts/player_state.json"))["params"]
pp = PlayerParams(**{**tpl, "min_resid": [np.asarray(x, float) for x in tpl["min_resid"]]})
rec = []


def collect(model, season, gid, rows):
    if season < 2023:
        return
    teams = rows.groupby("team")
    out = {"season": season, "game_id": gid}
    for side in ("home", "away"):
        pass
    for team, g in teams:
        played = set(g.loc[g["min"] > 0, "player_id"].astype(int))
        pool = set(model.pool(team))
        mv, _ = missing_value(model, team, [p for p in pool if p not in played])
        out[team] = mv
    rec.append(out)


L = load_logs([2022, 2023, 2024, 2025, 2026])
games = pd.concat([pd.read_csv(f"data/processed/games_cdn_{s}.csv")[["game_id", "home", "away"]] for s in (2023, 2024, 2025, 2026)])
hm = dict(zip(games.game_id, games.home)); am = dict(zip(games.game_id, games.away))
run_pass(L, pp, 2023, collector=collect)
MV = pd.DataFrame([{"season": r["season"], "game_id": r["game_id"], "mv_home": r.get(hm.get(r["game_id"]), np.nan), "mv_away": r.get(am.get(r["game_id"]), np.nan)} for r in rec])
MV.to_csv("data/processed/missing_value.csv", index=False)
P = pd.concat([pd.read_csv(f"data/processed/trend_proj_{s}.csv") for s in (2023, 2024, 2025, 2026)]).merge(MV, on=["season", "game_id"])
P = P.dropna(subset=["mv_home", "mv_away"])
print("games:", len(P), " missing value: mean", P.mv_home.mean().round(2), " share with >0:", (P.mv_home > 0).mean().round(2))


def stack(d):
    h = pd.DataFrame({"y": d.home_pts - d.sim_home, "own": d.mv_home, "opp": d.mv_away, "home": 1, "season": d.season})
    a = pd.DataFrame({"y": d.away_pts - d.sim_away, "own": d.mv_away, "opp": d.mv_home, "home": 0, "season": d.season})
    return pd.concat([h, a])


def fit(d):
    S = stack(d)
    X = np.column_stack([S.own, S.opp, S.home] + [(S.season == s).astype(float) for s in sorted(S.season.unique())])
    beta, *_ = np.linalg.lstsq(X, S.y.to_numpy(), rcond=None)
    res = S.y.to_numpy() - X @ beta
    cov = np.linalg.inv(X.T @ X) * res.var()
    return beta[:2], np.sqrt(np.diag(cov))[:2]


tr, te = P[P.season <= 2024], P[P.season >= 2025]
TYPICAL = float(pd.concat([tr.mv_home, tr.mv_away]).mean())
print('typical missing value (2023-24):', round(TYPICAL, 2))
(a, b), (sa, sb) = fit(tr)
print(f"fit 2023-24: own {a:+.3f} (se {sa:.3f})  opponent {b:+.3f} (se {sb:.3f})  points per unit of missing value")
for s in (2023, 2024, 2025, 2026):
    (aa, bb), (ssa, ssb) = fit(P[P.season == s]); print(f"  season {s}: own {aa:+.3f}±{ssa:.3f} opp {bb:+.3f}±{ssb:.3f}")


def evaluate(d, a, b, label):
    # season-level level shift is removed so the comparison isolates availability (intercept = mean residual of the fit sample)
    mbar = TYPICAL      # the team profiles already contain a typical amount of absence; only the deviation from it is added
    adj_h = d.sim_home + a * (d.mv_home - mbar) + b * (d.mv_away - mbar); adj_a = d.sim_away + a * (d.mv_away - mbar) + b * (d.mv_home - mbar)
    out = {}
    for nm, h, aw in (("without availability", d.sim_home, d.sim_away), ("with availability", adj_h, adj_a)):
        m = (d.home_pts - d.away_pts) - (h - aw); t = (d.home_pts + d.away_pts) - (h + aw)
        out[nm] = (m.abs().mean(), t.abs().mean(), np.sqrt((m ** 2).mean()), m.mean(), t.mean())
    print(label, " (margin MAE, total MAE, margin RMSE, margin bias, total bias)")
    for k, v in out.items():
        print("  ", k.ljust(22), *[f"{x:.3f}" for x in v])
    return out


evaluate(te, a, b, "TEST 2025-26 (coefficients from 2023-24)")
evaluate(P, *fit(P)[0], "ALL 2023-26 (in-sample)")
(a_all, b_all), _ = fit(P)
json.dump({"own_pts_per_unit": float(a_all), "opp_pts_per_unit": float(b_all), "fit_2023_24": [float(a), float(b)], "typical_missing_value": TYPICAL, "n_games": int(len(P)),
           "definition": "missing value = sum(usual minutes * max(0, quality/min - 0.32)) of rotation-pool players who did not play"},
          open("artifacts/availability_fit.json", "w"), indent=1)
