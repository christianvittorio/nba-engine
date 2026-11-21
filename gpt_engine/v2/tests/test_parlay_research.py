"""Daily parlay research test contracts: odds, refund pushes and no-lookahead."""
from __future__ import annotations

from copy import deepcopy

import pytest

from gpt_engine.v2.parlay_research import (
    build_parlay_board, render_markdown
)

NOW = "2026-11-21T16:10:00Z"
TIP = "2026-11-22T01:00:00Z"
CAPTURE = "2026-11-21T16:05:00Z"
FORECAST = "2026-11-21T16:08:00Z"


def quote(game, book="DraftKings", side="home", odds=2.1, p=.60,
          market_type="moneyline", line=None, captured=CAPTURE,
          push=0, decision="RESEARCH_ONLY", status="uncalibrated",
          lower=None):
    mid = ("game:moneyline" if market_type=="moneyline"
           else "game:total:230" if market_type=="total"
           else "game:spread:home:-5.5")
    return {
        "game_id":"game:nba:"+str(game), "market_id":mid,
        "market_type":market_type,"selection":side,
        "line":line,"player_id":None,"book":book,
        "tip_utc":TIP, "observed_at_utc":captured,
        "retrieved_at_utc":captured,
        "forecast_cutoff_utc":FORECAST,
        "snapshot_gap_minutes":3.0,
        "model_probability":p, "decimal_odds":odds,
        "no_vig_market_probability":.50,
        "push_probability":push,
        "expected_roi":p*odds+push-1,
        "decision":decision,
        "calibration_status":status,
        "model_probability_lower":lower,
    }


def board(rows, **kwargs):
    return build_parlay_board(
        {"research_only":True,"markets":rows,"games":[]},
        now_utc=NOW,date_eastern="2026-11-21",**kwargs
    )


def test_two_books_cannot_combine_best_prices_from_each():
    rows=[quote(1,"Book A",odds=2.1,p=.6),
          quote(2,"Book B",odds=2.4,p=.6)]
    result=board(rows)
    assert result["eligible_single_legs"]==2
    assert result["status"]=="NO_QUALIFYING_PARLAY"
    assert result["best_research_combination"] is None
    assert "NO PARLAY" in render_markdown(result)


def test_best_single_book_two_leg_roi_and_hit_rate():
    rows=[quote(1,p=.60,odds=2.1),quote(2,p=.57,odds=2.05)]
    result=board(rows)
    candidate=result["best_research_combination"]
    assert result["status"]=="RESEARCH_RANKING_AVAILABLE"
    assert candidate["book"]=="DraftKings"
    assert candidate["leg_count"]==2
    assert candidate["full_win_decimal_odds"]==pytest.approx(2.1*2.05)
    assert candidate["full_win_probability_independent"]==pytest.approx(.6*.57)
    assert candidate["estimated_roi_independent"]==pytest.approx(.6*2.1*.57*2.05-1)
    assert candidate["actionable"] is False
    assert result["betting_recommendation"] is None
    assert candidate["validation_status"]=="UNCALIBRATED_RESEARCH_ONLY"
    assert result["best_forward_validated_review"] is None
    assert "Neither modeled hit probability nor raw ROI is a calibrated" in render_markdown(result)


def test_no_same_game_parlays_or_unsupported_player_props():
    a=quote(1, side="home")
    b=quote(1,side="away",p=.58)
    c=quote(2,side="over",market_type="player_prop",line=20.5)
    result=board([a,b,c])
    assert result["status"]=="NO_QUALIFYING_PARLAY"
    assert result["eligible_single_legs"]==2


def test_highest_chance_prioritizes_two_leg_ticket_over_three():
    rows=[quote(1,odds=1.9,p=.6),quote(2,odds=1.9,p=.6),
          quote(3,odds=1.9,p=.6)]
    result=board(rows,maximum_results=5)
    assert result["ranking_metric"]=="full_win_probability_independent"
    assert result["best_research_combination"]["leg_count"]==2
    assert result["candidate_tickets_screened"]==4
    assert result["ranked_research_combinations"][-1]["leg_count"]==3
    result=board(rows,minimum_joint_win_probability=.3)
    assert result["best_research_combination"]["leg_count"]==2


