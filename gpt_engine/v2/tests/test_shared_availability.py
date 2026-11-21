"""Tests for honest Claude-source sharing, as-of timestamps and status semantics."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory

import pytest

from gpt_engine.v2.shared_availability import (
    SOURCE, normalize_status, compact_snapshot, capture_snapshot,
    latest_asof_archive, ingest_availability_snapshot
)
from gpt_engine.v2.contracts import Provenance
from gpt_engine.v2.warehouse import (
    connect, register_source, register_team, register_player,
    upsert_game, asof_availability, asof_lineup
)

GAME="game:nba:0022600400"
TIP="2026-11-22T01:00:00Z"
CAPTURE="2026-11-21T18:00:00Z"
NOW="2026-11-21T20:00:00Z"

def warehouse():
    con=connect()
    register_source(con,"nba_stats_archive","NBA official archive")
    register_source(con,"nba_schedule","Official schedule")
    register_team(con,"team:nba:1","ATL")
    register_team(con,"team:nba:2","BKN")
    for n in ("101","102","103"):
        register_player(con,"player:nba:"+n,"Athlete "+n)
    upsert_game(con,GAME,2027,"2026-11-21",TIP,
                "team:nba:1","team:nba:2","scheduled",
                Provenance("nba_schedule",CAPTURE))
    for team in ("team:nba:1","team:nba:2"):
        con.execute("INSERT INTO team_game_stats(game_id,team_id,season,stats_json,"
                    "source_id,retrieved_at_utc) VALUES(?,?,?,?,?,?)",
                    (GAME,team,2027,"{}","nba_stats_archive",CAPTURE))
    con.commit()
    return con

def shared_source():
    return {
        "generated_utc":CAPTURE,"source":"ESPN public JSON (unofficial)",
        "teams":{
            "ATL":{
                "roster":[
                    {"espn_id":"8901","nba_id":101,"name":"A","pos":"F"},
                    {"espn_id":"8902","nba_id":102,"name":"B","pos":"G"},
                    {"espn_id":"8999","nba_id":-8999,"name":"Unmatched","pos":"C"}
                ],
                "injuries":[
                    {"nba_id":101,"name":"A","status":"Out",
                     "date":"2026-11-20T08:00Z"},
                    {"nba_id":102,"name":"B","status":"Day-To-Day",
                     "date":"2026-11-20T19:00Z"},
                    {"nba_id":-8999,"name":"Unmatched","status":"Out",
                     "date":"2026-11-21T16:00Z"}
                ],
            },
            "BKN":{
                "roster":[{"espn_id":"8801","nba_id":103,"name":"C","pos":"G"}],
                "injuries":[{"nba_id":103,"name":"C","status":"Probable",
                             "date":"2026-11-20T09:00Z"}]
            },
        },
        "problems":[],
    }

def test_statuses_are_conservative():
    assert normalize_status("Out")=="out"
    assert normalize_status("DOUBTFUL")=="doubtful"
    assert normalize_status("Questionable")=="questionable"
    assert normalize_status("Day-To-Day")=="unknown"
    assert normalize_status("Active")=="unknown"
    assert normalize_status("Probable")=="probable"
    assert normalize_status("Workout")=="unknown"

def test_compact_uses_capture_time_not_original_injury_date():
    compact=compact_snapshot(shared_source(),cutoff_utc=NOW)
    assert compact["generated_utc"]==CAPTURE
    assert compact["teams"]["ATL"]["injuries"][0]["provider_date"]=="2026-11-20T08:00Z"
    assert compact["teams"]["ATL"]["injuries"][1]["normalized_status"]=="unknown"
    assert compact["is_confirmed_starting_lineup"] is False
    assert compact["unresolved_id_count"]==1

def test_time_travel_and_staleness_guard():
    with pytest.raises(ValueError,match="Future"):
        compact_snapshot(shared_source(),cutoff_utc="2026-11-18T17:00:00Z")
    with pytest.raises(ValueError,match="Stale"):
        compact_snapshot(shared_source(),cutoff_utc="2026-11-22T18:01:00Z")

def test_bridge_to_gpt_warehouse_without_fabricating_lineups():
    con=warehouse()
    snap=compact_snapshot(shared_source(),cutoff_utc=NOW)
    counts=ingest_availability_snapshot(con,GAME,NOW,snap)
    assert counts["injury_reports_imported"]==3
    assert counts["unmatched_player_ids"]==1
    assert counts["lineups_confirmed"]==0
    rows=asof_availability(con,GAME,NOW)
    assert {r["player_id"]:r["normalized_status"] for r in rows}=={
        "player:nba:101":"out","player:nba:102":"unknown",
        "player:nba:103":"probable"}
    # Old source provider date does not make a future capture available earlier.
    assert asof_availability(con,GAME,"2026-11-18T17:00:00Z")==[]
    assert asof_lineup(con,GAME,NOW)==[]
    counts2=ingest_availability_snapshot(con,GAME,NOW,snap)
    assert counts2["injury_reports_imported"]==3
    assert con.execute("SELECT COUNT(*) FROM availability_reports").fetchone()[0]==3

def test_append_only_archive_and_original_time():
    with TemporaryDirectory() as folder:
        raw=Path(folder)/"availability.json"
        raw.write_text(json.dumps(shared_source()),encoding="utf-8")
        one=capture_snapshot(raw,now_utc=NOW,folder=Path(folder)/"snapshots")
        two=capture_snapshot(raw,now_utc=NOW,folder=Path(folder)/"snapshots")
        assert one==two
        assert latest_asof_archive(one.parent,NOW)["generated_utc"]==CAPTURE
        assert latest_asof_archive(one.parent,"2026-11-18T17:00:00Z") is None
        assert latest_asof_archive(one.parent,"2026-11-22T18:01:00Z") is None

def test_malformed_source_incomplete_team_rejected_when_missing():
    src=shared_source()
    src["problems"]=["roster unavailable"]
    with pytest.raises(ValueError,match="ESPN feed reported errors"):
        compact_snapshot(src,cutoff_utc=NOW)
