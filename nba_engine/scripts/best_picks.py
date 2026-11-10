"""Over/under leans and parlays from the injury-adjusted player projections (player_refresh table, written by scripts/refresh_forecast.py).
Books' lines are not available here, so a stand-in line is used: the player's last-10-game average rounded to the nearest half (books anchor on recent form).
For each player-stat the side (over or under) with the higher model probability at that line is the lean. Probabilities get the bias correction measured by the
calibration check (scripts/player_ladder_calibration.py: the ladders ran high on overs). Parlay probability = product of leg probabilities (legs from
different players; independence is an approximation). Usage: python scripts/best_picks.py [YYYY-MM-DD]  -> artifacts/reports/best_picks_<date>.md"""
import os, sys, re, json, sqlite3
from itertools import combinations
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.players import PlayerModel
from datetime import datetime
from zoneinfo import ZoneInfo
day = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else str(datetime.now(ZoneInfo("America/New_York")).date())
pl = sqlite3.connect("artifacts/player_live.sqlite"); live = sqlite3.connect("artifacts/live.sqlite")
run = pl.execute("select max(run_utc) from player_refresh").fetchone()[0]
rows = pl.execute("select game_id,team,player_id,name,proj_min,p_play,details_json from player_refresh where run_utc=?", (run,)).fetchall()
tm = {g: json.loads(d) for g, d in live.execute("select game_id, details_json from forecasts where model_name='sim_mc'")}
pm = PlayerModel.load("artifacts/player_state.json")
GAP = {}
try:
    t = open("artifacts/reports/player_ladder_calibration_player_ladder_cal.md").read().split("## By stat")[1]
    for m in re.finditer(r"\|\s*(\w+)\s*\|\s*\d+\s*\|\s*[\d.]+\s*\|\s*[\d.]+\s*\|\s*(-?[\d.]+)\s*\|", t): GAP[m.group(1)] = float(m.group(2))
except Exception:
    pass
H = {"pts": ("pts",), "reb": ("reb",), "ast": ("ast",), "stl": ("stl",), "blk": ("blk",), "tov": ("tov",), "tpm": ("tpm",), "fta": ("fta",)}
COMBO = {"pra": ("pts", "reb", "ast"), "pr": ("pts", "reb"), "pa": ("pts", "ast"), "ra": ("reb", "ast")}
LABEL = {"pts": "Points", "reb": "Rebounds", "ast": "Assists", "stl": "Steals", "blk": "Blocks", "tov": "Turnovers", "tpm": "3-pointers made", "fta": "Free-throw attempts",
         "pra": "Pts+Reb+Ast", "pr": "Pts+Reb", "pa": "Pts+Ast", "ra": "Reb+Ast", "fg2m": "2-pointers made"}
legs = []
for gid, team, pid, name, pmin, pp, dj in rows:
    if pp < 0.85 or pmin < 18: continue
    base = pm.baseline_means(pid, 10)
    if base is None: continue
    d = json.loads(dj)
    stats = {**{k: base[k] for k in H}, **{k: sum(base[x] for x in v) for k, v in COMBO.items()}, "fg2m": base["fgm"] - base["tpm"]}
    for k, rec in stats.items():
        x = d.get(k)
        if not x or "ov" not in x: continue
        lo = np.floor(rec) + 0.5; ln = float(lo if abs(rec - lo) <= abs(rec - (lo + 1)) else lo + 1)
        if ln < 0.5: continue
        j = int(ln - 0.5) - x["t0"]; po = 1.0 if j < 0 else (0.01 if j >= len(x["ov"]) else x["ov"][j] / 1000.0)
        po = float(np.clip(po + GAP.get(k, 0.0), 0.02, 0.98))               # actual - predicted over-rate measured on past games
        side, p = ("OVER", po) if po >= 0.5 else ("UNDER", 1 - po)
        if p > 0.75: continue                                              # near-certainties are not lines a book prices at anything worth taking, and extreme model confidence is more likely model error
        if abs(x["m"] - rec) / max(rec, 1.0) > 0.30: continue              # the model and recent form disagree by more than 30%: more likely a model miss than an edge
        if k in ("stl", "blk", "tov") and ln < 1.5: continue               # 0.5 lines on rare events are near coin-flips with heavy juice, skip
        legs.append(dict(gid=gid, team=team, name=name, stat=k, line=ln, side=side, p=p, model=x["m"], recent=rec, pp=pp))
