"""Contract tests for the separate sportsbook market-value research lane."""
from datetime import datetime, timedelta, timezone
import pytest

from gpt_engine.v2.market_value import compare_markets

TIP = "2026-11-22T01:00:00Z"
ASOF = "2026-11-21T16:10:00Z"
BOOK_AT = "2026-11-21T16:05:00Z"
GID = "game:nba:0022600100"


def prediction(selection, probability, *, line=None, market_id="game:moneyline",
               market_type="moneyline", status="uncalibrated",
               lower=None, asof=ASOF, validation_reference=None):
    return {
        "game_id": GID, "tip_utc": TIP, "asof_utc": asof,
        "market_id": market_id, "market_type": market_type,
        "selection": selection, "line": line,
        "model_version": "gpt-v2-experimental",
        "calibration_status": status, "probability": probability,
        "probability_lower": lower,
        **({"validation_reference": validation_reference}
           if validation_reference is not None else {})
    }


def quote(selection, decimal_odds, *, line=None, book="Example Book",
          market_id="game:moneyline", market_type="moneyline",
          at=BOOK_AT, player_id=None):
    return {
        "game_id": GID, "tip_utc": TIP, "observed_at_utc": at,
        "market_id": market_id, "market_type": market_type,
        "selection": selection, "line": line, "book": book,
        "decimal_odds": decimal_odds,
        **({"player_id": player_id} if player_id is not None else {})
    }


def test_moneyline_price_and_no_vig_are_distinct():
    odds = [quote("home", 2.0), quote("away", 1.8)]
    p = [prediction("home", .58), prediction("away", .42)]
    result = compare_markets(odds, p)
    home = next(r for r in result["markets"] if r["selection"] == "home")
    assert home["expected_roi"] == pytest.approx(.16)
    assert home["break_even_probability"] == pytest.approx(.5)
    vig = .5 + 1/1.8
    assert home["book_overround"] == pytest.approx(vig - 1)
    assert home["no_vig_market_probability"] == pytest.approx(.5/vig)
    assert home["decision"] == "RESEARCH_ONLY"


def test_forward_validation_lower_bound_is_required_for_candidate():
    q = [quote("home", 2.0)]
    p = [prediction("home", .58, status="forward_validated",
                    lower=.54, validation_reference="independent-holdout")]
    record = compare_markets(q, p)["markets"][0]
    assert record["expected_roi"] == pytest.approx(.16)
    assert record["conservative_expected_roi"] == pytest.approx(.08)
    assert record["decision"] == "REVIEW_POSITIVE_EV"
    p[0]["probability_lower"] = None
    assert compare_markets(q,p)["markets"][0]["decision"] == "INSUFFICIENT_UNCERTAINTY"


def test_research_calibration_never_automatically_becomes_a_value_pick():
    q = [quote("home", 2.5)]
    p = [prediction("home", .6, status="research_calibrated", lower=.55)]
    assert compare_markets(q,p)["markets"][0]["decision"] == "RESEARCH_ONLY"


def test_stale_or_invalid_timestamps_are_blocked():
    p = [prediction("home", .58, status="forward_validated",
                    lower=.55, validation_reference="external")]
    stale = quote("home", 2.0, at="2026-11-20T19:00:00Z")
    assert compare_markets([stale],p)["markets"][0]["decision"] == "STALE_COMPARISON"
    with pytest.raises(ValueError,match="After-tip odds"):
        compare_markets([quote("home",2,at=TIP)],p)
    with pytest.raises(ValueError,match="After-tip model"):
        compare_markets([quote("home",2)], [
            prediction("home",.58,asof=TIP)])


def test_spread_opposite_lines_only_and_total_line_matching():
    spread = "game:spread:home:-5.5"
    q = [
        quote("home",1.91,line=-5.5,market_type="spread",market_id=spread),
        quote("away",1.91,line=+5.5,market_type="spread",market_id=spread),
    ]
    result = compare_markets(q, [])["markets"]
    assert all(x["no_vig_market_probability"] == pytest.approx(.5)
               for x in result)
    q[1]["line"] = 6.5  # Wrong handicap; must NOT normalize the vig
    result = compare_markets(q, [])["markets"]
    assert all(x["no_vig_market_probability"] is None for x in result)

    totals = "game:total:231.5"
    q = [
        quote("over",1.89,line=231.5,market_type="total",market_id=totals),
        quote("under",1.91,line=232.5,market_type="total",market_id=totals),
    ]
    result = compare_markets(q, [])["markets"]
    assert all(x["no_vig_market_probability"] is None for x in result)


