"""Current rosters and injury statuses from ESPN's public JSON, saved as artifacts/availability.json.

Safety rules:
* Never raises into the caller: every problem is recorded in the output's "problems" list.
* Read-only with respect to the forecasting model. Nothing here changes a forecast; the dashboard uses it to
  pre-fill who is on a team and who is listed as out, and the user can override both.
* ESPN's injury list is a convenience, not an official report. Its completeness and freshness are unverified.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from datetime import datetime, timezone

from .feed import nba_code

SUFFIX = {"jr", "sr", "ii", "iii", "iv", "v"}


def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z ]", "", s.lower().replace(".", "").replace("'", "").replace("-", " "))
    return " ".join(w for w in s.split() if w not in SUFFIX)


def _team_ids(feed) -> dict:
    js = feed._get(f"{feed.BASE}/teams?limit=40")
    out = {}
    for sp in js.get("sports", []):
        for lg in sp.get("leagues", []):
            for t in lg.get("teams", []):
                t = t.get("team", t)
                out[nba_code(t["abbreviation"])] = str(t["id"])
    return out


def _athletes(js: dict) -> list:
    """Roster endpoints return either a flat list of athletes or groups with 'items'."""
    res = []
    for a in js.get("athletes", []):
        if isinstance(a, dict) and "items" in a:
            res += a["items"]
        else:
            res.append(a)
    return res


def _short_key(name: str) -> str:
    """'Luka Doncic' and 'L. Doncic' both become 'l doncic' (first initial + the rest of the name)."""
    parts = norm_name(name).split()
    if len(parts) < 2:
        return ""
    return parts[0][0] + " " + " ".join(parts[1:])


def _model_index(player_state_path: str) -> dict:
    """short key -> [(NBA person id, games played, last team)] for every player the model knows."""
    if not player_state_path or not os.path.exists(player_state_path):
        return {}
    d = json.load(open(player_state_path))
    idx: dict = {}
    for pid, nm in d.get("names", {}).items():
        st = d["pl"].get(pid, {})
        k = _short_key(nm)
        if k:
            idx.setdefault(k, []).append((int(pid), st.get("n", 0), st.get("team")))
    return idx


def _resolve(idx: dict, name: str, team: str):
    """Match by initial+surname. Same-name players are split by last known team; unresolved ambiguity returns None."""
    c = idx.get(_short_key(name), [])
    if len(c) == 1:
        return c[0][0]
    same_team = [x for x in c if x[2] == team]
    if len(same_team) == 1:
        return same_team[0][0]
    pool = sorted(same_team or c, key=lambda x: -x[1])
    if len(pool) >= 2 and pool[0][1] >= 3 * max(pool[1][1], 1):      # one clearly established player with that initial+surname
        return pool[0][0]
    return None


def build_availability(feed, teams: list | None = None, player_state_path: str | None = None) -> dict:
    out = {"generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "source": "ESPN public JSON (unofficial; completeness and freshness unverified)",
           "teams": {}, "unmatched_roster_names": [], "problems": [], "probe": {}}
    idx = _model_index(player_state_path)
    ov_path = os.path.join(os.path.dirname(player_state_path or "."), "name_overrides.json")
    overrides = json.load(open(ov_path)) if os.path.exists(ov_path) else {}     # {"<espn athlete id>": <NBA person id>}
    map_path = os.path.join(os.path.dirname(player_state_path or "."), "player_id_map.json")
    idmap = json.load(open(map_path)) if os.path.exists(map_path) else {}       # written by the player update
    try:
        ids = _team_ids(feed)
    except Exception as ex:
        out["problems"].append(f"teams: {type(ex).__name__}: {ex}")
        return out
    wanted = [t for t in (teams or sorted(ids)) if t in ids]
    embedded = []
    by_espn_id = {}
    for code in wanted:
        try:
            js = feed._get(f"{feed.BASE}/teams/{ids[code]}/roster")
            if not out["probe"]:
                out["probe"] = {"roster_top_keys": sorted(js.keys()), "first_athlete_keys": sorted((_athletes(js) or [{}])[0].keys())}
            roster = []
            for a in _athletes(js):
                name = a.get("displayName") or a.get("fullName") or ""
                pos = (a.get("position") or {}).get("abbreviation")
                nid = overrides.get(str(a.get("id"))) or idmap.get(str(a.get("id"))) or _resolve(idx, name, code)
                if nid is None:
                    out["unmatched_roster_names"].append(f"{code}:{name}")
                row = {"espn_id": str(a.get("id")), "name": name, "pos": pos, "nba_id": nid}
                for inj in (a.get("injuries") or []):
                    if not isinstance(inj, dict):
                        continue
                    stx = inj.get("status") or (inj.get("type") or {}).get("description") or (inj.get("type") or {}).get("name")
                    embedded.append((code, row, stx, (inj.get("shortComment") or inj.get("longComment") or "")[:160], inj.get("date")))
                    if "embedded_injury_sample" not in out["probe"]:
                        out["probe"]["embedded_injury_sample"] = {k: (v if not isinstance(v, (dict, list)) else "<" + type(v).__name__ + ">") for k, v in list(inj.items())[:8]}
                roster.append(row)
                by_espn_id[row["espn_id"]] = (code, row)
            out["teams"][code] = {"roster": roster, "injuries": []}
        except Exception as ex:
            out["problems"].append(f"roster {code}: {type(ex).__name__}: {ex}")
    try:
        js = feed._get(f"{feed.BASE}/injuries")
        out["probe"]["injuries_top_keys"] = sorted(js.keys())
        out["probe"]["injuries_endpoint_teams"] = len(js.get("injuries", []))
        out["probe"]["injuries_endpoint_entries"] = sum(len(te.get("injuries", [])) for te in js.get("injuries", []))
        for te in js.get("injuries", []):
            for inj in te.get("injuries", []):
                ath = inj.get("athlete") or {}
                eid = str(ath.get("id"))
                hit = by_espn_id.get(eid)
                if hit is None:
                    continue                     # not on a roster we fetched (or id mismatch): skip rather than guess
                code, row = hit
                out["teams"][code]["injuries"].append({
                    "name": row["name"], "nba_id": row["nba_id"], "status": inj.get("status"),
                    "detail": (inj.get("shortComment") or (inj.get("details") or {}).get("type") or "")[:160],
                    "date": inj.get("date")})
    except Exception as ex:
        out["problems"].append(f"injuries: {type(ex).__name__}: {ex}")
    seen = {(c, i["name"]) for c, t in out["teams"].items() for i in t["injuries"]}
    for code, row, stx, detail, date in embedded:          # injuries listed on the roster itself
        if (code, row["name"]) not in seen and code in out["teams"]:
            out["teams"][code]["injuries"].append({"name": row["name"], "nba_id": row["nba_id"], "status": stx, "detail": detail, "date": date})
    out["probe"]["embedded_injuries"] = len(embedded)
    return out


def save_availability(av: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path + ".tmp", "w") as f:
        json.dump(av, f, indent=1)
    os.replace(path + ".tmp", path)
