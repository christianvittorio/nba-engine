"""Source-backed, research-only live game runner for GPT NBA v2.

Run from repository root after ingesting historical seasons:
  python -m gpt_engine.v2.ingest --seasons 2020 2021 2022 2023 2024 2025 2026 2027 --output /tmp/nba-v2.sqlite
  python -m gpt_engine.v2.research --db /tmp/nba-v2.sqlite --date 2026-11-21 --n 1000

This never overwrites prior forecasts. No games after their sourced tipoffs.
Candidate players are *historical recent participants*, not confirmed starters.
When real pregame injury data is missing, player projections are conditional
and carry explicit warnings. Do NOT use these outputs to place bets.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

import pandas as pd

from .contracts import GameContext, Prediction, display_tip, iso
from .features import build_team_features
from .players import estimate_player,allocate_minutes
from .simulation import TeamSettings,Matchup,simulate_game
from .warehouse import connect,asof_availability,asof_lineup,save_snapshot,save_model_version,save_prediction

VERSION="gpt-v2-research-0.1"
ROOT=Path(__file__).resolve().parents[2]
REPORTS=ROOT/"gpt_engine"/"v2"/"artifacts"/"reports"

def history_frame(con,kind):
    if kind=="team":
        rows=con.execute(
            "SELECT g.game_id,g.season,g.game_date_eastern,g.game_type,"
            "s.team_id,s.stats_json FROM team_game_stats s JOIN games g USING(game_id)"
            " WHERE g.status='final'").fetchall()
    elif kind=="player":
        rows=con.execute(
            "SELECT g.game_id,g.season,g.game_date_eastern,"
            "s.player_id,s.team_id,s.stats_json FROM player_game_stats s "
            "JOIN games g USING(game_id) WHERE g.status='final'").fetchall()
    else:
        raise ValueError("Expected team or player history")
    values=[]
    for r in rows:
        d=json.loads(r["stats_json"])
        d.update({"game_id":r["game_id"],"season":int(r["season"]),
                  "game_date":r["game_date_eastern"],"team_id":r["team_id"]})
        if kind=="team":
            d["game_type"]=r["game_type"]
            if d.get("opp_team_id") and not str(d["opp_team_id"]).startswith("team:"):
                d["opp_team_id"]="team:nba:"+str(d["opp_team_id"])
        else:d["player_id"]=r["player_id"]
        values.append(d)
    return pd.DataFrame(values)

def team_parameters(team_id,vec):
    def bounded(name,prior,lo,hi):
        return max(lo,min(hi,float(vec.get(name,prior))))
    pace=bounded("rolling20_pace",99,75,125)
    return TeamSettings(
        team_id=team_id,
        offense_rating=bounded("opponent_adjusted_off_rating",114,70,155),
        defense_rating=bounded("rolling20_def_rating",114,70,155),
        three_attempt_rate=bounded("rolling20_three_point_rate",.38,.20,.65),
        turnover_probability=bounded("rolling20_tov",13,4,25)/pace,
        offensive_rebound_probability=bounded("rolling20_oreb_pct",.26,.14,.48),
        free_throw_trip_probability=bounded("rolling20_fta_rate",.24,.10,.48)*.58
    )

def estimate_rotation(hist,team,day,season,status):
    prior=hist[(hist.team_id.astype(str)==team)&
               (hist.game_date.astype(str)<day)&
               (hist.season.astype(int)<=season)].sort_values(["game_date","game_id"])
    # Only recent actual participants are provisional candidates. This can miss
    # players acquired today, so it is explicitly NOT a validated lineup.
    candidates=prior.tail(180).player_id.value_counts().head(12).index.tolist()
    if len(candidates)<8:
        raise ValueError("Fewer than 8 evidenced recent player participants")
    parts=[]
    for pid in candidates:
        parts.append(estimate_player(prior[prior.player_id==pid],pid,team,day,
                    season=season,availability=status.get(pid,"unknown")))
    return allocate_minutes(parts)

def run_day(db_path:str,day:str,n:int=1000,seed:int=20261121):
    now=iso(datetime.now(timezone.utc))
    con=connect(db_path)
    games=con.execute("SELECT * FROM games WHERE game_date_eastern=? "
                      "AND status='scheduled' AND tip_utc>? ORDER BY tip_utc,game_id",
                      (day,now)).fetchall()
    if not games:
        return []
    team_data=history_frame(con,"team")
    player_data=history_frame(con,"player")
    if team_data.empty or player_data.empty:
        raise ValueError("Missing source-backed game/player history")
    save_model_version(con,VERSION,"possession_events_experimental",{
        "calibration":"not_yet_holdout_calibrated",
        "availability":"asof_or_unknown",
        "mc_target":10000
    })
    outcomes=[]
    for row in games:
        gc=GameContext(row["game_id"],int(row["season"]),row["game_date_eastern"],
                       row["tip_utc"],row["home_team_id"],row["away_team_id"],
                       bool(row["neutral_site"]))
        avail=asof_availability(con,gc.game_id,now)
        lineups=asof_lineup(con,gc.game_id,now)
        known={r["player_id"]:r["normalized_status"] for r in avail}
        snap=build_team_features(team_data,gc,now,availability=avail,lineup=lineups)
        try:
            hp=estimate_rotation(player_data,gc.home_team_id,day,gc.season,known)
            ap=estimate_rotation(player_data,gc.away_team_id,day,gc.season,known)
        except ValueError as error:
            print("SKIPPED "+gc.game_id+": "+str(error),flush=True)
            continue
        state=snap.features
        match=Matchup(
            team_parameters(gc.home_team_id,state["home"]),
            team_parameters(gc.away_team_id,state["away"]),
            max(70,min(130,float(state["expected_possessions"]))),
            float(state["home_court_points"]),
            -1.0 if state["home"].get("b2b") else 0.0,
            -1.0 if state["away"].get("b2b") else 0.0
        )
        sim=simulate_game(match,hp,ap,n=n,seed=seed)
        quality=list(snap.quality_flags)+[
            "UNVALIDATED_RESEARCH_MODEL",
            "recent_participants_not_confirmed_lineup",
            "absence_of_live_injury_report_requires_conditional_interpretation",
        ]
        sid=save_snapshot(con,snap,generated_at_utc=now)
        pred=Prediction(gc.game_id,sid,VERSION,now,now,"recent_participants_conditional",{
            "home_win_probability":sim["home_win_probability"],
            "expected_home_score":sim["expected_home_score"],
            "expected_away_score":sim["expected_away_score"],
            "total":sim["total"],
            "player_statistics":sim["player_statistics"],
            "quality_flags":quality,
        })
        try:pid=save_prediction(con,pred)
        except sqlite3.IntegrityError:
            # Same cutoff previously saved. Respect immutable claims.
            continue
        con.execute(
            "INSERT INTO simulation_summaries(simulation_id,prediction_id,seed,"
            "simulation_count,batch_size,parameters_json,summary_json,"
            "sample_error_json,created_at_utc) VALUES(?,?,?,?,?,?,?,?,?)",
            (pid+":sim",pid,seed,n,500,
             json.dumps({"scenario":"recent_participants_conditional"}),
             json.dumps({k:v for k,v in sim.items() if k!="player_statistics"}),
             json.dumps(sim["mc_sampling_error"]),now)
        )
        con.commit()
        REPORTS.mkdir(parents=True,exist_ok=True)
        report=REPORTS/(day+"_"+gc.game_id.replace(":","-")+".json")
        report.write_text(json.dumps({
            "game_id":gc.game_id,"tip_utc":gc.tip_utc,
            "tip_manila":display_tip(gc.tip_utc),
            "cutoff_utc":now,"model_version":VERSION,"prediction_id":pid,
            "result":sim,"quality_flags":quality,
            "betting_recommendation":False,
        },indent=2)+"\n",encoding="utf-8")
        outcomes.append({
            "game_id":gc.game_id,"prediction_id":pid,
            "home_win_probability":sim["home_win_probability"],
            "home_score":sim["expected_home_score"],
            "away_score":sim["expected_away_score"],
            "quality":"RESEARCH_UNCALIBRATED",
        })
    con.close()
    return outcomes

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--db",required=True)
    parser.add_argument("--date",required=True)
    parser.add_argument("--n",type=int,default=1000)
    parser.add_argument("--seed",type=int,default=20261121)
    a=parser.parse_args()
    print(json.dumps(run_day(a.db,a.date,a.n,a.seed),indent=2))

if __name__=="__main__":
    main()
