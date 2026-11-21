"""Optional on-demand NBA play-by-play and rotation ingestion.

The public NBA archive publishes game_events and game_rotations by season.
These may be millions of rows, so the default historical ingestion does not
materialize them into a huge SQLite database. They remain directly queryable
from source Parquet; this loader can materialize selected games on demand.

Important: action 'time' is elapsed GAME time, not a UTC clock timestamp.
We preserve it as clock_seconds and do not invent a wall-clock event_utc.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import json
import sqlite3

import pandas as pd
from .contracts import iso,canonical_json
from .ingest import _clean,_game_id,_team_id,_player_id,source_schedule
from .warehouse import connect

BASE="https://basketball-data.billmill.org/nba/stats"
def read_source(dataset:str,season:int,games:list[str]|None=None)->pd.DataFrame:
    if dataset not in ("game_events","game_rotations"):
        raise ValueError("Only verified source event tables are supported")
    if not 1997<=season<=2100:raise ValueError("Invalid season")
    import duckdb
    db=duckdb.connect()
    url=f"{BASE}/{dataset}/season={season}/data.parquet"
    if games:
        normalized=[str(g).replace("game:nba:","").zfill(10) for g in games]
        # Parameterized list, no user-generated SQL fragment.
        rows=db.execute("SELECT * FROM read_parquet(?) WHERE game_id IN "
                        "(SELECT unnest(?::VARCHAR[]))",[url,normalized]).df()
    else:
        rows=db.execute("SELECT * FROM read_parquet(?)",[url]).df()
    db.close()
    return rows

def import_events(con:sqlite3.Connection,season:int,games:list[str],include_rotations=True)->dict:
    if not games:
        raise ValueError("Supply explicit game IDs to avoid importing millions unintentionally")
    event_rows=read_source("game_events",season,games)
    if event_rows.empty:
        raise ValueError("No NBA event records for requested games")
    rotations=read_source("game_rotations",season,games) if include_rotations else pd.DataFrame()
    timestamp=iso(datetime.now(timezone.utc))
    counts={"events":0,"rotation_stints":0,"season":season,"games_requested":len(games)}
    with con:
        for _,r in event_rows.iterrows():
            gid=_game_id(r.game_id)
            if con.execute("SELECT 1 FROM games WHERE game_id=?",(gid,)).fetchone() is None:
                raise ValueError(f"Unregistered game: {gid}")
            tid=None if pd.isna(r.get("team_id")) else _team_id(r.team_id)
            pid=None if pd.isna(r.get("person_id")) else _player_id(r.person_id)
            if tid and con.execute("SELECT 1 FROM teams WHERE team_id=?",(tid,)).fetchone() is None:
                tid=None
            if pid and con.execute("SELECT 1 FROM players WHERE player_id=?",(pid,)).fetchone() is None:
                pid=None  # source may identify a coach or another non-player
            clock=_clean(r.get("time"))
            # A game clock is not wall clock time.
            event_type=None if pd.isna(r.get("action_type")) else str(r.action_type)
            if not event_type:event_type="unknown"
            details=canonical_json({str(k):_clean(v) for k,v in r.items()})
            con.execute(
                "INSERT OR IGNORE INTO play_by_play(game_id,action_id,period,clock_seconds,"
                "team_id,player_id,event_type,event_json,source_id,retrieved_at_utc,"
                "quality_flags_json) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (gid,str(r.action_id),_clean(r.get("period")),clock,tid,pid,
                 event_type,details,"nba_stats_archive",timestamp,
                 canonical_json(["archive_not_original_live_event_stream"]))
            )
            counts["events"]+=1
        if include_rotations:
            for _,r in rotations.iterrows():
                gid=_game_id(r.game_id)
                pid=_player_id(r.player_id)
                tid=_team_id(r.team_id)
                registered=con.execute("SELECT 1 FROM players WHERE player_id=?",(pid,)).fetchone()
                if registered is None:continue
                # Some players have multiple stints with the same in_time;
                # deterministic order within each player's source rows.
                con.execute(
                    "INSERT OR IGNORE INTO rotation_stints(game_id,player_id,team_id,"
                    "stint_index,in_elapsed_seconds,out_elapsed_seconds,"
                    "on_court_points_for,source_id,retrieved_at_utc,quality_flags_json)"
                    " VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (gid,pid,tid,int(r["_source_stint_index"]),float(r.in_time),
                     float(r.out_time),_clean(r.get("pts")),
                     "nba_stats_archive",timestamp,
                     canonical_json(["matches_box_score="+str(r.get("matches_box_score"))])))
                )
                counts["rotation_stints"]+=1
    return counts

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",required=True)
    p.add_argument("--season",type=int,required=True)
    p.add_argument("--game-ids",nargs="+",required=True)
    p.add_argument("--without-rotations",action="store_true")
    a=p.parse_args()
    conn=connect(a.db)
    result=import_events(conn,a.season,a.game_ids,not a.without_rotations)
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