def test_no_model_probability_means_no_imaginary_ev():
    item = compare_markets([quote("away",1.77)],[])["markets"][0]
    assert item["decision"] == "NO_MODEL_PROBABILITY"
    assert item["expected_roi"] is None


def test_player_props_require_id_and_exact_line():
    q = quote("over",2.0,line=24.5,market_id="player:points:24.5",
              market_type="player_prop",player_id="player:nba:99")
    p = prediction("over",.55,line=24.5,market_id="player:points:24.5",
                   market_type="player_prop")
    p["player_id"] = "player:nba:99"
    result = compare_markets([q],[p])["markets"][0]
    assert result["expected_roi"] == pytest.approx(.1)
    q.pop("player_id")
    with pytest.raises(ValueError,match="stable player_id"):
        compare_markets([q],[p])


def test_reject_invalid_prices_probs_duplicate_models_and_fake_validation():
    with pytest.raises(ValueError,match="Decimal odds"):
        compare_markets([quote("home",1)], [])
    with pytest.raises(ValueError,match="Probability"):
        compare_markets([], [prediction("home",1.3)])
    with pytest.raises(ValueError,match="Duplicate model"):
        p = prediction("home",.6)
        compare_markets([], [p,p])
    with pytest.raises(ValueError,match="documented reference"):
        compare_markets([], [prediction("home",.6,status="forward_validated")])


def test_whole_number_total_push_adjusts_expected_return():
    market_id = "game:total:230"
    q = [quote("over", 2.0, market_id=market_id,
               market_type="total", line=230)]
    # p(win)=.48, p(push)=.10, p(loss)=.42
    p = [prediction("over", .48, line=230, market_id=market_id,
                    market_type="total", lower=.42,
                    status="forward_validated",
                    validation_reference="documented-forward-sample")]
    assert compare_markets(q, p)["markets"][0]["decision"] == "MISSING_PUSH_PROBABILITY"
    p[0]["push_probability"] = .10
    item = compare_markets(q, p)["markets"][0]
    assert item["expected_roi"] == pytest.approx(.06)
    assert item["break_even_probability"] == pytest.approx(.5)
    assert item["unconditional_win_break_even"] == pytest.approx(.45)
    assert item["conservative_expected_roi"] == pytest.approx(-.16)
    assert item["decision"] == "NO_ROBUST_EDGE"


def test_exact_market_and_best_book_price_never_invented():
    q = [quote("home", 1.95, book="Book A"),
         quote("home", 2.05, book="Book B")]
    p = [prediction("home", .53)]
    rows = compare_markets(q, p)["markets"]
    assert rows[0]["book"] == "Book B"
    assert rows[0]["expected_roi"] == pytest.approx(.53*2.05-1)
    assert rows[1]["expected_roi"] == pytest.approx(.53*1.95-1)
    assert rows[0]["no_vig_market_probability"] is None
    assert rows[1]["no_vig_market_probability"] is None


def test_after_model_quote_cannot_be_valued_as_original_price():
    q = [quote("home", 2.0, at="2026-11-21T16:20:00Z")]
    p = [prediction("home", .58, asof="2026-11-21T16:10:00Z")]
    item = compare_markets(q, p)["markets"][0]
    assert item["decision"] == "QUOTE_NOT_AVAILABLE_AT_MODEL_CUTOFF"


def test_missing_retrieval_evidence_blocks_review_even_when_forward_validated():
    q = [quote("home", 2.0)]
    del q[0]["retrieved_at_utc"]
    p = [prediction("home", .58, lower=.54,
                    status="forward_validated",
                    validation_reference="documented-prospective-validation")]
    assert compare_markets(q,p)["markets"][0]["decision"] == "NO_RETRIEVAL_EVIDENCE"
