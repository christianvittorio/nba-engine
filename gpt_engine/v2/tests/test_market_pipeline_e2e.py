"""Full offline value-engine smoke: source -> NBA identity -> frozen model
-> immutable prices -> final score -> CLV. All dates/prices are synthetic.
"""
import json
import sqlite3
from pathlib import Path

import pytest

from gpt_engine.v2.odds_map import map_provider_events
from gpt_engine.v2.odds_ingest import normalize_provider_events, append_odds_ledger
from gpt_engine.v2.market_run import asof_market_report, read_jsonl
from gpt_engine.v2.market_results import extract_final_outcomes
from gpt_engine.v2.market_grade import evaluate_outcomes

GID="game:nba:0022600988"
TIP="2026-11-22T01:00:00Z"


def warehouse():
    con=sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE teams(team_id TEXT PRIMARY KEY,current_name TEXT);
    CREATE TABLE games(game_id TEXT PRIMARY KEY,game_date_eastern TEXT,
      tip_utc TEXT,status TEXT,game_type TEXT,home_team_id TEXT,away_team_id TEXT);
    CREATE TABLE actual_results(game_id TEXT,home_score INTEGER,
      away_score INTEGER,source_id TEXT,retrieved_at_utc TEXT);
    CREATE TABLE team_game_stats(game_id TEXT,team_id TEXT,stats_json TEXT);
    CREATE TABLE player_game_stats(game_id TEXT,player_id TEXT,stats_json TEXT);
    INSERT INTO teams VALUES('nba-home','BOS'),('nba-away','NYK');
    INSERT INTO games VALUES('game:nba:0022600988','2026-11-21',
      '2026-11-22T01:00:00Z','final','regular_season',
      'nba-home','nba-away');
    INSERT INTO actual_results VALUES('game:nba:0022600988',110,100,
      'fixture-final-source','2026-11-22T04:10:00Z');
    """)
    con.execute("INSERT INTO team_game_stats VALUES(?,?,?)",
                (GID,"nba-home",json.dumps({
                    "pts":110,"fgm":45,"fg3m":10,"ftm":10
                })))
    con.execute("INSERT INTO team_game_stats VALUES(?,?,?)",
                (GID,"nba-away",json.dumps({
                    "pts":100,"fgm":40,"fg3m":10,"ftm":10
                })))
    return con


def event(price_home=2.,price_away=1.8,updated="2026-11-21T20:00:00Z"):
    return [{
        "id":"provider-synthetic-game",
        "home_team":"Boston Celtics","away_team":"New York Knicks",
        "commence_time":TIP,"sport_key":"basketball_nba",
        "bookmakers":[{"key":"book_fixture","last_update":updated,
        "markets":[{"key":"h2h","last_update":updated,
        "outcomes":[{"name":"Boston Celtics","price":price_home},
                    {"name":"New York Knicks","price":price_away}]
        }]}]
    }]


def forecast():
    return {
        "game_id":GID,"prediction_id":"prediction:immutable",
        "model_version":"research-uncalibrated",
        "tip_utc":TIP,"cutoff_utc":"2026-11-21T20:10:00Z",
        "home_team_id":"nba-home","away_team_id":"nba-away",
        "result":{"home_win_probability":.58,
                  "expected_home_score":111.,"expected_away_score":106.,
                  "margin":{"mean":5.},"total":{"mean":217.},
                  "player_statistics":{}}
    }


def test_full_offline_pipeline_keeps_asof_vs_close_separate(tmp_path):
    db=warehouse()
    mapping=map_provider_events(event(),db)
    assert len(mapping["events"]) == 1
    first=normalize_provider_events(event(),mapping,
          retrieved_at_utc="2026-11-21T20:05:00Z")
    path=tmp_path/"quotes.jsonl"
    assert append_odds_ledger(path,first["quotes"])["new_quotes"] == 2
    asof=asof_market_report([forecast()],read_jsonl(path))
    assert asof["usable_asof_quote_count"] == 2
    home=next(r for r in asof["markets"] if r["selection"]=="home")
    assert home["expected_roi"] == pytest.approx(.16)
    assert home["decision"] == "RESEARCH_ONLY"
    assert home["no_vig_market_probability"] == pytest.approx(
        (1/2)/(1/2 + 1/1.8)
    )

    late=normalize_provider_events(
        event(price_home=1.8,price_away=2.1,
              updated="2026-11-22T00:40:00Z"),
        mapping,retrieved_at_utc="2026-11-22T00:45:00Z")
    assert append_odds_ledger(path,late["quotes"])["new_quotes"] == 2
    repeated=asof_market_report([forecast()],read_jsonl(path))
    assert repeated["usable_asof_quote_count"] == 2
    assert repeated["excluded"]
    assert all(r["decimal_odds"] in (2.0,1.8) for r in repeated["markets"])

    finals=extract_final_outcomes(db)
    assert len(finals["games"]) == 1
    graded=evaluate_outcomes(repeated,read_jsonl(path),finals)
    home_grade=next(r for r in graded["graded_markets"]
                    if r["selection"]=="home")
    assert home_grade["settlement"] == "WIN"
    assert home_grade["unit_return"] == pytest.approx(1)
    assert home_grade["closing_decimal_odds"] == pytest.approx(1.8)
    assert home_grade["closing_line_value"] == pytest.approx(2.0/1.8-1)
    quality=graded["calibration"]
    assert quality["model_brier"] == pytest.approx((.58-1)**2)
    assert quality["matched_consensus_games"] == 1
    assert quality["matched_game_market_brier"] is not None
    assert not quality["sample_large_enough_for_public_accuracy_claim"]
