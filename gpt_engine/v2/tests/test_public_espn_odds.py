"""No-login ESPN scoreboard odds: no invented markets and no lookahead."""
import sqlite3
import pytest

from gpt_engine.v2.public_espn_odds import (
    american_to_decimal,normalize_public_scoreboards,_favorite_home_line,
    fetch_public_scoreboard
)
from gpt_engine.v2.market_run import asof_market_report

TIP="2026-11-22T01:00:00Z"
CAPTURED="2026-11-21T20:05:00Z"
GID="game:nba:0022600999"


def db():
    con=sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE teams(team_id TEXT PRIMARY KEY,current_name TEXT);
    CREATE TABLE games(game_id TEXT PRIMARY KEY,tip_utc TEXT,
        home_team_id TEXT,away_team_id TEXT,game_type TEXT);
    INSERT INTO teams VALUES('team:nba:1','Boston Celtics'),
        ('team:nba:2','New York Knicks');
    INSERT INTO games VALUES('game:nba:0022600999',
        '2026-11-22T01:00:00Z',
        'team:nba:1','team:nba:2','regular_season');
    """)
    return con


def scoreboard(*, moneyline=True, spread=True, total=True, status="pre",
               provider="Draft Kings", with_source_time=False):
    h={"favorite":True,"moneyLine":-160}
    a={"favorite":False,"moneyLine":135}
    if spread:
        h["spreadOdds"]=-110
        a["spreadOdds"]=-110
    if not moneyline:
        h.pop("moneyLine")
        a.pop("moneyLine")
    odds={
        "provider":{"id":"100","name":provider},
        "homeTeamOdds":h,"awayTeamOdds":a,
        "details":"BOS -3.5","spread":-3.5,
    }
    if total:
        odds.update({"overUnder":225.5,"overOdds":-108,"underOdds":-112})
    if with_source_time:
        odds["lastModified"]="2026-11-21T19:59:00Z"
    return {
        "events":[{
            "id":"401909999","date":TIP,
            "status":{"type":{"state":status}},
            "competitions":[{
                "competitors":[
                    {"homeAway":"home","team":{"displayName":"Boston Celtics"}},
                    {"homeAway":"away","team":{"displayName":"New York Knicks"}},
                ],
                "odds":[odds]
            }]
        }]
    }


def forecast():
    return {
        "game_id":GID,"prediction_id":"prediction:immutable",
        "model_version":"uncalibrated",
        "tip_utc":TIP,"cutoff_utc":"2026-11-21T20:10:00Z",
        "home_team_id":"team:nba:1",
        "away_team_id":"team:nba:2",
        "result":{
            "home_win_probability":.58,"simulation_count":100,
            "expected_home_score":113,"expected_away_score":108,
            "margin":{"mean":5},"total":{"mean":221},
            "player_statistics":{}
        }
    }


def test_american_decimal_prices_and_bad_data():
    assert american_to_decimal("-160")==pytest.approx(1.625)
    assert american_to_decimal("+135")==pytest.approx(2.35)
    assert american_to_decimal("EVEN")==pytest.approx(2.)
    assert american_to_decimal(0) is None
    assert american_to_decimal("1.90") is None
    assert american_to_decimal(False) is None


def test_exact_home_away_spread_total_and_actual_capture():
    report=normalize_public_scoreboards(
        [(scoreboard(with_source_time=True),CAPTURED)],db())
    assert report["requires_api_key"] is False
    assert report["verified_bookmakers"]==["Draft Kings"]
    assert len(report["quotes"])==6
    assert all(q["observed_at_utc"]==CAPTURED for q in report["quotes"])
    assert all(q["retrieved_at_utc"]==CAPTURED for q in report["quotes"])
    assert all(q["provider_last_modified_utc"]==
               "2026-11-21T19:59:00Z" for q in report["quotes"])
    spread=[q for q in report["quotes"] if q["market_type"]=="spread"]
    assert {q["line"] for q in spread}=={-3.5,3.5}
    assert len(set(q["market_id"] for q in spread))==1
    totals=[q for q in report["quotes"] if q["market_type"]=="total"]
    assert {q["selection"] for q in totals}=={"over","under"}
    market=asof_market_report([forecast()],report["quotes"])
    assert market["usable_asof_quote_count"]==6
    moneylines=[r for r in market["markets"]
                if r["market_type"]=="moneyline"]
    assert len(moneylines)==2
    assert all(r["decision"]=="RESEARCH_ONLY" for r in moneylines)


def test_missing_prices_do_not_create_fake_odds():
    item=scoreboard(moneyline=False,spread=False,total=False)
    report=normalize_public_scoreboards([(item,CAPTURED)],db())
    assert report["quotes"]==[]
    assert any(x["reason"]=="NO_COMPLETE_PRICED_MARKET"
               for x in report["skipped"])


def test_post_tip_and_unmapped_games_skipped():
    data=scoreboard(status="post")
    assert normalize_public_scoreboards(
        [(data,CAPTURED)],db())["quotes"]==[]
    data=scoreboard()
    data["events"][0]["competitions"][0]["competitors"][0]["team"]["displayName"]=(
        "Los Angeles Lakers"
    )
    report=normalize_public_scoreboards([(data,CAPTURED)],db())
    assert report["quotes"]==[]
    assert any(x["reason"] in ("NO_UNIQUE_NBA_GAME_MATCH",)
               for x in report["skipped"])


def test_raw_capture_after_forecast_not_backfilled():
    fetched="2026-11-21T20:20:00Z"
    result=normalize_public_scoreboards([(scoreboard(),fetched)],db())
    report=asof_market_report([forecast()],result["quotes"])
    assert report["usable_asof_quote_count"]==0


def test_unknown_provider_and_ambiguous_handicap_are_not_assumed():
    data=scoreboard()
    data["events"][0]["competitions"][0]["odds"][0]["provider"]={}
    assert normalize_public_scoreboards([(data,CAPTURED)],db())["quotes"]==[]
    incomplete={
        "homeTeamOdds":{"favorite":False},
        "awayTeamOdds":{"favorite":False},
        "spread":-4.5,"details":"UNKNOWN -4.5",
    }
    assert _favorite_home_line(incomplete,
              "Boston Celtics","New York Knicks") is None


def test_fetch_validation_no_auth_or_key_required():
    with pytest.raises(ValueError,match="YYYYMMDD"):
        fetch_public_scoreboard("tomorrow")


def test_malformed_public_event_does_not_break_remaining_slate():
    original=scoreboard()
    malformed=scoreboard()
    malformed["events"][0]["id"]="unverified-bad"
    malformed["events"][0]["date"]="nonsense"
    malformed["events"][0]["competitions"]="not-a-competition-array"
    together={"events":malformed["events"]+original["events"]}
    result=normalize_public_scoreboards([(together,CAPTURED)],db())
    assert len(result["quotes"])==6
    assert any(r["reason"]=="AMBIGUOUS_COMPETITION"
               for r in result["skipped"])


def test_malformed_bookmaker_odds_do_not_crash_slate():
    original=scoreboard()
    bad=original["events"][0]["competitions"][0]["odds"][0]
    bad["homeTeamOdds"]="garbled"
    result=normalize_public_scoreboards([(original,CAPTURED)],db())
    assert result["quotes"]==[]
    assert any(x["reason"]=="MALFORMED_TEAM_ODDS"
               for x in result["skipped"])


def nested_2026_scoreboard():
    data=scoreboard(moneyline=False,spread=False,total=False,
                    provider="DraftKings")
    odds=data["events"][0]["competitions"][0]["odds"][0]
    odds["homeTeamOdds"]={"favorite":True,"team":{"abbreviation":"BOS"}}
    odds["awayTeamOdds"]={"favorite":False,"team":{"abbreviation":"NYK"}}
    odds["moneyline"]={
        "home":{"close":{"odds":"-160"},"open":{"odds":"-150"}},
        "away":{"close":{"odds":"+135"},"open":{"odds":"+125"}},
    }
    odds["pointSpread"]={
        "home":{"close":{"line":"-3.5","odds":"-110"},
                "open":{"line":"-3","odds":"-110"}},
        "away":{"close":{"line":"+3.5","odds":"-110"},
                "open":{"line":"+3","odds":"-110"}},
    }
    odds["total"]={
        "over":{"close":{"line":"225.5","odds":"-108"},
                "open":{"line":"224.5","odds":"-110"}},
        "under":{"close":{"line":"225.5","odds":"-112"},
                 "open":{"line":"224.5","odds":"-110"}},
    }
    return data


def test_real_2026_espn_nested_schema_prices_exact_lines_only():
    report=normalize_public_scoreboards(
        [(nested_2026_scoreboard(),CAPTURED)],db())
    assert len(report["quotes"])==6
    assert report["verified_bookmakers"]==["DraftKings"]
    moneylines=[x for x in report["quotes"] if x["market_type"]=="moneyline"]
    assert {x["decimal_odds"] for x in moneylines}=={1.625,2.35}
    spreads=[x for x in report["quotes"] if x["market_type"]=="spread"]
    assert {x["line"] for x in spreads}=={-3.5,3.5}
    totals=[x for x in report["quotes"] if x["market_type"]=="total"]
    assert {x["line"] for x in totals}=={225.5}
    assert all(x["observed_at_utc"]==CAPTURED for x in report["quotes"])


def test_2026_nested_mismatch_is_rejected_not_cross_paired():
    data=nested_2026_scoreboard()
    obj=data["events"][0]["competitions"][0]["odds"][0]
    obj["pointSpread"]["away"]["close"]["line"]="+4.5"
    obj["total"]["under"]["close"]["line"]="226.5"
    report=normalize_public_scoreboards([(data,CAPTURED)],db())
    assert all(x["market_type"]=="moneyline" for x in report["quotes"])
    assert len(report["quotes"])==2
    assert {r["reason"] for r in report["skipped"]}>={
        "CONTRADICTORY_SPREAD_LINES","CONTRADICTORY_TOTAL_LINES"
    }


def test_open_prices_never_substitute_for_missing_pretip_close():
    data=nested_2026_scoreboard()
    obj=data["events"][0]["competitions"][0]["odds"][0]
    for field in ("moneyline","pointSpread","total"):
        for side in obj[field]:
            obj[field][side].pop("close")
    report=normalize_public_scoreboards([(data,CAPTURED)],db())
    assert report["quotes"]==[]
