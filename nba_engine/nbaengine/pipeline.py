"""Self-updating loop: ingest finished games -> update state -> forecast today's slate -> store -> report.

Rules enforced here:
* a game is forecast only while it is still scheduled (before tip-off) and only once; forecasts are immutable;
* state (Elo, team profiles, online corrections) is updated from a result only AFTER that game's forecast exists;
* every run records what it fetched and whether it succeeded, so staleness is visible;
* nothing is retrained or re-tuned automatically; `monitor` only reports drift.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import date, datetime, timedelta, timezone

from . import MODEL_VERSION
from .backtest import RunningSD, _norm_q
from .elo import ELO_PER_POINT, Elo, EloParams
from .feed import FinalGame, UpcomingGame
from .sim import ProfileParams, TeamProfiles, apply_dispersion, simulate_game, summarize
from .store import Store, now_utc

SEED0 = 20261017
ALPHA_LATE, ALPHA_EARLY, N_EARLY = 0.01, 0.03, 60     # online scoring-level tracker: faster for the first N games of a season; level restarts at 0 each season
EXTRA_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs(run_id INTEGER PRIMARY KEY AUTOINCREMENT, started_utc TEXT, finished_utc TEXT,
  today TEXT, ok INTEGER, finals_ingested INTEGER, forecasts_made INTEGER, forecasts_skipped_late INTEGER, error TEXT);
CREATE TABLE IF NOT EXISTS game_dates(season INTEGER, game_id INTEGER, date TEXT, PRIMARY KEY(season, game_id));
CREATE TABLE IF NOT EXISTS team_box(season INTEGER, game_id INTEGER, side TEXT, team TEXT, opp TEXT, n_periods INTEGER, pts INTEGER,
  fga INTEGER, fgm INTEGER, fg3a INTEGER, fg3m INTEGER, fta INTEGER, ftm INTEGER, tov INTEGER, oreb INTEGER, dreb INTEGER,
  PRIMARY KEY(season, game_id, side));
"""
BOX_COLS = ("fga", "fgm", "3pa", "3pm", "fta", "ftm", "tov", "oreb", "dreb")


def _sd_to(r): return {"s": r.s, "n": r.n, "prior": list(r.prior)}
def _sd_from(d):
    r = RunningSD(1.0); r.s, r.n, r.prior = d["s"], d["n"], tuple(d["prior"]); return r


