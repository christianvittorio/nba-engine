"""End-of-day review: what the engine forecast vs what happened, and what it should learn from it.
Usage: python scripts/daily_review.py [YYYY-MM-DD]   (US Eastern game date; empty = latest date with finished games)
Writes artifacts/reports/review_<date>.md, appends one row per game/stat to review_log tables (player_live.sqlite, idempotent), and
refreshes artifacts/learned_biases.json (season-to-date bias per stat with its standard error, plus per-team margin residuals).
Nothing here changes a stored forecast. Only flagged, statistically supported biases are reported as lessons; small ones are noise."""
import os, sys, json, sqlite3
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.mdtable import md_table
pd.DataFrame.to_markdown = lambda self, *a, **k: md_table(self, index=False)
live = sqlite3.connect("artifacts/live.sqlite"); pl = sqlite3.connect("artifacts/player_live.sqlite")
pl.executescript("""create table if not exists review_game(game_id integer primary key, date text, home text, away text, p_home real, mean_margin real, mean_total real,
  act_margin real, act_total real, mkt_margin real, mkt_total real);
create table if not exists review_player(game_id integer, player_id integer, name text, team text, stat text, proj real, act real, primary key(game_id, player_id, stat));""")

# ---- team side
F = pd.read_sql_query("select f.game_id, f.p_home, f.mean_margin, f.mean_total, f.details_json from forecasts f join (select game_id, max(forecast_id) m from forecasts where model_name='sim_mc' group by game_id) l on l.m=f.forecast_id", live)
R = pd.read_sql_query("select game_id, home_pts, away_pts from results", live)
T = F.merge(R, on="game_id")
def det(r):
    d = json.loads(r); mk = (d.get("market") or {}).get("snapshot") or {}
    try: ln = float(mk["pointSpread"]["home"]["close"]["line"]); mm = -ln
    except Exception: mm = np.nan
    try: tl = float(mk["overUnder"])
    except Exception: tl = np.nan
    return pd.Series({"date": d.get("date"), "home": d.get("home"), "away": d.get("away"), "mkt_margin": mm, "mkt_total": tl})
T = pd.concat([T, T.details_json.apply(det)], axis=1)
T["act_margin"] = T.home_pts - T.away_pts; T["act_total"] = T.home_pts + T.away_pts
for r in T.itertuples():
    pl.execute("insert or replace into review_game values (?,?,?,?,?,?,?,?,?,?,?)", (int(r.game_id), r.date, r.home, r.away, float(r.p_home), float(r.mean_margin), float(r.mean_total), float(r.act_margin), float(r.act_total),
               None if np.isnan(r.mkt_margin) else float(r.mkt_margin), None if np.isnan(r.mkt_total) else float(r.mkt_total)))
pl.commit()
day = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else str(T.date.max())
D = T[T.date == day].copy()
if D.empty:
    print("no finished games for", day); sys.exit(0)
D["err_margin"] = D.mean_margin - D.act_margin; D["err_total"] = D.mean_total - D.act_total
D["win"] = (D.act_margin > 0).astype(float); D["brier"] = (D.p_home - D.win) ** 2
D["mkt_err_margin"] = D.mkt_margin - D.act_margin; D["mkt_err_total"] = D.mkt_total - D.act_total
md = [f"# End-of-day review, {day}", "",
      f"{len(D)} finished games. Everything below compares what the engine forecast before tip-off with what happened.", "", "## Team forecasts", ""]
tb = D[["away", "home", "mean_margin", "act_margin", "err_margin", "mean_total", "act_total", "err_total", "p_home", "mkt_margin"]].copy()
tb.columns = ["away", "home", "pred margin", "actual margin", "error", "pred total", "actual total", "error ", "P(home)", "DK margin"]
md += [tb.round(1).to_markdown(), ""]
ok = D.dropna(subset=["mkt_margin"])
md += [f"- Winner called right: {int(((D.p_home > .5) == (D.win == 1)).sum())} of {len(D)}. Brier {D.brier.mean():.3f} (0.25 = coin flip).",
       f"- Margin error (our projection minus actual): mean {D.err_margin.mean():+.1f}, typical miss {D.err_margin.abs().mean():.1f}. Total error: mean {D.err_total.mean():+.1f}, typical miss {D.err_total.abs().mean():.1f}."]
