"""NBA Intelligence Engine dashboard.   Run:  streamlit run app/dashboard.py"""
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from nbaengine.backtest import calibration_table, evaluate, metrics
from nbaengine.pipeline import monitor
from nbaengine.store import Store
from nbaengine.players import PlayerModel, sample_players, summarize_samples

LIVE_DB, LIVE_STATE = os.path.join(ROOT, "artifacts/live.sqlite"), os.path.join(ROOT, "artifacts/state.json")
DEMO_DB, DEMO_STATE = os.path.join(ROOT, "artifacts/demo_replay.sqlite"), os.path.join(ROOT, "artifacts/demo_state.json")
MODEL_LABEL = {"sim_mc_sit": "Simulator (back-to-back + form)", "sim_mc_all": "Simulator (back-to-back + form + injuries)", "elo_sit": "Elo (back-to-back + form)", "elo_all": "Elo (back-to-back + form + injuries)", "sim_mc_rest": "Simulator (back-to-back adj.)", "sim_mc_full": "Simulator (back-to-back + injuries)", "elo_rest": "Elo (back-to-back adj.)", "elo_full": "Elo (back-to-back + injuries)", "sim_mc_inj": "Simulator (injury-adjusted)", "elo_inj": "Elo (injury-adjusted)", "sim_mc": "Simulator", "elo": "Elo", "home_const": "Home-court baseline", "sim_mc_raw": "Simulator (uncalibrated)"}
COLORS = {"Simulator": "#2563eb", "Elo": "#d97706", "Home-court baseline": "#6b7280", "Simulator (uncalibrated)": "#93c5fd"}

st.set_page_config(page_title="NBA Engine", page_icon="🏀", layout="wide")


def n_forecasts(path: str) -> int:
    if not os.path.exists(path):
        return 0
    try:
        return sqlite3.connect(path).execute("SELECT COUNT(*) FROM forecasts").fetchone()[0]
    except sqlite3.Error:
        return 0


# ---------------------------------------------------------------- source selection
live_n, demo_n = n_forecasts(LIVE_DB), n_forecasts(DEMO_DB)
options = []
if live_n:
    options.append("Live")
if demo_n:
    options.append("Demo: 2025-26 season replay")
with st.sidebar:
    st.title("🏀 NBA Engine")
    if not options:
        st.error("No forecasts found yet. Run `python scripts/daily_update.py` first.")
        st.stop()
    source = st.radio("Data", options, index=0)
    if not live_n:
        st.caption("Live data appears here after the first successful `daily_update.py` run. Until then you are seeing the demo.")
    if st.button("Reload data"):
        st.cache_data.clear()
        st.rerun()
is_demo = source.startswith("Demo")
DB, STATE = (DEMO_DB, DEMO_STATE) if is_demo else (LIVE_DB, LIVE_STATE)


@st.cache_data(show_spinner=False, ttl=120)
def load(db: str, mtime: float):
    store = Store(db)
    con = store.con
    rows = con.execute("SELECT season, game_id, model_name, p_home, mean_home, mean_away, mean_total, p_ot, "
                       "q_margin_json, q_total_json, details_json, data_cutoff FROM forecasts").fetchall()
    f = pd.DataFrame(rows, columns=["season", "game_id", "model", "p_home", "mean_home", "mean_away", "mean_total", "p_ot",
                                    "qm", "qt", "det", "cutoff"])
    det = f["det"].map(lambda s: json.loads(s) if isinstance(s, str) else {})
    sim = f[f.model == "sim_mc"].copy()
    sd = det[sim.index]
    sim["date"] = sd.map(lambda d: d.get("date"))
    sim["home"] = sd.map(lambda d: d.get("home"))
    sim["away"] = sd.map(lambda d: d.get("away"))
    sim["modal"] = sd.map(lambda d: d.get("modal_score"))
    sim["market"] = sd.map(lambda d: d.get("market"))
    elo = f[f.model == "elo"].set_index(["season", "game_id"])["p_home"].rename("p_elo")
    sim = sim.join(elo, on=["season", "game_id"])
    inj = f[f.model == "sim_mc_inj"].set_index(["season", "game_id"])
    sim = sim.join(inj["p_home"].rename("p_inj"), on=["season", "game_id"])
    sim = sim.join(inj["det"].map(lambda s: (json.loads(s) if isinstance(s, str) else {}).get("injury_shift")).rename("inj_shift"),
                   on=["season", "game_id"])
    for tag in ("rest", "full", "sit", "all"):
        x = f[f.model == f"sim_mc_{tag}"].set_index(["season", "game_id"])
        sim = sim.join(x["p_home"].rename(f"p_{tag}"), on=["season", "game_id"])
    res = pd.read_sql_query("SELECT season, game_id, home_pts, away_pts FROM results", con)
    sim = sim.merge(res, on=["season", "game_id"], how="left")
    ev = evaluate(store)
    runs = pd.read_sql_query("SELECT started_utc, finished_utc, today, ok, finals_ingested, forecasts_made, "
                             "forecasts_skipped_late, error FROM runs ORDER BY run_id DESC", con)
    mon = monitor(store, window=200)
    return sim, ev, runs, mon


