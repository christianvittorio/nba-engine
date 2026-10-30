"""Player projection model: minutes, per-minute rates, availability, and box-score simulation.

(Source restored by hand from the compiled module after the file was overwritten; behaviour is
differential-tested against the original bytecode.)
"""
from __future__ import annotations

import copy
import json
import os
from dataclasses import asdict, dataclass, field

import numpy as np
import pandas as pd

BUCKETS = [("A", 30.0), ("B", 22.0), ("C", 14.0), ("D", 0.0)]
COUNT = ["fga", "fta", "reb", "ast", "stl", "blk", "tov"]
DEFAULT_LG = {"fga": 0.45, "fta": 0.12, "reb": 0.19, "ast": 0.12, "stl": 0.033, "blk": 0.02, "tov": 0.07,
              "s3": 0.4, "p3": 0.355, "p2": 0.55, "ft": 0.78}
HIST_STATS = ["min", "pts", "reb", "ast", "stl", "blk", "tov", "tpm", "tpa", "fgm", "fga", "ftm", "fta"]
MIN_EDGES = [0, 8, 15, 22, 28, 34, 100]
OUT_STATS = ["min", "pts", "reb", "ast", "stl", "blk", "tov", "tpm", "tpa", "fgm", "fga", "ftm", "fta", "pra"]
QS = [5, 10, 25, 50, 75, 90, 95]
SUMKEYS = ["min", "fga", "fta", "reb", "ast", "stl", "blk", "tov", "tpa", "tpm", "m2a", "m2m", "ftm"]


def bucket(m: float) -> str:
    for b, lo in BUCKETS:
        if m >= lo:
            return b
    return "D"


def min_bucket(m: float) -> int:
    for i in range(len(MIN_EDGES) - 1):
        if MIN_EDGES[i] <= m < MIN_EDGES[i + 1]:
            return i
    return len(MIN_EDGES) - 2


@dataclass
class PlayerParams:
    hl_min: float = 12.0
    hl_rate: float = 40.0
    rollover: float = 0.75
    k_min: float = 150.0
    k_s3: float = 60.0
    k_p3: float = 80.0
    k_p2: float = 120.0
    k_ft: float = 40.0
    cap: float = 40.0
    team_minutes: float = 241.0
    pool_window: int = 8
    ext_window: int = 40
    beta: dict = field(default_factory=lambda: {s: 0.0 for s in COUNT})
    nb_k: dict = field(default_factory=lambda: {s: 1e6 for s in COUNT})
    min_resid: list = field(default_factory=list)
    p_play: dict = field(default_factory=dict)
    sigma_shoot: float = 0.0


def allocate_minutes(base: np.ndarray, total: float, cap: float) -> np.ndarray:
    """Water-filling: minutes proportional to base, capped, summing to `total` when feasible."""
    b = np.asarray(base, dtype=float)
    if len(b) == 0:
        return b
    b = np.maximum(b, 0.5)
    if np.minimum(cap, b * 1e6).sum() <= total:
        return np.minimum(cap, b * 1e6)
    lo, hi = 0.0, 1e6
    for _ in range(60):
        s = 0.5 * (lo + hi)
        if np.minimum(cap, s * b).sum() > total:
            hi = s
        else:
            lo = s
    return np.minimum(cap, 0.5 * (lo + hi) * b)


def _zeros():
    return {k: 0.0 for k in SUMKEYS}