def test_best_hit_rate_not_highest_return_even_with_other_positive_value_tickets():
    # The longshot pair has higher ROI, but a much lower chance of winning.
    rows=[
        quote(1,odds=1.6,p=.70),
        quote(2,odds=1.6,p=.70),
        quote(3,odds=2.5,p=.46),
        quote(4,odds=2.5,p=.46),
    ]
    result=board(rows,maximum_results=20)
    leader=result["best_research_combination"]
    assert result["ranking_policy"]=="MAX_HIT_PROBABILITY_SUBJECT_TO_POSITIVE_ESTIMATED_VALUE"
    assert leader["leg_count"]==2
    assert {leg["game_id"] for leg in leader["legs"]}=={
        "game:nba:1","game:nba:2"
    }
    assert leader["full_win_probability_independent"]==pytest.approx(.49)
    longshot=next(
        combo for combo in result["ranked_research_combinations"]
        if {leg["game_id"] for leg in combo["legs"]}=={
           "game:nba:3","game:nba:4"
        }
    )
    assert longshot["estimated_roi_independent"]>leader["estimated_roi_independent"]
    assert leader["full_win_probability_independent"]>longshot["full_win_probability_independent"]
    assert "Highest modeled full-win probability" in render_markdown(result)


def test_highest_probability_is_still_required_to_have_positive_raw_value():
    # A .93 * .93 sure-looking ticket with bad price is not eligible.
    rows=[
        quote(1,odds=1.04,p=.93),
        quote(2,odds=1.04,p=.93),
        quote(3,odds=1.9,p=.60),
        quote(4,odds=1.9,p=.60),
    ]
    result=board(rows)
    best=result["best_research_combination"]
    assert {leg["game_id"] for leg in best["legs"]}=={
       "game:nba:3","game:nba:4"
    }
    assert result["eligible_single_legs"]==2


def test_tie_on_probability_uses_roi_as_tie_break_only():
    rows=[
      quote(1,odds=1.8,p=.7),
      quote(2,odds=1.7,p=.7),
      quote(3,odds=2.0,p=.7),
    ]
    result=board(rows,maximum_results=5)
    best=result["best_research_combination"]
    assert best["full_win_probability_independent"]==pytest.approx(.49)
    assert {leg["game_id"] for leg in best["legs"]}=={
        "game:nba:1","game:nba:3"
    }


def test_integer_line_pushes_are_refunds_not_full_wins():
    a=quote(1,side="over",market_type="total",line=230,odds=2.1,
            p=.5,push=.1)
    b=quote(2,odds=2,p=.6)
    result=board([a,b])
    choice=result["best_research_combination"]
    assert choice["estimated_roi_independent"]==pytest.approx(
        (.5*2.1+.1)*(.6*2)-1
    )
    assert choice["full_win_probability_independent"]==pytest.approx(.5*.6)
    assert choice["no_loss_probability_independent"]==pytest.approx(.6*.6)


def test_stale_post_tip_after_cutoff_and_missing_market_side_rejected():
    good=quote(1)
    stale=quote(2,captured="2026-11-21T15:00:00Z")
    late=quote(2,captured="2026-11-21T16:09:00Z")
    bad=quote(2)
    bad["no_vig_market_probability"]=None
    invalid=quote(2)
    invalid["decision"]="QUOTE_NOT_AVAILABLE_AT_MODEL_CUTOFF"
    for bad_item in (stale,late,bad,invalid):
        result=board([good,bad_item])
        assert result["status"]=="NO_QUALIFYING_PARLAY"
    past_tip=quote(2)
    past_tip["tip_utc"]="2026-11-21T15:30:00Z"
    assert board([good,past_tip])["best_research_combination"] is None


def test_capture_time_must_be_close_across_ticket():
    first=quote(1,captured="2026-11-21T16:00:00Z")
    last=quote(2,captured="2026-11-21T16:08:00Z")
    last["forecast_cutoff_utc"]="2026-11-21T16:09:00Z"
    assert board([first,last],max_capture_span_minutes=5)["best_research_combination"] is None
    assert board([first,last],max_capture_span_minutes=10)["best_research_combination"] is not None


