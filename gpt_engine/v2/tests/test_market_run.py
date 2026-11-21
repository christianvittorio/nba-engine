"""Scenario tests for deterministic event reconciliation and as-of reporting."""
import json
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from gpt_engine.v2.odds_map import abbreviation, map_provider_events
from gpt_engine.v2.market_run import (
    asof_market_report, render_markdown, read_frozen_forecasts
)

GID = "game:nba:0022600999"
TIP = "2026-11-22T01:00:00Z"
CUT = "2026-11-21T20:30:00Z"


def make_db():
    con = sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE teams(team_id TEXT PRIMARY KEY,current_name TEXT);
    CREATE TABLE games(game_id TEXT PRIMARY KEY,tip_utc TEXT,
      home_team_id TEXT,away_team_id TEXT,game_type TEXT);
    INSERT INTO teams VALUES('team:nba:1610612738','BOS'),
                            ('team:nba:1610612752','NYK');
    INSERT INTO games VALUES('game:nba:0022600999',
                            '2026-11-22T01:00:00Z',
                            'team:nba:1610612738',
                            'team:nba:1610612752','regular_season');
    """)
    return con


def doc():
    return {
        "game_id": GID, "prediction_id": "prediction:frozen-test",
        "model_version": "gpt-v2-unvalidated", "tip_utc": TIP,
        "cutoff_utc": CUT, "home_team_id": "team:nba:1610612738",
        "away_team_id": "team:nba:1610612752",
        "result": {
            "home_win_probability": .58,
            "expected_home_score": 118.4,
            "expected_away_score": 112.0,
            "margin": {"mean": 6.4},
            "total": {"mean": 230.4},
            "player_statistics": {
                "player:nba:1": {"pts": {"mean": 25.6}}
            }
        }
    }


def q(selection="home", odds=2.0, *, mtype="moneyline", market="game:moneyline",
      line=None, book="book_a", observed="2026-11-21T20:20:00Z",
      retrieved="2026-11-21T20:24:00Z", player_id=None, provider_key=None):
    return {
        "game_id": GID, "tip_utc": TIP,
        "book": book, "market_type": mtype, "market_id": market,
        "selection": selection, "line": line, "decimal_odds": odds,
        "observed_at_utc": observed, "retrieved_at_utc": retrieved,
        **({"player_id": player_id} if player_id else {}),
        **({"provider_market_key":provider_key} if provider_key else {})
    }


def test_nba_schedule_exact_time_and_team_match():
    events = [{
        "id":"provider-event", "home_team":"Boston Celtics",
        "away_team":"New York Knicks", "commence_time":TIP
    }]
    result = map_provider_events(events, make_db())
    assert result["events"]["provider-event"]["game_id"] == GID
    assert result["events"]["provider-event"]["settlement_scope"] == (
        "full_game_including_ot"
    )
    assert abbreviation("Los Angeles Clippers") == "LAC"
    assert abbreviation("LA Clippers") == "LAC"
    assert result["events"]["provider-event"]["players"] == {}
    wrong = [{**events[0], "commence_time":"2026-11-22T04:00:00Z"}]
    assert not map_provider_events(wrong, make_db())["events"]
    swapped = [{**events[0], "home_team":"New York Knicks",
                "away_team":"Boston Celtics"}]
    assert not map_provider_events(swapped, make_db())["events"]


def test_asof_prices_only_and_immutability_link():
    odds = [
        q("home",2.0),
        q("away",1.8),
        q("home",2.5,book="book_b",
          observed="2026-11-21T20:26:00Z",
          retrieved="2026-11-21T20:31:00Z"),
        q("home",2.4,book="book_c",
          observed="2026-11-21T20:29:00Z",
          retrieved="2026-11-21T20:29:00Z"),
    ]
    report = asof_market_report([doc()], odds)
    assert report["raw_quote_count"] == 4
    assert report["usable_asof_quote_count"] == 3
    assert report["excluded"][0]["reason"] == (
        "QUOTE_NOT_AVAILABLE_AT_FORECAST_CUTOFF"
    )
    a = next(x for x in report["markets"] if x["book"] == "book_a"
             and x["selection"] == "home")
    assert a["expected_roi"] == pytest.approx(.16)
    assert a["no_vig_market_probability"] == pytest.approx(
        (1/2)/(1/2 + 1/1.8))
    assert a["decision"] == "RESEARCH_ONLY"
    assert a["prediction_id"] == "prediction:frozen-test"
    assert "UNCALIBRATED" in render_markdown(report)
    c = next(x for x in report["markets"] if x["book"] == "book_c")
    assert c["decision"] == "RESEARCH_ONLY"


def test_point_differences_are_not_ev_for_missing_distributions():
    odds = [
        q("home",1.91,mtype="spread",
          market="game:spread:home:-5.5",line=-5.5),
        q("over",1.91,mtype="total",
          market="game:total:227.5",line=227.5),
        q("over",1.90,mtype="player_prop",
          market="player:pts:player:nba:1:24.5",
          line=24.5,player_id="player:nba:1",
          provider_key="player_points"),
    ]
    report = asof_market_report([doc()], odds)
    rows = report["markets"]
    assert all(r["expected_roi"] is None for r in rows)
    assert all(r["decision"] == "NO_MODEL_PROBABILITY" for r in rows)
    assert rows[0]["model_vs_book_point_difference"] is not None
    spread = next(r for r in rows if r["market_type"] == "spread")
    assert spread["model_vs_book_point_difference"] == pytest.approx(.9)
    total = next(r for r in rows if r["market_type"] == "total")
    assert total["model_vs_book_point_difference"] == pytest.approx(2.9)
    prop = next(r for r in rows if r["market_type"] == "player_prop")
    assert prop["model_stat_mean"] == pytest.approx(25.6)
    assert prop["model_vs_book_point_difference"] == pytest.approx(1.1)


def test_saved_forecast_hash_identity_is_checked_before_loading():
    with TemporaryDirectory() as td:
        root = Path(td)
        pred_file = root/"saved.json"
        pred_file.write_text(json.dumps(doc()))
        ledger = root/"forecast.jsonl"
        row = {
            "file": "saved.json", "game_id": GID,
            "prediction_id": "prediction:frozen-test",
            "cutoff_utc": CUT, "model_version": "gpt-v2-unvalidated"
        }
        ledger.write_text(json.dumps(row)+"\n")
        assert len(read_frozen_forecasts(ledger, root)) == 1
        row["prediction_id"] = "prediction:tampered"
        ledger.write_text(json.dumps(row)+"\n")
        with pytest.raises(ValueError,match="ledger"):
            read_frozen_forecasts(ledger,root)
