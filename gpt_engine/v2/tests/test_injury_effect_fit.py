"""Regression tests for genuine point-in-time injury features and fitting."""
from datetime import datetime,timezone,timedelta
import pandas as pd
import numpy as np
import pytest

from gpt_engine.v2.injury_effect_fit import (
    PregamePlayerRates,team_out_feature,snapshot_for_game,
    fit_coefficient,score_frame,chronological_experiment,VAL_BEFORE,
    TRAIN_BEFORE,
)

def test_source_must_be_generated_and_committed_before_game_cutoff():
    tip="2026-11-18T23:30:00Z"
    early={
        "commit_sha":"a"*40,
        "generated_utc":"2026-11-18T21:44:37Z",
        "committed_utc":"2026-11-18T21:44:57Z",
        "teams":{"ATL":{"roster":[1]}}
    }
    late={**early,"commit_sha":"b"*40,
          "generated_utc":"2026-11-18T22:40:00Z",
          "committed_utc":"2026-11-18T22:45:00Z"}
    wrong_date={**early,"commit_sha":"c"*40,
               "generated_utc":"2026-11-17T21:44:37Z",
               "committed_utc":"2026-11-17T21:44:57Z"}
    assert snapshot_for_game([wrong_date,late,early],"2026-11-18",tip)["commit_sha"]=="a"*40
    assert snapshot_for_game([late],"2026-11-18",tip) is None
    assert snapshot_for_game([wrong_date],"2026-11-18",tip) is None

def test_same_day_or_future_player_points_do_not_enter_injury_values():
    rows=[]
    for i in range(7):
        rows.append({"player_id":"101","game_id":str(i),
                     "game_date":str((pd.Timestamp("2026-11-10")
                        +pd.Timedelta(days=i)).date()),"min":32,"pts":21})
    base=pd.DataFrame(rows)
    with_today=pd.concat([base,pd.DataFrame([{
         "player_id":"101","game_id":"NOW","game_date":"2026-11-17",
         "min":43,"pts":99}])],ignore_index=True)
    first=PregamePlayerRates(base).pregame_value("101","2026-11-17")
    second=PregamePlayerRates(with_today).pregame_value("101","2026-11-17")
    assert first==second
    future=PregamePlayerRates(with_today).pregame_value("101","2026-11-16")
    assert future[1]=="2026-11-15"

def test_unknown_injuries_not_assumed_out_and_unresolved_not_fabricated():
    history=pd.DataFrame([
        {"player_id":"101","game_id":str(i),
         "game_date":f"2026-11-{i+1:02d}","min":35,"pts":25}
        for i in range(10)])
    rates=PregamePlayerRates(history)
    snapshot={"teams":{"GSW":{
        "roster":[{"nba_id":101},{"nba_id":-99}],
        "injuries":[
            {"nba_id":101,"name":"Sample A","status":"Out"},
            {"nba_id":-99,"name":"Unknown","status":"Out"},
            {"nba_id":102,"name":"Questionable","status":"Day-To-Day"},
        ]}}}
    outcome=team_out_feature(snapshot,"GSW","2026-11-12",rates)
    assert outcome["matched_out_names"]==["Sample A"]
    assert outcome["value"]>0
    assert outcome["out_missing_history_or_id"]==["Unknown"]
    assert outcome["uncertain_player_names"]==["Questionable"]
    assert outcome["last_player_game_date"]=="2026-11-10"

def _fake_examples():
    rng=np.random.default_rng(16)
    days=list(pd.date_range("2026-11-01",periods=20))
    rows=[]
    for day in days:
        for i in range(6):
            x=float(rng.choice([-12,-5,0,0,3,10]))
            raw_margin=float(rng.normal(0,6))
            # Fixed true beta 0.65 before noisy actual observation.
            actual=raw_margin+0.65*x+rng.normal(0,3)
            p=1/(1+np.exp(-raw_margin*.1554))
            rows.append({
                "game_id":f"g-{day.day}-{i}","game_date":day.strftime("%Y-%m-%d"),
                "net_out_above_replacement":x,"base_margin":raw_margin,
                "actual_margin":actual,"base_p_home":p,"home_win":int(actual>0),
                "source_sha":"a"*40,
            })
    return pd.DataFrame(rows)

def test_train_fit_recovers_positive_response():
    d=_fake_examples()
    train=d[d.game_date<TRAIN_BEFORE]
    coefficient=fit_coefficient(train,25)
    assert 0.25<coefficient<1.0,coefficient

def test_heldout_actual_scores_cannot_change_fitted_parameter():
    base=_fake_examples()
    report=chronological_experiment(base)
    assert report["status"]=="RESEARCH_FIT_COMPLETED_NOT_PRODUCTION_APPROVED"
    assert report["candidate_live_adoption"] is False
    assert report["counts"]["train"]>=70
    assert report["counts"]["validation"]>=10
    assert report["counts"]["test"]>=10
    altered=base.copy()
    mask=altered.game_date>=VAL_BEFORE
    altered.loc[mask,"actual_margin"]+=50
    altered.loc[mask,"home_win"]=1
    poisoned=chronological_experiment(altered)
    assert report["selected_from_validation_only"]==poisoned["selected_from_validation_only"]
    assert report["frozen_test"]!=poisoned["frozen_test"]

def test_too_few_reports_refuses_trained_status():
    d=_fake_examples()
    report=chronological_experiment(d.head(15))
    assert report["status"]=="INSUFFICIENT_HISTORICAL_PREGAME_SAMPLE"
    assert report["candidate_live_adoption"] is False