sim, ev, runs, mon = load(DB, os.path.getmtime(DB))
sim["q"] = sim["qm"].map(json.loads); sim["qtot"] = sim["qt"].map(json.loads)

st.title("NBA game forecasts")
if is_demo:
    st.warning("Demo data: a replay of the 2025-26 season through the daily loop, to show how the dashboard looks. "
               "These are not live forecasts.")
elif not runs.empty:
    ok = runs[runs.ok == 1]
    st.caption(f"Last successful refresh: {ok.finished_utc.iloc[0] if len(ok) else 'never'} UTC")

tab_games, tab_players, tab_trends, tab_cal, tab_perf, tab_ratings, tab_tstats, tab_status = st.tabs(["Forecasts", "Players", "Trends & streaks", "Calibration", "How accurate is it?", "Team ratings", "Team stats", "Run status"])

# ---------------------------------------------------------------- forecasts
with tab_games:
    dates = sorted(sim.date.dropna().unique())
    if not dates:
        st.info("No dated forecasts yet.")
    else:
        d = st.selectbox("Date", dates[::-1], index=0)
        day = sim[sim.date == d].sort_values("game_id").reset_index(drop=True)
        show = pd.DataFrame({
            "Game": day.away + " at " + day.home,
            "Home win % (sim)": (day.p_home * 100).round(0).astype(int),
            "Home win % (Elo)": (day.p_elo * 100).round(0).astype(int),
            "Home win % (injury-adj.)": day.p_inj.map(lambda v: "" if pd.isna(v) else f"{v * 100:.0f}"),
            "Home win % (back-to-back adj.)": day.p_rest.map(lambda v: "" if pd.isna(v) else f"{v * 100:.0f}"),
            "Home win % (b2b + injuries)": day.p_full.map(lambda v: "" if pd.isna(v) else f"{v * 100:.0f}"),
            "Home win % (b2b + form)": day.p_sit.map(lambda v: "" if pd.isna(v) else f"{v * 100:.0f}"),
            "Home win % (b2b + form + injuries)": day.p_all.map(lambda v: "" if pd.isna(v) else f"{v * 100:.0f}"),
            "Projected score": day.apply(lambda r: f"{r.mean_away:.0f} - {r.mean_home:.0f}", axis=1),
            "Total": day.mean_total.round(1),
            "Likely margin (80%)": day.q.map(lambda q: f"{q['10']:+.0f} to {q['90']:+.0f}"),
            "OT chance %": (day.p_ot * 100).round(1),
            "Final": day.apply(lambda r: "" if pd.isna(r.home_pts) else f"{int(r.away_pts)} - {int(r.home_pts)}", axis=1),
        })
        st.caption("Injury-adjusted is experimental: it shifts the margin for rotation players ESPN lists as out (empty = no data). "
                   "Projected score is written away - home. Margin is home minus away; the range holds 80% of simulated games.")
        st.dataframe(show, hide_index=True, width="stretch", height=min(38 + 35 * len(show), 700))

        st.subheader("Game detail")
        pick = st.selectbox("Game", day.index, format_func=lambda i: show.loc[i, "Game"])
        g = day.loc[pick]
        c1, c2, c3, c4 = st.columns(4)
        fav, pf = (g.home, g.p_home) if g.p_home >= 0.5 else (g.away, 1 - g.p_home)
        c1.metric("Favourite (sim)", fav, f"{pf:.0%}")
        c2.metric("Elo says", f"{max(g.p_elo, 1 - g.p_elo):.0%}", g.home if g.p_elo >= 0.5 else g.away, delta_color="off")
        c3.metric("Projected total", f"{g.mean_total:.1f}")
        c4.metric("Overtime chance", f"{g.p_ot:.1%}")
        qs = [("5", "95", "90%"), ("10", "90", "80%"), ("25", "75", "50%")]
        bands = pd.DataFrame([{"Range": lab, "lo": g.q[lo], "hi": g.q[hi]} for lo, hi, lab in qs])
        base = alt.Chart(bands).encode(y=alt.Y("Range:N", sort=["90%", "80%", "50%"], title="Share of games", axis=alt.Axis(labelOverlap=False)))
        chart = base.mark_bar(height=24, color="#93c5fd", opacity=0.75).encode(x=alt.X("lo:Q", title=f"Margin: <- {g.away} wins   |   {g.home} wins ->"), x2="hi:Q")
        zero = alt.Chart(pd.DataFrame({"x": [0]})).mark_rule(color="#ef4444", strokeDash=[4, 3]).encode(x="x:Q")
        mid = alt.Chart(pd.DataFrame({"x": [g.q["50"]]})).mark_rule(color="#1e3a8a", size=3).encode(x="x:Q")
        st.altair_chart((chart + zero + mid).properties(height=170), width="stretch")
        st.caption(f"Dark line = median margin ({g.q['50']:+.0f}); red dashed line = tie. Most frequent exact score in simulation: "
                   f"{g.modal[1]}-{g.modal[0]} (away-home), which still happens in under 1% of games, so don't read it as a prediction.")
        if g.market:
            st.caption("Market snapshot at forecast time (stored for later comparison only, not used by the model): "
                       + json.dumps(g.market.get("snapshot", g.market))[:300])
        if pd.notna(g.home_pts):
            st.success(f"Final: {g.away} {int(g.away_pts)}, {g.home} {int(g.home_pts)}  "
                       f"(margin {int(g.home_pts - g.away_pts):+d}, total {int(g.home_pts + g.away_pts)})")

