"""Daily sportsbook parlay RESEARCH ranking from exact as-of market comparisons.

This estimates an independent-game payoff, NOT a profitable bet.
The live model is uncalibrated, and paper ranks are never actionable.
A single ticket must be placeable at ONE named sportsbook at one observation
window; never multiply unrelated shops' best prices or same-game events.
No raw sportsbook data is published by this module.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
import json
from math import isfinite, prod
from pathlib import Path
from zoneinfo import ZoneInfo

from .contracts import iso, utc

VERSION = "gpt-v2-parlay-research-0.1"
EASTERN = ZoneInfo("America/New_York")
_ALLOWED_MARKETS = frozenset({"moneyline", "spread", "total"})
_ALLOWED_DECISIONS = frozenset({"RESEARCH_ONLY", "REVIEW_POSITIVE_EV"})


def _valid_leg(row: dict, *, now: datetime, date_eastern: str | None,
               max_quote_age_minutes: float, minimum_leg_roi: float,
               max_decimal_odds: float) -> dict | None:
    """Reject missing odds, unsupported markets, invalid/stale time or model."""
    if not isinstance(row, dict):
        return None
    if row.get("decision") not in _ALLOWED_DECISIONS:
        return None
    if row.get("market_type") not in _ALLOWED_MARKETS:
        return None
    for name in ("game_id", "market_id", "book", "selection", "tip_utc",
                 "retrieved_at_utc", "observed_at_utc", "forecast_cutoff_utc"):
        if not str(row.get(name) or "").strip():
            return None
    try:
        tip, captured, observed, cutoff = (
            utc(row["tip_utc"]), utc(row["retrieved_at_utc"]),
            utc(row["observed_at_utc"]), utc(row["forecast_cutoff_utc"])
        )
        if (tip <= now or captured > now or observed > captured or
                captured > cutoff or cutoff >= tip):
            return None
        if (now-captured).total_seconds() > max_quote_age_minutes * 60:
            return None
        if date_eastern is not None and tip.astimezone(EASTERN).date().isoformat() != date_eastern:
            return None
        # Original report's 30-minute price-vs-model freshness gate.
        gap = float(row["snapshot_gap_minutes"])
        if not isfinite(gap) or gap > 30 or gap < 0:
            return None
        # Require both sides of the bookmaker market; a lone quote may be
        # promotional, stale, misreported or missing overround evidence.
        if row.get("no_vig_market_probability") is None:
            return None
        odds, p = float(row["decimal_odds"]), float(row["model_probability"])
        push = float(row.get("push_probability") or 0)
        if not all(map(isfinite, (odds, p, push))):
            return None
        if not 1 < odds <= max_decimal_odds or not 0 <= p <= 1:
            return None
        if not 0 <= push <= 1-p:
            return None
        one_leg_roi = p * odds + push - 1
        if one_leg_roi < minimum_leg_roi:
            return None
    except (ValueError, TypeError, OverflowError, KeyError):
        return None
    lower = row.get("model_probability_lower")
    if lower is not None:
        try:
            lower = float(lower)
            if not isfinite(lower) or not 0 <= lower <= p:
                return None
        except (TypeError, ValueError, OverflowError):
            return None
    # Exclude rows claiming forward validation without auditable uncertainty.
    calibrated = (row.get("calibration_status") == "forward_validated"
                  and row["decision"] == "REVIEW_POSITIVE_EV"
                  and lower is not None)
    return {
        "game_id": str(row["game_id"]), "market_id": str(row["market_id"]),
        "market_type": row["market_type"], "selection": row["selection"],
        "line": row.get("line"), "book": str(row["book"]),
        "decimal_odds": odds, "model_probability": p,
        "push_probability": push, "model_probability_lower": lower,
        "retrieved_at_utc": iso(captured), "tip_utc": iso(tip),
        "individual_research_roi": one_leg_roi,
        "forward_validated": calibrated,
    }


def build_parlay_board(report: dict, *, date_eastern: str | None = None,
                       now_utc: str | None = None, min_legs: int = 2,
                       max_legs: int = 3, max_quote_age_minutes: float = 30,
                       max_capture_span_minutes: float = 10,
                       minimum_leg_roi: float = 0.01,
                       minimum_joint_win_probability: float = 0.10,
                       max_decimal_odds: float = 5,
                       maximum_results: int = 5) -> dict:
    """Find top raw expected-ROI tickets within limited, verifiable scope.

    A ticket is NOT a recommendation. Independence across DIFFERENT NBA
    games is an assumption, not a measured joint distribution. Push returns
    the leg stake (multiplier 1) rather than an automatic loss.
    """
    if not isinstance(report, dict) or report.get("research_only") is not True:
        raise ValueError("As-of research report required")
    if min_legs < 2 or max_legs < min_legs or max_legs > 4:
        raise ValueError("Require two to four legs")
    if maximum_results < 1 or maximum_results > 20:
        raise ValueError("Invalid result count")
    if date_eastern is not None:
        datetime.strptime(date_eastern, "%Y-%m-%d")
    if any(not isfinite(float(x)) or float(x) < 0 for x in
           (max_quote_age_minutes, max_capture_span_minutes,
            minimum_leg_roi, minimum_joint_win_probability)):
        raise ValueError("Invalid finite nonnegative threshold")
    if not 0 <= minimum_joint_win_probability <= 1 or not 1 < max_decimal_odds <= 100:
        raise ValueError("Invalid parlay constraints")
    now = utc(now_utc) if now_utc else datetime.now(timezone.utc)
    candidates = []
    for row in report.get("markets", []):
        parsed = _valid_leg(
            row, now=now, date_eastern=date_eastern,
            max_quote_age_minutes=max_quote_age_minutes,
            minimum_leg_roi=minimum_leg_roi,
            max_decimal_odds=max_decimal_odds,
        )
        if parsed is not None:
            candidates.append(parsed)
    by_book = defaultdict(list)
    for leg in candidates:
        by_book[leg["book"]].append(leg)
    eligible, considered = [], 0
    for book, pool in sorted(by_book.items()):
        for size in range(min_legs, min(max_legs, len(pool))+1):
            for combo in combinations(pool, size):
                # A true parlay at one sportsbook may not include two
                # selections from the same game. No guessed SGP correlations.
                if len({leg["game_id"] for leg in combo}) != size:
                    continue
                captured = [utc(leg["retrieved_at_utc"]) for leg in combo]
                span = (max(captured)-min(captured)).total_seconds() / 60
                if span > max_capture_span_minutes:
                    continue
                joint_win = prod(x["model_probability"] for x in combo)
                if joint_win < minimum_joint_win_probability:
                    continue
                considered += 1
                all_win_odds = prod(x["decimal_odds"] for x in combo)
                # For independent events E[return] multiplies leg payouts;
                # push is refund at multiplier 1, NOT a losing ticket.
                ev = prod(
                    x["model_probability"] * x["decimal_odds"] +
                    x["push_probability"] for x in combo
                ) - 1
                all_validated = all(x["forward_validated"] for x in combo)
                conservative_ev = (
                    prod(x["model_probability_lower"] * x["decimal_odds"]
                         for x in combo) - 1 if all_validated else None
                )
                eligible.append({
                    "book": book, "leg_count": size,
                    "legs": list(combo),
                    "full_win_decimal_odds": all_win_odds,
                    "full_win_probability_independent": joint_win,
                    "no_loss_probability_independent": prod(
                        x["model_probability"] + x["push_probability"]
                        for x in combo
                    ),
                    "estimated_roi_independent": ev,
                    "conservative_roi_lower_bound": conservative_ev,
                    "retrieval_span_minutes": round(span, 3),
                    "validation_status": (
                        "FORWARD_VALIDATED_REVIEW_ONLY"
                        if all_validated and conservative_ev is not None
                        and conservative_ev > 0
                        else "UNCALIBRATED_RESEARCH_ONLY"
                    ),
                    "actionable": False,
                })
    eligible.sort(key=lambda x: (
        -x["estimated_roi_independent"],
        -x["full_win_probability_independent"],
        x["leg_count"], x["book"],
        tuple((p["game_id"],p["market_id"],p["selection"]) for p in x["legs"])
    ))
    best = eligible[:maximum_results]
    return {
        "version": VERSION, "research_only": True, "actionable": False,
        "generated_at_utc": iso(now),
        "date_eastern": date_eastern,
        "eligible_single_legs": len(candidates),
        "candidate_tickets_screened": considered,
        "ranking_metric": "estimated_roi_independent",
        "filters": {
            "minimum_leg_roi": minimum_leg_roi,
            "minimum_joint_win_probability": minimum_joint_win_probability,
            "min_legs": min_legs, "max_legs": max_legs,
            "max_quote_age_minutes": max_quote_age_minutes,
            "max_capture_span_minutes": max_capture_span_minutes,
            "max_decimal_odds": max_decimal_odds,
            "same_book_only": True, "max_one_leg_per_game": True,
        },
        "best_research_combination": best[0] if best else None,
        "ranked_research_combinations": best,
        "best_forward_validated_review": next(
            (x for x in eligible if
             x["validation_status"] == "FORWARD_VALIDATED_REVIEW_ONLY"), None
        ),
        "betting_recommendation": None,
        "status": ("RESEARCH_RANKING_AVAILABLE" if best
                   else "NO_QUALIFYING_PARLAY"),
        "limitations": [
            "Ranking maximizes model-estimated ROI, not observed betting profit.",
            "Live possession model is uncalibrated. A research leader is NOT a pick.",
            "Inter-game independence is assumed; common news/pace can correlate outcomes.",
            "Full-win odds assume every leg wins; push refunds reduce settlement payout.",
            "Only one bookmaker's actual observed pretip prices per ticket.",
            "Only markets with complete sourced two-sided prices and forecasts qualify.",
            "Captured prices can change and may not be executable at ranking time.",
            "No auto wagering, staking instructions, or guarantee of profitability.",
        ],
    }


def render_markdown(board: dict) -> str:
    out = ["# NBA Engine — Parlay of the Day (RESEARCH ONLY)", "",
           "**Not a betting recommendation. Live model is not calibrated.**", "",
           "Status: **" + board["status"] + "**", "",
           f"Eligible priced legs: {board['eligible_single_legs']}; "
           f"screened qualifying combinations: {board['candidate_tickets_screened']}.",
           ""]
    first = board["best_research_combination"]
    if first is None:
        out.append("**NO PARLAY** — no simultaneously observed, sufficiently "
                   "fresh, individually positive-EV legs meet the filters.")
    else:
        out.extend([
            f"## Highest model-estimated ROI — {first['book']}, "
            f"{first['leg_count']} legs",
            "", "| Game | Market | Side | Line | Model P | Quoted odds |",
            "|---|---|---|---:|---:|---:|",
        ])
        for leg in first["legs"]:
            line = "—" if leg["line"] is None else f"{leg['line']:+g}"
            out.append(f"| {leg['game_id']} | {leg['market_type']} | "
                       f"{leg['selection']} | {line} | "
                       f"{leg['model_probability']:.1%} | "
                       f"{leg['decimal_odds']:.2f} |")
        out.extend(["",
            f"Combined decimal price (all win): **{first['full_win_decimal_odds']:.2f}**.",
            f"Estimated all-win probability (independence): "
            f"**{first['full_win_probability_independent']:.1%}**.",
            f"Raw model-estimated ROI (pushes accounted for): "
            f"**{first['estimated_roi_independent']:+.1%}**.",
            f"Validation: **{first['validation_status']}**.",
            "", "This number is NOT a calibrated edge or expected real-world return.",
        ])
    out.extend(["", "## Method and exclusions", ""])
    out.extend("- " + item for item in board["limitations"])
    out.append("")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--asof-report", required=True, type=Path)
    ap.add_argument("--date", default=None, help="US Eastern slate YYYY-MM-DD")
    ap.add_argument("--output-json", required=True, type=Path)
    ap.add_argument("--output-md", required=True, type=Path)
    ap.add_argument("--max-legs", type=int, default=3)
    args = ap.parse_args(argv)
    report = json.loads(args.asof_report.read_text(encoding="utf-8"))
    board = build_parlay_board(report, date_eastern=args.date,
                               max_legs=args.max_legs)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(board, indent=2, allow_nan=False)+"\n", encoding="utf-8"
    )
    args.output_md.write_text(render_markdown(board), encoding="utf-8")
    # No raw bookmaker quotes or user wagers written to public logs.
    print(json.dumps({
        "parlay_research": True, "status": board["status"],
        "eligible_single_legs": board["eligible_single_legs"],
        "screened_tickets": board["candidate_tickets_screened"],
        "has_validation_backed_review": (
            board["best_forward_validated_review"] is not None
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
