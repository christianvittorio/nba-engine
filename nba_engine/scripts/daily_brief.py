"""Plain-English daily brief: for each game, who we expect to win and WHY, in sentences a person can read.
Usage: python scripts/daily_brief.py [YYYY-MM-DD]   -> artifacts/reports/brief_<date>.md
Every sentence comes from a stored number (Elo, team profiles, recent results, injuries, the market line, the player projections); nothing is invented.
The technical per-model listing stays in forecasts_<date>.md."""
import os, sys, json, sqlite3
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
live = sqlite3.connect("artifacts/live.sqlite"); pl = sqlite3.connect("artifacts/player_live.sqlite")
st = json.load(open("artifacts/state.json")); elo = st["elo"]["ratings"]; prof = st["prof"]
NAME = {"ATL": "Hawks", "BOS": "Celtics", "BKN": "Nets", "CHA": "Hornets", "CHI": "Bulls", "CLE": "Cavaliers", "DAL": "Mavericks", "DEN": "Nuggets", "DET": "Pistons", "GSW": "Warriors",
        "HOU": "Rockets", "IND": "Pacers", "LAC": "Clippers", "LAL": "Lakers", "MEM": "Grizzlies", "MIA": "Heat", "MIL": "Bucks", "MIN": "Timberwolves", "NOP": "Pelicans", "NYK": "Knicks",
        "OKC": "Thunder", "ORL": "Magic", "PHI": "76ers", "PHX": "Suns", "POR": "Trail Blazers", "SAC": "Kings", "SAS": "Spurs", "TOR": "Raptors", "UTA": "Jazz", "WAS": "Wizards"}
nm = lambda t: NAME.get(t, t)
day = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else None
if not day:
    day = live.execute("select max(json_extract(details_json,'$.date')) from forecasts where model_name='sim_mc'").fetchone()[0]

# ---- team ratings from the profiles: points per possession and the four factors, ranked 1 (best) to 30
def rates(tab, t):
    x = prof[tab][t]; p = max(x["poss"], 1.0)
    return {"eff": (2 * x["fg2m"] + 3 * x["fg3m"] + x["ftm"]) / p, "tov": x["tov"] / p, "oreb": x["oreb_fg"] / max(x["fgmiss"], 1.0), "ft": x["ftrip"] / p, "three": x["fg3a"] / max(x["fga"], 1.0), "fg3": x["fg3m"] / max(x["fg3a"], 1.0)}
teams = sorted(prof["off"]); OFF = {t: rates("off", t) for t in teams}; DEF = {t: rates("deff", t) for t in teams}
def rank(tab, key, t, high_good=True):
    v = sorted((tab[x][key] for x in teams), reverse=high_good); return v.index(tab[t][key]) + 1
pace = {t: st["prof"]["pace_w"][t][0] / max(st["prof"]["pace_w"][t][1], 1e-9) if st["prof"]["pace_w"].get(t) and st["prof"]["pace_w"][t][1] > 0 else None for t in teams}
erank = {t: i + 1 for i, (t, _) in enumerate(sorted(elo.items(), key=lambda x: -x[1]))}
ord_ = lambda n: f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"

# ---- results this season: record and recent margins
G = live.execute("select g.game_id, g.home, g.away, r.home_pts, r.away_pts from games g join results r on r.game_id=g.game_id and r.season=g.season where g.season=(select max(season) from games) order by g.seq").fetchall()
hist = {}
for gid, h, a, hp, ap in G:
    hist.setdefault(h, []).append(hp - ap); hist.setdefault(a, []).append(ap - hp)
def form(t):
    m = hist.get(t, [])
    if not m: return None
    w = sum(1 for x in m if x > 0); l5 = m[-5:]
    return dict(rec=f"{w}-{len(m) - w}", n=len(m), l5=f"{sum(1 for x in l5 if x > 0)}-{sum(1 for x in l5 if x <= 0)}", avg5=float(np.mean(l5)), avg=float(np.mean(m)))

