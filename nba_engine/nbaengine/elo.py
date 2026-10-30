"""Margin-of-victory Elo baseline (FiveThirtyEight-style).

State is updated strictly AFTER each game's forecast has been produced, so a
single chronological pass is leakage-free by construction.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math

ELO_PER_POINT = 28.0  # ~538: one point of margin ~ 28 Elo


@dataclass
class EloParams:
    k: float = 20.0
    home_adv: float = 100.0         # Elo points
    carryover: float = 0.75         # share of rating kept across seasons
    init: float = 1505.0
    mov_scale: float = 1.0          # 0 disables the margin-of-victory multiplier


@dataclass
class Elo:
    params: EloParams = field(default_factory=EloParams)
    ratings: dict = field(default_factory=dict)
    season: int | None = None

    def rating(self, team: str) -> float:
        return self.ratings.get(team, self.params.init)

    def new_season(self, season: int) -> None:
        if self.season is not None and season != self.season:
            p = self.params
            for t in list(self.ratings):
                self.ratings[t] = p.carryover * self.ratings[t] + (1 - p.carryover) * p.init
        self.season = season

    def predict(self, home: str, away: str) -> dict:
        d = self.rating(home) + self.params.home_adv - self.rating(away)
        p_home = 1.0 / (1.0 + 10.0 ** (-d / 400.0))
        return {"p_home": p_home, "exp_margin": d / ELO_PER_POINT, "elo_diff": d}

    def update(self, home: str, away: str, home_pts: float, away_pts: float) -> None:
        p = self.params
        pred = self.predict(home, away)
        home_win = 1.0 if home_pts > away_pts else 0.0
        margin = abs(home_pts - away_pts)
        d_win = pred["elo_diff"] if home_win else -pred["elo_diff"]
        mult = 1.0
        if p.mov_scale > 0:
            mult = ((margin + 3.0) ** 0.8) / (7.5 + 0.006 * d_win)
            mult = 1.0 + p.mov_scale * (mult - 1.0)
        shift = p.k * mult * (home_win - pred["p_home"])
        self.ratings[home] = self.rating(home) + shift
        self.ratings[away] = self.rating(away) - shift


def log_loss(p: float, y: float, eps: float = 1e-9) -> float:
    p = min(max(p, eps), 1 - eps)
    return -(y * math.log(p) + (1 - y) * math.log(1 - p))


def tune_elo(games, grid: list[EloParams], burn_in_seasons: int = 3) -> list[tuple[EloParams, float]]:
    """Grid-search Elo parameters by walk-forward log loss on `games`.

    `games` must have columns season, home, away, home_pts, away_pts in
    chronological order. The first `burn_in_seasons` seasons are used for
    warm-up only (not scored).
    """
    seasons = sorted(games["season"].unique())
    scored_from = seasons[burn_in_seasons] if len(seasons) > burn_in_seasons else seasons[0]
    rows = games[["season", "home", "away", "home_pts", "away_pts"]].itertuples(index=False)
    rows = list(rows)
    results = []
    for prm in grid:
        e = Elo(prm)
        tot, n = 0.0, 0
        for s, h, a, hp, ap in rows:
            e.new_season(s)
            pr = e.predict(h, a)["p_home"]
            if s >= scored_from:
                tot += log_loss(pr, 1.0 if hp > ap else 0.0)
                n += 1
            e.update(h, a, hp, ap)
        results.append((prm, tot / n))
    return sorted(results, key=lambda r: r[1])
