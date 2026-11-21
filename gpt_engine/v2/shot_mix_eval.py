"""Historical opt-in player shot-mix Monte Carlo benchmark, never live promotion.

Uses only earlier team/player games to generate projections; actual FG3A,
3PM, FTA and final team scores are read strictly AFTER both simulations
have finished for each game. Source is a corrected retrospective archive,
not an original point-in-time injury/lineup/roster snapshot.
"""
from __future__ import annotations
import argparse,json
from datetime import datetime,timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .contracts import GameContext,iso,utc
from .features import build_team_features
from .replay import (
    _roster,_datetime_cutoff,historical_source_csv,source_schedule
)
from .research import team_parameters
from .simulation import Matchup,simulate_game

VERSION="player-shot-mix-out-of-time-smoke-0.1"

def evaluate_shot_mix(*,start="2026-02-01",end="2026-02-08",
                      max_games=16,n=120,seed=61)->dict:
    if not start<end or n<50 or max_games<1:
        raise ValueError("Expected valid historical interval and simulation size")
    current=2026
    years=[2024,2025,2026]
    teams=historical_source_csv("teams",years)
    players=historical_source_csv("players",years)
    schedule=source_schedule(current)
    schedule["game_id"]=schedule.game_id.astype(str).str.zfill(10)
    scheduled=schedule[
        (schedule.game_date.astype(str)>=start)&
        (schedule.game_date.astype(str)<end)&
        (schedule.game_id.str.startswith("002"))
    ].sort_values(["game_date","start_time","game_id"]).head(max_games)
    if scheduled.empty:raise ValueError("No historical games in selected interval")
    outcomes=teams.copy()
    outcomes["game_id"]=outcomes.game_id.astype(str).str.zfill(10)
    actual_players=players.copy()
    actual_players["game_id"]=actual_players.game_id.astype(str).str.zfill(10)
    records=[]
    skipped=[]
    for i,g in enumerate(scheduled.itertuples(index=False)):
        day=str(g.game_date)[:10]
        tip=iso(str(g.start_time))
        cutoff=_datetime_cutoff(day)
        if utc(cutoff)>=utc(tip):
            skipped.append({"game_id":g.game_id,"reason":"Tip at/before cutoff"})
            continue
        prior_t=teams[teams.game_date.astype(str)<day]
        prior_p=players[players.game_date.astype(str)<day]
        if not (prior_t.game_date.astype(str)<day).all() or \
           not (prior_p.game_date.astype(str)<day).all():
            raise AssertionError("Same day or future stats in forecast")
        home=str(g.home_team_id);away=str(g.away_team_id)
        context=GameContext("game:nba:"+str(g.game_id).zfill(10),
                            current,day,tip,home,away,
                            bool(getattr(g,"neutral_site",False)))
        try:
            snap=build_team_features(prior_t,context,cutoff)
            hp=_roster(prior_p,home,day,current)
            ap=_roster(prior_p,away,day,current)
            vec=snap.features
            match=Matchup(
                team_parameters(home,vec["home"]),
                team_parameters(away,vec["away"]),
                max(70.0,min(130.0,float(vec["expected_possessions"]))),
                float(vec["home_court_points"]),
                -1.0 if vec["home"].get("b2b") else 0.,
                -1.0 if vec["away"].get("b2b") else 0.,
            )
        except (ValueError,KeyError) as ex:
            skipped.append({"game_id":g.game_id,"reason":str(ex)})
            continue
        original=simulate_game(match,hp,ap,n=n,seed=seed+i*199,batch_size=120)
        challenger=simulate_game(match,hp,ap,n=n,seed=seed+i*199,batch_size=120,
                                 event_model="player_shot_mix")
        # Only now open the corresponding current-game target labels.
        score=outcomes[outcomes.game_id.astype(str).str.zfill(10)==g.game_id]
        box=actual_players[actual_players.game_id==g.game_id]
        if len(score)!=2:
            skipped.append({"game_id":g.game_id,"reason":"Missing paired final scores"})
            continue
        sh=score[score.team_id.astype(str)==home]
        sa=score[score.team_id.astype(str)==away]
        if len(sh)!=1 or len(sa)!=1:
            skipped.append({"game_id":g.game_id,"reason":"Wrong final team IDs"})
            continue
        truth_h=float(sh.iloc[0].pts)
        truth_a=float(sa.iloc[0].pts)
        actual_stat={}
        for raw in box.itertuples(index=False):
            pid=str(raw.player_id)
            if pid not in actual_stat:
                actual_stat[pid]={
                    "fg3a":float(raw.fg3a),
                    "fg3m":float(raw.fg3m),
                    "fta":float(raw.fta),
                }
        players_in_projection=[p.player_id for p in hp+ap]
        if len(players_in_projection)!=len(set(players_in_projection)):
            raise ValueError("Duplicate projected player ID across teams")
        stats={}
        for key in ("fg3a","fg3m","fta"):
            actual=np.asarray([actual_stat.get(pid,{}).get(key,0)
                               for pid in players_in_projection],dtype=float)
            stats[key]={
                model:round(float(np.mean(np.abs(np.asarray([
                    forecast["player_statistics"][pid][key]["mean"]
                    for pid in players_in_projection
                ])-actual))),5)
                for model,forecast in (("baseline",original),
                                       ("player_shot_mix",challenger))
            }
        scores={}
        for model,forecast in (("baseline",original),
                               ("player_shot_mix",challenger)):
            scores[model]={
                "total_error":round(abs(float(forecast["total"]["mean"])-
                                      (truth_h+truth_a)),4),
                "margin_error":round(abs(float(forecast["margin"]["mean"])-
                                       (truth_h-truth_a)),4),
                "home_win_probability":float(forecast["home_win_probability"]),
            }
        records.append({
            "game_id":g.game_id,"date_eastern":day,
            "score_errors":scores,
            "player_stat_mae":stats,
            "projected_players":len(players_in_projection),
            "observed_same_player_id_appearances":sum(
                int(p in actual_stat) for p in players_in_projection),
        })
        print("SHOT_MIX_GAME "+json.dumps({
            "id":g.game_id,"date":day,"player_mae":stats,
            "score_error":scores
        },separators=(",",":")),flush=True)
    if len(records)<8:
        raise ValueError(f"Not enough grounded games for shot-mix smoke: {len(records)}")
    aggregate={}
    for target in ("fg3a","fg3m","fta"):
        aggregate[target]={
            model:round(float(np.mean([
                row["player_stat_mae"][target][model] for row in records])),5)
            for model in ("baseline","player_shot_mix")
        }
    for target in ("total_error","margin_error"):
        aggregate[target]={
            model:round(float(np.mean([
                row["score_errors"][model][target] for row in records])),4)
            for model in ("baseline","player_shot_mix")
        }
    report={
        "version":VERSION,
        "interval":[start,end],
        "target_games_requested":len(scheduled),
        "matched_games":len(records),
        "simulations_per_game_and_scenario":n,
        "aggregate_mean_per_game_errors":aggregate,
        "per_game":records,
        "skipped":skipped,
        "deployment":{
            "daily_model_unchanged":True,
            "automatic_promotion":False,
        },
        "limitations":[
            "Small 8–16 game retrospective smoke test, not statistically powered.",
            "Historical corrected NBA boxscores; original historical injury/starting five snapshots unavailable.",
            "Projected players are previous-participant candidates, not confirmed starters.",
            "Players without same-game minutes are scored as zero for all actual counting stats.",
            "Both variants use the same seed but consume different RNG draws after event assignment.",
            "No original pregame sportsbook comparison, causal lineup effects or evaluated profitability.",
        ],
    }
    return report

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--start",default="2026-02-01")
    p.add_argument("--end",default="2026-02-08")
    p.add_argument("--n",type=int,default=120)
    p.add_argument("--max-games",type=int,default=16)
    p.add_argument("--output",required=True)
    a=p.parse_args(argv)
    r=evaluate_shot_mix(start=a.start,end=a.end,max_games=a.max_games,n=a.n)
    path=Path(a.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(r,indent=2,allow_nan=False)+"\n")
    print("SHOT_MIX_SUMMARY "+json.dumps({
        "games":r["matched_games"],
        "aggregate":r["aggregate_mean_per_game_errors"]
    },separators=(",",":")),flush=True)

if __name__=="__main__":
    main()
