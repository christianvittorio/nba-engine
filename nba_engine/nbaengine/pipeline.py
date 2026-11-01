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
EXTRA_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs(run_id INTEGER PRIMARY KEY AUTOINCREMENT, started_utc TEXT, finished_utc TEXT,
  today TEXT, ok INTEGER, finals_ingested INTEGER, forecasts_made INTEGER, forecasts_skipped_late INTEGER, error TEXT);
"""


def _sd_to(r): return {"s": r.s, "n": r.n, "prior": list(r.prior)}
def _sd_from(d):
    r = RunningSD(1.0); r.s, r.n, r.prior = d["s"], d["n"], tuple(d["prior"]); return r


class Engine:
    def __init__(self, store: Store, elo: Elo, prof: TeamProfiles, kappa_m: float, kappa_t: float,
                 level_delta: float, base: dict, sds: dict, applied: set):
        self.store, self.elo, self.prof = store, elo, prof
        self.kappa_m, self.kappa_t, self.level_delta = kappa_m, kappa_t, level_delta
        self.base, self.sds, self.applied = base, sds, applied
        self.alpha = 0.01
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
                "applied": sorted(self.applied)}

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
        return cls(store, elo, prof, d["kappa_m"], d["kappa_t"], d["level_delta"], d["base"],
                   {k: _sd_from(v) for k, v in d["sds"].items()}, set(d["applied"]))

    @classmethod
    def load(cls, store: Store, path: str) -> "Engine":
        return cls.from_dict(store, json.load(open(path)))

    # ---------------- ingest a finished game (state update happens AFTER its forecast was stored)
    def _stored(self, season, gid, model):
        r = self.store.con.execute("SELECT mean_margin, mean_total, details_json FROM forecasts WHERE season=? AND game_id=? "
                                   "AND model_name=? AND model_version=?", (season, gid, model, MODEL_VERSION)).fetchone()
        return None if r is None else (r[0], r[1], json.loads(r[2]) if r[2] else {})

    def ingest(self, fg: FinalGame) -> bool:
        key = f"{fg.season}:{fg.game_id}"
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
            self.level_delta = (1 - self.alpha) * self.level_delta + self.alpha * (at - r[1])
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
        sim = simulate_game(self.prof, h, a, n_sims, seed, 0.0)
        raw = summarize(sim)
        cal = summarize(apply_dispersion(sim, self.kappa_m, self.kappa_t, self.level_delta))
        mk = {"market": ug.market} if ug.market else {}
        for name, sm, det in (("sim_mc_raw", raw, {}), ("sim_mc", cal, {"level_delta": self.level_delta, **mk})):
            sv(s, gid, name, MODEL_VERSION, cutoff, seed, n_sims, sm["p_home"], sm["mean_home"], sm["mean_away"],
               sm["mean_total"], sm["p_ot"], q_margin=sm["q_margin"], q_total=sm["q_total"],
               details={**det, "mc_se_p_home": sm["mc_se_p_home"], "mean_poss": sm["mean_poss"],
                        "modal_score": [sm["modal_score_home"], sm["modal_score_away"]],
                        "median_score": [sm["median_home"], sm["median_away"]], "tip_utc": ug.tip_utc, "date": ug.date,
                        "home": h, "away": a})
        self._forecast_injury_adjusted(ug, sim, e, bt, n_sims, seed, cutoff)
        return "made"

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
    lines = [f"# NBA forecasts for {today}", f"Data refresh: last successful run {last_success(store)} UTC. Model {MODEL_VERSION}.", ""]
    for gid, m in by.items():
        s = m.get("sim_mc")
        if not s or s[1].get("date") != str(today):
            continue
        r, det = s
        qm, qt = json.loads(r[7]), json.loads(r[8])
        el = m["elo"][0][2] if "elo" in m else float("nan")
        lines.append(f"- {det['away']} at {det['home']} (game {gid}): P(home) sim {r[2]:.3f} / Elo {el:.3f}; mean score {r[3]:.1f}-{r[4]:.1f} (total {r[5]:.1f}); "
                     f"margin 50% [{qm['25']:.1f}, {qm['75']:.1f}], 80% [{qm['10']:.1f}, {qm['90']:.1f}]; total 80% [{qt['10']:.1f}, {qt['90']:.1f}]; "
                     f"P(OT) {r[6]:.3f}; most frequent exact score {det['modal_score'][0]}-{det['modal_score'][1]} (rarely hit).")
        ij = m.get("sim_mc_inj")
        if ij:
            d2 = ij[1]
            outs = [f"{n} (home)" for n, _ in d2.get("home_out", [])] + [f"{n} (away)" for n, _ in d2.get("away_out", [])]
            lines.append(f"  - injury-adjusted: P(home) sim {ij[0][2]:.3f}, margin shift {d2.get('injury_shift', 0):+.1f} pts; "
                         f"rotation players listed out: {', '.join(outs) if outs else 'none'}.")
    lines += ["", *monitor(store), "",
              "Known gaps: injuries come only from ESPN's unofficial list (injury-adjusted lines are separate and experimental), no confirmed lineups, no rest/travel features."]
    open(path, "w").write("\n".join(lines))
    return "\n".join(lines)
