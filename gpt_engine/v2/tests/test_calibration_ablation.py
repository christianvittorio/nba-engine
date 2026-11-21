"""Calibration and season-blocked matchup layer tests."""
import numpy as np
import pandas as pd
import pytest

from gpt_engine.v2.calibration import (
    PlattCalibrator,ConformalIntervals,log_loss,brier,
    paired_bootstrap_loss_delta
)
from gpt_engine.v2.feature_ablation import (
    BASE_PRIORS,FEATURE_GROUPS,rolling_team_features,
    append_tracked_features,ablation_feature_sets
)
from gpt_engine.v2.ablation_eval import evaluate_ablation

def _source_games():
    rows=[]
    for i in range(35):
        date=str((pd.Timestamp("2024-10-01")+pd.Timedelta(days=i)).date())
        for team,opp,home in (("1","2",True),("2","1",False)):
            d={k:val for k,val in BASE_PRIORS.items()}
            d.update({"season":2025,"game_id":f"002240{i:04d}",
                      "game_date":date,"game_type":"regular_season",
                      "team_id":team,"opp_team_id":opp,"home":home,
                      "pts":112+i%7})
            # Raw 3PA defense is needed to reconstruct 3P% allowed.
            d["opp_fg3m"]=12;d["opp_fg3a"]=34
            rows.append(d)
    return pd.DataFrame(rows)

def test_current_day_box_score_poison_does_not_affect_features():
    raw=_source_games()
    a=rolling_team_features(raw)
    changed=raw.copy()
    changed.loc[changed.game_date=="2024-10-15","off_rating"]=1000
    b=rolling_team_features(changed)
    sel=(a.team_id=="1")&(a.game_date=="2024-10-15")
    sel_b=(b.team_id=="1")&(b.game_date=="2024-10-15")
    for col in ("rolling5_off_rating","rolling20_off_rating",
                "multi_off_rating","rolling20_efg_pct"):
        assert float(a.loc[sel,col].iloc[0])==float(b.loc[sel_b,col].iloc[0])
    # But the next day's features ARE allowed to learn yesterday's game.
    next_d=(a.team_id=="1")&(a.game_date=="2024-10-16")
    next_b=(b.team_id=="1")&(b.game_date=="2024-10-16")
    assert float(a.loc[next_d,"rolling5_off_rating"].iloc[0])!=float(
        b.loc[next_b,"rolling5_off_rating"].iloc[0])

def test_tracked_matchup_observations_are_previous_day_only():
    base=rolling_team_features(_source_games())
    tracking=pd.DataFrame([
        {"season":2025,"def_team_id":"1","team_id":"1",
         "game_id":"0022400000","game_date":"2024-10-13",
         "off_position":"F","partial_possessions":100,
         "matchup_assists":10,"matchup_potential_assists":19,
         "player_points":38},
        {"season":2025,"def_team_id":"1","team_id":"1",
         "game_id":"0022400001","game_date":"2024-10-15",
         "off_position":"F","partial_possessions":100,
         "matchup_assists":900,"matchup_potential_assists":900,
         "player_points":900},
    ])
    a=append_tracked_features(base,tracking)
    present=a[(a.team_id=="1")&(a.game_date=="2024-10-15")]
    assert float(present.tracked_F_assists_per100.iloc[0])<20
    nextgame=a[(a.team_id=="1")&(a.game_date=="2024-10-16")]
    assert float(nextgame.tracked_F_assists_per100.iloc[0])>200

def test_conformal_width_and_coverage():
    rng=np.random.default_rng(3)
    pred=np.full(400,220.0)
    true=pred+rng.normal(0,15,400)
    intervals=ConformalIntervals().fit(pred,true)
    q=intervals.quantiles
    assert q["0.9"]>=q["0.8"]>=q["0.5"]
    results=intervals.score(pred,true)
    assert results["0.8"]["observed_coverage"]>=.8