from nbaengine.props import norm, american_to_decimal
def pge(x, k):            # P(stat >= k | plays) from the stored ladder
    j = k - 1 - x["t0"]
    return 1.0 if j < 0 else (0.005 if j >= len(x["ov"]) else x["ov"][j] / 1000.0)
real = []
WBLEND = 0.0
WSTAT = {}
try:
    WSTAT = {k: float(v["w_used"]) for k, v in json.load(open("artifacts/props_blend.json")).get("stats", {}).items()}
except Exception:
    pass
try:
    WBLEND = float(np.clip(json.load(open("artifacts/props_blend.json"))["w"], 0.0, 1.0))        # weight the model has EARNED against the book (backtest on finished games)
except Exception:
    pass
ORIENT_OK = "first=over" in open("artifacts/reports/props_orientation.md").read() if os.path.exists("artifacts/reports/props_orientation.md") else False
lines_in = []                      # (game, player id, stat, line, over price, under price, book)
try:
    for g, pid, stat, line, pa_, pb_ in pl.execute("select e.game_id, e.nba_id, e.stat, e.line, e.price_a, e.price_b from espn_props e join (select game_id, max(fetched_utc) m from espn_props group by game_id) l on l.game_id=e.game_id and l.m=e.fetched_utc where e.nba_id is not null"):
        if ORIENT_OK: lines_in.append((g, int(pid), stat, line, pa_, pb_, "DraftKings via ESPN"))
except sqlite3.OperationalError:
    pass
try:
    for g, pkey, stat, line, po_, pu_, bk in pl.execute("select p.game_id, p.player_key, p.stat, p.line, p.over_price, p.under_price, p.book from prop_lines p join (select game_id, max(fetched_utc) m from prop_lines group by game_id) l on l.game_id=p.game_id and l.m=p.fetched_utc"):
        hit = [r_ for (gg, k_), r_ in {(gg, k_): v for (gg, k_), v in {(gid, norm(name)): (pid,) for gid, team, pid, name, pmin, pp, dj in rows}.items()}.items() if gg == g and k_ == pkey]
        if hit: lines_in.append((g, int(hit[0][0]), stat, line, po_, pu_, bk))
except sqlite3.OperationalError:
    pass
byid = {(gid, pid): (team, pid, name, pmin, pp, json.loads(dj)) for gid, team, pid, name, pmin, pp, dj in rows}
for g, pid, stat, line, op, up, book in lines_in:
    r = byid.get((g, pid))
    if not r: continue
    team, pid, name, pmin, pp, d = r; x = d.get(stat)
    if not x or "ov" not in x or pp < 0.80 or pmin < 15: continue
    if line == int(line):                       # whole-number line: a push refunds the stake
        p_over, p_push = pge(x, int(line) + 1), pge(x, int(line)) - pge(x, int(line) + 1)
    else:
        p_over, p_push = pge(x, int(np.ceil(line))), 0.0
    p_over = float(np.clip(p_over + GAP.get(stat, 0.0), 0.02, 0.98)); do, du = american_to_decimal(op), american_to_decimal(up)
    fair_o = (1 / do) / ((1 / do) + (1 / du))                                    # book's no-vig probability of the over
    p_over_raw = p_over
    p_over = fair_o + WSTAT.get(stat, 0.0) * (p_over - fair_o)                     # shrink toward the book by the weight the model has earned for THIS stat
    p_under = max(0.0, 1.0 - p_over - p_push)
    for side, p, dec, fair in (("OVER", p_over, do, fair_o), ("UNDER", p_under, du, 1 - fair_o)):
        ev = p * (dec - 1) - (1 - p - p_push)                                     # per 1 staked
        praw = p_over_raw if side == "OVER" else max(0.0, 1.0 - p_over_raw - p_push)
        real.append(dict(gid=g, team=team, name=name, stat=stat, line=line, side=side, p=p, dec=dec, ev=ev, fair=fair, book=book, model=x["m"], recent=line,
                         price=(op if side == "OVER" else up), pp=pp, praw=praw))
