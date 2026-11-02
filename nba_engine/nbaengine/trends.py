"""Trend / streak finder over walk-forward model projections.

IMPORTANT LIMITS (also printed in every report):
* There are no sportsbook lines in this data. "beat projection" / "over projected total" mean the team did better than
  OUR MODEL's projection, not that a bet at a bookmaker's price would have won.
* Projections exist for seasons 2023-2026 (2022 is the model's warm-up). Outcome-only angles (win, rest, streaks)
  can use 2022 as well.
* Thousands of situations are scanned; some will look perfect by luck. `mine()` therefore reports a Benjamini-Hochberg
  false-discovery filter and `holdout()` checks whether trends found in early seasons held in later ones.
"""
from __future__ import annotations

import itertools
import os
import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALPHA = 0.01                    # same online scoring-level correction rate as the backtest
OUTCOMES = {
    "win": "won the game",
    "beat_margin": "beat the model's projected margin",
    "over_total": "game total went over the model's projected total",
    "over_team": "scored more than the model's projected team points",
    "blowout_win": "won by 10+",
    "ot": "game went to overtime",
}


# ----------------------------------------------------------------------------------------------- loading
def load_projected(root: str = ROOT, extra: pd.DataFrame | None = None) -> pd.DataFrame:
    """One row per game with projections (2023-2026) + level-corrected projected totals.
    `extra` may hold more games with the same columns (e.g. the live 2026-27 season)."""
    dd = [pd.read_csv(os.path.join(root, "data/processed", f"trend_proj_{s}.csv")) for s in (2023, 2024, 2025, 2026)]
    if extra is not None and len(extra):
        dd.append(extra)
    d = pd.concat(dd, ignore_index=True).sort_values(["season", "game_id"]).reset_index(drop=True)
    delta, lv = 0.0, []
    for h, a, sh, sa in zip(d.home_pts, d.away_pts, d.sim_home, d.sim_away):
        lv.append(delta)                                   # correction known BEFORE the game
        if np.isnan(sh) or np.isnan(sa):                   # game without a stored projection (live season before forecasting started)
            continue
        delta = (1 - ALPHA) * delta + ALPHA * ((h + a) - (sh + sa))
    d["level"] = lv
    d["proj_total"] = d.sim_home + d.sim_away + d.level
    d["proj_home"] = d.sim_home + d.level / 2
    d["proj_away"] = d.sim_away + d.level / 2
    d["proj_margin"] = d.sim_home - d.sim_away               # home perspective
    return d


def live_extra(db_path: str) -> pd.DataFrame:
    """Live-season games from the daily store (needs game_dates). Games without a stored forecast keep NaN projections:
    they still count for rest calculations and for outcome-only angles."""
    import json, sqlite3
    if not os.path.exists(db_path):
        return pd.DataFrame()
    con = sqlite3.connect(db_path)
    try:
        g = pd.read_sql_query("""SELECT g.season, g.game_id, d.date, g.home, g.away, r.home_pts, r.away_pts, g.n_periods
                                 FROM games g JOIN results r USING(season, game_id) JOIN game_dates d USING(season, game_id)""", con)
        f = pd.read_sql_query("SELECT season, game_id, model_name, p_home, mean_home, mean_away, details_json FROM forecasts "
                              "WHERE model_name IN ('sim_mc_raw','sim_mc','elo')", con)
    except Exception:
        return pd.DataFrame()
    finally:
        con.close()
    if g.empty:
        return pd.DataFrame()
    raw = f[f.model_name == "sim_mc_raw"].set_index(["season", "game_id"])
    cal = f[f.model_name == "sim_mc"].set_index(["season", "game_id"])
    elo = f[f.model_name == "elo"].set_index(["season", "game_id"])
    k = list(zip(g.season, g.game_id))
    g["sim_home"] = [raw.mean_home.get(x, np.nan) for x in k]
    g["sim_away"] = [raw.mean_away.get(x, np.nan) for x in k]
    g["sim_p_home"] = [cal.p_home.get(x, np.nan) for x in k]
    g["elo_p_home"] = [elo.p_home.get(x, np.nan) for x in k]
    g["elo_margin"] = [json.loads(elo.details_json[x]).get("exp_margin", np.nan) if x in elo.index else np.nan for x in k]
    return g.sort_values(["season", "game_id"]).reset_index(drop=True)


