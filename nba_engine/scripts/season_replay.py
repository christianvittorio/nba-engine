"""Test-run simulation of every game played so far this season, as if forecast just before it started, compared with what happened.

Start state = the model after 2021-22 .. 2025-26 (rebuilt from the game and player tables, so nothing from this season leaks in).
Then, day by day (US Eastern dates, like the live job): forecast every game of the day from the state before the day -> ingest the results ->
update the player model. Team layer = the live engine (Elo + possession simulator; back-to-back and form variants). Player layer = the live
player model in two modes: 'unconfirmed' (lineup unknown, what the daily job stores) and 'confirmed' (told who actually played).
Injury information is not replayed (past ESPN injury lists are not available), so injury-adjusted variants are absent.

Source of this season's games:  ESPN (default, needs network access: run via the season-replay GitHub workflow)
                                REPLAY_SOURCE=csv<season>  offline self-test on a past season (first REPLAY_LIMIT games, default 120)
Outputs (artifacts/replay_<label>/): games.csv, players.csv, report.md"""
import json, os, sys, time
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import numpy as np, pandas as pd
from nbaengine.availability import _resolve, _short_key
from nbaengine.elo import Elo, EloParams
from nbaengine.feed import EspnFeed, FinalGame, UpcomingGame
from nbaengine.pipeline import Engine, _sd_to
from nbaengine.backtest import RunningSD
from nbaengine.players import PlayerModel, PlayerParams, sample_players, summarize_samples
from nbaengine.players_backtest import load_logs, run_pass
from nbaengine.playerfeed import COLS, parse_summary
from nbaengine.sim import ProfileParams, TeamProfiles
from nbaengine.store import Store

SRC = os.environ.get("REPLAY_SOURCE", "espn")
N_SIMS = int(os.environ.get("N_SIMS", 2000))
P_SIMS = int(os.environ.get("PLAYER_SIMS", 600))
LIMIT = int(os.environ.get("REPLAY_LIMIT", 120))
RECON = os.environ.get("REPLAY_RECONCILE", "1") == "1"
PPOW = float(os.environ.get("P_PLAY_POW", 1.3))
ALL = [2022, 2023, 2024, 2025, 2026]
if SRC.startswith("csv"):
    TARGET = int(SRC[3:])                      # label of the self-test season (2026 = 2025-26)
    WARM = [s for s in ALL if s < TARGET]
    OUT = f"artifacts/replay_selftest_{TARGET}"
else:
    TARGET, WARM, OUT = 2027, ALL, "artifacts/replay_2027"
QS = [5, 10, 25, 50, 75, 90, 95]
KEEP = ["min", "pts", "reb", "ast", "stl", "blk", "tov", "tpm", "pra"]
FILES = {2022: "games_cdn_2022.csv", 2023: "games_cdn_2023.csv", 2024: "games_cdn_2024.csv", 2025: "games_cdn_2025.csv", 2026: "games_cdn_2026.csv"}
t0 = time.time()
log = lambda *a: print(f"[{time.time() - t0:5.0f}s]", *a, flush=True)


# ------------------------------------------------------------------------------------------ start state
def build_team_engine(store) -> Engine:
    tpl = json.load(open("artifacts/state.json"))
    elo, prof = Elo(EloParams(**tpl["elo"]["params"])), TeamProfiles(ProfileParams(**tpl["prof"]["params"]))
    n = hw = m = tt = 0.0
    for s in WARM:
        g = pd.read_csv(f"data/processed/{FILES[s]}").sort_values("game_id")
        for gd in g.to_dict("records"):
            elo.new_season(s); prof.new_season(s)
            pp = prof.expected_poss(gd["home"], gd["away"])
            elo.update(gd["home"], gd["away"], gd["home_pts"], gd["away_pts"])
            prof.record_pace_residual(pp, gd); prof.update(gd)
            n += 1; hw += float(gd["home_pts"] > gd["away_pts"]); m += gd["home_pts"] - gd["away_pts"]; tt += gd["home_pts"] + gd["away_pts"]
    d = dict(tpl)
    d["elo"] = {"params": tpl["elo"]["params"], "ratings": elo.ratings, "season": elo.season}
    d["prof"] = {"params": tpl["prof"]["params"], "off": prof.off, "deff": prof.deff, "pace_w": prof.pace_w, "lg_side": prof.lg_side,
                 "lg_pace": prof.lg_pace, "pace_sq": prof.pace_sq, "season": prof.season}
    d["level_delta"], d["level_n"], d["level_season"] = 0.0, 0, None
    d["base"] = {"n": n, "hw": hw, "m": m, "t": tt}
    d["sds"] = {"elo": _sd_to(RunningSD(13.5)), "base_m": _sd_to(RunningSD(13.5)), "base_t": _sd_to(RunningSD(18.5))}
    d["applied"], d["last_played"], d["last_margin"] = [], {}, {}
    eng = Engine.from_dict(store, d)
    eng.rest_coef = json.load(open("artifacts/rest_fit.json"))
    return eng


