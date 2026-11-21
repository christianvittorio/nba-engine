"""Reconstruct historical NBA slates from strictly earlier games (retrospective).

Cutoff: Eastern date's 11 AM (typically 16:00 UTC in November).
Use no target-date/after box scores or player appearances for features.
Does NOT recreate injury/lineup snapshots the archive did not capture.
A source retrieved after the target is a corrected historical archive,
NOT proof the features were available at the historical time.

Usage:
 python -m gpt_engine.v2.replay --date 2026-11-20 --n 1000 --output /tmp/replay-nov20.json
 python -m gpt_engine.v2.replay --date 2026-11-18 --n 1000 --output /tmp/replay-nov18.json
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from .contracts import GameContext, iso, utc, display_tip
from .features import build_team_features
from .players import estimate_player, allocate_minutes
from .research import team_parameters
from .simulation import Matchup, simulate_game

REPO_ROOT=Path(__file__).resolve().parents[2]
DATA=REPO_ROOT/"data_foundation"/"artifacts"
VERSION="gpt-v2-possession-research-0.1"
DEFAULT_CUTOFF_ET="11:00"
NBA_TO_ABBREV={}

def historical_source_csv(kind:str, seasons:list[int]) -> pd.DataFrame:
    if kind not in ("teams","players"):
        raise ValueError("Invalid source table")
    frames=[]
    for season in seasons:
        file=DATA/kind/(str(season)+".csv.gz")
        if not file.exists():
            raise FileNotFoundError(file)
        headings=pd.read_csv(file,compression="gzip",nrows=0).columns
        dtype={k:str for k in ("game_id","team_id","opp_team_id","player_id")
               if k in headings}
        d=pd.read_csv(file,compression="gzip",dtype=dtype,low_memory=False)
        if "season" not in d:
            d["season"]=season
        d["season"]=pd.to_numeric(d.season,errors="raise").astype(int)
        d["game_date"]=d.game_date.astype(str).str[:10]
        frames.append(d)
    return pd.concat(frames,ignore_index=True)

def source_schedule(season:int) -> pd.DataFrame:
    from data_foundation.build import read_season
    import duckdb
    con=duckdb.connect()
    try:
        return read_season(con,"schedule",season)
    finally:
        con.close()

def _datetime_cutoff(day:str, hour=11):
    date=datetime.fromisoformat(day)
    if date.tzinfo is not None:raise ValueError("Use Eastern game date only")
    return iso(date.replace(hour=hour,minute=0,second=0,
                            tzinfo=ZoneInfo("America/New_York")))

def _roster(history:pd.DataFrame,team:str,target_day:str,season:int) -> list:
    d=history[(history.team_id.astype(str)==team)&
              (history.game_date.astype(str)<target_day)&
              (history.season.astype(int)<=season)]
    d=d.sort_values(["game_date","game_id"])
    # No latest 'player refresh' snapshots: players are selected from
    # actual historical appearances *strictly before* the target game.
    candidates=d.tail(180).player_id.value_counts().head(12).index.tolist()
    if len(candidates)<8:
        raise ValueError(f"Only {len(candidates)} evidenced prior players for {team}")
    players=[]
    for pid in candidates:
        player_history=d[d.player_id==pid]
        projection=estimate_player(
            player_history,pid,team,target_day,season=season,
            availability="unknown",position="UNKNOWN")
        players.append(projection)
    return allocate_minutes(players)

def _abbrev(teams:pd.DataFrame,raw_team_id:str) -> str:
    rows=teams[teams.team_id.astype(str)==str(raw_team_id)]
    return str(rows.iloc[-1]["team"]) if len(rows) else str(raw_team_id)

def _clock(g):
    return None if pd.isna(g.start_time) else iso(str(g.start_time))

def replay_day(day:str,simulations:int=1000,seed:int=20261120,
               seasons:list[int]|None=None,
               *,include_player_samples=False)->dict:
    if simulations<50:raise ValueError("At least 50 simulations")
    season=int(day[:4])+1 if day[5:7]>="07" else int(day[:4])
    if seasons is None:
        seasons=list(range(2020,season+1))
    if season not in seasons:
        raise ValueError("Current season missing")
    cutoff=_datetime_cutoff(day)
    schedule=source_schedule(season)
    # Only NBA official Eastern date, no converted Manila date.
    scheduled=schedule[(schedule.game_date.astype(str).str[:10]==day) &
                       (schedule.game_id.astype(str).str.zfill(10).str.startswith("002"))].copy()
    if scheduled.empty:
        raise ValueError(f"No regular-season NBA games scheduled for {day}")
    if scheduled.duplicated(["game_id"]).any():
        raise ValueError("Duplicate game IDs in official schedule")
    scheduled=scheduled.sort_values(["start_time","game_id"])
    historical_team=historical_source_csv("teams",seasons)
    historical_player=historical_source_csv("players",seasons)
    prior_team=historical_team[historical_team.game_date<day].copy()
    prior_player=historical_player[historical_player.game_date<day].copy()
    # Leakage detectors: current date or future results must never enter.
    assert (prior_team.game_date<day).all()
    assert (prior_player.game_date<day).all()
    if len(prior_team)==0 or len(prior_player)==0:
        raise ValueError("Insufficient historical data")
    games=[]
    for i,g in enumerate(scheduled.itertuples(index=False)):
        tip=_clock(g)
        if not tip or utc(tip)<=utc(cutoff):
            raise ValueError("Missing/suspicious pregame tip: "+str(g.game_id))
        home=str(g.home_team_id)
        away=str(g.away_team_id)
        game=GameContext("game:nba:"+str(g.game_id).zfill(10),
                         season,day,tip,home,away,
                         False if pd.isna(getattr(g,"neutral_site",None))
                         else bool(getattr(g,"neutral_site")))
        features=build_team_features(prior_team,game,cutoff)
        hp=_roster(prior_player,home,day,season)
        ap=_roster(prior_player,away,day,season)
        f=features.features
        state=Matchup(team_parameters(home,f["home"]),
                      team_parameters(away,f["away"]),
                      max(70.0,min(130.0,float(f["expected_possessions"]))),
                      float(f["home_court_points"]),
                      -1.0 if f["home"].get("b2b") else 0.0,
                      -1.0 if f["away"].get("b2b") else 0.0)
        result=simulate_game(state,hp,ap,n=simulations,
                             seed=seed+i*977,batch_size=250,
                             include_samples=include_player_samples)
        game_result={
            "game_id":game.game_id,
            "date_eastern":day,
            "tip_utc":tip,
            "tip_manila":display_tip(tip,"Asia/Manila"),
            "away":_abbrev(prior_team,away),
            "home":_abbrev(prior_team,home),
            "away_team_id":away,"home_team_id":home,
            "home_win_probability":result["home_win_probability"],
            "away_win_probability":result["away_win_probability"],
            "home_expected_score":result["expected_home_score"],
            "away_expected_score":result["expected_away_score"],
            "expected_total":result["total"]["mean"],
            "total_80pct_interval":result["total"]["interval_80"],
            "margin_80pct_interval":result["margin"]["interval_80"],
            "expected_possessions":round(state.expected_possessions,2),
            "overtime_probability":result["overtime_probability"],
            "mc_win_probability_standard_error":result["mc_sampling_error"]["home_win_probability"],
            "minutes_coverage":sum(p.minutes for p in hp),
            "missing_live_injury_lineups":True,
            "model_version":VERSION,
            "simulation_seed":seed+i*977,
            "model_confidence":"UNVALIDATED_RESEARCH",
        }
        if include_player_samples:
            game_result["player_statistics"]=result["player_statistics"]
        games.append(game_result)
        print("REPLAY_GAME "+json.dumps(game_result,separators=(",",":"),allow_nan=False),flush=True)
    return {
        "kind":"RETROSPECTIVE_PRETIP_RECONSTRUCTION",
        "requested_game_date_eastern":day,
        "cutoff_utc":cutoff,
        "cutoff_us_eastern":day+" "+DEFAULT_CUTOFF_ET+" ET",
        "historical_data_rule":"only game_date strictly before target date",
        "historical_team_games_used":int(prior_team.game_id.nunique()),
        "historical_player_game_rows_used":len(prior_player),
        "historical_archive_was_retrieved_after_cutoff":True,
        "model_version":VERSION,
        "simulations_per_game":simulations,
        "game_count":len(games),
        "games":games,
        "warnings":[
          "Not original forecasts saved on November 20.",
          "Backfilled source archive is corrected later; actual point-in-time snapshot provenance not established.",
          "No source-backed historical pre-tip injury report, confirmed lineups, betting odds, or market states.",
          "Player rotations selected only from earlier appearances; no future player stats, results or playing time.",
          "V2 possession probabilities were not holdout-fitted or calibrated; projections are research-grade only.",
          "This is NOT a validated betting recommendation, and win probabilities can be miscalibrated.",
        ],
    }

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--date",required=True)
    parser.add_argument("--n",type=int,default=1000)
    parser.add_argument("--seed",type=int,default=20261120)
    parser.add_argument("--output",required=True)
    parser.add_argument("--players",action="store_true")
    args=parser.parse_args(argv)
    result=replay_day(args.date,args.n,args.seed,include_player_samples=args.players)
    target=Path(args.output)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("REPLAY_SUMMARY "+json.dumps({k:v for k,v in result.items() if k!="games"},
                                        separators=(",",":")),flush=True)

if __name__=="__main__":
    main()
