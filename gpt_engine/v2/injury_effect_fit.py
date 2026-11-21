"""Timestamp-authenticated injury replacement experiment using Claude's ESPN source.

This fits a *single heavily regularized coefficient* for the effect of
missing expected above-replacement player scoring on game margin.

Historical source snapshots must have been both GENERATED and COMMITTED in
Git before each game's (tip - 60 minutes) cutoff. Player rates use only
game dates strictly earlier than the target. Raw same-day outcomes are
used solely for POST-feature-fit labels and prior-day Elo updates.

This is NOT a verified causal injury impact model. Non-random injuries,
opponent strength, matchup/roster bias and noisy minutes can confound it.
The selected coefficient is never automatically deployed to live bets.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left
from collections import defaultdict
from dataclasses import dataclass
from datetime import timedelta
import json
import math
from pathlib import Path
import subprocess
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from .contracts import iso,utc
from .feature_ablation import read_season_csv
from .models import Elo
from .replay import historical_source_csv,source_schedule
from .shared_availability import _nba_id, normalize_status

EAST=ZoneInfo("America/New_York")
VERSION="gpt-v2-injury-replacement-ridge-0.1"
SOURCE_PATH="nba_engine/artifacts/availability.json"
TRAIN_BEFORE="2026-11-15"
VAL_BEFORE="2026-11-18"
TEST_BEFORE="2026-11-21"
REPLACEMENT_POINTS_PER_MIN=0.37  # predetermined feature definition, not a fitted effect
ELO_LOG_ODDS_PER_POINT=math.log(10)*27/400
MIN_HISTORY_GAMES=3
ALPHAS=(0.0,25.0,100.0,400.0,1600.0)

def _git(root:Path,*args:str)->str:
    return subprocess.check_output(["git","-C",str(root),*args],text=True)

def historical_git_snapshots(root:Path,*,until_utc="2026-11-21T00:00:00Z")->list[dict]:
    """Original Git SHA and commit time are essential to point-in-time validity."""
    listing=_git(root,"log","--format=%H|%cI","--",SOURCE_PATH).splitlines()
    snapshots=[]
    seen=set()
    for line in listing:
        if "|" not in line:continue
        sha,committed=line.split("|",1)
        commit=utc(committed)
        if commit>utc(until_utc):
            continue
        raw=json.loads(_git(root,"show",sha+":"+SOURCE_PATH))
        if not isinstance(raw,dict) or not isinstance(raw.get("teams"),dict):
            continue
        if raw.get("problems") or len(raw["teams"])<28:
            continue
        if not raw.get("generated_utc"):
            continue
        captured=utc(raw["generated_utc"])
        # If source claims the file was created after the commit, it is not
        # authentic as-of evidence even if the injury dates look old.
        if captured>commit or commit-captured>timedelta(hours=4):
            continue
        key=(iso(captured),sha)
        if key in seen:continue
        seen.add(key)
        snapshots.append({
            "commit_sha":sha,
            "generated_utc":iso(captured),
            "committed_utc":iso(commit),
            "teams":raw["teams"],
            "source":raw.get("source"),
        })
    return sorted(snapshots,key=lambda s:(s["committed_utc"],s["generated_utc"]))

def snapshot_for_game(snapshots:list[dict],day:str,tip_utc:str,
                      *,lead_minutes:int=60,max_age_hours:float=12.0)->dict|None:
    """Pick the latest bona fide pre-cutoff commit from the SAME Eastern game date."""
    cutoff=utc(tip_utc)-timedelta(minutes=lead_minutes)
    matched=[]
    for snapshot in snapshots:
        committed=utc(snapshot["committed_utc"])
        captured=utc(snapshot["generated_utc"])
        if committed>cutoff or captured>cutoff or captured>committed:
            continue
        if captured.astimezone(EAST).date().isoformat()!=day:
            continue
        age=(cutoff-captured).total_seconds()/3600
        if 0<=age<=max_age_hours:
            matched.append(snapshot)
    return max(matched,key=lambda x:(x["committed_utc"],x["generated_utc"])) if matched else None

def finished_games(team_games:pd.DataFrame)->pd.DataFrame:
    """NBA regular season from original two-sided box scores."""
    t=team_games.copy()
    t=t[t.game_type.astype(str)=="regular_season"].copy()
    t["game_id"]=t.game_id.astype(str).str.zfill(10)
    t["team_id"]=t.team_id.astype(str)
    t["home"]=t.home.astype(str).str.lower().isin(("true","1"))
    out=[]
    for gid,group in t.groupby("game_id",sort=False):
        if len(group)!=2:
            continue
        h=group[group.home];a=group[~group.home]
        if len(h)!=1 or len(a)!=1:
            # Neutral site archive often records both as away; cannot
            # deduce an actual home designation from team game stats.
            continue
        home=h.iloc[0];away=a.iloc[0]
        out.append({
            "game_id":gid,"season":int(home.season),
            "game_date":str(home.game_date)[:10],
            "home_team_id":str(home.team_id),"away_team_id":str(away.team_id),
            "home":str(home.team),"away":str(away.team),
            "home_score":int(home.pts),"away_score":int(away.pts),
        })
    df=pd.DataFrame(out)
    if df.empty:raise ValueError("No finished NBA game data")
    if df.duplicated("game_id").any():
        raise ValueError("Duplicate game IDs in historic replay")
    return df.sort_values(["season","game_date","game_id"]).reset_index(drop=True)

class PregamePlayerRates:
    """Bisect player histories so target-day statistics are never read."""
    def __init__(self,history:pd.DataFrame):
        self.records={}
        for raw,group in history.groupby("player_id",sort=False):
            d=group.copy()
            d["game_date"]=d.game_date.astype(str).str[:10]
            d["min"]=pd.to_numeric(d["min"],errors="coerce")
            d["pts"]=pd.to_numeric(d["pts"],errors="coerce")
            d=d[(d["min"]>0)&(d["min"]<=53)&d["pts"].notna()]
            d=d.sort_values(["game_date","game_id"])
            if d.empty:continue
            self.records[str(raw)]=(
                d.game_date.to_list(),
                d["min"].astype(float).to_numpy(),
                d.pts.astype(float).to_numpy()
            )

    def pregame_value(self,player_id:str,game_date:str)->tuple[float,str|None,int]:
        record=self.records.get(str(player_id))
        if record is None:
            return 0.0,None,0
        days,mins,pts=record
        idx=bisect_left(days,game_date)
        if idx<MIN_HISTORY_GAMES:
            return 0.0,days[idx-1] if idx else None,idx
        recent=mins[max(0,idx-10):idx]
        long=mins[max(0,idx-40):idx]
        expected_minutes=.70*float(recent.mean())+.30*float(long.mean())
        # Prior 100 player-minutes at a broad league-level per-minute rate.
        last=mins[max(0,idx-30):idx]
        last_pts=pts[max(0,idx-30):idx]
        ppm=(float(last_pts.sum())+100*.42)/(float(last.sum())+100)
        # A scored-at-the-rim replacement is not automatically 0 PPG.
        # Positive, capped ABOVE-replacement value becomes a feature
        # whose multiplier will be fitted exclusively on earlier games.
        value=float(np.clip(expected_minutes*(ppm-REPLACEMENT_POINTS_PER_MIN),
                            0,16))
        return round(value,6),days[idx-1],idx

def team_out_feature(snap:dict,team_code:str,game_date:str,
                     rates:PregamePlayerRates)->dict:
    team=snap["teams"].get(team_code)
    if not team or not team.get("roster"):
        raise ValueError("Archived roster absent for team "+team_code)
    roster={_nba_id(r.get("nba_id")) for r in team["roster"]}
    roster.discard(None)
    names=[]
    missing=[]
    unknown=[]
    values=[]
    latest_dates=[]
    for inj in team.get("injuries",[]):
        status=normalize_status(inj.get("status"))
        if status=="unknown":
            unknown.append(str(inj.get("name") or ""))
        if status!="out":
            continue
        pid=_nba_id(inj.get("nba_id"))
        if pid is None or pid not in roster:
            missing.append(str(inj.get("name") or pid or "unknown"))
            continue
        value,last,n=rates.pregame_value(pid,game_date)
        if last is not None and last>=game_date:
            raise AssertionError("Same-day/future player box score leaked")
        if n<MIN_HISTORY_GAMES:
            missing.append(str(inj.get("name") or pid))
            continue
        values.append(value)
        latest_dates.append(last)
        names.append(str(inj.get("name") or pid))
    return {
        "value":round(float(min(32,sum(values))),6),
        "matched_out_players":len(names),
        "matched_out_names":names,
        "out_missing_history_or_id":missing,
        "uncertain_player_names":unknown,
        "last_player_game_date":max(latest_dates) if latest_dates else None,
        "mapped_roster_count":len(roster),
    }

def historical_feature_rows(root:Path,snapshots:list[dict]|None=None,
                            *,season_years=(2026,2027),
                            lead_minutes=60)->pd.DataFrame:
    if snapshots is None:
        snapshots=historical_git_snapshots(root)
    if not snapshots:
        raise ValueError("No verified historical pretip injury source revisions")
    teams=historical_source_csv("teams",list(season_years))
    players=historical_source_csv("players",list(season_years))
    games=finished_games(teams)
    elo=Elo().pregame_series(games)
    games=games.merge(
        elo[["game_id","home_win_probability","margin"]],
        on="game_id",validate="one_to_one",
    )
    season=max(season_years)
    schedule=source_schedule(season)
    schedule=schedule.copy()
    schedule["game_id"]=schedule.game_id.astype(str).str.zfill(10)
    sch={r.game_id:r for r in schedule.itertuples(index=False)}
    rates=PregamePlayerRates(players)
    source_days=sorted({utc(x["generated_utc"]).astimezone(EAST).date().isoformat()
                       for x in snapshots})
    valid_days=set(source_days)
    out=[]
    missing_schedule=0
    for row in games.itertuples(index=False):
        if int(row.season)!=season or row.game_date not in valid_days:
            continue
        source=sch.get(row.game_id)
        if source is None or pd.isna(source.start_time):
            missing_schedule+=1
            continue
        # Timetable is the authoritative actual home vs away identity.
        if str(source.home_team_id)!=str(row.home_team_id) or \
           str(source.away_team_id)!=str(row.away_team_id):
            raise ValueError(f"Home/away NBA ID mismatch {row.game_id}")
        tip=iso(str(source.start_time))
        snap=snapshot_for_game(snapshots,row.game_date,tip,
                               lead_minutes=lead_minutes)
        if snap is None:continue
        home=team_out_feature(snap,str(row.home),row.game_date,rates)
        away=team_out_feature(snap,str(row.away),row.game_date,rates)
        margin_elo=float(row.margin)
        p_elo=float(row.home_win_probability)
        actual=int(row.home_score)-int(row.away_score)
        out.append({
            "game_id":row.game_id,"game_date":row.game_date,
            "season":int(row.season),
            "home":row.home,"away":row.away,
            "home_score":int(row.home_score),
            "away_score":int(row.away_score),
            "actual_margin":actual,"home_win":int(actual>0),
            "base_margin":margin_elo,"base_p_home":p_elo,
            "net_out_above_replacement":round(away["value"]-home["value"],6),
            "home_out_value":home["value"],"away_out_value":away["value"],
            "home_out_names":home["matched_out_names"],
            "away_out_names":away["matched_out_names"],
            "home_out_unmapped":home["out_missing_history_or_id"],
            "away_out_unmapped":away["out_missing_history_or_id"],
            "home_uncertain_names":home["uncertain_player_names"],
            "away_uncertain_names":away["uncertain_player_names"],
            "home_prior_max_date":home["last_player_game_date"],
            "away_prior_max_date":away["last_player_game_date"],
            "source_sha":snap["commit_sha"],
            "source_generated_utc":snap["generated_utc"],
            "source_committed_utc":snap["committed_utc"],
            "tip_utc":tip,
            "cutoff_utc":iso(utc(tip)-timedelta(minutes=lead_minutes)),
        })
    if not out:
        raise ValueError("No verified pre-tip NBA games matched archived injuries")
    return pd.DataFrame(out).sort_values(["game_date","game_id"]).reset_index(drop=True)

def fit_coefficient(train:pd.DataFrame,alpha:float)->float:
    """Constrained, zero-intercept ridge on Elo pregame margin residuals."""
    x=train.net_out_above_replacement.to_numpy(dtype=float)
    y=(train.actual_margin-train.base_margin).to_numpy(dtype=float)
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Non-finite pregame feature or outcome")
    return float(np.clip(np.dot(x,y)/(np.dot(x,x)+float(alpha)+1e-10),0,1))

def score_frame(frame:pd.DataFrame,beta:float)->dict:
    baseline=frame.base_margin.to_numpy(dtype=float)
    x=frame.net_out_above_replacement.to_numpy(dtype=float)
    actual=frame.actual_margin.to_numpy(dtype=float)
    raw_p=np.clip(frame.base_p_home.to_numpy(dtype=float),1e-6,1-1e-6)
    logit=np.log(raw_p/(1-raw_p))
    shift=beta*x
    adjusted=baseline+shift
    new_p=1/(1+np.exp(-np.clip(logit+shift*ELO_LOG_ODDS_PER_POINT,-30,30)))
    labels=frame.home_win.to_numpy(dtype=int)
    def met(margin,p):
        return {
            "margin_mae":round(float(np.mean(np.abs(margin-actual))),4),
            "winner_accuracy":round(float(np.mean((p>=.5)==labels)),4),
            "win_brier":round(float(np.mean((p-labels)**2)),5),
            "win_log_loss":round(float(np.mean(-labels*np.log(np.clip(p,1e-6,1))-
                                      (1-labels)*np.log(np.clip(1-p,1e-6,1)))),5)
        }
    return {
        "no_injury":met(baseline,raw_p),
        "learned_injury":met(adjusted,new_p),
    }

def _bootstrap_margin_mae_delta(test:pd.DataFrame,beta:float,*,n=500,seed=57)->dict:
    """Day-block bootstrap, not independent-game bootstrap."""
    groups=[g for _,g in test.groupby("game_date",sort=True)]
    rng=np.random.default_rng(seed)
    samples=[]
    def delta(frame):
        x=frame.net_out_above_replacement.to_numpy(dtype=float)
        actual=frame.actual_margin.to_numpy(dtype=float)
        baseline=frame.base_margin.to_numpy(dtype=float)
        return float(np.mean(np.abs(baseline+beta*x-actual)-
                             np.abs(baseline-actual)))
    for _ in range(n):
        selected=rng.integers(len(groups),size=len(groups))
        block=pd.concat([groups[i] for i in selected],ignore_index=True)
        samples.append(delta(block))
    return {
        "injury_minus_no_injury_margin_mae":round(delta(test),4),
        "day_block_bootstrap_95pct_interval":[round(float(x),4)
            for x in np.quantile(samples,[.025,.975])],
        "test_dates":len(groups),
        "warning":"Few held-out dates: a bootstrap interval cannot make this a reliable causal result."
    }

def chronological_experiment(frame:pd.DataFrame)->dict:
    if frame.duplicated("game_id").any():
        raise ValueError("Duplicate game IDs")
    train=frame[frame.game_date<TRAIN_BEFORE].copy()
    validation=frame[(frame.game_date>=TRAIN_BEFORE)&
                     (frame.game_date<VAL_BEFORE)].copy()
    test=frame[(frame.game_date>=VAL_BEFORE)&
               (frame.game_date<TEST_BEFORE)].copy()
    if min(len(train),len(validation),len(test))<10:
        return {
            "status":"INSUFFICIENT_HISTORICAL_PREGAME_SAMPLE",
            "counts":{"train":len(train),"validation":len(validation),
                      "test":len(test)},
            "candidate_live_adoption":False,
            "reason":"Require at least ten labeled game examples in EACH chronological segment",
        }
    # All choices are made on training and validation only. Test labels are
    # not used for model selection.
    candidates=[]
    for alpha in ALPHAS:
        beta=fit_coefficient(train,alpha)
        val=score_frame(validation,beta)
        candidates.append({
            "alpha":alpha,"beta":round(beta,6),
            "validation":val,
            "validation_margin_mae":val["learned_injury"]["margin_mae"],
        })
    chosen=min(candidates,key=lambda c:(c["validation_margin_mae"],
                                         abs(c["beta"]),c["alpha"]))
    beta=float(chosen["beta"])
    # Preserve zero/no-effect fallback whenever val does not favor a correction.
    baseline_val=score_frame(validation,0)["no_injury"]["margin_mae"]
    if chosen["validation_margin_mae"]>=baseline_val:
        beta=0
    scored=score_frame(test,beta)
    matched=int((frame.net_out_above_replacement!=0).sum())
    return {
        "status":"RESEARCH_FIT_COMPLETED_NOT_PRODUCTION_APPROVED",
        "version":VERSION,
        "feature_definition":"difference of previous-game estimated unavailable points above replacement",
        "fixed_replacement_per_min":REPLACEMENT_POINTS_PER_MIN,
        "training":f"dates < {TRAIN_BEFORE}",
        "validation":f"{TRAIN_BEFORE} <= date < {VAL_BEFORE}",
        "evaluation":f"{VAL_BEFORE} <= date < {TEST_BEFORE}",
        "counts":{
            "train":len(train),"validation":len(validation),"test":len(test),
            "matched_nonzero_injury_feature_games":matched,
            "source_git_commits":int(frame.source_sha.nunique()),
            "dates_with_games":int(frame.game_date.nunique())
        },
        "selected_from_validation_only":{
            "candidates":candidates,
            "selected_alpha":chosen["alpha"],
            "raw_selected_beta":chosen["beta"],
            "effective_beta":beta,
            "zero_fallback_used":bool(beta==0),
            "validation_baseline_margin_mae":baseline_val,
        },
        "frozen_test":scored,
        "uncertainty":_bootstrap_margin_mae_delta(test,beta),
        "limitations":[
            "Only October 31–November 20, 2026 original source revisions exist in this Git history.",
            "Nov 18 results were previously inspected; the last three days are chronological evaluation, NOT an untouched research holdout.",
            "The same injuries can be confounded with underlying team strength and coaching choices.",
            "Injured players with no valid pregame NBA ID or previous minutes are excluded, not fabricated.",
            "Day-to-day is UNKNOWN; only status Out yields an absent player feature.",
            "No genuine confirmed starting fives or earlier multi-year injury history.",
            "Elo probabilities are not calibrated specifically for this small injury-adjusted sample.",
        ],
        "candidate_live_adoption":False,
        "forecasting_changes_deployed":False,
    }

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--repo",default=".")
    p.add_argument("--output",required=True)
    p.add_argument("--games-output",default=None)
    args=p.parse_args(argv)
    root=Path(args.repo).resolve()
    snapshots=historical_git_snapshots(root)
    frame=historical_feature_rows(root,snapshots)
    report=chronological_experiment(frame)
    report.update({
        "historical_source_revision_count":len(snapshots),
        "first_source_commit_utc":min(s["committed_utc"] for s in snapshots),
        "last_source_commit_utc":max(s["committed_utc"] for s in snapshots),
        "eligible_game_rows":len(frame),
        "source_cutoff_policy":"latest same-day source snapshot whose generated and commit times precede tipoff minus 60 min",
        "source_provenance":"Original Claude bot's Git availability.json revisions",
    })
    dest=Path(args.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    if args.games_output:
        Path(args.games_output).parent.mkdir(parents=True,exist_ok=True)
        frame.to_json(args.games_output,orient="records",indent=2)
    print(json.dumps(report,indent=2,allow_nan=False))

if __name__=="__main__":
    main()