# ---- forecasts for the day
def latest(model):
    q = "select f.game_id, f.p_home, f.mean_home, f.mean_away, f.q_margin_json, f.details_json from forecasts f join (select game_id, max(forecast_id) m from forecasts where model_name=? and json_extract(details_json,'$.date')=? group by game_id) l on l.m=f.forecast_id"
    return {r[0]: r[1:] for r in live.execute(q, (model, day))}
M, AV = latest("sim_mc"), latest("sim_mc_av")
BL = latest("blend_v2")
ALL = latest("sim_mc_all"); RST = latest("sim_mc_rest")
CUR = json.load(open("artifacts/availability.json"))["teams"] if os.path.exists("artifacts/availability.json") else {}
if not M:
    print("no forecasts for", day); sys.exit(0)
ref_run = pl.execute("select max(run_utc) from player_refresh").fetchone()[0]
stars = {}
for g, t, name, pm, pp, dj in pl.execute("select game_id, team, name, proj_min, p_play, details_json from player_refresh where run_utc=?", (ref_run,)):
    pts = json.loads(dj).get("pts", {}).get("m")
    if pts is not None: stars.setdefault((g, t), []).append((name, float(pts), float(pp), float(pm)))

lvl = lambda v: "key player" if v >= 4 else ("rotation player" if v >= 1.5 else "minor role")
def edge_lines(att, dfn):
    """strongest style advantages of attacking team `att` against defence of `dfn` (rank 1 = best; gap of 8+ places counts as an edge)"""
    out = []
    r1, r2 = rank(OFF, "eff", att), rank(DEF, "eff", dfn, False)
    if r1 <= 8 and r2 <= 8: out.append(f"a top-8 offence ({ord_(r1)} in points per possession) running into a top-8 defence ({ord_(r2)}), so scoring should be hard-earned")
    elif r1 <= 8 and r2 >= 20: out.append(f"{nm(att)} have a top-8 offence ({ord_(r1)}) against a defence that ranks {ord_(r2)}")
    elif r1 >= 20 and r2 <= 8: out.append(f"{nm(att)} have a weak offence ({ord_(r1)}) against a top-8 defence ({ord_(r2)})")
    elif r1 >= 20 and r2 >= 20: out.append(f"two leaky matchups for the scorers: {nm(att)}'s offence ranks {ord_(r1)} and {nm(dfn)}'s defence {ord_(r2)}")
    for key, hi, label in (("tov", False, "turnovers"), ("oreb", True, "offensive rebounding"), ("ft", True, "getting to the free-throw line"), ("fg3", True, "3-point shooting")):
        a = rank(OFF, key, att, hi); d = rank(DEF, key, dfn, not hi)       # defence rank: 1 = forces/limits most
        if key == "tov": a_good, d_good = a <= 8, d <= 8              # lowest turnover rate on offence; defence that forces most (highest opp tov rate)
        if key == "tov":
            d = rank(DEF, "tov", dfn, True); a = rank(OFF, "tov", att, False)
            if a <= 8 and d >= 20: out.append(f"{nm(att)} protect the ball well ({ord_(a)} in turnover rate) and {nm(dfn)} rarely force turnovers ({ord_(d)})")
            elif a >= 23 and d <= 8: out.append(f"{nm(att)} are turnover-prone ({ord_(a)}) and {nm(dfn)} force a lot of them ({ord_(d)})")
        else:
            d = rank(DEF, key, dfn, False)                               # 1 = allows the least
            if a <= 8 and d >= 20: out.append(f"{nm(att)} are strong at {label} ({ord_(a)}) and {nm(dfn)} are weak at stopping it ({ord_(d)})")
            elif a >= 23 and d <= 8: out.append(f"{nm(att)} are poor at {label} ({ord_(a)}) and {nm(dfn)} are good at stopping it ({ord_(d)})")
    return out[:3]

lines = [f"# NBA forecast brief for {day}", "",
         "Plain-English reasons behind each forecast. Every claim comes from the model's own numbers (ratings, team style profiles, recent results, injuries, the betting line). "
         "The technical per-model numbers are in `forecasts_" + day + ".md`. Ranks run 1 (best) to 30. Early in a season ranks lean on last year's data, so treat them loosely.", ""]
