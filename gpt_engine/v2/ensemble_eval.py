"""Conservative Elo + matchup-Ridge probability/score ensemble research.

Priority 5, distinct historical windows:
  2022-2024-09 TRAIN: fit regularized prior-game ridge.
  2024-10 to 2025-01 SELECT: choose ONLY the blend weight.
  2025-01 to 2025-06 CAL: Platt calibration + split-conformal intervals.
  2025-10 to 2026-06 HOLDOUT: frozen score/interval/accuracy evaluation.

No use of the 2025-26 labels for choosing weights or calibration. Elo's
pregame features update from COMPLETED games on the prior calendar date
only. The historical corrected archive is not an original point-in-time
sportsbook/ESPN snapshot. This is a research challenger; there is no
automatic production replacement.
"""
from __future__ import annotations
import argparse,json
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import pandas as pd

from .ablation_eval import (
    split_dates,_learn,_predict,_metrics,TRAIN_BEFORE,SELECT_BEFORE,
    CAL_BEFORE,TEST_FROM,TEST_TO
)
from .feature_ablation import game_feature_frame,ablation_feature_sets
from .calibration import (
    PlattCalibrator,ConformalIntervals,log_loss,brier,
    paired_bootstrap_loss_delta,bounded_prob
)
from .models import Elo

VERSION="gpt-v2-elo-ridge-ensemble-0.1"
# The matchup predictor was chosen by earlier selection-stage experiments;
# do NOT tune its columns/alpha on 2025–26 game outcomes.
RIDGE_GROUP="core+offense_defense_crossmatchups"
RIDGE_ALPHA=100.0
WEIGHTS=(0.0,.25,.50,.75,1.0)  # Elo weights; 1.0 is native Elo
EPSILON=1e-5

def blend(elo_p,ridge_p,elo_margin,ridge_margin,ridge_total,
          elo_weight:float)->tuple[np.ndarray,np.ndarray,np.ndarray]:
    if not 0<=elo_weight<=1:raise ValueError("Elo weight outside [0,1]")
    ep=np.asarray(elo_p,dtype=float)
    rp=np.asarray(ridge_p,dtype=float)
    em=np.asarray(elo_margin,dtype=float)
    rm=np.asarray(ridge_margin,dtype=float)
    total=np.asarray(ridge_total,dtype=float)
    if not (ep.shape==rp.shape==em.shape==rm.shape==total.shape):
        raise ValueError("Ensemble dimensions mismatch")
    if not all(np.isfinite(x).all() for x in (ep,rp,em,rm,total)):
        raise ValueError("Non-finite ensemble component")
    p=bounded_prob(elo_weight*ep+(1-elo_weight)*rp)
    margin=elo_weight*em+(1-elo_weight)*rm
    return p,margin,total

def choose_blend(elo_p,ridge_p,elo_margin,ridge_margin,ridge_total,
                 target_winner,target_margin)->dict:
    y=np.asarray(target_winner,dtype=int)
    m=np.asarray(target_margin,dtype=float)
    if len(y)<80 or len(m)!=len(y):
        raise ValueError("Need >=80 separate selection games")
    if not set(np.unique(y))<={0,1}:
        raise ValueError("Nonbinary outcome")
    options=[]
    for w in WEIGHTS:
        p,margin,_=blend(elo_p,ridge_p,elo_margin,ridge_margin,ridge_total,w)
        ll=log_loss(p,y)
        mae=float(np.mean(np.abs(margin-m)))
        # Predeclared emphasis on calibrated winner distribution; modest
        # margin-accuracy tie-breaker. No fitting on the eventual holdout.
        objective=ll+.0025*mae
        options.append({
            "elo_weight":w,"ridge_weight":1-w,
            "selection_log_loss":round(ll,6),
            "selection_margin_mae":round(mae,4),
            "selection_objective":round(objective,6),
        })
    selected=min(options,key=lambda r:(
        r["selection_objective"],
        -r["elo_weight"],
    ))
    return {"candidates":options,"selected":selected,
            "no_holdout_labels_used_to_choose_weight":True}

