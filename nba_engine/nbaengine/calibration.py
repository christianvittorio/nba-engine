"""Calibration checks of the team layer (win probability, margin, total, team points, intervals) and the player layer
(minutes and box-score stats), on past walk-forward projections and on the live season, plus a controlled recalibration
of the dispersion constants.

Nothing here changes a forecast by itself: `suggest_dispersion` only reports; scripts/calibration_report.py applies a
change to state.json only when its guard conditions are met and says so.
"""
from __future__ import annotations

import json
import os
import sqlite3

import numpy as np
import pandas as pd
from scipy.stats import norm

from . import trends as T

QS = (5, 10, 25, 50, 75, 90, 95)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------------------------- team frame
def walk_forward_frame(root: str = ROOT, kappa_m: float | None = None, kappa_t: float | None = None) -> pd.DataFrame:
    """2023-2026 walk-forward projections, one row per game, with calibrated quantiles built from the stored raw ones."""
    km, kt = (kappa_m, kappa_t) if kappa_m is not None else (0.7839391839831196, 0.9209561875321809)
    d = T.load_projected(root)
    need = {"m_mean", "t_mean", "rm_q50", "rt_q50"}
    if not need <= set(d.columns):
        raise RuntimeError("trend_proj files lack quantile columns: rerun scripts/build_trend_projections.py for each season")
    d["margin"] = d.home_pts - d.away_pts
    d["total"] = d.home_pts + d.away_pts
    d["ot"] = (d.n_periods > 4).astype(float)
    d["proj_margin_c"] = d.m_mean                                           # calibration keeps the mean margin
    d["proj_total_c"] = d.t_mean + d.level                                  # + online scoring-level correction
    for q in QS:
        d[f"cm_q{q}"] = d.m_mean + km * (d[f"rm_q{q}"] - d.m_mean)
        d[f"ct_q{q}"] = d.t_mean + d.level + kt * (d[f"rt_q{q}"] - d.t_mean)
    d["source"] = np.where(d.season <= 2026, "walk-forward", "live")
    return d


def live_frame(db_path: str) -> pd.DataFrame:
    """Live-season games with stored forecasts (immutable) and results."""
    if not os.path.exists(db_path):
        return pd.DataFrame()
    con = sqlite3.connect(db_path)
    try:
        f = pd.read_sql_query("""SELECT f.season, f.game_id, f.model_name, f.p_home, f.mean_home, f.mean_away, f.mean_margin, f.mean_total,
               f.p_ot, f.q_margin_json, f.q_total_json, r.home_pts, r.away_pts, g.n_periods, g.home, g.away
               FROM forecasts f JOIN results r USING(season, game_id) JOIN games g USING(season, game_id)
               WHERE f.model_name IN ('sim_mc','elo','sim_mc_rest','sim_mc_sit','sim_mc_inj','sim_mc_full','sim_mc_all')""", con)
    except Exception:
        return pd.DataFrame()
    finally:
        con.close()
    if f.empty:
        return f
    f["margin"] = f.home_pts - f.away_pts
    f["total"] = f.home_pts + f.away_pts
    f["ot"] = (f.n_periods > 4).astype(float)
    return f


# ---------------------------------------------------------------------------------------------- metrics
def _ll(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean())


def reliability(p: np.ndarray, y: np.ndarray, bins=(0, .15, .25, .35, .45, .55, .65, .75, .85, 1.0)) -> pd.DataFrame:
    b = pd.cut(p, list(bins), include_lowest=True)
    d = pd.DataFrame({"b": b, "p": p, "y": y}).groupby("b", observed=True).agg(n=("y", "size"), predicted=("p", "mean"), observed=("y", "mean"))
    d["gap"] = d.observed - d.predicted
    return d.reset_index().assign(bin=lambda x: x.b.astype(str)).drop(columns="b")