def load_warmup_games(root: str = ROOT) -> pd.DataFrame:
    g = pd.read_csv(os.path.join(root, "data/processed/games_cdn_2022.csv"))[
        ["season", "game_id", "date", "home", "away", "home_pts", "away_pts", "n_periods"]]
    return g


def team_games(proj: pd.DataFrame, warm: pd.DataFrame | None = None) -> pd.DataFrame:
    """Long frame: one row per team per game, with context features and outcomes."""
    d = proj.copy()
    if warm is not None:
        d = pd.concat([warm, d], ignore_index=True)       # 2022 rows have NaN projections
    d["date"] = pd.to_datetime(d["date"])
    h = pd.DataFrame({"season": d.season, "game_id": d.game_id, "date": d.date, "team": d.home, "opp": d.away,
                      "home": 1, "pts": d.home_pts, "opp_pts": d.away_pts, "n_periods": d.n_periods,
                      "proj_pts": d.get("proj_home"), "proj_opp_pts": d.get("proj_away"),
                      "proj_total": d.get("proj_total"), "proj_margin": d.get("proj_margin"),
                      "p_win": d.get("sim_p_home"), "elo_p": d.get("elo_p_home")})
    a = pd.DataFrame({"season": d.season, "game_id": d.game_id, "date": d.date, "team": d.away, "opp": d.home,
                      "home": 0, "pts": d.away_pts, "opp_pts": d.home_pts, "n_periods": d.n_periods,
                      "proj_pts": d.get("proj_away"), "proj_opp_pts": d.get("proj_home"),
                      "proj_total": d.get("proj_total"),
                      "proj_margin": -d.get("proj_margin") if "proj_margin" in d else None,
                      "p_win": 1 - d["sim_p_home"] if "sim_p_home" in d else None,
                      "elo_p": 1 - d["elo_p_home"] if "elo_p_home" in d else None})
    t = pd.concat([h, a], ignore_index=True).sort_values(["team", "date", "game_id"]).reset_index(drop=True)
    t["margin"], t["total"] = t.pts - t.opp_pts, t.pts + t.opp_pts
    t["win"] = (t.margin > 0).astype(int)

    # ---- rest / schedule density (days off between games; NaN at the first game of a season)
    g = t.groupby(["team", "season"])
    t["rest"] = (t.date - g.date.shift(1)).dt.days - 1
    t["next_gap"] = (g.date.shift(-1) - t.date).dt.days - 1
    t["game_no"] = g.cumcount() + 1
    gap3 = (t.date - g.date.shift(2)).dt.days
    t["three_in_four"] = (gap3 <= 3).astype(int)
    gap4 = (t.date - g.date.shift(3)).dt.days
    t["four_in_six"] = (gap4 <= 5).astype(int)
    opp = t[["game_id", "team", "rest", "next_gap"]].rename(columns={"team": "opp", "rest": "opp_rest", "next_gap": "opp_next_gap"})
    t = t.merge(opp, on=["game_id", "opp"], how="left")
    t = t.sort_values(["team", "date", "game_id"]).reset_index(drop=True)

    # ---- previous-game / streak context (within season)
    t["beat_margin"] = ((t.margin - t.proj_margin) > 0).astype(float).where(t.proj_margin.notna())
    t["over_total"] = ((t.total - t.proj_total) > 0).astype(float).where(t.proj_total.notna())
    t["over_team"] = ((t.pts - t.proj_pts) > 0).astype(float).where(t.proj_pts.notna())
    t["blowout_win"] = (t.margin >= 10).astype(int)
    t["ot"] = (t.n_periods > 4).astype(int)
    g = t.groupby(["team", "season"])
    t["prev_margin"] = g.margin.shift(1)
    t["prev_win"] = g.win.shift(1)
    t["vs_proj"] = t.margin - t.proj_margin
    t["prev_vs_proj"] = t.groupby(["team", "season"]).vs_proj.shift(1)
    t["prev_total"] = g.total.shift(1)
    t["prev_ot"] = g.ot.shift(1)

    def run_len(w):
        out, cur = [], 0
        for x in w.tolist():
            out.append(cur)                                   # streak entering this game
            cur = (cur + 1 if cur > 0 else 1) if x == 1 else (cur - 1 if cur < 0 else -1)
        return pd.Series(out, index=w.index)
    t["streak_in"] = g.win.transform(run_len)
    t["wins_in"] = g.win.transform(lambda s: s.cumsum() - s)
    t["pct_in"] = t.wins_in / (t.game_no - 1).replace(0, np.nan)
    oppw = t[["game_id", "team", "pct_in", "game_no"]].rename(columns={"team": "opp", "pct_in": "opp_pct_in", "game_no": "opp_game_no"})
    t = t.merge(oppw, on=["game_id", "opp"], how="left").sort_values(["team", "date", "game_id"]).reset_index(drop=True)
    return t