# ---------------------------------------------------------------- players
PLAYER_STATE = os.path.join(ROOT, "artifacts/player_state.json")
SHOW = ["pts", "reb", "ast", "tpm", "stl", "blk", "tov", "pra"]


@st.cache_resource(show_spinner=False)
def load_players(mtime: float):
    return PlayerModel.load(PLAYER_STATE)


@st.cache_data(show_spinner=False)
def project(team: str, active: tuple, pool: tuple, n_sims: int, _mtime: float):
    pm = load_players(_mtime)
    extra = {p: 12.0 for p in pool if p < 0}            # no history yet: assume a 12-minute role
    proj = pm.project_team(team, active=list(active), pool_ids=list(pool), extra_unknown=extra)
    samp = sample_players(proj, pm.p, n_sims, seed=2026)
    return proj, summarize_samples(samp)


with tab_players:
    if not os.path.exists(PLAYER_STATE):
        st.info("No player state found. Run scripts/player_fit_eval.py to build it.")
    else:
        pmt = os.path.getmtime(PLAYER_STATE)
        pm = load_players(pmt)
        st.subheader("Player projections")
        st.caption("Projections are conditional on the availability you choose. The model does not know who is injured: "
                   "it uses the injury list below (or what you choose) and redistributes minutes and usage. "
                   f"Player history is learned through season {pm.season} ({pm.n_games} games).")
        teams = sorted(pm.team_gp)
        c1, c2 = st.columns([1, 3])
        team = c1.selectbox("Team", teams, index=0)
        window = c1.slider("Roster window (team games since a player last played)", 5, 82, 8,
                           help="Players who last played for this team within this many team games are listed. "
                                "8 is the setting used in the backtest. Wider windows pull in players who may have left the team.")
        AV_PATH = os.path.join(ROOT, "artifacts/availability.json")
        try:
            av = json.load(open(AV_PATH)) if os.path.exists(AV_PATH) else None
        except Exception:
            av = None
        team_av = (av or {}).get("teams", {}).get(team)
        if team_av and team_av.get("roster"):
            status = {i["name"]: (i.get("status") or "") for i in team_av.get("injuries", [])}
            label, roster, default_out = {}, [], []
            for r in team_av["roster"]:
                pid = r["nba_id"] if r.get("nba_id") is not None else -int(r["espn_id"])
                if pid in label:
                    continue
                if r.get("nba_id") is None:
                    pm.names[pid] = r["name"]
                    base = f"{r['name']} (no history)"
                else:
                    base = f"{r['name']} ({(pm.ewm_min(pid) or 0):.0f} min)"
                st_ = status.get(r["name"], "")
                label[pid] = base + (f" - {st_}" if st_ else "")
                roster.append(pid)
                if "out" in st_.lower():
                    default_out.append(pid)
            roster.sort(key=lambda x: -(pm.ewm_min(x) or 0.0))
            st.caption(f"Roster and injury statuses from ESPN, fetched {av.get('generated_utc', '?')} UTC. ESPN's injury list is not an "
                       "official report and may be late or incomplete: the players marked out are pre-selected, and you can change them. "
                       "Players with no history use a 12-minute default and league-average rates.")
            out = c2.multiselect("Out / not playing", roster, default=default_out, format_func=lambda x: label[x], key=f"out_{team}")
            pool = list(roster)
        else:
            roster = pm.pool(team, window=window)
            roster = sorted(roster, key=lambda x: -(pm.ewm_min(x) or 0.0))
            label = {x: f"{pm.names.get(x, x)} ({(pm.ewm_min(x) or 0):.0f} min)" for x in roster}
            st.caption("No current roster file for this team, so rosters come from each team's most recent games in the data. Players who "
                       "have moved teams since then still appear: mark them as out. Newly arrived players are not listed.")
            out = c2.multiselect("Out / not playing", roster, format_func=lambda x: label[x])
            extra = c2.multiselect("Also include (not on the list)", [x for x in pm.pool(team, window=82) if x not in roster],
                                   format_func=lambda x: f"{pm.names.get(x, x)} ({(pm.ewm_min(x) or 0):.0f} min)")
            pool = roster + extra
        rot_n = c1.slider("Players in the rotation", 8, 13, 10,
                          help="Only about 10 players play meaningful minutes. The healthy players with the most usual minutes are used, "
                               "so when a regular is out, the next man in the roster moves up.")

        def rotation(ids):
            ranked = sorted(ids, key=lambda x: -((pm.ewm_min(x) or 12.0) if x >= 0 else 12.0))
            return ranked[:rot_n]

        active = rotation([x for x in pool if x not in out])
        n_sims = c1.select_slider("Simulations", [1000, 4000, 10000], value=4000)
        if len(active) < 5:
            st.warning("Fewer than five players are active. Pick at least five.")
        else:
            proj, summ = project(team, tuple(active), tuple(pool), n_sims, pmt)
            rows = []
            for (_, r), d in zip(proj.iterrows(), summ):
                row = {"Player": r["name"], "Min": r["proj_min"], "Games (history)": int(r["n_games"])}
                for s_ in SHOW:
                    row[s_.upper()] = d[s_]["mean"]
                row["PTS 10-90%"] = f"{d['pts']['q'][1]:.0f} to {d['pts']['q'][5]:.0f}"
                row["PTS line"] = d["pts"]["line"]
                row["P(over line)"] = d["pts"]["p_over"]
                rows.append(row)
            tbl = pd.DataFrame(rows).sort_values("Min", ascending=False)
            fmt = {c: "{:.1f}" for c in ["Min"] + [s_.upper() for s_ in SHOW] + ["PTS line"]}
            fmt["P(over line)"] = "{:.0%}"
            st.dataframe(tbl.style.format(fmt), hide_index=True, width="stretch")
            if out:
                base_proj, _ = project(team, tuple(rotation(pool)), tuple(pool), n_sims, pmt)
                cmp = pd.DataFrame({"Player": proj["name"], "Min (now)": proj["proj_min"].values})
                cmp = cmp.merge(pd.DataFrame({"Player": base_proj["name"], "Min (all healthy)": base_proj["proj_min"].values}),
                                on="Player", how="left")
                cmp["Change"] = cmp["Min (now)"] - cmp["Min (all healthy)"]
                st.markdown("**Effect of the absences on minutes**")
                st.dataframe(cmp.sort_values("Change", ascending=False).style.format(
                    {"Min (now)": "{:.1f}", "Min (all healthy)": "{:.1f}", "Change": "{:+.1f}"}), hide_index=True, width="stretch")
            st.caption("Accuracy on 2025-26 (walk-forward, 26,545 confirmed-lineup player-games): points MAE 4.45 vs 4.68 for a "
                       "10-game-average baseline; the 80% intervals covered 83%. Stat lines for one player are not reconciled to the "
                       "team simulation, so player totals will not sum exactly to a team forecast. Projections for players with few games "
                       "(rookies, new arrivals) lean on league averages and are less reliable.")