def _pre_gameday_elo(frame:pd.DataFrame)->pd.DataFrame:
    source=frame[["game_id","game_date","season","home_team_id",
                  "away_team_id","home_score","away_score"]].copy()
    if source.duplicated("game_id").any():
        raise ValueError("Elo duplicate game ID")
    elo=Elo().pregame_series(source)
    joined=frame[["game_id"]].merge(
        elo[["game_id","home_win_probability","margin","total"]],
        on="game_id",how="left",validate="one_to_one",sort=False
    )
    if joined.isna().any().any() or len(joined)!=len(frame):
        raise ValueError("Unaligned Elo prior-game predictions")
    return joined

def _coverage(cal:ConformalIntervals,margin,total,test:pd.DataFrame):
    return {
        "margin":cal.score(margin,test.margin.to_numpy(dtype=float)),
        "total":total.score(
            test["ensemble_total_prediction"].to_numpy(dtype=float),
            test.total.to_numpy(dtype=float)
        )
    }

def _reliability(p,y):
    labels=np.asarray(y,dtype=int)
    probs=np.asarray(p,dtype=float)
    b=[]
    for lo,hi in ((0,.2),(.2,.4),(.4,.6),(.6,.8),(.8,1.001)):
        mask=(probs>=lo)&(probs<hi)
        b.append({
            "bucket":f"{lo:.1f}–{min(hi,1):.1f}",
            "n_games":int(mask.sum()),
            "mean_predicted_home_win":round(float(probs[mask].mean()),4)
                    if mask.any() else None,
            "actual_home_win":round(float(labels[mask].mean()),4)
                    if mask.any() else None,
        })
    return b