# ----------------------------------------------------------------------------------------------- labels
def _rest_label(x):
    if pd.isna(x):
        return "opener"
    return "B2B" if x == 0 else ("1d" if x == 1 else ("2d" if x == 2 else "3d+"))


def add_labels(t: pd.DataFrame) -> pd.DataFrame:
    """Categorical situation labels used by the miner (each row gets one value per feature)."""
    L = pd.DataFrame(index=t.index)
    L["venue"] = np.where(t.home == 1, "home", "away")
    L["rest"] = t.rest.map(_rest_label)
    L["opp_rest"] = t.opp_rest.map(_rest_label)
    edge = np.sign(t.rest.clip(upper=3).fillna(9) - t.opp_rest.clip(upper=3).fillna(9))
    L["rest_edge"] = np.where(t.rest.isna() | t.opp_rest.isna(), "n/a", np.where(edge > 0, "more rest", np.where(edge < 0, "less rest", "equal rest")))
    L["next_day_game"] = np.where(t.next_gap == 0, "plays tomorrow", "no game tomorrow")
    L["density"] = np.where(t.three_in_four == 1, "3-in-4", "normal")
    pw = t.p_win
    L["favorite"] = pd.cut(pw, [0, .25, .40, .60, .75, 1.0], labels=["heavy dog", "dog", "pick'em", "fav", "heavy fav"]).astype(object)
    L["proj_total"] = pd.cut(t.proj_total, [0, 220, 225, 230, 235, 400], labels=["<220", "220-225", "225-230", "230-235", "235+"]).astype(object)
    L["proj_pts"] = pd.cut(t.proj_pts, [0, 108, 112, 116, 120, 300], labels=["<108", "108-112", "112-116", "116-120", "120+"]).astype(object)
    L["prev_result"] = np.where(t.prev_win.isna(), "n/a", np.where(t.prev_margin >= 10, "won by 10+", np.where(t.prev_win == 1, "won close", np.where(t.prev_margin <= -10, "lost by 10+", "lost close"))))
    L["prev_vs_model"] = np.where(t.prev_vs_proj.isna(), "n/a", np.where(t.prev_vs_proj >= 8, "beat model by 8+", np.where(t.prev_vs_proj <= -8, "missed model by 8+", "near model")))
    L["prev_total"] = np.where(t.prev_total.isna(), "n/a", np.where(t.prev_total >= 240, "high-scoring (240+)", np.where(t.prev_total <= 215, "low-scoring (<=215)", "normal")))
    L["prev_ot"] = np.where(t.prev_ot == 1, "prev went OT", "prev regulation")
    L["streak"] = np.where(t.streak_in >= 3, "won 3+ straight", np.where(t.streak_in <= -3, "lost 3+ straight", "no streak"))
    L["record"] = np.where(t.game_no < 16, "n/a", np.where(t.pct_in >= .6, "good team (.600+)", np.where(t.pct_in <= .4, "bad team (.400-)", "middling")))
    L["opp_record"] = np.where(t.opp_game_no < 16, "n/a", np.where(t.opp_pct_in >= .6, "good opp (.600+)", np.where(t.opp_pct_in <= .4, "bad opp (.400-)", "middling opp")))
    L["month"] = t.date.dt.strftime("%b")
    L["weekday"] = t.date.dt.strftime("%a")
    L["part"] = np.where(t.game_no <= 20, "first 20 games", np.where(t.game_no >= 62, "last 20 games", "middle"))
    L["team"] = t.team
    L["opponent"] = t.opp
    return L


