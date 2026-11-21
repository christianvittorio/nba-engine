"""Leakage-audited forecast grading, matched-model comparisons and optional odds.

No profit assumption. Odds must be observed and *retrieved* before the
prediction cutoff. Public line archives fetched later are excluded from
historical actionable-edge claims, even if the provider quotes an old time.
"""
from __future__ import annotations
from collections import defaultdict
from math import log,sqrt
from typing import Any
import numpy as np

from .contracts import utc

def _actual_win(r:dict)->int:
    if r["home_score"]==r["away_score"]:
        raise ValueError("Final NBA games cannot tie")
    return int(r["home_score"]>r["away_score"])

def verify_pregame(pred:dict,game:dict)->None:
    for key in ("cutoff_utc","created_at_utc","model_version","game_id"):
        if not pred.get(key):
            raise ValueError(f"Missing immutable forecast field: {key}")
    if pred["game_id"]!=game["game_id"]:
        raise ValueError("Game ID mismatch")
    if not game.get("tip_utc"):
        raise ValueError("Missing historical source UTC tipoff")
    tip=utc(game["tip_utc"])
    if utc(pred["cutoff_utc"])>=tip or utc(pred["created_at_utc"])>=tip:
        raise ValueError("Post-tip prediction masquerading as pregame")
    if utc(pred["created_at_utc"])<utc(pred["cutoff_utc"]):
        raise ValueError("Prediction predates input cutoff")
    if pred.get("source_max_timestamp_utc") and \
       utc(pred["source_max_timestamp_utc"])>utc(pred["cutoff_utc"]):
        raise ValueError("Feature source leaked beyond prediction cutoff")

def evaluate(predictions:list[dict],games:dict[str,dict],actuals:dict[str,dict],
             *,reject_invalid=True)->dict:
    metrics=[]
    for pred in predictions:
        game=games.get(pred.get("game_id"))
        actual=actuals.get(pred.get("game_id"))
        if game is None or actual is None:
            continue
        try:
            verify_pregame(pred,game)
        except ValueError:
            if reject_invalid: raise
            continue
        p=float(pred["home_win_probability"])
        if not .00001<=p<=.99999:
            raise ValueError("Invalid/overconfident p_home")
        y=_actual_win(actual)
        h=float(pred["expected_home_score"])
        a=float(pred["expected_away_score"])
        sh=int(actual["home_score"]);sa=int(actual["away_score"])
        line={
            "game_id":pred["game_id"],
            "brier":(p-y)**2,
            "log_loss":-y*log(p)-(1-y)*log(1-p),
            "correct":float((p>=.5)==bool(y)),
            "home_mae":abs(h-sh),
            "away_mae":abs(a-sa),
            "margin_mae":abs((h-a)-(sh-sa)),
            "total_mae":abs((h+a)-(sh+sa)),
            "lead_hours":(utc(game["tip_utc"])-utc(pred["created_at_utc"])).total_seconds()/3600,
        }
        for label,span in (("80",.8),("90",.9)):
            if pred.get("margin_intervals",{}).get(label):
                low,hi=pred["margin_intervals"][label]
                line["margin_coverage_"+label]=float(low<=sh-sa<=hi)
        metrics.append(line)
    if not metrics: return {"n":0,"warning":"No verified pre-tip forecasts with results"}
    names=[k for k in metrics[0] if k!="game_id"]
    return {
        "n":len(metrics),
        **{k:round(float(np.mean([r[k] for r in metrics if k in r])),5)
           for k in names if all(k in r for r in metrics)},
        "game_ids":[r["game_id"] for r in metrics],
    }

def paired_compare(pred_a:list[dict],pred_b:list[dict],
                   games:dict[str,dict],actuals:dict[str,dict])->dict:
    a={p["game_id"]:p for p in pred_a}
    b={p["game_id"]:p for p in pred_b}
    matched=sorted(set(a)&set(b)&set(games)&set(actuals))
    return {
        "matched_games":len(matched),
        "a":evaluate([a[g] for g in matched],games,actuals),
        "b":evaluate([b[g] for g in matched],games,actuals),
        "warning":"Use same forecast lead-time windows and source-as-of policies",
    }

def odds_edge(pred:dict,market:dict,game:dict,selection:str)->dict:
    """A descriptive edge computation. No strategy or profit guarantee."""
    verify_pregame(pred,game)
    if selection not in ("home","away"):
        raise ValueError("Only two-way moneyline selection supported")
    if not market.get("observed_at_utc") or not market.get("retrieved_at_utc"):
        raise ValueError("Odds snapshot must contain actual observation/retrieval times")
    if utc(market["observed_at_utc"])>utc(pred["cutoff_utc"]) or \
       utc(market["retrieved_at_utc"])>utc(pred["cutoff_utc"]):
        raise ValueError("Odds were not available at the prediction cutoff")
    if market["game_id"]!=pred["game_id"]:
        raise ValueError("Market belongs to wrong game")
    decimal=float(market["decimal_odds"])
    if decimal<=1 or not np.isfinite(decimal):
        raise ValueError("Invalid odds")
    p=float(pred["home_win_probability"])
    if selection=="away":p=1-p
    ev=p*(decimal-1)-(1-p)
    return {
        "selection":selection,
        "decimal_odds":decimal,
        "model_probability":round(p,5),
        "book_implied_probability_raw":round(1/decimal,5),
        "expected_net_return_per_unit":round(ev,5),
        "estimated_positive_edge":ev>0,
        "warning":"Model probability may be biased. A positive estimated EV is not proof of profitability.",
    }

def calibration_bins(pred:list[dict],actuals:dict[str,dict],bins=10)->list[dict]:
    grouped=defaultdict(list)
    for p in pred:
        if p["game_id"] not in actuals:
            continue
        prob=float(p["home_win_probability"])
        if not 0<prob<1:continue
        idx=min(bins-1,int(prob*bins))
        grouped[idx].append((prob,_actual_win(actuals[p["game_id"]])))
    return [{
        "interval":[round(i/bins,3),round((i+1)/bins,3)],
        "n":len(grouped[i]),
        "avg_p":round(float(np.mean([x[0] for x in grouped[i]])),4),
        "observed_win_rate":round(float(np.mean([x[1] for x in grouped[i]])),4)
    } for i in range(bins) if grouped[i]]