def model_index(pm: PlayerModel) -> dict:
    idx: dict = {}
    for pid, nm in pm.names.items():
        k = _short_key(nm)
        if k:
            idx.setdefault(k, []).append((int(pid), pm.pl.get(pid, {}).get("n", 0), pm.pl.get(pid, {}).get("team")))
    return idx


# ------------------------------------------------------------------------------------------ day source
def espn_days():
    feed = EspnFeed(pause_s=0.5)
    today = datetime.now(ZoneInfo("America/New_York")).date()
    day, days = date(2026, 10, 18), {}
    while day <= today:
        fin, _ = feed.scoreboard(day.strftime("%Y%m%d"))
        if fin:
            days[str(day)] = [(fg, parse_summary(feed.summaries[str(fg.game_id)][2]) if str(fg.game_id) in feed.summaries else []) for fg in sorted(fin, key=lambda g: g.game_id)]
            log("fetched", day, len(fin), "games")
        day += timedelta(days=1)
    return days


def csv_days():
    g = pd.read_csv(f"data/processed/{FILES[TARGET]}").sort_values("game_id").head(LIMIT)
    P = pd.read_csv(f"data/processed/player_games_{TARGET}.csv")
    days = {}
    for gd in g.itertuples(index=False):
        box = {k: int(getattr(gd, k)) for k in gd._fields if k.startswith(("home_", "away_")) and k not in ("home_pts", "away_pts")}
        fg = FinalGame(int(gd.game_id), int(gd.season), gd.date, gd.home, gd.away, int(gd.home_pts), int(gd.away_pts), int(gd.n_periods), box)
        rows = [{"espn_id": str(r.player_id), "name": r.name, "team": r.team, **{c: float(getattr(r, c)) for c in COLS if c not in ("team", "player_id", "name")}, "player_id": int(r.player_id)}
                for r in P[(P.game_id == gd.game_id) & (P["min"] > 0)].itertuples()]
        days.setdefault(gd.date, []).append((fg, rows))
    return days


# ------------------------------------------------------------------------------------------ player forecasts for one game
def player_rows(pm, fg, rows_by_team, mode_rows, out, team_pts=None):
    """Forecast both teams in both modes from the CURRENT state, attach actuals. rows_by_team: team -> DataFrame of players who played."""
    for ti, team in enumerate((fg.home, fg.away)):
        played = rows_by_team.get(team)
        actual = {} if played is None else {int(r.player_id): r for r in played.itertuples(index=False)}
        for mode in ("unconfirmed", "confirmed"):
            if mode == "confirmed":
                ids = list(actual)
                if len(ids) < 5:
                    continue
                pr = pm.project_team(team, active=ids, mode="confirmed", team_pts=(team_pts or {}).get(team))
            else:
                if not pm.pool(team):
                    continue
                pr = pm.project_team(team, mode="unconfirmed", team_pts=(team_pts or {}).get(team))
            pr = pr.sort_values("base_min", ascending=False).head(14 if mode == "unconfirmed" else 20).reset_index(drop=True)
            seed = 20271021 + fg.game_id % 100000 * 10 + ti * 2 + (mode == "confirmed")
            summ = summarize_samples(sample_players(pr, pm.p, P_SIMS, seed, mode))
            for row, d in zip(pr.itertuples(index=False), summ):
                a = actual.get(int(row.player_id))
                bm = pm.baseline_means(int(row.player_id))
                rec = {"game_id": fg.game_id, "date": fg.date, "team": team, "opp": fg.away if team == fg.home else fg.home, "player_id": int(row.player_id),
                       "name": row.name, "mode": mode, "is_new": int(row.is_new), "proj_min": float(row.proj_min), "p_play": float(row.p_play),
                       "played": int(a is not None)}
                for s in KEEP:
                    rec[f"mean_{s}"] = d[s]["mean"]
                    rec[f"q10_{s}"], rec[f"q25_{s}"], rec[f"q75_{s}"], rec[f"q90_{s}"] = d[s]["q"][1], d[s]["q"][2], d[s]["q"][4], d[s]["q"][5]
                    av = 0.0 if a is None else (float(a.pts + a.reb + a.ast) if s == "pra" else float(getattr(a, "tpm" if s == "tpm" else s)))
                    rec[f"a_{s}"] = av
                    rec[f"b10_{s}"] = float((bm["pts"] + bm["reb"] + bm["ast"]) if (s == "pra" and bm) else (bm.get(s, np.nan) if bm else np.nan))
                out.append(rec)


