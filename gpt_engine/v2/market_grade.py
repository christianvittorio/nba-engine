"""Outcome grading, prospective reliability and same-book closing-line tracking.

Accepts frozen as-of reports, append-only sportsbook quotes and independently
sourced final scores. No game results are used to select or modify forecasts.
No wagering or inference of profit from small/noisy samples.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from math import log
from statistics import median
from pathlib import Path

from .contracts import iso, utc
from .market_run import read_jsonl
from .market_value import _validate_quote

VERSION = "gpt-v2-market-grading-0.1"
PLAYER_STAT_KEYS = frozenset({"pts", "reb", "ast", "fg3m"})


def _finals_index(source: dict) -> dict:
    result = {}
    for g in source.get("games", []):
        gid = str(g.get("game_id", ""))
        if not gid or gid in result:
            raise ValueError("Missing or duplicate final game ID")
        if g.get("status") != "final":
            continue
        for key in ("tip_utc", "final_at_utc", "source_id",
                    "retrieved_at_utc", "home_score", "away_score"):
            if g.get(key) is None or g.get(key) == "":
                raise ValueError(f"Final game {gid} missing {key}")
        if utc(g["final_at_utc"]) <= utc(g["tip_utc"]):
            raise ValueError("Final outcome timestamp at/before tip")
        if utc(g["retrieved_at_utc"]) < utc(g["final_at_utc"]):
            raise ValueError("Claimed final source retrieval predates final result")
        for k in ("home_score", "away_score"):
            value = g[k]
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 250:
                raise ValueError("Final score must be a nonnegative NBA integer")
        if g["home_score"] == g["away_score"]:
            raise ValueError("Final NBA games cannot end tied")
        result[gid] = g
    return result


def _grade_market(row: dict, game: dict) -> str:
    """WIN / LOSS / PUSH / VOID / MISSING_PLAYER_RESULT."""
    home = game["home_score"]
    away = game["away_score"]
    mtype = row["market_type"]
    selection = row["selection"]
    if mtype == "moneyline":
        if selection not in ("home", "away"):
            raise ValueError("Invalid moneyline selection")
        return "WIN" if (home > away) == (selection == "home") else "LOSS"
    if mtype == "spread":
        delta = (home-away) if selection == "home" else (away-home)
        adjusted = delta + float(row["line"])
    elif mtype == "total":
        if selection not in ("over", "under"):
            raise ValueError("Invalid total selection")
        delta = home+away - float(row["line"])
        adjusted = delta if selection == "over" else -delta
    elif mtype == "player_prop":
        if selection not in ("over", "under"):
            raise ValueError("Invalid player prop side")
        player = game.get("players", {}).get(row.get("player_id"))
        if player is None:
            return "MISSING_PLAYER_RESULT"
        if player.get("status") == "dnp":
            return "VOID"  # Game appearance must be verified, not inferred
        if player.get("status") != "played":
            return "MISSING_PLAYER_RESULT"
        # ID includes the market stat, no fragile split on player:nba:<id>
        parts = str(row["market_id"]).split(":")
        if len(parts) < 4 or parts[0] != "player":
            return "MISSING_PLAYER_RESULT"
        stat = parts[1]
        if stat not in PLAYER_STAT_KEYS or stat not in player:
            return "MISSING_PLAYER_RESULT"
        actual = float(player[stat])
        delta = actual - float(row["line"])
        adjusted = delta if selection == "over" else -delta
    else:
        raise ValueError("Unknown market type")
    if abs(adjusted) <= 1e-9:
        return "PUSH"
    return "WIN" if adjusted > 0 else "LOSS"


def _close_quote(asof_row: dict, odds_history: list[dict],
                 *, max_close_age_minutes: float = 60) -> dict | None:
    """Only exact same book, selection and LINE; never price a shifted line."""
    tip = utc(asof_row["tip_utc"])
    matches = []
    for q in odds_history:
        if (q["game_id"] != asof_row["game_id"]
                or q["book"] != asof_row["book"]
                or q["market_id"] != asof_row["market_id"]
                or q["selection"] != asof_row["selection"]
                or q.get("line") != asof_row.get("line")
                or q.get("player_id") != asof_row.get("player_id")):
            continue
        retrieved = q.get("retrieved_at_utc")
        if retrieved is None:
            continue
        # True pretip capture, not later backfilled quote observations.
        if not (utc(q["observed_at_utc"]) <= utc(retrieved) < tip):
            continue
        observed = utc(q["observed_at_utc"])
        if (tip-observed).total_seconds() > max_close_age_minutes*60:
            continue
        if utc(retrieved) < utc(asof_row["retrieved_at_utc"]):
            continue
        matches.append(q)
    return max(matches, key=lambda q: (
        utc(q["observed_at_utc"]), utc(q["retrieved_at_utc"])
    )) if matches else None


def _summary(rows: list[dict]) -> dict:
    complete = [r for r in rows if r["settlement"] in ("WIN", "LOSS", "PUSH", "VOID")]
    settled = [r for r in complete if r["settlement"] != "VOID"]
    clvs = [r["closing_line_value"] for r in rows if r["closing_line_value"] is not None]
    return {
        "observations": len(rows), "settled": len(settled),
        "win": sum(r["settlement"] == "WIN" for r in settled),
        "loss": sum(r["settlement"] == "LOSS" for r in settled),
        "push": sum(r["settlement"] == "PUSH" for r in settled),
        "void": sum(r["settlement"] == "VOID" for r in complete),
        "hypothetical_flat_unit_roi": (
            sum(r["unit_return"] for r in settled)/len(settled)
            if settled else None
        ),
        "paired_closing_line_count": len(clvs),
        "mean_same_line_same_book_clv": (
            sum(clvs)/len(clvs) if clvs else None
        ),
        "minimum_sample_met": len(settled) >= 100,
    }


def evaluate_outcomes(asof_report: dict, odds_history: list[dict],
                      finals: dict, *, reference_book: str = "") -> dict:
    """Unselected market audit plus fixed best-odds positive-raw-EV paper cohort."""
    scores = _finals_index(finals)
    q, invalid_closing_captures = [], []
    for raw in odds_history:
        retrieval = raw.get("retrieved_at_utc")
        if retrieval and utc(retrieval) >= utc(raw["tip_utc"]):
            # This is not a pre-tip closing price. Audit its exclusion,
            # rather than contaminating CLV with data fetched after start.
            invalid_closing_captures.append({
                "game_id": raw["game_id"], "book": raw["book"],
                "reason": "QUOTE_RETRIEVED_AT_OR_AFTER_TIP"
            })
            continue
        q.append(_validate_quote(raw))
    graded, skipped = [], []
    for row in asof_report.get("markets", []):
        game = scores.get(row["game_id"])
        if game is None:
            skipped.append({"game_id": row["game_id"],
                            "reason": "FINAL_NOT_PROVIDED"})
            continue
        if iso(game["tip_utc"]) != iso(row["tip_utc"]):
            raise ValueError("Final and frozen forecast tip mismatch")
        if utc(game["final_at_utc"]) <= utc(row["forecast_cutoff_utc"]):
            raise ValueError("Final event before model cutoff")
        outcome = _grade_market(row, game)
        odds = float(row["decimal_odds"])
        unit_return = (
            odds-1 if outcome == "WIN" else
            -1.0 if outcome == "LOSS" else
            0.0 if outcome in ("PUSH", "VOID") else None
        )
        close = _close_quote(row, q)
        closing_odds = float(close["decimal_odds"]) if close else None
        clv = odds/closing_odds - 1 if close else None
        graded.append({
            "game_id": row["game_id"], "market_id": row["market_id"],
            "market_type": row["market_type"],
            "selection": row["selection"], "line": row.get("line"),
            "player_id": row.get("player_id"), "book": row["book"],
            "model_version": asof_report.get("version"),
            "prediction_id": row["prediction_id"],
            "entry_decimal_odds": odds, "entry_retrieved_at_utc": row["retrieved_at_utc"],
            "expected_roi_uncalibrated": row.get("expected_roi"),
            "screening_decision": row.get("decision"),
            "settlement": outcome, "unit_return": unit_return,
            "closing_decimal_odds": closing_odds,
            "closing_observed_at_utc": close["observed_at_utc"] if close else None,
            "closing_line_value": clv,
        })

    # Paper-only cohort fixed BEFORE seeing any outcomes, based exclusively
    # on the original pretip report. One highest-odds quote per exact contract.
    chosen = {}
    for row in graded:
        if (row["expected_roi_uncalibrated"] is None
                or row["expected_roi_uncalibrated"] <= 0
                or row["screening_decision"] not in (
                    "RESEARCH_ONLY", "REVIEW_POSITIVE_EV")):
            continue
        key = (row["game_id"], row["market_id"], row["selection"],
               row.get("line"), row.get("player_id"))
        old = chosen.get(key)
        if old is None or (row["entry_decimal_odds"],row["book"]) > (
                old["entry_decimal_odds"],old["book"]):
            chosen[key] = row
    cohort = list(chosen.values())

    # Game-level calibration measures: once per immutable game, never count
    # multiple bookmakers as independent win observations.
    by_game = {x["game_id"]: x for x in asof_report.get("games", [])}
    quality, market_baseline, consensus_baseline = [], [], []
    for gid, g in by_game.items():
        actual = scores.get(gid)
        if actual is None:
            continue
        y = 1.0 if actual["home_score"] > actual["away_score"] else 0.0
        p = float(g["model_home_win_probability"])
        quality.append({"game_id": gid, "model_p": p, "home_win": y,
                        "brier": (p-y)**2,
                        "log_loss": -(y*log(max(1e-9,p))+
                                      (1-y)*log(max(1e-9,1-p)))})
        # Fixed, predeclared equal-book-weight median of eligible no-vig
        # home moneyline quotes, never selected using realized outcomes.
        consensus_candidates = [
            r["no_vig_market_probability"]
            for r in asof_report.get("markets", [])
            if r["game_id"] == gid and r["market_type"] == "moneyline"
            and r["selection"] == "home"
            and r.get("no_vig_market_probability") is not None
            and r.get("decision") == "RESEARCH_ONLY"
        ]
        if consensus_candidates:
            cp = median(consensus_candidates)
            consensus_baseline.append({
                "game_id":gid, "model_brier":(p-y)**2,
                "market_brier":(cp-y)**2,
                "model_logloss":-(y*log(max(1e-9,p)) + (1-y)*log(max(1e-9,1-p))),
                "market_logloss":-(y*log(max(1e-9,cp)) + (1-y)*log(max(1e-9,1-cp))),
                "market_p":cp, "book_count":len(consensus_candidates)
            })
        if reference_book:
            candidates = [
                r for r in asof_report.get("markets", [])
                if r["game_id"] == gid and r["market_type"] == "moneyline"
                and r["selection"] == "home" and r["book"] == reference_book
                and r.get("no_vig_market_probability") is not None
            ]
            if len(candidates) == 1:
                b = candidates[0]["no_vig_market_probability"]
                market_baseline.append({"game_id": gid, "brier": (b-y)**2,
                                        "market_p": b})

    def mean(xs):
        return sum(xs)/len(xs) if xs else None

    return {
        "version": VERSION, "research_only": True,
        "paper_cohort_rule": (
            "Pregame raw model EV > 0, eligible pre-cutoff price, "
            "best price per exact selection; rule does not imply calibrated edge"
        ),
        "market_audit": _summary(graded),
        "hypothetical_positive_raw_ev_cohort": _summary(cohort),
        "calibration": {
            "settled_game_count": len(quality),
            "model_brier": mean([r["brier"] for r in quality]),
            "model_log_loss": mean([r["log_loss"] for r in quality]),
            "reference_book": reference_book or None,
            "reference_book_games": len(market_baseline),
            "reference_book_no_vig_brier": mean(
                [r["brier"] for r in market_baseline]
            ),
            "consensus_rule": "Preselected median of eligible per-book no-vig home moneylines",
            "matched_consensus_games": len(consensus_baseline),
            "matched_game_model_brier": mean([r["model_brier"] for r in consensus_baseline]),
            "matched_game_market_brier": mean([r["market_brier"] for r in consensus_baseline]),
            "matched_game_model_logloss": mean([r["model_logloss"] for r in consensus_baseline]),
            "matched_game_market_logloss": mean([r["market_logloss"] for r in consensus_baseline]),
            "sample_large_enough_for_public_accuracy_claim": (
                len(quality) >= 200
            ),
        },
        "graded_markets": graded,
        "excluded_without_final": skipped,
        "excluded_closing_captures": invalid_closing_captures,
        "limitations": [
            "All returns are hypothetical flat-unit paper results, not executed bets.",
            "A market audit counts multiple books/selections per event; not independent wagers.",
            "Consensus benchmark is a predeclared median, not independent bookmaker observations.",
            "The experimental paper cohort may be severely miscalibrated and correlated.",
            "Closing-line value is quoted-price movement, not a guaranteed realized edge.",
            "Same-book, same-line, pretip captured close is required; no line interpolation.",
            "Missing market/grade data is not treated as a loss or push.",
            "Must use genuinely out-of-time frozen predictions and market snapshots.",
            "No claim of profitability or verified forward model calibration.",
        ],
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--asof-report", type=Path, required=True)
    ap.add_argument("--odds-ledger", type=Path, required=True)
    ap.add_argument("--finals-json", type=Path, required=True)
    ap.add_argument("--reference-book", default="")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(argv)
    report = evaluate_outcomes(
        json.loads(args.asof_report.read_text(encoding="utf-8")),
        read_jsonl(args.odds_ledger),
        json.loads(args.finals_json.read_text(encoding="utf-8")),
        reference_book=args.reference_book
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n",
                           encoding="utf-8")
    print(json.dumps({
        "sample_games": report["calibration"]["settled_game_count"],
        "paper_cohort": report["hypothetical_positive_raw_ev_cohort"],
        "research_only": True
    }))


if __name__ == "__main__":
    main()
