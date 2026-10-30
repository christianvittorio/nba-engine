"""Walk-forward (rolling-origin) backtest and metrics.

One chronological pass: for every game the forecast is produced and STORED
from state that has seen only earlier games; only then is the result ingested
and the state updated.  Evaluation reads the stored forecasts back from SQLite.
"""
from __future__ import annotations

import json
import math
import numpy as np
import pandas as pd

from . import MODEL_VERSION
from .elo import Elo, EloParams
from .sim import TeamProfiles, ProfileParams, simulate_game, apply_dispersion, summarize
from .store import Store

PCTS = [5, 10, 25, 50, 75, 90, 95]


class RunningSD:
    """Online RMS of forecast residuals (used to give Elo / baselines a predictive spread)."""

    def __init__(self, prior_sd: float, prior_n: float = 100.0):
        self.s, self.n, self.prior = 0.0, 0.0, (prior_sd ** 2, prior_n)

    def sd(self) -> float:
        return math.sqrt((self.s + self.prior[0] * self.prior[1]) / (self.n + self.prior[1]))

    def add(self, resid: float):
        self.s += resid ** 2
        self.n += 1


def _norm_q(mean: float, sd: float) -> dict:
    from scipy.stats import norm
    return {str(p): float(mean + sd * norm.ppf(p / 100)) for p in PCTS}


def _norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def calibrate_dispersion(games: pd.DataFrame, profiles: TeamProfiles, n_sims: int, stride: int,
                         seed0: int) -> dict:
    """Fit kappa_margin / kappa_total on a warm-up season; leaves `profiles` advanced through it."""
    M, T, smu, stu, ssd_m, ssd_t = [], [], [], [], [], []
    for i, g in enumerate(games.itertuples(index=False)):
        gd = g._asdict()
        profiles.new_season(gd["season"])
        pred_poss = profiles.expected_poss(gd["home"], gd["away"])
        if i % stride == 0:
            sim = simulate_game(profiles, gd["home"], gd["away"], n_sims, seed0 + int(gd["game_id"]), 0.0)
            m = sim["home_pts"] - sim["away_pts"]
            t = sim["home_pts"] + sim["away_pts"]
            M.append(gd["home_pts"] - gd["away_pts"]); T.append(gd["home_pts"] + gd["away_pts"])
            smu.append(m.mean()); stu.append(t.mean()); ssd_m.append(m.std()); ssd_t.append(t.std())
        profiles.record_pace_residual(pred_poss, gd)
        profiles.update(gd)
    M, T, smu, stu = map(np.array, (M, T, smu, stu))
    resid_t = T - stu
    return {"kappa_margin": float((M - smu).std() / np.mean(ssd_m)),
            "kappa_total": float(resid_t.std() / np.mean(ssd_t)),
            "n_calibration_games": int(len(M)),
            "total_level_bias_end": float(resid_t[-60:].mean())}


