"""Daily player-history update from ESPN per-game box scores (best effort; never raises into the caller).

ESPN athlete ids differ from the NBA person ids the player model was built on, so each ESPN player is mapped to a model id:
  1. a manual override (artifacts/name_overrides.json: {"<espn id>": <nba id>}),
  2. a previously stored mapping (artifacts/player_id_map.json),
  3. initial + surname match against players the model already knows (same-name players split by last team),
  4. otherwise a new player keyed by the NEGATED ESPN id (no history yet; it accumulates from now on).
Mappings are stored so a player keeps one id for good.
"""
from __future__ import annotations

import json
import os

import pandas as pd

from .availability import _model_index, _resolve
from .feed import nba_code
from .players import PlayerModel

# ESPN stat key (or label) -> our column
KEYMAP = {"minutes": "min", "MIN": "min", "points": "pts", "PTS": "pts", "rebounds": "reb", "REB": "reb",
          "offensiveRebounds": "oreb", "OREB": "oreb", "assists": "ast", "AST": "ast", "steals": "stl", "STL": "stl",
          "blocks": "blk", "BLK": "blk", "turnovers": "tov", "TO": "tov"}
PAIRS = {"fieldGoalsMade-fieldGoalsAttempted": ("fgm", "fga"), "FG": ("fgm", "fga"),
         "threePointFieldGoalsMade-threePointFieldGoalsAttempted": ("tpm", "tpa"), "3PT": ("tpm", "tpa"),
         "freeThrowsMade-freeThrowsAttempted": ("ftm", "fta"), "FT": ("ftm", "fta")}
COLS = ["team", "player_id", "name", "min", "pts", "reb", "oreb", "ast", "stl", "blk", "tov", "fgm", "fga", "tpm", "tpa", "ftm", "fta"]


def _num(x):
    try:
        return float(str(x).split(":")[0]) + (float(str(x).split(":")[1]) / 60 if ":" in str(x) else 0.0)
    except Exception:
        return 0.0


def parse_summary(js: dict) -> list[dict]:
    """One dict per player who has a stat line. Keys: espn_id, name, team + COLS stats. Skips DNP rows."""
    rows = []
    for tb in js.get("boxscore", {}).get("players", []):
        team = nba_code((tb.get("team") or {}).get("abbreviation", ""))
        for grp in tb.get("statistics", []):
            keys = grp.get("keys") or grp.get("labels") or grp.get("names") or []
            for a in grp.get("athletes", []):
                if a.get("didNotPlay") or not a.get("stats"):
                    continue
                ath = a.get("athlete") or {}
                r = {"espn_id": str(ath.get("id")), "name": ath.get("displayName") or ath.get("shortName") or "", "team": team}
                for k, v in zip(keys, a["stats"]):
                    if k in PAIRS:
                        try:
                            m, att = str(v).split("-")
                            r[PAIRS[k][0]], r[PAIRS[k][1]] = float(m), float(att)
                        except Exception:
                            pass
                    elif k in KEYMAP:
                        r[KEYMAP[k]] = _num(v)
                if r.get("min", 0) > 0:
                    rows.append(r)
    return rows


def _load(path, default):
    try:
        return json.load(open(path)) if os.path.exists(path) else default
    except Exception:
        return default


def _save(path, obj):
    with open(path + ".tmp", "w") as f:
        json.dump(obj, f)
    os.replace(path + ".tmp", path)


def update_players(feed, art_dir: str = "artifacts", sink=None) -> dict:
    out = {"games_applied": 0, "rows": 0, "mapped_existing": 0, "new_players": 0, "skipped_games": 0, "problems": []}
    try:
        state = os.path.join(art_dir, "player_state.json")
        applied_p, map_p = os.path.join(art_dir, "player_applied.json"), os.path.join(art_dir, "player_id_map.json")
        pm = PlayerModel.load(state)
        applied = set(_load(applied_p, []))
        idmap = _load(map_p, {})
        overrides = _load(os.path.join(art_dir, "name_overrides.json"), {})
        idx = _model_index(state)
        todo = sorted(((d, int(eid), season, js) for eid, (d, season, js) in feed.summaries.items() if eid not in applied),
                      key=lambda t: (t[0], t[1]))
        for date, eid, season, js in todo:
            rows = parse_summary(js)
            if len(rows) < 10:                      # a real game has >= 10 players with minutes; otherwise the format is not what we expect
                out["skipped_games"] += 1
                out["problems"].append(f"game {eid}: only {len(rows)} player rows parsed")
                continue
            for r in rows:
                key = r["espn_id"]
                pid = overrides.get(key) or idmap.get(key)
                if pid is None:
                    pid = _resolve(idx, r["name"], r["team"])
                    if pid is None:
                        pid = -int(key)
                        out["new_players"] += 1
                    else:
                        out["mapped_existing"] += 1
                    idmap[key] = int(pid)
                r["player_id"] = int(pid)
            df = pd.DataFrame(rows)
            for c in COLS:
                if c not in df:
                    df[c] = 0.0 if c not in ("team", "name") else ""
            df = df[COLS].fillna(0)
            pm.update_game(df, season)
            if sink is not None:                    # e.g. store the actual box score for live calibration; never blocks the update
                try:
                    sink(season, eid, df)
                except Exception as ex:
                    out["problems"].append(f"sink game {eid}: {type(ex).__name__}: {ex}")
            applied.add(str(eid))
            out["games_applied"] += 1
            out["rows"] += len(df)
        if out["games_applied"]:
            pm.save(state)
            _save(applied_p, sorted(applied))
            _save(map_p, idmap)
    except Exception as ex:
        out["problems"].append(f"{type(ex).__name__}: {ex}")
    return out