if len(ok):
    md += [f"- Against the DraftKings closing line on the same games: our typical margin miss {ok.err_margin.abs().mean():.1f} vs the book's {ok.mkt_err_margin.abs().mean():.1f}; total {ok.err_total.abs().mean():.1f} vs {ok.mkt_err_total.abs().mean():.1f}."]
worst = D.reindex(D.err_margin.abs().sort_values(ascending=False).index).head(3)
md += ["- Biggest misses: " + "; ".join(f"{r.away} at {r.home} (projected {r.mean_margin:+.1f}, actual {r.act_margin:+.0f}" + (f", book {r.mkt_margin:+.1f}" if not np.isnan(r.mkt_margin) else "") + ")" for r in worst.itertuples()), ""]

WHY_AT = len(md)
# ---- season to date (all finished games): is there a bias we can trust?
S = T.copy(); S["em"] = S.mean_margin - S.act_margin; S["et"] = S.mean_total - S.act_total
learned = {"games": int(len(S)), "margin_bias": [float(S.em.mean()), float(S.em.std() / np.sqrt(len(S)))], "total_bias": [float(S.et.mean()), float(S.et.std() / np.sqrt(len(S)))], "player": {}, "teams": {}}
md += ["## Season to date (bias only counts when it is bigger than its standard error)", "",
       f"- Margin bias {learned['margin_bias'][0]:+.2f} ± {learned['margin_bias'][1]:.2f} over {len(S)} games; total bias {learned['total_bias'][0]:+.2f} ± {learned['total_bias'][1]:.2f}."]
rows = []
for team in sorted(set(S.home) | set(S.away)):
    e = list(S[S.home == team].em) + list(-S[S.away == team].em)         # + = we overrated the team
    if len(e) >= 5:
        se = float(np.std(e) / np.sqrt(len(e))); rows.append((team, len(e), -float(np.mean(e)), se))      # reported as actual minus projected
        learned["teams"][team] = [rows[-1][2], se, len(e)]
flag = [r for r in rows if abs(r[2]) > 2 * r[3] and abs(r[2]) >= 2.0]
md += ["- Teams the engine is persistently wrong about (actual margin minus projected, more than 2 standard errors from zero): " + ("; ".join(f"{t} {m:+.1f} ± {s:.1f} over {n} games" + (" (we underrate them)" if m > 0 else " (we overrate them)") for t, n, m, s in sorted(flag, key=lambda r: -abs(r[2]))) if flag else "none yet, so no team needs a correction."), ""]

# ---- players
P = pd.read_sql_query("select f.game_id, f.player_id, f.name, f.team, f.proj_min, f.p_play, f.details_json from player_fc f join (select game_id, player_id, max(made_at_utc) m from player_fc group by game_id, player_id) l on l.game_id=f.game_id and l.player_id=f.player_id and l.m=f.made_at_utc", pl)
A = pd.read_sql_query("select * from player_act", pl)
PA = P.merge(A, on=["game_id", "player_id"], suffixes=("", "_a"))
PA = PA.merge(T[["game_id", "date"]], on="game_id")
STATS = {"pts": "pts", "reb": "reb", "ast": "ast", "stl": "stl", "blk": "blk", "tov": "tov", "tpm": "tpm", "fta": "fta", "min": "min"}
long = []
for r in PA.itertuples():
    d = json.loads(r.details_json)
    for k, col in STATS.items():
        x = d.get(k)
        if not x or "m" not in x: continue
        long.append((r.game_id, r.player_id, r.name, r.team, k, float(x["m"]) / max(float(r.p_play), 0.05), float(getattr(r, col)),   # stored mean includes the did-not-play zeros; divide by P(play) to compare with players who played
                      r.min, r.p_play, r.date))
