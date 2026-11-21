"""Frozen slate-based master Markdown: one day, no made-up prices or props."""
from pathlib import Path
import sqlite3
import json

import pytest

from gpt_engine.v2.daily_master_report import (
    render_master_report,generate,DVP_REF
)

NOW="2026-11-21T16:10:00Z"
DATE="2026-11-21"
TIP="2026-11-22T01:00:00Z"
GID1="game:nba:0022600997"
GID2="game:nba:0022600998"


def daily(date=DATE):
    return (
        f"# GPT v2 NBA daily simulation report — {date} (US Eastern)\n"
        "\n**Status:** RESEARCH / UNCALIBRATED — simulation only\n"
        "\n## Slate at a glance\n\n| Game | Projected score |\n"
        "|---|---:|\n| A @ B | 100–101 |\n"
        "\n## Game-by-game breakdown\n\n### A @ B\n\n"
        "**Situational:** historical rest context\n"
    )


def quote(gid, p):
    return {
        "game_id":gid, "market_id":"game:moneyline",
        "market_type":"moneyline", "book":"Fixture Book",
        "selection":"home", "line":None,
        "tip_utc":TIP,
        "retrieved_at_utc":"2026-11-21T16:05:00Z",
        "observed_at_utc":"2026-11-21T16:05:00Z",
        "forecast_cutoff_utc":"2026-11-21T16:08:00Z",
        "snapshot_gap_minutes":3.0,
        "no_vig_market_probability":0.52,
        "decimal_odds":1.6,
        "model_probability":p,
        "push_probability":0.0,
        "decision":"RESEARCH_ONLY",
        "calibration_status":"uncalibrated",
        "source_raw_provider_payload":"NEVER EXPOSE SECRET MARKET PAYLOAD",
    }


def data():
    markets={"research_only":True, "markets":[quote(GID1,.72),
           quote(GID2,.70)]}
    parlay={"research_only":True,"generated_at_utc":NOW,
            "ranking_metric":"full_win_probability_independent"}
    alt={"research_only":True,
         "candidates":[
            {
              "date_eastern":DATE,
              "game_id":GID1,
              "player":"Test Athlete",
              "position_group":"G",
              "stat":"pts",
              "alt_over_line":19.5,
              "season_hits":14,"season_games":15,
              "raw_season_hit_rate":14/15,
              "last_five_hits":5,
              "estimated_usage_percent":34.5,
              "team_usage_rank":1,
              "availability":"UNCONFIRMED",
              "opponent_defense":{"rank_most_allowed":2}
            },
            {
              "date_eastern":"2026-11-22",
              "game_id":"another-day",
              "player":"Tomorrow Athlete",
              "position_group":"F",
              "stat":"reb","alt_over_line":6.5,
              "season_hits":12,"season_games":12,
              "raw_season_hit_rate":1.0,"last_five_hits":5,
              "estimated_usage_percent":29,
              "team_usage_rank":1,
              "availability":"probable",
              "opponent_defense":{"rank_most_allowed":1}
            }
         ],
         "priced_alternate_legs":[],
         "same_book_parlay":None,
         "missing_requirements":[
            "NO_SOURCE_VERIFIED_ALT_PLAYER_PROP_ODDS_AND_MODEL_PRICE_MATCH"
         ],
         "defense_coverage":[
            {"asof_date_eastern":DATE,
             "position_coverage":{
              "G":{"valid_defensive_teams":30,"required_teams":30,"rankable":True},
              "F":{"valid_defensive_teams":30,"required_teams":30,"rankable":True},
              "C":{"valid_defensive_teams":29,"required_teams":30,"rankable":False}
             }}
         ],
         "prior_final_freshness":[
            {"date_eastern":DATE,"missing_due_final_games":9,
             "candidate_teams_with_unsettled_past_game":{
                "team:nba:123":1
             }}
         ]}
    graded={"research_only":True,"graded_markets":[]}
    lookups={
        GID1:{"matchup":"Memphis Grizzlies @ Minnesota Timberwolves","tip_utc":TIP},
        GID2:{"matchup":"Boston Celtics @ Sacramento Kings","tip_utc":TIP},
    }
    return markets,parlay,alt,graded,lookups


