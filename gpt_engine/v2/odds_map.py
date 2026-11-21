"""Conservative one-to-one The Odds API event <-> official NBA SQLite resolver.

No inferred matchup by date alone. Resolve only approved full-name/abbr
aliases AND the same home/away AND a bounded UTC tip difference; reject
multiple schedule matches. Player IDs are NEVER resolved from names here.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3

from .contracts import iso, utc

NBA_ABBREVIATIONS = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BKN",
    "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "LA Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS",
}
_NAME_TO_ABBR = {**{name.casefold():code
                    for name,code in NBA_ABBREVIATIONS.items()},
                 **{code.casefold():code
                    for code in set(NBA_ABBREVIATIONS.values())}}
_VERSION = "gpt-v2-nba-odds-event-map-0.1"


def abbreviation(name: str) -> str | None:
    return _NAME_TO_ABBR.get(" ".join(str(name).casefold().split()))


def map_provider_events(events: list[dict], connection: sqlite3.Connection,
                        *, max_tip_difference_minutes: float = 30) -> dict:
    if not 0 <= max_tip_difference_minutes <= 60:
        raise ValueError("Tip tolerance must be in [0,60] minutes")
    connection.row_factory = sqlite3.Row
    schedule = connection.execute(
        """SELECT g.game_id, g.tip_utc, g.home_team_id, g.away_team_id,
                  h.current_name AS home_name, a.current_name AS away_name
           FROM games g JOIN teams h ON h.team_id=g.home_team_id
                        JOIN teams a ON a.team_id=g.away_team_id
           WHERE g.game_type='regular_season' AND g.tip_utc IS NOT NULL"""
    ).fetchall()
    mapped, skipped, used_game_ids = {}, [], set()
    for e in events:
        eid = str(e.get("id", ""))
        home_name = str(e.get("home_team", ""))
        away_name = str(e.get("away_team", ""))
        home_abbr = abbreviation(home_name)
        away_abbr = abbreviation(away_name)
        if not eid or not home_abbr or not away_abbr or home_abbr == away_abbr:
            skipped.append({"provider_event_id": eid,
                            "reason": "UNKNOWN_PROVIDER_TEAM_IDENTITY"})
            continue
        try:
            tip = iso(e["commence_time"])
        except (KeyError, TypeError, ValueError):
            skipped.append({"provider_event_id": eid,
                            "reason": "INVALID_PROVIDER_TIP"})
            continue
        matches = []
        for g in schedule:
            db_home = abbreviation(g["home_name"])
            db_away = abbreviation(g["away_name"])
            if db_home != home_abbr or db_away != away_abbr:
                continue
            delta = abs((utc(g["tip_utc"]) - utc(tip)).total_seconds())
            if delta <= max_tip_difference_minutes * 60:
                matches.append(g)
        if len(matches) != 1:
            skipped.append({"provider_event_id": eid,
                            "reason": "NO_UNIQUE_NBA_GAME_MATCH",
                            "candidate_count": len(matches)})
            continue
        g = matches[0]
        if g["game_id"] in used_game_ids or eid in mapped:
            skipped.append({"provider_event_id": eid,
                            "reason": "DUPLICATE_EVENT_TO_GAME_MATCH"})
            continue
        used_game_ids.add(g["game_id"])
        mapped[eid] = {
            "game_id": g["game_id"], "tip_utc": iso(g["tip_utc"]),
            "home_team": home_name, "away_team": away_name,
            "home_team_id": g["home_team_id"],
            "away_team_id": g["away_team_id"],
            "settlement_scope": "full_game_including_ot",
            "players": {},  # Never infer prop identities from player names
        }
    return {"version": _VERSION, "events": mapped, "skipped": skipped}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, required=True)
    ap.add_argument("--source-json", type=Path, required=True,
                    help="Saved response from /v4/sports/basketball_nba/events or /odds")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(argv)
    data = json.loads(args.source_json.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "data" in data:
        data = data["data"]
    if not isinstance(data, list):
        raise ValueError("Expected NBA provider event array")
    with sqlite3.connect(args.db) as con:
        report = map_provider_events(data, con)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n",
                           encoding="utf-8")
    print(json.dumps({"matched":len(report["events"]),
                      "skipped":len(report["skipped"])}))


if __name__ == "__main__":
    main()
