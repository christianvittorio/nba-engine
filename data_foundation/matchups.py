"""Season-by-season player-versus-defender matchup observations.

Source: SportsDataverse nba_stats_game_matchups (NBA tracking matchup feed).
This is a *tracked matchup attribution*, not evidence of exclusive one-on-one
coverage on every possession or a coach's play-call preference.
"""
from __future__ import annotations

from pathlib import Path
import tempfile
import urllib.request

import pandas as pd

BASE = ("https://github.com/sportsdataverse/sportsdataverse-data/releases/"
        "download/nba_stats_game_matchups/game_matchups_{season}.parquet")
NEEDED = ("game_id", "off_team_id", "def_team_id", "off_person_id",
          "def_person_id", "off_position", "partial_possessions",
          "matchup_assists", "matchup_potential_assists")
COUNT_FIELDS = ("partial_possessions", "player_points", "team_points",
                "matchup_assists", "matchup_potential_assists",
                "matchup_turnovers", "matchup_blocks",
                "matchup_field_goals_made", "matchup_field_goals_attempted",
                "matchup_three_pointers_made", "matchup_three_pointers_attempted",
                "matchup_free_throws_made", "matchup_free_throws_attempted",
                "shooting_fouls", "switches_on")


def download_matchups(con, season: int) -> pd.DataFrame:
    url = BASE.format(season=season)
    try:
        with urllib.request.urlopen(url, timeout=90) as response:
            raw = response.read()
    except Exception as exc:
        raise RuntimeError(f"Failed to download {url}: {exc}") from exc
    if not raw.startswith(b"PAR1"):
        raise ValueError(f"Matchup download is not a parquet file: {url}")
    with tempfile.NamedTemporaryFile(suffix=".parquet") as f:
        f.write(raw)
        f.flush()
        frame = con.execute("SELECT * FROM read_parquet(?)", [f.name]).df()
    if frame.empty:
        raise ValueError(f"Empty matchup table: {url}")
    frame.columns = [str(c).strip().lower() for c in frame.columns]
    missing = set(NEEDED) - set(frame.columns)
    if missing:
        raise ValueError(f"Matchup table missing {sorted(missing)}")
    return frame


def matchup_layers(raw: pd.DataFrame, teams: pd.DataFrame,
                   season: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Return observed tracked matchups, per-game defense allowed, season aggregate."""
    data = raw.copy()
    for col in ("game_id", "off_team_id", "def_team_id", "off_person_id", "def_person_id"):
        data[col] = data[col].astype(str).str.replace(r"\.0$", "", regex=True)
    data["game_id"] = data.game_id.str.zfill(10)
    data["season"] = season
    data["game_type"] = data.game_id.map(
        lambda x: {"002": "regular_season", "004": "playoffs",
                   "005": "play_in", "006": "cup_final"}.get(x[:3], "other"))
    allowed = set(teams.game_id.astype(str))
    data = data[data.game_id.isin(allowed) &
                data.game_type.isin(("regular_season", "playoffs",
                                   "play_in", "cup_final"))].copy()
    if data.empty:
        raise ValueError(f"Season {season} has no joinable matchup data")
    data["off_position"] = data.off_position.fillna("UNKNOWN").astype(str).str.upper()
    # Positions are the tracking source's official labels (usually G/F/C), not SF/SG guesses.
    for col in COUNT_FIELDS:
        if col in data:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    # Convert primary matchup statistics into a team defensive observation.
    names = teams[["game_id", "team_id", "team", "game_date"]].copy()
    names = names.rename(columns={"team_id": "def_team_id",
                                  "team": "defense_team"})
    data = data.merge(names, on=["game_id", "def_team_id"], how="left",
                      validate="many_to_one")
    if data.defense_team.isna().any():
        raise ValueError("Tracked defender team does not match historical NBA team game log")
    measures = [x for x in COUNT_FIELDS if x in data.columns]
    by_game = data.groupby(["season", "game_id", "game_date", "game_type",
                            "def_team_id", "defense_team", "off_position"],
                           as_index=False, dropna=False)[measures].sum(min_count=1)
    by_game["matchup_pair_rows"] = data.groupby(
        ["season", "game_id", "game_date", "game_type",
         "def_team_id", "defense_team", "off_position"],
        dropna=False).size().values

    dims = ["season", "game_type", "def_team_id", "defense_team", "off_position"]
    by_season = by_game.groupby(dims, as_index=False, dropna=False)[measures].sum(min_count=1)
    rows = by_game.groupby(dims, dropna=False).game_id.nunique().reset_index(name="sample_games")
    by_season = by_season.merge(rows, on=dims, validate="one_to_one")
    for col in ("matchup_assists", "matchup_potential_assists", "player_points",
                "matchup_field_goals_attempted"):
        if col in by_season:
            by_season[col + "_per_game"] = by_season[col] / by_season.sample_games
            by_season[col + "_per_100_matchup_possessions"] = (
                100 * by_season[col] /
                by_season.partial_possessions.replace(0, float("nan"))
            )
    return data, by_game, by_season, {
        "source": BASE.format(season=season),
        "matchup_rows": len(data),
        "tracked_games": int(data.game_id.nunique()),
        "regular_season_tracked_games": int(
            data.loc[data.game_type == "regular_season", "game_id"].nunique()),
        "position_labels": {str(k): int(v) for k, v in
                            data.off_position.value_counts(dropna=False).items()},
        "matchup_attribution_is_exclusive_defender_truth": False,
    }