L = pd.DataFrame(long, columns=["game_id", "player_id", "name", "team", "stat", "proj", "act", "mins", "p_play", "date"])
played = L[L.mins.fillna(0) > 0].copy()
for r in played.itertuples():
    pl.execute("insert or replace into review_player values (?,?,?,?,?,?,?)", (int(r.game_id), int(r.player_id), r.name, r.team, r.stat, r.proj, r.act))
pl.commit()
played["err"] = played.proj - played.act
td = played[played.date == day]
md += ["## Player projections (players who played; error = projection minus actual)", ""]
if td.empty:
    md += ["No player forecasts cover this date's games.", ""]
else:
    g = td.groupby("stat").agg(n=("err", "size"), proj=("proj", "mean"), actual=("act", "mean"), bias=("err", "mean"), mae=("err", lambda x: x.abs().mean())).round(2)
    s = played.groupby("stat").agg(n=("err", "size"), bias=("err", "mean"), se=("err", lambda x: x.std() / np.sqrt(len(x)))).round(3)
    g["season bias"] = s.bias; g["z"] = (s.bias / s.se).round(1)
    md += [g.reset_index().to_markdown(), ""]
    for k, r in s.iterrows(): learned["player"][k] = [float(r.bias), float(r.se), int(r.n)]
    persistent = [(k, r.bias, r.bias / r.se) for k, r in s.iterrows() if abs(r.bias / r.se) > 3 and k != "min"]
    md += ["- Persistent player biases (|z| > 3 over the season): " + ("; ".join(f"{k} {b:+.2f} per player-game" + (" (we over-project)" if b > 0 else " (we under-project)") for k, b, z in persistent) if persistent else "none."), ""]
    big = td[td.stat.isin(["pts", "reb", "ast"])].assign(a=lambda d_: d_.err.abs()).sort_values("a", ascending=False).head(8)
    md += ["Biggest individual misses today: " + "; ".join(f"{r.name} {r.stat} projected {r.proj:.1f}, actual {r.act:.0f}" for r in big.itertuples()), ""]
    pm = PA[PA.date == day]
    dnp = pm[(pm["min"].fillna(0) == 0) & (pm.p_play >= 0.8)]
    surprise = pm[(pm["min"].fillna(0) > 0) & (pm.p_play < 0.5)]
    md += [f"- Availability: {len(dnp)} players we rated 80%+ to play did not ({', '.join(dnp.name.head(6)) or 'none'}); {len(surprise)} players we rated under 50% did play ({', '.join(surprise.name.head(6)) or 'none'}).", ""]