# ----------------------------------------------------------------------------------------------- queries
def query(t: pd.DataFrame, expr: str) -> pd.DataFrame:
    """pandas query on the team-game frame. Columns: team, opp, home(1/0), rest (0 = second night of a back-to-back),
    opp_rest, proj_total, proj_pts, proj_margin, p_win, game_no, streak_in, season, ...
    Example: "team=='BOS' and home==1 and rest==0 and proj_total>230"."""
    return t.query(expr, engine="python").sort_values(["date", "game_id"])


def record(rows: pd.DataFrame, outcome: str = "win") -> dict:
    r = rows[rows[outcome].notna()].sort_values(["date", "game_id"])
    x = r[outcome].astype(int).to_numpy()
    n, k = len(x), int(x.sum())
    cur = 0
    for v in x[::-1]:
        if v == x[-1]:
            cur += 1
        else:
            break
    best = cur_b = 0
    for v in x:
        cur_b = cur_b + 1 if v == 1 else 0
        best = max(best, cur_b)
    return {"n": n, "hits": k, "misses": n - k, "rate": k / n if n else float("nan"),
            "current_run": (cur if n and x[-1] == 1 else -cur) if n else 0, "longest_hit_run": best}


# ----------------------------------------------------------------------------------------------- miner
BASE_FEATURES = ["venue", "rest", "opp_rest", "rest_edge", "next_day_game", "density", "favorite", "proj_total",
                 "proj_pts", "prev_result", "prev_vs_model", "prev_total", "prev_ot", "streak", "record",
                 "opp_record", "month", "weekday", "part"]
PROJ_FEATURES = {"favorite", "proj_total", "proj_pts"}


def _indicators(L: pd.DataFrame, feats: list[str]) -> dict:
    ind = {}
    for f in feats:
        for v in L[f].dropna().unique():
            if v in ("n/a",):
                continue
            ind[(f, v)] = (L[f] == v).to_numpy()
    return ind


