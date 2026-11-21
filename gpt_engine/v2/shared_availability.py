"""Read-only integration of Claude's *source data*, not Claude's predictions.

The legacy engine already captures ESPN roster and injury JSON in
nba_engine/artifacts/availability.json. Reuse that single data feed instead
of fetching conflicting sources or borrowing Claude's model adjustments.

IMPORTANT: this feed is unofficial, sometimes incomplete, and contains
no confirmed starting-lineup observations. A present roster entry is NOT
proof that the player will play, and "Day-To-Day" is NOT "Questionable".
Statuses are observed when the source file was generated; the injury's
provider-native date is retained separately rather than being mistaken for
a historical capture timestamp.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any

from .contracts import iso, utc, canonical_json
from .warehouse import register_source, register_player

SOURCE="espn_unofficial_shared_feed"
ROOT=Path(__file__).resolve().parents[2]
CLAUDE_SNAPSHOT=ROOT/"nba_engine/artifacts/availability.json"
ARCHIVE=ROOT/"gpt_engine/v2/artifacts/availability"
PROBABLE={"probable"}
UNKNOWN={"day-to-day","day to day","dtd","gtd","game-time decision",
         "game time decision","unknown","","injured"}
CONFIRMED={"confirmed available","confirmed_available"}
VALID={"confirmed_available","probable","questionable","doubtful","out","unknown"}

def normalize_status(value:str | None) -> str:
    """Conservative cross-provider mapping; never invent certainty."""
    status=str(value or "").strip().lower().replace("_","-")
    if status in ("out","inactive","ruled out"):return "out"
    if status=="doubtful":return "doubtful"
    if status=="questionable":return "questionable"
    if status in PROBABLE:return "probable"
    if status in CONFIRMED:return "confirmed_available"
    # ESPN uses 'Day-To-Day' for many injuries; no one-to-one Q status.
    return "unknown"

def verify_source_snapshot(av:dict,cutoff_utc:str, *,
                           max_age_hours:float=12.0) -> tuple[str,list[str]]:
    if not isinstance(av,dict) or not av.get("teams"):
        raise ValueError("Empty/unavailable ESPN roster/injury source")
    if av.get("problems"):
        raise ValueError("ESPN feed reported errors; do not silently infer a complete snapshot")
    capture=iso(av["generated_utc"])
    cutoff=utc(cutoff_utc)
    if utc(capture)>cutoff:
        raise ValueError("Future ESPN availability snapshot cannot enter past features")
    age=(cutoff-utc(capture)).total_seconds()/3600.0
    if age>max_age_hours:
        raise ValueError(f"Stale ESPN availability snapshot: {age:.1f}h")
    if age<0:raise ValueError("Snapshot from future")
    return capture,["unofficial_espn_source","not_official_confirmed_lineups"]

def _team_codes(con:sqlite3.Connection,season:int) -> dict[str,str]:
    """Map official NBA team IDs by stored official team-game abbreviations."""
    rows=con.execute(
        "SELECT team_id,json_extract(stats_json,'$.team') AS abbrev "
        "FROM team_game_stats WHERE season=? AND json_extract(stats_json,'$.team') IS NOT NULL "
        "GROUP BY team_id,abbrev",(season,)
    ).fetchall()
    result={}
    for row in rows:
        code=str(row["abbrev"]).upper()
        if code in result and result[code]!=row["team_id"]:
            raise ValueError(f"Conflicting official team code {code}")
        result[code]=row["team_id"]
    return result

def _nba_id(raw:Any)->str | None:
    try:
        if raw is None or isinstance(raw,bool):return None
        n=int(str(raw))
    except (ValueError,TypeError):
        return None
    # Negative IDs in the legacy model are ESPN-only placeholders, not NBA IDs.
    if n<=0:return None
    return str(n)

def compact_snapshot(source:dict,*,cutoff_utc:str,
                     max_age_hours:float=12.0)->dict:
    capture,flags=verify_source_snapshot(source,cutoff_utc,max_age_hours=max_age_hours)
    teams={}
    for abbrev,record in source["teams"].items():
        roster=[{
            "espn_id":str(x.get("espn_id")),
            "nba_id":_nba_id(x.get("nba_id")),
            "name":str(x.get("name") or ""),
            "position":x.get("pos"),
        } for x in record.get("roster",[])]
        injuries=[{
            "nba_id":_nba_id(x.get("nba_id")),
            "espn_id":str(next((p["espn_id"] for p in roster
                if p["nba_id"] and p["nba_id"]==_nba_id(x.get("nba_id"))),"")),
            "name":x.get("name"),
            "provider_status":str(x.get("status") or ""),
            "normalized_status":normalize_status(x.get("status")),
            "provider_date":x.get("date"),
        } for x in record.get("injuries",[])]
        teams[str(abbrev).upper()]={"roster":roster,"injuries":injuries}
    return {
        "generated_utc":capture,
        "source_id":SOURCE,
        "source_label":source.get("source"),
        "quality_flags":flags+["historical_capture_uses_source_generated_utc"],
        "teams":teams,
        "unresolved_id_count":sum(1 for v in teams.values() for i in v["injuries"]
                                   if not i["nba_id"]),
        "is_confirmed_starting_lineup":False,
        "provenance":"Claude ESPN roster/injury collector; raw source reused, model remains independent",
    }

def capture_snapshot(file:Path | str=CLAUDE_SNAPSHOT,*,now_utc:str | None=None,
                     folder:Path | str=ARCHIVE,
                     max_age_hours:float=12)->Path:
    current=now_utc or iso(datetime.now(timezone.utc))
    raw=json.loads(Path(file).read_text(encoding="utf-8"))
    snap=compact_snapshot(raw,cutoff_utc=current,max_age_hours=max_age_hours)
    target=Path(folder)
    target.mkdir(parents=True,exist_ok=True)
    name=snap["generated_utc"].replace("-","").replace(":","").replace("Z","Z")+".json"
    output=target/name
    body=canonical_json(snap)+"\n"
    if output.exists():
        if output.read_text(encoding="utf-8")!=body:
            raise ValueError("Same timestamp, different injury snapshot; refusing overwrite")
        return output
    output.write_text(body,encoding="utf-8")
    return output

def _snapshots(archive:Path | str,cutoff:str,max_age_hours:float):
    for p in sorted(Path(archive).glob("*.json"),reverse=True):
        try:
            d=json.loads(p.read_text(encoding="utf-8"))
            verify_source_snapshot(d,cutoff,max_age_hours=max_age_hours)
        except (ValueError,KeyError,TypeError):
            continue
        if d.get("source_id")!=SOURCE:continue
        return d
    return None

def latest_asof_archive(archive:Path | str, cutoff:str,
                        *,max_age_hours:float=12)->dict | None:
    return _snapshots(archive,cutoff,max_age_hours)

def ingest_availability_snapshot(con:sqlite3.Connection,game_id:str,
                                 cutoff_utc:str,source:dict,
                                 *,max_age_hours:float=12.0)->dict:
    """Insert only relevant observed injury statuses, with explicit raw source time.

    Source created_at is the observation timestamp. ESPN's injury date may
    be old. The first known archive capture must precede forecast cutoff
    and tip-off. Missing athletes are never upgraded to 'active'.
    """
    capture,flags=verify_source_snapshot(source,cutoff_utc,max_age_hours=max_age_hours)
    game=con.execute(
        "SELECT season,tip_utc,home_team_id,away_team_id FROM games WHERE game_id=?",
        (game_id,)
    ).fetchone()
    if not game:raise KeyError(f"No matching game {game_id}")
    if not game["tip_utc"] or utc(cutoff_utc)>=utc(game["tip_utc"]):
        raise ValueError("No pre-tip observation cutoff")
    if utc(capture)>=utc(game["tip_utc"]):
        raise ValueError("Injury snapshot after tip")
    teams=_team_codes(con,int(game["season"]))
    allowed_ids={str(game["home_team_id"]),str(game["away_team_id"])}
    active_codes=[x for x,y in teams.items() if y in allowed_ids]
    if set(teams.get(code) for code in active_codes)!=allowed_ids or len(active_codes)!=2:
        raise ValueError("Official team identifiers could not map both opponents")
    register_source(con,SOURCE,"ESPN public JSON shared with Claude",
                    "https://site.api.espn.com/apis/site/v2/sports/basketball/nba")
    counts={"source_generated_utc":capture,"injury_reports_imported":0,
            "unmatched_player_ids":0,"statuses":{},"teams":active_codes,
            "lineups_confirmed":0,"quality_flags":list(flags)}
    for code in active_codes:
        team_data=source["teams"].get(code)
        if not team_data:
            counts["quality_flags"].append("missing_team_roster:"+code)
            continue
        for inj in team_data.get("injuries",[]):
            nbaid=_nba_id(inj.get("nba_id"))
            if not nbaid:
                counts["unmatched_player_ids"]+=1
                continue
            internal="player:nba:"+nbaid
            if con.execute("SELECT 1 FROM players WHERE player_id=?",(internal,)).fetchone() is None:
                # NBA ID was provided by legacy cross-provider mapping, but
                # may be absent from old source history (e.g. new rookie).
                register_player(con,internal,str(inj.get("name") or "") or None)
            raw_status=inj.get("provider_status",inj.get("status"))
            normalized=normalize_status(raw_status)
            rid="injury:"+hashlib.sha256(
                canonical_json([game_id,internal,raw_status,capture,SOURCE]).encode()
            ).hexdigest()[:32]
            con.execute(
                "INSERT OR IGNORE INTO availability_reports(report_id,game_id,player_id,"
                "provider_status,normalized_status,is_confirmed,report_utc,source_id,"
                "source_timestamp,retrieved_at_utc,quality_flags_json) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (rid,game_id,internal,str(raw_status or ""),normalized,0,
                 capture,SOURCE,inj.get("provider_date",inj.get("date")),capture,
                 canonical_json(["unofficial_espn","injury_date_is_provider_native",
                                 "not_confirmed_starter"])),
            )
            counts["injury_reports_imported"]+=1
            counts["statuses"][normalized]=counts["statuses"].get(normalized,0)+1
    con.commit()
    return counts
