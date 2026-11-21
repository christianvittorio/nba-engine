"""Join frozen GPT v2 pretip reports with historically available sportsbook odds.

Never use bookmaker snapshots retrieved after the model's forecast cutoff,
even when their provider 'last_update' happens to predate the model.
Current possession probabilities are explicitly marked uncalibrated.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .contracts import iso, utc
from .market_value import compare_markets, _validate_quote
from .odds_ingest import PROPS

VERSION = "gpt-v2-market-asof-report-0.1"


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def read_frozen_forecasts(forecast_ledger: Path, root: Path) -> list[dict]:
    docs = []
    for record in read_jsonl(forecast_ledger):
        source = root / record["file"]
        if not source.is_file():
            raise FileNotFoundError(f"Missing frozen prediction: {source}")
        doc = json.loads(source.read_text(encoding="utf-8"))
        if (doc["prediction_id"] != record["prediction_id"]
                or doc["game_id"] != record["game_id"]
                or iso(doc["cutoff_utc"]) != iso(record["cutoff_utc"])
                or doc["model_version"] != record["model_version"]):
            raise ValueError("Immutable prediction ledger does not match report")
        if utc(doc["cutoff_utc"]) >= utc(doc["tip_utc"]):
            raise ValueError("Forecast made after tipoff")
        docs.append(doc)
    if len({x["game_id"] for x in docs}) != len(docs):
        raise ValueError("Duplicate game forecast; use explicit versions separately")
    return docs


def asof_market_report(forecasts: list[dict], quotes: list[dict], *,
                       max_snapshot_gap_minutes: float = 30) -> dict:
    """Return a paper-analysis slate; not a source of validated bet picks."""
    model_by_game = {}
    for doc in forecasts:
        gid = doc["game_id"]
        if gid in model_by_game:
            raise ValueError("Duplicate immutable per-game forecast")
        if utc(doc["cutoff_utc"]) >= utc(doc["tip_utc"]):
            raise ValueError("After-tip forecast")
        if not 0 <= float(doc["result"]["home_win_probability"]) <= 1:
            raise ValueError("Invalid model win probability")
        model_by_game[gid] = doc

    observed, excluded = {}, []
    for raw in quotes:
        q = _validate_quote(raw)
        doc = model_by_game.get(q["game_id"])
        if doc is None:
            excluded.append({"game_id": q["game_id"], "book": q["book"],
                             "reason": "NO_IMMUTABLE_FORECAST"})
            continue
        if q["tip_utc"] != iso(doc["tip_utc"]):
            excluded.append({"game_id": q["game_id"], "book": q["book"],
                             "reason": "TIP_MISMATCH"})
            continue
        retrieval = q.get("retrieved_at_utc")
        if retrieval is None:
            excluded.append({"game_id": q["game_id"], "book": q["book"],
                             "reason": "NO_ORIGINAL_RETRIEVAL_EVIDENCE"})
            continue
        if not (utc(q["observed_at_utc"]) <= utc(retrieval)
                <= utc(doc["cutoff_utc"])):
            excluded.append({"game_id": q["game_id"], "book": q["book"],
                             "reason": "QUOTE_NOT_AVAILABLE_AT_FORECAST_CUTOFF"})
            continue
        identity = (q["game_id"], q["book"], q["market_id"],
                    q["selection"], q.get("line"), q.get("player_id"))
        previous = observed.get(identity)
        if previous is None or (q["observed_at_utc"], retrieval) > (
                previous["observed_at_utc"], previous["retrieved_at_utc"]):
            observed[identity] = q

    picked = list(observed.values())
    preds = []
    for gid, doc in model_by_game.items():
        base = {
            "game_id": gid, "tip_utc": iso(doc["tip_utc"]),
            "asof_utc": iso(doc["cutoff_utc"]),
            "model_version": doc["model_version"],
            "market_id": "game:moneyline", "market_type": "moneyline",
            "line": None, "calibration_status": "uncalibrated",
        }
        hprob = float(doc["result"]["home_win_probability"])
        preds.extend([
            {**base, "selection": "home", "probability": hprob},
            {**base, "selection": "away", "probability": 1-hprob},
        ])
    compared = compare_markets(
        picked, preds, max_snapshot_gap_minutes=max_snapshot_gap_minutes
    )
    quote_by_key = {
        (q["game_id"], q["book"], q["market_id"], q["selection"],
         q.get("line"), q.get("player_id")): q for q in picked
    }
    rows = []
    for result in compared["markets"]:
        gid = result["game_id"]
        doc = model_by_game[gid]
        q = quote_by_key[(
            gid, result["book"], result["market_id"], result["selection"],
            result["line"], result.get("player_id")
        )]
        sim = doc["result"]
        row = {**result, "prediction_id": doc["prediction_id"],
               "forecast_cutoff_utc": doc["cutoff_utc"],
               "retrieved_at_utc": q["retrieved_at_utc"],
               "model_vs_book_point_difference": None,
               "model_stat_mean": None}
        if result["market_type"] == "spread":
            home_spread = (
                result["line"] if result["selection"] == "home"
                else -result["line"]
            )
            row["model_vs_book_point_difference"] = (
                float(sim["margin"]["mean"]) + home_spread
            )
        elif result["market_type"] == "total":
            row["model_vs_book_point_difference"] = (
                float(sim["total"]["mean"]) - result["line"]
            )
        elif result["market_type"] == "player_prop":
            stat = PROPS.get(q.get("provider_market_key"))
            if stat is not None:
                player = sim.get("player_statistics", {}).get(
                    q.get("player_id"), {}
                )
                data = player.get(stat, {})
                if isinstance(data, dict) and "mean" in data:
                    row["model_stat_mean"] = float(data["mean"])
                    row["model_vs_book_point_difference"] = (
                        row["model_stat_mean"] - result["line"]
                    )
        rows.append(row)

    games = [{
        "game_id": doc["game_id"],
        "prediction_id": doc["prediction_id"],
        "model_version": doc["model_version"],
        "cutoff_utc": iso(doc["cutoff_utc"]),
        "tip_utc": iso(doc["tip_utc"]),
        "home_team_id": doc["home_team_id"],
        "away_team_id": doc["away_team_id"],
        "model_home_win_probability": float(
            doc["result"]["home_win_probability"]),
        "expected_home_score": float(doc["result"]["expected_home_score"]),
        "expected_away_score": float(doc["result"]["expected_away_score"]),
        "observed_quote_count": sum(x["game_id"] == doc["game_id"]
                                    for x in rows),
    } for doc in forecasts]
    return {
        "version": VERSION, "research_only": True,
        "validation": "UNCALIBRATED_LIVE_POSSESSION_SIMULATOR",
        "games": games, "markets": rows,
        "raw_quote_count": len(quotes),
        "usable_asof_quote_count": len(picked),
        "excluded": excluded,
        "notes": [
            "Only odds actually retrieved by forecast cutoff are eligible.",
            "No line-specific spread/total/prop distribution calibrated yet.",
            "For spreads, positive point difference favors the home handicap.",
            "For totals/props, positive point difference means model mean above line.",
            "Point differences are not win probability or expected value.",
            "Game moneyline EV is research-only; live simulator is uncalibrated.",
            "Unknown player minutes mean prop projections are conditional.",
            "No staking, betting execution or validated profitability claims.",
        ],
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# GPT v2 sportsbook vs model — frozen as-of research comparison",
        "",
        "**RESEARCH / NOT VALIDATED FOR BETTING**",
        "",
        f"Games: {len(report['games'])}; quotes in ledger: {report['raw_quote_count']}; "
        f"available at forecast cutoff: {report['usable_asof_quote_count']}; "
        f"excluded: {len(report['excluded'])}.",
        "",
        "Only original pretip sportsbook quotes actually retrieved by the "
        "model cutoff are considered; no retrospective latest odds.",
        "",
    ]
    for game in report["games"]:
        gid = game["game_id"]
        lines.extend([
            f"## {game['away_team_id']} @ {game['home_team_id']}",
            "",
            f"- NBA game: `{gid}` | forecast: `{game['prediction_id']}`",
            f"- Forecast cutoff: {game['cutoff_utc']}",
            f"- Predicted score: away {game['expected_away_score']:.1f}, "
            f"home {game['expected_home_score']:.1f}",
            f"- Home win simulation: {game['model_home_win_probability']:.1%} "
            "(UNCALIBRATED)",
            "",
            "| Book | Market | Selection | Line | Odds | Model P | No-vig P | "
            "Raw EV* | Mean − market (pts) | Status |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
        ])
        matched = [r for r in report["markets"] if r["game_id"] == gid]
        if not matched:
            lines.append("| No matching timestamp-verified odds | — | — | — | — | — | — | — | — | — |")
        for r in matched:
            fmt = lambda v, spec: "—" if v is None else format(v, spec)
            lines.append("| " + " | ".join([
                r["book"], r["market_id"], r["selection"],
                fmt(r["line"], "+g"), fmt(r["decimal_odds"], ".2f"),
                fmt(r["model_probability"], ".1%"),
                fmt(r["no_vig_market_probability"], ".1%"),
                fmt(r["expected_roi"], "+.1%"),
                fmt(r["model_vs_book_point_difference"], "+.1f"),
                r["decision"],
            ]) + " |")
        lines.append("")
    lines.extend([
        "*Raw EV is a mathematical estimate conditional on the uncalibrated "
        "model, not evidence of a profitable wager.*",
        "",
        "## Limitations",
        "",
    ])
    lines.extend("- " + s for s in report["notes"])
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--forecast-ledger", type=Path, required=True)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--odds-ledger", type=Path, required=True)
    ap.add_argument("--output-json", type=Path, required=True)
    ap.add_argument("--output-md", type=Path, required=True)
    ap.add_argument("--max-snapshot-gap-minutes", type=float, default=30)
    args = ap.parse_args(argv)
    docs = read_frozen_forecasts(args.forecast_ledger, args.root)
    report = asof_market_report(
        docs, read_jsonl(args.odds_ledger),
        max_snapshot_gap_minutes=args.max_snapshot_gap_minutes
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8"
    )
    args.output_md.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({
        "games": len(report["games"]),
        "asof_quotes": report["usable_asof_quote_count"],
        "excluded_quotes": len(report["excluded"]),
        "research_only": True,
    }))


if __name__ == "__main__":
    main()
