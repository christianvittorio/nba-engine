"""Sportsbook player-prop lines from The Odds API (https://the-odds-api.com, v4). Needs a free API key in the environment variable ODDS_API_KEY
(never stored in the repo). Credit cost per call = markets x regions per game, so a budget guard stops before the monthly quota runs out.
Lines are stored with their fetch time, so a later grading can use the line that was actually on the board before tip-off."""
import os, re, json, time, sqlite3, unicodedata
from datetime import datetime, timezone
import urllib.request, urllib.parse

BASE = "https://api.the-odds-api.com/v4"
MARKET_STAT = {"player_points": "pts", "player_rebounds": "reb", "player_assists": "ast", "player_threes": "tpm", "player_points_rebounds_assists": "pra",
               "player_points_rebounds": "pr", "player_points_assists": "pa", "player_rebounds_assists": "ra", "player_steals": "stl",
               "player_blocks": "blk", "player_turnovers": "tov", "player_blocks_steals": "sb"}
TEAM_ABBR = {"Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN", "Charlotte Hornets": "CHA", "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE",
             "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN", "Detroit Pistons": "DET", "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND",
             "Los Angeles Clippers": "LAC", "LA Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM", "Miami Heat": "MIA", "Milwaukee Bucks": "MIL",
             "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOP", "New York Knicks": "NYK", "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL",
             "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHX", "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS",
             "Toronto Raptors": "TOR", "Utah Jazz": "UTA", "Washington Wizards": "WAS"}
DDL = """CREATE TABLE IF NOT EXISTS prop_lines(fetched_utc TEXT, game_id INTEGER, event_id TEXT, book TEXT, player TEXT, player_key TEXT, stat TEXT, line REAL,
         over_price REAL, under_price REAL, PRIMARY KEY(fetched_utc, game_id, book, player_key, stat, line))"""


def norm(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'`,-]", " ", s)
    return " ".join(w for w in s.split() if w not in ("jr", "sr", "ii", "iii", "iv"))


def american_to_decimal(a: float) -> float:
    return 1 + a / 100.0 if a > 0 else 1 + 100.0 / abs(a)


def _get(path: str, params: dict):
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as r:
        left = r.headers.get("x-requests-remaining")
        return json.loads(r.read().decode()), (float(left) if left not in (None, "") else None)


def parse_event(js: dict) -> list:
    """Rows (book, player, stat, line, over_price, under_price) from one event's odds response."""
    rows = []
    for bk in js.get("bookmakers", []):
        for mk in bk.get("markets", []):
            stat = MARKET_STAT.get(mk.get("key"))
            if not stat: continue
            pair = {}
            for o in mk.get("outcomes", []):
                key = (o.get("description"), o.get("point"))
                pair.setdefault(key, {})[str(o.get("name")).lower()] = o.get("price")
            for (pname, point), px in pair.items():
                if pname and point is not None and "over" in px and "under" in px:
                    rows.append((bk.get("key"), pname, stat, float(point), float(px["over"]), float(px["under"])))
    return rows


def fetch_slate(db_path: str, games: list, markets: str = "player_points,player_rebounds,player_assists,player_threes,player_points_rebounds_assists",
                books: str = "draftkings,fanduel", reserve: int = 40, key: str | None = None) -> dict:
    """games: [{'game_id', 'home', 'away'}] (abbreviations). Fetches only these games' events. Stops before dipping under `reserve` credits."""
    key = key or os.environ.get("ODDS_API_KEY")
    if not key:
        return {"skipped": "no ODDS_API_KEY set"}
    con = sqlite3.connect(db_path); con.execute(DDL)
    events, left = _get("/sports/basketball_nba/events", {"apiKey": key, "dateFormat": "iso"})          # free: does not use credits
    want = {(g["home"], g["away"]): g["game_id"] for g in games}
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"); n_rows = n_ev = 0; cost = len(markets.split(","))
    for ev in events:
        k = (TEAM_ABBR.get(ev.get("home_team")), TEAM_ABBR.get(ev.get("away_team")))
        gid = want.get(k)
        if gid is None: continue
        if left is not None and left - cost < reserve:
            return {"stopped": f"credit reserve: {left:.0f} left, a game costs {cost}", "events": n_ev, "rows": n_rows}
        js, left = _get(f"/sports/basketball_nba/events/{ev['id']}/odds", {"apiKey": key, "regions": "us", "markets": markets, "oddsFormat": "american", "bookmakers": books})
        for book, player, stat, line, op, up in parse_event(js):
            con.execute("INSERT OR IGNORE INTO prop_lines VALUES(?,?,?,?,?,?,?,?,?,?)", (stamp, gid, ev["id"], book, player, norm(player), stat, line, op, up)); n_rows += 1
        n_ev += 1; time.sleep(0.3)
    con.commit()
    return {"events": n_ev, "rows": n_rows, "credits_left": left, "fetched_utc": stamp}
