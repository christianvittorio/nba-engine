"""Extract independently observed NBA outcomes for market audit from SQLite.

Historical outcomes are allowed AFTER forecasts are frozen. A score that
fails team scoring identities is NOT graded. Provider retrieval time is
used as the earliest known 'final observed' time; true final whistle is
not inferred from the scheduled tip time.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3

from .contracts import iso, utc

VERSION = "gpt-v2-source-backed-market-outcomes-0.1"
COUNTING_STATS = ("pts", "reb", "ast", "fg3m")


def _stat_value(source: dict, key: str) -> float | None:
    try:
        x = source.get(key)
        if x is None or isinstance(x, bool):
            return None
        value = float(x)
        if not 0 <= value <= 100:
            return None
        return value
    except (ValueError, TypeError, OverflowError):
        return None


def _minutes_value(stats: dict) -> float | None:
    for key in ("min", "minutes"):
        raw = stats.get(key)
        if isinstance(raw, str) and ":" in raw:
            parts = raw.split(":")
            if len(parts) == 2 and all(x.isdigit() for x in parts):
                minutes = int(parts[0]) + int(parts[1])/60
                if 0 <= minutes <= 65 and 0 <= int(parts[1]) < 60:
                    return minutes
        value = _stat_value(stats, key)
        if value is not None and value <= 65:
            return value
    return None


def _score_consistent(stats: dict, actual: int) -> bool:
    try:
        if not all(k in stats for k in ("fgm", "fg3m", "ftm", "pts")):
            return False
        return (int(stats["pts"]) == int(actual)
                and 2*int(stats["fgm"]) + int(stats["fg3m"])
                + int(stats["ftm"]) == int(actual))
    except (ValueError, TypeError, OverflowError):
        return False


def extract_final_outcomes(connection: sqlite3.Connection, *,
                           date_from: str | None = None,
                           date_before: str | None = None) -> dict:
    connection.row_factory = sqlite3.Row
    query = (
        "SELECT r.game_id,g.game_date_eastern,g.tip_utc,r.home_score,"
        "r.away_score,r.source_id,r.retrieved_at_utc "
        "FROM actual_results r JOIN games g USING(game_id) "
        "WHERE g.status='final' AND g.game_type='regular_season'"
    )
    params = []
    if date_from:
        query += " AND g.game_date_eastern>=?"
        params.append(date_from)
    if date_before:
        query += " AND g.game_date_eastern<?"
        params.append(date_before)
    query += " ORDER BY g.tip_utc,g.game_id"
    rows, excluded = [], []
    for g in connection.execute(query, params).fetchall():
        gid = g["game_id"]
        tip = g["tip_utc"]
        observed = g["retrieved_at_utc"]
        if not tip or not observed or utc(observed) <= utc(tip):
            excluded.append({"game_id":gid,
                             "reason":"FINAL_NOT_OBSERVED_AFTER_TIP"})
            continue
        stat_rows = connection.execute(
            "SELECT t.team_id,t.stats_json FROM team_game_stats t "
            "WHERE t.game_id=?", (gid,)
        ).fetchall()
        if len(stat_rows) != 2:
            excluded.append({"game_id":gid,
                             "reason":"INVALID_TEAM_SCORE_COMPONENTS"})
            continue
        home_score, away_score = int(g["home_score"]), int(g["away_score"])
        # Team stats order is not guaranteed! Verify against actual
        # home/away IDs, never compare positional rows.
        sides = connection.execute(
            "SELECT home_team_id,away_team_id FROM games WHERE game_id=?",
            (gid,)
        ).fetchone()
        by_team = {r["team_id"]:json.loads(r["stats_json"])
                   for r in stat_rows}
        if (sides is None or set(by_team) != {
                sides["home_team_id"], sides["away_team_id"]}
                or not _score_consistent(by_team[sides["home_team_id"]],home_score)
                or not _score_consistent(by_team[sides["away_team_id"]],away_score)):
            excluded.append({"game_id":gid,
                             "reason":"INVALID_TEAM_SCORE_COMPONENTS"})
            continue
        players = {}
        player_rows = connection.execute(
            "SELECT player_id,stats_json FROM player_game_stats "
            "WHERE game_id=?", (gid,)
        ).fetchall()
        for p in player_rows:
            stats = json.loads(p["stats_json"])
            minutes = _minutes_value(stats)
            entry = {"status": "unknown"}
            if minutes is not None and minutes > 0:
                entry["status"] = "played"
                for key in COUNTING_STATS:
                    value = _stat_value(stats,key)
                    if value is not None:
                        entry[key] = value
            elif stats.get("dnp") is True or str(stats.get("comment","")).upper().startswith("DNP"):
                entry["status"] = "dnp"
            # Unknown minutes are NOT an evidence-backed DNP.
            players[str(p["player_id"])] = entry
        rows.append({
            "game_id":gid,
            "tip_utc":iso(tip),
            "status":"final",
            "final_at_utc":iso(observed),
            "retrieved_at_utc":iso(observed),
            "source_id":g["source_id"]+":retrieved-final-observation",
            "home_score":home_score,
            "away_score":away_score,
            "players":players
        })
    return {
        "version":VERSION,
        "games":rows,
        "excluded":excluded,
        "warning":(
            "Source-retrieval timestamp is the first documented final "
            "observation, not an actual final whistle timestamp. "
            "Historical player appearance data may be incomplete; "
            "unverified DNP player props remain ungraded."
        )
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--date-from",default="")
    ap.add_argument("--date-before",default="")
    args=ap.parse_args(argv)
    with sqlite3.connect(args.db) as con:
        result=extract_final_outcomes(con,
                                      date_from=args.date_from or None,
                                      date_before=args.date_before or None)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",
                           encoding="utf-8")
    print(json.dumps({"valid_finals":len(result["games"]),
                      "excluded":len(result["excluded"])}))


if __name__=="__main__":
    main()
