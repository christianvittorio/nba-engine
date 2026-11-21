"""Independent NBA matchup-layer ablations + frozen chronological calibration.

Intended split (NBA Eastern dates):
  TRAIN             before 2024-10-01
  FEATURE SELECTION  2024-10-01 .. 2025-01-30
  PROB/INTERVAL CAL  2025-01-30 .. 2025-06-30
  UNTOUCHED TEST     2025-10-01 .. 2026-06-30 (2025–26 season)

We never select features, fit Platt regression or choose conformal widths
on the final test set. Models are fitted on TRAIN only. We *report* every
ablation's selection metric; only selected ablation reaches calibration.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from math import exp

import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

from .feature_ablation import game_feature_frame,ablation_feature_sets
from .calibration import PlattCalibrator,ConformalIntervals,bounded_prob,log_loss,brier,paired_bootstrap_loss_delta
from .models import Elo

TRAIN_BEFORE="2024-10-01"
SELECT_BEFORE="2025-01-30"
CAL_BEFORE="2025-07-01"
TEST_FROM="2025-10-01"
TEST_TO="2026-07-01"
VERSION="gpt-v2-matchup-ablation-calibration-0.1"
ALPHAS=(10.0,100.0,400.0)

def split_dates(frame:pd.DataFrame)->tuple:
    date=frame.game_date.astype(str)
    sets=(
        frame[date<TRAIN_BEFORE].copy(),
        frame[(date>=TRAIN_BEFORE)&(date<SELECT_BEFORE)].copy(),
        frame[(date>=SELECT_BEFORE)&(date<CAL_BEFORE)].copy(),
        frame[(date>=TEST_FROM)&(date<TEST_TO)].copy()
    )
    if min(len(s) for s in sets)<80:
        raise ValueError("At least 80 NBA games required in each chronological stage")
    ids=[set(s.game_id) for s in sets]
    if any(ids[i]&ids[j] for i in range(4) for j in range(i+1,4)):
        raise ValueError("Game ID overlap between train/selection/calibration/test")
    for earlier,later in zip(sets,sets[1:]):
        if str(earlier.game_date.max())>=str(later.game_date.min()):
            raise ValueError("Not chronological")
    return sets

def model_for(alpha:float):
    return make_pipeline(
        SimpleImputer(strategy="median",add_indicator=True,
                      keep_empty_features=True),
        StandardScaler(),
        Ridge(alpha=alpha)
    )

def _learn(train:pd.DataFrame,cols:list[str],alpha:float)->tuple:
    X=train[cols].apply(pd.to_numeric,errors="coerce")
    margin=model_for(alpha).fit(X,train.margin.astype(float))
    total=model_for(alpha).fit(X,train.total.astype(float))
    return margin,total

def _predict(models:tuple,df:pd.DataFrame,cols:list[str]):
    X=df[cols].apply(pd.to_numeric,errors="coerce")
    margin=np.asarray(models[0].predict(X),dtype=float)
    total=np.asarray(models[1].predict(X),dtype=float)
    # Fixed before feature selection. Later Platt is fitted on a disjoint
    # calibration stage, not on the feature-selection games.
    p=bounded_prob(1/(1+np.exp(-np.clip(margin/13.0,-30,30))))
    return p,margin,total

def _metrics(p,margin,total,actual:pd.DataFrame):
    win=actual.winner_home.to_numpy(dtype=int)
    return {
        "win_log_loss":round(log_loss(p,win),5),
        "win_brier":round(brier(p,win),5),
        "win_accuracy":round(float(np.mean((p>=.5)==win)),5),
        "margin_mae":round(float(np.mean(np.abs(margin-actual.margin))),4),
        "total_mae":round(float(np.mean(np.abs(total-actual.total))),4),
    }

def _objective(m):
    # Prespecified composite covering winner and two score targets.
    return float(.55*m["win_log_loss"]+.025*m["margin_mae"]+
                 .012*m["total_mae"])

def evaluate_ablation(frame:pd.DataFrame,seed:int=41)->dict:
    tr,select,cal,test=split_dates(frame)
    sets=ablation_feature_sets(frame)
    experiments=[]
    chosen=None
    for name,cols in sets.items():
        best=None
        for alpha in ALPHAS:
            mod=_learn(tr,cols,alpha)
            result=_predict(mod,select,cols)
            metrics=_metrics(*result,select)
            score=_objective(metrics)
            candidate={"group":name,"alpha":alpha,"selection_score":score,
                       "selection_metrics":metrics,"n_features":len(cols),
                       "missing_fraction_selection":round(float(
                           select[cols].isna().to_numpy().mean()),4)}
            if best is None or score<best["selection_score"]:
                best={**candidate,"_model":mod,"_columns":cols}
        experiments.append({k:v for k,v in best.items() if not k.startswith("_")})
        if chosen is None or best["selection_score"]<chosen["selection_score"]:
            chosen=best
    # Entire feature-group and alpha selection ends here. Neither calibration
    # nor holdout were read for selecting the model.
    model=chosen["_model"]
    columns=chosen["_columns"]
    raw_cal,m_cal,t_cal=_predict(model,cal,columns)
    calibrator=PlattCalibrator(c=.4).fit(raw_cal,cal.winner_home.to_numpy())
    margin_intervals=ConformalIntervals().fit(m_cal,cal.margin.to_numpy())
    total_intervals=ConformalIntervals().fit(t_cal,cal.total.to_numpy())

    raw_p,m_test,t_test=_predict(model,test,columns)
    adjusted_p=calibrator.predict(raw_p)
    raw_metrics=_metrics(raw_p,m_test,t_test,test)
    calibrated_metrics=_metrics(adjusted_p,m_test,t_test,test)
    baseline_options=[r for r in experiments if r["group"]=="core"]
    if len(baseline_options)!=1:raise AssertionError("Core feature benchmark missing")
    baseline=baseline_options[0]
    base_columns=sets["core"]
    base_model=_learn(tr,base_columns,baseline["alpha"])
    core_p,core_m,core_t=_predict(base_model,test,base_columns)

    # Elo is evolved with each completed *prior day*, never same-day results.
    series=frame[[
        "game_id","game_date","season","home_team_id","away_team_id",
        "home_score","away_score"
    ]].drop_duplicates("game_id")
    elo=Elo().pregame_series(series)
    aligned=test[["game_id"]].merge(
        elo[["game_id","home_win_probability","margin","total"]],
        on="game_id",validate="one_to_one",sort=False)
    if len(aligned)!=len(test):
        raise ValueError("Elo holdout game alignment mismatch")
    elo_p=aligned.home_win_probability.to_numpy()
    elo_margin=aligned.margin.to_numpy()
    elo_total=aligned.total.to_numpy()
    y=test.winner_home.to_numpy()
    return {
        "experiment_version":VERSION,
        "generated_utc":datetime.now(timezone.utc).isoformat(),
        "source":"Historical NBA team stats and tracked broad-position defender data",
        "historical_caveat":"Source archive corrected after games. Pre-game features use strictly previous game dates, not original live source snapshots.",
        "training":f"before {TRAIN_BEFORE}",
        "feature_selection":f"{TRAIN_BEFORE} .. <{SELECT_BEFORE}",
        "calibration":f"{SELECT_BEFORE} .. <{CAL_BEFORE}",
        "locked_test":f"{TEST_FROM} .. <{TEST_TO}",
        "counts":{"train":len(tr),"selection":len(select),
                  "calibration":len(cal),"test":len(test)},
        "individual_ablation_validation_results":sorted(
            experiments,key=lambda r:r["selection_score"]),
        "chosen_on_selection_only":{
            "group":chosen["group"],"ridge_alpha":chosen["alpha"],
            "selection_objective":round(chosen["selection_score"],5),
            "selection_objective_formula":
                "0.55*win_log_loss+0.025*margin_MAE+0.012*total_MAE",
        },
        "probability_calibrator":{
            "method":"regularized Platt on separate chronological CAL segment",
            **calibrator.parameters(),
        },
        "holdout_metrics":{
            "elo_no_player_injury_adjustments":_metrics(
                elo_p,elo_margin,elo_total,test),
            "core_ridge_uncalibrated":_metrics(
                core_p,core_m,core_t,test),
            "selected_raw":raw_metrics,
            "selected_calibrated":calibrated_metrics,
        },
        "holdout_paired_logloss_change":{
            "selected_calibrated_vs_elo":paired_bootstrap_loss_delta(
                elo_p,adjusted_p,y,seed=seed),
            "selected_calibrated_vs_core":paired_bootstrap_loss_delta(
                core_p,adjusted_p,y,seed=seed+1),
            "selected_calibrated_vs_selected_raw":paired_bootstrap_loss_delta(
                raw_p,adjusted_p,y,seed=seed+2),
        },
        "holdout_intervals":{
            "margin_points":margin_intervals.score(m_test,test.margin.to_numpy()),
            "total_points":total_intervals.score(t_test,test.total.to_numpy()),
        },
        "release_gate":{
            "automatic_live_model_replacement":False,
            "evidence_of_validated_bookmaker_edge":False,
            "uses_future_injuries_or_claude_probabilities":False,
            "notes":[
                "No future injury/lineup snapshots available for historical archive; not claimed.",
                "Observed team styles are not proven coaching systems.",
                "Tracked matchup categories are broad G/F/C, not exact small forwards.",
                "Ablation and calibration must improve out-of-sample metrics before promoted.",
                "This test does not establish positive betting EV or an edge over bookmakers.",
            ]
        },
    }

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--years",nargs="+",type=int,
                        default=[2022,2023,2024,2025,2026])
    parser.add_argument("--output",default="/tmp/gpt-v2-matchup-ablation.json")
    args=parser.parse_args(argv)
    frame=game_feature_frame(args.years)
    report=evaluate_ablation(frame)
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "rows":len(frame),
        "counts":report["counts"],
        "selected":report["chosen_on_selection_only"],
        "holdout":report["holdout_metrics"],
        "paired":report["holdout_paired_logloss_change"],
        "coverage":report["holdout_intervals"],
    },indent=2))

if __name__=="__main__":
    main()
