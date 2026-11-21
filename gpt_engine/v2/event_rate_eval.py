"""Point-in-time NBA possession-event forecasting: rate-blend research gate.

Priorities 3/4: learn how much an opponent's observed shot/turnover/FT/OREB
allowance improves a team's own 20-game prior for the NEXT game's event rates.
No raw same-game source statistic is allowed in the estimate.

We fit ONLY 4 bounded blending weights on a separate validation window.
The 2025-26 holdout is graded without refitting. Candidate rates may be
passed to future experimental Monte Carlo runs, but are NOT automatically
promoted to the daily simulator or advertised as calibrated scores.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .feature_ablation import game_feature_frame,load_teams
from .ablation_eval import TRAIN_BEFORE,SELECT_BEFORE,CAL_BEFORE,TEST_FROM,TEST_TO

VERSION="gpt-v2-opponent-event-blend-research-0.1"
WEIGHTS=(0.0,.2,.4,.6,.8,1.0)
RATE_SPEC={
    "three_point_rate":{
        "own":"three_point_rate","opp":"opp_3pa_rate_allowed",
        "label":"three_point_rate","prior":.37,"range":(.12,.68)},
    "turnover_rate":{
        "own":"tm_tov_pct","opp":"opp_tov_rate_forced",
        "label":"tm_tov_pct","prior":.13,"range":(.055,.28)},
    "offensive_rebound_rate":{
        "own":"oreb_pct","opp":"opp_oreb_rate_allowed",
        "label":"oreb_pct","prior":.26,"range":(.08,.48)},
    "free_throw_rate":{
        "own":"fta_rate","opp":"opp_fta_rate_allowed",
        "label":"fta_rate","prior":.25,"range":(.06,.62)},
}

def _clipped(x,limits):
    return np.clip(np.asarray(x,dtype=float),*limits)

def candidate_event_rate(own,opponent_allowed,weight:float,
                         *,league_prior:float,limits:tuple[float,float]):
    if not 0<=weight<=1:
        raise ValueError("Opponent weight must be [0,1]")
    own=np.asarray(own,dtype=float)
    opponent_allowed=np.asarray(opponent_allowed,dtype=float)
    if own.shape!=opponent_allowed.shape:
        raise ValueError("Own/opp rates must align")
    a=np.where(np.isfinite(own),own,league_prior)
    b=np.where(np.isfinite(opponent_allowed),opponent_allowed,league_prior)
    return _clipped((1-weight)*a+weight*b,limits)

def _event_input_frame(game_frame:pd.DataFrame,raw:pd.DataFrame)->pd.DataFrame:
    """Current-game event rates are TARGETS ONLY, strictly not features."""
    fields=["game_id","game_date","season"]
    rows=[]
    for side,other in (("home","away"),("away","home")):
        frame=game_frame[fields].copy()
        frame["team_id"]=game_frame[f"{side}_team_id"].astype(str)
        frame["side"]=side
        for event,spec in RATE_SPEC.items():
            frame[event+"_own_prior"]=game_frame[
                f"{side}__rolling20_{spec['own']}"].to_numpy(dtype=float)
            frame[event+"_opponent_prior"]=game_frame[
                f"{other}__rolling20_{spec['opp']}"].to_numpy(dtype=float)
        rows.append(frame)
    all_inputs=pd.concat(rows,ignore_index=True)
    cols=["game_id","team_id"]+[spec["label"] for spec in RATE_SPEC.values()]
    real=raw[cols].copy()
    real["team_id"]=real.team_id.astype(str)
    real=real.rename(columns={v["label"]:k+"_actual" for k,v in RATE_SPEC.items()})
    merged=all_inputs.merge(real,on=["game_id","team_id"],
                            validate="one_to_one",how="inner")
    if len(merged)!=2*len(game_frame):
        raise ValueError("Event-rate target join missing a game/team")
    if merged.duplicated(["game_id","team_id"]).any():
        raise ValueError("Duplicate team-game observation")
    return merged.sort_values(["game_date","game_id","side"]).reset_index(drop=True)

def event_rate_frame(years=(2022,2023,2024,2025,2026))->pd.DataFrame:
    from .feature_ablation import load_teams,game_feature_frame
    games=game_feature_frame(list(years),with_tracking=False)
    raw=load_teams(list(years))
    return _event_input_frame(games,raw)

def _metrics(y,estimate):
    y=np.asarray(y,dtype=float)
    p=np.asarray(estimate,dtype=float)
    ok=np.isfinite(y)&np.isfinite(p)
    if int(ok.sum())<5:
        return {"n_valid":int(ok.sum()),"mae":None,"signed_bias":None}
    return {
        "n_valid":int(ok.sum()),
        "mae":round(float(np.mean(np.abs(y[ok]-p[ok]))),6),
        "signed_bias":round(float(np.mean(p[ok]-y[ok])),6),
    }

def validate_event_rates(frame:pd.DataFrame)->dict:
    date=frame.game_date.astype(str)
    train=frame[date<TRAIN_BEFORE]
    select=frame[(date>=TRAIN_BEFORE)&(date<SELECT_BEFORE)]
    cal=frame[(date>=SELECT_BEFORE)&(date<CAL_BEFORE)]
    test=frame[(date>=TEST_FROM)&(date<TEST_TO)]
    if min(len(train),len(select),len(cal),len(test))<100:
        raise ValueError("Need >=100 team-game rows in each chronological stage")
    results={}
    for event,spec in RATE_SPEC.items():
        target=event+"_actual"
        own=event+"_own_prior"
        opp=event+"_opponent_prior"
        def predictions(df,weight):
            return candidate_event_rate(
                df[own].to_numpy(dtype=float),df[opp].to_numpy(dtype=float),
                weight,league_prior=spec["prior"],limits=spec["range"]
            )
        ys=select[target].to_numpy(dtype=float)
        candidates=[]
        for weight in WEIGHTS:
            metrics=_metrics(ys,predictions(select,weight))
            if metrics["n_valid"]<100:
                raise ValueError(f"No sufficient event data: {event}")
            candidates.append({"opponent_weight":weight,**metrics})
        best=min(candidates,key=lambda c:(c["mae"],c["opponent_weight"]))
        base_val=candidates[0]
        chosen=(best["opponent_weight"] if best["mae"]<base_val["mae"]
                else 0.0)
        # Evaluate calibration drift separately without tuning the blend to
        # 2025-26 outcomes. Cal data only diagnostic here, not selection.
        results[event]={
            "validation_candidates":candidates,
            "chosen_on_validation_only":chosen,
            "selected_opponent_weight_before_fallback":best["opponent_weight"],
            "selection_improves_baseline":bool(chosen>0),
            "calibration_period_diagnostic":{
                "own_only":_metrics(cal[target],predictions(cal,0)),
                "candidate":_metrics(cal[target],predictions(cal,chosen)),
            },
            "frozen_holdout":{
                "own_only":_metrics(test[target],predictions(test,0)),
                "candidate":_metrics(test[target],predictions(test,chosen)),
            },
            "input_coverage":{
                "opponent_rate_missing_on_selection":round(
                    float(select[opp].isna().mean()),4),
                "opponent_rate_missing_on_test":round(
                    float(test[opp].isna().mean()),4),
            },
            "predictor_definition":"prior-20-game attack rate blended with opponent prior-20-game allowance",
            "range":list(spec["range"]),
        }
    improvements=sum(
        int(x["frozen_holdout"]["candidate"]["mae"] <
            x["frozen_holdout"]["own_only"]["mae"])
        for x in results.values()
    )
    return {
        "version":VERSION,
        "generated_utc":datetime.now(timezone.utc).isoformat(),
        "counts":{"train":len(train),"selection":len(select),
                  "calibration":len(cal),"test":len(test)},
        "split":{"train_before":TRAIN_BEFORE,
                 "selection_before":SELECT_BEFORE,
                 "calibration_before":CAL_BEFORE,
                 "test_from":TEST_FROM,"test_to":TEST_TO},
        "results":results,
        "holdout_event_rates_with_lower_mae":improvements,
        "available_as_research_candidate":True,
        "production_simulator_changed":False,
        "warnings":[
            "This evaluates single-game team event rates, not full possession simulations or score accuracy.",
            "The 2025-26 holdout has been examined in other GPT v2 work; this is a frozen chronological diagnostic, not a newly pristine final test.",
            "Rate blends selected on validation only; no 2025-26 labels were used for weight selection.",
            "Current-game event targets are joined exclusively AFTER prior game features have been constructed.",
            "Missing defensive allowance columns shrink to predefined league-level priors.",
            "Even lower event-rate MAE does not establish lower win-probability log loss or betting value.",
        ],
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--years",nargs="+",type=int,
                   default=[2022,2023,2024,2025,2026])
    p.add_argument("--output",required=True)
    args=p.parse_args()
    result=validate_event_rates(event_rate_frame(tuple(args.years)))
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print("EVENT_RATE_VALIDATION "+json.dumps({
        "counts":result["counts"],
        "results":{key:{
            "selected_opponent_weight":value["chosen_on_validation_only"],
            "holdout":value["frozen_holdout"],
            "input_coverage":value["input_coverage"]
        } for key,value in result["results"].items()},
        "rates_improved":result["holdout_event_rates_with_lower_mae"]
    },separators=(",",":")),flush=True)

if __name__=="__main__":
    main()