class PlayerModel:
    def __init__(self, params: PlayerParams | None = None):
        self.p = params or PlayerParams()
        self.pl: dict = {}
        self.names: dict = {}
        self.team_gp: dict = {}
        self.lg = {b: _zeros() for b, _ in BUCKETS}
        self.season = None
        self.n_games = 0

    def _lam(self, hl):
        return 0.5 ** (1.0 / hl)

    def ewm_min(self, pid: int):
        st = self.pl.get(pid)
        if not st or st["w_den"] <= 0:
            return None
        return st["w_num"] / st["w_den"]

    def league_rates(self, b: str) -> dict:
        r = dict(DEFAULT_LG)
        s = self.lg[b]
        if s["min"] > 300:
            for k in COUNT:
                r[k] = s[k] / s["min"]
        if s["fga"] > 100:
            r["s3"] = s["tpa"] / s["fga"]
        if s["tpa"] > 100:
            r["p3"] = s["tpm"] / s["tpa"]
        if s["m2a"] > 100:
            r["p2"] = s["m2m"] / s["m2a"]
        if s["fta"] > 100:
            r["ft"] = s["ftm"] / s["fta"]
        return r

    def rates(self, pid: int) -> dict:
        p = self.p
        st = self.pl.get(pid)
        m = self.ewm_min(pid)
        lg = self.league_rates(bucket(m if m is not None else 10.0))
        S = st["S"] if st else _zeros()
        r = {k: (S[k] + p.k_min * lg[k]) / (S["min"] + p.k_min) for k in COUNT}
        r["s3"] = (S["tpa"] + p.k_s3 * lg["s3"]) / (S["fga"] + p.k_s3)
        r["p3"] = (S["tpm"] + p.k_p3 * lg["p3"]) / (S["tpa"] + p.k_p3)
        r["p2"] = (S["m2m"] + p.k_p2 * lg["p2"]) / (S["m2a"] + p.k_p2)
        r["ft"] = (S["ftm"] + p.k_ft * lg["ft"]) / (S["fta"] + p.k_ft)
        return r

    def pool(self, team: str, window: int | None = None) -> list:
        w = window if window is not None else self.p.pool_window
        gp = self.team_gp.get(team, 0)
        return [pid for pid, st in self.pl.items() if st["team"] == team and gp - st["last_tg"] < w]

    def misses_last5(self, pid: int) -> int:
        return int(sum(1 for x in self.pl[pid]["flags"][-5:] if x == 0))

    def update_game(self, rows: pd.DataFrame, season: int) -> None:
        p = self.p
        if self.season is not None and self.season != season:
            for st in self.pl.values():
                for k in SUMKEYS:
                    st["S"][k] *= p.rollover
            for b in self.lg:
                for k in SUMKEYS:
                    self.lg[b][k] *= 0.6
        self.season = season
        lam_r, lam_m = self._lam(p.hl_rate), self._lam(p.hl_min)
        for team, g in rows.groupby("team"):
            self.team_gp[team] = self.team_gp.get(team, 0) + 1
            gp = self.team_gp[team]
            played = g[g["min"] > 0]
            ids = set(int(x) for x in played["player_id"])
            flagged = set()
            for pid, st in self.pl.items():
                if st["team"] == team and gp - 1 - st["last_tg"] < p.ext_window:
                    st["flags"] = (st["flags"] + [1 if pid in ids else 0])[-10:]
                    flagged.add(pid)
            for r in played.itertuples(index=False):
                pid = int(r.player_id)
                if r.name:
                    self.names[pid] = r.name
                st = self.pl.get(pid)
                if st is None:
                    st = {"team": team, "last_tg": gp, "n": 0, "w_num": 0.0, "w_den": 0.0, "S": _zeros(),
                          "hist": [], "flags": [], "start_ewm": 0.0}
                    self.pl[pid] = st
                m_pre = self.ewm_min(pid)
                b = bucket(m_pre if m_pre is not None else 10.0)
                vals = {"min": r.min, "fga": r.fga, "fta": r.fta, "reb": r.reb, "ast": r.ast, "stl": r.stl,
                        "blk": r.blk, "tov": r.tov, "tpa": r.tpa, "tpm": r.tpm, "m2a": r.fga - r.tpa,
                        "m2m": r.fgm - r.tpm, "ftm": r.ftm}
                for k in SUMKEYS:
                    self.lg[b][k] += vals[k]
                    st["S"][k] = st["S"][k] * lam_r + vals[k]
                st["w_num"] = st["w_num"] * lam_m + r.min
                st["w_den"] = st["w_den"] * lam_m + 1.0
                st["n"] += 1
                st["team"], st["last_tg"] = team, gp
                st["hist"] = (st["hist"] + [[float(getattr(r, k)) for k in HIST_STATS]])[-10:]
                if pid not in flagged:
                    st["flags"] = (st["flags"] + [1])[-10:]
        self.n_games += 1

    def project_team(self, team: str, active: list | None = None, mode: str = "confirmed",
                     extra_unknown: dict | None = None, pool_ids: list | None = None) -> pd.DataFrame:
        p = self.p
        pool = list(pool_ids) if pool_ids is not None else self.pool(team)
        act = pool if active is None else list(active)
        actset = set(act)
        absent = [x for x in pool if x not in actset]
        confirmed = mode == "confirmed"
        f = min(0.6, sum(self.ewm_min(x) or 0.0 for x in absent) / 240.0) if confirmed else 0.0
        ids = act if confirmed else pool
        base, unknown = [], []
        for pid in ids:
            m = self.ewm_min(pid)
            if m is None:
                m = (extra_unknown or {}).get(pid, 10.0)
                unknown.append(pid)
            base.append(m)
        base = np.array(base, dtype=float)
        mins = allocate_minutes(base, p.team_minutes, p.cap) if confirmed else base
        rows = []
        for pid, m0, m in zip(ids, base, mins):
            r = self.rates(pid)
            if confirmed:
                for s in COUNT:
                    r[s] *= 1.0 + p.beta.get(s, 0.0) * f
            st = self.pl.get(pid)
            miss = self.misses_last5(pid) if st else 2
            pp = p.p_play.get(f"{bucket(m0)}|{min(miss, 2)}", 0.85) if mode == "unconfirmed" else 1.0
            row = {"player_id": pid, "name": self.names.get(pid, str(pid)), "base_min": float(m0),
                   "proj_min": float(m), "p_play": float(pp), "is_new": pid in unknown, "f": f,
                   "n_games": st["n"] if st else 0}
            row.update({f"r_{k}": v for k, v in r.items()})
            rows.append(row)
        return pd.DataFrame(rows)

    def baseline_means(self, pid: int, n: int = 10):
        st = self.pl.get(pid)
        if not st or not st["hist"]:
            return None
        return dict(zip(HIST_STATS, np.array(st["hist"][-n:]).mean(axis=0)))

    def to_dict(self) -> dict:
        return {"params": asdict(self.p),
                "pl": {str(k): v for k, v in self.pl.items()},
                "names": {str(k): v for k, v in self.names.items()},
                "team_gp": self.team_gp, "lg": self.lg, "season": self.season, "n_games": self.n_games}

    @staticmethod
    def from_dict(d: dict) -> "PlayerModel":
        pr = dict(d["params"])
        pr["min_resid"] = [np.asarray(x, dtype=float) for x in pr.get("min_resid", [])]
        m = PlayerModel(PlayerParams(**pr))
        m.pl = {int(k): v for k, v in d["pl"].items()}
        m.names = {int(k): v for k, v in d["names"].items()}
        m.team_gp = d["team_gp"]
        m.lg = d["lg"]
        m.season = d["season"]
        m.n_games = d["n_games"]
        return m

    def save(self, path: str) -> None:
        d = self.to_dict()
        d["params"]["min_resid"] = [list(map(float, np.asarray(x))) for x in self.p.min_resid]
        with open(path + ".tmp", "w") as fh:
            json.dump(d, fh)
        os.replace(path + ".tmp", path)

    @staticmethod
    def load(path: str) -> "PlayerModel":
        with open(path) as fh:
            return PlayerModel.from_dict(json.load(fh))