# ------------------------------------------------------------------------------------------ main replay
def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    DBP = f"{OUT}/replay.sqlite"
    if os.path.exists(DBP):
        os.remove(DBP)
    store = Store(DBP)
    eng = build_team_engine(store); log("team state built from", WARM)
    tpl = json.load(open("artifacts/player_state.json"))
    pp = PlayerParams(**{**tpl["params"], "min_resid": [np.asarray(x, float) for x in tpl["params"]["min_resid"]]})
    pp.p_play_pow = PPOW
    pm = PlayerModel(pp)
    run_pass(load_logs(WARM), pp, 99999, model=pm); log("player state built from", WARM, "players:", len(pm.pl))
    idmap = json.load(open("artifacts/player_id_map.json")) if os.path.exists("artifacts/player_id_map.json") else {}
    overrides = json.load(open("artifacts/name_overrides.json")) if os.path.exists("artifacts/name_overrides.json") else {}
    idx = model_index(pm)
    days = espn_days() if SRC == "espn" else csv_days()
    log("days:", len(days), "games:", sum(len(v) for v in days.values()))
    prow, extra = [], []
    for dstr in sorted(days):
        games = days[dstr]
        # 1) team forecasts for the whole day from the state before the day
        for fg, _ in games:
            eng.forecast(UpcomingGame(fg.game_id, fg.season, fg.date, "2099-01-01T00:00:00Z", fg.home, fg.away), N_SIMS, "replay", enforce_tip=False)
        # 2) map players, forecast players from the state before the day
        mapped = []
        for fg, rows in games:
            for r in rows:
                k = str(r.get("espn_id"))
                pid = overrides.get(k) or idmap.get(k) if SRC == "espn" else r["player_id"]
                if pid is None:
                    pid = _resolve(idx, r["name"], r["team"])
                    pid = -int(k) if pid is None else pid
                    idmap[k] = int(pid)
                r["player_id"] = int(pid)
            df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=COLS)
            for c in COLS:
                if c not in df:
                    df[c] = 0.0 if c not in ("team", "name") else ""
            df = df[COLS].fillna(0)
            mapped.append(df)
            if len(df) >= 10:
                tp = None
                if RECON:
                    r_ = store.con.execute("SELECT mean_home, mean_away FROM forecasts WHERE game_id=? AND model_name='sim_mc'", (fg.game_id,)).fetchone()
                    tp = {fg.home: r_[0], fg.away: r_[1]} if r_ else None
                player_rows(pm, fg, {t: g for t, g in df.groupby("team")}, None, prow, tp)
            h_box = fg.box
            poss = lambda p: h_box[f"{p}_fga"] - h_box[f"{p}_oreb"] + h_box[f"{p}_tov"] + 0.44 * h_box[f"{p}_fta"]
            extra.append({"game_id": fg.game_id, "actual_poss": (poss("home") + poss("away")) / 2,
                          "actual_3pa": h_box["home_3pa"] + h_box["away_3pa"], "actual_3pm": h_box["home_3pm"] + h_box["away_3pm"],
                          "actual_fta": h_box["home_fta"] + h_box["away_fta"], "actual_tov": h_box["home_tov"] + h_box["away_tov"],
                          "actual_oreb": h_box["home_oreb"] + h_box["away_oreb"], "ot": int(fg.n_periods > 4)})
        # 3) ingest results, update player state
        for (fg, _), df in zip(games, mapped):
            eng.ingest(fg)
            if len(df) >= 10:
                pm.update_game(df, fg.season)
    store.commit()
    log("replay done; building comparison")
    build_outputs(store, pd.DataFrame(prow), pd.DataFrame(extra))
    try:                                   # team box-score / advanced stats and how well each team stat was predicted
        import importlib.util
        sp = importlib.util.spec_from_file_location("team_stats_report", os.path.join(ROOT, "scripts/team_stats_report.py"))
        tsr = importlib.util.module_from_spec(sp); sp.loader.exec_module(tsr); tsr.build(DBP, f"{OUT}/team_stats.md")
    except Exception as ex:
        print("team stats report failed:", type(ex).__name__, ex)
    store.con.close(); os.remove(DBP)