# ---------------------------------------------------------------- accuracy
with tab_perf:
    if ev.empty:
        st.info("No completed forecasted games yet. Results appear after the first games finish.")
    else:
        ev = ev.copy()
        ev["Model"] = ev.model_name.map(MODEL_LABEL)
        m = metrics(ev)
        m.index = m.index.map(MODEL_LABEL)
        n = int(m["n"].iloc[0])
        st.subheader(f"Scorecard over {n} completed games")
        st.caption("Log loss and Brier: lower is better. A coin flip scores 0.693 log loss. The home-court baseline always predicts the "
                   "league's running home-win rate, so it shows what you get with no team knowledge.")
        tbl = m[["log_loss", "brier", "accuracy", "margin_mae", "total_mae"]].rename(columns={
            "log_loss": "Log loss", "brier": "Brier", "accuracy": "Winner accuracy", "margin_mae": "Margin error (pts)",
            "total_mae": "Total error (pts)"})
        tbl["Winner accuracy"] = (tbl["Winner accuracy"] * 100).round(1).astype(str) + "%"
        tbl["Total error (pts)"] = tbl["Total error (pts)"].map(lambda v: "n/a" if pd.isna(v) else f"{v:.2f}")
        tbl["Margin error (pts)"] = tbl["Margin error (pts)"].map(lambda v: f"{v:.2f}")
        st.dataframe(tbl[["Log loss", "Brier"]].round(4).join(tbl[["Winner accuracy", "Margin error (pts)", "Total error (pts)"]]), width="stretch")
        for line in mon:
            (st.warning if "FLAG" in line else st.caption)(line)

        st.subheader("Rolling log loss (100-game window)")
        roll = []
        for name, dd in ev[ev.model_name.isin(["sim_mc", "elo", "home_const"])].groupby("Model"):
            dd = dd.sort_values("game_id")
            p, y = dd.p_home.clip(1e-6, 1 - 1e-6), dd.y
            l = -(y * np.log(p) + (1 - y) * np.log(1 - p))
            r = l.rolling(100).mean()
            roll.append(pd.DataFrame({"Game #": range(len(dd)), "Log loss": r.values, "Model": name}))
        roll = pd.concat(roll).dropna()
        if len(roll):
            st.altair_chart(alt.Chart(roll).mark_line().encode(
                x="Game #:Q", y=alt.Y("Log loss:Q", scale=alt.Scale(zero=False)),
                color=alt.Color("Model:N", scale=alt.Scale(domain=list(COLORS), range=list(COLORS.values())))).properties(height=300),
                width="stretch")
        else:
            st.caption("Needs at least 100 completed games.")

        st.subheader("Are the percentages honest?")
        model_pick = st.radio("Model", ["Simulator", "Elo"], horizontal=True)
        cal = calibration_table(ev.assign(model_name=ev.model_name), "sim_mc" if model_pick == "Simulator" else "elo").reset_index()
        cal["bin"] = cal["bin"].astype(str)
        if len(cal):
            pts = alt.Chart(cal).mark_circle(size=120, color=COLORS[model_pick]).encode(
                x=alt.X("mean_pred:Q", scale=alt.Scale(domain=[0, 1]), title="Predicted home-win probability"),
                y=alt.Y("observed:Q", scale=alt.Scale(domain=[0, 1]), title="How often the home team actually won"),
                tooltip=["bin", "n", "mean_pred", "observed"])
            diag = alt.Chart(pd.DataFrame({"x": [0, 1], "y": [0, 1]})).mark_line(color="#9ca3af", strokeDash=[4, 3]).encode(x="x", y="y")
            st.altair_chart((diag + pts).properties(height=340), width="stretch")
            st.caption("Points on the dashed line mean the stated chances match reality. Points below it mean overconfidence.")