def _nb(rng, mu, k):
    mu = np.maximum(mu, 1e-9)
    return rng.negative_binomial(k, k / (k + mu))


def sample_players(proj: pd.DataFrame, params: PlayerParams, n_sims: int, seed: int,
                   mode: str = "confirmed") -> dict:
    """Draw box-score lines. Returns {stat: array (players, sims)}."""
    rng = np.random.default_rng(seed)
    P = len(proj)
    if P == 0:
        return {s: np.zeros((0, n_sims)) for s in OUT_STATS}
    pm = proj["proj_min"].to_numpy()
    minutes = np.empty((P, n_sims))
    for i in range(P):
        pool = params.min_resid[min_bucket(pm[i])] if params.min_resid else np.array([0.0])
        pool = np.asarray(pool) if len(pool) else np.array([0.0])
        minutes[i] = pm[i] + rng.choice(pool, size=n_sims)
    minutes = np.clip(minutes, 0.5, 48.0)

    def col(name):
        return proj[name].to_numpy()[:, None]

    def mu(s):
        return minutes * col("r_" + s)

    fga = _nb(rng, mu("fga"), params.nb_k["fga"])
    fta = _nb(rng, mu("fta"), params.nb_k["fta"])
    form = rng.normal(0.0, params.sigma_shoot, size=(P, n_sims)) if params.sigma_shoot > 0 else 0.0

    def lg(p):
        return 1.0 / (1.0 + np.exp(-(np.log(p / (1 - p)) + form)))

    p3 = lg(np.clip(col("r_p3"), 0.02, 0.98))
    p2 = lg(np.clip(col("r_p2"), 0.02, 0.98))
    pft = lg(np.clip(col("r_ft"), 0.02, 0.99))
    tpa = rng.binomial(fga, np.clip(col("r_s3"), 0, 1))
    tpm = rng.binomial(tpa, p3)
    m2m = rng.binomial(fga - tpa, p2)
    ftm = rng.binomial(fta, pft)
    out = {"min": minutes, "fga": fga, "fta": fta, "tpa": tpa, "tpm": tpm, "fgm": m2m + tpm, "ftm": ftm,
           "pts": 2 * m2m + 3 * tpm + ftm}
    for s in ("reb", "ast", "stl", "blk", "tov"):
        out[s] = _nb(rng, mu(s), params.nb_k[s])
    out["pra"] = out["pts"] + out["reb"] + out["ast"]
    if mode == "unconfirmed":
        played = rng.random((P, n_sims)) < col("p_play")
        out = {k: np.where(played, v, 0) for k, v in out.items()}
    return out


def summarize_samples(samp: dict, line_from_mean: bool = True) -> list:
    P = next(iter(samp.values())).shape[0]
    res = []
    for i in range(P):
        d = {}
        for s in OUT_STATS:
            x = samp[s][i]
            mean = float(x.mean())
            line = float(np.floor(mean) + 0.5)
            d[s] = {"mean": mean, "q": [float(v) for v in np.percentile(x, QS)], "line": line,
                    "p_over": float((x > line).mean())}
        res.append(d)
    return res