def fmt(l): return f"{l['name']} ({l['team']}) {l['side']} {l['line']:g} {LABEL[l['stat']]}"
def best_parlay(L, n, max_per_game=9, by_ev=None):
    by_ev = (REAL and not NOEDGE) if by_ev is None else by_ev
    L = sorted(L, key=(lambda l: -l["ev"]) if by_ev else (lambda l: -l["p"])); pick, used, per = [], set(), {}
    for l in L:
        if l["name"] in used or per.get(l["gid"], 0) >= max_per_game: continue
        pick.append(l); used.add(l["name"]); per[l["gid"]] = per.get(l["gid"], 0) + 1
        if len(pick) == n: break
    return pick
prob = lambda P: float(np.prod([l["p"] for l in P]))
pay = lambda P: float(np.prod([l.get("dec", 1.0) for l in P]))
out = [f"# Best over/under leans and parlays (injury-adjusted projections, run {run} UTC)", "",
       "**Read this first.** I do not have sportsbook prop lines, so the line used for each leg is a stand-in: the player's last-10-game average rounded to the nearest half. "
       "Books price off recent form too, so a lean means the model, with the injuries and the opponent, disagrees with recent form. It does not mean there is a +EV bet: "
       "the real line and price may differ, and the model is not proven to beat the market (the market's closing line beat it on team margins). "
       "Check real lines with `python scripts/prop_price.py \"<player>\" <stat> <line>`. Probabilities are shifted by the calibration bias measured so far (the ladders ran high on overs). "
       "A parlay's probability multiplies its legs, treating players as independent; real legs in one game are usually positively linked, so treat it as approximate. "
       "Legs are skipped when the model and recent form differ by more than 30% (more likely a model miss), when the model is more than 75% sure, and for 0.5 steal/block lines. Legs void if the player does not play; only players with P(play) of at least 0.85 and 18+ projected minutes are used.", ""]
REAL = bool(real)
NOEDGE = REAL and max(WSTAT.values(), default=0.0) < 0.05
if REAL:                       # one line per player-stat: DraftKings first, then FanDuel; keep only legs the model rates above the book's fair probability
    pref = {"draftkings": 0, "fanduel": 1}
    best = {}
    for l in sorted(real, key=lambda l: pref.get(l["book"], 9)):
        best.setdefault((l["gid"], l["name"], l["stat"], l["side"]), l)
    if NOEDGE:        # the model has no earned say: list the book's own most likely outcomes (their expected profit is negative by the vig)
        legs = [l for l in best.values() if 0.55 <= l["p"] <= 0.75]
    else:
      legs = [l for l in best.values() if l["ev"] > 0 and 0.52 <= l["p"] <= 0.75 and abs(l["model"] - l["line"]) / max(l["line"], 1.0) <= 0.35]   # above 75% sure against a book is more likely a model miss
    for l in legs: l["recent"] = l["line"]
games = sorted({l["gid"] for l in legs})
if REAL:
    out = [f"# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run {run} UTC)", "",
           "Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). "
           + (f"**Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig. " if NOEDGE else f"The model has earned a weight against the book only on: {', '.join(f'{k} ({v:.2f})' for k, v in WSTAT.items() if v >= 0.05)}. Other stats are held at the book's probability, and every probability is shrunk toward the book by its stat's weight. ") + " For each prop the model's probability for each side is compared with the book: "
           "EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, "
           "and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the "
           "model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs "
           "(players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.", ""]
    HDR = ["| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |", "|---|---|---|---|---|---|"]
    row = lambda l: f"| {fmt(l)} | {l['price']:+.0f} ({l['book']}) | {l['model']:.1f} | {l['p']:.0%} | {l['fair']:.0%} | {l['ev']:+.2f} |"
    tail = lambda P: f"Combined probability {prob(P):.1%}; parlay pays {pay(P):.1f}x; expected profit per 1 staked {prob(P) * pay(P) - 1:+.2f}."
else:
    HDR = ["| Leg | Model proj | Recent avg | Win prob |", "|---|---|---|---|"]
    row = lambda l: f"| {fmt(l)} | {l['model']:.1f} | {l['recent']:.1f} | {l['p']:.0%} |"
    tail = lambda P: f"Combined probability {prob(P):.1%} (fair odds about {1 / max(prob(P), 1e-9):.1f} to 1; a book's payout must beat that for it to be worth anything)."