# ---------------------------------------------------------------- trends & streaks
with tab_trends:
    from nbaengine import trends as TR

    @st.cache_data(show_spinner="Building the trend frame...")
    def _trend_frame():
        p = TR.load_projected(extra=TR.live_extra(DB)); t = TR.team_games(p, TR.load_warmup_games()); return t, TR.add_labels(t)

    @st.cache_data(show_spinner="Scanning situations...")
    def _league_trends(_t, _L):
        return TR.league_trends(_t, _L)

    try:
        tt, LL = _trend_frame()
    except Exception as ex:
        st.info(f"Trend data not available: {type(ex).__name__}: {ex}"); tt = None
    if tt is not None:
        st.subheader("Check a trend")
        st.caption("Pick a situation and see how teams did in it, season by season, against what the model expected. "
                   "There are no sportsbook lines in this data, so 'beat the projection' means better than OUR model, not a bet that cashed. "
                   "Projections exist for 2023-2026; 2022 is only used for outcome-only angles and is not included in model comparisons.")
        c1, c2, c3 = st.columns(3)
        _opts = sorted(s_ for s_ in tt.season.unique() if s_ >= 2023)
        seasons = c1.multiselect("Seasons", _opts, default=_opts, format_func=lambda s_: f"{s_-1}-{str(s_)[2:]}",
                                 help="2026-27 is the live season: only games forecast by the daily job (and dated) count for projection-based angles.")
        team = c2.multiselect("Team", sorted(tt.team.unique())); opp = c3.multiselect("Opponent", sorted(tt.team.unique()))
        d1, d2, d3, d4 = st.columns(4)
        venue = d1.multiselect("Venue", ["home", "away"]); rest = d2.multiselect("Team rest", ["B2B", "1d", "2d", "3d+"],
            help="B2B = second night of a back-to-back (0 days off)")
        opp_rest = d3.multiselect("Opponent rest", ["B2B", "1d", "2d", "3d+"]); edge = d4.multiselect("Rest edge", ["more rest", "equal rest", "less rest"])
        e1, e2, e3, e4 = st.columns(4)
        fav = e1.multiselect("Model's view", ["heavy dog", "dog", "pick'em", "fav", "heavy fav"])
        prev = e2.multiselect("Previous game", ["won by 10+", "won close", "lost close", "lost by 10+"])
        strk = e3.multiselect("Streak entering", ["won 3+ straight", "lost 3+ straight", "no streak"])
        orec = e4.multiselect("Opponent quality", ["good opp (.600+)", "middling opp", "bad opp (.400-)"], help="Record entering the game, from game 16 on")
        f1, f2, f3, f4 = st.columns(4)
        tmin = f1.number_input("Projected game total at least", value=0.0, step=0.5); tmax = f2.number_input("... at most", value=400.0, step=0.5)
        pmin = f3.number_input("Team projected points at least", value=0.0, step=0.5); pmax = f4.number_input("... at most", value=300.0, step=0.5)
        labels = {"team": team, "opponent": opp, "venue": venue, "rest": rest, "opp_rest": opp_rest, "rest_edge": edge,
                  "favorite": fav, "prev_result": prev, "streak": strk, "opp_record": orec}
        rows = TR.select(tt, LL, labels, {"proj_total": (tmin if tmin > 0 else None, tmax if tmax < 400 else None),
                                          "proj_pts": (pmin if pmin > 0 else None, pmax if pmax < 300 else None)}, seasons)
        rows = rows[rows.p_win.notna()]
        if rows.empty:
            st.warning("No games match this situation.")
        else:
            st.markdown(f"**{len(rows):,} team-games match.** (Each game appears once for each team, so a game can appear twice if both teams fit.)")
            summ = TR.summarize_situation(rows, tt)
            st.dataframe(summ.style.format({"hit rate": "{:.1%}", "expected rate": "{:.1%}", "z (vs expected)": "{:+.2f}"}), hide_index=True, width="stretch")
            st.caption("'Expected rate' is what the model (win) or the league-wide base rate (other outcomes) predicted for these exact games. "
                       "z beyond about +/-3 is worth a look; a long run alone is not, because thousands of situations exist and some will look perfect by luck. "
                       "'Current run' is the streak of hits (positive) or misses (negative) ending at the most recent matching game.")
            by = rows.groupby("season").agg(games=("win", "size"), wins=("win", "sum"), beat_margin=("beat_margin", "mean"),
                                            over_total=("over_total", "mean")).reset_index()
            by["season"] = by.season.map(lambda s: f"{s-1}-{str(s)[2:]}")
            st.dataframe(by.rename(columns={"beat_margin": "beat projected margin", "over_total": "over projected total"}).style.format(
                {"beat projected margin": "{:.1%}", "over projected total": "{:.1%}"}), hide_index=True, width="stretch")
            if st.checkbox("Show the games", value=False):
                show = rows[["date", "team", "opp", "home", "rest", "opp_rest", "pts", "opp_pts", "proj_pts", "proj_opp_pts", "proj_total", "p_win", "win", "beat_margin", "over_total"]].copy()
                show["date"] = show.date.dt.date; show["home"] = np.where(show.home == 1, "home", "away")
                st.dataframe(show.round(2), hide_index=True, width="stretch")


        st.subheader("Active niche streaks for upcoming games")
        st.caption("Situations that describe an upcoming game, the team's record in the same situation since 2022-23, and the run it is on. "
                   "Most are what chance produces when thousands of situations are scanned, and team-specific streaks did not carry over in the "
                   "early-vs-late seasons test. Descriptive, not predictive.")
        try:
            import importlib.util
            _spec = importlib.util.spec_from_file_location("niche_streaks", os.path.join(ROOT, "scripts/niche_streaks.py"))
            _ns = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_ns)
            _fd = _ns.forecast_dates(DB)
            _d = st.selectbox("Slate date", _fd[::-1], index=0, key="streak_date") if _fd else None
            if _d:
                @st.cache_data(show_spinner="Finding streaks...")
                def _streaks(d, mtime):
                    c = _ns.compute(DB, d, 6)
                    return (c[0], c[1]) if c else (pd.DataFrame(), pd.DataFrame())
                sdf, sup = _streaks(_d, os.path.getmtime(DB))
                st.write(f"Games on {_d} (situations as they stood before tip-off)")
                oc = st.multiselect("Outcome", list(TR.STREAK_OUTCOMES), default=["win", "beat_margin"], key="streak_oc")
                tms = st.multiselect("Team", sorted(set(sup.home) | set(sup.away)), key="streak_tm")
                sh = sdf[sdf.outcome.isin(oc)]
                if tms:
                    sh = sh[sh.team.isin(tms)]
                sh = sh.assign(game=sh.opp.where(sh.home == 1, sh.opp) + "")
                st.dataframe(sh[["team", "opp", "situation", "outcome", "n", "hits", "run", "model_chance_of_run"]].head(60).style.format(
                    {"model_chance_of_run": "{:.3%}"}), hide_index=True, width="stretch")
            else:
                st.info("No upcoming forecast games right now.")
        except Exception as ex:
            st.info(f"Streaks unavailable: {type(ex).__name__}: {ex}")

        st.subheader("What the scan found (league-wide)")
        st.caption("Every combination of up to two situation features across all teams was tested against the model's expectation. "
                   "Shown: the strongest found on 2023-24 after a false-discovery filter, then re-measured on 2025-26. "
                   "'Held up' means the later seasons moved the same direction.")
        lt = _league_trends(tt, LL)
        st.dataframe(lt.style.format({"rate_found": "{:.1%}", "expected_found": "{:.1%}", "edge_found": "{:+.1%}", "rate_later": "{:.1%}", "edge_later": "{:+.1%}"}),
                     hide_index=True, width="stretch")
        st.info("Honest reading: two families held up in both periods. (1) Rest: teams on the second night of a back-to-back scored about 2 to 3 "
                "points worse than the model expected. (2) Mismatches: good teams against bad opponents beat the projected margin more often than half the time, "
                "although a direct test found no scale error in the margins themselves. Month-based patterns flipped sign between periods, and team-specific streaks "
                "(for example 'Team A is 22-0 in this exact spot') did not carry over, which is what luck predicts.")

