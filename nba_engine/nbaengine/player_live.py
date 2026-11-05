"""Live player-stat forecasts and actual box scores, for calibration of the player layer on the current season.

* Before tip-off (daily job): for every game that already has a stored team forecast and has not started, project each team's
  rotation (top 12 by usual minutes, players ESPN lists as Out removed) in the model's 'unconfirmed' mode (it does not know who
  starts; it includes the chance a player sits) and store mean + quantiles for the main stats. Rows are immutable (first write wins).
* After the game: the box score from the daily player update is stored as actuals.
* calibration_report.py reads both back and measures bias and interval coverage.
Stored in a separate file (artifacts/player_live.sqlite) so the team database stays small. Best effort: never raises into the caller.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from .players import OUT_STATS, QS, sample_players, summarize_samples

KEEP = ["min", "pts", "reb", "ast", "stl", "blk", "tov", "tpm", "tpa", "fgm", "fga", "ftm", "fta", "pra"]
ACT = ["min", "pts", "reb", "ast", "stl", "blk", "tov", "tpm", "tpa", "fgm", "fga", "ftm", "fta"]
SCHEMA = """
CREATE TABLE IF NOT EXISTS player_fc(season INTEGER, game_id INTEGER, team TEXT, player_id INTEGER, name TEXT, made_at_utc TEXT,
  proj_min REAL, p_play REAL, is_new INTEGER, details_json TEXT, PRIMARY KEY(season, game_id, player_id));
CREATE TRIGGER IF NOT EXISTS pfc_no_update BEFORE UPDATE ON player_fc BEGIN SELECT RAISE(ABORT, 'player forecasts are immutable'); END;
CREATE TRIGGER IF NOT EXISTS pfc_no_delete BEFORE DELETE ON player_fc BEGIN SELECT RAISE(ABORT, 'player forecasts are immutable'); END;
CREATE TABLE IF NOT EXISTS player_act(season INTEGER, game_id INTEGER, team TEXT, player_id INTEGER, min REAL, pts REAL, reb REAL, ast REAL,
  stl REAL, blk REAL, tov REAL, tpm REAL, tpa REAL, fgm REAL, fga REAL, ftm REAL, fta REAL, PRIMARY KEY(season, game_id, player_id));
"""


def connect(path: str) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    return con


def _out_ids(av: dict, team: str) -> set:
    t = (av or {}).get("teams", {}).get(team, {})
    return {i["nba_id"] for i in t.get("injuries", []) if i.get("nba_id") is not None and "out" in str(i.get("status", "")).lower()}


def forecast_slate(db_path: str, pm, av: dict | None, games: list[dict], n_sims: int = 1000, top: int = 12) -> dict:
    """games: [{season, game_id, home, away, seed}] — only games not yet started. Returns counts."""
    out = {"games": 0, "rows": 0, "skipped_existing": 0}
    con = connect(db_path)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for g in games:
        if con.execute("SELECT 1 FROM player_fc WHERE season=? AND game_id=? LIMIT 1", (g["season"], g["game_id"])).fetchone():
            out["skipped_existing"] += 1
            continue
        for ti, team in enumerate((g["home"], g["away"])):
            roster = [r["nba_id"] for r in (av or {}).get("teams", {}).get(team, {}).get("roster", []) if r.get("nba_id") is not None]
            outs = _out_ids(av, team)
            pool = [i for i in roster if i not in outs and i in pm.pl] if roster else [i for i in pm.pool(team) if i not in outs]
            if not pool:
                continue
            pr = pm.project_team(team, mode="unconfirmed", pool_ids=pool, team_pts=(g.get("team_pts") or {}).get(team))
            pr = pr.sort_values("base_min", ascending=False).head(top).reset_index(drop=True)
            samp = sample_players(pr, pm.p, n_sims, g["seed"] + ti, "unconfirmed")
            summ = summarize_samples(samp)
            for row, d in zip(pr.itertuples(index=False), summ):
                det = {k: {"m": round(d[k]["mean"], 3), "q": [round(x, 2) for x in d[k]["q"]]} for k in KEEP if k in d}
                try:
                    con.execute("INSERT OR IGNORE INTO player_fc VALUES(?,?,?,?,?,?,?,?,?,?)",
                                (g["season"], g["game_id"], team, int(row.player_id), row.name, now, float(row.proj_min),
                                 float(row.p_play), int(row.is_new), json.dumps(det)))
                    out["rows"] += 1
                except Exception:
                    pass
        out["games"] += 1
    con.commit(); con.close()
    return out


def store_actuals(db_path: str, season: int, game_id: int, df: pd.DataFrame) -> None:
    con = connect(db_path)
    con.executemany("INSERT OR IGNORE INTO player_act VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    [(int(season), int(game_id), r.team, int(r.player_id), *[float(getattr(r, c)) for c in ACT]) for r in df.itertuples(index=False)])
    con.commit(); con.close()


def load_frame(db_path: str) -> pd.DataFrame:
    """Forecast + actual per rostered player for games whose box score has arrived (a forecast player who did not play = 0)."""
    con = sqlite3.connect(db_path)
    try:
        F = pd.read_sql_query("SELECT * FROM player_fc", con)
        A = pd.read_sql_query("SELECT * FROM player_act", con)
    except Exception:
        return pd.DataFrame()
    finally:
        con.close()
    if F.empty or A.empty:
        return pd.DataFrame()
    A = A.rename(columns={c: f"a_{c}" for c in ACT})
    done = set(zip(A.season, A.game_id))
    F = F[[k in done for k in zip(F.season, F.game_id)]]
    M = F.merge(A.drop(columns=["team"]), on=["season", "game_id", "player_id"], how="left")
    M["played"] = M.a_min.fillna(0).gt(0).astype(int)
    for c in [c for c in M.columns if c.startswith("a_")]:
        M[c] = M[c].fillna(0.0)
    M["a_pra"] = M.a_pts + M.a_reb + M.a_ast
    det = M.details_json.map(json.loads)
    new = {}
    for s in KEEP:
        new[f"mean_{s}"] = det.map(lambda d: d[s]["m"])
        for qi, k in zip((5, 10, 25, 50, 75, 90, 95), range(7)):
            new[f"q{qi}_{s}"] = det.map(lambda d: d[s]["q"][k])
    return pd.concat([M.drop(columns=["details_json"]), pd.DataFrame(new)], axis=1)
