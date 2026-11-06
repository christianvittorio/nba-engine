"""Compare team_stats_backtest.py predictions with real box scores (regulation games only). Prints tables; --md writes a report."""
import sys, os
import pandas as pd, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEAS = (2023, 2024, 2025, 2026)
ACT = {"fga": "fga", "fgm": "fgm", "fg3a": "3pa", "fg3m": "3pm", "fta": "fta", "ftm": "ftm", "tov": "tov", "oreb": "oreb"}


def load():
    B = pd.concat([pd.read_csv(f"{ROOT}/data/processed/team_stats_bt_{s}.csv") for s in SEAS])
    A = pd.concat([pd.read_csv(f"{ROOT}/data/processed/games_cdn_{s}.csv") for s in SEAS]).drop(columns=["date", "home", "away", "season", "n_periods"])
    D = B.merge(A, on="game_id")
    return D[D.n_periods == 4].sort_values("game_id").reset_index(drop=True)


def team_long(D, variant):
    """one row per team-game: predicted and actual box stats plus opponent's"""
    rows = []
    for side, opp in (("home", "away"), ("away", "home")):
        r = pd.DataFrame({"game_id": D.game_id, "season": D.season, "team": D[side], "opp": D[opp], "side": side})
        for k, a in ACT.items():
            r[f"p_{k}"] = D[f"{variant}_{side}_{k}"]; r[f"a_{k}"] = D[f"{side}_{a}"]
            r[f"po_{k}"] = D[f"{variant}_{opp}_{k}"]; r[f"ao_{k}"] = D[f"{opp}_{a}"]
        rows.append(r)
    return pd.concat(rows).sort_values("game_id").reset_index(drop=True)


def derived(T, pre):
    T[f"{pre}fg"] = T[f"{pre}fgm"] / T[f"{pre}fga"]
    T[f"{pre}fg3"] = T[f"{pre}fg3m"] / T[f"{pre}fg3a"]
    T[f"{pre}efg"] = (T[f"{pre}fgm"] + .5 * T[f"{pre}fg3m"]) / T[f"{pre}fga"]
    T[f"{pre}3par"] = T[f"{pre}fg3a"] / T[f"{pre}fga"]
    T[f"{pre}ftr"] = T[f"{pre}fta"] / T[f"{pre}fga"]
    return T


def table(variant, D):
    T = derived(derived(team_long(D, variant), "p_"), "a_")
    # leakage-safe baselines: team's own expanding mean, league expanding mean
    out = []
    stats = ["fga", "fgm", "fg3a", "fg3m", "fta", "tov", "oreb", "fg", "fg3", "efg", "3par", "ftr"]
    T = T.sort_values("game_id")
    for k in stats:
        a, p = T[f"a_{k}"], T[f"p_{k}"]
        own = T.groupby(["season", "team"])[f"a_{k}"].transform(lambda x: x.shift().expanding(min_periods=5).mean())
        lg = T.groupby("season")[f"a_{k}"].transform(lambda x: x.shift().expanding(min_periods=50).mean())
        m = own.notna() & lg.notna()
        out.append({"stat": k, "predicted": p.mean(), "actual": a.mean(), "bias": (a - p).mean(), "MAE model": (a - p).abs().mean(),
                    "MAE team-avg": (a - own)[m].abs().mean(), "MAE league-avg": (a - lg)[m].abs().mean(),
                    "MAE model (same games)": (a - p)[m].abs().mean(), "corr": float(np.corrcoef(a[m], p[m])[0, 1])})
    return pd.DataFrame(out), T


if __name__ == "__main__":
    D = load(); print("regulation games:", len(D))
    for v in ("base", "def"):
        t, _ = table(v, D); print("\n== variant", v); print(t.round(4).to_string(index=False))