def team_metrics(d: pd.DataFrame) -> dict:
    """d: walk_forward_frame rows (any subset)."""
    y = (d.margin > 0).astype(float).to_numpy()
    out = {"n": int(len(d))}
    for name, col in (("sim", "sim_p_home"), ("elo", "elo_p_home")):
        out[f"{name}_brier"] = float(((d[col] - y) ** 2).mean()); out[f"{name}_log_loss"] = _ll(d[col].to_numpy(), y)
        out[f"{name}_accuracy"] = float(((d[col] > .5) == (y == 1)).mean())
    out["home_win_rate_actual"] = float(y.mean()); out["home_win_rate_predicted"] = float(d.sim_p_home.mean())
    e_m, e_t = d.margin - d.proj_margin_c, d.total - d.proj_total_c
    out.update({"margin_bias": float(e_m.mean()), "margin_mae": float(e_m.abs().mean()), "margin_rmse": float(np.sqrt((e_m ** 2).mean())),
                "total_bias": float(e_t.mean()), "total_mae": float(e_t.abs().mean()), "total_rmse": float(np.sqrt((e_t ** 2).mean())),
                "home_pts_bias": float((d.home_pts - (d.proj_total_c + d.proj_margin_c) / 2).mean()),
                "away_pts_bias": float((d.away_pts - (d.proj_total_c - d.proj_margin_c) / 2).mean()),
                "p_ot_pred": float(d.sim_p_ot.mean()), "p_ot_actual": float(d.ot.mean())})
    for tag, a, p in (("margin", d.margin, d.proj_margin_c), ("total", d.total, d.proj_total_c)):
        X = np.column_stack([np.ones(len(d)), p - p.mean()])
        b = np.linalg.lstsq(X, a.to_numpy(), rcond=None)[0]
        res = a.to_numpy() - X @ b
        se = np.sqrt(res.var() / ((p - p.mean()) ** 2).sum())
        out[f"{tag}_slope"], out[f"{tag}_slope_se"] = float(b[1]), float(se)
    for tag, a in (("margin", d.margin), ("total", d.total)):
        for lo, hi, lab in ((25, 75, 50), (10, 90, 80), (5, 95, 90)):
            c = "cm" if tag == "margin" else "ct"
            out[f"{tag}_cov{lab}"] = float(((a >= d[f"{c}_q{lo}"]) & (a <= d[f"{c}_q{hi}"])).mean())
    return out


def by_total_bucket(d: pd.DataFrame) -> pd.DataFrame:
    b = pd.cut(d.proj_total_c, [0, 220, 226, 232, 238, 400], labels=["<220", "220-226", "226-232", "232-238", "238+"])
    g = d.assign(b=b, err=d.total - d.proj_total_c, over=(d.total > d.proj_total_c).astype(float)).groupby("b", observed=True)
    return g.agg(n=("err", "size"), projected=("proj_total_c", "mean"), actual=("total", "mean"), bias=("err", "mean"), over_rate=("over", "mean")).reset_index().assign(b=lambda x: x.b.astype(str)).rename(columns={"b": "projected total"})


def team_bias(d: pd.DataFrame, last_n: int = 25) -> pd.DataFrame:
    """Per-team recent bias of points scored/allowed versus projection (shrunk toward zero), to spot teams the model misjudges."""
    rows = []
    h = pd.DataFrame({"date": d.date, "team": d.home, "pts": d.home_pts, "allowed": d.away_pts,
                      "proj": (d.proj_total_c + d.proj_margin_c) / 2, "proj_allowed": (d.proj_total_c - d.proj_margin_c) / 2})
    a = pd.DataFrame({"date": d.date, "team": d.away, "pts": d.away_pts, "allowed": d.home_pts,
                      "proj": (d.proj_total_c - d.proj_margin_c) / 2, "proj_allowed": (d.proj_total_c + d.proj_margin_c) / 2})
    t = pd.concat([h, a]).sort_values(["team", "date"])
    for tm, g in t.groupby("team"):
        g = g.tail(last_n)
        e_o, e_d = g.pts - g.proj, g.allowed - g.proj_allowed
        n = len(g)
        rows.append({"team": tm, "n": n, "points_vs_proj": e_o.mean(), "allowed_vs_proj": e_d.mean(),
                     "z_points": e_o.mean() / (e_o.std() / np.sqrt(n)) if n > 3 else 0.0,
                     "z_allowed": e_d.mean() / (e_d.std() / np.sqrt(n)) if n > 3 else 0.0,
                     "margin_vs_proj": (e_o - e_d).mean()})
    return pd.DataFrame(rows).sort_values("margin_vs_proj")


