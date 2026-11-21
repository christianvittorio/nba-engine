"""Offline tests for the five selected bookmakers (no API key or wagering)."""
import json
import sqlite3

import pytest

from gpt_engine.v2.odds_api_io import (
    BOOKS, normalize_five_book_events, _flatten_one_market,
    fetch_five_book_snapshots
)
from gpt_engine.v2.odds_ingest import append_odds_ledger
from gpt_engine.v2.market_run import asof_market_report

GID="game:nba:0022600300"
TIP="2026-11-22T01:00:00Z"
STAMP="2026-11-21T20:00:00Z"


def db():
    c=sqlite3.connect(":memory:")
    c.executescript("""
    CREATE TABLE teams(team_id TEXT PRIMARY KEY,current_name TEXT);
    CREATE TABLE games(game_id TEXT PRIMARY KEY,tip_utc TEXT,
      home_team_id TEXT,away_team_id TEXT,game_type TEXT);
    INSERT INTO teams VALUES('nba:home','BOS'),('nba:away','NYK');
    INSERT INTO games VALUES('game:nba:0022600300',
      '2026-11-22T01:00:00Z','nba:home','nba:away','regular_season');
    """)
    return c


def event():
    return {
        "id":12345,"league":{"name":"NBA","slug":"nba"},
        "home":"Boston Celtics","away":"New York Knicks","date":TIP,
        "status":"pending"
    }


def books_response():
    return {
        "id":12345,"home":"Boston Celtics","away":"New York Knicks",
        "date":TIP,"status":"pending",
        "bookmakers":{
            book:[
                {"name":"ML","odds":[{"home":"2.10","away":"1.80"}],
                 "updatedAt":"2026-11-21T19:58:00Z"},
                {"name":"Spread","odds":[{"hdp":-5.5,"home":"1.91","away":"1.91"}],
                 "updatedAt":"2026-11-21T19:58:00Z"},
                {"name":"Totals","odds":[{"max":230.5,"over":"1.95","under":"1.87"}],
                 "updatedAt":"2026-11-21T19:58:00Z"},
            ] for book in BOOKS
        }
    }


def test_five_bookmaker_normalization_all_three_markets():
    assert BOOKS==("FanDuel","Stake","MelBet","1xbet","Bet365")
    report=normalize_five_book_events(
        [event()],[books_response()],db(),retrieved_at_utc=STAMP)
    assert report["mapped_nba_events"]==1
    assert report["missing_bookmakers"]==[]
    assert len(report["quotes"])==30
    assert set(q["book"] for q in report["quotes"])==set(BOOKS)
    assert all(q["provider"]=="odds-api-io" for q in report["quotes"])
    assert all(q["retrieved_at_utc"]==STAMP for q in report["quotes"])
    for book in BOOKS:
        assert report["quote_counts_by_bookmaker"][book]==6
        pairs=[q for q in report["quotes"]
               if q["book"]==book and q["market_type"]=="spread"]
        assert len(pairs)==2
        assert {q["line"] for q in pairs}=={-5.5,5.5}
        assert len(set(q["market_id"] for q in pairs))==1


def test_market_asof_report_compares_all_five_without_inventing_odds():
    response=normalize_five_book_events(
        [event()],[books_response()],db(),retrieved_at_utc=STAMP)
    forecast={
        "game_id":GID,"prediction_id":"prediction:fixed","tip_utc":TIP,
        "cutoff_utc":"2026-11-21T20:05:00Z",
        "home_team_id":"nba:home","away_team_id":"nba:away",
        "model_version":"experimental",
        "result":{
            "home_win_probability":0.58,
            "expected_home_score":120,"expected_away_score":115,
            "margin":{"mean":5},"total":{"mean":235},
            "simulation_count":100,
            "player_statistics":{},
            "market_distributions":{
                "sample_count":100,"calibration_status":"uncalibrated",
                "settlement_scope":"full_game_including_overtime",
                "home_margin_counts":{"5":100},
                "game_total_counts":{"235":100},
                "player_counts":{}
            }
        }
    }
    out=asof_market_report([forecast],response["quotes"])
    assert out["usable_asof_quote_count"]==30
    assert len(out["markets"])==30
    assert all(x["decision"]=="RESEARCH_ONLY" for x in out["markets"])
    assert set(q["book"] for q in out["markets"])==set(BOOKS)
    # each bookmaker's moneyline is quoted, not estimated by the engine
    home=[r for r in out["markets"] if r["market_type"]=="moneyline"
          and r["selection"]=="home"]
    assert len(home)==5
    assert all(r["decimal_odds"]==pytest.approx(2.10) for r in home)


def test_missing_books_are_visible_not_synthesized():
    response=books_response()
    response["bookmakers"]={"FanDuel":response["bookmakers"]["FanDuel"]}
    result=normalize_five_book_events(
        [event()],[response],db(),retrieved_at_utc=STAMP)
    assert result["quote_counts_by_bookmaker"]["FanDuel"]==6
    assert result["missing_bookmakers"]==[
        "Stake","MelBet","1xbet","Bet365"
    ]


def test_three_way_moneyline_and_missing_timestamps_blocked():
    response=books_response()
    response["bookmakers"]["1xbet"][0]["odds"][0]["draw"]="4.30"
    response["bookmakers"]["Stake"][0].pop("updatedAt")
    result=normalize_five_book_events(
        [event()],[response],db(),retrieved_at_utc=STAMP)
    assert result["quote_counts_by_bookmaker"]["1xbet"]==4
    assert result["quote_counts_by_bookmaker"]["Stake"]==4
    assert any(x["reason"]=="THREE_WAY_MONEYLINE_UNSUPPORTED"
               for x in result["skipped"])
    assert any(x["reason"]=="NO_ODDS_UPDATED_AT"
               for x in result["skipped"])


def test_live_and_late_bookmaker_prices_never_enter_pretip_set():
    e=event()
    r=books_response()
    r["status"]="live"
    result=normalize_five_book_events([e],[r],db(),retrieved_at_utc=STAMP)
    assert not result["quotes"]
    late=normalize_five_book_events(
        [e],[books_response()],db(),
        retrieved_at_utc="2026-11-22T01:02:00Z"
    )
    assert late["quotes"]==[]


def test_api_fails_closed_without_key(monkeypatch):
    monkeypatch.delenv("ODDS_API_IO_KEY",raising=False)
    with pytest.raises(ValueError,match="ODDS_API_IO_KEY"):
        fetch_five_book_snapshots()


def test_invalid_spread_and_total_pairs_are_not_guessed():
    outcome,issues=_flatten_one_market(
        "Spread",[{"hdp":-5.5,"home":"1.9"}]
    )
    assert not outcome
    assert "INCOMPLETE_SPREAD_PAIR" in issues
    outcome,issues=_flatten_one_market(
        "Totals",[{"max":230.5,"over":"1.9"}]
    )
    assert not outcome
    assert "INCOMPLETE_TOTAL_PAIR" in issues
