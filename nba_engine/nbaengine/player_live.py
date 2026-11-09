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
import os
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
    cal_path = os.path.join(os.path.dirname(os.path.abspath(db_path)), "p_play_cal.json")
    if os.path.exists(cal_path):          # live pool excludes players listed Out, so the all-roster play table understates P(play): recalibrate (scripts/fit_p_play_cal.py)
        try:
            c_ = json.load(open(cal_path)); pm.p.p_play_cal = [float(c_["a"]), float(c_["b"])]
        except Exception:
            pm.p.p_play_cal = []
    try:
        return _forecast_slate(db_path, pm, av, games, n_sims, top, out)
    finally:
        pm.p.p_play_cal = []              # never persisted into the saved player state


def _forecast_slate(db_path, pm, av, games, n_sims, top, out) -> dict:
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
            pr = pm.project_team(team, mode="unconfirmed", pool_ids=pool, team_pts=(g.get("team_pts") or {}).get(team), opp_team=(g["away"] if team == g["home"] else g["home"]))
            pr = pr.sort_values("base_min", ascending=False).head(top).reset_index(drop=True)
            samp = sample_players(pr, pm.p, n_sims, g["seed"] + ti, "unconfirmed")
            summ = summarize_samples(samp)
            ladder = _ladders(samp)
            for i, (row, d) in enumerate(zip(pr.itertuples(index=False), summ)):
                det = {k: {"m": round(d[k]["mean"], 3), "q": [round(x, 2) for x in d[k]["q"]]} for k in KEEP if k in d}
                for k, v in (ladder[i].items() if float(row.proj_min) >= 10 else ()):   # full market ladders (P over x.5) incl. combos and 2-pointers; rotation players only
                    det.setdefault(k, {"m": v["m"], "q": v["q"]}).update(t0=v["t0"], ov=v["ov"])
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


COMBOS = {"pr": ("pts", "reb"), "pa": ("pts", "ast"), "ra": ("reb", "ast"), "sb": ("stl", "blk")}


def _ladders(samp: dict) -> list:
    """per player: for every market stat (singles, 2-pointers, combos) the mean, quantiles and P(over t+0.5) for t = 0,1,2,... from the same
    simulated draws, so a book's line can be priced directly. ov[j] = per-mille P(stat >= t0+j+1 | he plays) = P(over t0+j+0.5); below t0 it is above 98%, above the list under 2%."""
    arr = {k: samp[k] for k in ("pts", "reb", "ast", "stl", "blk", "tov", "tpm", "tpa", "fgm", "fga", "ftm", "fta", "pra") if k in samp}
    for k, (a, b) in COMBOS.items():
        arr[k] = arr[a] + arr[b]
    arr["fg2m"] = arr["fgm"] - arr["tpm"]; arr["fg2a"] = arr["fga"] - arr["tpa"]
    P = next(iter(arr.values())).shape[0]; out = []
    for i in range(P):
        played = np.asarray(samp["min"][i], dtype=float) > 0
        n_pl = max(int(played.sum()), 1)
        d = {}
        for k, x in arr.items():
            xa = np.asarray(x[i], dtype=float)
            allp = [float((xa >= t + 1).mean()) for t in range(int(min(xa.max(), 80)))]
            cond = [min(1.0, float(((xa >= t + 1) & played).sum()) / n_pl) for t in range(len(allp))]   # P(over t+0.5 | he plays)
            t0 = next((t for t, p in enumerate(cond) if p < 0.98), len(cond)); t1 = max((t for t, p in enumerate(cond) if p > 0.02), default=-1) + 1
            d[k] = {"m": round(float(xa.mean()), 3), "q": [round(float(v), 2) for v in np.percentile(xa, QS)],
                    "t0": t0, "ov": [int(round(p * 1000)) for p in cond[t0:t1]]}
        out.append(d)
    return out


def with_ladder(con, gid: int, pid: int, det: dict, table: str = "player_ladder") -> dict:
    """det from player_fc, with market ladders merged in: stored at forecast time (new forecasts) or from the player_ladder table (re-simulated for older ones)."""
    if "ov" in (det.get("pts") or {}):
        return det
    try:
        r = con.execute(f"SELECT ladder_json FROM {table} WHERE game_id=? AND player_id=?", (gid, pid)).fetchone()
    except sqlite3.OperationalError:
        return det
    if r:
        for k, v in json.loads(r[0]).items():
            x = det.setdefault(k, {"m": v["m"], "q": v["q"]}); x["t0"] = v["t0"]; x["ov"] = v["ov"]
    return det


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
