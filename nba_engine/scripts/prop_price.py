"""Price a betting line from the stored player simulation.
Usage: python scripts/prop_price.py "<player name part>" <stat> <line> [date]
stat: pts reb ast stl blk tov tpm tpa fgm fga fg2m fg2a ftm fta pra pr pa ra sb.  Prints P(over), P(under) given the player plays."""
import os, sys, json, sqlite3
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from nbaengine.player_live import with_ladder as WL
name, stat, line = sys.argv[1], sys.argv[2], float(sys.argv[3])
live = sqlite3.connect(f"{ROOT}/artifacts/live.sqlite"); pl = sqlite3.connect(f"{ROOT}/artifacts/player_live.sqlite")
day = sys.argv[4] if len(sys.argv) > 4 else live.execute("select max(date) from game_dates").fetchone()[0]
gids = [r[0] for r in live.execute("select game_id from game_dates where date=?", (day,))]
found = False
for gid in gids:
    for nm, team, pp, dj, pid in pl.execute("select name,team,p_play,details_json,player_id from player_fc where game_id=? and name like ?", (gid, f"%{name}%")):
        x = WL(pl, gid, pid, json.loads(dj)).get(stat); found = True
        if not x or "ov" not in x: print(nm, team, "no ladder stored for", stat, "(forecast predates ladders)"); continue
        j = int(line - 0.5) - x["t0"]; po = 1.0 if j < 0 else (0.01 if j >= len(x["ov"]) else x["ov"][j] / 1000.0)
        print(f"{nm} ({team}) {stat} line {line:g}: projection {x['m']:.1f}; P(over) {po:.1%}, P(under) {1-po:.1%}; chance he plays {pp:.0%}")
if not found: print("no forecast found for", name, "on", day)
