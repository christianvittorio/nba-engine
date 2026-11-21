"""Point-in-time sportsbook EV comparison for NBA GPT v2 (research only).

This module does not scrape odds, claim model calibration, or place bets.
It accepts independent, explicitly time-stamped bookmaker snapshots and
line-specific probabilities. Both must be pre-tip, and comparisons that are
not near-contemporaneous are marked ineligible.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from math import isfinite
from pathlib import Path

from .contracts import iso, utc

VERSION = "gpt-v2-market-value-research-0.1"
TYPES = frozenset({"moneyline", "spread", "total", "player_prop"})
STATUSES = frozenset({"uncalibrated", "research_calibrated", "forward_validated"})


def _number(value, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number")
    try:
        number = float(value)
    except (TypeError, ValueError) as ex:
        raise ValueError(f"{name} must be a finite number") from ex
    if not isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _identity(row: dict) -> tuple:
    """Exact selection/line identity, never match a nearby but different line."""
    return (
        str(row["game_id"]), str(row["market_id"]),
        str(row["selection"]), row.get("line"), row.get("player_id")
    )


def _validate_common(row: dict) -> dict:
    required = ("game_id", "market_id", "market_type", "selection",
                "tip_utc")
    for field in required:
        if not str(row.get(field, "")).strip():
            raise ValueError(f"Missing required {field}")
    value = dict(row)
    if value["market_type"] not in TYPES:
        raise ValueError("Unsupported market_type")
    value["tip_utc"] = iso(value["tip_utc"])
    if value.get("line") is not None:
        value["line"] = _number(value["line"], "line")
    if value["market_type"] == "moneyline" and value.get("line") is not None:
        raise ValueError("Moneyline must not specify a point line")
    if value["market_type"] != "moneyline" and value.get("line") is None:
        raise ValueError("Line-specific markets require an exact line")
    if value["market_type"] == "player_prop" and not value.get("player_id"):
        raise ValueError("Player props require a stable player_id")
    return value


def _validate_quote(row: dict) -> dict:
    quote = _validate_common(row)
    if not str(quote.get("book", "")).strip():
        raise ValueError("Quote missing sportsbook name")
    quote["observed_at_utc"] = iso(quote["observed_at_utc"])
    quote["decimal_odds"] = _number(quote["decimal_odds"], "decimal_odds")
    if quote["decimal_odds"] <= 1.0:
        raise ValueError("Decimal odds must exceed 1.0")
    if utc(quote["observed_at_utc"]) >= utc(quote["tip_utc"]):
        raise ValueError("After-tip odds are not valid pregame evidence")
    return quote


def _validate_prediction(row: dict) -> dict:
    pred = _validate_common(row)
    pred["asof_utc"] = iso(pred["asof_utc"])
    if utc(pred["asof_utc"]) >= utc(pred["tip_utc"]):
        raise ValueError("After-tip model predictions cannot be evaluated")
    pred["probability"] = _number(pred["probability"], "probability")
    if not 0 <= pred["probability"] <= 1:
        raise ValueError("Probability outside [0,1]")
    lower = pred.get("probability_lower")
    if lower is not None:
        lower = _number(lower, "probability_lower")
        if not 0 <= lower <= pred["probability"]:
            raise ValueError("Lower probability bound invalid")
    pred["probability_lower"] = lower
    push = _number(pred.get("push_probability", 0), "push_probability")
    if not 0 <= push <= 1 - pred["probability"]:
        raise ValueError("Win and push probabilities must sum to at most 1")
    pred["push_probability"] = push
    status = pred.get("calibration_status", "uncalibrated")
    if status not in STATUSES:
        raise ValueError("Unknown calibration_status")
    pred["calibration_status"] = status
    if not str(pred.get("model_version", "")).strip():
        raise ValueError("Model version required")
    if status == "forward_validated" and not str(
        pred.get("validation_reference", "")
    ).strip():
        raise ValueError("Forward validation requires a documented reference")
    return pred


def _same_market_lines(a: dict, b: dict) -> bool:
    """Prevent false no-vig pairs across incompatible spread/total lines."""
    if a["market_type"] != b["market_type"]:
        return False
    kind = a["market_type"]
    if kind == "moneyline":
        return (a.get("line") is None and b.get("line") is None
                and {a["selection"], b["selection"]} == {"home", "away"})
    if kind == "spread":
        return (
            {a["selection"], b["selection"]} == {"home", "away"}
            and abs(a["line"] + b["line"]) < 1e-8
        )
    return (
        {a["selection"], b["selection"]} == {"over", "under"}
        and a["line"] == b["line"]
        and a.get("player_id") == b.get("player_id")
    )


def _no_vig_pairs(quotes: list[dict]) -> dict[int, dict]:
    """Two-sided proportional normalization; not a forecast of true chances."""
    by_market = defaultdict(list)
    for index, q in enumerate(quotes):
        key = (q["game_id"], q["market_id"], q["book"],
               q["observed_at_utc"], q["market_type"])
        by_market[key].append((index, q))
    results = {}
    for group in by_market.values():
        if len(group) != 2:
            continue
        (ia, a), (ib, b) = group
        if not _same_market_lines(a, b):
            continue
        pa = 1 / a["decimal_odds"]
        pb = 1 / b["decimal_odds"]
        overround = pa + pb - 1
        results[ia] = {"no_vig_market_probability": pa / (pa+pb),
                       "book_overround": overround}
        results[ib] = {"no_vig_market_probability": pb / (pa+pb),
                       "book_overround": overround}
    return results


def compare_markets(
    quotes: list[dict], predictions: list[dict],
    *, max_snapshot_gap_minutes: float = 30.0,
    minimum_lower_ev: float = 0.02
) -> dict:
    """Compare exact outcome/line matches; never fabricate unseen markets.

    Forward-validation status is caller evidence, not asserted or obtained
    by this module. 'REVIEW_POSITIVE_EV' never means an approved bet.
    """
    gap_limit = _number(max_snapshot_gap_minutes, "max_snapshot_gap_minutes")
    min_ev = _number(minimum_lower_ev, "minimum_lower_ev")
    if gap_limit < 0 or min_ev < 0:
        raise ValueError("Thresholds must be nonnegative")
    qq = [_validate_quote(q) for q in quotes]
    pp = [_validate_prediction(p) for p in predictions]
    by_id = {}
    for p in pp:
        key = _identity(p)
        if key in by_id:
            raise ValueError(f"Duplicate model probability for {key}")
        by_id[key] = p
    matched = _no_vig_pairs(qq)
    rows = []
    for i, q in enumerate(qq):
        price = q["decimal_odds"]
        implied = 1 / price
        p = by_id.get(_identity(q))
        record = {
            "game_id": q["game_id"], "market_id": q["market_id"],
            "market_type": q["market_type"], "selection": q["selection"],
            "line": q.get("line"), "player_id": q.get("player_id"),
            "book": q["book"], "decimal_odds": price,
            "observed_at_utc": q["observed_at_utc"],
            "tip_utc": q["tip_utc"], "break_even_probability": implied,
            "no_vig_market_probability": None, "book_overround": None,
            "model_probability": None, "model_probability_lower": None,
            "model_vs_no_vig_probability_gap": None,
            "expected_roi": None, "conservative_expected_roi": None,
            "push_probability": None, "unconditional_win_break_even": None,
            "decision": "NO_MODEL_PROBABILITY",
            "warnings": [],
        }
        record.update(matched.get(i, {}))
        if p is None:
            rows.append(record)
            continue
        if p["tip_utc"] != q["tip_utc"] or p["market_type"] != q["market_type"]:
            record["decision"] = "INVALID_COMPARISON"
            record["warnings"].append("Model and quote market/tip identity mismatch")
            rows.append(record)
            continue
        age = abs((utc(q["observed_at_utc"]) - utc(p["asof_utc"])).total_seconds()) / 60
        prob = p["probability"]
        lower = p["probability_lower"]
        push = p["push_probability"]
        # Whole-number lines can push (stake refunded); the standard
        # p*odds - 1 formula is only valid when push probability is zero.
        if (p["market_type"] != "moneyline"
                and float(p["line"]).is_integer()
                and "push_probability" not in next(
                    item for item in predictions if _identity(_validate_common(item)) == _identity(p)
                )):
            record["warnings"].append(
                "Whole-number line: explicit push probability unavailable"
            )
        record.update({
            "model_probability": prob, "model_probability_lower": lower,
            "model_asof_utc": p["asof_utc"],
            "model_version": p["model_version"],
            "calibration_status": p["calibration_status"],
            "snapshot_gap_minutes": round(age, 3),
            "push_probability": push,
            "unconditional_win_break_even": (1-push)/price,
            "expected_roi": prob*price + push - 1,
            # Bound is conservative: it does not credit uncertain pushes.
            "conservative_expected_roi": (
                lower*price - 1 if lower is not None else None
            ),
        })
        if record["no_vig_market_probability"] is not None:
            record["model_vs_no_vig_probability_gap"] = (
                prob - record["no_vig_market_probability"]
            )
        missing_push = any("explicit push probability unavailable" in w
                           for w in record["warnings"])
        if age > gap_limit:
            record["decision"] = "STALE_COMPARISON"
            record["warnings"].append("Market and model snapshots too far apart")
        elif missing_push:
            record["decision"] = "MISSING_PUSH_PROBABILITY"
        elif p["calibration_status"] != "forward_validated":
            record["decision"] = "RESEARCH_ONLY"
            record["warnings"].append(
                "Not forward validated; positive EV is a research estimate"
            )
        elif lower is None:
            record["decision"] = "INSUFFICIENT_UNCERTAINTY"
            record["warnings"].append("Conservative probability bound missing")
        elif lower*price-1 >= min_ev:
            record["decision"] = "REVIEW_POSITIVE_EV"
            record["warnings"].append(
                "Candidate needs independent source, lineup and market review"
            )
        else:
            record["decision"] = "NO_ROBUST_EDGE"
        if utc(q["observed_at_utc"]) > utc(p["asof_utc"]):
            record["warnings"].append(
                "Quote observed after model snapshot: news/lineup drift unverified"
            )
        rows.append(record)
    return {
        "version": VERSION,
        "generated_utc": iso(datetime.now(timezone.utc)),
        "research_only": True,
        "price_snapshot_count": len(qq),
        "model_prediction_count": len(pp),
        "markets": sorted(rows, key=lambda r: (
            r["expected_roi"] is None,
            -(r["expected_roi"] if r["expected_roi"] is not None else 0),
            r["game_id"], r["market_id"], r["book"]
        )),
        "limitations": [
            "No bookie API or automatically verified odds feed is connected.",
            "Expected ROI is conditional on model probability accuracy.",
            "No-vig market probabilities use proportional two-way normalization.",
            "No calibrated live possession Monte Carlo exists yet.",
            "Forward validation status must be independently evidenced.",
            "No betting execution, staking policy or guaranteed profitability.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--quotes", required=True)
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-snapshot-gap-minutes", type=float, default=30)
    args = parser.parse_args(argv)
    quotes = json.loads(Path(args.quotes).read_text(encoding="utf-8"))["quotes"]
    predictions = json.loads(
        Path(args.predictions).read_text(encoding="utf-8")
    )["predictions"]
    report = compare_markets(
        quotes, predictions,
        max_snapshot_gap_minutes=args.max_snapshot_gap_minutes
    )
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n",
                    encoding="utf-8")
    print(f"MARKET_VALUE_RESEARCH {path}: {len(report['markets'])} quotes")


if __name__ == "__main__":
    main()
