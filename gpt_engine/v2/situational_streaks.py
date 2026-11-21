"""NBA situational *records*, not self-fulfilling streak betting signals.

Predeclared conditions: team x home/away x prior full days off
(0, 1, exactly 2, >=3). This creates 8 cells per team, not an unlimited
search over arbitrary schedules and thresholds.

Every training row is built BEFORE its game result is added to history:
same-day and future wins cannot alter that game's feature. Source records
are corrected historical archives, not originally captured as-of snapshots.

A 21-0 conditional record is NOT an asserted 100% chance of winning:
the condition is selected from many candidates, opponent strength changes,
and teams' rosters/coaches change between seasons. The report provides the
raw 21/21 and a shrinkage estimate, never an invented betting edge.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime
import json
from pathlib import Path

import numpy as np
import pandas as pd

BUCKETS=("0","1","2","3+")
VENUES=("home","away")
VERSION="situational-rest-venue-v1"
LOOKBACK_SEASONS=3
VENUE_PRIOR={"home":.55,"away":.45}
VENUE_PRIOR_GAMES=18.0
CONDITION_PRIOR_GAMES=25.0

NUMERIC_FEATURES=(
    "situation_rest_days","situation_venue_games",
    "situation_venue_prior","situation_sample",
    "situation_win_count","situation_loss_count",
    "situation_raw_win_rate","situation_shrunk_win_rate",
    "situation_edge","situation_low_sample",
)

def rest_bucket(days:int|float|None)->str|None:
    if days is None or pd.isna(days):
        return None
    n=int(days)
    if n<0 or float(days)!=float(n):
        raise ValueError("Rest days must be a nonnegative whole number")
    return str(n) if n<3 else "3+"

def season_from_eastern_date(game_day:str)->int:
    date=datetime.strptime(game_day,"%Y-%m-%d")
    return date.year+1 if date.month>=7 else date.year

def add_finished_game_context(team_games:pd.DataFrame)->pd.DataFrame:
    """Scores only produce historical outcomes; team-based rest is reconstructed.

    Games with ambiguous home/away identity (e.g. neutral-site both marked
    away) are *not* misclassified as normal home wins. Their days may still
    affect subsequent team rest, but not venue conditional win rates.
    """
    required={"game_id","team_id","season","game_date","pts","home"}
    missing=required-set(team_games.columns)
    if missing:
        raise ValueError(f"Missing official source columns: {sorted(missing)}")
    d=team_games.copy()
    d["game_id"]=d.game_id.astype(str).str.zfill(10)
    d["team_id"]=d.team_id.astype(str)
    d["season"]=pd.to_numeric(d.season,errors="raise").astype(int)
    d["game_date"]=d.game_date.astype(str).str[:10]
    if d.duplicated(["game_id","team_id"]).any():
        raise ValueError("Duplicated game/team source record")
    if d.duplicated(["team_id","game_date"]).any():
        raise ValueError("More than one team game on a single Eastern date")
    if (d.groupby("game_id").size()!=2).any():
        raise ValueError("Official NBA game must have two teams")
    d["pts"]=pd.to_numeric(d.pts,errors="raise")
    if d.pts.isna().any():
        raise ValueError("Incomplete game results")
    d["home"] = d.home.astype(str).str.lower().isin(("true","1"))
    d["venue_valid"]=d.groupby("game_id")["home"].transform("sum")==1
    d["venue"]=np.where(d.home,"home","away")
    d["opp_pts"]=d.groupby("game_id")["pts"].transform("sum")-d.pts
    if (d["pts"]==d["opp_pts"]).any():
        raise ValueError("Final NBA game cannot tie")
    d["won"]=(d.pts>d.opp_pts).astype(int)
    d=d.sort_values(["team_id","season","game_date","game_id"]).reset_index(drop=True)
    date=pd.to_datetime(d.game_date,errors="raise")
    previous=d.groupby(["team_id","season"],sort=False).game_date.shift(1)
    days=(date-pd.to_datetime(previous)).dt.days-1
    if (days.dropna()<0).any():
        raise ValueError("Invalid same-day or backwards team schedule")
    d["true_rest_days"]=days.astype(float)
    d["rest_bucket"]=[rest_bucket(v) for v in d.true_rest_days]
    return d

def _summary(history:list[dict],season:int,venue:str,
             bucket:str|None,lookback_seasons:int)->dict:
    if lookback_seasons<1:
        raise ValueError("At least one season of history required")
    if venue not in VENUES:
        raise ValueError("Expected home or away venue")
    eligible=[r for r in history
              if season-lookback_seasons+1<=r["season"]<=season
              and r["venue_valid"] and r["venue"]==venue]
    total=len(eligible)
    venue_wins=sum(r["won"] for r in eligible)
    venue_prior=(venue_wins+VENUE_PRIOR_GAMES*VENUE_PRIOR[venue])/(
        total+VENUE_PRIOR_GAMES)
    conditioned=[r for r in eligible if bucket is not None
                 and r["rest_bucket"]==bucket]
    n=len(conditioned)
    wins=sum(r["won"] for r in conditioned)
    shrunk=(wins+CONDITION_PRIOR_GAMES*venue_prior)/(
        n+CONDITION_PRIOR_GAMES)
    raw=(wins/n if n else None)
    return {
        "venue":venue,"rest_bucket":bucket,"sample":n,
        "wins":wins,"losses":n-wins,
        "raw_win_rate":raw,
        "venue_sample":total,
        "venue_prior":venue_prior,
        "shrunk_win_rate":shrunk,
        "edge":shrunk-venue_prior,
        "low_sample":n<12,
        "lookback_seasons":lookback_seasons,
        "min_season":season-lookback_seasons+1,
        "max_season":season,
    }

def append_pregame_situational_features(team_games:pd.DataFrame,
                                       lookback_seasons:int=LOOKBACK_SEASONS)->pd.DataFrame:
    """Generate leakage-safe historical features on each row.

    Historical games from the TARGET DATE must never be used for its own
    features, and the target game's result is inserted only afterwards.
    """
    d=add_finished_game_context(team_games)
    history=defaultdict(list)
    values={}
    for idx,row in d.sort_values(["game_date","game_id","team_id"]).iterrows():
        venue=str(row.venue)
        bucket=row.rest_bucket
        # An unknown venue or current-season first game without previous
        # rest has *no* conditional-history feature.
        if not row.venue_valid or bucket is None:
            s=_summary(history[str(row.team_id)],int(row.season),venue,
                       None,lookback_seasons)
            s["sample"]=0
            s["wins"]=0
            s["losses"]=0
            s["raw_win_rate"]=None
            s["shrunk_win_rate"]=s["venue_prior"]
            s["edge"]=0.
            s["low_sample"]=True
        else:
            s=_summary(history[str(row.team_id)],int(row.season),venue,
                       bucket,lookback_seasons)
        values[idx]={
            "situation_rest_days":float(row.true_rest_days) if
                not pd.isna(row.true_rest_days) else np.nan,
            "situation_venue_games":float(s["venue_sample"]),
            "situation_venue_prior":float(s["venue_prior"]),
            "situation_sample":float(s["sample"]),
            "situation_win_count":float(s["wins"]),
            "situation_loss_count":float(s["losses"]),
            "situation_raw_win_rate":float(s["raw_win_rate"]) if
                s["raw_win_rate"] is not None else np.nan,
            "situation_shrunk_win_rate":float(s["shrunk_win_rate"]),
            "situation_edge":float(s["edge"]),
            "situation_low_sample":float(s["low_sample"]),
        }
        # Two team rows from same game are independent histories, so their
        # scores cannot affect each other's pregame features.
        history[str(row.team_id)].append({
            "season":int(row.season),
            "game_date":str(row.game_date),"venue":venue,
            "venue_valid":bool(row.venue_valid),
            "rest_bucket":bucket,"won":int(row.won),
        })
    out=d.copy()
    # The chronological loop interleaves two teams while d is grouped by
    # team. Reindex by original source ROW ID rather than assigning insertion
    # order; otherwise home/away records can be silently swapped.
    vals=pd.DataFrame.from_dict(values,orient="index").reindex(out.index)
    if vals.isna().all(axis=1).any():
        raise ValueError("Lost a team-row situational feature identity")
    for col in NUMERIC_FEATURES:
        out[col]=vals[col].to_numpy()
    return out

def current_matching_run(finished:pd.DataFrame,team_id:str,
                         target_day:str,target_season:int,venue:str,
                         rest_days:int,lookback_seasons:int=LOOKBACK_SEASONS)->dict:
    """As-of consecutive wins or losses in the *matching* condition.

    This does not imply a game-by-game overall winning streak: games that
    do not satisfy the condition are skipped. No result from target date
    or later can enter this calculation.
    """
    if venue not in VENUES or not isinstance(rest_days,int) or rest_days<0:
        raise ValueError("Invalid venue/rest")
    source=(add_finished_game_context(finished)
            if "true_rest_days" not in finished else finished)
    d=source[(source.team_id.astype(str)==str(team_id))&
             (source.game_date.astype(str)<target_day)&
             (source.season.astype(int)<=target_season)&
             (source.season.astype(int)>=target_season-lookback_seasons+1)&
             (source.venue_valid)&
             (source.venue==venue)&
             (source.rest_bucket==rest_bucket(rest_days))]
    d=d.sort_values(["game_date","game_id"])
    if d.empty:
        return {"result":None,"length":0,"game_date":None,
                "interpretation":"No matching prior games"}
    last=int(d.iloc[-1].won)
    length=0
    for outcome in reversed(d.won.astype(int).tolist()):
        if outcome!=last:break
        length+=1
    return {
        "result":"win" if last else "loss",
        "length":length,
        "game_date":str(d.iloc[-1].game_date),
        "interpretation":"Consecutive matching-condition games, NOT an overall team win/loss streak"
    }


def matchup_record_asof(finished:pd.DataFrame,team_id:str,
                        target_day:str,target_season:int,venue:str,
                        rest_days:int,lookback_seasons:int=LOOKBACK_SEASONS)->dict:
    """Exact 2-days-off home record as of target game's *start of date*."""
    if venue not in VENUES:
        raise ValueError("Unknown venue")
    if not isinstance(rest_days,int) or rest_days<0:
        raise ValueError("rest_days must be a nonnegative integer")
    source=add_finished_game_context(finished) if "true_rest_days" not in finished else finished
    prior=source[(source.team_id.astype(str)==str(team_id))&
                 (source.game_date.astype(str)<target_day)&
                 (source.season.astype(int)<=target_season)]
    records=[{
        "season":int(r.season),"game_date":str(r.game_date),
        "venue":str(r.venue),"venue_valid":bool(r.venue_valid),
        "rest_bucket":r.rest_bucket,"won":int(r.won),
    } for r in prior.itertuples(index=False)]
    s=_summary(records,target_season,venue,rest_bucket(rest_days),
               lookback_seasons)
    s.update({
        "team_id":str(team_id),"asof_eastern_date":target_day,
        "rest_days_exact":rest_days,
        "quality":"retrospective_corrected_source; exploratory_only",
        "is_betting_probability":False,
        "has_lookahead":False,
    })
    return s

