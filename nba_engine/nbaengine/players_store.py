"""SQLite persistence for player forecasts. Rows are immutable (UPDATE and DELETE abort), like team forecasts."""
from __future__ import annotations

import json
import sqlite3

from .store import now_utc

SCHEMA = """
CREATE TABLE IF NOT EXISTS player_forecasts(
  forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
  season INTEGER, game_id INTEGER, team TEXT, player_id INTEGER, name TEXT, mode TEXT,
  model_version TEXT, made_at_utc TEXT, data_cutoff TEXT, seed INTEGER, n_sims INTEGER,
  proj_min REAL, p_play REAL, is_new INTEGER, assumptions_json TEXT, details_json TEXT,
  UNIQUE(season, game_id, player_id, mode, model_version));
CREATE TRIGGER IF NOT EXISTS pf_no_update BEFORE UPDATE ON player_forecasts
BEGIN SELECT RAISE(ABORT, 'player forecasts are immutable'); END;
CREATE TRIGGER IF NOT EXISTS pf_no_delete BEFORE DELETE ON player_forecasts
BEGIN SELECT RAISE(ABORT, 'player forecasts are immutable'); END;
CREATE TABLE IF NOT EXISTS injury_snapshots(
  snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT, retrieved_utc TEXT, source TEXT, team TEXT, player TEXT,
  status TEXT, note TEXT, reported_date TEXT);
"""


class PlayerStore:
    def __init__(self, path: str):
        self.con = sqlite3.connect(path)
        self.con.executescript(SCHEMA)

    def save(self, season, game_id, team, player_id, name, mode, version, cutoff, seed, n_sims, proj_min, p_play,
             is_new, assumptions, details):
        self.con.execute(
            """INSERT INTO player_forecasts(season,game_id,team,player_id,name,mode,model_version,made_at_utc,data_cutoff,
               seed,n_sims,proj_min,p_play,is_new,assumptions_json,details_json) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (int(season), int(game_id), team, int(player_id), name, mode, version, now_utc(), cutoff, seed, n_sims,
             float(proj_min), float(p_play), int(is_new), json.dumps(assumptions), json.dumps(details)))

    def add_injuries(self, source: str, rows: list[dict]):
        t = now_utc()
        self.con.executemany(
            "INSERT INTO injury_snapshots(retrieved_utc,source,team,player,status,note,reported_date) VALUES(?,?,?,?,?,?,?)",
            [(t, source, r.get("team"), r.get("player"), r.get("status"), r.get("note"), r.get("date")) for r in rows])

    def commit(self):
        self.con.commit()