def test_master_has_full_sections_and_correct_date_scoped_parlay():
    markets,parlay,alt,grade,names=data()
    result=render_master_report(
        DATE,daily(),markets,parlay,alt,grade,names,
        generated_at_utc=NOW
    )
    assert "# NBA Engine V2 — Unified Daily Research — 2026-11-21" in result
    assert "High-hit single-game" in result
    assert "Highest modeled chance — same-book game parlay" in result
    assert "50.4%" in result # 72% * 70% joint assumed independent
    assert "Memphis Grizzlies @ Minnesota Timberwolves" in result
    assert "Test Athlete" in result
    assert "14/15 (93.3%)" in result
    assert "Tomorrow Athlete" not in result
    assert "C:** 29/30" in result
    assert "NO SOURCE-VERIFIED ALTERNATE-PROP PARLAY" in result
    assert DVP_REF in result
    assert "NOT sourced or imported" in result
    assert "Missing past-game finals: **9**" in result
    assert "## Detailed game-by-game forecasts" in result
    assert "### Slate at a glance" in result
    assert "### Game-by-game breakdown" in result
    assert "RESEARCH / UNCALIBRATED" in result
    assert "NEVER EXPOSE SECRET MARKET PAYLOAD" not in result
    assert "1.6" not in result  # no bookmaker decimal price leaks
    assert "decimal_odds" not in result


def test_reject_wrong_day_original_report_and_missing_research_contract():
    market,parlay,alt,grades,names=data()
    with pytest.raises(ValueError,match="wrong date"):
        render_master_report(
            DATE,daily("2026-11-22"),market,parlay,alt,grades,names,
            generated_at_utc=NOW
        )
    market["research_only"]=False
    with pytest.raises(ValueError,match="research-only"):
        render_master_report(
            DATE,daily(),market,parlay,alt,grades,names,
            generated_at_utc=NOW
        )


def test_no_original_saved_forecast_cannot_generate_master(tmp_path):
    market,parlay,alt,grades,names=data()
    db=tmp_path/"db.sqlite"
    with sqlite3.connect(db) as con:
        con.executescript(
            "CREATE TABLE games(game_id TEXT,game_date_eastern TEXT,"
            "game_type TEXT,away_team_id TEXT,home_team_id TEXT,tip_utc TEXT);"
            "CREATE TABLE teams(team_id TEXT,current_name TEXT);"
        )
    def write(path,value):
        path.write_text(json.dumps(value))
        return path
    with pytest.raises(FileNotFoundError,match="Daily original"):
        generate(db,tmp_path,
                 write(tmp_path/"market.json",market),
                 write(tmp_path/"parlay.json",parlay),
                 write(tmp_path/"alt.json",alt),
                 write(tmp_path/"grade.json",grades),
                 date_eastern=DATE,now_utc=NOW)


def test_writes_repo_ready_archive_file_to_same_reports_folder(tmp_path):
    market,parlay,alt,grades,names=data()
    db=tmp_path/"db.sqlite"
    with sqlite3.connect(db) as con:
        con.executescript(
            "CREATE TABLE games(game_id TEXT,game_date_eastern TEXT,"
            "game_type TEXT,away_team_id TEXT,home_team_id TEXT,tip_utc TEXT);"
            "CREATE TABLE teams(team_id TEXT PRIMARY KEY,current_name TEXT);"
        )
        con.executemany("INSERT INTO teams VALUES (?,?)",[
            ("team_a","Boston Celtics"),("team_b","Sacramento Kings")
        ])
        con.execute("INSERT INTO games VALUES (?,?,?,?,?,?)",
            (GID2,DATE,"regular_season","team_a","team_b",TIP))
    (tmp_path/f"daily_{DATE}.md").write_text(daily())
    def write(path,value):
        path.write_text(json.dumps(value))
        return path
    result=generate(db,tmp_path,
                    write(tmp_path/"market.json",market),
                    write(tmp_path/"parlay.json",parlay),
                    write(tmp_path/"alt.json",alt),
                    write(tmp_path/"grade.json",grades),
                    date_eastern=DATE,now_utc=NOW)
    assert result==[tmp_path/f"research_{DATE}.md"]
    master=result[0].read_text()
    assert "Boston Celtics @ Sacramento Kings" in master
    assert "Memphis Grizzlies" not in master
    assert "NO QUALIFYING GAME PARLAY" in master
    assert "Hashtag Basketball" in master