# ---------------------------------------------------------------- calibration
with tab_cal:
    _cp = os.path.join(ROOT, "artifacts/reports/calibration.md")
    if os.path.exists(_cp):
        st.caption("Team and player forecasts checked against results. Regenerated by every daily run. Live-season sections start small and grow.")
        st.markdown(open(_cp).read())
    else:
        st.info("No calibration report yet. It is written by the daily run (scripts/calibration_report.py).")

# ---------------------------------------------------------------- ratings
with tab_ratings:
    if not os.path.exists(STATE):
        st.info("No state file found.")
    else:
        stt = json.load(open(STATE))
        elo = pd.DataFrame(sorted(stt["elo"]["ratings"].items(), key=lambda kv: -kv[1]), columns=["Team", "Elo"])
        st.subheader("Elo ratings (current)")
        st.altair_chart(alt.Chart(elo).mark_bar(color="#d97706").encode(
            x=alt.X("Elo:Q", scale=alt.Scale(domain=[1100, 1800], clamp=True), title="Elo (axis starts at 1100)"),
            y=alt.Y("Team:N", sort="-x", title=None, axis=alt.Axis(labelOverlap=False, labelFontSize=12)),
            tooltip=["Team", alt.Tooltip("Elo:Q", format=".0f")]).properties(height=780),
            width="stretch")
        st.caption(f"Average team is about 1505. A 100-point gap is roughly a 64% win chance for the stronger team before home-court. "
                   f"Season label in state: {stt['elo']['season']}.")