def run_backtest(games: pd.DataFrame, store: Store, elo_params: EloParams, warmup_seasons: list[int],
                 calib_season: int, eval_seasons: list[int], n_sims: int, seed0: int = 20261017,
                 calib_sims: int = 1000, calib_stride: int = 3, progress=print) -> dict:
    prof = TeamProfiles(ProfileParams())
    elo = Elo(elo_params)

    # ---- warm-up (no forecasts scored): advance state only
    for g in games[games.season.isin(warmup_seasons)].itertuples(index=False):
        gd = g._asdict()
        elo.new_season(gd["season"]); prof.new_season(gd["season"])
        elo.update(gd["home"], gd["away"], gd["home_pts"], gd["away_pts"])
        prof.record_pace_residual(prof.expected_poss(gd["home"], gd["away"]), gd)
        prof.update(gd)

    # ---- calibration season: Elo advanced fully, simulator dispersion fitted
    cal = games[games.season == calib_season]
    for g in cal.itertuples(index=False):
        gd = g._asdict()
        elo.new_season(gd["season"])
        elo.update(gd["home"], gd["away"], gd["home_pts"], gd["away_pts"])
    cal_info = calibrate_dispersion(cal, prof, calib_sims, calib_stride, seed0)
    progress(f"calibration (season {calib_season}): {json.dumps(cal_info)}")
    kappa_m, kappa_t = cal_info["kappa_margin"], cal_info["kappa_total"]

    # baselines' running state (start from the warm-up+calibration seasons)
    prior = games[games.season.isin(warmup_seasons + [calib_season])]
    hw = (prior.home_pts > prior.away_pts).mean()
    mm, mt = (prior.home_pts - prior.away_pts).mean(), (prior.home_pts + prior.away_pts).mean()
    base = {"n": float(len(prior)), "hw": hw * len(prior), "m": mm * len(prior), "t": mt * len(prior)}
    sd_m_elo, sd_m_base, sd_t_base = RunningSD(13.5), RunningSD(13.5), RunningSD(18.5)
    level_delta, alpha = cal_info["total_level_bias_end"], 0.01   # online total-level correction

    sim_params = {"sim_engine": "possession_mc", "n_sims": n_sims, "kappa_margin": kappa_m,
                  "kappa_total": kappa_t, "profile": vars(prof.p), "calibration": cal_info}
    store.add_model_version("sim_mc", MODEL_VERSION, sim_params)
    store.add_model_version("sim_mc_raw", MODEL_VERSION, {**sim_params, "note": "no dispersion calibration"})
    store.add_model_version("elo", MODEL_VERSION, vars(elo_params))
    store.add_model_version("home_const", MODEL_VERSION, {"note": "running home-win rate / margin / total"})

    ev = games[games.season.isin(eval_seasons)].reset_index(drop=True)
    store.add_games(ev)
    total = len(ev)
    for i, g in enumerate(ev.itertuples(index=False)):
        gd = g._asdict()
        s, gid, h, a = gd["season"], int(gd["game_id"]), gd["home"], gd["away"]
        elo.new_season(s); prof.new_season(s)
        cutoff = f"all games before season {s} game_id {gid} (schedule-order proxy; no timestamps in source)"
        seed = seed0 + gid

        # --- Elo (margin only; its "total" is left empty rather than borrowed from a baseline)
        bhw, bm, bt = base["hw"] / base["n"], base["m"] / base["n"], base["t"] / base["n"]
        e = elo.predict(h, a)
        sd_e = sd_m_elo.sd()
        store.save_forecast(s, gid, "elo", MODEL_VERSION, cutoff, None, None, e["p_home"],
                            (bt + e["exp_margin"]) / 2, (bt - e["exp_margin"]) / 2, None, None,
                            q_margin=_norm_q(e["exp_margin"], sd_e), q_total=None,
                            details={"elo_diff": e["elo_diff"], "margin_sd": sd_e, "exp_margin": e["exp_margin"]})
        # --- constant baseline
        store.save_forecast(s, gid, "home_const", MODEL_VERSION, cutoff, None, None, bhw,
                            (bt + bm) / 2, (bt - bm) / 2, bt, None,
                            q_margin=_norm_q(bm, sd_m_base.sd()), q_total=_norm_q(bt, sd_t_base.sd()),
                            details={})
        # --- simulator (raw and calibrated)
        pred_poss = prof.expected_poss(h, a)
        sim = simulate_game(prof, h, a, n_sims, seed, 0.0)
        raw = summarize(sim)
        cal = summarize(apply_dispersion(sim, kappa_m, kappa_t, level_delta))
        for name, summ, det in (("sim_mc_raw", raw, {}), ("sim_mc", cal, {"level_delta": level_delta})):
            store.save_forecast(s, gid, name, MODEL_VERSION, cutoff, seed, n_sims, summ["p_home"],
                                summ["mean_home"], summ["mean_away"], summ["mean_total"], summ["p_ot"],
                                q_margin=summ["q_margin"], q_total=summ["q_total"],
                                details={**det, "mc_se_p_home": summ["mc_se_p_home"],
                                         "modal_score": [summ["modal_score_home"], summ["modal_score_away"]],
                                         "median_score": [summ["median_home"], summ["median_away"]],
                                         "mean_poss": summ["mean_poss"]})
        # ------- the game is played: ingest result, THEN update state
        store.add_result(s, gid, gd["home_pts"], gd["away_pts"])
        am, at = gd["home_pts"] - gd["away_pts"], gd["home_pts"] + gd["away_pts"]
        level_delta = (1 - alpha) * level_delta + alpha * (at - raw["mean_total"])
        sd_m_elo.add(am - e["exp_margin"]); sd_m_base.add(am - bm); sd_t_base.add(at - bt)
        base["n"] += 1; base["hw"] += float(am > 0); base["m"] += am; base["t"] += at
        elo.update(h, a, gd["home_pts"], gd["away_pts"])
        prof.record_pace_residual(pred_poss, gd)
        prof.update(gd)
        if (i + 1) % 300 == 0:
            store.commit(); progress(f"  {i + 1}/{total} games forecast")
    store.commit()
    return cal_info


