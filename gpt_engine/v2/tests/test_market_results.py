"""Warehouse score-integrity regression tests for market outcome extraction."""
import json
import sqlite3

from gpt_engine.v2.market_results import (
    extract_final_outcomes, _minutes_value
)


def db():
    con = sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE games(game_id TEXT PRIMARY KEY,game_date_eastern TEXT,
     tip_utc TEXT, status TEXT,game_type TEXT,home_team_id TEXT,
     away_team_id TEXT);
    CREATE TABLE actual_results(game_id TEXT,home_score INTEGER,away_score INTEGER,
      source_id TEXT,retrieved_at_utc TEXT);
    CREATE TABLE team_game_stats(game_id TEXT,team_id TEXT,stats_json TEXT);
    CREATE TABLE player_game_stats(game_id TEXT,player_id TEXT,stats_json TEXT);
    INSERT INTO games VALUES('game:nba:123','2026-11-21',
      '2026-11-22T01:00:00Z','final','regular_season','home','away');
    INSERT INTO actual_results VALUES('game:nba:123',110,100,
      'nba_stats_archive','2026-11-22T04:30:00Z');
    """)
    # Deliberately insert team rows in reverse order to catch positional joins.
    con.execute("INSERT INTO team_game_stats VALUES(?,?,?)",
                ("game:nba:123","away",json.dumps({
                   "pts":100,"fgm":40,"fg3m":10,"ftm":10
                })))
    con.execute("INSERT INTO team_game_stats VALUES(?,?,?)",
                ("game:nba:123","home",json.dumps({
                   "pts":110,"fgm":45,"fg3m":10,"ftm":10
                })))
    con.execute("INSERT INTO player_game_stats VALUES(?,?,?)",
                ("game:nba:123","player:nba:1",
                 json.dumps({"min":"35:30","pts":25,"reb":6,"ast":5,"fg3m":3})))
    con.execute("INSERT INTO player_game_stats VALUES(?,?,?)",
                ("game:nba:123","player:nba:2",
                 json.dumps({"min":0,"pts":0,"reb":0,"ast":0,"fg3m":0})))
    return con


def test_valid_final_extraction_and_player_identity():
    result = extract_final_outcomes(db())
    assert len(result["games"]) == 1
    assert not result["excluded"]
    g = result["games"][0]
    assert g["home_score"] == 110
    assert g["away_score"] == 100
    assert g["final_at_utc"] == g["retrieved_at_utc"]
    assert g["players"]["player:nba:1"]["status"] == "played"
    assert g["players"]["player:nba:1"]["pts"] == 25
    assert g["players"]["player:nba:2"]["status"] == "unknown"
    assert _minutes_value({"min":"35:30"}) == 35.5


def test_score_components_not_reconciled_means_no_grading():
    con = db()
    con.execute("UPDATE actual_results SET home_score=111")
    result = extract_final_outcomes(con)
    assert result["games"] == []
    assert result["excluded"][0]["reason"] == "INVALID_TEAM_SCORE_COMPONENTS"


def test_false_final_timestamp_is_rejected():
    con = db()
    con.execute(
        "UPDATE actual_results SET retrieved_at_utc='2026-11-21T23:00:00Z'"
    )
    result = extract_final_outcomes(con)
    assert result["games"] == []
    assert result["excluded"][0]["reason"] == "FINAL_NOT_OBSERVED_AFTER_TIP"


def test_scoped_date_range_excludes_other_games():
    assert extract_final_outcomes(
        db(), date_from="2026-11-22"
    )["games"] == []