S = best_parlay(legs, 4, 1); S3 = best_parlay(legs, 3, 1)
if not S:
    out += ["No qualifying legs: no prop lines were available for these games yet (the lines are fetched before tip-off).", ""]
out += ["## Best parlay across the whole slate (4 legs, one per game)", ""] + HDR + [row(l) for l in S] + ["", "**" + tail(S) + "**", "",
        "Safest 3-leg slate parlay: " + "; ".join(fmt(l) + f" ({l['p']:.0%})" for l in S3) + ". " + tail(S3), ""]
if REAL:       # the model's own view: unshrunk probabilities, ranked by the model's expected profit at the book's price
    M = {}
    for l in best.values():
        m = dict(l); m["p"] = m["praw"]; m["ev"] = m["p"] * (m["dec"] - 1) - (1 - m["p"])
        if 0.52 <= m["p"] <= 0.75 and abs(m["model"] - m["line"]) / max(m["line"], 1.0) <= 0.35 and m["ev"] > 0: M[(m["gid"], m["name"], m["stat"], m["side"])] = m
    ML = sorted(M.values(), key=lambda l: -l["ev"])
    out += ["## Our model's own picks (unshrunk model probabilities)", "",
            "These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. "
            "**The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.", ""]
    for n_, ttl in ((2, "Best 2-leg"), (3, "Best 3-leg"), (4, "Best 4-leg")):
        Pm = best_parlay(ML, n_, 1, by_ev=True)
        if len(Pm) == n_:
            out += [f"**{ttl} slate parlay (one leg per game, ranked by model edge)**", ""] + HDR + [row(l) for l in Pm] + ["", tail(Pm), ""]
    out += ["Top single picks by model edge:", ""] + [f"- {fmt(l)}: model {l['p']:.0%} vs book {l['fair']:.0%}, EV {l['ev']:+.2f} at {l['price']:+.0f} (projection {l['model']:.1f})" for l in ML[:12]] + [""]
    for l in ML: pass
for gid in games:
    d = tm.get(gid, {}); L = [l for l in legs if l["gid"] == gid]
    P = best_parlay(L, 3, 9)
    out += [f"## {d.get('away', '?')} at {d.get('home', '?')} (game {gid})", "", "**Best 3-leg parlay for this game:**", ""] + HDR + [row(l) for l in P] + ["", tail(P), "",
           "Top single picks (over or under, whichever the model prefers):", ""] + \
           [f"- {fmt(l)}: {l['p']:.0%}" + (f", EV {l['ev']:+.2f} at {l['price']:+.0f}" if REAL else f" (model {l['model']:.1f} vs recent {l['recent']:.1f})") for l in sorted(L, key=(lambda l: -l["ev"]) if (REAL and not NOEDGE) else (lambda l: -l["p"]))[:8]] + [""]
pl.execute("CREATE TABLE IF NOT EXISTS picks_log(run_utc TEXT, game_id INTEGER, player_id INTEGER, name TEXT, stat TEXT, line REAL, side TEXT, p REAL, model REAL, recent REAL, in_parlay INTEGER, PRIMARY KEY(run_utc, game_id, name, stat))")
inpar = {(l["gid"], l["name"], l["stat"]) for g in games for l in best_parlay([x for x in legs if x["gid"] == g], 3)} | {(l["gid"], l["name"], l["stat"]) for l in S}
try:
    pl.execute("ALTER TABLE picks_log ADD COLUMN price REAL"); pl.execute("ALTER TABLE picks_log ADD COLUMN book TEXT")
except sqlite3.OperationalError:
    pass
for l in legs:      # every lean is logged before the games finish so it can be graded honestly later (scripts/grade_picks.py)
    pl.execute("INSERT OR IGNORE INTO picks_log VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (run, l["gid"], 0, l["name"], l["stat"], l["line"], l["side"], l["p"], l["model"], l["recent"], int((l["gid"], l["name"], l["stat"]) in inpar), l.get("price"), l.get("book")))
pl.commit()
p = f"artifacts/reports/best_picks_{day or 'latest'}.md"; open(p, "w").write("\n".join(out)); print("wrote", p, len(legs), "legs", len(games), "games"); print("\n".join(out[7:20]))
