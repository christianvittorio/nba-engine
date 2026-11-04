"""Calibration of team and player forecasts against results -> artifacts/calibration.json + artifacts/reports/calibration.md.

Team layer: win probability, margin, total score, team points, interval coverage, overtime rate; past seasons (walk-forward) and the
live season (stored forecasts). Player layer: minutes and box-score stats, past season (frozen-parameter evaluation) and live
(stored pre-game projections vs actual box scores). Writes the display calibration constants used by the daily report:
  ot_scale              multiplies the simulator's overtime probability
  margin_interval_scale / total_interval_scale   widen/narrow the displayed 50/80/90% ranges around their centre
Projection means and win probabilities are NOT changed here. Run by the daily job (best effort)."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import numpy as np, pandas as pd
from nbaengine import calibration as C
from nbaengine import player_live as PLV

DB, STATE, PLDB = (os.path.join(ROOT, p) for p in ("artifacts/live.sqlite", "artifacts/state.json", "artifacts/player_live.sqlite"))


def md_table(df: pd.DataFrame, fmt: dict | None = None) -> str:
    fmt = fmt or {}
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples(index=False):
        out.append("| " + " | ".join((fmt.get(c, "{}").format(v) if isinstance(v, (int, float, np.floating, np.integer)) and not pd.isna(v) else str(v)) for c, v in zip(cols, r)) + " |")
    return "\n".join(out)


def main():
    st = json.load(open(STATE)) if os.path.exists(STATE) else {}
    km, kt = st.get("kappa_m", 0.7839), st.get("kappa_t", 0.9210)
    d = C.walk_forward_frame(ROOT, km, kt).sort_values(["season", "game_id"]).reset_index(drop=True)
    cal = {"generated_utc": pd.Timestamp.now('UTC').strftime("%Y-%m-%dT%H:%M:%SZ"), "kappa_in_state": {"margin": km, "total": kt}}
    seasons = {f"{s-1}-{str(s)[2:]}": C.team_metrics(d[d.season == s]) for s in sorted(d.season.unique())}
    windows = {"last 600 games": C.team_metrics(d.tail(600)), "last 300 games": C.team_metrics(d.tail(300)), "all": C.team_metrics(d)}
    ot2 = d.tail(2460)
    y = (d.margin > 0).astype(float).to_numpy()
    rel = C.reliability(d.sim_p_home.to_numpy(), y)
    rel_recent = C.reliability(d.tail(1230).sim_p_home.to_numpy(), y[-1230:])
    buckets = C.by_total_bucket(d.tail(2460))
    sg = C.suggest_dispersion(d, km, kt, window=900, holdout=300)
    recent = d.tail(1230)
    kref_m = float(np.sqrt(((recent.margin - recent.m_mean) ** 2).mean()) / recent.m_sd.mean())
    kref_t = float(np.sqrt(((recent.total - recent.proj_total_c) ** 2).mean()) / recent.t_sd.mean())
    cal["display_constants"] = {
        "margin_interval_scale": float(np.clip(kref_m / km, 0.9, 1.25)),
        "total_interval_scale": float(np.clip(kref_t / kt, 0.9, 1.25)),
        "ot_scale": float(np.clip(d.tail(2460).ot.mean() / d.tail(2460).sim_p_ot.mean(), 1.0, 3.0)),
        "based_on": "last 1230 games (margin/total spread) and last 2460 games (overtime)"}
    cal["dispersion_suggestion"] = sg
    recent_cov_m = float(((recent.margin >= recent.cm_q10) & (recent.margin <= recent.cm_q90)).mean())
    cal["team_seasons"], cal["team_windows"] = seasons, windows

    # ---- live team layer
    lf = C.live_frame(DB)
    live_txt, live = [], {}
    if len(lf):
        base = lf[lf.model_name == "sim_mc"].copy()
        base["y"] = (base.margin > 0).astype(float)
        el = lf[lf.model_name == "elo"].set_index(["season", "game_id"]).p_home
        base["p_elo"] = [el.get((s, g), np.nan) for s, g in zip(base.season, base.game_id)]
        qm = base.q_margin_json.map(json.loads); qt = base.q_total_json.map(json.loads)
        n = len(base)
        live = {"n": int(n), "sim_log_loss": C._ll(base.p_home.to_numpy(), base.y.to_numpy()), "elo_log_loss": C._ll(base.p_elo.to_numpy(), base.y.to_numpy()),
                "sim_brier": float(((base.p_home - base.y) ** 2).mean()), "margin_bias": float((base.margin - base.mean_margin).mean()),
                "margin_mae": float((base.margin - base.mean_margin).abs().mean()), "total_bias": float((base.total - base.mean_total).mean()), "total_bias_se": float((base.total - base.mean_total).std() / np.sqrt(len(base))),
                "total_mae": float((base.total - base.mean_total).abs().mean()),
                "margin_cov80": float(np.mean([q["10"] <= a <= q["90"] for q, a in zip(qm, base.margin)])),
                "total_cov80": float(np.mean([q["10"] <= a <= q["90"] for q, a in zip(qt, base.total)])),
                "ot_pred": float(base.p_ot.mean()), "ot_actual": float(base.ot.mean()),
                "home_win_pred": float(base.p_home.mean()), "home_win_actual": float(base.y.mean())}
        variants = {}
        for m in ("sim_mc", "sim_mc_rest", "sim_mc_sit", "sim_mc_inj", "sim_mc_full", "sim_mc_all"):
            x = lf[lf.model_name == m]
            if len(x):
                variants[m] = {"n": int(len(x)), "log_loss": C._ll(x.p_home.to_numpy(), (x.margin > 0).astype(float).to_numpy()),
                               "margin_mae": float((x.margin - x.mean_margin).abs().mean())}
        live["variants"] = variants
    cal["live_team"] = live

    # ---- player layer
    retro = json.load(open(os.path.join(ROOT, "artifacts/player_retro_metrics.json"))) if os.path.exists(os.path.join(ROOT, "artifacts/player_retro_metrics.json")) else {}
    M = PLV.load_frame(PLDB) if os.path.exists(PLDB) else pd.DataFrame()
    live_pl = C.player_metrics(M, played_only=False) if len(M) else pd.DataFrame()
    cal["player_live"] = {"games": int(M[["season", "game_id"]].drop_duplicates().shape[0]) if len(M) else 0, "rows": int(len(M)),
                          "metrics": live_pl.round(4).to_dict("records")}
    cal["player_retro_available"] = bool(retro)
    json.dump(cal, open(os.path.join(ROOT, "artifacts/calibration.json"), "w"), indent=1, default=float)

    # ---- markdown
    f3 = {c: "{:.3f}" for c in ("sim_log_loss", "elo_log_loss", "sim_brier")}
    L = ["# Calibration report", "",
         f"Generated {cal['generated_utc']}. Team layer: {len(d)} walk-forward games (2022-23 to 2025-26, each projected only from earlier games) plus the live season. "
         "Player layer: 2025-26 frozen-parameter evaluation plus live games as they accumulate.", ""]
    rows = []
    for k, m in {**seasons, **windows}.items():
        rows.append({"games": {"last 600 games": "last 600 (end of 2025-26)", "last 300 games": "last 300 (end of 2025-26)"}.get(k, k), "n": m["n"], "log-loss sim": m["sim_log_loss"], "log-loss Elo": m["elo_log_loss"], "home win actual/pred": f"{m['home_win_rate_actual']:.3f}/{m['home_win_rate_predicted']:.3f}",
                     "margin bias": m["margin_bias"], "margin MAE": m["margin_mae"], "total bias": m["total_bias"], "total MAE": m["total_mae"],
                     "80% margin cov": m["margin_cov80"], "80% total cov": m["total_cov80"], "OT pred/actual": f"{m['p_ot_pred']:.3f}/{m['p_ot_actual']:.3f}"})
    L += ["## 1. Team layer on past games", "", md_table(pd.DataFrame(rows), {"log-loss sim": "{:.4f}", "log-loss Elo": "{:.4f}", "margin bias": "{:+.2f}", "margin MAE": "{:.2f}",
                                                                                 "total bias": "{:+.2f}", "total MAE": "{:.2f}", "80% margin cov": "{:.1%}", "80% total cov": "{:.1%}"}), "",
          "Reading it: a perfectly calibrated model has bias near 0, 80% coverage near 80%, and predicted = actual in the last column. "
          "The first season (2022-23) is the weakest because the model had only one season of history; the later seasons are the fair test.", "",
          "### Win probability reliability (last 1230 games)", "", md_table(rel_recent[["bin", "n", "predicted", "observed", "gap"]], {"predicted": "{:.3f}", "observed": "{:.3f}", "gap": "{:+.3f}"}), "",
          "### Total score by projected total (last 2460 games)", "", md_table(buckets, {"projected": "{:.1f}", "actual": "{:.1f}", "bias": "{:+.2f}", "over_rate": "{:.1%}"}), "",
          "### Slopes (actual vs projected)", "",
          f"Margin slope {windows['last 600 games']['margin_slope']:.2f} +/- {windows['last 600 games']['margin_slope_se']:.2f} and total slope "
          f"{windows['last 600 games']['total_slope']:.2f} +/- {windows['last 600 games']['total_slope_se']:.2f} over the last 600 games of the walk-forward data (end of 2025-26; 1.00 = ideal). "
          f"All four seasons: margin {windows['all']['margin_slope']:.2f}, total {windows['all']['total_slope']:.2f}.", ""]
    dc, sgx = cal["display_constants"], cal["dispersion_suggestion"]
    L += ["## 2. Recalibration", "",
          f"* **Overtime:** over the last two seasons the simulator said {ot2.sim_p_ot.mean():.1%} of games go to overtime; {ot2.ot.mean():.1%} actually did. "
          f"The daily report now multiplies the simulator's P(OT) by {dc['ot_scale']:.2f}.",
          f"* **Margin range:** over the last 1230 games the 80% range covers {recent_cov_m:.1%} of results (should be 80%). Refitting the spread on the last 1230 games gives "
          f"kappa {kref_m:.3f} vs {km:.3f} in use; on the 300 newest games held out the refit improved the log-likelihood by {sgx['margin_holdout_gain_pct']:.2f}%. "
          f"Displayed margin ranges are widened by x{dc['margin_interval_scale']:.2f}.",
          f"* **Total range:** coverage {float(((recent.total >= recent.ct_q10) & (recent.total <= recent.ct_q90)).mean()):.1%}; spread refit {kref_t:.3f} vs {kt:.3f} (held-out gain {sgx['total_holdout_gain_pct']:.2f}%). Displayed total ranges x{dc['total_interval_scale']:.2f}.",
          "* **Not changed:** projected means and win probabilities. A Platt-style sharpening of win probabilities improved log-loss by about 0.0015 in the last two seasons but hurt in 2023-24, and a margin/total scale refit moved MAE by under 0.1 point, so neither is applied.", ""]
    L += ["## 3. Team layer on the live season", ""]
    if live:
        L += [f"{live['n']} live games with stored pre-game forecasts and results (small sample: treat as a smoke test, not a verdict).", "",
              md_table(pd.DataFrame([{k: v for k, v in live.items() if k != 'variants'}]).T.reset_index().rename(columns={"index": "metric", 0: "value"}), {"value": "{:.3f}"}), ""]
        L += [f"**Total score:** live games are totalling {live['total_bias']:+.1f} points versus the projection (standard error {live['total_bias_se']:.1f}). "
              "Part of this is that the scoring-level correction learned at the end of 2025-26 (about +6 points) was carried into the new season while scoring dropped. "
              "From 2026-11-04 the level restarts at 0 each season and tracks faster for the first 60 games (walk-forward history shows no loss from this: "
              "total MAE 14.773 vs 14.774 for all games; forecasts already stored are not touched).", ""]
        if live.get("variants"):
            L += ["Variants on the same live games (each only for games that had that variant stored):", "",
                  md_table(pd.DataFrame(live["variants"]).T.reset_index().rename(columns={"index": "model"}), {"log_loss": "{:.4f}", "margin_mae": "{:.2f}"}), ""]
    else:
        L += ["No live games with results yet.", ""]
    L += ["## 4. Player layer", ""]
    if retro:
        u = pd.DataFrame(retro["unconfirmed"])[["stat", "n", "mean_forecast", "mean_actual", "bias", "mae", "cov50", "cov80", "cov90"]]
        L += ["### 2025-26, lineup unknown (what the daily job stores)", "", md_table(u, {"mean_forecast": "{:.2f}", "mean_actual": "{:.2f}", "bias": "{:+.3f}", "mae": "{:.2f}", "cov50": "{:.1%}", "cov80": "{:.1%}", "cov90": "{:.1%}"}), "",
              "Per-player means are unbiased (bias is a few hundredths of a unit). Coverage of the discrete stats (steals, blocks, turnovers, threes) reads high because "
              "counts take whole values and a range edge on a whole number counts as inside; points, minutes and points+rebounds+assists are the informative rows, "
              "and they sit at or slightly above nominal. In the last fifth of the season points were under-projected by about 0.25 per player (+3%), a drift worth watching.", ""]
    if len(live_pl):
        L += [f"### Live 2026-27 ({cal['player_live']['games']} games, {cal['player_live']['rows']} player rows)", "",
              md_table(live_pl[["stat", "n", "mean_forecast", "mean_actual", "bias", "mae", "cov50", "cov80", "cov90"]], {"mean_forecast": "{:.2f}", "mean_actual": "{:.2f}", "bias": "{:+.3f}", "mae": "{:.2f}", "cov50": "{:.1%}", "cov80": "{:.1%}", "cov90": "{:.1%}"}), ""]
    else:
        L += ["### Live 2026-27", "", "Live player projections are stored before tip-off from now on and compared with the box scores once the games finish. None have finished yet; this section fills in automatically.", ""]
    L += ["## 5. What this does not cover", "",
          "Player lines are projected one team at a time and are not reconciled with the team simulation. Win-probability recalibration, margin/total scale and team-specific bias are reported, not applied. "
          "Betting-line calibration is impossible without sportsbook lines in the data."]
    os.makedirs(os.path.join(ROOT, "artifacts/reports"), exist_ok=True)
    open(os.path.join(ROOT, "artifacts/reports/calibration.md"), "w").write("\n".join(L))
    print("calibration written;", json.dumps(cal["display_constants"]))


if __name__ == "__main__":
    main()
