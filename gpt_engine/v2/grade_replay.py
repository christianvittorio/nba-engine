"""Grade an immutable historical injury replay AFTER forecasting is complete.

Actual November 18 scores are opened only by this separate command after
the simulation JSON already exists. Never modify the original forecast JSON.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from .replay import historical_source_csv

def grade_report(data:dict,actual_source=None)->dict:
    if data["kind"]!="RETROSPECTIVE_GAME_DAY_WITH_AUTHENTIC_HISTORIC_ESPN_INJURIES":
        raise ValueError("Expected source-authenticated injury replay")
    day=data["date_eastern"]
    year=int(day[:4])+1 if day[5:7]>="07" else int(day[:4])
    actual=actual_source if actual_source is not None else historical_source_csv("teams",[year])
    actual=actual[actual.game_date.astype(str)==day]
    lookup={}
    for game,df in actual.groupby("game_id"):
        lookup[str(game).zfill(10)]={str(row.team_id):int(row.pts)
                                      for row in df.itertuples(index=False)}
    rows=[]
    for rec in data["games"]:
        gid=rec["game_id"].replace("game:nba:","")
        scores=lookup.get(gid)
        if scores is None or len(scores)!=2:
            raise ValueError("Missing/twice-counted final score for "+gid)
        h,a=rec["home_team_id"],rec["away_team_id"]
        if h not in scores or a not in scores:
            raise ValueError("Final team's identity mismatch for "+gid)
        sh,sa=scores[h],scores[a]
        truth=int(sh>sa)
        if sh==sa:raise ValueError("Cannot grade tied final NBA game")
        row={
            "game_id":rec["game_id"],"away":rec["away"],"home":rec["home"],
            "actual_away_score":sa,"actual_home_score":sh,
            "actual_total":sa+sh,
            "actual_margin_home":sh-sa,
            "winner_actual":rec["home"] if truth else rec["away"]
        }
        for label,ref in (("without_injury","base_model"),
                          ("with_claude_injury","asof_claude_injury")):
            forecast=rec[ref]
            p=float(forecast["home_win_probability"])
            row[label]={
                "predicted_away":round(float(forecast["away_expected_score"]),1),
                "predicted_home":round(float(forecast["home_expected_score"]),1),
                "predicted_winner":rec["home"] if p>=0.5 else rec["away"],
                "predicted_winner_probability":round(max(p,1-p),4),
                "correct_winner":int((p>=.5)==truth),
                "total_absolute_error":round(abs(float(forecast["expected_total"])-(sh+sa)),2),
                "margin_absolute_error":round(abs(float(forecast["expected_margin"])-(sh-sa)),2),
                "home_win_probability":p
            }
        rows.append(row)
    metrics={}
    for label in ("without_injury","with_claude_injury"):
        pp=np.asarray([row[label]["home_win_probability"] for row in rows])
        yy=np.asarray([int(row["winner_actual"]==row["home"]) for row in rows])
        eps=np.clip(pp,1e-5,1-1e-5)
        metrics[label]={
            "correct_picks":int(sum(r[label]["correct_winner"] for r in rows)),
            "n_games":len(rows),
            "winner_accuracy":round(float(np.mean((pp>=.5)==yy)),4),
            "win_brier":round(float(np.mean((pp-yy)**2)),5),
            "win_log_loss":round(float(np.mean(-yy*np.log(eps)-(1-yy)*np.log(1-eps))),5),
            "total_mae":round(float(np.mean([r[label]["total_absolute_error"] for r in rows])),3),
            "margin_mae":round(float(np.mean([r[label]["margin_absolute_error"] for r in rows])),3),
        }
    out={
        "scoring_stage":"POST_FORECAST_GRADE_ONLY",
        "replay_source_commit":data["original_git_commit_sha"],
        "cutoff_utc":data["cutoff_utc"],
        "original_forecast_untouched":True,
        "grade_uses_actual_results_only_after_the_predictions_were_saved":True,
        "metrics":metrics,
        "rows":rows,
        "warning":"One slate cannot prove model improvement, statistical significance, probability calibration or positive betting ROI."
    }
    for row in rows:
        print("GRADED_REPLAY_ROW "+json.dumps(row,separators=(",",":")),flush=True)
    print("GRADED_SUMMARY "+json.dumps(metrics,separators=(",",":")),flush=True)
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--forecast",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    data=json.loads(Path(a.forecast).read_text(encoding="utf-8"))
    graded=grade_report(data)
    path=Path(a.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(graded,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
