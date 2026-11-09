"""Keyless DraftKings player props from ESPN's odds feed (same unofficial ESPN JSON the rest of the engine reads; no account or key).
Each prop line is two adjacent items (athlete, market, same line, two prices) and the feed does NOT label which is the over: both prices are stored in
the order given (price_a first, price_b second) and the orientation is verified against finished games before any pick relies on it
(scripts/props_orientation.py)."""
import json, time, sqlite3, urllib.request
from datetime import datetime, timezone
CORE = "https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/events/{e}/competitions/{e}/odds/100/propBets?lang=en&region=us&limit=200&page={p}"
TYPE_STAT = {"1": "pts", "2": "ast", "3": "reb", "4": "tpm", "5": "stl", "6": "blk"}
DDL = """CREATE TABLE IF NOT EXISTS espn_props(fetched_utc TEXT, game_id INTEGER, espn_athlete INTEGER, nba_id INTEGER, name TEXT, stat TEXT, line REAL,
         price_a REAL, price_b REAL, open_line REAL, updated TEXT, PRIMARY KEY(fetched_utc, game_id, espn_athlete, stat, line))"""


def _get(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())


def fetch_event(eid: int, roster: dict) -> list:
    """Rows (espn_athlete, nba_id, name, stat, line, price_a, price_b, open_line, updated) for one game. roster: espn athlete id -> (nba_id, name)."""
    items, page, pages = [], 1, 1
    while page <= pages:
        js = _get(CORE.format(e=eid, p=page)); pages = int(js.get("pageCount") or 1); items += js.get("items") or []; page += 1; time.sleep(0.2)
    rows, i = [], 0
    while i + 1 < len(items):
        a, b = items[i], items[i + 1]
        t = (a.get("type") or {}).get("id")
        try:
            ida = int(a["athlete"]["$ref"].split("/athletes/")[1].split("?")[0]); idb = int(b["athlete"]["$ref"].split("/athletes/")[1].split("?")[0])
            la, lb = float(a["current"]["target"]["value"]), float(b["current"]["target"]["value"])
        except Exception:
            i += 1; continue
        if t in TYPE_STAT and ida == idb and (b.get("type") or {}).get("id") == t and la == lb:
            nid, nm = roster.get(ida, (None, None))
            try:
                rows.append((ida, nid, nm, TYPE_STAT[t], la, float(a["odds"]["american"]["value"]), float(b["odds"]["american"]["value"]),
                             float(a["open"]["target"]["value"]), a.get("lastUpdated")))
            except Exception:
                pass
            i += 2
        else:
            i += 1
    return rows


def store(db_path: str, game_id: int, rows: list) -> int:
    con = sqlite3.connect(db_path); con.execute(DDL); stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for r in rows:
        con.execute("INSERT OR IGNORE INTO espn_props VALUES(?,?,?,?,?,?,?,?,?,?,?)", (stamp, game_id) + tuple(r))
    con.commit(); con.close(); return len(rows)