def build_outputs(store, P, X):
    q = """SELECT f.game_id, f.model_name, f.p_home, f.mean_home, f.mean_away, f.mean_margin, f.mean_total, f.p_ot, f.q_margin_json, f.q_total_json, f.details_json,
                  r.home_pts, r.away_pts, g.home, g.away, g.n_periods FROM forecasts f JOIN results r USING(season, game_id) JOIN games g USING(season, game_id)"""
    F = pd.read_sql_query(q, store.con)
    dts = pd.read_sql_query("SELECT game_id, date FROM game_dates", store.con)
    base = F[F.model_name == "sim_mc"].drop(columns=["model_name"]).copy()
    base = base.merge(dts, on="game_id", how="left").merge(X, on="game_id", how="left")
    det = base.details_json.map(json.loads)
    base["pred_poss"] = det.map(lambda d: d.get("mean_poss")); base["level_delta"] = det.map(lambda d: d.get("level_delta"))
    base["modal"] = det.map(lambda d: d.get("modal_score"))
    for name, tag in (("elo", "elo"), ("sim_mc_rest", "rest"), ("sim_mc_sit", "sit"), ("home_const", "const")):
        base = base.merge(F[F.model_name == name][["game_id", "p_home"]].rename(columns={"p_home": f"p_{tag}"}), on="game_id", how="left")
    qm, qt = base.q_margin_json.map(json.loads), base.q_total_json.map(json.loads)
    for k in ("10", "25", "75", "90"):
        base[f"qm{k}"], base[f"qt{k}"] = qm.map(lambda q: q[k]), qt.map(lambda q: q[k])
    base["margin"], base["total"] = base.home_pts - base.away_pts, base.home_pts + base.away_pts
    base = base.drop(columns=["q_margin_json", "q_total_json", "details_json", "modal"]).sort_values(["date", "game_id"]).reset_index(drop=True)
    base.to_csv(f"{OUT}/games.csv", index=False)
    if len(P):
        P.to_csv(f"{OUT}/players.csv", index=False)
    write_report(base, P)


def _ll(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean())


def md(df, fmt=None):
    fmt = fmt or {}
    out = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    for r in df.itertuples(index=False):
        out.append("| " + " | ".join(fmt.get(c, "{}").format(v) if isinstance(v, (int, float, np.floating, np.integer)) and not pd.isna(v) else str(v) for c, v in zip(df.columns, r)) + " |")
    return "\n".join(out)


