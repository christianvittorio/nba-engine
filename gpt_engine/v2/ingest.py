"""Ingest source-backed NBA foundation archives into the normalized SQLite schema.

Historical stats are marked *retrospective corrected archive*. A record
downloaded after tip can train retrospective features if its game occurred
earlier than the target, but cannot serve as a contemporaneous injury or
lineup confirmation or create a fake historically live forecast.

Run from repo root:
  python -m gpt_engine.v2.ingest --seasons 2027 --output /tmp/nba-v2.sqlite
  python -m gpt_engine.v2.ingest --seasons 2020 2021 ... 2027 --output /tmp/nba-v2.sqlite

The optional 1.7M tracked matchups remain in verified Parquet by default;
--include-tracking materializes them into SQLite, which can exceed GitHub's
single-file size limit. Never commit this full binary SQLite database.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Any

import numpy as np
import pandas as pd

from .contracts import Provenance,iso,internal_id,canonical_json
from .warehouse import connect, register_source
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data_foundation"/"artifacts"


def _clean(x:Any):
    if isinstance(x,(np.integer,)):return int(x)
    if isinstance(x,(np.floating,)):return float(x) if np.isfinite(x) else None
    if isinstance(x,np.bool_):return bool(x)
    if isinstance(x,(pd.Timestamp,datetime)):return x.isoformat()
    if isinstance(x,(dict,list,tuple)):return [_clean(v) for v in x] if not isinstance(x,dict) else {k:_clean(v) for k,v in x.items()}
    if x is None:return None
    try:
        if pd.isna(x):return None
    except (TypeError,ValueError):
        pass
    if isinstance(x,(str,int,float,bool)):
        if isinstance(x,float) and not np.isfinite(x):return None
        return x
    return str(x)

def _json_record(row:pd.Series,except_fields:set[str]):
    return canonical_json({str(k):_clean(v) for k,v in row.items()
                           if k not in except_fields})

def load_file(folder:str,season:int)->pd.DataFrame:
    if not 1997<=season<=2100:
        raise ValueError("Invalid season")
    p=DATA/folder/f"{season}.csv.gz"
    if not p.exists():
        raise FileNotFoundError(p)
    # Object IDs are identifiers, never floats or truncated NBA IDs.
    cols=pd.read_csv(p,compression="gzip",nrows=0).columns
    dtype={k:str for k in cols if k in {"game_id","team_id","opp_team_id",
                 "player_id","coach_id","def_team_id","off_person_id","def_person_id"}}
    result=pd.read_csv(p,compression="gzip",dtype=dtype,low_memory=False)
    if result.empty:
        raise ValueError(f"No {folder} data for {season}")
    return result

def source_schedule(season:int)->pd.DataFrame:
    """Official NBA schedule: preserves true UTC tip-offs, never guesses midnight."""
    import duckdb
    from data_foundation.build import read_season
    con=duckdb.connect()
    try:
        d=read_season(con,"schedule",season)
    finally:
        con.close()
    needed={"game_id","game_date","start_time","home_team_id","away_team_id"}
    if not needed<=set(d):
        raise ValueError(f"Schedule lacks required columns {needed-set(d)}")
    return d

def _safe_date(x)->str:
    return str(x)[:10]

def _game_id(x)->str:
    return internal_id("game","nba",str(x).zfill(10))

def _team_id(x)->str:
    return internal_id("team","nba",str(x))

def _player_id(x)->str:
    return internal_id("player","nba",str(x))

def _coach_id(x)->str:
    return internal_id("coach","nba",str(x))

def ingest_season(con:sqlite3.Connection,season:int, *, schedule:pd.DataFrame,
                  include_tracking:bool=False)->dict:
    if not 1997<=season<=2100:raise ValueError("Season out of range")
    teams=load_file("teams",season)
    players=load_file("players",season)
    rosters=load_file("rosters",season)
    coaches=load_file("coaches",season)
    needed={"game_id","team_id","team","home","pts","game_date","game_type"}
    if not needed<=set(teams):
        raise ValueError("Team game archive malformed")
    if set(players.game_id.astype(str))-set(teams.game_id.astype(str)):
        raise ValueError("Player history references unknown games")
    if teams.duplicated(["game_id","team_id"]).any():
        raise ValueError("Duplicate team/game rows")
    if not {"game_id","game_date","start_time","home_team_id","away_team_id"}<=set(schedule):
        raise ValueError("No verified tipoff-bearing schedule")
    retrieved=iso(datetime.now(timezone.utc))
    historic_flags=canonical_json(["corrected_historical_archive",
                                  "not_point_in_time_capture"])
    current_flags=canonical_json(["source_retrieved_at_ingestion"])
    # One transaction: partial seasons are rolled back on failed validation.
    with con:
        name_map={}
        for row in teams[["team_id","team"]].drop_duplicates().itertuples(index=False):
            name_map[str(row.team_id)]=str(row.team)
        for season_row in rosters.itertuples(index=False):
            name_map.setdefault(str(season_row.team_id),str(season_row.team_id))
        schedule_teams=set(schedule.home_team_id.dropna().astype(str))|set(
            schedule.away_team_id.dropna().astype(str))
        for raw in sorted(set(name_map)|schedule_teams):
            con.execute("INSERT OR IGNORE INTO teams(team_id,current_name,created_at_utc)"
                        " VALUES(?,?,?)",(_team_id(raw),name_map.get(raw),retrieved))
            con.execute("INSERT OR IGNORE INTO provider_ids VALUES(?,?,?,?,?,?)",
                        ("team",_team_id(raw),"nba_stats_archive",raw,retrieved,"[]"))
        known_players=set(players.player_id.dropna().astype(str))|set(
            rosters.player_id.dropna().astype(str))
        # Published roster names are labels, not identity keys.
        roster_names={}
        if "player" in rosters:
            for rr in rosters[["player_id","player"]].dropna().itertuples(index=False):
                roster_names.setdefault(str(rr.player_id),str(rr.player))
        for raw in sorted(known_players):
            con.execute("INSERT OR IGNORE INTO players(player_id,canonical_name,created_at_utc)"
                        " VALUES(?,?,?)",(_player_id(raw),roster_names.get(raw),retrieved))
            con.execute("INSERT OR IGNORE INTO provider_ids VALUES(?,?,?,?,?,?)",
                        ("player",_player_id(raw),"nba_stats_archive",raw,retrieved,"[]"))
        # Index official scheduled home/away BEFORE resolving neutral-site box
        # scores: NBA logs may mark both sides 'away' at neutral venues.
        schedule_rows={}
        for row in schedule.itertuples(index=False):
            gid=str(row.game_id).zfill(10)
            if gid in schedule_rows:
                raise ValueError(f"Duplicate NBA schedule game {gid}")
            schedule_rows[gid]=row
        actual_games={}
        for raw,group in teams.groupby("game_id"):
            if len(group)!=2:
                raise ValueError(f"Expected two official team rows for NBA game {raw}")
            gid=str(raw).zfill(10)
            sched=schedule_rows.get(gid)
            if sched is None or pd.isna(sched.home_team_id) or pd.isna(sched.away_team_id):
                raise ValueError(f"Missing sourced home/away identity for finished game {gid}")
            home=group[group.team_id.astype(str)==str(sched.home_team_id)]
            away=group[group.team_id.astype(str)==str(sched.away_team_id)]
            if len(home)!=1 or len(away)!=1:
                raise ValueError(f"Team identities do not reconcile against schedule for {gid}")
            actual_games[gid]=(home.iloc[0],away.iloc[0])
        for gid,(home,away) in actual_games.items():
            if gid not in schedule_rows:
                raise ValueError(f"Archived finished game absent in official schedule: {gid}")
            sched=schedule_rows[gid]
            if str(sched.home_team_id)!=str(home.team_id) or str(sched.away_team_id)!=str(away.team_id):
                raise ValueError(f"Schedule team mismatch for {gid}")
        for gid,sch in schedule_rows.items():
            if pd.isna(sch.home_team_id) or pd.isna(sch.away_team_id):
                continue  # unscheduled playoff TBD, not a real named matchup
            internal=_game_id(gid)
            tip=iso(sch.start_time) if not pd.isna(sch.start_time) else None
            is_final=gid in actual_games
            date_eastern=_safe_date(sch.game_date)
            game_type=("regular_season" if gid[:3]=="002" else
                       "playoffs" if gid[:3]=="004" else
                       "play_in" if gid[:3]=="005" else
                       "cup_final" if gid[:3]=="006" else "other")
            status="final" if is_final else "scheduled"
            # Preserve official neutral-site designation rather than giving
            # pandemic bubble/Paris games an invented home-court advantage.
            raw_neutral=getattr(sch,"neutral_site",None)
            neutral=0 if raw_neutral is None or pd.isna(raw_neutral) else int(bool(raw_neutral))
            if is_final:
                boxhome,boxaway=actual_games[gid]
                # Score identity reconciliation against official source.
                if (int(boxhome.pts)!=2*int(boxhome.fgm)+int(boxhome.fg3m)+int(boxhome.ftm) or
                    int(boxaway.pts)!=2*int(boxaway.fgm)+int(boxaway.fg3m)+int(boxaway.ftm)):
                    raise ValueError(f"Scoring identity failure in {gid}")
            con.execute(
                "INSERT INTO games(game_id,season,game_date_eastern,tip_utc,home_team_id,"
                "away_team_id,game_type,neutral_site,status,source_id,source_timestamp,retrieved_at_utc,"
                "quality_flags_json) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) "
                "ON CONFLICT(game_id) DO UPDATE SET tip_utc=excluded.tip_utc,"
                "neutral_site=excluded.neutral_site,status=excluded.status,"
                "retrieved_at_utc=excluded.retrieved_at_utc",
                (internal,season,date_eastern,tip,_team_id(sch.home_team_id),
                 _team_id(sch.away_team_id),game_type,neutral,status,"nba_schedule",
                 str(sch.start_time) if tip else None,retrieved,
                 historic_flags if is_final else current_flags)
            )
            con.execute("INSERT OR IGNORE INTO provider_ids VALUES(?,?,?,?,?,?)",
                        ("game",internal,"nba_stats_archive",gid,retrieved,"[]"))
            if is_final:
                h,a=actual_games[gid]
                con.execute(
                    "INSERT INTO actual_results(game_id,season,home_score,away_score,"
                    "source_id,source_timestamp,retrieved_at_utc,quality_flags_json)"
                    " VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(game_id) DO NOTHING",
                    (internal,season,int(h.pts),int(a.pts),"nba_stats_archive",
                     str(sch.start_time) if tip else None,retrieved,historic_flags)
                )
        # All observed box scores and lineup stints remain separate from
        # pre-tip status/lineup reports (which require genuine timestamps).
        exclude={"season","game_id","team_id","team","opp","game_type"}
        for _,row in teams.iterrows():
            con.execute(
                "INSERT OR IGNORE INTO team_game_stats(game_id,team_id,season,stats_json,"
                "source_id,source_timestamp,retrieved_at_utc,quality_flags_json)"
                " VALUES(?,?,?,?,?,?,?,?)",
                (_game_id(row.game_id),_team_id(row.team_id),season,
                 _json_record(row,exclude),"nba_stats_archive",
                 str(row.game_date),retrieved,historic_flags)
            )
        excluded_player={"season","game_id","player_id","team_id","team",
                         "opp","position","position_quality","game_type"}
        for _,row in players.iterrows():
            con.execute(
                "INSERT OR IGNORE INTO player_game_stats(game_id,player_id,team_id,season,"
                "stats_json,source_id,source_timestamp,retrieved_at_utc,quality_flags_json)"
                " VALUES(?,?,?,?,?,?,?,?,?)",
                (_game_id(row.game_id),_player_id(row.player_id),_team_id(row.team_id),
                 season,_json_record(row,excluded_player),"nba_stats_archive",
                 str(row.game_date),retrieved,historic_flags)
            )
        for _,r in rosters.iterrows():
            if pd.isna(r.get("player_id")) or pd.isna(r.get("team_id")):
                continue
            con.execute(
                "INSERT INTO roster_assignments(player_id,team_id,season,source_id,"
                "retrieved_at_utc,published_position,quality_flags_json)"
                " VALUES(?,?,?,?,?,?,?)",
                (_player_id(r.player_id),_team_id(r.team_id),season,
                 "sportsdataverse",retrieved,
                 None if pd.isna(r.get("position")) else str(r.position),
                 canonical_json(["season_roster_only","start_end_dates_unknown"]))
            )
        for _,r in coaches.iterrows():
            if pd.isna(r.get("coach_id")) or pd.isna(r.get("team_id")):
                continue
            cid=_coach_id(r.coach_id)
            con.execute("INSERT OR IGNORE INTO coaches(coach_id,coach_name,created_at_utc)"
                        " VALUES(?,?,?)",
                        (cid,str(r.coach_name),retrieved))
            con.execute("INSERT OR IGNORE INTO provider_ids VALUES(?,?,?,?,?,?)",
                        ("coach",cid,"sportsdataverse",str(r.coach_id),retrieved,"[]"))
            con.execute("INSERT INTO coach_tenures(team_id,coach_id,role,season,source_id,"
                        "retrieved_at_utc,quality_flags_json) VALUES(?,?,?,?,?,?,?)",
                        (_team_id(r.team_id),cid,str(r.coach_type),season,
                         "sportsdataverse",retrieved,
                         canonical_json(["season_staff_membership_only",
                                         "game_level_tenure_dates_unverified"])))
        observed_matchups=0
        if include_tracking:
            import duckdb
            p=DATA/"player_defender_matchups"/f"{season}.parquet"
            if not p.exists():raise FileNotFoundError(p)
            c=duckdb.connect()
            tracked=c.execute("SELECT * FROM read_parquet(?)",[str(p)]).df()
            c.close()
            for idx,row in tracked.iterrows():
                gid=_game_id(row.game_id)
                if con.execute("SELECT 1 FROM games WHERE game_id=?",(gid,)).fetchone() is None:
                    raise ValueError(f"Unknown matchup game {gid}")
                # Use a source-row offset instead of assuming pair rows are unique.
                kwargs=lambda name:None if pd.isna(row.get(name)) else str(row[name])
                ofp=kwargs("off_person_id");dfp=kwargs("def_person_id")
                for rawpid in (ofp,dfp):
                    if rawpid and con.execute("SELECT 1 FROM players WHERE player_id=?",
                                (_player_id(rawpid),)).fetchone() is None:
                        con.execute("INSERT INTO players(player_id,created_at_utc) VALUES(?,?)",
                                    (_player_id(rawpid),retrieved))
                con.execute(
                    "INSERT INTO tracking_matchups(game_id,observation_id,offensive_player_id,"
                    "defensive_player_id,offensive_team_id,defensive_team_id,observed_position,"
                    "partial_possessions,minutes,stats_json,source_id,retrieved_at_utc,"
                    "quality_flags_json) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (gid,str(idx),_player_id(ofp) if ofp else None,
                     _player_id(dfp) if dfp else None,
                     _team_id(row.off_team_id),_team_id(row.def_team_id),
                     kwargs("off_position"),
                     _clean(row.get("partial_possessions")),
                     _clean(row.get("matchup_minutes_sort")),
                     _json_record(row,{"game_id","season","game_date"}),
                     "sportsdataverse",retrieved,
                     canonical_json(["tracked_matchup_not_exclusive_defender_causality"]))
                )
                observed_matchups+=1
    return {
        "season":season,"games_in_official_schedule":len(schedule_rows),
        "final_games":len(actual_games),
        "team_game_stat_rows":len(teams),
        "player_game_stat_rows":len(players),
        "roster_rows":len(rosters),"coach_staff_rows":len(coaches),
        "tracking_rows_materialized":observed_matchups,
        "retrieved_at_utc":retrieved
    }

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--seasons",nargs="+",type=int,default=[2027])
    parser.add_argument("--output",default="/tmp/nba-gpt-v2.sqlite")
    parser.add_argument("--include-tracking",action="store_true")
    args=parser.parse_args(argv)
    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    con=connect(output)
    register_source(con,"nba_stats_archive","Official NBA historical stats",
                    "https://basketball-data.billmill.org/nba/",
                    "Confirm commercial redistribution permissions")
    register_source(con,"nba_schedule","Official NBA schedule",
                    "https://basketball-data.billmill.org/nba/stats/schedule")
    register_source(con,"sportsdataverse","SportsDataverse NBA history",
                    "https://github.com/sportsdataverse/sportsdataverse-data")
    reports=[]
    for season in sorted(set(args.seasons)):
        report=ingest_season(con,season,schedule=source_schedule(season),
                             include_tracking=args.include_tracking)
        reports.append(report)
        print(json.dumps(report),flush=True)
    con.close()
    print(f"Initialized v2 research SQLite warehouse at {output}; "
          "DO NOT commit full SQLite files to public GitHub.")

if __name__=="__main__":
    main()
