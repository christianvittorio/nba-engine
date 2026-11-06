"""Team box-score and advanced statistics from the stored per-game team box (`team_box` table) and, optionally, the simulator's
predicted box for the same games. All values per game unless named as a percentage/rating. Regulation-time normalisation is not
applied (overtime games count in full), exactly as published box scores do."""
from __future__ import annotations
import json, sqlite3
import numpy as np, pandas as pd

BOX = ["pts", "fga", "fgm", "fg3a", "fg3m", "fta", "ftm", "tov", "oreb", "dreb"]


def load_box(db_path: str, season: int | None = None) -> pd.DataFrame:
    con = sqlite3.connect(db_path)
    try:
        q = "SELECT b.*, d.date FROM team_box b LEFT JOIN game_dates d USING(season, game_id)"
        df = pd.read_sql_query(q + (f" WHERE b.season={int(season)}" if season else ""), con)
    except Exception:
        df = pd.DataFrame()
    con.close()
    return df


def with_opponent(df: pd.DataFrame) -> pd.DataFrame:
    """one row per team-game with the opponent's box next to it (prefix o_)"""
    o = df[["season", "game_id", "side"] + BOX].copy()
    o["side"] = np.where(o["side"] == "home", "away", "home")
    o = o.rename(columns={c: "o_" + c for c in BOX})
    return df.merge(o, on=["season", "game_id", "side"])


def advanced_table(df: pd.DataFrame) -> pd.DataFrame:
    """Per-team averages and advanced ratings (ORtg/DRtg per 100 possessions, four factors, shooting splits, both ends)."""
    if df.empty:
        return pd.DataFrame()
    t = with_opponent(df)
    t["poss"] = t.fga - t.oreb + t.tov + 0.44 * t.fta
    t["o_poss"] = t.o_fga - t.o_oreb + t.o_tov + 0.44 * t.o_fta
    g = t.groupby("team")
    s = g[BOX + ["o_" + c for c in BOX] + ["poss", "o_poss"]].sum()
    n = g.size()
    p = (s.poss + s.o_poss) / 2
    out = pd.DataFrame({
        "GP": n, "pts": s.pts / n, "opp pts": s.o_pts / n,
        "ORtg": 100 * s.pts / p, "DRtg": 100 * s.o_pts / p, "pace": p / n,
        "FG%": s.fgm / s.fga, "opp FG%": s.o_fgm / s.o_fga,
        "eFG%": (s.fgm + .5 * s.fg3m) / s.fga, "opp eFG%": (s.o_fgm + .5 * s.o_fg3m) / s.o_fga,
        "3PA": s.fg3a / n, "3PM": s.fg3m / n, "3P%": s.fg3m / s.fg3a, "opp 3PA": s.o_fg3a / n, "opp 3PM": s.o_fg3m / n, "opp 3P%": s.o_fg3m / s.o_fg3a,
        "3PAr": s.fg3a / s.fga, "opp 3PAr": s.o_fg3a / s.o_fga,
        "FTA": s.fta / n, "opp FTA": s.o_fta / n, "FTr": s.fta / s.fga, "FT%": s.ftm / s.fta,
        "TOV%": 100 * s.tov / s.poss, "opp TOV%": 100 * s.o_tov / s.o_poss,
        "ORB%": 100 * s.oreb / (s.oreb + s.o_dreb), "DRB%": 100 * s.dreb / (s.dreb + s.o_oreb),
    })
    out["NetRtg"] = out.ORtg - out.DRtg
    cols = ["GP", "pts", "opp pts", "ORtg", "DRtg", "NetRtg", "pace", "FG%", "opp FG%", "eFG%", "opp eFG%", "3PA", "3PM", "3P%", "opp 3PA", "opp 3PM", "opp 3P%",
            "3PAr", "opp 3PAr", "FTA", "opp FTA", "FTr", "FT%", "TOV%", "opp TOV%", "ORB%", "DRB%"]
    return out[cols].sort_values("NetRtg", ascending=False)


def predicted_vs_actual(db_path: str, season: int | None = None) -> pd.DataFrame:
    """Per game and side: simulator-predicted regulation box (from the immutable sim_mc forecast) next to the actual box. Regulation games only."""
    con = sqlite3.connect(db_path)
    try:
        F = pd.read_sql_query("SELECT season, game_id, details_json FROM forecasts WHERE model_name='sim_mc'", con)
    except Exception:
        con.close(); return pd.DataFrame()
    con.close()
    rows = []
    for r in F.itertuples():
        tb = json.loads(r.details_json).get("team_box")
        if tb:
            for side in ("home", "away"):
                rows.append({"season": r.season, "game_id": r.game_id, "side": side, **{f"p_{k}": v for k, v in tb[side].items()}})
    if not rows:
        return pd.DataFrame()
    P = pd.DataFrame(rows)
    A = load_box(db_path, season)
    if A.empty:
        return pd.DataFrame()
    A = A[A.n_periods == 4].rename(columns={c: f"a_{c}" for c in BOX})
    return A.merge(P, on=["season", "game_id", "side"])


def accuracy_table(M: pd.DataFrame) -> pd.DataFrame:
    if M.empty:
        return pd.DataFrame()
    rows = []
    M = M.copy()
    for k in ("fg", "fg3"):
        M[f"p_{k}"] = M[f"p_{k}m"] / M[f"p_{k}a"] if k == "fg3" else M["p_fgm"] / M["p_fga"]
        M[f"a_{k}"] = M[f"a_{k}m"] / M[f"a_{k}a"] if k == "fg3" else M["a_fgm"] / M["a_fga"]
    M["p_efg"] = (M.p_fgm + .5 * M.p_fg3m) / M.p_fga; M["a_efg"] = (M.a_fgm + .5 * M.a_fg3m) / M.a_fga
    labels = {"fga": "FGA", "fgm": "FGM", "fg": "FG%", "fg3a": "3PA", "fg3m": "3PM", "fg3": "3P%", "efg": "eFG%", "fta": "FTA", "ftm": "FTM", "tov": "TOV", "oreb": "OREB"}
    for k, lab in labels.items():
        a, p = M[f"a_{k}"], M[f"p_{k}"]
        ok = a.notna() & p.notna()
        rows.append({"stat": lab, "predicted": p[ok].mean(), "actual": a[ok].mean(), "bias": (a - p)[ok].mean(), "MAE": (a - p)[ok].abs().mean(),
                     "corr": float(np.corrcoef(a[ok], p[ok])[0, 1]) if ok.sum() > 3 else np.nan, "n": int(ok.sum())})
    return pd.DataFrame(rows)