if os.path.exists("artifacts/lessons_latest.md"):
    les = open("artifacts/lessons_latest.md").read().strip()
    if les: lines += ["## What the latest results taught us", "", "From the most recent end-of-day review. Items under 'What changes next' are the adjustments the engine is learning from the data.", "", les, ""]
for gid, (ph, mh, ma, qj, dj) in sorted(M.items(), key=lambda kv: json.loads(kv[1][4]).get("tip_utc", "")):
    d = json.loads(dj); H, A = d["home"], d["away"]
    ph_raw, mh_raw, ma_raw = ph, mh, ma
    adj = gid in ALL
    if adj: ph, mh, ma, qj = ALL[gid][0], ALL[gid][1], ALL[gid][2], ALL[gid][3]      # lead with the forecast that includes rest, injuries and sitting risk
    fav, dog, pf = (H, A, ph) if ph >= 0.5 else (A, H, 1 - ph)
    pf_home = fav == H
    margin = abs(mh - ma)
    conf = "a clear favourite" if pf >= 0.75 else ("a solid favourite" if pf >= 0.62 else ("a slight favourite" if pf >= 0.53 else "a coin flip"))
    head = f"## {nm(A)} at {nm(H)}: " + (f"{nm(fav)} favoured ({pf:.0%})" if pf >= 0.53 else "too close to call")
    lines += [head, "", (f"**Forecast basis:** adjusted for rest, injuries and rest-day risk. The unadjusted simulation says {nm(H if ph_raw >= 0.5 else A)} {max(ph_raw, 1 - ph_raw):.0%} (projected {nm(A)} {ma_raw:.0f}, {nm(H)} {mh_raw:.0f}).\n" if adj else ""), f"**Projected final:** {nm(A)} {ma:.0f}, {nm(H)} {mh:.0f} (the average outcome; total {mh + ma:.0f}). {nm(fav)} are {conf}" + (f", about {margin:.1f} points ahead on average." if pf >= 0.53 else f"; the model sees them about {margin:.1f} points apart.")]
    why = []
    if gid in BL:
        pb = BL[gid][0]; why.append(f"**Blended view.** Mixing the simulation with the updated Elo (home advantage 45, the modern setting) gives {nm(H) if pb >= 0.5 else nm(A)} a {max(pb, 1 - pb):.0%} chance. This blend is the better-scoring forecast in testing (log-loss 0.610 vs 0.616 for the simulation alone).")
    ef, ed = elo[fav], elo[dog]
    why.append(f"**Team strength.** {nm(fav)} are rated {ef:.0f} ({ord_(erank[fav])} of 30) against {nm(dog)} at {ed:.0f} ({ord_(erank[dog])})."
               + f" Home court is worth roughly 3 points to {nm(H)}.")
    ff, fd = form(fav), form(dog)
    if ff and fd:
        why.append(f"**Recent form.** {nm(fav)} are {ff['rec']} this season, {ff['l5']} in their last five (average margin {ff['avg5']:+.1f}). {nm(dog)} are {fd['rec']}, {fd['l5']} in their last five ({fd['avg5']:+.1f}).")
    e1 = edge_lines(fav, dog); e2 = edge_lines(dog, fav)
    if e1 or e2:
        why.append("**Style matchup.** " + "; ".join([x[0].upper() + x[1:] for x in e1[:2]] + [x[0].upper() + x[1:] for x in e2[:1]]) + ".")
    pc = (pace.get(H), pace.get(A))
    mp = d.get("mean_poss")
    if mp: why.append(f"**Pace.** The model expects about {mp:.0f} possessions, " + ("a fast game" if mp >= 100 else ("a slow game" if mp <= 96 else "a typical pace")) + ", which sets the scoring environment.")
    rs = RST.get(gid)
    if rs:
        rd = json.loads(rs[4]); b2h, b2a = rd.get("home_b2b"), rd.get("away_b2b")
        if b2h or b2a:
            who = [nm(x) for x, f in ((H, b2h), (A, b2a)) if f]
            why.append(f"**Rest.** {' and '.join(who)} {'play' if len(who) == 1 else 'both play'} the second night of a back-to-back; the rest adjustment moves the margin by {abs(rd.get('shift', 0)):.1f} points toward {nm(A if (b2h and not b2a) else H) if (b2h != b2a) else 'neither team'}.")
    def cur(t_):
        inj = (CUR.get(t_) or {}).get("injuries") or []
        return [i["name"] for i in inj if i["status"] in ("Out", "Doubtful")], [f'{i["name"]} ({i["status"].lower()})' for i in inj if i["status"] not in ("Out", "Doubtful")]
    if CUR:
        ho_, hq_ = cur(H); ao_, aq_ = cur(A)
        segs = []
        for t_, o_, q_ in ((H, ho_, hq_), (A, ao_, aq_)):
            if o_ or q_: segs.append(f"{nm(t_)}: " + ("out " + ", ".join(o_) if o_ else "") + ("; " if o_ and q_ else "") + ("uncertain " + ", ".join(q_) if q_ else ""))
        why.append("**Injury report (latest).** " + (" | ".join(segs) if segs else "no one listed out on either side") + ". Both teams' absences are counted, so a depleted opponent does not help if your own side is thin too.")
    av = AV.get(gid)
    if av and not CUR:
        ad = json.loads(av[4]); ho, ao = ad.get("home_out") or [], ad.get("away_out") or []
        parts = []
        if ho: parts.append(f"{nm(H)} without " + ", ".join(f"{n} ({lvl(v)})" for n, v in ho))
        if ao: parts.append(f"{nm(A)} without " + ", ".join(f"{n} ({lvl(v)})" for n, v in ao))
        if parts: why.append("**Injuries.** " + "; ".join(parts) + f". Effect on expected scoring: {nm(H)} {ad.get('home_pts_shift', 0):+.1f}, {nm(A)} {ad.get('away_pts_shift', 0):+.1f} points.")
        else: why.append("**Injuries.** No rotation players are listed out on either side.")
    mk = (d.get("market") or {}).get("snapshot") or {}
    try:
        line = -float(mk["pointSpread"]["home"]["close"]["line"]); tl = float(mk["overUnder"])
        diff = (mh - ma) - line
        agree = "agrees closely with" if abs(diff) < 2 else ("is more favourable to the home team than" if diff > 0 else "is less favourable to the home team than")
        why.append(f"**The betting line.** DraftKings makes {nm(H if line > 0 else A)} {abs(line):.1f}-point favourites with a total of {tl:g}; our model has {nm(H if mh > ma else A)} by {abs(mh - ma):.1f}, which {agree} the market. "
                   + ("When we differ by this much the book has usually been closer, so lean toward the line." if abs(diff) >= 4 else ""))
    except Exception:
        pass
    for t in (fav, dog):
        s = sorted(stars.get((gid, t), []), key=lambda x: -x[1] * x[2])[:2]
        if s: why.append(f"**{nm(t)} to watch.** " + ", ".join(f"{n} (projected {p:.0f} pts{'' if pp >= 0.85 else f', {pp:.0%} to play'})" for n, p, pp, _ in s) + ".")
    lines += [""] + [f"- {w}" for w in why]
    q = json.loads(qj) if qj else None
    rng_ = f"between {nm(A)} by {-q['10'] if q['10'] < 0 else 0:.0f} and {nm(H)} by {q['90']:.0f}" if q else ""
    lo, hi = (q["10"], q["90"]) if q else (0, 0)
    rng_ = (f"the final margin lands between {nm(A)} by {-lo:.0f} and {nm(H)} by {hi:.0f}" if lo < 0 < hi else (f"the final margin lands between {nm(H)} by {lo:.0f} and {hi:.0f}" if lo >= 0 else f"the final margin lands between {nm(A)} by {-hi:.0f} and {-lo:.0f}")) if q else ""
    lines += ["", f"**What could go wrong:** in the middle 80% of the 10,000 simulations {rng_}, so an upset is always live" + (f" ({1 - pf:.0%} for {nm(dog)})" if pf >= 0.53 else "") + ".", ""]
open(f"artifacts/reports/brief_{day}.md", "w").write("\n".join(lines))
print("wrote", f"artifacts/reports/brief_{day}.md")
