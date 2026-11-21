"""Time-ordered NBA training / holdout evaluation from official archived game rows.

Offline retrospective experiment, **not** a record of historical live forecasts.
Never insert reconstructed predictions into the immutable pregame ledger.
The historical archive includes corrected stats and is insufficient by itself
to validate live injury/market timing.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone,timedelta
import hashlib
import json
from pathlib import Path

import pandas as pd

from .contracts import GameContext,iso
from .features import build_team_features,flatten_team_features
from .models import Elo,train_candidates,chronological_split
from .research import history_frame
from .warehouse import connect

FEATURE_DEFINITION="feature-v2.1"
EXPERIMENT_VERSION="gpt-v2-retrospective-challenger-0.1"

def make_experiment_frame(con,train_from="2019-10-01",stop_at="2026-07-01",
                          max_games:int|None=None):
    """Reconstruct features using only games on earlier Eastern dates."""
    team=history_frame(con,"team")
    if team.empty: raise ValueError("No historical game stats")
    game_rows=con.execute(
        "SELECT g.*,r.home_score,r.away_score FROM games g "
        "JOIN actual_results r USING(game_id) "
        "WHERE g.game_type='regular_season' AND g.tip_utc IS NOT NULL "
        "AND g.game_date_eastern>=? AND g.game_date_eastern<? "
        "ORDER BY g.game_date_eastern,g.tip_utc,g.game_id",
        (train_from,stop_at)).fetchall()
    if max_games is not None:
        game_rows=game_rows[:max_games]
    features=[]
    for idx,r in enumerate(game_rows):
        ctx=GameContext(r["game_id"],int(r["season"]),r["game_date_eastern"],
                        r["tip_utc"],r["home_team_id"],r["away_team_id"],
                        bool(r["neutral_site"]))
        # Two hours before scheduled tip, but no same-day game results either.
        cutoff=iso(datetime.fromisoformat(ctx.tip_utc.replace("Z","+00:00"))
                   -timedelta(hours=2))
        try:
            snap=build_team_features(team,ctx,cutoff)
        except ValueError:
            # Insufficient prior history at the beginning of the dataset.
            continue
        item=flatten_team_features(snap)
        item.update({
            "game_id":ctx.game_id,
            "game_date":ctx.game_date_eastern,
            "season":ctx.season,
            "tip_utc":ctx.tip_utc,
            "feature_cutoff_utc":cutoff,
            "home_team_id":ctx.home_team_id,
            "away_team_id":ctx.away_team_id,
            "home_score":int(r["home_score"]),
            "away_score":int(r["away_score"]),
            "neutral_site":bool(r["neutral_site"]),
            "data_status":"retrospective_corrected_not_live_asof",
        })
        features.append(item)
    if not features:
        raise ValueError("No time-valid feature rows could be built")
    return pd.DataFrame(features)

def train_experiment(con,train_before="2024-10-01",
                     validation_before="2025-10-01",
                     *,enable_lightgbm=False,max_games=None)->dict:
    rows=make_experiment_frame(con,max_games=max_games)
    basic={"game_id","game_date","season","tip_utc","feature_cutoff_utc",
           "home_team_id","away_team_id","home_score","away_score",
           "neutral_site","data_status"}
    features=sorted(set(rows.columns)-basic)
    fitted=train_candidates(rows,features,train_before,validation_before,
                            enable_lightgbm)
    train,val,test=chronological_split(rows,train_before,validation_before)
    # Run a separate, honest Elo fallback against the exact same completed games.
    full=rows[["game_id","game_date","season","home_team_id","away_team_id",
               "home_score","away_score","neutral_site"]].copy()
    elo=Elo().pregame_series(full)
    same=elo[elo.game_id.isin(test.game_id)]
    compare=test.merge(same[["game_id","home_win_probability","margin","total"]],
                       on="game_id",validate="one_to_one")
    if len(compare)!=len(test):
        raise ValueError("Elo/test matchup mismatch")
    import numpy as np
    py=compare.home_win_probability.to_numpy()
    truth=(compare.home_score>compare.away_score).to_numpy()
    elo_test={
        "win_brier":round(float(np.mean((py-truth)**2)),5),
        "margin_mae":round(float(np.mean(np.abs(compare.margin-
                               (compare.home_score-compare.away_score)))),5),
        "total_mae":round(float(np.mean(np.abs(compare.total-
                              (compare.home_score+compare.away_score)))),5),
        "winner_accuracy":round(float(np.mean((py>=.5)==truth)),5),
    }
    rows_hash=hashlib.sha256(
        ("\n".join(rows.game_id.astype(str))+"\n"+FEATURE_DEFINITION).encode()
    ).hexdigest()
    return {
        "experiment_version":EXPERIMENT_VERSION,
        "generated_at_utc":iso(datetime.now(timezone.utc)),
        "feature_version":FEATURE_DEFINITION,
        "source_data_status":"historically_corrected_asof_reconstruction",
        "source_games_sha256":rows_hash,
        "selection_data":"validation_only",
        "test_used_for_hyperparameter_selection":False,
        "train_before":train_before,
        "validation_before":validation_before,
        "eligible_games":len(rows),
        "baseline_elo_test":elo_test,
        "chosen_candidate":fitted["selected_kind"],
        "candidate_alpha":fitted["selected_alpha"],
        "candidate_validation_results":fitted["validation_objectives"],
        "candidate_holdout_test":fitted["test_metrics"],
        "n_train":fitted["train_n"],
        "n_validation":fitted["validation_n"],
        "n_test":fitted["test_n"],
        "warnings":[
            "Retrospective corrected stats; no original pre-tip data snapshots.",
            "No historical injury and lineup data in this candidate fit.",
            "This is an academic model comparison, NOT a profitable betting backtest.",
        ]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",required=True)
    p.add_argument("--train-before",default="2024-10-01")
    p.add_argument("--validation-before",default="2025-10-01")
    p.add_argument("--lightgbm",action="store_true")
    p.add_argument("--max-games",type=int,default=None)
    p.add_argument("--output",default="gpt_engine/v2/artifacts/experiments/latest.json")
    args=p.parse_args()
    con=connect(args.db)
    report=train_experiment(con,args.train_before,args.validation_before,
                            enable_lightgbm=args.lightgbm,max_games=args.max_games)
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
