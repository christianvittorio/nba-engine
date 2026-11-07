"""Raw game-level data from the ESPN game summary, kept so that new layers (lineups, shot zones, quarters, officials, odds ...) can be built and
tested later without re-fetching. Stored append-only as one gzip JSON-lines file per game date: artifacts/gamedata/YYYY-MM-DD.jsonl.gz
(one record per game). Nothing is invented: fields ESPN does not provide are simply absent. Parsing is defensive; unknown shapes are skipped,
and the raw `pickcenter`/`odds`/`officials` blocks are stored as ESPN sent them."""
from __future__ import annotations
import gzip, json, os


def _g(d, *path, default=None):
    for k in path:
        if isinstance(d, dict):
            d = d.get(k)
        elif isinstance(d, list) and isinstance(k, int) and -len(d) <= k < len(d):
            d = d[k]
        else:
            return default
        if d is None:
            return default
    return d


def _slim_odds(pc):
    """keep the numbers (current and opening lines, odds), drop links, logos and deep-link URLs"""
    out = []
    for o in pc or []:
        out.append({"provider": _g(o, "provider", "name"), "details": o.get("details"), "overUnder": o.get("overUnder"), "spread": o.get("spread"),
                    "overOdds": o.get("overOdds"), "underOdds": o.get("underOdds"),
                    "home": {k: v for k, v in (o.get("homeTeamOdds") or {}).items() if k not in ("team", "links")},
                    "away": {k: v for k, v in (o.get("awayTeamOdds") or {}).items() if k not in ("team", "links")},
                    "moneyline": o.get("moneyline"), "pointSpread": o.get("pointSpread"), "total": o.get("total")})
    return out


def extract(event_id: str, date: str, season: int, js: dict) -> dict:
    comp = _g(js, "header", "competitions", 0, default={}) or {}
    teams = {}
    for c in comp.get("competitors", []) or []:
        teams[str(_g(c, "team", "id"))] = {"abbr": _g(c, "team", "abbreviation"), "home_away": c.get("homeAway"), "score": c.get("score"),
                                           "linescores": [x.get("displayValue") for x in (c.get("linescores") or [])], "winner": c.get("winner")}
    plays = []
    for p in js.get("plays") or []:
        plays.append({"seq": p.get("sequenceNumber"), "period": _g(p, "period", "number"), "clock": _g(p, "clock", "displayValue"),
                      "type": _g(p, "type", "text"), "text": p.get("text"), "team": _g(p, "team", "id"), "scoring": p.get("scoringPlay"),
                      "shooting": p.get("shootingPlay"), "value": p.get("scoreValue"), "away": p.get("awayScore"), "home": p.get("homeScore"),
                      "xy": [_g(p, "coordinate", "x"), _g(p, "coordinate", "y")] if p.get("coordinate") else None,
                      "players": [_g(a, "athlete", "id") for a in (p.get("participants") or [])]})
    return {"game_id": str(event_id), "date": date, "season": season, "teams": teams, "plays": plays,
            "officials": _g(js, "gameInfo", "officials", default=[]), "venue": _g(js, "gameInfo", "venue", "fullName"), "attendance": _g(js, "gameInfo", "attendance"),
            "odds": _slim_odds(js.get("pickcenter")), "againstTheSpread": js.get("againstTheSpread"),
            "team_stats": [{"team": _g(t, "team", "id"), "stats": [{"name": s.get("name"), "value": s.get("displayValue")} for s in (t.get("statistics") or [])]}
                           for t in (_g(js, "boxscore", "teams", default=[]) or [])],
            "winprob_home": [round(float(w.get("homeWinPercentage")), 4) for w in (js.get("winprobability") or []) if w.get("homeWinPercentage") is not None]}


def save_day(out_dir: str, date: str, records: list[dict]) -> str:
    """merge by game_id (idempotent: a re-run replaces a game's record, never duplicates it)"""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{date}.jsonl.gz")
    cur = {}
    if os.path.exists(path):
        with gzip.open(path, "rt") as fh:
            for line in fh:
                r = json.loads(line); cur[r["game_id"]] = r
    for r in records:
        cur[r["game_id"]] = r
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt", compresslevel=9) as fh:
        for gid in sorted(cur):
            fh.write(json.dumps(cur[gid], separators=(",", ":")) + "\n")
    os.replace(tmp, path)
    return path


def load_all(out_dir: str):
    """iterate every stored game record, oldest day first"""
    for fn in sorted(os.listdir(out_dir)) if os.path.isdir(out_dir) else []:
        if fn.endswith(".jsonl.gz"):
            with gzip.open(os.path.join(out_dir, fn), "rt") as fh:
                for line in fh:
                    yield json.loads(line)


def collect_from_feed(feed, out_dir: str = "artifacts/gamedata") -> int:
    """store every summary the feed fetched in this run; returns number of games written"""
    by_day: dict = {}
    for eid, (d, season, js) in feed.summaries.items():
        try:
            by_day.setdefault(d, []).append(extract(eid, d, season, js))
        except Exception:
            continue
    for d, recs in by_day.items():
        save_day(out_dir, d, recs)
    return sum(len(v) for v in by_day.values())