def discover_historical_patterns(finished:pd.DataFrame,target_day:str,
                                 *,lookback_seasons:int=LOOKBACK_SEASONS,
                                 min_games:int=10)->dict:
    """List predeclared venue/rest cells; not every data-mined combination."""
    d=add_finished_game_context(finished)
    if min_games<1:raise ValueError("min_games must be positive")
    season=season_from_eastern_date(target_day)
    earlier=d[(d.game_date<target_day)&
              (d.season<=season)&(d.season>=season-lookback_seasons+1)]
    rows=[]
    for team_id,group in earlier.groupby("team_id"):
        for venue in VENUES:
            for bucket in BUCKETS:
                history=[{
                    "season":int(x.season),"game_date":x.game_date,
                    "venue":x.venue,"venue_valid":bool(x.venue_valid),
                    "rest_bucket":x.rest_bucket,"won":int(x.won)
                } for x in group.itertuples(index=False)]
                s=_summary(history,season,venue,bucket,lookback_seasons)
                if s["sample"]<min_games:
                    continue
                rows.append({
                    "team_id":str(team_id),
                    "team":str(group.iloc[-1].get("team") or team_id),
                    "venue":venue,"rest_condition":(
                        "exactly "+bucket+" full rest days" if bucket!="3+"
                        else "3 or more full rest days"),
                    "rest_bucket":bucket,
                    "wins":s["wins"],"losses":s["losses"],
                    "games":s["sample"],
                    "raw_win_rate":round(s["raw_win_rate"],4),
                    "venue_baseline_rate":round(s["venue_prior"],4),
                    "shrunk_rate":round(s["shrunk_win_rate"],4),
                    "shrunken_edge_vs_team_venue":round(s["edge"],4),
                    "low_sample":s["low_sample"],
                })
    # Sort by raw win rate then sample, but label these as exploratory!
    rows.sort(key=lambda r:(r["raw_win_rate"],r["games"]),reverse=True)
    return {
        "version":VERSION,
        "asof_eastern_date":target_day,
        "seasons_included":[season-lookback_seasons+1,season],
        "season_policy":"current season plus previous two, all games strictly before asof",
        "conditions_per_team":8,
        "pattern_testing":"exploratory predeclared venue/rest combinations, still multiple comparisons",
        "n_tests_up_to":int(8*earlier.team_id.nunique()),
        "min_games":min_games,
        "result_count":len(rows),
        "perfect_records":[x for x in rows if x["losses"]==0],
        "top_patterns":rows[:30],
        "all_patterns":rows,
        "warnings":[
            "Conditional record is NOT an uninterrupted overall win streak.",
            "Streaks chosen from hundreds of cells are subject to multiple-comparison selection bias.",
            "Historical teams and coaches may differ, and opponent strength is not controlled by these descriptive records.",
            "Shrunk rate is a stabilized description, NOT a calibrated win probability or EV.",
            "Unknown rest on each team's first game of a season is not assigned a bucket.",
            "Neutral-site games with ambiguous home designation are excluded from venue streaks.",
            "No same-day or future final scores enter the pattern discovery as-of date.",
        ]
    }

def main(argv=None):
    from .feature_ablation import load_teams
    p=argparse.ArgumentParser()
    p.add_argument("--asof",required=True,help="Eastern calendar date YYYY-MM-DD")
    p.add_argument("--seasons",nargs="+",type=int,required=True)
    p.add_argument("--min-games",type=int,default=10)
    p.add_argument("--output",required=True)
    args=p.parse_args(argv)
    source=load_teams(args.seasons)
    report=discover_historical_patterns(source,args.asof,min_games=args.min_games)
    target=Path(args.output)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        k:v for k,v in report.items() if k not in ("all_patterns","top_patterns")
    },indent=2))
    print("TOP_STREAK_PATTERNS "+json.dumps(report["top_patterns"][:15]))

if __name__=="__main__":
    main()
