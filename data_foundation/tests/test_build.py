"""Local validation tests: no network or NBA credentials."""
import pandas as pd
import pytest

from data_foundation.matchups import matchup_layers
from data_foundation.build import (
    classify_game, defense_vs_position, normalize_players, normalize_teams,
    season_url
)


def _sample():
    team_meta = pd.DataFrame({
        "team_id": ["1", "2"], "nba_abbrev": ["BOS", "NYK"]
    })
    team_raw = pd.DataFrame([
        {"season": 2020, "game_id": "0021900001", "team_id": "1",
         "opp_team_id": "2", "game_date": "2019-10-22", "home": True,
         "pts": 110, "fga": 80, "fgm": 40, "fg3a": 20, "fg3m": 10,
         "fta": 20, "ftm": 20, "oreb": 10, "dreb": 30,
         "reb": 40, "ast": 25, "tov": 12, "stl": 5, "blk": 4},
        {"season": 2020, "game_id": "0021900001", "team_id": "2",
         "opp_team_id": "1", "game_date": "2019-10-22", "home": False,
         "pts": 100, "fga": 78, "fgm": 35, "fg3a": 22, "fg3m": 10,
         "fta": 20, "ftm": 20, "oreb": 8, "dreb": 33,
         "reb": 41, "ast": 20, "tov": 13, "stl": 6, "blk": 3},
    ])
    teams = normalize_teams(team_raw, team_meta, 2020)
    player_raw = pd.DataFrame([
        {"game_id": "0021900001", "player_id": "100", "team_id": "1",
         "opp_team_id": "2", "pts": 20, "ast": 5, "reb": 6,
         "fg3m": 2, "min": 35},
        {"game_id": "0021900001", "player_id": "101", "team_id": "2",
         "opp_team_id": "1", "pts": 16, "ast": 8, "reb": 4,
         "fg3m": 1, "min": 30},
    ])
    player_meta = pd.DataFrame({"player_id": ["100", "101"],
                                "position": ["SF", "G-F"]})
    players = normalize_players(player_raw, player_meta, teams, 2020)
    return teams, players


def test_known_season_game_types():
    assert classify_game("0021900001") == "regular_season"
    assert classify_game("0041900401") == "playoffs"
    assert classify_game("0051900001") == "play_in"
    assert classify_game("0011900001") == "other"


def test_source_url_validated():
    assert "season=2020" in season_url("team_game_logs", 2020)
    with pytest.raises(ValueError):
        season_url("../private", 2020)


def test_advanced_and_opponent_stats_are_paired():
    teams, _ = _sample()
    bos = teams[teams.team == "BOS"].iloc[0]
    assert bos.opp_pts == 100
    assert bos.opp_ast == 20
    assert bos.opp_fg3a == 22
    assert bos.three_point_rate == .25
    assert round(bos.efg_recalc, 3) == .562


def test_positions_not_inferred_from_hybrids():
    teams, players = _sample()
    assert players.loc[players.player_id == "100", "position"].iloc[0] == "SF"
    assert players.loc[players.player_id == "101", "position"].iloc[0] == "G-F"
    assert players.loc[players.player_id == "101", "position_quality"].iloc[0] == "broad_or_hybrid"
    games, summary = defense_vs_position(players, 2020)
    assert len(games) == 2
    bos_def = summary[(summary.defense_team == "BOS") &
                      (summary.position == "G-F")].iloc[0]
    assert bos_def.ast_allowed_per_game == 8
    assert bos_def.ast_allowed_per_48_position_minutes == 12.8


def test_team_rejects_incomplete_opponent_pair():
    teams, _ = _sample()
    raw = teams[["season", "game_id", "team_id", "opp_team_id",
                 "game_date", "home", "pts", "fga", "fgm", "fg3a", "fg3m",
                 "fta", "ftm", "oreb", "dreb", "ast", "tov"]].iloc[:1]
    with pytest.raises(ValueError, match="two team rows"):
        normalize_teams(raw, pd.DataFrame(
            {"team_id": ["1", "2"], "nba_abbrev": ["BOS", "NYK"]}), 2020)

def test_tracked_player_defender_assists_and_possessions():
    teams, players = _sample()
    raw = pd.DataFrame([{
        "game_id": "0021900001", "off_team_id": "1", "def_team_id": "2",
        "off_person_id": "100", "def_person_id": "101",
        "off_position": "F", "partial_possessions": 11.5,
        "matchup_assists": 2, "matchup_potential_assists": 4,
        "player_points": 8, "matchup_field_goals_attempted": 5
    }])
    tracked, game, season, audit = matchup_layers(raw, teams, 2020)
    assert audit["matchup_rows"] == 1
    assert audit["tracked_games"] == 1
    assert game.iloc[0].defense_team == "NYK"
    assert game.iloc[0].matchup_assists == 2
    assert season.iloc[0].matchup_assists_per_game == 2
    assert abs(season.iloc[0].matchup_assists_per_100_matchup_possessions - 200 / 11.5) < 0.01