# ----------------------------------------------------------------------------
# Evaluation (reads stored forecasts back from SQLite)
# ----------------------------------------------------------------------------
def evaluate(store: Store, results_scope: str = "all") -> pd.DataFrame:
    q = """SELECT f.season, f.game_id, f.model_name, f.model_version, f.p_home, f.mean_margin, f.mean_total,
                  f.q_margin_json, f.q_total_json, f.p_ot, r.home_pts, r.away_pts, g.n_periods
           FROM forecasts f JOIN results r USING(season, game_id) JOIN games g USING(season, game_id)"""
    df = pd.read_sql_query(q, store.con)
    df["y"] = (df.home_pts > df.away_pts).astype(int)
    df["margin"] = df.home_pts - df.away_pts
    df["total"] = df.home_pts + df.away_pts
    df["ot"] = (df.n_periods > 4).astype(int)
    return df


def metrics(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, d in df.groupby("model_name"):
        p = d.p_home.clip(1e-6, 1 - 1e-6)
        y = d.y
        row = {"model": name, "n": len(d),
               "brier": float(((p - y) ** 2).mean()),
               "log_loss": float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()),
               "accuracy": float(((p > .5) == (y == 1)).mean()),
               "margin_mae": float((d.margin - d.mean_margin).abs().mean()),
               "margin_rmse": float(np.sqrt(((d.margin - d.mean_margin) ** 2).mean()))}
        if d.mean_total.notna().all():
            row["total_mae"] = float((d.total - d.mean_total).abs().mean())
            row["total_rmse"] = float(np.sqrt(((d.total - d.mean_total) ** 2).mean()))
        for lo, hi, label in ((25, 75, "50"), (10, 90, "80"), (5, 95, "90")):
            qm = d.q_margin_json.map(lambda s: json.loads(s) if isinstance(s, str) else None)
            if qm.notna().all():
                lo_v = qm.map(lambda q: q[str(lo)]); hi_v = qm.map(lambda q: q[str(hi)])
                row[f"margin_cov{label}"] = float(((d.margin >= lo_v) & (d.margin <= hi_v)).mean())
                row[f"margin_width{label}"] = float((hi_v - lo_v).mean())
            qt = d.q_total_json.map(lambda s: json.loads(s) if isinstance(s, str) else None)
            if qt.notna().all():
                lo_v = qt.map(lambda q: q[str(lo)]); hi_v = qt.map(lambda q: q[str(hi)])
                row[f"total_cov{label}"] = float(((d.total >= lo_v) & (d.total <= hi_v)).mean())
        if d.p_ot.notna().all():
            row["ot_brier"] = float(((d.p_ot - d.ot) ** 2).mean())
        rows.append(row)
    return pd.DataFrame(rows).set_index("model")


def calibration_table(df: pd.DataFrame, model: str, bins=(0, .3, .4, .5, .6, .7, .8, 1.0)) -> pd.DataFrame:
    d = df[df.model_name == model].copy()
    d["bin"] = pd.cut(d.p_home, bins=list(bins), include_lowest=True)
    t = d.groupby("bin", observed=True).agg(n=("y", "size"), mean_pred=("p_home", "mean"), observed=("y", "mean"))
    return t.round(3)
