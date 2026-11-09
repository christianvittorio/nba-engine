"""Daily player projections in betting-market form: every stat a book offers, per game and player.
Usage: python scripts/player_projections_report.py [YYYY-MM-DD]  -> artifacts/reports/player_projections_<date>.md
Means come from the player simulation; 2-pointers, PRA and the other combos are sums of the same simulated stats. 25-75% ranges where stored."""
import os, sys, json, sqlite3
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
day = sys.argv[1] if len(sys.argv) > 1 else None
live = sqlite3.connect(f"{ROOT}/artifacts/live.sqlite"); pl = sqlite3.connect(f"{ROOT}/artifacts/player_live.sqlite")
if day is None:
    day = live.execute("select max(date) from game_dates").fetchone()[0]
games = [r[0] for r in live.execute("select game_id from game_dates where date=? order by game_id", (day,))]
teams = {}
for gid, det in live.execute("select game_id, details_json from forecasts where model_name='sim_mc'"):
    d = json.loads(det); teams[gid] = (d.get("away"), d.get("home"))
m = lambda d, k: d[k]["m"] if k in d else 0.0
def p_over(d, k, line):
    """P(stat > line | he plays) from the stored ladder; None for older forecasts without one"""
    x = d.get(k) or {}
    if "ov" not in x: return None
    j = int(line - 0.5) - x["t0"]
    return 1.0 if j < 0 else (0.01 if j >= len(x["ov"]) else x["ov"][j] / 1000.0)
PROPS = [("pts", "PTS"), ("reb", "REB"), ("ast", "AST"), ("pra", "PRA"), ("tpm", "3PM"), ("fg2m", "2PM"), ("fta", "FTA"), ("stl", "STL"), ("tov", "TOV"), ("pr", "P+R"), ("pa", "P+A"), ("ra", "R+A")]
rng = lambda d, k: f"{d[k]['q'][2]:.0f}-{d[k]['q'][4]:.0f}"
out = [f"# Player projections for {day}", "Means from the player simulation (2PM/2PA, PRA and combos are sums of the same simulated stats). Pts/Reb/Ast/3PM show the middle-50% range. p_play = chance the player is in the game.", ""]
for gid in games:
    rows = pl.execute("select team,name,proj_min,p_play,details_json from player_fc where game_id=? order by team, proj_min*p_play desc", (gid,)).fetchall()
    if not rows: continue
    a, h = teams.get(gid, ("?", "?"))
    out += [f"## {a} at {h} (game {gid})", "",
            "| Player | Tm | Min | P(play) | PTS | REB | AST | PRA | 3PM | 3PA | FGM | FGA | 2PM | 2PA | FTM | FTA | STL | BLK | S+B | TOV | P+R | P+A | R+A |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for team, name, pm, pp, dj in rows:
        d = json.loads(dj)
        if pp < 0.15 or pm < 5: continue
        f = lambda k: f"{m(d, k):.1f}"
        pts, reb, ast = m(d, "pts"), m(d, "reb"), m(d, "ast")
        out.append(f"| {name} | {team} | {pm:.0f} | {pp:.2f} | {pts:.1f} ({rng(d,'pts')}) | {reb:.1f} ({rng(d,'reb')}) | {ast:.1f} ({rng(d,'ast')}) | {pts+reb+ast:.1f} | "
                   f"{m(d,'tpm'):.1f} ({rng(d,'tpm')}) | {f('tpa')} | {f('fgm')} | {f('fga')} | {m(d,'fgm')-m(d,'tpm'):.1f} | {m(d,'fga')-m(d,'tpa'):.1f} | {f('ftm')} | {f('fta')} | "
                   f"{f('stl')} | {f('blk')} | {m(d,'stl')+m(d,'blk'):.1f} | {f('tov')} | {pts+reb:.1f} | {pts+ast:.1f} | {reb+ast:.1f} |")
    out.append("")
    ov_rows = []
    for team, name, pm, pp, dj in rows:
        d = json.loads(dj)
        if pp < 0.15 or pm < 5 or "ov" not in (d.get("pts") or {}): continue
        cells = []
        for k, _ in PROPS:
            ln = int(m(d, k)) + 0.5; po = p_over(d, k, ln)
            cells.append(f"o{ln:g} {po:.0%}")
        ov_rows.append(f"| {name} | {team} | " + " | ".join(cells) + " |")
    if ov_rows:
        out += [f"**Over probabilities, {a} at {h}** (at the half-line just above each projection, given the player plays; any other line is priced with `scripts/prop_price.py`)", "",
                "| Player | Tm | " + " | ".join(n for _, n in PROPS) + " |", "|---|---|" + "---|" * len(PROPS)] + ov_rows + [""]
p = f"{ROOT}/artifacts/reports/player_projections_{day}.md"; open(p, "w").write("\n".join(out)); print("wrote", p, len(out), "lines")
