"""Observable team-style features. NOT coach identities or tactical play calls."""
from __future__ import annotations
import pandas as pd

STYLE_STATS = (
    "pace", "poss", "off_rating", "def_rating", "net_rating", "efg_pct", "ts_pct",
    "three_point_rate", "fta_rate", "ast", "ast_pct", "ast_ratio", "tov",
    "tm_tov_pct", "oreb", "oreb_pct", "dreb_pct", "opp_efg_pct",
    "opp_fg3a", "opp_fg3m", "opp_ast", "opp_oreb", "opp_pts",
)


def build_style_snapshots(team_games: pd.DataFrame, min_games: int = 5) -> pd.DataFrame:
    """Prior 20 games only. Daily sort avoids using this game's outcome."""
    g = team_games[team_games.game_type == "regular_season"].copy()
    g = g.sort_values(["season", "team_id", "game_date", "game_id"]).reset_index(drop=True)
    fields = [f for f in STYLE_STATS if f in g.columns]
    result = g[["season", "game_id", "game_date", "team", "team_id", "opp",
                "opp_team_id", "game_type"]].copy()
    for col in fields:
        numerics = pd.to_numeric(g[col], errors="coerce")
        # Shift by one game, so today's feature is computed only from earlier box scores.
        result["prior20_" + col] = numerics.groupby([g["season"], g["team_id"]]).transform(
            lambda x: x.shift(1).rolling(window=20, min_periods=min_games).mean()
        )
    result["prior_games"] = g.groupby(["season", "team_id"]).cumcount()
    result["style_sample_ok"] = result["prior_games"] >= min_games
    result["coach_name"] = pd.NA
    result["coach_source"] = "not_collected"
    result["style_type"] = "statistical_tendencies_not_verified_tactics"
    return result
