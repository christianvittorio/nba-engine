"""Test exact two full rest days, no future scores, and conditional-record shrinkage."""
from __future__ import annotations
import pandas as pd
import pytest
import numpy as np

from gpt_engine.v2.situational_streaks import (
    rest_bucket,add_finished_game_context,
    append_pregame_situational_features,
    matchup_record_asof,discover_historical_patterns
)

def games_for_dates(days, seasons=None, home_a=True, winners=None):
    rows=[]
    if seasons is None:
        seasons=[2026]*len(days)
    if winners is None:
        winners=["A"]*len(days)
    for i,(date,season,winner) in enumerate(zip(days,seasons,winners)):
        gid=f"002260{i:04d}"
        for team,opp in (("A","B"),("B","A")):
            home=(team=="A") if home_a else (team=="B")
            rows.append({
                "game_id":gid,"game_date":date,"season":season,
                "game_type":"regular_season",
                "team_id":team,"team":team,
                "opp_team_id":opp,"home":home,
                "pts":110 if team==winner else 98,
            })
    return pd.DataFrame(rows)

def test_exact_rest_definition():
    assert rest_bucket(0)=="0"
    assert rest_bucket(1)=="1"
    assert rest_bucket(2)=="2"
    assert rest_bucket(3)=="3+"
    assert rest_bucket(12)=="3+"
    assert rest_bucket(None) is None
    with pytest.raises(ValueError):
        rest_bucket(-1)
    with pytest.raises(ValueError):
        rest_bucket(1.5)

def test_same_game_result_never_enters_its_pregame_record():
    days=["2025-10-01","2025-10-04","2025-10-07",
          "2025-10-10","2025-10-13"]
    frame=games_for_dates(days)
    a=append_pregame_situational_features(frame)
    cur=a[(a.team_id=="A")&(a.game_date=="2025-10-10")].iloc[0]
    assert cur.true_rest_days==2
    assert cur.situation_sample==2
    assert cur.situation_win_count==2
    assert cur.situation_loss_count==0
    assert cur.situation_shrunk_win_rate<1
    poisoned=frame.copy()
    # Current and future games can be overwritten with large blowouts:
    # only later games may see their results.
    poisoned.loc[poisoned.game_date>="2025-10-10","pts"]=(
        np.where(poisoned.loc[poisoned.game_date>="2025-10-10","team_id"]=="A",
                 15,220)
    )
    changed=append_pregame_situational_features(poisoned)
    target=changed[(changed.team_id=="A")&
                   (changed.game_date=="2025-10-10")].iloc[0]
    for column in ("situation_sample","situation_win_count",
                   "situation_shrunk_win_rate","situation_edge"):
        assert target[column]==cur[column]
    later=changed[(changed.team_id=="A")&
                  (changed.game_date=="2025-10-13")].iloc[0]
    assert later.situation_win_count<3

def test_asof_is_strictly_before_target_eastern_date():
    days=["2025-10-01","2025-10-04","2025-10-07","2025-10-10"]
    frame=games_for_dates(days)
    result=matchup_record_asof(frame,"A","2025-10-10",
                               2026,"home",2)
    assert (result["wins"],result["losses"],result["sample"])==(2,0,2)
    assert result["is_betting_probability"] is False

def test_three_seasons_21_0_is_not_100_percent_probability():
    days=[]
    seasons=[]
    idx=0
    for s in (2024,2025,2026):
        begin=pd.Timestamp(f"{s-1}-11-01")
        for i in range(8):
            days.append(str((begin+pd.Timedelta(days=3*i)).date()))
            seasons.append(s)
            idx+=1
    d=games_for_dates(days,seasons)
    record=matchup_record_asof(d,"A","2026-04-01",2026,"home",2)
    assert record["wins"]==21
    assert record["losses"]==0
    assert record["sample"]==21
    assert record["raw_win_rate"]==1.0
    assert .5<record["shrunk_win_rate"]<1.0
    result=discover_historical_patterns(d,"2026-04-01",min_games=10)
    a=[r for r in result["all_patterns"]
       if r["team"]=="A" and r["venue"]=="home" and r["rest_bucket"]=="2"]
    assert len(a)==1
    assert a[0]["wins"]==21
    assert a[0]["shrunk_rate"]<1
    assert result["n_tests_up_to"]==16

def test_rest_resets_each_season_and_unknown_not_forced_to_two():
    days=["2025-03-30","2025-10-01","2025-10-04"]
    d=games_for_dates(days,[2025,2026,2026])
    ctx=add_finished_game_context(d)
    first=ctx[(ctx.team_id=="A")&(ctx.game_date=="2025-10-01")].iloc[0]
    second=ctx[(ctx.team_id=="A")&(ctx.game_date=="2025-10-04")].iloc[0]
    assert np.isnan(first.true_rest_days)
    assert first.rest_bucket is None
    assert second.rest_bucket=="2"

def test_ambiguous_neutral_venue_is_excluded_not_fabricated():
    d=games_for_dates(["2025-10-01","2025-10-04","2025-10-07"])
    mask=d.game_date=="2025-10-04"
    d.loc[mask,"home"]=False
    ctx=add_finished_game_context(d)
    neutral=ctx[ctx.game_date=="2025-10-04"]
    assert not neutral.venue_valid.any()
    s=matchup_record_asof(ctx,"A","2025-10-08",2026,"home",2)
    assert s["sample"]==1
    assert s["wins"]==1

def test_duplicate_source_row_rejected():
    d=games_for_dates(["2025-10-01"])
    with pytest.raises(ValueError,match="Duplicated"):
        add_finished_game_context(pd.concat([d,d.iloc[[0]]]))