class Engine:
    def __init__(self, store: Store, elo: Elo, prof: TeamProfiles, kappa_m: float, kappa_t: float,
                 level_delta: float, base: dict, sds: dict, applied: set):
        self.store, self.elo, self.prof = store, elo, prof
        self.kappa_m, self.kappa_t, self.level_delta = kappa_m, kappa_t, level_delta
        self.base, self.sds, self.applied = base, sds, applied
        self.alpha = ALPHA_LATE
        self.level_n = 0             # games used to learn the scoring level in the current season
        self.level_season = None     # season the level belongs to; it restarts at 0 when the season changes
        self.last_margin = {}        # team -> [ISO date, margin] of its latest game seen (for the after-a-10+-win effect)
        self.last_played = {}        # team -> ISO date of its latest game seen (for back-to-back detection)
        self.rest_coef = None        # {'home_b2b': .., 'away_b2b': ..} margin points; set by the daily job
        self.injury_fn = None        # optional f(home, away) -> (margin_shift, detail); set by the daily job
        store.con.executescript(EXTRA_SCHEMA)

    # ---------------- persistence (plain JSON; diffable, no pickle)
    def to_dict(self) -> dict:
        p = self.prof
        return {"version": 1, "model_version": MODEL_VERSION,
                "elo": {"params": vars(self.elo.params), "ratings": self.elo.ratings, "season": self.elo.season},
                "prof": {"params": vars(p.p), "off": p.off, "deff": p.deff, "pace_w": p.pace_w, "lg_side": p.lg_side,
                         "lg_pace": p.lg_pace, "pace_sq": p.pace_sq, "season": p.season},
                "kappa_m": self.kappa_m, "kappa_t": self.kappa_t, "level_delta": self.level_delta,
                "base": self.base, "sds": {k: _sd_to(v) for k, v in self.sds.items()},
                "applied": sorted(self.applied), "last_played": self.last_played, "last_margin": self.last_margin,
                "level_n": self.level_n, "level_season": self.level_season}

    def save_state(self, path: str) -> None:
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.to_dict(), f)
        os.replace(tmp, path)

    @classmethod
    def from_dict(cls, store: Store, d: dict) -> "Engine":
        elo = Elo(EloParams(**d["elo"]["params"])); elo.ratings = d["elo"]["ratings"]; elo.season = d["elo"]["season"]
        prof = TeamProfiles(ProfileParams(**d["prof"]["params"]))
        for k in ("off", "deff", "pace_w", "lg_side", "lg_pace", "pace_sq", "season"):
            setattr(prof, k, d["prof"][k])
        eng = cls(store, elo, prof, d["kappa_m"], d["kappa_t"], d["level_delta"], d["base"],
                  {k: _sd_from(v) for k, v in d["sds"].items()}, set(d["applied"]))
        eng.last_played = dict(d.get("last_played", {}))
        eng.last_margin = dict(d.get("last_margin", {}))
        eng.level_n, eng.level_season = d.get("level_n", 0), d.get("level_season")
        return eng

    @classmethod
    def load(cls, store: Store, path: str) -> "Engine":
        return cls.from_dict(store, json.load(open(path)))

    # ---------------- ingest a finished game (state update happens AFTER its forecast was stored)
    def _roll_level(self, season: int) -> None:
        """The level correction learned from last season's surprises does not carry into a new season: restart at 0."""
        if self.level_season is None:
            self.level_season = season                      # old state files: keep what was learned, adopt the label
        elif season != self.level_season:
            self.level_delta, self.level_n, self.level_season = 0.0, 0, season

    def _stored(self, season, gid, model):
        r = self.store.con.execute("SELECT mean_margin, mean_total, details_json FROM forecasts WHERE season=? AND game_id=? "
                                   "AND model_name=? AND model_version=?", (season, gid, model, MODEL_VERSION)).fetchone()
        return None if r is None else (r[0], r[1], json.loads(r[2]) if r[2] else {})

    def ingest(self, fg: FinalGame) -> bool:
        key = f"{fg.season}:{fg.game_id}"
        self.store.con.execute("INSERT OR IGNORE INTO game_dates VALUES(?,?,?)", (fg.season, fg.game_id, fg.date))
        try:                                           # full team box score, kept for the team-stat report (also repairs older days on re-ingest)
            for side, tm, op, pts in (("home", fg.home, fg.away, fg.home_pts), ("away", fg.away, fg.home, fg.away_pts)):
                if all(f"{side}_{c}" in fg.box for c in BOX_COLS):
                    self.store.con.execute("INSERT OR IGNORE INTO team_box VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                           (fg.season, fg.game_id, side, tm, op, fg.n_periods, pts, *[int(fg.box[f"{side}_{c}"]) for c in BOX_COLS]))
        except Exception:
            pass
        for tm in (fg.home, fg.away):                 # schedule memory, updated even for already-applied games
            if fg.date >= self.last_played.get(tm, ""):     # ">=": re-ingesting a day repairs fields added later
                self.last_played[tm] = fg.date
                self.last_margin[tm] = [fg.date, (fg.home_pts - fg.away_pts) * (1 if tm == fg.home else -1)]
        if key in self.applied:
            return False
        gd = {"game_id": fg.game_id, "season": fg.season, "home": fg.home, "away": fg.away, "home_pts": fg.home_pts,
              "away_pts": fg.away_pts, "n_periods": fg.n_periods, **fg.box}
        self.elo.new_season(fg.season); self.prof.new_season(fg.season)
        con = self.store.con
        con.execute("INSERT OR IGNORE INTO games VALUES(?,?,?,?,?,?)",
                    (fg.season, fg.game_id, len(self.applied), fg.home, fg.away, fg.n_periods))
        self.store.add_result(fg.season, fg.game_id, fg.home_pts, fg.away_pts)
        am, at = fg.home_pts - fg.away_pts, fg.home_pts + fg.away_pts
        e, b, r = (self._stored(fg.season, fg.game_id, m) for m in ("elo", "home_const", "sim_mc_raw"))
        pred_poss = (r[2].get("mean_poss") if r else None) or self.prof.expected_poss(fg.home, fg.away)
        if e and b and r:      # forecasts existed before the result: update the online correction trackers
            self._roll_level(fg.season)
            a = ALPHA_EARLY if self.level_n < N_EARLY else self.alpha
            self.level_delta = (1 - a) * self.level_delta + a * (at - r[1])
            self.level_n += 1
            self.sds["elo"].add(am - e[2]["exp_margin"])
            self.sds["base_m"].add(am - b[0]); self.sds["base_t"].add(at - b[1])
        self.base["n"] += 1; self.base["hw"] += float(am > 0); self.base["m"] += am; self.base["t"] += at
        self.elo.update(fg.home, fg.away, fg.home_pts, fg.away_pts)
        self.prof.record_pace_residual(pred_poss, gd)
        self.prof.update(gd)
        self.applied.add(key)
        return True

    # ---------------- forecast an upcoming game (once; immutable)
    def forecast(self, ug: UpcomingGame, n_sims: int, now_iso: str, enforce_tip: bool = True) -> str:
        con = self.store.con
        if con.execute("SELECT 1 FROM forecasts WHERE season=? AND game_id=? AND model_name='sim_mc'",
                       (ug.season, ug.game_id)).fetchone():
            return "exists"
        if enforce_tip and ug.tip_utc:
            parse = lambda x: datetime.fromisoformat(x.replace("Z", "+00:00")).astimezone(timezone.utc)
            if parse(ug.tip_utc) <= parse(now_iso):
                return "late"
        self.elo.new_season(ug.season); self.prof.new_season(ug.season)
        self._roll_level(ug.season)
        s, gid, h, a = ug.season, ug.game_id, ug.home, ug.away
        cutoff = now_iso
        seed = SEED0 + gid
        base = self.base
        bhw, bm, bt = base["hw"] / base["n"], base["m"] / base["n"], base["t"] / base["n"]
        e = self.elo.predict(h, a); sd_e = self.sds["elo"].sd()
        sv = self.store.save_forecast
        sv(s, gid, "elo", MODEL_VERSION, cutoff, None, None, e["p_home"], (bt + e["exp_margin"]) / 2,
           (bt - e["exp_margin"]) / 2, None, None, q_margin=_norm_q(e["exp_margin"], sd_e),
           details={"elo_diff": e["elo_diff"], "margin_sd": sd_e, "exp_margin": e["exp_margin"]})
        sv(s, gid, "home_const", MODEL_VERSION, cutoff, None, None, bhw, (bt + bm) / 2, (bt - bm) / 2, bt, None,
           q_margin=_norm_q(bm, self.sds["base_m"].sd()), q_total=_norm_q(bt, self.sds["base_t"].sd()), details={})
        sim = simulate_game(self.prof, h, a, n_sims, seed, 0.0, track=True)     # tracking adds no random draws: same scores as before
        raw = summarize(sim)
        cal = summarize(apply_dispersion(sim, self.kappa_m, self.kappa_t, self.level_delta))
        mk = {"market": ug.market} if ug.market else {}
        for name, sm, det in (("sim_mc_raw", raw, {}), ("sim_mc", cal, {"level_delta": self.level_delta, "level_n": self.level_n, **mk})):
            sv(s, gid, name, MODEL_VERSION, cutoff, seed, n_sims, sm["p_home"], sm["mean_home"], sm["mean_away"],
               sm["mean_total"], sm["p_ot"], q_margin=sm["q_margin"], q_total=sm["q_total"],
               details={**det, "mc_se_p_home": sm["mc_se_p_home"], "mean_poss": sm["mean_poss"],
                        "modal_score": [sm["modal_score_home"], sm["modal_score_away"]],
                        "median_score": [sm["median_home"], sm["median_away"]], "tip_utc": ug.tip_utc, "date": ug.date,
                        "home": h, "away": a,
                        "team_box": {sd: {k: round(float(v.mean()), 2) for k, v in sim["box_" + sd].items()} for sd in ("home", "away")}})
        con.execute("INSERT OR IGNORE INTO game_dates VALUES(?,?,?)", (s, gid, ug.date))
        self._forecast_injury_adjusted(ug, sim, e, bt, n_sims, seed, cutoff)
        self._forecast_rest_adjusted(ug, sim, e, bt, n_sims, seed, cutoff)
        return "made"

    def rest_shift(self, ug) -> tuple[float, dict] | None:
        """Margin shift (home perspective) for teams on the second night of a back-to-back, from the fitted effect."""
        if not self.rest_coef:
            return None
        day = date.fromisoformat(ug.date)
        def b2b(tm):
            lp = self.last_played.get(tm)
            return bool(lp) and (day - date.fromisoformat(lp)).days == 1
        hb, ab = b2b(ug.home), b2b(ug.away)
        return (self.rest_coef["home_b2b"] * hb + self.rest_coef["away_b2b"] * ab), {"home_b2b": hb, "away_b2b": ab}

    def _save_shifted(self, ug, sim, e, bt, n_sims, seed, cutoff, tag: str, shift: float, det: dict) -> None:
        s, gid, h, a = ug.season, ug.game_id, ug.home, ug.away
        sv = self.store.save_forecast
        em = e["exp_margin"] + shift
        d2 = e["elo_diff"] + ELO_PER_POINT * shift
        info = {"shift": shift, "date": ug.date, "home": h, "away": a, **det}
        sv(s, gid, f"elo_{tag}", MODEL_VERSION, cutoff, None, None, 1.0 / (1.0 + 10.0 ** (-d2 / 400.0)), (bt + em) / 2, (bt - em) / 2,
           None, None, q_margin=_norm_q(em, self.sds["elo"].sd()), details=info)
        sm = summarize(apply_dispersion(sim, self.kappa_m, self.kappa_t, self.level_delta, margin_shift=shift))
        sv(s, gid, f"sim_mc_{tag}", MODEL_VERSION, cutoff, seed, n_sims, sm["p_home"], sm["mean_home"], sm["mean_away"], sm["mean_total"],
           sm["p_ot"], q_margin=sm["q_margin"], q_total=sm["q_total"],
           details={**info, "modal_score": [sm["modal_score_home"], sm["modal_score_away"]]})

    def _forecast_rest_adjusted(self, ug, sim, e, bt, n_sims, seed, cutoff) -> None:
        """Separately named forecasts: `*_rest` (back-to-back effect only) and `*_full` (rest + injuries, when both exist). Never raises."""
        try:
            rs = self.rest_shift(ug)
            if rs is None:
                return
            shift, det = rs
            self._save_shifted(ug, sim, e, bt, n_sims, seed, cutoff, "rest", shift, det)
            ir = self.injury_fn(ug.home, ug.away) if self.injury_fn else None
            if ir is not None:
                self._save_shifted(ug, sim, e, bt, n_sims, seed, cutoff, "full", shift + ir[0],
                                   {**det, "injury_shift": ir[0], "rest_shift": shift})
            sit = self.rest_coef.get("sit")
            if sit:                       # back-to-back + coming off a 10+ point win (fitted jointly)
                day = date.fromisoformat(ug.date)
                def big_win(tm):
                    lm = self.last_margin.get(tm)
                    return bool(lm) and lm[1] >= 10 and 0 < (day - date.fromisoformat(lm[0])).days <= 10
                hw, aw = big_win(ug.home), big_win(ug.away)
                ssh = sit["home_b2b"] * det["home_b2b"] + sit["away_b2b"] * det["away_b2b"] + sit["after_10plus_win"] * (hw - aw)
                d2 = {**det, "home_after_big_win": hw, "away_after_big_win": aw}
                self._save_shifted(ug, sim, e, bt, n_sims, seed, cutoff, "sit", ssh, d2)
                if ir is not None:
                    self._save_shifted(ug, sim, e, bt, n_sims, seed, cutoff, "all", ssh + ir[0],
                                       {**d2, "injury_shift": ir[0], "situational_shift": ssh})
        except Exception:
            pass

    def _forecast_injury_adjusted(self, ug, sim, e, bt, n_sims, seed, cutoff) -> None:
        """Extra, separately named forecasts that shift the margin for players ESPN lists as out. Never raises."""
        try:
            if self.injury_fn is None:
                return
            r = self.injury_fn(ug.home, ug.away)
            if r is None:
                return
            shift, det = r
            s, gid, h, a = ug.season, ug.game_id, ug.home, ug.away
            sv = self.store.save_forecast
            em = e["exp_margin"] + shift
            d2 = e["elo_diff"] + ELO_PER_POINT * shift
            sv(s, gid, "elo_inj", MODEL_VERSION, cutoff, None, None, 1.0 / (1.0 + 10.0 ** (-d2 / 400.0)), (bt + em) / 2, (bt - em) / 2,
               None, None, q_margin=_norm_q(em, self.sds["elo"].sd()),
               details={"injury_shift": shift, "date": ug.date, "home": h, "away": a, **det})
            sm = summarize(apply_dispersion(sim, self.kappa_m, self.kappa_t, self.level_delta, margin_shift=shift))
            sv(s, gid, "sim_mc_inj", MODEL_VERSION, cutoff, seed, n_sims, sm["p_home"], sm["mean_home"], sm["mean_away"], sm["mean_total"],
               sm["p_ot"], q_margin=sm["q_margin"], q_total=sm["q_total"],
               details={"injury_shift": shift, "date": ug.date, "home": h, "away": a,
                        "modal_score": [sm["modal_score_home"], sm["modal_score_away"]], **det})
        except Exception:
            pass


# ----------------------------------------------------------------------------
def _ymd(d: date) -> str:
    return d.strftime("%Y%m%d")


def run_update(engine: Engine, feed, today: date, n_sims: int = 10000, now_iso: str | None = None,
               lookback_days: int = 3, enforce_tip: bool = True) -> dict:
    """One daily run. Results come from the `lookback_days` days BEFORE `today`; forecasts only for today's slate."""
    started = now_utc()
    now_iso = now_iso or started
    con = engine.store.con
    summary = {"today": str(today), "finals_ingested": 0, "forecasts_made": 0, "forecasts_late": 0, "ok": 1, "error": None}
    try:
        finals = []
        for k in range(lookback_days, 0, -1):
            fin, _ = feed.scoreboard(_ymd(today - timedelta(days=k)))
            finals += fin
        for fg in sorted(finals, key=lambda g: (g.date, g.game_id)):
            summary["finals_ingested"] += int(engine.ingest(fg))
        engine.store.commit()
        _, up = feed.scoreboard(_ymd(today))
        for ug in sorted(up, key=lambda g: (g.tip_utc, g.game_id)):
            r = engine.forecast(ug, n_sims, now_iso, enforce_tip)
            summary["forecasts_made"] += int(r == "made"); summary["forecasts_late"] += int(r == "late")
        engine.store.commit()
    except Exception as ex:           # a failed refresh must be visible, never silent
        summary["ok"], summary["error"] = 0, f"{type(ex).__name__}: {ex}"
    con.execute("INSERT INTO runs(started_utc,finished_utc,today,ok,finals_ingested,forecasts_made,forecasts_skipped_late,error)"
                " VALUES(?,?,?,?,?,?,?,?)", (started, now_utc(), str(today), summary["ok"], summary["finals_ingested"],
                                             summary["forecasts_made"], summary["forecasts_late"], summary["error"]))
    con.commit()
    return summary


def last_success(store: Store) -> str | None:
    r = store.con.execute("SELECT finished_utc FROM runs WHERE ok=1 ORDER BY run_id DESC LIMIT 1").fetchone()
    return r[0] if r else None


def monitor(store: Store, window: int = 200, ref_log_loss: float = 0.6162) -> list[str]:
    """Report-only drift check. Never changes any model."""
    from .backtest import evaluate, metrics
    df = evaluate(store)
    if df.empty:
        return ["monitor: no completed forecasted games yet"]
    ids = sorted(df.game_id.unique())[-window:]
    d = df[df.game_id.isin(ids)]
    m = metrics(d)
    out = [f"monitor: last {len(ids)} completed forecasted games - log loss " +
           ", ".join(f"{k}={v:.4f}" for k, v in m["log_loss"].items())]
    if len(ids) >= 100:
        if m.loc["sim_mc", "log_loss"] > ref_log_loss + 0.04:
            out.append(f"  FLAG: sim_mc log loss exceeds backtest reference ({ref_log_loss}) by more than 0.04 - review, do not auto-retune")
        if m.loc["sim_mc", "log_loss"] > m.loc["elo", "log_loss"] + 0.02:
            out.append("  FLAG: simulator is >0.02 worse than Elo on this window")
    else:
        out.append("  (fewer than 100 games: too noisy to judge drift)")
    return out


def write_report(store: Store, today: date, path: str) -> str:
    q = """SELECT f.game_id, f.model_name, f.p_home, f.mean_home, f.mean_away, f.mean_total, f.p_ot, f.q_margin_json,
                  f.q_total_json, f.details_json, g.home, g.away FROM forecasts f LEFT JOIN games g USING(season, game_id)"""
    rows = store.con.execute(q).fetchall()
    by = {}
    for r in rows:
        det = json.loads(r[9]) if r[9] else {}
        by.setdefault(r[0], {})[r[1]] = (r, det)
    try:      # display calibration constants from scripts/calibration_report.py (never change a stored forecast)
        dc = json.load(open(os.path.join(os.path.dirname(path) or ".", "..", "calibration.json")))["display_constants"]
    except Exception:
        dc = {}
    ots, mis = float(dc.get("ot_scale", 1.0)), float(dc.get("margin_interval_scale", 1.0))
    tis = float(dc.get("total_interval_scale", 1.0))
    sc = lambda q, k, f: q["50"] + f * (q[k] - q["50"])
    lines = [f"# NBA forecasts for {today}", f"Data refresh: last successful run {last_success(store)} UTC. Model {MODEL_VERSION}.", ""]
    for gid, m in by.items():
        s = m.get("sim_mc")
        if not s or s[1].get("date") != str(today):
            continue
        r, det = s
        qm, qt = json.loads(r[7]), json.loads(r[8])
        el = m["elo"][0][2] if "elo" in m else float("nan")
        lines.append(f"- {det['away']} at {det['home']} (game {gid}): P(home) sim {r[2]:.3f} / Elo {el:.3f}; mean score {r[3]:.1f}-{r[4]:.1f} (total {r[5]:.1f}); "
                     f"margin 50% [{sc(qm, '25', mis):.1f}, {sc(qm, '75', mis):.1f}], 80% [{sc(qm, '10', mis):.1f}, {sc(qm, '90', mis):.1f}]; total 80% [{sc(qt, '10', tis):.1f}, {sc(qt, '90', tis):.1f}]; "
                     f"P(OT) {min(0.25, r[6] * ots):.3f}; most frequent exact score {det['modal_score'][0]}-{det['modal_score'][1]} (rarely hit).")
        ij = m.get("sim_mc_inj")
        if ij:
            d2 = ij[1]
            outs = [f"{n} (home)" for n, _ in d2.get("home_out", [])] + [f"{n} (away)" for n, _ in d2.get("away_out", [])]
            lines.append(f"  - injury-adjusted: P(home) sim {ij[0][2]:.3f}, margin shift {d2.get('injury_shift', 0):+.1f} pts; "
                         f"rotation players listed out: {', '.join(outs) if outs else 'none'}.")
        fu = m.get("sim_mc_full") or m.get("sim_mc_rest")
        if fu:
            d3 = fu[1]
            who = [t for t, f in (("home", d3.get("home_b2b")), ("away", d3.get("away_b2b"))) if f]
            lines.append(f"  - with rest{' and injuries' if m.get('sim_mc_full') else ''}: P(home) sim {fu[0][2]:.3f}, margin shift {d3.get('shift', 0):+.1f} pts; "
                         f"second night of a back-to-back: {', '.join(who) if who else 'neither team'}.")
        al = m.get("sim_mc_all") or m.get("sim_mc_sit")
        if al:
            d4 = al[1]
            fm = [t for t, f in (("home", d4.get("home_after_big_win")), ("away", d4.get("away_after_big_win"))) if f]
            lines.append(f"  - with back-to-back, form{' and injuries' if m.get('sim_mc_all') else ''}: P(home) sim {al[0][2]:.3f}, margin shift {d4.get('shift', 0):+.1f} pts; "
                         f"coming off a 10+ point win: {', '.join(fm) if fm else 'neither team'}.")
    lines += ["", *monitor(store), "",
              "Known gaps: injuries come only from ESPN's unofficial list; no confirmed lineups, no travel distance; rest/injury-adjusted lines are separate and experimental (rest effect fitted on 2023-2026 projections, see artifacts/rest_fit.json)."]
    open(path, "w").write("\n".join(lines))
    return "\n".join(lines)