# ---------------------------------------------------------------- team stats
with tab_tstats:
    from nbaengine.teamstats import load_box, advanced_table, predicted_vs_actual, accuracy_table
    _bx = load_box(DB)
    if _bx.empty:
        st.info("No team box scores stored yet. They are saved as games are ingested by the daily run.")
    else:
        _ssn = int(_bx.season.max())
        _tt = advanced_table(_bx[_bx.season == _ssn])
        st.subheader(f"Team stats, {_ssn - 1}-{str(_ssn)[2:]} season ({_bx[_bx.season == _ssn].game_id.nunique()} games)")
        st.caption("Ratings per 100 possessions. 'opp' columns are what the team allows. Click a column header to sort.")
        st.dataframe(_tt.round(3), width="stretch", height=560)
        _pick = st.multiselect("Compare teams", list(_tt.index), default=[], max_selections=2)
        if len(_pick) == 2:
            st.dataframe(_tt.loc[_pick].T.round(3), width="stretch")
        _M = predicted_vs_actual(DB)
        if len(_M):
            st.subheader("How well the simulator predicted each team stat")
            st.caption("Forecasts stored before tip-off (regulation games), against the final box score.")
            st.dataframe(accuracy_table(_M).round(3), width="stretch", hide_index=True)

# ---------------------------------------------------------------- status
with tab_status:
    if runs.empty:
        st.info("No runs recorded.")
    else:
        bad = runs[runs.ok == 0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Runs recorded", len(runs)); c2.metric("Failed runs", len(bad))
        c3.metric("Games forecast", int(runs.forecasts_made.sum()))
        if len(bad):
            st.warning("Some runs failed. Their games may lack forecasts, though results are re-ingested on later runs.")
        runs = runs.assign(error=runs.error.fillna(""))
        st.dataframe(runs.rename(columns={"started_utc": "Started (UTC)", "finished_utc": "Finished (UTC)", "today": "Slate date",
                                          "ok": "OK", "finals_ingested": "Results ingested", "forecasts_made": "Forecasts made",
                                          "forecasts_skipped_late": "Skipped (already started)", "error": "Error"}),
                     hide_index=True, width="stretch")
    st.caption("Known gaps: injuries come from ESPN's unofficial list, no confirmed lineups, no travel distance, offseason roster changes are learned only gradually. "
               "Forecasts are probabilities, never certainties.")
