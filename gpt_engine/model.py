"""Independent, deterministic team-score baseline for the GPT comparison lane.

Inputs are FINAL historical scores from the existing SQLite archives.
Neither Claude's Elo ratings nor Claude's simulations are used for our predictions.
All parameters are deliberately fixed until a time-split validation justifies changes.
"""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timezone
from math import erf, log, sqrt
from pathlib import Path
import sqlite3

VERSION = "gpt-stat-v1.0"
DB_PATHS = (
    Path("nba_engine/artifacts/nba_engine.sqlite"),
    Path("nba_engine/artifacts/demo_replay.sqlite"),
    Path("nba_engine/artifacts/live.sqlite"),
)


@dataclass(frozen=True)
class Game:
    season: int
    game_id: int
    home: str
    away: str
    home_pts: int
    away_pts: int
    date: str = ""


def load_games(paths=DB_PATHS) -> list[Game]:
    """Read-only union of results, keyed by (season, game_id), preferring dated rows."""
    games: dict[tuple[int, int], Game] = {}
    for path in paths:
        path = Path(path)
        if not path.exists():
            continue
        con = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
        try:
            names = {row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not {"games", "results"} <= names:
                continue
            date_join = ("LEFT JOIN game_dates d ON d.season=g.season AND d.game_id=g.game_id"
                         if "game_dates" in names else "")
            date_col = "COALESCE(d.date, '')" if "game_dates" in names else "''"
            sql = ("SELECT g.season, g.game_id, g.home, g.away, r.home_pts, r.away_pts, "
                   + date_col + " FROM games g JOIN results r "
                   "ON r.season=g.season AND r.game_id=g.game_id " + date_join)
            for row in con.execute(sql):
                game = Game(int(row[0]), int(row[1]), str(row[2]), str(row[3]),
                            int(row[4]), int(row[5]), str(row[6] or ""))
                key = (game.season, game.game_id)
                old = games.get(key)
                if old is not None and (old.home_pts, old.away_pts) != (game.home_pts, game.away_pts):
                    raise ValueError(f"Conflicting final scores for {key}: {old} vs {game}")
                if old is None or (game.date and not old.date):
                    games[key] = game
        finally:
            con.close()
    return sorted(games.values(), key=lambda g: (g.season, g.game_id))


class TeamModel:
    """Mov-adjusted Elo plus shrinkage of recent points scored and allowed.

    This is an intentionally simple, auditable challenger. It is not yet
    calibrated to sportsbook prices and makes no claim of profitable edges.
    """

    def __init__(self):
        self.ratings: dict[str, float] = {}
        self.teams = defaultdict(lambda: deque(maxlen=35))
        self.league = deque(maxlen=450)
        self.season = None

    def _advance(self, season: int):
        if self.season is not None and season != self.season:
            self.ratings = {t: 1500.0 + 0.72 * (r - 1500.0) for t, r in self.ratings.items()}
            self.teams = defaultdict(lambda: deque(maxlen=35))
        self.season = season

    def _rating(self, team: str) -> float:
        return self.ratings.get(team, 1500.0)

    def _recent_rate(self, team: str, slot: int, prior: float) -> float:
        hist = list(self.teams[team])
        weights = [0.5 ** ((len(hist) - i - 1) / 14.0) for i in range(len(hist))]
        weight_sum = sum(weights)
        if not weight_sum:
            return prior
        rate = sum(w * g[slot] for w, g in zip(weights, hist)) / weight_sum
        return (weight_sum * rate + 9.0 * prior) / (weight_sum + 9.0)

    def predict(self, home: str, away: str) -> dict:
        league_pts = (sum(self.league) / len(self.league)) if self.league else 113.5
        h_off = self._recent_rate(home, 0, league_pts)
        a_off = self._recent_rate(away, 0, league_pts)
        h_allowed = self._recent_rate(home, 1, league_pts)
        a_allowed = self._recent_rate(away, 1, league_pts)

        h_box = (h_off + a_allowed) / 2.0 + 0.75
        a_box = (a_off + h_allowed) / 2.0 - 0.75
        elo_diff = self._rating(home) - self._rating(away) + 45.0
        elo_p = 1.0 / (1.0 + 10.0 ** (-elo_diff / 400.0))
        elo_margin = elo_diff / 28.0

        box_margin = h_box - a_box
        margin = 0.80 * elo_margin + 0.20 * box_margin
        total = h_box + a_box
        score_h = (total + margin) / 2.0
        score_a = (total - margin) / 2.0
        box_p = 0.5 * (1.0 + erf(box_margin / (14.0 * sqrt(2.0))))
        p_home = 0.80 * elo_p + 0.20 * box_p
        return {
            "p_home": round(p_home, 5),
            "mean_home": round(score_h, 3),
            "mean_away": round(score_a, 3),
            "mean_margin": round(margin, 3),
            "mean_total": round(total, 3),
            "margin_80": [round(margin - 1.28155 * 14.0, 2), round(margin + 1.28155 * 14.0, 2)],
            "total_80": [round(total - 1.28155 * 19.0, 2), round(total + 1.28155 * 19.0, 2)],
            "elo_p_home": round(elo_p, 5),
            "history_games": len(self.league) // 2,
        }

    def ingest(self, game: Game):
        self._advance(game.season)
        diff = self._rating(game.home) - self._rating(game.away) + 45.0
        p = 1.0 / (1.0 + 10.0 ** (-diff / 400.0))
        winner = 1.0 if game.home_pts > game.away_pts else 0.0
        surprise = winner - p
        mov = abs(game.home_pts - game.away_pts)
        winner_elo_adv = diff if winner else -diff
        multiplier = ((mov + 3.0) ** 0.8) / max(2.0, 7.5 + 0.006 * winner_elo_adv)
        delta = 18.0 * multiplier * surprise
        self.ratings[game.home] = self._rating(game.home) + delta
        self.ratings[game.away] = self._rating(game.away) - delta

        self.teams[game.home].append((game.home_pts, game.away_pts))
        self.teams[game.away].append((game.away_pts, game.home_pts))
        self.league.extend([game.home_pts, game.away_pts])


def history_before(games: list[Game], season: int, game_date: str) -> list[Game]:
    """Un-dated games in the target season are excluded rather than risk leakage."""
    return [g for g in games if g.season < season or
            (g.season == season and bool(g.date) and g.date < game_date)]


def build_model(games: list[Game], season: int, game_date: str) -> TeamModel:
    m = TeamModel()
    for game in history_before(games, season, game_date):
        m.ingest(game)
    m._advance(season)
    return m


def evaluate_saved(predictions: list[dict], games: list[Game]) -> dict:
    """Score only forecasts already saved before their games, never retroactive reruns."""
    lookup = {(g.season, g.game_id): g for g in games}
    rows = []
    for pred in predictions:
        game = lookup.get((int(pred["season"]), int(pred["game_id"])))
        if game is None:
            continue
        tip = pred.get("tip_utc")
        made = pred.get("made_at_utc")
        if not tip or not made:
            continue
        try:
            tip_dt = datetime.fromisoformat(tip.replace("Z", "+00:00")).astimezone(timezone.utc)
            made_dt = datetime.fromisoformat(made.replace("Z", "+00:00")).astimezone(timezone.utc)
        except (TypeError, ValueError):
            continue
        if made_dt >= tip_dt:
            continue
        y = float(game.home_pts > game.away_pts)
        p = max(1e-5, min(1 - 1e-5, float(pred["p_home"])))
        rows.append({
            "brier": (p - y) ** 2,
            "log_loss": -(y * log(p) + (1 - y) * log(1 - p)),
            "winner": float((p >= 0.5) == bool(y)),
            "margin_mae": abs(float(pred["mean_margin"]) - (game.home_pts - game.away_pts)),
            "total_mae": abs(float(pred["mean_total"]) - (game.home_pts + game.away_pts)),
        })
    if not rows:
        return {"n": 0}
    return {"n": len(rows), **{k: round(sum(r[k] for r in rows) / len(rows), 4) for k in rows[0]}}
