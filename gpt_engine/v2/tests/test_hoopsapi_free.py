"""HoopsAPI free-tier NBA odds normalization and absence safeguards."""
import sqlite3
import pytest
from gpt_engine.v2.hoopsapi_free import (
    normalize_hoopsapi,fetch_free_nba_odds,FREE_BOOKS
)
from gpt_engine.v2.market_run import asof_market_report

TIP="2026-11-22T01:00:00Z"
STAMP="2026-11-21T20:05:00Z"
CAPTURE="2026-11-21T20:00:00Z"
GID="game:nba:0022600999"

def db():
    con=sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE teams(team_id TEXT PRIMARY KEY,current_name TEXT);
    CREATE TABLE games(game_id TEXT PRIMARY KEY,tip_utc TEXT,
      home_team_id TEXT,away_team_id TEXT,game_type TEXT);
    INSERT INTO teams VALUES('nba:home','BOS'),('nba:away','NYK');
    INSERT INTO games VALUES('game:nba:0022600999',
      '2026-11-22T01:00:00Z','nba:home','nba:away','regular_season');
    """)
    return con

def payload():
    book_odds={
        "moneyline":{"home":2.10,"away":1.80},
        "spread":{"line":-5.5,"home":1.91,"away":1.91},
        "total":{"line":230.5,"over":1.95,"under":1.87}
    }
    names=("fanduel","1xbet","betway","pinnacle","unibet")
    return {"count":1,"games":[{
        "game_id":222,"competition":"NBA","container":"USA",
        "home":"Boston Celtics","away":"New York Knicks",
        "start_time":TIP,
        "updated_at":CAPTURE,
        "providers":{b:{"captured_at":CAPTURE} for b in names},
        "periods":{"ft":{b:dict(book_odds) for b in names}},
    }]}

def doc():
    return {
        "game_id":GID,"prediction_id":"prediction:frozen",
        "tip_utc":TIP,"cutoff_utc":"2026-11-21T20:10:00Z",
        "home_team_id":"nba:home","away_team_id":"nba:away",
        "model_version":"research",
        "result":{"home_win_probability":.58,
                  "expected_home_score":120.,"expected_away_score":115.,
                  "margin":{"mean":5.},"total":{"mean":235.},
                  "player_statistics":{}}
    }

def test_five_free_books_capture_moneyline_spread_totals():
    result=normalize_hoopsapi(payload(),db(),retrieved_at_utc=STAMP)
    assert set(FREE_BOOKS)=={"FanDuel","1xbet","Betway","Pinnacle","Unibet"}
    assert result["free_tier"] is True
    assert result["free_requests_per_day"]==10
    assert len(result["quotes"])==30
    assert result["mapped_nba_games"]==1
    assert set(q["book"] for q in result["quotes"])==set(FREE_BOOKS)
    assert all(q["observed_at_utc"]==CAPTURE for q in result["quotes"])
    assert all(q["retrieved_at_utc"]==STAMP for q in result["quotes"])
    assert all(q["provider"]=="hoopsapi-free" for q in result["quotes"])
    assert result["missing_original_books"]==["Stake","MelBet","Bet365"]

def test_free_quotes_match_frozen_model_without_inventing_other_books():
    result=normalize_hoopsapi(payload(),db(),retrieved_at_utc=STAMP)
    report=asof_market_report([doc()],result["quotes"])
    assert report["usable_asof_quote_count"]==30
    home=[r for r in report["markets"] if
          r["selection"]=="home" and r["market_type"]=="moneyline"]
    assert len(home)==5
    assert all(r["decimal_odds"]==pytest.approx(2.1) for r in home)
    assert all(r["decision"]=="RESEARCH_ONLY" for r in home)
    assert not any(r["book"] in ("Stake","MelBet","Bet365")
                   for r in report["markets"])

def test_missing_provider_capture_time_never_invents_bookie_quote():
    p=payload()
    p["games"][0]["providers"]["fanduel"]["captured_at"]=None
    result=normalize_hoopsapi(p,db(),retrieved_at_utc=STAMP)
    assert result["quote_counts_by_book"]["FanDuel"]==0
    assert any(s["reason"]=="NO_BOOK_CAPTURE_TIMESTAMP"
               for s in result["skipped"])

def test_retrospective_api_access_cannot_backfill_original_odds():
    p=payload()
    late=normalize_hoopsapi(
        p,db(),retrieved_at_utc="2026-11-22T02:00:00Z")
    assert late["quotes"]==[]
    # A frozen prediction is earlier than original source retrieval.
    p["games"][0]["providers"]["1xbet"]["captured_at"]=(
        "2026-11-21T20:09:00Z"
    )
    early=normalize_hoopsapi(p,db(),
                             retrieved_at_utc="2026-11-21T20:12:00Z")
    assert len(early["quotes"])>0
    report=asof_market_report([doc()],early["quotes"])
    assert report["usable_asof_quote_count"]==0

def test_absent_key_fails_closed_without_network(monkeypatch):
    monkeypatch.delenv("HOOPSAPI_KEY",raising=False)
    with pytest.raises(ValueError,match="HOOPSAPI_KEY"):
        fetch_free_nba_odds()