# ---------------------------------------------------------------------------------------------- dispersion recalibration
def _nll(a, mu, sd):
    return float(-norm.logpdf(a, mu, sd).mean())


def suggest_dispersion(d: pd.DataFrame, current_km: float, current_kt: float, window: int = 600, holdout: int = 300) -> dict:
    """Refit the two spread constants on the window just BEFORE the most recent `holdout` games, then compare current vs refit on
    those held-out games (normal log-likelihood with the stored simulator spread). kappa = RMS residual / mean simulator sd."""
    d = d.sort_values(["season", "game_id"]).reset_index(drop=True)
    te = d.tail(holdout)
    tr = d.iloc[max(0, len(d) - holdout - window): len(d) - holdout]
    res = {"window_games": int(len(tr)), "holdout_games": int(len(te)), "current": {"kappa_margin": current_km, "kappa_total": current_kt}}
    km = float(np.sqrt(((tr.margin - tr.m_mean) ** 2).mean()) / tr.m_sd.mean())
    kt = float(np.sqrt(((tr.total - tr.proj_total_c) ** 2).mean()) / tr.t_sd.mean())
    res["refit"] = {"kappa_margin": km, "kappa_total": kt}
    for tag, a, mu, sd_raw, k0, k1 in (("margin", te.margin, te.m_mean, te.m_sd, current_km, km),
                                       ("total", te.total, te.proj_total_c, te.t_sd, current_kt, kt)):
        res[f"{tag}_holdout_nll_current"] = _nll(a, mu, k0 * sd_raw)
        res[f"{tag}_holdout_nll_refit"] = _nll(a, mu, k1 * sd_raw)
        res[f"{tag}_holdout_gain_pct"] = 100 * (res[f"{tag}_holdout_nll_current"] - res[f"{tag}_holdout_nll_refit"]) / abs(res[f"{tag}_holdout_nll_current"])
    return res


# ---------------------------------------------------------------------------------------------- player layer
PSTATS = ["min", "pts", "reb", "ast", "stl", "blk", "tov", "tpm", "fgm", "fga", "ftm", "fta", "pra"]


def player_metrics(M: pd.DataFrame, played_only: bool, stats=PSTATS) -> pd.DataFrame:
    D = M[M.played == 1] if played_only else M
    rows = []
    for s in stats:
        if f"mean_{s}" not in D or f"a_{s}" not in D:
            continue
        y = D[f"a_{s}"]
        row = {"stat": s, "n": int(len(D)), "mean_forecast": float(D[f"mean_{s}"].mean()), "mean_actual": float(y.mean()),
               "bias": float((y - D[f"mean_{s}"]).mean()), "mae": float((y - D[f"mean_{s}"]).abs().mean())}
        for lo, hi, lab in ((25, 75, 50), (10, 90, 80), (5, 95, 90)):
            row[f"cov{lab}"] = float(((y >= D[f"q{lo}_{s}"]) & (y <= D[f"q{hi}_{s}"])).mean())
        rows.append(row)
    return pd.DataFrame(rows)


def retrospective_player_frame(root: str = ROOT) -> pd.DataFrame:
    p = os.path.join(root, "artifacts/player_eval_frame.pkl")
    return pd.read_pickle(p) if os.path.exists(p) else pd.DataFrame()
