"""SQLite persistence: immutable forecasts, results and evaluations.

`forecasts` rows can never be UPDATEd or DELETEd (enforced by triggers), which
implements the rule "never overwrite a past prediction after the outcome is known".
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS data_sources(
  source_id INTEGER PRIMARY KEY, name TEXT, url TEXT, retrieved_at_utc TEXT,
  season_coverage TEXT, sha256 TEXT, reliability TEXT, limitations TEXT);
CREATE TABLE IF NOT EXISTS games(
  season INTEGER, game_id INTEGER, seq INTEGER, home TEXT, away TEXT, n_periods INTEGER,
  PRIMARY KEY(season, game_id));
CREATE TABLE IF NOT EXISTS results(
  season INTEGER, game_id INTEGER, home_pts INTEGER, away_pts INTEGER, ingested_at_utc TEXT,
  PRIMARY KEY(season, game_id));
CREATE TABLE IF NOT EXISTS forecasts(
  forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
  season INTEGER, game_id INTEGER, model_name TEXT, model_version TEXT,
  made_at_utc TEXT, data_cutoff TEXT, seed INTEGER, n_sims INTEGER,
  p_home REAL, mean_home REAL, mean_away REAL, mean_margin REAL, mean_total REAL,
  p_ot REAL, q_margin_json TEXT, q_total_json TEXT, details_json TEXT,
  UNIQUE(season, game_id, model_name, model_version));
CREATE TRIGGER IF NOT EXISTS forecasts_no_update BEFORE UPDATE ON forecasts
BEGIN SELECT RAISE(ABORT, 'forecasts are immutable'); END;
CREATE TRIGGER IF NOT EXISTS forecasts_no_delete BEFORE DELETE ON forecasts
BEGIN SELECT RAISE(ABORT, 'forecasts are immutable'); END;
CREATE TABLE IF NOT EXISTS model_versions(
  model_name TEXT, model_version TEXT, params_json TEXT, created_at_utc TEXT,
  PRIMARY KEY(model_name, model_version));
CREATE TABLE IF NOT EXISTS evaluations(
  model_name TEXT, model_version TEXT, scope TEXT, metric TEXT, value REAL, n INTEGER,
  computed_at_utc TEXT, PRIMARY KEY(model_name, model_version, scope, metric));
"""


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Store:
    def __init__(self, path: str):
        self.con = sqlite3.connect(path)
        self.con.executescript(SCHEMA)

    def add_source(self, **kw):
        cols = ["name", "url", "retrieved_at_utc", "season_coverage", "sha256", "reliability", "limitations"]
        self.con.execute(f"INSERT INTO data_sources({','.join(cols)}) VALUES({','.join('?' * len(cols))})",
                         [kw.get(c) for c in cols])

    def add_model_version(self, name: str, version: str, params: dict):
        self.con.execute("INSERT OR IGNORE INTO model_versions VALUES(?,?,?,?)",
                         (name, version, json.dumps(params, default=str), now_utc()))

    def add_games(self, games):
        self.con.executemany(
            "INSERT OR IGNORE INTO games VALUES(?,?,?,?,?,?)",
            [(int(r.season), int(r.game_id), int(r.order), r.home, r.away, int(r.n_periods))
             for r in games.itertuples()])

    def add_result(self, season, game_id, home_pts, away_pts):
        self.con.execute("INSERT OR IGNORE INTO results VALUES(?,?,?,?,?)",
                         (int(season), int(game_id), int(home_pts), int(away_pts), now_utc()))

    def save_forecast(self, season, game_id, model_name, model_version, data_cutoff, seed, n_sims,
                      p_home, mean_home, mean_away, mean_total, p_ot=None,
                      q_margin=None, q_total=None, details=None):
        self.con.execute(
            """INSERT INTO forecasts(season,game_id,model_name,model_version,made_at_utc,data_cutoff,seed,n_sims,
               p_home,mean_home,mean_away,mean_margin,mean_total,p_ot,q_margin_json,q_total_json,details_json)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (int(season), int(game_id), model_name, model_version, now_utc(), data_cutoff, seed, n_sims,
             p_home, mean_home, mean_away, mean_home - mean_away, mean_total, p_ot,
             json.dumps(q_margin) if q_margin else None, json.dumps(q_total) if q_total else None,
             json.dumps(details, default=str) if details else None))

    def commit(self):
        self.con.commit()