# ---- why the misses happened (from box scores: this is what the data can show, not play-by-play or film)
def why_section():
    out = ["## Why we missed (what the box scores show)", "",
           "Games where the winner was wrong or the margin missed by 8+ points. The causes are read from the box score against what the simulation expected; "
           "things like double-teams, scheme or in-game injuries are not in the data we have, so they are not claimed.", ""]
    TB = pd.read_sql_query("select game_id, side, team, pts, fga, fgm, fg3a, fg3m, fta, ftm, tov, oreb, dreb from team_box", live)
    EX = {(r[0], r[1]): json.loads(r[2]) for r in live.execute("select game_id, side, stats_json from team_box_extra")}
    bad = D[((D.p_home > .5) != (D.win == 1)) | (D.err_margin.abs() >= 8)].sort_values("err_margin", key=lambda s: -s.abs())
    if bad.empty:
        return out + ["No game missed by that much today.", ""]
    for g in bad.itertuples():
        d = json.loads(F.set_index("game_id").loc[g.game_id, "details_json"]); ex = (d.get("team_box") or {})
        tb = TB[TB.game_id == g.game_id].set_index("side")
        if "home" not in tb.index or "away" not in tb.index or not ex:
            continue
        winner = g.home if g.act_margin > 0 else g.away
        proj_w = g.home if g.mean_margin > 0 else g.away
        head = f"### {g.away} at {g.home}: we had {proj_w} by {abs(g.mean_margin):.1f}; {winner} won by {abs(g.act_margin):.0f}" + ("" if winner == proj_w else " (wrong winner)")
        # swing in points for the HOME team versus expectation, by cause
        sw = {}
        for s, sign in (("home", 1), ("away", -1)):
            a, e = tb.loc[s], ex.get(s, {})
            if not e: continue
            a3, e3 = a.fg3m, e["fg3m"]; a2, e2 = a.fgm - a.fg3m, e["fgm"] - e["fg3m"]
            sw["3-point shooting"] = sw.get("3-point shooting", 0) + sign * 3 * (a3 - e3)
            sw["2-point shooting"] = sw.get("2-point shooting", 0) + sign * 2 * (a2 - e2)
            sw["free throws"] = sw.get("free throws", 0) + sign * (a.ftm - e["ftm"])
            sw["turnovers"] = sw.get("turnovers", 0) + sign * 1.1 * (e["tov"] - a.tov)
            sw["offensive rebounds"] = sw.get("offensive rebounds", 0) + sign * 1.1 * (a.oreb - e["oreb"])
        # margin error in points explained (home-team view): positive = home did better than we expected
        resid = g.act_margin - g.mean_margin
        items = sorted(sw.items(), key=lambda kv: -abs(kv[1]))[:3]
        parts = []
        for k, v in items:
            if abs(v) < 2: continue
            who = g.home if v > 0 else g.away
            parts.append(f"{k} favoured {who} by about {abs(v):.0f} points versus what we expected")
        lines_ = [head, ""]
        h, a_ = tb.loc["home"], tb.loc["away"]
        lines_ += [f"- Shooting: {g.home} {int(h.fgm)}/{int(h.fga)} FG, {int(h.fg3m)}/{int(h.fg3a)} from 3 (expected {ex['home']['fg3m']:.0f} threes); {g.away} {int(a_.fgm)}/{int(a_.fga)} FG, {int(a_.fg3m)}/{int(a_.fg3a)} from 3 (expected {ex['away']['fg3m']:.0f})."]
        lines_ += [f"- Possessions: turnovers {g.home} {int(h.tov)} (expected {ex['home']['tov']:.0f}), {g.away} {int(a_.tov)} (expected {ex['away']['tov']:.0f}); offensive rebounds {g.home} {int(h.oreb)} (expected {ex['home']['oreb']:.0f}), {g.away} {int(a_.oreb)} (expected {ex['away']['oreb']:.0f}); free throws made {g.home} {int(h.ftm)} (expected {ex['home']['ftm']:.0f}), {g.away} {int(a_.ftm)} (expected {ex['away']['ftm']:.0f})."]
        if parts: lines_ += ["- Biggest swings: " + "; ".join(parts) + "."]
        # style from the extra box: fast-break and paint points
        eh, ea = EX.get((g.game_id, "home"), {}), EX.get((g.game_id, "away"), {})
        if eh and ea and "fastBreakPoints" in eh:
            lines_ += [f"- Where the points came from: fast breaks {g.home} {eh['fastBreakPoints']:.0f}, {g.away} {ea['fastBreakPoints']:.0f}; in the paint {g.home} {eh['pointsInPaint']:.0f}, {g.away} {ea['pointsInPaint']:.0f}; off turnovers {g.home} {eh.get('turnoverPoints', 0):.0f}, {g.away} {ea.get('turnoverPoints', 0):.0f}."]
        # players: biggest over/under-performers and surprise absences
        pp = PA[PA.game_id == g.game_id].copy()
        pp["proj_pts"] = [json.loads(x).get("pts", {}).get("m", np.nan) / max(pl_, 0.05) for x, pl_ in zip(pp.details_json, pp.p_play)]
        pp["d"] = pp.pts - pp.proj_pts
        pl_ = pp[pp["min"].fillna(0) > 0].sort_values("d", key=lambda s: -s.abs()).head(3)
        if len(pl_): lines_ += ["- Players who moved the result: " + "; ".join(f"{r['name']} ({r['team']}) scored {r['pts']:.0f} vs {r['proj_pts']:.0f} projected in {r['min']:.0f} min" for _, r in pl_.iterrows()) + "."]
        dnp = pp[(pp["min"].fillna(0) == 0) & (pp.p_play >= 0.8)].sort_values("proj_min", ascending=False).head(3)
        surp = pp[(pp["min"].fillna(0) >= 12) & (pp.p_play < 0.5)].sort_values("min", ascending=False).head(3)
        if len(dnp): lines_ += ["- We expected these players and they did not play: " + ", ".join(f"{r['name']} ({r['team']}, {r['proj_min']:.0f} min projected)" for _, r in dnp.iterrows()) + "."]
        if len(surp): lines_ += ["- Played more than we expected: " + ", ".join(f"{r['name']} ({r['team']}, {r['min']:.0f} min, we gave {r['p_play']:.0%} to play)" for _, r in surp.iterrows()) + "."]
        total_swing = sum(sw.values())
        lines_ += [f"- Reading: these swings add up to about {abs(total_swing):.0f} points against a {abs(resid):.0f}-point miss. Most of a miss like this is shooting luck (makes and misses against the shots we expected); what the data cannot show is why a team shot that way, such as double-teams, defensive scheme, in-game injuries or garbage time."]
        out += lines_ + [""]
    return out

