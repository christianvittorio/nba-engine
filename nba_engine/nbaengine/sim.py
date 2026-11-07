"""Team profiles (leakage-safe, exponentially weighted, shrunk) and a
possession-level Monte Carlo game simulator.

Simulation model (documented approximation, see BLUEPRINT.md section 5):

* The number of possessions per team in regulation is drawn per simulation
  (shared pace, both teams get the same count).
* Each possession ends in one of: turnover, a free-throw trip, or a field-goal
  attempt (2PA or 3PA). A missed FGA is followed by an offensive rebound with
  probability `oreb`, which grants another shot within the same possession.
* Team make-probabilities are shifted on the logit scale by a per-game,
  per-team "shooting night" effect N(0, sigma_form) so that game-level scoring
  variance is not just binomial noise. sigma_form is calibrated on warm-up games.
* Ties after regulation go to 5-minute overtimes simulated with the same
  engine (pace scaled by 5/48), repeated until broken.

Not modelled in v0.1: individual players, minutes, fouls/bonus, and-ones,
end-of-game fouling, garbage time, fatigue, injuries. Free-throw trips use a
fixed 2-or-3-attempt approximation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np

KEYS = ["poss", "tov", "ftrip", "fta", "ftm", "fga", "fg2a", "fg2m", "fg3a", "fg3m",
        "oreb_fg", "fgmiss", "oreb_ft", "ftmiss_trip"]
# (numerator, denominator, prior exposure in denominator units)
RATES = {
    "tov":   ("tov", "poss", 500.0),
    "ftrip": ("ftrip", "poss", 500.0),
    "s3":    ("fg3a", "fga", 400.0),
    "p2":    ("fg2m", "fg2a", 400.0),
    "p3":    ("fg3m", "fg3a", 250.0),
    "ft":    ("ftm", "fta", 150.0),
    "oreb":  ("oreb_fg", "fgmiss", 200.0),       # offensive rebound rate after a missed FG
    "orebft": ("oreb_ft", "ftmiss_trip", 80.0),  # ... after a missed last free throw of a trip
}
FT_PER_POSS_TRIP = 0.44
Q3 = 1.0 / FT_PER_POSS_TRIP - 2.0   # P(3 attempts) so that mean attempts/trip = 1/0.44


def _offense_row(g, side: str, opp: str, ot_norm: float) -> dict:
    fga, fg3a, fg3m, fgm = g[f"{side}_fga"], g[f"{side}_3pa"], g[f"{side}_3pm"], g[f"{side}_fgm"]
    fta = g[f"{side}_fta"]
    poss = g[f"{side}_fga"] + FT_PER_POSS_TRIP * fta - g[f"{side}_oreb"] + g[f"{side}_tov"]
    return {
        "poss": poss * ot_norm, "tov": g[f"{side}_tov"] * ot_norm, "ftrip": FT_PER_POSS_TRIP * fta * ot_norm,
        "fta": fta * ot_norm, "ftm": g[f"{side}_ftm"] * ot_norm, "fga": fga * ot_norm,
        "fg2a": (fga - fg3a) * ot_norm, "fg2m": (fgm - fg3m) * ot_norm,
        "fg3a": fg3a * ot_norm, "fg3m": fg3m * ot_norm,
        "oreb_fg": g[f"{side}_oreb_fg"] * ot_norm, "fgmiss": (fga - fgm) * ot_norm,
        "oreb_ft": g[f"{side}_oreb_ft"] * ot_norm,
        "ftmiss_trip": FT_PER_POSS_TRIP * (fta - g[f"{side}_ftm"]) * ot_norm,
    }


@dataclass
class ProfileParams:
    half_life_games: float = 40.0
    season_rollover: float = 0.6
    pace_prior_sd: float = 4.5
    league_half_life_games: float = 1230.0   # ~1 season: league scoring environment drifts
    def_effect: tuple = ()                   # rates whose DEFENSIVE side also moves the matchup (default: only offense for s3/ft/orebft)


class TeamProfiles:
    """Exponentially weighted offensive/defensive event profiles, updated game by game."""

    def __init__(self, params: ProfileParams | None = None):
        self.p = params or ProfileParams()
        self.lam = 0.5 ** (1.0 / self.p.half_life_games)
        self.lam_lg = 0.5 ** (1.0 / self.p.league_half_life_games)
        self.off: dict[str, dict] = {}
        self.deff: dict[str, dict] = {}
        self.pace_w: dict[str, list] = {}          # [sum_w*poss, sum_w]
        self.lg_side = {"home": {k: 0.0 for k in KEYS}, "away": {k: 0.0 for k in KEYS}}
        self.lg_pace = [0.0, 0.0]
        self.pace_sq = [0.0, 0.0]                   # [sum sq residual, n]
        self.season = None

    # ---- helpers
    def _zero(self):
        return {k: 0.0 for k in KEYS}

    def new_season(self, season: int):
        if self.season is not None and season != self.season:
            r = self.p.season_rollover
            for d in (self.off, self.deff):
                for t in d:
                    for k in KEYS:
                        d[t][k] *= r
            for t in self.pace_w:
                self.pace_w[t] = [self.pace_w[t][0] * r, self.pace_w[t][1] * r]
        self.season = season

    def league_rate(self, rate: str, side: str | None = None) -> float:
        num, den, prior = RATES[rate]
        if side is None:
            n = self.lg_side["home"][num] + self.lg_side["away"][num]
            d = self.lg_side["home"][den] + self.lg_side["away"][den]
        else:
            n, d = self.lg_side[side][num], self.lg_side[side][den]
        return n / d if d > 0 else {"tov": .13, "ftrip": .10, "s3": .39, "p2": .55, "p3": .36, "ft": .78, "oreb": .30, "orebft": .15}[rate]

    def _rate(self, table: dict, team: str, rate: str) -> float:
        num, den, prior = RATES[rate]
        lg = self.league_rate(rate)
        row = table.get(team)
        if row is None:
            return lg
        return (row[num] + prior * lg) / (row[den] + prior)

    def team_pace(self, team: str) -> float:
        lg = self.lg_pace[0] / self.lg_pace[1] if self.lg_pace[1] > 0 else 98.0
        w = self.pace_w.get(team)
        if not w or w[1] <= 0:
            return lg
        prior = 3.0  # games
        return (w[0] + prior * lg) / (w[1] + prior)

    def pace_sd(self) -> float:
        n0 = 50.0
        s, n = self.pace_sq
        return float(np.sqrt((s + n0 * self.p.pace_prior_sd ** 2) / (n + n0)))

    # ---- matchup rates for one team's offense vs the other's defense
    def matchup(self, off_team: str, def_team: str, side: str) -> dict:
        out = {}
        for r in RATES:
            lg = self.league_rate(r)
            lg_side = self.league_rate(r, side)
            val = lg_side + (self._rate(self.off, off_team, r) - lg) + (self._rate(self.deff, def_team, r) - lg)
            if r in ("ft", "s3", "orebft") and r not in self.p.def_effect:   # own-offense properties; defence has little causal pull here
                val = lg_side + (self._rate(self.off, off_team, r) - lg)
            out[r] = float(np.clip(val, 0.01, 0.99))
        return out

    def expected_poss(self, home: str, away: str) -> float:
        lg = self.lg_pace[0] / self.lg_pace[1] if self.lg_pace[1] > 0 else 98.0
        return self.team_pace(home) + self.team_pace(away) - lg

    # ---- update AFTER the game has been forecast
    def update(self, g) -> None:
        n_per = int(g["n_periods"])
        ot_norm = 48.0 / (48.0 + 5.0 * max(0, n_per - 4))
        rows = {"home": _offense_row(g, "home", "away", ot_norm),
                "away": _offense_row(g, "away", "home", ot_norm)}
        # decay each participating team's history once per game, then add the new game
        for team in (g["home"], g["away"]):
            for table in (self.off, self.deff):
                cur = table.setdefault(team, self._zero())
                for k in KEYS:
                    cur[k] *= self.lam
            w = self.pace_w.setdefault(team, [0.0, 0.0])
            w[0] *= self.lam
            w[1] *= self.lam
        for side in ("home", "away"):
            for k in KEYS:
                self.lg_side[side][k] *= self.lam_lg
        self.lg_pace[0] *= self.lam_lg
        self.lg_pace[1] *= self.lam_lg
        for side, team, other in (("home", g["home"], g["away"]), ("away", g["away"], g["home"])):
            for k in KEYS:
                self.off[team][k] += rows[side][k]
                self.deff[other][k] += rows[side][k]
                self.lg_side[side][k] += rows[side][k]
        game_poss = 0.5 * (rows["home"]["poss"] + rows["away"]["poss"])
        for team in (g["home"], g["away"]):
            self.pace_w[team][0] += game_poss
            self.pace_w[team][1] += 1.0
        self.lg_pace[0] += game_poss
        self.lg_pace[1] += 1.0

    def record_pace_residual(self, predicted: float, g) -> None:
        n_per = int(g["n_periods"])
        ot_norm = 48.0 / (48.0 + 5.0 * max(0, n_per - 4))
        actual = 0.5 * (_offense_row(g, "home", "away", ot_norm)["poss"] +
                        _offense_row(g, "away", "home", ot_norm)["poss"])
        self.pace_sq[0] += (actual - predicted) ** 2
        self.pace_sq[1] += 1.0


# ----------------------------------------------------------------------------
# Monte Carlo engine
# ----------------------------------------------------------------------------
def _simulate_possessions(rng, n_poss: np.ndarray, r: dict, z: np.ndarray, track: dict | None = None) -> np.ndarray:
    """Points scored by ONE team given per-sim possession counts. Vectorised over sims."""
    N = n_poss.shape[0]
    pts = np.zeros(N, dtype=np.int32)
    logit = lambda p: np.log(p / (1 - p))
    sig = lambda x: 1.0 / (1.0 + np.exp(-x))
    p2 = sig(logit(r["p2"]) + z)
    p3 = sig(logit(r["p3"]) + z)
    max_n = int(n_poss.max())
    for t in range(max_n):
        active = n_poss > t
        u = rng.random(N)
        is_tov = active & (u < r["tov"])
        is_ft = active & ~is_tov & (u < r["tov"] + r["ftrip"])
        is_shot = active & ~is_tov & ~is_ft
        if is_ft.any():
            att = 2 + (rng.random(N) < Q3).astype(np.int32)
            made = rng.binomial(att, r["ft"])
            pts += np.where(is_ft, made, 0).astype(np.int32)
            if track is not None:
                track["fta"] += np.where(is_ft, att, 0); track["ftm"] += np.where(is_ft, made, 0)
            last_missed = rng.random(N) < (1.0 - r["ft"])
            ft_reb = is_ft & last_missed & (rng.random(N) < r["orebft"])
            is_shot = is_shot | ft_reb
            if track is not None:
                track["oreb"] += ft_reb
        live = is_shot
        if track is not None:
            track["tov"] += is_tov
        for _it in range(5):   # shot, then up to 4 offensive-rebound re-tries
            if not live.any():
                break
            is3 = rng.random(N) < r["s3"]
            make = rng.random(N) < np.where(is3, p3, p2)
            if track is not None:
                if _it > 0:
                    track["oreb"] += live
                track["fga"] += live; track["fgm"] += live & make
                track["fg3a"] += live & is3; track["fg3m"] += live & make & is3
            pts += np.where(live & make, np.where(is3, 3, 2), 0).astype(np.int32)
            miss = live & ~make
            live = miss & (rng.random(N) < r["oreb"])
    return pts


def simulate_game(profiles: TeamProfiles, home: str, away: str, n_sims: int, seed: int,
                  sigma_form: float, home_override: dict | None = None,
                  away_override: dict | None = None, track: bool = False,
                  shift_home: float = 0.0, shift_away: float = 0.0) -> dict:
    rng = np.random.default_rng(seed)
    r_h = profiles.matchup(home, away, "home")
    r_a = profiles.matchup(away, home, "away")
    if home_override:
        r_h.update(home_override)
    if away_override:
        r_a.update(away_override)
    mu = profiles.expected_poss(home, away)
    sd = profiles.pace_sd()
    n_poss = np.clip(np.rint(rng.normal(mu, sd, n_sims)), 80, 125).astype(np.int32)
    z_h = rng.normal(0.0, sigma_form, n_sims) + shift_home     # shift = logit change of both 2- and 3-point make probability (availability)
    z_a = rng.normal(0.0, sigma_form, n_sims) + shift_away
    th = {k: np.zeros(n_sims, dtype=np.int32) for k in ("fga", "fgm", "fg3a", "fg3m", "fta", "ftm", "tov", "oreb")} if track else None
    ta = {k: np.zeros(n_sims, dtype=np.int32) for k in th} if track else None
    hp = _simulate_possessions(rng, n_poss, r_h, z_h, th)
    ap = _simulate_possessions(rng, n_poss, r_a, z_a, ta)

    # overtime(s)
    ot = np.zeros(n_sims, dtype=np.int32)
    tied = hp == ap
    guard = 0
    while tied.any() and guard < 8:
        idx = np.where(tied)[0]
        n_ot = np.clip(np.rint(rng.normal(mu * 5.0 / 48.0, 1.5, idx.size)), 6, 18).astype(np.int32)
        hp[idx] += _simulate_possessions(rng, n_ot, r_h, z_h[idx])
        ap[idx] += _simulate_possessions(rng, n_ot, r_a, z_a[idx])
        ot[idx] += 1
        tied = hp == ap
        guard += 1
    still = hp == ap  # vanishingly rare; resolve by coin flip of a single point
    if still.any():
        flip = rng.random(still.sum()) < 0.5
        hp[still] += flip.astype(np.int32)
        ap[still] += (~flip).astype(np.int32)

    out = {"home_pts": hp, "away_pts": ap, "overtimes": ot, "n_poss": n_poss,
           "rates_home": r_h, "rates_away": r_a, "mu_poss": mu, "pace_sd": sd}
    if track:                      # regulation-time box score of the simulated game (before any overtime)
        out["box_home"], out["box_away"] = th, ta
    return out


def apply_dispersion(sim: dict, kappa_margin: float, kappa_total: float, total_shift: float = 0.0,
                     margin_shift: float = 0.0) -> dict:
    """Documented approximation: shrink simulated margin/total deviations about
    their own simulation means by kappa (fit on warm-up games only).

    `total_shift` is an online, leakage-safe correction of the league scoring
    level (the simulator is anchored to past seasons and cannot see a
    season-to-season jump in scoring until it happens).

    Rationale: independent possession outcomes over-disperse game margins
    relative to observed NBA games (late-game management, shot-quality
    heterogeneity and other serial dependence are not modelled). After this
    step final scores are rounded integers but are no longer the exact sum of
    simulated scoring events; the raw event-level arrays are kept in `raw_*`.
    """
    hp, ap = sim["home_pts"].astype(float), sim["away_pts"].astype(float)
    m, t = hp - ap, hp + ap
    mm, mt = m.mean(), t.mean()
    m2 = mm + margin_shift + kappa_margin * (m - mm)   # margin_shift: optional availability adjustment (home minus away, points)
    t2 = mt + total_shift + kappa_total * (t - mt)   # total_shift: online league-level correction
    h2 = np.rint((t2 + m2) / 2.0).astype(np.int32)
    a2 = np.rint((t2 - m2) / 2.0).astype(np.int32)
    tie = h2 == a2
    if tie.any():  # keep the raw winner when rounding creates a tie
        h2[tie & (m + margin_shift > 0)] += 1
        a2[tie & (m + margin_shift <= 0)] += 1
    out = dict(sim)
    out["raw_home_pts"], out["raw_away_pts"] = sim["home_pts"], sim["away_pts"]
    out["home_pts"], out["away_pts"] = h2, a2
    out["dispersion_kappa"] = (kappa_margin, kappa_total)
    return out


def summarize(sim: dict, thresholds: dict | None = None) -> dict:
    """thresholds: {name: (stat, op, value)}, stat in home/away/margin/total."""
    hp, ap = sim["home_pts"], sim["away_pts"]
    margin, total = hp - ap, hp + ap
    n = len(hp)
    p_home = float((margin > 0).mean())
    q = [5, 10, 25, 50, 75, 90, 95]
    pairs, counts = np.unique(np.stack([hp, ap], 1), axis=0, return_counts=True)
    modal = pairs[counts.argmax()]
    out = {
        "n_sims": int(n),
        "p_home": p_home, "p_away": 1 - p_home,
        "mc_se_p_home": float(np.sqrt(p_home * (1 - p_home) / n)),
        "mean_home": float(hp.mean()), "mean_away": float(ap.mean()),
        "median_home": float(np.median(hp)), "median_away": float(np.median(ap)),
        "modal_score_home": int(modal[0]), "modal_score_away": int(modal[1]),
        "modal_score_prob": float(counts.max() / n),
        "mean_margin": float(margin.mean()), "median_margin": float(np.median(margin)),
        "mean_total": float(total.mean()), "median_total": float(np.median(total)),
        "p_ot": float((sim["overtimes"] > 0).mean()),
        "q_margin": {str(k): float(np.percentile(margin, k)) for k in q},
        "q_total": {str(k): float(np.percentile(total, k)) for k in q},
        "mean_poss": float(sim["n_poss"].mean()),
    }
    # basketball-consistency diagnostics
    out["points_per_100_home"] = float(100 * hp.mean() / sim["n_poss"].mean())
    out["points_per_100_away"] = float(100 * ap.mean() / sim["n_poss"].mean())
    if thresholds:
        series = {"home": hp, "away": ap, "margin": margin, "total": total}
        ops = {">": np.greater, ">=": np.greater_equal, "<": np.less, "<=": np.less_equal}
        out["thresholds"] = {name: float(ops[op](series[stat], val).mean())
                             for name, (stat, op, val) in thresholds.items()}
    return out
