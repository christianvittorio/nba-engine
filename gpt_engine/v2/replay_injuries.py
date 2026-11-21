"""Replay an actual NBA slate with Claude's HISTORICALLY ARCHIVED ESPN injury feed.

This is a *reconstructed* pre-tip forecast. Only games before the target
Eastern calendar date are used for team and player stats. A saved, pre-tip
Claude-source availability.json is read but Claude's predictions, coefficients
and game results are never imported. The same player pool and random seed
are used for an injury-blind and an injury-adjusted forecast per matchup.

Example (run on GitHub Actions with the archived snapshot from git show):
 python -m gpt_engine.v2.replay_injuries \
     --date 2026-11-18 --cutoff-utc 2026-11-18T22:00:00Z \
     --claude-snapshot /tmp/claude-nov18-availability.json \
     --source-commit bef881fc0722a22291a35f304feba29ea4ad9656 \
     --n 1000 --output /tmp/nov18-claude-injury-replay.json

Warning: the v2 possession simulator and roster substitution impact are
research heuristics, NOT validated sportsbook probabilities.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from datetime import datetime
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .contracts import GameContext, utc, iso, display_tip
from .features import build_team_features
from .players import estimate_player, allocate_minutes, conditional_rotation
from .research import team_parameters
from .scenarios import _adjusted_team
from .shared_availability import compact_snapshot
from .simulation import Matchup,simulate_game
from .replay import historical_source_csv,source_schedule,_abbrev,_clock

MODEL="gpt-v2-possession-research-0.1+claude-asof-espn"

def _select_roster(history:pd.DataFrame,team_id:str,team_code:str,
                   day:str,season:int,espn_team:dict)->tuple:
    """Use Claude's *historically captured* roster, not today's roster."""
    source_roster=espn_team.get("roster") or []
    official_ids={str(p["nba_id"]) for p in source_roster if p.get("nba_id")}
    known=history[(history.team_id.astype(str)==team_id)&
                  (history.game_date.astype(str)<day)&
                  (history.season.astype(int)<=season)].copy()
    known=known.sort_values(["game_date","game_id"])
    if not official_ids:
        raise ValueError(f"Missing source-backed roster for {team_code}")
    # Keep only athlete IDs that existed on the 2026-11-18 pregame roster.
    known=known[known.player_id.astype(str).isin(official_ids)]
    candidates=known.tail(220).player_id.value_counts().head(12).index.tolist()
    if len(candidates)<8:
        raise ValueError(
            f"Only {len(candidates)} evidenced pre-cutoff rotation players for {team_code}")
    roster=[]
    for pid in candidates:
        roster.append(estimate_player(known[known.player_id==pid],pid,team_id,day,
                                     season=season,availability="unknown",
                                     position="UNKNOWN"))
    return allocate_minutes(roster),set(candidates),{
        "historical_roster_entries":len(source_roster),
        "mapped_positive_nba_id_entries":len(official_ids),
        "roster_candidates_with_prior_games":len(candidates),
        "unmatched_roster_names":sum(1 for p in source_roster if not p.get("nba_id"))
    }

def _injury_conditions(espn_team:dict,candidates:set[str])->tuple[dict,list,list]:
    status={}
    out=[]
    uncertain=[]
    seen=set()
    for injury in espn_team.get("injuries") or []:
        id_=injury.get("nba_id")
        if id_ is None:
            continue  # Never use ESPN-only placeholder IDs as NBA IDs.
        pid=str(id_)
        if pid not in candidates:
            continue
        if pid in seen:
            raise ValueError("Duplicate ESPN injury for the same team/player")
        seen.add(pid)
        s=injury["normalized_status"]
        name=str(injury.get("name") or pid)
        if s=="out":
            status[pid]="out"
            out.append(name)
        elif s=="doubtful":
            # A conditional doubtful-out scenario is shown separately; there
            # is no empirical probability or promise the player sat.
            uncertain.append({"player":name,"status":"doubtful"})
        elif s in ("questionable","unknown"):
            uncertain.append({"player":name,"status":s,
                              "raw":injury.get("provider_status","")})
        elif s in ("probable","confirmed_available"):
            status[pid]=s
    return status,sorted(out),uncertain

def _numbers(sim:dict)->dict:
    return {
        "home_win_probability":sim["home_win_probability"],
        "away_win_probability":sim["away_win_probability"],
        "home_expected_score":sim["expected_home_score"],
        "away_expected_score":sim["expected_away_score"],
        "expected_total":sim["total"]["mean"],
        "expected_margin":sim["margin"]["mean"],
        "total_80pct_interval":sim["total"]["interval_80"],
        "margin_80pct_interval":sim["margin"]["interval_80"],
        "overtime_probability":sim["overtime_probability"],
        "mc_win_probability_standard_error":sim["mc_sampling_error"]["home_win_probability"],
    }

def replay_with_claude_injury(day:str,cutoff_utc:str,snapshot_path:str,
                             source_commit:str,simulations:int=1000,
                             seed:int=20261118,seasons:list[int]|None=None,
                             *,include_player_statistics:bool=False)->dict:
    if simulations<50:
        raise ValueError("Minimum 50 simulations per forecast")
    cutoff=iso(cutoff_utc)
    raw=json.loads(Path(snapshot_path).read_text(encoding="utf-8"))
    snapshot=compact_snapshot(raw,cutoff_utc=cutoff,max_age_hours=12)
    captured=snapshot["generated_utc"]
    if not source_commit or len(source_commit)!=40 or not all(
        c in "0123456789abcdef" for c in source_commit.lower()
    ):
        raise ValueError("Historical Git commit SHA required to authenticate snapshot")
    season=int(day[:4])+1 if day[5:7]>="07" else int(day[:4])
    if seasons is None:
        seasons=list(range(2020,season+1))
    scheduled=source_schedule(season)
    scheduled=scheduled[
        (scheduled.game_date.astype(str).str[:10]==day)&
        (scheduled.game_id.astype(str).str.zfill(10).str.startswith("002"))
    ].sort_values(["start_time","game_id"])
    if len(scheduled)!=len(set(scheduled.game_id)):
        raise ValueError("Duplicate official game schedule row")
    if not len(scheduled):
        raise ValueError("No regular season slate on target date")
    times=[_clock(g) for g in scheduled.itertuples(index=False)]
    if any(tip is None or utc(cutoff)>=utc(tip) or utc(captured)>=utc(tip)
           for tip in times):
        raise ValueError("Injury snapshot or cutoff is at/after an actual game tipoff")
    if str(datetime.fromisoformat(day).date())!=day:
        raise ValueError("Malformed game date")
    source_day=utc(captured).astimezone(
        __import__("zoneinfo").ZoneInfo("America/New_York")).date().isoformat()
    if source_day!=day:
        raise ValueError("Archived injury snapshot is not from the requested game day")
    team=historical_source_csv("teams",seasons)
    player=historical_source_csv("players",seasons)
    prior_team=team[(team.game_date<day)&
                    (team.game_type=="regular_season")].copy()
    prior_player=player[player.game_date<day].copy()
    assert prior_team.game_date.max()<day
    assert prior_player.game_date.max()<day
    results=[]
    for i,g in enumerate(scheduled.itertuples(index=False)):
        gid=str(g.game_id).zfill(10)
        tip=times[i]
        home_id,away_id=str(g.home_team_id),str(g.away_team_id)
        home_code=_abbrev(prior_team,home_id)
        away_code=_abbrev(prior_team,away_id)
        if home_code not in snapshot["teams"] or away_code not in snapshot["teams"]:
            raise ValueError("Missing Claude injury/roster team "+home_code+"/"+away_code)
        context=GameContext("game:nba:"+gid,season,day,tip,home_id,away_id,
             False if pd.isna(getattr(g,"neutral_site",None))
             else bool(getattr(g,"neutral_site")))
        base_features=build_team_features(prior_team,context,cutoff)
        h_base,h_ids,h_info=_select_roster(
            prior_player,home_id,home_code,day,season,snapshot["teams"][home_code])
        a_base,a_ids,a_info=_select_roster(
            prior_player,away_id,away_code,day,season,snapshot["teams"][away_code])
        h_status,h_out,h_uncertain=_injury_conditions(
            snapshot["teams"][home_code],h_ids)
        a_status,a_out,a_uncertain=_injury_conditions(
            snapshot["teams"][away_code],a_ids)
        f=base_features.features
        matchup=Matchup(
            team_parameters(home_id,f["home"]),
            team_parameters(away_id,f["away"]),
            max(70.0,min(130.0,float(f["expected_possessions"]))),
            float(f["home_court_points"]),
            -1.0 if f["home"].get("b2b") else 0.0,
            -1.0 if f["away"].get("b2b") else 0.0
        )
        both_status={**h_status,**a_status}
        h_adjusted=conditional_rotation(h_base,h_status)
        a_adjusted=conditional_rotation(a_base,a_status)
        injury_match=replace(
            matchup,
            home=_adjusted_team(matchup.home,h_base,h_adjusted,matchup.expected_possessions),
            away=_adjusted_team(matchup.away,a_base,a_adjusted,matchup.expected_possessions),
        )
        rng_seed=seed+i*977
        baseline=simulate_game(matchup,h_base,a_base,
                               n=simulations,seed=rng_seed,batch_size=250)
        injured=simulate_game(injury_match,h_adjusted,a_adjusted,
                              n=simulations,seed=rng_seed,batch_size=250)
        if abs(sum(p.minutes for p in h_adjusted)-240)>1e-3 or \
           abs(sum(p.minutes for p in a_adjusted)-240)>1e-3:
            raise ValueError("Injury replacement minutes do not reconcile")
        # There is no retroactive fitting to how these games turned out:
        # both counterfactuals use identical pre-tip team/player history.
        record={
            "game_id":"game:nba:"+gid,
            "game_date_eastern":day,
            "tip_utc":tip,
            "tip_manila":display_tip(tip),
            "away":away_code,"home":home_code,
            "away_team_id":away_id,"home_team_id":home_id,
            "source_capture_utc":captured,
            "base_model":_numbers(baseline),
            "asof_claude_injury":_numbers(injured),
            "delta_home_win_probability":round(
                injured["home_win_probability"]-baseline["home_win_probability"],4),
            "delta_total":round(injured["total"]["mean"]-baseline["total"]["mean"],2),
            "injury_labels_applied":{
                "home_out":h_out,"away_out":a_out,
                "home_uncertain":h_uncertain,"away_uncertain":a_uncertain,
                "home_matched_status_count":len(h_status),
                "away_matched_status_count":len(a_status),
            },
            "pregame_roster":{home_code:h_info,away_code:a_info},
            "team_minutes_after_injuries":{
                home_code:round(sum(p.minutes for p in h_adjusted),5),
                away_code:round(sum(p.minutes for p in a_adjusted),5)
            },
            "warning":"Source-confirmed Out statuses only; day-to-day status is unknown. Usage replacement and score response are uncalibrated research heuristics.",
            "model_version":MODEL,
            "simulation_seed":rng_seed,
        }
        if include_player_statistics:
            record["injury_adjusted_player_stats"]={
                pid:{
                    "minutes":stat["minutes"]["mean"],
                    "pts":stat["pts"]["mean"],
                    "reb":stat["reb"]["mean"],
                    "ast":stat["ast"]["mean"],
                    "fg3m":stat["fg3m"]["mean"],
                    "tov":stat["tov"]["mean"],
                    "availability":stat["availability"],
                    "sample_games":stat["sample_games"],
                    "quality_flags":stat["quality_flags"],
                } for pid,stat in injured["player_statistics"].items()
            }
        results.append(record)
        print("ASOF_REPLAY_GAME "+json.dumps(record,separators=(",",":")),flush=True)
    return {
        "kind":"RETROSPECTIVE_GAME_DAY_WITH_AUTHENTIC_HISTORIC_ESPN_INJURIES",
        "date_eastern":day,
        "cutoff_utc":cutoff,
        "original_source_generated_utc":captured,
        "original_git_commit_sha":source_commit,
        "source":"Claude's HISTORICAL ESPN injury roster observations, not its predictions",
        "historic_data_policy":"team and player boxscores strictly before target Eastern date",
        "current_game_results_consulted":False,
        "official_starters_confirmed":False,
        "player_uncertainty":"day-to-day unknown; conditional alternative availability scenarios needed",
        "game_count":len(results),
        "simulations_per_game_per_scenario":simulations,
        "simulated_scenarios_per_game":2,
        "games":results,
        "warnings":[
            "The injury data was archived by Claude BEFORE each scheduled tip, verified by Git commit and generated_utc.",
            "Team and player historical stats remain retrospective corrected archives rather than original immutable dated copies.",
            "Only source-mapped existing rotation players change playing status; unmatched and out-of-rotation injuries cannot be resolved.",
            "The prior game rotation contains only athletes with prior team games; current unknown debutants can be missed.",
            "Not confirmed starting lineups, and no probabilistic scenarios for day-to-day statuses.",
            "Possession/event and replacement-value simulation parameters are not rigorously holdout calibrated.",
            "Never treat a better score on this single slate as evidence of a profitable betting strategy."
        ]
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--date",required=True)
    parser.add_argument("--cutoff-utc",required=True)
    parser.add_argument("--claude-snapshot",required=True)
    parser.add_argument("--source-commit",required=True)
    parser.add_argument("--n",type=int,default=1000)
    parser.add_argument("--seed",type=int,default=20261118)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    result=replay_with_claude_injury(
        args.date,args.cutoff_utc,args.claude_snapshot,
        args.source_commit,args.n,args.seed
    )
    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("ASOF_REPLAY_SUMMARY "+json.dumps({
        k:v for k,v in result.items() if k!="games"
    },separators=(",",":")),flush=True)

if __name__=="__main__":
    main()