def test_platt_fit_and_small_sample_rejected():
    with pytest.raises(ValueError):
        PlattCalibrator().fit([.5]*10,[0,1]*5)
    rng=np.random.default_rng(4)
    p=np.clip(rng.uniform(.15,.85,400),.01,.99)
    y=(rng.random(400)<p).astype(int)
    fitted=PlattCalibrator().fit(p,y)
    out=fitted.predict(p)
    assert np.all((out>0)&(out<1))
    assert fitted.parameters()["calibration_games"]==400

def test_paired_bootstrap_sign_and_count():
    y=np.array([0,1]*50)
    incorrect=np.where(y==1,.1,.9)
    correct=np.where(y==1,.9,.1)
    summary=paired_bootstrap_loss_delta(incorrect,correct,y,iterations=150)
    assert summary["n_games"]==100
    assert summary["delta_new_minus_reference"]<0
    assert summary["paired_95pct_interval"][1]<0

def _synthetic_experiment():
    rng=np.random.default_rng(41)
    dates=(list(pd.date_range("2023-10-01",periods=150))+
           list(pd.date_range("2024-10-15",periods=100))+
           list(pd.date_range("2025-02-01",periods=100))+
           list(pd.date_range("2025-11-01",periods=100)))
    from gpt_engine.v2.feature_ablation import CROSS_FEATURES, EVENT_CROSS_FEATURES
    frame=pd.DataFrame({
        "game_id":[f"game-{i}" for i in range(len(dates))],
        "game_date":[str(d.date()) for d in dates],
        "home_team_id":["1"]*len(dates),"away_team_id":["2"]*len(dates),
        "season":[d.year+1 if d.month>=7 else d.year for d in dates],
    })
    sets={key:[f"{side}__{c}" for c in cols for side in ("home","away")]
          for key,cols in FEATURE_GROUPS.items()}
    allnames=list(dict.fromkeys(sum(sets.values(),[])+
                                list(CROSS_FEATURES)+list(EVENT_CROSS_FEATURES)
                                +["home_court_advantage"]))
    for name in allnames:
        frame[name]=rng.normal(0,1,len(frame))
    strength=3*frame["home__rolling20_off_rating"]-2*frame["away__rolling20_off_rating"]
    raw_margin=3+strength+rng.normal(0,9,len(frame))
    margin=np.where(raw_margin>=0,1,-1)*np.maximum(2,np.abs(np.rint(raw_margin)))
    total=np.rint(225+rng.normal(0,16,len(frame)))
    frame["margin"]=margin
    frame["total"]=total
    frame["home_score"]=np.rint((margin+total)/2).astype(int)
    frame["away_score"]=np.rint((total-margin)/2).astype(int)
    frame["margin"]=frame.home_score-frame.away_score
    frame["total"]=frame.home_score+frame.away_score
    frame["winner_home"]=(margin>0).astype(int)
    return frame

def test_holdout_cannot_select_features_or_calibrate():
    frame=_synthetic_experiment()
    one=evaluate_ablation(frame)
    assert one["counts"]=={"train":150,"selection":100,
                            "calibration":100,"test":100}
    assert one["release_gate"]["automatic_live_model_replacement"] is False
    assert "tracked_defender_matchups" in str(
        one["individual_ablation_validation_results"])
    # Poison the never-seen holdout scores: chosen features and Platt params
    # MUST be unchanged; only final holdout scores/metrics may change.
    poisoned=frame.copy()
    test=poisoned.game_date>="2025-10-01"
    poisoned.loc[test,"home_score"]+=70
    poisoned.loc[test,"margin"]+=70
    poisoned.loc[test,"total"]+=70
    poisoned.loc[test,"winner_home"]=1
    two=evaluate_ablation(poisoned)
    assert one["chosen_on_selection_only"]==two["chosen_on_selection_only"]
    assert one["probability_calibrator"]==two["probability_calibrator"]
    assert one["holdout_metrics"]!=two["holdout_metrics"]
