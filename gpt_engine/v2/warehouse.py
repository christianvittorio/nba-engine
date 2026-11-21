"""SQLite warehouse with provider mappings and point-in-time-safe accessors."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

from .contracts import Availability, FeatureSnapshot, Prediction, Provenance, iso, utc, canonical_json

SCHEMA = Path(__file__).with_name("schema.sql")

def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    con = sqlite3.connect(str(path))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript(SCHEMA.read_text(encoding="utf-8"))
    con.execute(
        "INSERT OR IGNORE INTO schema_migrations(version,applied_at_utc,description)"
        " VALUES(1,?,?)",
        (iso(datetime.now(timezone.utc)), "GPT NBA schema v2 initial"),
    )
    con.commit()
    return con

def register_source(con, source: str, label: str, url: str | None = None,
                    license_notes: str | None = None):
    con.execute(
        "INSERT OR IGNORE INTO sources(source_id,label,upstream_uri,license_notes,created_at_utc)"
        " VALUES(?,?,?,?,?)",
        (source,label,url,license_notes,iso(datetime.now(timezone.utc)))
    )
    con.commit()

def register_team(con, team_id: str, name: str):
    con.execute(
        "INSERT INTO teams(team_id,current_name,created_at_utc) VALUES(?,?,?)"
        " ON CONFLICT(team_id) DO UPDATE SET current_name=excluded.current_name",
        (team_id,name,iso(datetime.now(timezone.utc)))
    )
    con.commit()

def register_player(con, player_id: str, name: str | None = None,
                    rookie_season: int | None = None):
    con.execute(
        "INSERT INTO players(player_id,canonical_name,rookie_season,created_at_utc)"
        " VALUES(?,?,?,?) ON CONFLICT(player_id) DO UPDATE SET "
        "canonical_name=COALESCE(excluded.canonical_name,players.canonical_name),"
        "rookie_season=COALESCE(excluded.rookie_season,players.rookie_season)",
        (player_id,name,rookie_season,iso(datetime.now(timezone.utc)))
    )
    con.commit()

def map_provider_id(con, entity_type: str, internal_id: str, source: str,
                    provider_id: str, observed_at_utc: str, flags=()):
    """Map to an EXISTING internal entity. Conflicting mapping fails."""
    if entity_type not in ("team","player","game","coach"):
        raise ValueError("Unknown entity type")
    table, col = {"team":("teams","team_id"),"player":("players","player_id"),
                  "game":("games","game_id"),"coach":("coaches","coach_id")}[entity_type]
    if con.execute(f"SELECT 1 FROM {table} WHERE {col}=?", (internal_id,)).fetchone() is None:
        raise KeyError(f"Internal {entity_type} not registered: {internal_id}")
    existing = con.execute(
        "SELECT internal_id FROM provider_ids WHERE entity_type=? AND source_id=? AND provider_id=?",
        (entity_type,source,provider_id)
    ).fetchone()
    if existing and existing["internal_id"] != internal_id:
        raise ValueError("Provider ID conflict. Manual resolution required.")
    con.execute(
        "INSERT OR IGNORE INTO provider_ids VALUES(?,?,?,?,?,?)",
        (entity_type,internal_id,source,str(provider_id),iso(observed_at_utc),
         canonical_json(list(flags)))
    )
    con.commit()

def upsert_game(con, game_id: str, season: int, day_eastern: str,
                tip_utc: str | None, home_id: str, away_id: str, status: str,
                provenance: Provenance, game_type="regular_season", neutral=False):
    tip = iso(tip_utc) if tip_utc is not None else None
    # Unknown time is nullable, never replaced by an invented midnight tip.
    con.execute(
        "INSERT INTO games(game_id,season,game_date_eastern,tip_utc,home_team_id,"
        "away_team_id,game_type,neutral_site,status,source_id,source_timestamp,"
        "retrieved_at_utc,quality_flags_json) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(game_id) DO UPDATE SET "
        "tip_utc=COALESCE(excluded.tip_utc,games.tip_utc),"
        "status=excluded.status,source_timestamp=excluded.source_timestamp,"
        "retrieved_at_utc=excluded.retrieved_at_utc,"
        "quality_flags_json=excluded.quality_flags_json",
        (game_id,season,day_eastern,tip,home_id,away_id,game_type,int(neutral),
         status,provenance.source_id,provenance.source_timestamp,
         provenance.retrieved_at_utc,canonical_json(list(provenance.quality_flags)))
    )
    con.commit()

def put_availability(con, report_id: str, game_id: str, item: Availability,
                     provenance: Provenance):
    con.execute(
        "INSERT INTO availability_reports(report_id,game_id,player_id,provider_status,"
        "normalized_status,is_confirmed,report_utc,source_id,source_timestamp,"
        "retrieved_at_utc,quality_flags_json) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        (report_id,game_id,item.player_id,item.provider_status,item.normalized_status,
         int(item.normalized_status == "confirmed_available"),item.report_utc,
         provenance.source_id,provenance.source_timestamp,provenance.retrieved_at_utc,
         canonical_json(list(provenance.quality_flags)))
    )
    con.commit()

def asof_availability(con, game_id: str, cutoff_utc: str) -> list[dict]:
    """No future report, and no record retrieved after the forecast cutoff."""
    cutoff = iso(cutoff_utc)
    rows = con.execute(
        "WITH eligible AS (SELECT *,ROW_NUMBER() OVER "
        "(PARTITION BY player_id ORDER BY report_utc DESC,retrieved_at_utc DESC) AS n "
        "FROM availability_reports WHERE game_id=? AND report_utc<=? "
        "AND retrieved_at_utc<=?) SELECT player_id,normalized_status,provider_status,"
        "report_utc,source_id,source_timestamp,retrieved_at_utc,quality_flags_json "
        "FROM eligible WHERE n=1 ORDER BY player_id",
        (game_id,cutoff,cutoff)
    ).fetchall()
    return [dict(r) for r in rows]

def asof_lineup(con, game_id: str, cutoff_utc: str) -> list[dict]:
    cutoff = iso(cutoff_utc)
    rows = con.execute(
        "WITH ranked AS (SELECT *,ROW_NUMBER() OVER "
        "(PARTITION BY team_id,player_id ORDER BY confirmation_utc DESC, retrieved_at_utc DESC) AS n "
        "FROM lineup_reports WHERE game_id=? AND confirmation_utc<=? "
        "AND retrieved_at_utc<=?) "
        "SELECT team_id,player_id,lineup_type,confirmation_utc,source_id "
        "FROM ranked WHERE n=1 ORDER BY team_id,player_id",
        (game_id,cutoff,cutoff)
    ).fetchall()
    return [dict(r) for r in rows]

def save_snapshot(con, item: FeatureSnapshot, max_source_timestamp_utc: str | None = None,
                  generated_at_utc: str | None = None) -> str:
    if max_source_timestamp_utc and utc(max_source_timestamp_utc) > utc(item.cutoff_utc):
        raise ValueError("Feature source is later than the information cutoff")
    generated = iso(generated_at_utc or datetime.now(timezone.utc))
    snap_id = item.stable_id()
    con.execute(
        "INSERT INTO feature_snapshots(snapshot_id,game_id,cutoff_utc,generated_at_utc,"
        "definition_version,features_json,source_max_timestamp_utc,"
        "source_manifest_hash,missingness_json,source_ids_json,quality_flags_json)"
        " VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        (snap_id,item.game_id,item.cutoff_utc,generated,item.definition_version,
         canonical_json(item.features),iso(max_source_timestamp_utc) if max_source_timestamp_utc else None,
         None,canonical_json(item.missingness),canonical_json(item.sources),
         canonical_json(item.quality_flags))
    )
    con.commit()
    return snap_id

def save_model_version(con, version: str, architecture: str, config: dict,
                       code_sha: str | None = None, train_cutoff: str | None = None,
                       data_hash: str | None = None):
    con.execute(
        "INSERT INTO model_versions(model_version,created_at_utc,code_commit_sha,"
        "architecture,config_json,training_cutoff_utc,training_manifest_hash)"
        " VALUES(?,?,?,?,?,?,?) ON CONFLICT(model_version) DO NOTHING",
        (version,iso(datetime.now(timezone.utc)),code_sha,architecture,
         canonical_json(config),iso(train_cutoff) if train_cutoff else None,data_hash)
    )
    con.commit()

def save_prediction(con, item: Prediction) -> str:
    row = con.execute("SELECT tip_utc FROM games WHERE game_id=?",(item.game_id,)).fetchone()
    if not row or not row["tip_utc"]:
        raise ValueError("An independently sourced UTC tip-off is required")
    if utc(item.cutoff_utc) >= utc(row["tip_utc"]) or utc(item.created_at_utc) >= utc(row["tip_utc"]):
        raise ValueError("An actual pregame forecast must be produced before tip-off")
    prediction_id = item.stable_id()
    con.execute(
        "INSERT INTO pregame_predictions(prediction_id,game_id,snapshot_id,model_version,"
        "cutoff_utc,created_at_utc,prediction_json,scenario_label)"
        " VALUES(?,?,?,?,?,?,?,?)",
        (prediction_id,item.game_id,item.snapshot_id,item.model_version,
         item.cutoff_utc,item.created_at_utc,canonical_json(item.values),item.scenario_label)
    )
    con.commit()
    return prediction_id

def finished_game_rows_asof(con, cutoff: str, season: int | None = None) -> list[dict]:
    """Corrected finished-game stats available only after the previous game day.

    Historical data backfilled later is suitable for retrospective experiments,
    NOT proof of what the pipeline retrieved on a historical date.
    """
    params = [iso(cutoff)[:10]]
    cond = "g.game_date_eastern < ?"
    if season is not None:
        cond += " AND g.season=?"
        params.append(season)
    rows = con.execute(
        "SELECT g.game_id,g.season,g.game_date_eastern,g.tip_utc,"
        "g.home_team_id,g.away_team_id,g.game_type,"
        "r.home_score,r.away_score FROM games g JOIN actual_results r USING(game_id) "
        f"WHERE {cond} AND g.game_type='regular_season' "
        "ORDER BY g.game_date_eastern,g.game_id",params
    ).fetchall()
    return [dict(r) for r in rows]
