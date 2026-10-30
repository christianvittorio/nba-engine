"""Walk-forward harness for the player model: calibration passes and evaluation.

All statistics used to tune or fit parameters come from the warm-up/calibration seasons only; the evaluation season is
never touched until parameters are frozen.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .players import (COUNT, HIST_STATS, OUT_STATS, PlayerModel, PlayerParams, allocate_minutes, bucket, min_bucket)

LOG_COLS = ["game_id", "season", "date", "team", "player_id", "name", "start", "min", "pts", "reb", "oreb", "ast", "stl",
            "blk", "tov", "fgm", "fga", "tpm", "tpa", "ftm", "fta", "n_periods", "is_home", "opp"]


def load_logs(labels, root="data/processed") -> pd.DataFrame:
    L = pd.concat([pd.read_csv(f"{root}/player_games_{y}.csv") for y in labels], ignore_index=True)
    L["name"] = L["name"].fillna("")
    return L.sort_values(["season", "date", "game_id"]).reset_index(drop=True)


def run_pass(L: pd.DataFrame, params: PlayerParams, first_eval_label: int, collector=None, last_label: int | None = None,
             model: PlayerModel | None = None) -> PlayerModel:
    model = model or PlayerModel(params)
    for (season, _date, gid), rows in L.groupby(["season", "date", "game_id"], sort=True):
        if last_label is not None and season > last_label:
            break
        if collector is not None and season >= first_eval_label:
            collector(model, int(season), int(gid), rows)
        model.update_game(rows, int(season))
    return model


def participants(rows: pd.DataFrame, team: str) -> pd.DataFrame:
    g = rows[(rows["team"] == team) & (rows["min"] > 0)]
    return g


# ------------------------------------------------------------------------------ stage collectors
class MinutesCollector:
    """Minutes error of the confirmed-availability allocation (several caps) vs a last-10 average baseline."""

    def __init__(self, caps):
        self.caps = caps
        self.err = {c: [] for c in caps}
        self.err_base10, self.err_raw, self.w = [], [], []

    def __call__(self, model, season, gid, rows):
        for team in rows["team"].unique():
            g = participants(rows, team)
            ids = [int(x) for x in g["player_id"]]
            if len(ids) < 5:
                continue
            pr = model.project_team(team, active=ids, mode="confirmed")
            actual = dict(zip(g["player_id"].astype(int), g["min"]))
            known = ~pr["is_new"].to_numpy()
            a = np.array([actual[i] for i in pr["player_id"]])
            base = pr["base_min"].to_numpy()
            for c in self.caps:
                m = allocate_minutes(base, model.p.team_minutes, c)
                self.err[c].append(np.abs(m - a)[known])
            b10 = []
            for pid in pr["player_id"]:
                bm = model.baseline_means(int(pid))
                b10.append(bm["min"] if bm else np.nan)
            b10 = np.array(b10)
            self.err_base10.append(np.abs(b10 - a)[known])
            self.err_raw.append(np.abs(base - a)[known])

    def result(self):
        out = {f"cap{c}": float(np.nanmean(np.concatenate(v))) for c, v in self.err.items()}
        out["raw_ewm"] = float(np.nanmean(np.concatenate(self.err_raw)))
        out["last10_avg"] = float(np.nanmean(np.concatenate(self.err_base10)))
        return out


def poisson_dev(y, mu):
    mu = np.maximum(mu, 1e-9)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(y > 0, y * np.log(y / mu), 0.0)
    return 2 * (t - (y - mu))


class RateCollector:
    """Per-minute rate quality: Poisson deviance of count stats given ACTUAL minutes (isolates the rate model)."""

    def __init__(self):
        self.dev = {s: [] for s in COUNT}
        self.mae_pts = []
        self.base_mae_pts = []

    def __call__(self, model, season, gid, rows):
        for team in rows["team"].unique():
            g = participants(rows, team)
            for r in g.itertuples(index=False):
                pid = int(r.player_id)
                if pid not in model.pl or model.pl[pid]["n"] < 3:
                    continue
                rt = model.rates(pid)
                for s in COUNT:
                    self.dev[s].append(poisson_dev(getattr(r, s), rt[s] * r.min))
                mu_pts = rt["fga"] * r.min * (rt["s3"] * rt["p3"] * 3 + (1 - rt["s3"]) * rt["p2"] * 2) + rt["fta"] * r.min * rt["ft"]
                self.mae_pts.append(abs(r.pts - mu_pts))
                bm = model.baseline_means(pid)
                if bm:
                    self.base_mae_pts.append(abs(r.pts - bm["pts"] * r.min / max(bm["min"], 1.0)))

    def result(self):
        d = {s: float(np.mean(v)) for s, v in self.dev.items()}
        return {"dev": d, "dev_total": float(sum(d.values())), "pts_mae_given_minutes": float(np.mean(self.mae_pts)),
                "pts_mae_last10_per_min": float(np.mean(self.base_mae_pts))}


# ------------------------------------------------------------------------------ final calibration collector
class FitCollector:
    """Collect what is needed to fit the absence effect, dispersions, minutes residuals and DNP rates."""

    def __init__(self):
        self.conf, self.unconf = [], []

    def __call__(self, model, season, gid, rows):
        for team in rows["team"].unique():
            g = participants(rows, team)
            ids = [int(x) for x in g["player_id"]]
            pool = model.pool(team)
            if len(ids) >= 5:
                pr = model.project_team(team, active=ids, mode="confirmed")
                a = g.set_index("player_id")
                for r in pr.itertuples(index=False):
                    x = a.loc[r.player_id]
                    self.conf.append({"game_id": gid, "team": team, "player_id": r.player_id, "is_new": r.is_new,
                                      "base_min": r.base_min, "proj_min": r.proj_min, "f": r.f, "min": x["min"],
                                      **{f"r_{s}": getattr(r, f"r_{s}") for s in COUNT},
                                      **{f"r_{s}": getattr(r, f"r_{s}") for s in ("s3", "p3", "p2", "ft")},
                                      **{s: x[s] for s in COUNT}, "a_pts": x["pts"], "a_fgm": x["fgm"], "a_tpm": x["tpm"],
                                      "a_ftm": x["ftm"], "a_tpa": x["tpa"]})
            if pool:
                pu = model.project_team(team, mode="unconfirmed")
                played = set(ids)
                for r in pu.itertuples(index=False):
                    miss = model.misses_last5(int(r.player_id))
                    self.unconf.append({"bucket": bucket(r.base_min), "miss": min(miss, 2),
                                        "played": int(r.player_id in played)})


def fit_params(params: PlayerParams, fc: FitCollector, rng_seed: int = 7) -> tuple[PlayerParams, dict]:
    from dataclasses import replace
    diag = {}
    C = pd.DataFrame(fc.conf)
    C = C[~C["is_new"]].copy()
    # --- absence effect beta (through-origin weighted LS): beta = sum((a-e)f) / sum(e f^2), e = rate * actual minutes
    beta, k_nb = {}, {}
    for s in COUNT:
        e = C[f"r_{s}"] * C["min"]
        a = C[s]
        f = C["f"]
        beta[s] = float(((a - e) * f).sum() / max((e * f * f).sum(), 1e-9))
    diag["beta_raw"] = dict(beta)
    beta = {s: float(np.clip(v, -0.5, 2.5)) for s, v in beta.items()}
    # --- NB dispersion given ACTUAL minutes (after absence adjustment)
    for s in COUNT:
        mu = C[f"r_{s}"] * C["min"] * (1 + beta[s] * C["f"])
        v = ((C[s] - mu) ** 2 - mu).sum()
        k_nb[s] = float(np.clip((mu ** 2).sum() / v, 0.5, 1e6)) if v > 0 else 1e6
    diag["nb_k"] = dict(k_nb)
    # --- minutes residuals by bucket (given player plays)
    resid = []
    for b in range(len(MIN_EDGES) - 1):
        m = C[(C["proj_min"] >= MIN_EDGES[b]) & (C["proj_min"] < MIN_EDGES[b + 1])]
        r = (m["min"] - m["proj_min"]).to_numpy()
        resid.append(r if len(r) >= 30 else np.array([0.0]))
    diag["min_resid_n"] = [int(len(r)) for r in resid]
    diag["min_resid_sd"] = [float(np.std(r)) for r in resid]
    # --- DNP table
    U = pd.DataFrame(fc.unconf)
    pp = {}
    for (b, m), g in U.groupby(["bucket", "miss"]):
        pp[f"{b}|{m}"] = float((g["played"].sum() + 5 * 0.8) / (len(g) + 5))
    diag["p_play"] = pp
    diag["conf_rows"], diag["unconf_rows"] = int(len(C)), int(len(U))
    return replace(params, beta=beta, nb_k=k_nb, min_resid=resid, p_play=pp), diag


from .players import MIN_EDGES  # noqa: E402  (kept at the bottom to avoid a circular-looking import order)


# ------------------------------------------------------------------------------ evaluation pass
class EvalCollector:
    """Forecast every player of every game (both modes), store immutably, before the game updates the state."""

    def __init__(self, store, params: PlayerParams, n_sims: int, seed0: int, version: str):
        from .players import sample_players, summarize_samples
        self.store, self.params, self.n, self.seed0, self.version = store, params, n_sims, seed0, version
        self._sample, self._summ = sample_players, summarize_samples
        self.count = 0

    def _store(self, season, gid, team, pr, samp, mode, seed, active_ids, model):
        summ = self._summ(samp)
        for row, d in zip(pr.itertuples(index=False), summ):
            bm = model.baseline_means(int(row.player_id))
            st = model.pl.get(int(row.player_id))
            fl = st["flags"][-10:] if st else []
            part = (sum(fl) / len(fl)) if fl else 1.0
            details = {k: {"mean": round(v["mean"], 4), "q": [round(x, 3) for x in v["q"]], "line": v["line"],
                           "p_over": round(v["p_over"], 4)} for k, v in d.items()}
            details["baseline10"] = {k: round(float(v), 4) for k, v in bm.items()} if bm else None
            details["participation10"] = round(part, 3)
            self.store.save(season, gid, team, row.player_id, row.name, mode, self.version,
                            f"state before season {season} game {gid}", seed, self.n, row.proj_min, row.p_play,
                            row.is_new, {"active": active_ids, "absence_share_f": round(float(row.f), 4)}, details)
            self.count += 1

    def __call__(self, model, season, gid, rows):
        for ti, team in enumerate(sorted(rows["team"].unique())):
            g = participants(rows, team)
            ids = [int(x) for x in g["player_id"]]
            if len(ids) >= 5:
                pr = model.project_team(team, active=ids, mode="confirmed")
                seed = self.seed0 + gid * 100 + ti * 10 + 1
                self._store(season, gid, team, pr, self._sample(pr, self.params, self.n, seed, "confirmed"),
                            "confirmed", seed, ids, model)
            pool = model.pool(team)
            if pool:
                pu = model.project_team(team, mode="unconfirmed")
                seed = self.seed0 + gid * 100 + ti * 10 + 2
                self._store(season, gid, team, pu, self._sample(pu, self.params, self.n, seed, "unconfirmed"),
                            "unconfirmed", seed, pool, model)


# ------------------------------------------------------------------------------ metrics (read back from SQLite)
EVAL_STATS = ["min", "pts", "reb", "ast", "stl", "blk", "tov", "tpm", "tpa", "fgm", "fga", "ftm", "fta", "pra"]


def load_player_forecasts(db: str, version: str | None = None) -> pd.DataFrame:
    import json
    import sqlite3
    con = sqlite3.connect(db)
    q = ("SELECT season, game_id, team, player_id, name, mode, proj_min, p_play, is_new, assumptions_json, details_json "
         "FROM player_forecasts" + (f" WHERE model_version='{version}'" if version else ""))
    raw = pd.read_sql_query(q, con)
    recs = []
    for r in raw.itertuples(index=False):
        d = json.loads(r.details_json)
        a = json.loads(r.assumptions_json)
        x = {"season": r.season, "game_id": r.game_id, "team": r.team, "player_id": r.player_id, "name": r.name,
             "mode": r.mode, "proj_min": r.proj_min, "p_play": r.p_play, "is_new": r.is_new, "f": a.get("absence_share_f", 0.0),
             "part10": d.get("participation10", 1.0)}
        for s in EVAL_STATS:
            v = d[s]
            x[f"mean_{s}"] = v["mean"]
            for qi, qq in zip((5, 10, 25, 50, 75, 90, 95), v["q"]):
                x[f"q{qi}_{s}"] = qq
            x[f"line_{s}"], x[f"pover_{s}"] = v["line"], v["p_over"]
        b = d.get("baseline10")
        for s in EVAL_STATS:
            if s == "pra":
                x["b10_pra"] = (b["pts"] + b["reb"] + b["ast"]) if b else np.nan
            else:
                x[f"b10_{s}"] = b[s] if b else np.nan
        recs.append(x)
    return pd.DataFrame(recs)


def attach_actuals(F: pd.DataFrame, L: pd.DataFrame) -> pd.DataFrame:
    A = L[["season", "game_id", "team", "player_id", *[c for c in ["min", "pts", "reb", "ast", "stl", "blk", "tov", "tpm", "tpa", "fgm", "fga", "ftm", "fta"]]]].copy()
    A = A.rename(columns={c: f"a_{c}" for c in A.columns if c not in ("season", "game_id", "team", "player_id")})
    A["a_pra"] = A["a_pts"] + A["a_reb"] + A["a_ast"]
    M = F.merge(A, on=["season", "game_id", "team", "player_id"], how="left")
    M["played"] = M["a_min"].fillna(0).gt(0).astype(int)
    for c in [c for c in M.columns if c.startswith("a_")]:
        M[c] = M[c].fillna(0.0)
    return M


def player_metrics(M: pd.DataFrame) -> dict:
    out = {}
    for mode in ("confirmed", "unconfirmed"):
        D = M[(M["mode"] == mode) & (M["is_new"] == 0)].copy()
        if mode == "confirmed":
            D = D[D["played"] == 1]
        D = D[D["b10_pts"].notna()]
        rows = []
        for s in EVAL_STATS:
            y = D[f"a_{s}"]
            base = D[f"b10_{s}"] * (D["part10"] if mode == "unconfirmed" else 1.0)
            row = {"stat": s, "n": int(len(D)),
                   "mae_model_median": float((y - D[f"q50_{s}"]).abs().mean()),
                   "mae_model_mean": float((y - D[f"mean_{s}"]).abs().mean()),
                   "mae_baseline10": float((y - base).abs().mean()),
                   "rmse_model": float(np.sqrt(((y - D[f"mean_{s}"]) ** 2).mean())),
                   "rmse_baseline10": float(np.sqrt(((y - base) ** 2).mean())),
                   "actual_mean": float(y.mean()), "model_mean": float(D[f"mean_{s}"].mean())}
            for lo, hi, lab in ((25, 75, "50"), (10, 90, "80"), (5, 95, "90")):
                inside = (y >= D[f"q{lo}_{s}"]) & (y <= D[f"q{hi}_{s}"])
                row[f"cov{lab}"] = float(inside.mean())
                row[f"width{lab}"] = float((D[f"q{hi}_{s}"] - D[f"q{lo}_{s}"]).mean())
            rows.append(row)
        out[mode] = pd.DataFrame(rows).set_index("stat")
        # threshold probabilities
        th = []
        for s in ("pts", "reb", "ast", "pra", "tpm"):
            over = (D[f"a_{s}"] > D[f"line_{s}"]).astype(int)
            th.append(pd.DataFrame({"stat": s, "p": D[f"pover_{s}"], "y": over}))
        T = pd.concat(th)
        T["bin"] = pd.cut(T["p"], [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0], include_lowest=True)
        out[f"{mode}_threshold"] = T.groupby("bin", observed=True).agg(n=("y", "size"), predicted=("p", "mean"), observed=("y", "mean")).round(3)
        out[f"{mode}_brier_threshold"] = float(((T["p"] - T["y"]) ** 2).mean())
        # by projected minutes (role) for points, and by absence share
        D["role"] = pd.cut(D["proj_min"], [0, 15, 25, 32, 60], labels=["<15 min", "15-25", "25-32", "32+"])
        by = D.groupby("role", observed=True).apply(lambda g: pd.Series({
            "n": len(g), "mae_model_pts": (g["a_pts"] - g["q50_pts"]).abs().mean(),
            "mae_base_pts": (g["a_pts"] - g["b10_pts"] * (g["part10"] if mode == "unconfirmed" else 1.0)).abs().mean()}), include_groups=False)
        out[f"{mode}_by_role"] = by.round(3)
        if mode == "confirmed":
            D["fbin"] = pd.cut(D["f"], [-0.01, 0.0001, 0.1, 0.2, 1.0], labels=["no regulars out", "<10% of minutes out", "10-20%", ">20%"])
            byf = D.groupby("fbin", observed=True).apply(lambda g: pd.Series({
                "n": len(g), "mae_model_pts": (g["a_pts"] - g["q50_pts"]).abs().mean(), "mae_base_pts": (g["a_pts"] - g["b10_pts"]).abs().mean(),
                "mae_model_min": (g["a_min"] - g["q50_min"]).abs().mean(), "mae_base_min": (g["a_min"] - g["b10_min"]).abs().mean(),
                "model_mean_pts": g["mean_pts"].mean(), "actual_mean_pts": g["a_pts"].mean()}), include_groups=False)
            out["confirmed_by_absence"] = byf.round(3)
        else:
            D["pbin"] = pd.cut(D["p_play"], [0, .5, .7, .85, .95, 1.0], include_lowest=True)
            out["dnp_calibration"] = D.groupby("pbin", observed=True).agg(n=("played", "size"), predicted=("p_play", "mean"), observed=("played", "mean")).round(3)
    return out


def fit_sigma_shoot(params: PlayerParams, conf: pd.DataFrame, n_rows: int = 4000, n_sims: int = 300, seed: int = 11):
    """Choose the per-player-game shooting-form shock so predictive intervals for points are neither too tight nor too wide.
    Uses calibration rows only (full pipeline: minutes residuals + counts + shooting)."""
    from dataclasses import replace
    from .players import sample_players
    C = conf[~conf["is_new"]].sample(n=min(n_rows, len(conf)), random_state=seed).reset_index(drop=True)
    for s in COUNT:
        C[f"r_{s}"] = C[f"r_{s}"] * (1 + params.beta[s] * C["f"])
    res = {}
    for sig in (0.0, 0.1, 0.2, 0.3, 0.4):
        sm = sample_players(C, replace(params, sigma_shoot=sig), n_sims, seed, "confirmed")["pts"]
        y = C["a_pts"].to_numpy()[:, None]
        q = np.percentile(sm, [5, 10, 25, 75, 90, 95], axis=1)
        cov = {"50": float(((y[:, 0] >= q[2]) & (y[:, 0] <= q[3])).mean()),
               "80": float(((y[:, 0] >= q[1]) & (y[:, 0] <= q[4])).mean()),
               "90": float(((y[:, 0] >= q[0]) & (y[:, 0] <= q[5])).mean())}
        res[sig] = {"coverage": cov, "miss": abs(cov["50"] - .5) + abs(cov["80"] - .8) + abs(cov["90"] - .9)}
    best = min(res, key=lambda k: res[k]["miss"])
    return best, res