def write_report(G, P):
    n = len(G); y = (G.margin > 0).astype(float)
    L = [f"# Season replay: {n} games, {G.date.min()} to {G.date.max()}", "",
         "Every game forecast from the model state before its day, then the real result and box score compared. "
         f"Start state rebuilt from seasons {WARM[0]}-{WARM[-1]} ({'ESPN results' if SRC == 'espn' else 'offline self-test on a past season'}); {N_SIMS} simulations per game. "
         "No injury information is replayed, and these replay forecasts are not the immutable live forecasts (those only exist for games forecast before tip-off).", ""]
    rows = []
    for nm, col in (("Simulator", "p_home"), ("Elo", "p_elo"), ("Simulator + back-to-back", "p_rest"), ("Simulator + back-to-back + form", "p_sit"), ("Home-court constant", "p_const")):
        p = G[col]
        rows.append({"model": nm, "winner right": f"{int(((p > .5) == (y == 1)).sum())}/{n}", "accuracy": float(((p > .5) == (y == 1)).mean()), "Brier": float(((p - y) ** 2).mean()), "log-loss": _ll(p.to_numpy(), y.to_numpy())})
    L += ["## 1. Who wins", "", md(pd.DataFrame(rows), {"accuracy": "{:.1%}", "Brier": "{:.4f}", "log-loss": "{:.4f}"}), "",
          f"Home teams won {y.mean():.1%} of games; the simulator expected {G.p_home.mean():.1%}.", ""]
    hp_hat = (G.mean_total + G.mean_margin) / 2; ap_hat = (G.mean_total - G.mean_margin) / 2
    c_tot, c_mar = G.total.mean(), G.margin.mean()
    sc = pd.DataFrame([
        {"quantity": "Home points", "predicted avg": hp_hat.mean(), "actual avg": G.home_pts.mean(), "bias": (G.home_pts - hp_hat).mean(), "MAE": (G.home_pts - hp_hat).abs().mean()},
        {"quantity": "Away points", "predicted avg": ap_hat.mean(), "actual avg": G.away_pts.mean(), "bias": (G.away_pts - ap_hat).mean(), "MAE": (G.away_pts - ap_hat).abs().mean()},
        {"quantity": "Total points", "predicted avg": G.mean_total.mean(), "actual avg": G.total.mean(), "bias": (G.total - G.mean_total).mean(), "MAE": (G.total - G.mean_total).abs().mean()},
        {"quantity": "Margin (home - away)", "predicted avg": G.mean_margin.mean(), "actual avg": G.margin.mean(), "bias": (G.margin - G.mean_margin).mean(), "MAE": (G.margin - G.mean_margin).abs().mean()},
        {"quantity": "Possessions", "predicted avg": G.pred_poss.mean(), "actual avg": G.actual_poss.mean(), "bias": (G.actual_poss - G.pred_poss).mean(), "MAE": (G.actual_poss - G.pred_poss).abs().mean()}])
    cov = {f"{lab}% {t}": float(((G[t] >= G[f"q{t[0]}{lo}"]) & (G[t] <= G[f"q{t[0]}{hi}"])).mean()) for t in ("margin", "total") for lo, hi, lab in (("25", "75", 50), ("10", "90", 80))}
    L += ["## 2. Scores", "", md(sc, {"predicted avg": "{:.1f}", "actual avg": "{:.1f}", "bias": "{:+.2f}", "MAE": "{:.2f}"}), "",
          f"For comparison, always guessing the season-to-date average ({c_tot:.1f} total) would give a total MAE of {(G.total - c_tot).abs().mean():.2f} and always guessing the average margin a margin MAE of {(G.margin - c_mar).abs().mean():.2f} "
          "(that comparison uses the full set of results, so it flatters the baseline).", "",
          "Predicted ranges that actually contained the result (nominal 50% / 80%): "
          + "; ".join(f"{k}: {v:.1%}" for k, v in cov.items()) + ".", "",
          f"Overtime: the simulator said {G.p_ot.mean():.1%}; {G.ot.mean():.1%} of these games went to overtime. Three-pointers made per game {G.actual_3pm.mean():.1f}, attempts {G.actual_3pa.mean():.1f}, "
          f"free-throw attempts {G.actual_fta.mean():.1f}, turnovers {G.actual_tov.mean():.1f}, offensive rebounds {G.actual_oreb.mean():.1f} (actual, both teams).", ""]
    G2 = G.assign(pred=lambda d: d.apply(lambda r: f"{r.mean_home:.0f}-{r.mean_away:.0f}", axis=1), act=lambda d: d.apply(lambda r: f"{r.home_pts}-{r.away_pts}", axis=1),
                  game=lambda d: d.away + " at " + d.home, ok=lambda d: np.where((d.p_home > .5) == (d.margin > 0), "yes", "NO"),
                  marg_err=lambda d: (d.margin - d.mean_margin), tot_err=lambda d: (d.total - d.mean_total))
    show = lambda d: d[["date", "game", "pred", "act", "p_home", "ok", "marg_err", "tot_err"]].rename(columns={"pred": "predicted (home-away)", "act": "actual (home-away)", "p_home": "P(home)", "ok": "winner right?", "marg_err": "margin error", "tot_err": "total error"})
    fm = {"P(home)": "{:.0%}", "margin error": "{:+.0f}", "total error": "{:+.0f}"}
    L += ["### Biggest margin misses", "", md(show(G2.reindex(G2.marg_err.abs().sort_values(ascending=False).index).head(10)), fm), "",
          "### Biggest total misses", "", md(show(G2.reindex(G2.tot_err.abs().sort_values(ascending=False).index).head(10)), fm), "",
          "### Every game", "", md(show(G2), fm), ""]
    tb = []
    for tm in sorted(set(G.home) | set(G.away)):
        h, a = G[G.home == tm], G[G.away == tm]
        pts = pd.concat([h.home_pts - hp_hat[h.index], a.away_pts - ap_hat[a.index]]); alw = pd.concat([h.away_pts - ap_hat[h.index], a.home_pts - hp_hat[a.index]])
        w = pd.concat([(h.margin > 0), (a.margin < 0)]); pw = pd.concat([h.p_home, 1 - a.p_home])
        tb.append({"team": tm, "games": len(pts), "wins": int(w.sum()), "expected wins": float(pw.sum()), "points vs proj": pts.mean(), "allowed vs proj": alw.mean()})
    L += ["## 3. Team by team", "", md(pd.DataFrame(tb).sort_values("expected wins", ascending=False), {"expected wins": "{:.1f}", "points vs proj": "{:+.1f}", "allowed vs proj": "{:+.1f}"}), "",
          "Small samples (a handful of games per team): differences of a few points are noise.", ""]
    if len(P):
        L += ["## 4. Player stats", ""]
        for mode, title, only in (("unconfirmed", "Lineup unknown (what the daily job stores): every rostered rotation player, 0 if they did not play", False),
                                  ("confirmed", "Told who actually played (minutes shared among them): players who played", True)):
            D = P[(P["mode"] == mode) & (P.is_new == 0)]
            D = D[D.played == 1] if only else D
            rows = []
            for s in KEEP:
                a, mu = D[f"a_{s}"], D[f"mean_{s}"]
                b = D[f"b10_{s}"] * (1.0 if only else 1.0)
                rows.append({"stat": s, "n": len(D), "forecast avg": mu.mean(), "actual avg": a.mean(), "bias": (a - mu).mean(), "MAE": (a - mu).abs().mean(),
                             "MAE last-10 avg": (a - b).abs().mean() if b.notna().any() else np.nan,
                             "50% range": float(((a >= D[f"q25_{s}"]) & (a <= D[f"q75_{s}"])).mean()), "80% range": float(((a >= D[f"q10_{s}"]) & (a <= D[f"q90_{s}"])).mean())})
            L += [f"### {title}", "", md(pd.DataFrame(rows), {"forecast avg": "{:.2f}", "actual avg": "{:.2f}", "bias": "{:+.3f}", "MAE": "{:.2f}", "MAE last-10 avg": "{:.2f}", "50% range": "{:.1%}", "80% range": "{:.1%}"}), ""]
        D = P[(P["mode"] == "confirmed") & (P.played == 1) & (P.is_new == 0)]
        pl = D.groupby("name").agg(games=("a_pts", "size"), forecast=("mean_pts", "mean"), actual=("a_pts", "mean")).assign(diff=lambda x: x.actual - x.forecast)
        pl = pl[pl.games >= 5].sort_values("diff")
        L += ["### Players furthest from their points projection (5+ games, told who played)", "",
              "Under-delivering:", "", md(pl.head(8).reset_index(), {"forecast": "{:.1f}", "actual": "{:.1f}", "diff": "{:+.1f}"}), "",
              "Over-delivering:", "", md(pl.tail(8).iloc[::-1].reset_index(), {"forecast": "{:.1f}", "actual": "{:.1f}", "diff": "{:+.1f}"}), ""]
    open(f"{OUT}/report.md", "w").write("\n".join(L))
    log("report written:", f"{OUT}/report.md")


if __name__ == "__main__":
    main()
