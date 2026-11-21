"""Reproducible final-outcome and CLV paper-tracking regression tests."""
import pytest

from gpt_engine.v2.market_grade import (
    evaluate_outcomes, _grade_market, _finals_index
)

TIP = "2026-11-22T01:00:00Z"
MODEL_AT = "2026-11-21T20:30:00Z"
GID = "game:nba:0022600999"


def final():
    return {
        "game_id": GID, "tip_utc": TIP, "status": "final",
        "final_at_utc": "2026-11-22T04:00:00Z",
        "retrieved_at_utc": "2026-11-22T04:05:00Z",
        "source_id": "fixture:official-box",
        "home_score": 110, "away_score": 100,
        "players": {
            "player:nba:1":{"status":"played","pts":25,"reb":8},
            "player:nba:2":{"status":"dnp"}
        }
    }


def report_row(*, market="game:moneyline", mtype="moneyline",
               selection="home", line=None, player_id=None,
               price=2.0, raw_ev=.16, book="a"):
    return {
        "game_id":GID, "tip_utc": TIP,
        "forecast_cutoff_utc": MODEL_AT,
        "prediction_id":"prediction:fixture",
        "market_id":market, "market_type":mtype, "selection":selection,
        "line":line, "player_id": player_id, "book":book,
        "decimal_odds":price,
        "retrieved_at_utc":"2026-11-21T20:25:00Z",
        "observed_at_utc":"2026-11-21T20:20:00Z",
        "expected_roi":raw_ev, "decision":"RESEARCH_ONLY",
    }


def odds(*, price, observed, retrieved):
    return {
        "game_id":GID, "tip_utc":TIP, "market_id":"game:moneyline",
        "market_type":"moneyline", "selection":"home", "line":None,
        "book":"a", "decimal_odds":price,
        "observed_at_utc":observed,
        "retrieved_at_utc":retrieved,
    }


def report(rows):
    return {
        "version":"gpt-v2-market-asof-report-0.1",
        "games":[{"game_id":GID,"model_home_win_probability":.58}],
        "markets":rows,
    }


def test_score_settlement_spread_total_player_prop_void_and_push():
    game = final()
    assert _grade_market(report_row(),game) == "WIN"
    assert _grade_market(report_row(selection="away"),game) == "LOSS"
    assert _grade_market(report_row(market="spread:+10",mtype="spread",
                                    line=-10), game) == "PUSH"
    assert _grade_market(report_row(market="spread:away:+9",mtype="spread",
                                    selection="away",line=9),game) == "LOSS"
    assert _grade_market(report_row(market="total:210",mtype="total",
                                    selection="over",line=210),game) == "PUSH"
    assert _grade_market(report_row(market="total:211",mtype="total",
                                    selection="under",line=211),game) == "WIN"
    assert _grade_market(report_row(market="player:pts:player:nba:1:24.5",
                                    mtype="player_prop",selection="over",
                                    line=24.5,player_id="player:nba:1"),game) == "WIN"
    assert _grade_market(report_row(market="player:pts:player:nba:2:24.5",
                                    mtype="player_prop",selection="over",
                                    line=24.5,player_id="player:nba:2"),game) == "VOID"
    assert _grade_market(report_row(market="player:pts:player:nba:3:24.5",
                                    mtype="player_prop",selection="over",
                                    line=24.5,player_id="player:nba:3"),game) == "MISSING_PLAYER_RESULT"


def test_clv_requires_pretip_capture_same_book_same_market_and_line():
    original = odds(price=2.0,observed="2026-11-21T20:20:00Z",
                    retrieved="2026-11-21T20:25:00Z")
    near_tip = odds(price=1.8,observed="2026-11-22T00:40:00Z",
                    retrieved="2026-11-22T00:42:00Z")
    # Later collected history is NOT a pretip closing capture.
    post_tip = odds(price=1.6,observed="2026-11-22T00:55:00Z",
                    retrieved="2026-11-22T01:05:00Z")
    outcome = evaluate_outcomes(report([report_row()]),
                                [original,near_tip,post_tip],
                                {"games":[final()]})
    row = outcome["graded_markets"][0]
    assert row["settlement"] == "WIN"
    assert row["unit_return"] == pytest.approx(1.0)
    assert row["closing_decimal_odds"] == pytest.approx(1.8)
    assert row["closing_line_value"] == pytest.approx(2/1.8-1)
    assert outcome["calibration"]["model_brier"] == pytest.approx((.58-1)**2)
    assert outcome["hypothetical_positive_raw_ev_cohort"]["settled"] == 1
    assert not outcome["calibration"]["sample_large_enough_for_public_accuracy_claim"]


def test_paper_cohort_uses_one_best_book_without_lookahead():
    rows = [
        report_row(book="a",price=1.95,raw_ev=.08),
        report_row(book="b",price=2.05,raw_ev=.14),
        report_row(selection="away",book="b",price=1.7,raw_ev=-.2),
    ]
    result = evaluate_outcomes(report(rows), [], {"games":[final()]})
    cohort = result["hypothetical_positive_raw_ev_cohort"]
    assert cohort["observations"] == 1
    assert cohort["win"] == 1
    assert result["market_audit"]["observations"] == 3
    assert result["market_audit"]["win"] == 2
    assert result["market_audit"]["loss"] == 1


def test_no_finals_and_invalid_source_evidence_are_not_settled():
    result = evaluate_outcomes(report([report_row()]), [], {"games":[]})
    assert result["market_audit"]["settled"] == 0
    assert result["calibration"]["model_brier"] is None
    bad = final()
    bad["retrieved_at_utc"] = "2026-11-22T00:30:00Z"
    with pytest.raises(ValueError, match="predates final"):
        _finals_index({"games":[bad]})
    bad = final()
    bad["home_score"] = bad["away_score"]
    with pytest.raises(ValueError, match="tied"):
        _finals_index({"games":[bad]})


def test_multiclass_probability_scoring_counts_push_and_only_one_contract():
    a=report_row(market="game:total:210",mtype="total",
                 selection="over",line=210,price=2.0,raw_ev=0.0)
    a["model_probability"]=.45
    a["push_probability"]=.10
    b={**a,"book":"other-book","decimal_odds":2.2}
    result=evaluate_outcomes(report([a,b]), [], {"games":[final()]})
    scored=result["market_probability_scoring"]["total"]
    assert scored["distinct_settled_contracts"] == 1
    assert scored["categorical_log_loss"] == pytest.approx(
        2.302585092994046
    )
    assert scored["categorical_brier"] == pytest.approx(
        .45**2+(.10-1)**2+.45**2
    )
    assert scored["binary_brier_nonpush"] is None