def mine(t: pd.DataFrame, L: pd.DataFrame, outcomes=("win", "beat_margin", "over_total", "over_team"),
         seasons=None, min_n=40, with_team=True, max_feats=2, fdr=0.10, outcome_df=None) -> pd.DataFrame:
    """Scan situations made of up to `max_feats` situation features (+ optionally a team). Returns every tested
    situation with n, hit rate, expected rate (venue-adjusted), z, p and a Benjamini-Hochberg flag."""
    m = np.ones(len(t), bool) if seasons is None else t.season.isin(seasons).to_numpy()
    tt, LL = t[m], L[m]
    ind = _indicators(LL, BASE_FEATURES)
    keys = list(ind)
    out = []
    hm = tt.home.to_numpy()
    # Row-level expectation: for "win" the model's own win probability (so "good team beats bad team" is NOT a trend);
    # for the other outcomes the venue-specific base rate.
    Y, E = {}, {}
    for oc in outcomes:
        y = tt[oc].to_numpy(float)
        Y[oc] = y
        if oc == "win":
            pw = (0.5 * tt.p_win + 0.5 * tt.elo_p).to_numpy(float)
            E[oc] = pw
            Y[oc] = np.where(np.isnan(pw), np.nan, y)
        else:
            E[oc] = np.where(hm == 1, np.nanmean(y[hm == 1]), np.nanmean(y[hm == 0]))
    teams = [None] + (sorted(tt.team.unique()) if with_team else [])
    tmask = {tm: (tt.team.to_numpy() == tm) for tm in teams if tm}
    combos = [(k,) for k in keys]
    if max_feats >= 2:
        combos += [(a, b) for a, b in itertools.combinations(keys, 2) if a[0] != b[0]]
    for combo in combos:
        cm = ind[combo[0]].copy()
        for k in combo[1:]:
            cm &= ind[k]
        if cm.sum() < min_n:
            continue
        for tm in teams:
            mk = cm if tm is None else cm & tmask[tm]
            need = min_n if tm is None else max(12, min_n // 4)
            if int(mk.sum()) < need:
                continue
            for oc in outcomes:
                y = Y[oc][mk]
                ok = ~np.isnan(y)
                n = int(ok.sum())
                if n < need:
                    continue
                e = E[oc][mk][ok]
                hits = float(y[ok].sum())
                var = float((e * (1 - e)).sum())
                z = (hits - e.sum()) / np.sqrt(var) if var > 0 else 0.0
                out.append((tm or "ALL", " & ".join(f"{k[0]}={k[1]}" for k in combo), oc, n, int(hits), hits / n, float(e.mean()), z))
    df = pd.DataFrame(out, columns=["team", "situation", "outcome", "n", "hits", "rate", "expected", "z"])
    df["p"] = 2 * norm.sf(df.z.abs())
    df = df.sort_values("p").reset_index(drop=True)
    mtests = len(df)
    df["bh_threshold"] = (np.arange(1, mtests + 1) / mtests) * fdr
    passed = df.p <= df.bh_threshold
    last = np.where(passed)[0]
    df["survives_fdr"] = False
    if len(last):
        df.loc[: last.max(), "survives_fdr"] = True
    df.attrs["n_tests"] = mtests
    return df


def holdout(t: pd.DataFrame, L: pd.DataFrame, train_seasons, test_seasons, top=200, **kw) -> dict:
    """Do the best-looking situations from early seasons keep their edge in later seasons?"""
    tr = mine(t, L, seasons=train_seasons, **kw)
    te = mine(t, L, seasons=test_seasons, **{**kw, "min_n": max(10, kw.get("min_n", 40) // 3)})
    key = ["team", "situation", "outcome"]
    j = tr.merge(te, on=key, suffixes=("_tr", "_te"))
    j["edge_tr"] = j.rate_tr - j.expected_tr
    j["edge_te"] = j.rate_te - j.expected_te
    best = j.sort_values("p_tr").head(top)
    sign_keep = ((np.sign(best.edge_tr) == np.sign(best.edge_te)) & (best.edge_te != 0)).mean()
    allj = j[j.p_tr < 0.05]
    return {"n_compared": len(j), "top": top, "top_mean_edge_train": float(best.edge_tr.mean()),
            "top_mean_edge_test": float(best.edge_te.mean()),
            "top_share_same_direction": float(sign_keep),
            "corr_all": float(np.corrcoef(j.edge_tr, j.edge_te)[0, 1]),
            "p05_mean_edge_train": float(allj.edge_tr.abs().mean()), "p05_n": int(len(allj)),
            "p05_signed_test_edge": float((np.sign(allj.edge_tr) * allj.edge_te).mean()),
            "frame": best}


def perfect_records(t: pd.DataFrame, L: pd.DataFrame, outcome="win", min_n=12, seasons=None,
                    simulate_seed: int | None = None) -> pd.DataFrame:
    """Team-specific situations (<=3 features) where a team went perfect (or winless), e.g. 22-0.
    Adds the model's own chance of such a run (product of its pre-game win probabilities) so an easy schedule is
    not mistaken for a trend. With `simulate_seed`, outcomes are re-drawn from the model's probabilities (a null world
    in which NO situation matters) to show how many perfect runs luck alone produces."""
    m = np.ones(len(t), bool) if seasons is None else t.season.isin(seasons).to_numpy()
    tt, LL = t[m].reset_index(drop=True), L[m].reset_index(drop=True)
    pw = (0.5 * tt.p_win + 0.5 * tt.elo_p).to_numpy(float)
    y = tt[outcome].to_numpy(float)
    if simulate_seed is not None:
        y = (np.random.default_rng(simulate_seed).random(len(tt)) < pw).astype(float)
    y = np.where(np.isnan(pw), np.nan, y)
    feats = ["venue", "rest", "opp_rest", "favorite", "proj_total", "prev_result", "streak", "next_day_game", "opp_record"]
    ind = _indicators(LL, feats)
    keys = list(ind)
    res = []
    tm_arr = tt.team.to_numpy()
    for tm in sorted(set(tm_arr)):
        tmk = tm_arr == tm
        yy, pp = y[tmk], pw[tmk]
        sub = {k: v[tmk] for k, v in ind.items()}
        for r in (1, 2, 3):
            for combo in itertools.combinations(keys, r):
                if len({c[0] for c in combo}) < r:
                    continue
                cm = sub[combo[0]].copy()
                for c in combo[1:]:
                    cm &= sub[c]
                cm &= ~np.isnan(yy)
                n = int(cm.sum())
                if n >= min_n:
                    h = int(yy[cm].sum())
                    if h == n or h == 0:
                        pr = pp[cm]
                        prob = float(np.prod(pr if h == n else 1 - pr))
                        res.append((tm, " & ".join(f"{c[0]}={c[1]}" for c in combo), n, h, float(pr.sum()), prob))
    return pd.DataFrame(res, columns=["team", "situation", "n", "wins", "model_expected_wins", "model_chance_of_this_run"])


# ----------------------------------------------------------------------------------------------- situation builder
def select(t: pd.DataFrame, L: pd.DataFrame, labels: dict | None = None, ranges: dict | None = None,
           seasons=None) -> pd.DataFrame:
    """Rows matching a situation. labels: {"rest": ["B2B"], "venue": ["home"], "team": ["BOS"], ...} (any listed value);
    ranges: {"proj_total": (212.5, None), "proj_pts": (None, 110)} numeric bounds (None = open)."""
    m = np.ones(len(t), bool)
    if seasons is not None:
        m &= t.season.isin(list(seasons)).to_numpy()
    for k, vals in (labels or {}).items():
        if vals:
            m &= L[k].isin(list(vals)).to_numpy()
    for k, (lo, hi) in (ranges or {}).items():
        col = t[k]
        if lo is not None:
            m &= (col >= lo).to_numpy()
        if hi is not None:
            m &= (col <= hi).to_numpy()
    return t[m].sort_values(["date", "game_id"])


def summarize_situation(rows: pd.DataFrame, t: pd.DataFrame) -> pd.DataFrame:
    """Per outcome: n, hits, hit rate, what the model/base rate expected, current and longest hit run."""
    bases = {oc: {v: np.nanmean(t.loc[(t.home == v) & t[oc].notna(), oc]) for v in (0, 1)} for oc in OUTCOMES if oc != "win"}
    out = []
    for oc, desc in OUTCOMES.items():
        r = rows[rows[oc].notna()]
        if oc == "win":
            r = r[r.p_win.notna()]
            e = (0.5 * r.p_win + 0.5 * r.elo_p).to_numpy(float)
        else:
            e = np.where(r.home == 1, bases[oc][1], bases[oc][0]).astype(float) if len(r) else np.array([])
        if not len(r):
            continue
        rec = record(r, oc)
        var = float((e * (1 - e)).sum())
        z = (rec["hits"] - e.sum()) / np.sqrt(var) if var > 0 else 0.0
        out.append({"outcome": desc, "n": rec["n"], "hits": rec["hits"], "misses": rec["misses"],
                    "hit rate": rec["rate"], "expected rate": float(e.mean()), "z (vs expected)": z,
                    "current run": rec["current_run"], "longest hit run": rec["longest_hit_run"]})
    return pd.DataFrame(out)


def league_trends(t: pd.DataFrame, L: pd.DataFrame, top=30, min_n=60) -> pd.DataFrame:
    """League-wide situations (<=2 features) that beat the model's expectation, with a train/test split:
    found on 2023-24, re-measured on 2025-26 (edge = hit rate minus expected rate)."""
    tr = mine(t, L, seasons=[2023, 2024], with_team=False, min_n=min_n)
    te = mine(t, L, seasons=[2025, 2026], with_team=False, min_n=max(10, min_n // 3))
    key = ["team", "situation", "outcome"]
    j = tr.merge(te, on=key, suffixes=("_found", "_later"))
    j["edge_found"] = j.rate_found - j.expected_found
    j["edge_later"] = j.rate_later - j.expected_later
    j["held_up"] = np.sign(j.edge_found) == np.sign(j.edge_later)
    j = j[j.survives_fdr_found].sort_values("p_found")
    cols = ["situation", "outcome", "n_found", "rate_found", "expected_found", "edge_found", "n_later", "rate_later",
            "edge_later", "held_up"]
    return j[cols].head(top).reset_index(drop=True)