def evaluate_ensemble(frame:pd.DataFrame)->dict:
    train,selection,cal,test=split_dates(frame)
    cols=ablation_feature_sets(frame)[RIDGE_GROUP]
    ridge=_learn(train,cols,RIDGE_ALPHA)
    elo=_pre_gameday_elo(frame)
    values=frame.reset_index(drop=True)
    elo_map=pd.DataFrame({
        "game_id":values.game_id.to_numpy(),
        "elo_p":elo.home_win_probability.to_numpy(dtype=float),
        "elo_margin":elo.margin.to_numpy(dtype=float),
        "elo_total":elo.total.to_numpy(dtype=float)
    })
    def anchored(part):
        m=part[["game_id"]].merge(
            elo_map,on="game_id",validate="one_to_one",sort=False)
        if len(m)!=len(part) or m.isna().any().any():
            raise ValueError("Elo date-period join mismatch")
        return m
    elos,eloc,elot=(anchored(x) for x in (selection,cal,test))
    rs,ms,ts=_predict(ridge,selection,cols)
    pick=choose_blend(
        elos.elo_p,rs,elos.elo_margin,ms,ts,
        selection.winner_home,selection.margin
    )
    w=pick["selected"]["elo_weight"]
    rc,mc,tc=_predict(ridge,cal,cols)
    pc,margin_cal,total_cal=blend(
        eloc.elo_p,rc,eloc.elo_margin,mc,tc,w
    )
    # CAL period is never used to select the weight or Ridge features.
    calibrator=PlattCalibrator(c=.4).fit(pc,cal.winner_home.to_numpy(dtype=int))
    margin_intervals=ConformalIntervals().fit(
        margin_cal,cal.margin.to_numpy(dtype=float))
    total_intervals=ConformalIntervals().fit(
        total_cal,cal.total.to_numpy(dtype=float))
    rt,mt,tt=_predict(ridge,test,cols)
    pb,mb,tb=blend(elot.elo_p,rt,elot.elo_margin,mt,tt,w)
    calibrated_p=calibrator.predict(pb)
    # Use existing v2 metric definitions for apples-to-apples holdout.
    # Force positional numeric arrays: test retains original historical
    # row indices, whereas the game-ID-aligned Elo merge has 0..N indices.
    # Subtracting pandas Series would silently align on unrelated indices,
    # yielding NaN MAE despite otherwise valid predictions.
    baseline_elo=_metrics(
        elot.elo_p.to_numpy(dtype=float),
        elot.elo_margin.to_numpy(dtype=float),
        elot.elo_total.to_numpy(dtype=float),test
    )
    ridge_metrics=_metrics(rt,mt,tt,test)
    raw_metrics=_metrics(pb,mb,tb,test)
    calibrated_metrics=_metrics(calibrated_p,mb,tb,test)
    ylabel=test.winner_home.to_numpy(dtype=int)
    return {
        "experiment_version":VERSION,
        "generated_utc":datetime.now(timezone.utc).isoformat(),
        "training":f"dates < {TRAIN_BEFORE}",
        "blend_selection":f"{TRAIN_BEFORE} <= date < {SELECT_BEFORE}",
        "probability_interval_calibration":f"{SELECT_BEFORE} <= date < {CAL_BEFORE}",
        "historical_frozen_holdout":f"{TEST_FROM} <= date < {TEST_TO}",
        "counts":{
            "train":len(train),"selection":len(selection),
            "calibration":len(cal),"test":len(test)
        },
        "frozen_ridge_component":{
            "feature_group":RIDGE_GROUP,
            "alpha":RIDGE_ALPHA,
            "model_fit_on_train_only":True,
        },
        "blend_weight_selected_on_selection_only":pick,
        "calibrator":{
            "method":"Platt trained ONLY on nonoverlapping chronological calibration games",
            "parameters":calibrator.parameters(),
        },
        "locked_holdout":{
            "elo_baseline":baseline_elo,
            "ridge_component_raw":ridge_metrics,
            "ensemble_raw":raw_metrics,
            "ensemble_platt_calibrated":calibrated_metrics,
        },
        "ensemble_80pct_interval_coverage":{
            "margin":margin_intervals.score(mb,test.margin.to_numpy(dtype=float))["0.8"],
            "total":total_intervals.score(tb,test.total.to_numpy(dtype=float))["0.8"],
        },
        "ensemble_interval_90pct_coverage":{
            "margin":margin_intervals.score(mb,test.margin.to_numpy(dtype=float))["0.9"],
            "total":total_intervals.score(tb,test.total.to_numpy(dtype=float))["0.9"],
        },
        "heldout_win_probability_reliability":{
            "ensemble_calibrated":_reliability(calibrated_p,ylabel),
            "elo":_reliability(elot.elo_p,ylabel),
        },
        "heldout_paired_logloss_difference":{
            "calibrated_ensemble_vs_elo":paired_bootstrap_loss_delta(
                elot.elo_p,calibrated_p,ylabel),
            "raw_ensemble_vs_elo":paired_bootstrap_loss_delta(
                elot.elo_p,pb,ylabel,seed=42),
            "calibrated_ensemble_vs_ridge":paired_bootstrap_loss_delta(
                rt,calibrated_p,ylabel,seed=43),
        },
        "promotion_gate":{
            "auto_deploy":False,
            "current_daily_simulator_unchanged":True,
            "requires_new_forward_holdout_and_full_mc_prob_calibration":True,
            "not_equivalent_to_calibrating_possession_monte_carlo":True,
        },
        "warnings":[
            "Elo + Ridge only; live possession-simulation forecasts are not a component of this historical ensemble.",
            "The locked 2025–26 season was inspected in other GPT v2 research, so its status is chronological but not newly independent of all project decisions.",
            "An ensemble that has lower historical log-loss may still underperform future Elo or pretip market prices.",
            "Platt calibration and conformal intervals apply to THIS ensemble, not to the live possession simulator.",
            "No automatic promotion and no sportsbook recommendations.",
        ]
    }

def _require_json_finite(data,path="$"):
    """Reject non-finite model diagnostics without silently rewriting NaN."""
    if isinstance(data,dict):
        for k,v in data.items():
            _require_json_finite(v,path+"."+str(k))
    elif isinstance(data,(list,tuple)):
        for i,v in enumerate(data):
            _require_json_finite(v,path+f"[{i}]")
    elif isinstance(data,(float,np.floating)) and not np.isfinite(data):
        raise ValueError(f"Non-finite ensemble metric at {path}: {data!r}")


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--years",type=int,nargs="+",
                    default=[2022,2023,2024,2025,2026])
    ap.add_argument("--output",required=True)
    a=ap.parse_args(argv)
    frame=game_feature_frame(a.years)
    report=evaluate_ensemble(frame)
    _require_json_finite(report)
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print("ENSEMBLE_HOLDOUT "+json.dumps({
        "counts":report["counts"],
        "selection":report["blend_weight_selected_on_selection_only"]["selected"],
        "metrics":report["locked_holdout"],
        "intervals80":report["ensemble_80pct_interval_coverage"],
        "intervals90":report["ensemble_interval_90pct_coverage"],
        "paired":report["heldout_paired_logloss_difference"],
    },separators=(",",":")),flush=True)

if __name__=="__main__":main()