def test_forward_validated_review_requires_every_leg_and_lower_bound():
    rows=[quote(1,decision="REVIEW_POSITIVE_EV",status="forward_validated",
                lower=.54),
          quote(2,decision="REVIEW_POSITIVE_EV",status="forward_validated",
                lower=.52)]
    result=board(rows)
    assert result["best_forward_validated_review"] is not None
    assert result["best_forward_validated_review"]["actionable"] is False
    rows[1]["calibration_status"]="uncalibrated"
    result=board(rows)
    assert result["best_forward_validated_review"] is None


def test_research_never_becomes_validated_without_provenance():
    rows=[quote(1,p=.6,odds=2.2),quote(2,p=.6,odds=2.2)]
    rows[0]["calibration_status"]="forward_validated"
    result=board(rows)
    assert result["best_forward_validated_review"] is None


def test_date_filter_and_failed_report_contract():
    rows=[quote(1),quote(2)]
    assert board(rows)["candidate_tickets_screened"]==1
    assert build_parlay_board({"research_only":True,"markets":rows},
             now_utc=NOW,date_eastern="2026-11-22")["candidate_tickets_screened"]==0
    with pytest.raises(ValueError,match="As-of research"):
        build_parlay_board({"research_only":False,"markets":rows},now_utc=NOW)
    with pytest.raises(ValueError,match="two to four"):
        board(rows,min_legs=1)
    with pytest.raises(ValueError,match="two to four"):
        board(rows,max_legs=5)


def test_no_positive_single_leg_edge_means_no_parlay():
    result=board([quote(1,p=.4,odds=1.91),quote(2,p=.4,odds=1.91)])
    assert result["status"]=="NO_QUALIFYING_PARLAY"
    assert result["candidate_tickets_screened"]==0


def test_single_board_ranks_hit_probability_before_raw_ev_and_one_per_game():
    rows = [
        quote(1,odds=1.28,p=.80),
        quote(2,odds=1.43,p=.72),
        quote(3,odds=2.0,p=.60),
        quote(1,side="away",odds=1.5,p=.75),
    ]
    result=board(rows)
    assert result["single_ranking_metric"]=="model_probability"
    assert result["single_selection_status"]=="RESEARCH_SINGLES_AVAILABLE"
    singles=result["ranked_high_hit_singles"]
    assert len(singles)==3
    assert [x["game_id"] for x in singles]==[
        "game:nba:1","game:nba:2","game:nba:3"
    ]
    assert [x["model_probability"] for x in singles]==[.80,.72,.60]
    assert singles[0]["individual_research_roi"] < singles[2]["individual_research_roi"]
    assert all(x["actionable"] is False for x in singles)
    md=render_markdown(result)
    assert "individual games" in md and "Break-even P" in md


def test_tiny_positive_ev_below_old_one_percent_cutoff_is_now_eligible():
    a=quote(1,odds=1.431,p=.70)  # 0.17% raw modeled ROI
    b=quote(2,odds=1.431,p=.70)
    result=board([a,b])
    assert result["filters"]["minimum_leg_roi"]==pytest.approx(.001)
    assert result["eligible_single_legs"]==2
    assert result["best_research_single"]["model_probability"]==pytest.approx(.70)
    assert result["best_research_combination"]["full_win_probability_independent"]==pytest.approx(.49)


def test_even_high_probability_losing_value_is_not_a_single_or_parlay():
    negative=quote(1,odds=1.04,p=.93)
    positive=quote(2,odds=1.5,p=.72)
    result=board([negative,positive])
    assert result["eligible_single_legs"]==1
    assert result["best_research_single"]["game_id"]=="game:nba:2"
    assert result["best_research_combination"] is None


def test_singles_require_a_model_win_chance_above_55_percent():
    result=board([quote(1,p=.53,odds=2.0),quote(2,p=.52,odds=2.0)])
    assert result["eligible_single_legs"]==2
    assert result["single_selection_status"]=="NO_QUALIFYING_SINGLE"
    assert result["ranked_high_hit_singles"]==[]
    assert result["best_research_combination"] is not None


def test_parlay_only_combines_games_from_same_eastern_slate_day():
    a=quote(1)
    b=quote(2)
    # Both are pre-tip in UTC, but November 22 01:00 UTC vs November 23 01:00
    b["tip_utc"]="2026-11-23T01:00:00Z"
    report={"research_only":True,"markets":[a,b]}
    result=build_parlay_board(report,now_utc=NOW,date_eastern=None)
    assert result["eligible_single_legs"]==2
    assert result["best_research_combination"] is None
