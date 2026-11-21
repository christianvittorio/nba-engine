"""Offline provider integration / append-only quote history tests."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from gpt_engine.v2.odds_ingest import (
    normalize_provider_events, append_odds_ledger, fetch_live_odds
)

TIP = "2026-11-22T01:00:00Z"
RETRIEVED = "2026-11-21T20:05:00Z"
UPDATED = "2026-11-21T20:00:00Z"
EVENT = "fixture-nba-event-1"
GID = "game:nba:0022600999"


def fixture_payload():
    return [{
        "id": EVENT, "sport_key": "basketball_nba",
        "home_team": "Boston Celtics", "away_team": "New York Knicks",
        "commence_time": TIP,
        "bookmakers": [{
            "key": "book_alpha", "last_update": UPDATED,
            "markets": [
                {"key": "h2h", "last_update": UPDATED,
                 "outcomes": [
                     {"name": "Boston Celtics", "price": 1.83},
                     {"name": "New York Knicks", "price": 2.08},
                 ]},
                {"key": "spreads", "last_update": UPDATED,
                 "outcomes": [
                     {"name": "Boston Celtics", "price": 1.91, "point": -5.5},
                     {"name": "New York Knicks", "price": 1.91, "point": 5.5},
                 ]},
                {"key": "totals", "last_update": UPDATED,
                 "outcomes": [
                     {"name": "Over", "price": 1.90, "point": 225.5},
                     {"name": "Under", "price": 1.90, "point": 225.5},
                 ]},
                {"key": "player_points", "last_update": UPDATED,
                 "outcomes": [
                     {"name": "Over", "description": "Example Player",
                      "price": 1.9, "point": 26.5},
                     {"name": "Under", "description": "Example Player",
                      "price": 1.9, "point": 26.5},
                     {"name": "Over", "description": "Unknown Player",
                      "price": 1.9, "point": 22.5},
                 ]},
            ]
        }]
    }]


def mapping():
    return {"events": {EVENT: {
        "game_id": GID,
        "home_team": "Boston Celtics",
        "away_team": "New York Knicks",
        "tip_utc": TIP,
        "settlement_scope": "full_game_including_ot",
        "players": {"Example Player": "player:nba:12345"}
    }}}


def test_offline_normalizes_markets_and_prevents_player_fabrication():
    result = normalize_provider_events(fixture_payload(), mapping(),
                                        retrieved_at_utc=RETRIEVED)
    quotes = result["quotes"]
    assert len(quotes) == 8
    assert {q["market_type"] for q in quotes} == {
        "moneyline", "spread", "total", "player_prop"
    }
    spread = [q for q in quotes if q["market_type"] == "spread"]
    assert spread[0]["market_id"] == spread[1]["market_id"]
    assert {q["line"] for q in spread} == {-5.5, 5.5}
    props = [q for q in quotes if q["market_type"] == "player_prop"]
    assert len(props) == 2
    assert all(q["player_id"] == "player:nba:12345" for q in props)
    assert all(q["observed_at_utc"] == UPDATED for q in quotes)
    assert all(q["retrieved_at_utc"] == RETRIEVED for q in quotes)
    assert any(x["reason"] == "UNRESOLVED_SELECTION_OR_PLAYER"
               for x in result["skipped"])


def test_unmapped_or_unverified_event_is_omitted():
    result = normalize_provider_events(fixture_payload(), {"events": {}},
                                        retrieved_at_utc=RETRIEVED)
    assert result["quotes"] == []
    assert result["skipped"][0]["reason"] == "UNMAPPED_EVENT"
    bad = mapping()
    bad["events"][EVENT]["away_team"] = "Miami Heat"
    result = normalize_provider_events(fixture_payload(), bad,
                                        retrieved_at_utc=RETRIEVED)
    assert result["quotes"] == []
    assert result["skipped"][0]["reason"] == "UNVERIFIED_EVENT_MAPPING"


def test_retrieval_and_source_time_must_be_pretip_and_in_sequence():
    result = normalize_provider_events(fixture_payload(), mapping(),
                                        retrieved_at_utc=TIP)
    assert not result["quotes"]
    event = fixture_payload()
    event[0]["bookmakers"][0]["markets"][0]["last_update"] = (
        "2026-11-21T20:20:00Z"
    )
    result = normalize_provider_events(event, mapping(),
                                        retrieved_at_utc=RETRIEVED)
    assert len(result["quotes"]) == 6  # h2h unavailable; rest still valid
    assert any(s["reason"] == "INVALID_SOURCE_TIMESTAMP"
               for s in result["skipped"])


def test_ledger_keeps_original_bytes_on_duplicate_and_adds_new_price():
    original = normalize_provider_events(fixture_payload(), mapping(),
                                          retrieved_at_utc=RETRIEVED)["quotes"]
    with TemporaryDirectory() as td:
        ledger = Path(td)/"odds.jsonl"
        a = append_odds_ledger(ledger, original)
        assert a["new_quotes"] == 8
        before = ledger.read_bytes()
        reread = [{**q, "retrieved_at_utc": "2026-11-21T20:10:00Z"}
                  for q in original]
        assert append_odds_ledger(ledger, reread)["new_quotes"] == 0
        assert ledger.read_bytes() == before
        next_quote = {**original[0],
                      "decimal_odds": 1.99,
                      "quote_id": "odds:changed-quote"}
        assert append_odds_ledger(ledger, [next_quote])["new_quotes"] == 1
        assert len(ledger.read_text().splitlines()) == 9
        with pytest.raises(ValueError, match="Conflicting"):
            append_odds_ledger(ledger, [{**next_quote,"decimal_odds": 2.08}])


def test_live_requires_key_and_rejects_invalid_region(monkeypatch):
    monkeypatch.delenv("THE_ODDS_API_KEY", raising=False)
    with pytest.raises(ValueError, match="THE_ODDS_API_KEY"):
        fetch_live_odds()
    monkeypatch.setenv("THE_ODDS_API_KEY", "placeholder")
    with pytest.raises(ValueError, match="Unsupported odds region"):
        fetch_live_odds(region="not-a-region")
