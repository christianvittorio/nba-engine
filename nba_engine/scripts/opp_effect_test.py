"""Does the opponent's defence predict a player's stats beyond the player's own rates?  Walk-forward, 2025-26 player forecasts (confirmed lineup).
Opponent factor for stat s = (opponent's recent allowed s per game, half-life 25 games, shrunk to league) / league average, using only earlier games.
Test: weighted regression of  actual/forecast - 1  on  factor - 1  (weights = forecast), first half of season fits k, second half checks it."""
import sys, json
import numpy as np, pandas as pd
STATS = ["pts", "ast", "tpm", "tpa", "reb", "fga", "fta", "tov", "stl", "blk"]
HL, PRIOR = 25.0, 8.0


def team_games():
    L = pd.concat([pd.read_csv(f"data/processed/player_games_{y}.csv") for y in (2022, 2023, 2024, 2025, 2026)])
    L = L[L["min"] > 0]
    T = L.groupby(["season", "game_id", "team", "opp"])[STATS].sum().reset_index().sort_values("game_id")
    return T


def opp_factors(T):
    """for every (game, team): factors describing the OPPONENT's defence before that game"""
    lam = 0.5 ** (1.0 / HL)
    state, lg, rows = {}, {s: [0.0, 0.0] for s in STATS}, []      # state[team] = {stat: [wsum_x, wsum_w]}
    for gid, g in T.groupby("game_id", sort=True):
        if len(g) != 2:
            continue
        a, b = g.iloc[0], g.iloc[1]
        lgm = {s: lg[s][0] / lg[s][1] if lg[s][1] > 0 else np.nan for s in STATS}
        for me, op in ((a, b), (b, a)):
            st = state.get(op.team)
            f = {"season": me.season, "game_id": gid, "team": me.team}
            for s in STATS:
                if st is None or np.isnan(lgm[s]):
                    f[f"of_{s}"] = 1.0
                else:
                    f[f"of_{s}"] = ((st[s][0] + PRIOR * lgm[s]) / (st[s][1] + PRIOR)) / lgm[s]
            rows.append(f)
        for me, op in ((a, b), (b, a)):      # then update: `me.<stat>` was ALLOWED by op's defence
            st = state.setdefault(op.team, {s: [0.0, 0.0] for s in STATS})
            for s in STATS:
                st[s][0] = st[s][0] * lam + me[s]; st[s][1] = st[s][1] * lam + 1.0
                lg[s][0] = lg[s][0] * 0.9995 + me[s]; lg[s][1] = lg[s][1] * 0.9995 + 1.0
    return pd.DataFrame(rows)


if __name__ == "__main__":
    F = opp_factors(team_games())
    F.to_pickle("data/processed/opp_factors.pkl")
    d = pd.read_pickle("/home/claude/nba_engine/artifacts/player_eval_frame.pkl")
    d = d[(d["mode"] == "confirmed") & (d.played == 1)].merge(F, on=["season", "game_id", "team"])
    d = d.sort_values("game_id"); half = d.game_id.median()
    print("rows", len(d), "factor spread (sd of PHX-type factors):", {s: round(float(d[f'of_{s}'].std()), 3) for s in STATS})
    rows = []
    for s in STATS:
        f, a = d[f"mean_{s}"].to_numpy(), d[f"a_{s}"].to_numpy(); x = d[f"of_{s}"].to_numpy() - 1.0
        ok = f > 0.05
        def kfit(m):
            w = f[ok & m]; y = (a[ok & m] / f[ok & m] - 1.0); xx = x[ok & m]
            k = (w * xx * y).sum() / (w * xx * xx).sum(); se = np.sqrt(((w * (y - k * xx) ** 2).sum() / (len(w) - 1)) / (w * xx * xx).sum())
            return k, se
        k1, s1 = kfit(d.game_id.to_numpy() <= half); k2, s2 = kfit(d.game_id.to_numpy() > half); kk, sk = kfit(np.ones(len(d), bool))
        # held-out: apply k fitted on first half to second half
        m2 = (d.game_id.to_numpy() > half) & ok
        e0 = np.abs(a[m2] - f[m2]).mean(); e1 = np.abs(a[m2] - f[m2] * (1 + k1 * x[m2]).clip(0.7, 1.3)).mean()
        rows.append({"stat": s, "k first half": k1, "k 2nd half": k2, "k all": kk, "se all": sk, "t": kk / sk, "2nd-half MAE before": e0, "after (k from 1st half)": e1})
    print(pd.DataFrame(rows).round(3).to_string(index=False))