# ---- picks
try:
    K = pd.read_sql_query("select * from picks_log", pl).merge(T[["game_id", "date"]], on="game_id")
    K = K[K.date == day].merge(A, on=["game_id", "player_id"], how="left", suffixes=("", "_a"))
    f = {"pts": K.pts, "reb": K.reb, "ast": K.ast, "stl": K.stl, "blk": K.blk, "tov": K.tov, "tpm": K.tpm, "fta": K.fta, "pra": K.pts + K.reb + K.ast, "pr": K.pts + K.reb, "pa": K.pts + K.ast, "ra": K.reb + K.ast, "fg2m": K.fgm - K.tpm}
    K["act"] = [f[s_][i] for i, s_ in zip(K.index, K.stat)]; K = K[K["min"].fillna(0) > 0]
    K = K[K.act != K.line].copy(); K["hit"] = np.where(K.side == "OVER", K.act > K.line, K.act < K.line)
    K = K.drop_duplicates(["game_id", "player_id", "stat", "side", "line"])
    md += ["## Picks logged for these games", ""]
    if len(K):
        md += [f"{len(K)} graded legs: hit {K.hit.mean():.0%} vs model's own average {K.p.mean():.0%}."]
        by = K.groupby(["stat", "side"]).agg(n=("hit", "size"), model_p=("p", "mean"), hit=("hit", "mean")).round(2).reset_index()
        md += ["", by.to_markdown(), ""]
        md += ["Wrong calls with the biggest model confidence: " + "; ".join(f"{r.name} {r.side} {r.line:g} {r.stat} (model {r.p:.0%}, actual {r.act:.0f})" for r in K[~K.hit].sort_values("p", ascending=False).head(5).itertuples()), ""]
    else:
        md += ["No logged picks cover these games.", ""]
except Exception as ex:
    md += [f"Pick grading skipped: {type(ex).__name__}.", ""]

md += ["## What the engine does with this", "",
       "- Stored forecasts are never edited. The review only measures.",
       "- Elo, team profiles and player rates update themselves from every result (that is the learning loop for the models).",
       "- Calibration shifts for the over/under ladders and the play probability are refit from these same results (`player_ladder_calibration`, `fit_p_play_cal`).",
       "- This report adds the check on top: biases are only flagged when their z-score is large. Season-to-date numbers are saved in `artifacts/learned_biases.json` so a correction can be added once a bias holds up over many games.", ""]
md[WHY_AT:WHY_AT] = why_section()
open(f"artifacts/reports/review_{day}.md", "w").write("\n".join(md))
json.dump(learned, open("artifacts/learned_biases.json", "w"), indent=1)
print("wrote", f"artifacts/reports/review_{day}.md")
