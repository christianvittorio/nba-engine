"""Time-split forward probability-calibration experiment on immutable forecasts.

Never retroactively label an experimental or retrospectively fitted model
as forward validated. Fitting and holdout use strictly disjoint UTC cutoffs.
Output is always a research calibrator, NOT approved for market decisions.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np

from .contracts import iso, utc
from .calibration import (
    PlattCalibrator, brier, log_loss, paired_bootstrap_loss_delta
)
from .market_grade import _finals_index
from .market_run import read_frozen_forecasts

VERSION = "gpt-v2-forward-calibration-research-0.1"


def observations_from_frozen(forecasts: list[dict], finals: dict) -> list[dict]:
    source = _finals_index(finals)
    rows = []
    seen = set()
    for d in forecasts:
        gid = d["game_id"]
        if gid in seen:
            raise ValueError("Duplicate game in frozen forecast set")
        seen.add(gid)
        game = source.get(gid)
        if game is None:
            continue
        forecast_asof = iso(d["cutoff_utc"])
        tip = iso(d["tip_utc"])
        if tip != iso(game["tip_utc"]):
            raise ValueError("Final and pretip game identity mismatch")
        if utc(forecast_asof) >= utc(tip):
            raise ValueError("Forecast cutoff is not before tip")
        if utc(game["final_at_utc"]) <= utc(forecast_asof):
            raise ValueError("Outcome available before the prediction")
        p = float(d["result"]["home_win_probability"])
        if not 0 <= p <= 1:
            raise ValueError("Invalid raw probability")
        rows.append({
            "game_id":gid, "prediction_id": d["prediction_id"],
            "model_version": d["model_version"],
            "cutoff_utc": forecast_asof, "tip_utc":tip,
            "outcome_retrieved_at_utc": iso(game["retrieved_at_utc"]),
            "probability": p,
            "home_won": int(game["home_score"]>game["away_score"]),
        })
    return sorted(rows,key=lambda r:(r["cutoff_utc"],r["game_id"]))


def evaluate_time_split(observations: list[dict], *,
                        calibration_before: str,
                        holdout_from: str,
                        holdout_before: str,
                        trained_at_utc: str | None = None) -> dict:
    before, start, end = (iso(calibration_before), iso(holdout_from),
                          iso(holdout_before))
    if not utc(before) <= utc(start) < utc(end):
        raise ValueError("Chronological calibration and holdout windows overlap")
    rows = sorted(observations,key=lambda x:(x["cutoff_utc"],x["game_id"]))
    if len({r["game_id"] for r in rows}) != len(rows):
        raise ValueError("Repeated game outcome in evaluation")
    versions = {r["model_version"] for r in rows}
    if len(versions) != 1:
        raise ValueError("Different model versions must be calibrated separately")
    if not rows:
        raise ValueError("No observed outcomes")
    cal = [r for r in rows if utc(r["cutoff_utc"]) < utc(before)]
    test = [r for r in rows if utc(start) <= utc(r["cutoff_utc"]) < utc(end)]
    if len(cal) < 80 or len({r["home_won"] for r in cal}) != 2:
        raise ValueError("At least 80 pre-holdout games with both outcomes required")
    if not test:
        raise ValueError("No frozen future-window games with independent outcomes")

    # Labels cannot be known until their genuinely timestamped final result
    # has been retrieved. Calibrator would have to be trained after ALL cal
    # outcomes existed; a holdout is prospective only if training preceded it.
    cal_ready = max(utc(r["outcome_retrieved_at_utc"]) for r in cal)
    first_test_cutoff = min(utc(r["cutoff_utc"]) for r in test)
    stamp = iso(trained_at_utc or datetime.now(timezone.utc))
    if utc(stamp) < cal_ready:
        raise ValueError("Calibrator creation time predates calibration outcomes")
    training_was_pretip_for_holdout = (
        utc(stamp) < first_test_cutoff and cal_ready < first_test_cutoff
    )
    cp = np.asarray([r["probability"] for r in cal],dtype=float)
    cy = np.asarray([r["home_won"] for r in cal],dtype=int)
    tp = np.asarray([r["probability"] for r in test],dtype=float)
    ty = np.asarray([r["home_won"] for r in test],dtype=int)

    model = PlattCalibrator(c=.4).fit(cp,cy)
    out = model.predict(tp)
    raw = {"brier": brier(tp,ty), "log_loss": log_loss(tp,ty)}
    calibrated = {"brier": brier(out,ty), "log_loss": log_loss(out,ty)}
    # A research result is NOT promoted merely because its in-sample metrics
    # are smaller, or because the chronological holdout was evaluated once.
    paired = paired_bootstrap_loss_delta(tp,out,ty,iterations=500) if len(test)>=30 else None
    buckets = []
    for low in np.arange(0,1,.1):
        mask = (out >= low) & ((out < low+.1) if low < .9 else (out <= 1))
        if mask.any():
            buckets.append({
                "forecast_range":[round(float(low),2),round(float(low+.1),2)],
                "n":int(mask.sum()),
                "mean_calibrated_p":float(np.mean(out[mask])),
                "observed_home_win_rate":float(np.mean(ty[mask]))
            })
    return {
        "version": VERSION,
        "model_version": next(iter(versions)),
        "calibration_before": before, "holdout_from":start,
        "holdout_before":end, "artifact_issued_at_utc":stamp,
        "calibration_games": len(cal), "holdout_games":len(test),
        "calibrator_parameters":model.parameters(),
        "raw_holdout":raw, "calibrated_holdout":calibrated,
        "paired_logloss_delta":paired,
        "reliability_buckets":buckets,
        "training_completed_before_holdout_predictions":training_was_pretip_for_holdout,
        "promotion_gate": {
            "automatic_promotion":False,
            "historical_research_only":True,
            "at_least_200_test_games":len(test)>=200,
            "prospectively_trained":training_was_pretip_for_holdout,
            "improved_holdout_brier":calibrated["brier"] < raw["brier"],
            "improved_holdout_logloss":calibrated["log_loss"] < raw["log_loss"],
            "approved_for_live_value_decisions":False,
        },
        "warning": (
            "Calibrator fit on frozen outcomes only; retrospective fitting "
            "against already-occurred test games is research, not forward "
            "validation. Requires future issued calibration and independent "
            "new test games before considering any live deployment."
        ),
    }


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--forecast-ledger",type=Path,required=True)
    ap.add_argument("--root",type=Path,default=Path("."))
    ap.add_argument("--finals-json",type=Path,required=True)
    ap.add_argument("--calibration-before",required=True)
    ap.add_argument("--holdout-from",required=True)
    ap.add_argument("--holdout-before",required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args(argv)
    docs=read_frozen_forecasts(args.forecast_ledger,args.root)
    finals=json.loads(args.finals_json.read_text(encoding="utf-8"))
    data=observations_from_frozen(docs,finals)
    result=evaluate_time_split(
        data,calibration_before=args.calibration_before,
        holdout_from=args.holdout_from,
        holdout_before=args.holdout_before)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",
                           encoding="utf-8")
    print(json.dumps({
        "calibration_games":result["calibration_games"],
        "test_games":result["holdout_games"],
        "promotion":result["promotion_gate"]
    }))


if __name__=="__main__":
    main()
