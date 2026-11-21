"""Combine independently generated V2 reports into dated, readable Markdown.

The combined report is a research VIEW, not a new forecast. Source odds
remain private: the public file contains derived probabilities, market
identities, names and statistical evidence but NO raw provider price.
All betting research must be reconstructed using existing frozen, pre-tip
market snapshots; never recompute a historical forecast from future data.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sqlite3
from zoneinfo import ZoneInfo

from .contracts import iso
from .parlay_research import build_parlay_board

ET = ZoneInfo("America/New_York")
PH = ZoneInfo("Asia/Manila")
VERSION = "gpt-v2-master-daily-research-0.1"
DVP_REF = "https://hashtagbasketball.com/nba-defense-vs-position"


def _safe(x) -> str:
    """Escape only interpolated pipe/line-break content in Markdown tables."""
    return str(x).replace("|", r"\|").replace("\r", " ").replace("\n", " ")


def _p(x) -> str:
    return f"{float(x):.1%}"


def _lookup(con, day: str) -> dict[str, dict]:
    sql = (
        "SELECT g.game_id,g.game_date_eastern,g.tip_utc,"
        "a.current_name,h.current_name "
        "FROM games g JOIN teams a ON a.team_id=g.away_team_id "
        "JOIN teams h ON h.team_id=g.home_team_id "
        "WHERE g.game_date_eastern=? AND g.game_type='regular_season'"
    )
    return {
        str(gid): {"matchup": f"{away} @ {home}", "tip_utc":tip}
        for gid,_,tip,away,home in con.execute(sql,(day,))
    }


def _line(leg: dict) -> str:
    val=leg.get("line")
    return "—" if val is None else f"{float(val):+g}"


def _market_label(leg: dict, matchups: dict) -> str:
    return matchups.get(leg.get("game_id"), {}).get(
        "matchup", _safe(leg.get("game_id", "Unmapped game"))
    )


def _selected_single_table(singles: list, matchups: dict) -> list[str]:
    rows=[
        "| Game | Market | Side | Line | Model win/cover | Break-even | Raw model EV | Book |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    if not singles:
        rows.append("| No qualifying priced high-hit single | — | — | — | — | — | — | — |")
    for x in singles:
        rows.append(
            f"| {_safe(_market_label(x,matchups))} | {x['market_type']} | "
            f"{_safe(x['selection'])} | {_line(x)} | "
            f"{_p(x['model_probability'])} | "
            f"{_p(x['bookmaker_break_even_win_probability'])} | "
            f"{float(x['individual_research_roi']):+.1%} | {_safe(x['book'])} |"
        )
    return rows


def _insert_daily_detail(daily_markdown: str) -> str:
    """Nest original detailed report as a subsection without altering facts."""
    shifted=[]
    for line in daily_markdown.splitlines():
        if line.startswith("#"):
            n=len(line)-len(line.lstrip("#"))
            if n<=4 and line[n:n+1]==" ":
                line=("#"*(n+1))+line[n:]
        shifted.append(line)
    return "\n".join(shifted)


def render_master_report(
    day: str, daily_markdown: str, market_report: dict,
    parlay_report: dict, alt_report: dict, evaluation: dict,
    matchups: dict, *, generated_at_utc: str
) -> str:
    """Deterministic per-Eastern-day report; NO future dates or raw odds."""
    datetime.strptime(day,"%Y-%m-%d")
    if not daily_markdown.startswith("# GPT v2 NBA daily simulation report"):
        raise ValueError("Exact dated original daily simulation report required")
    if f"— {day} (US Eastern)" not in daily_markdown.splitlines()[0]:
        raise ValueError("Daily forecast Markdown is for the wrong date")
    if not all(isinstance(x,dict) and x.get("research_only") is True
               for x in (market_report,parlay_report,alt_report,evaluation)):
        raise ValueError("All research components must be research-only")
    if not generated_at_utc:
        raise ValueError("Original pretip research timestamp required")

    # Re-rank the exact frozen market/quotes for THIS date; a combined
    # two-day global leader must never be advertised for both dates.
    current_day_market={
        **market_report,
        "markets":[x for x in market_report.get("markets",[])
                   if x.get("game_id") in matchups],
    }
    filtered_board=build_parlay_board(
        current_day_market,date_eastern=day,
        now_utc=parlay_report["generated_at_utc"]
    )
    singles=[x for x in filtered_board["ranked_high_hit_singles"]
             if x["game_id"] in matchups]
    best=filtered_board["best_research_combination"]
    if best and not all(x["game_id"] in matchups for x in best["legs"]):
        raise ValueError("Cross-date parlay presented in dated report")
    alt=[x for x in alt_report.get("candidates",[])
         if x["date_eastern"]==day and x["game_id"] in matchups]
    alt.sort(key=lambda x:(-x["raw_season_hit_rate"],
                           -x["estimated_usage_percent"],
                           x["game_id"],x.get("player_id",""),x["stat"]))
    alt_priced=[x for x in alt_report.get("priced_alternate_legs",[])
                if x.get("date_eastern")==day and x["game_id"] in matchups]
    alt_ticket=alt_report.get("same_book_parlay")
    if alt_ticket and any(x.get("date_eastern")!=day or
                          x.get("game_id") not in matchups
                          for x in alt_ticket.get("legs",[])):
        alt_ticket=None
    source_names=sorted({x["book"] for x in market_report.get("markets",[])
                         if x.get("game_id") in matchups and x.get("book")})
    coverage=next((x for x in alt_report.get("defense_coverage",[])
                   if x.get("asof_date_eastern")==day),None)
    freshness=[x for x in alt_report.get("prior_final_freshness",[])
               if x.get("date_eastern")==day]
    missing_prior=max((int(x["missing_due_final_games"]) for x in freshness),default=0)
    impacted=set()
    for x in freshness:
        impacted.update(x.get("candidate_teams_with_unsettled_past_game",{}))
    local_date=(datetime.strptime(day,"%Y-%m-%d").date()+timedelta(days=1)).isoformat()
    forecasted=(
        daily_markdown.count("### ") if "### " in daily_markdown else 0
    )
    lines=[
        f"# NBA Engine V2 — Unified Daily Research — {day} (US Eastern)",
        "",
        f"**Generated:** {iso(generated_at_utc)}",
        f"**Date interpretation:** games dated {day} Eastern often begin "
        f"on {local_date} in the Philippines; see each actual tip below.",
        "**Status:** RESEARCH / UNCALIBRATED — NOT A BETTING RECOMMENDATION.",
        "**Sources:** immutable pretip NBA simulations, current-season verified "
        "game logs, and only actually observed named-book prices.",
        "",
        "## Executive summary and data health",
        "",
        f"- **Scheduled games covered by current NBA database:** {len(matchups)}.",
        f"- **Actual named bookmakers in this date's quote evidence:** "
        f"{', '.join(source_names) if source_names else 'none'} "
        "(does not imply all markets or alternate props are available).",
        f"- **Eligible high-hit single-game research markets:** {len(singles)}.",
        f"- **Positive-value parlay candidates screened for THIS date:** "
        f"{filtered_board['candidate_tickets_screened']}.",
        f"- **90%-season-hit high-usage DvP statistical candidates:** {len(alt)}.",
        f"- **Exact source-priced alternative player-prop legs:** {len(alt_priced)}.",
        f"- **Past games missing sourced final box scores:** {missing_prior}"
        f" (affected candidate teams this date: {len(impacted)}).",
        f"- **DVP provider used by engine:** independent completed-game NBA logs "
        "with published **G / F / C** group labels. Fine-grained "
        "**PG / SG / SF / PF / C is NOT sourced or imported**.",
        f"- **External five-position comparison:** [Hashtag Basketball DvP]({DVP_REF}) "
        "reports per-48 PG/SG/SF/PF/C values. **Reference only, not ingested;** "
        "access/redistribution rights and exact-position player mappings "
        "are still unverified.",
        "",
        "## High-hit single-game research rankings",
        "",
        "Eligible singles are ranked by **modeled** win/cover probability, "
        "not ROI; +0.1% raw model-EV per leg is an eligibility floor. "
        "Neither model hit rate nor EV is calibrated.",
        "",
        *_selected_single_table(singles,matchups),
        "",
        "## Highest modeled chance — same-book game parlay",
        "",
    ]
    if not best:
        lines+=["**NO QUALIFYING GAME PARLAY** for this specific Eastern date.",
                "No ticket is forced when eligible prices or independent "
                "same-game safeguards are missing.",""]
    else:
        lines+= [
            f"**Research status:** {best['validation_status']} — "
            f"{best['leg_count']} legs from {_safe(best['book'])}.",
            "",
            "| Game | Market | Side | Line | Modeled single-leg hit |",
            "|---|---|---|---:|---:|",
        ]
        for x in best["legs"]:
            lines.append(
                f"| {_safe(_market_label(x,matchups))} | {x['market_type']} | "
                f"{_safe(x['selection'])} | {_line(x)} | "
                f"{_p(x['model_probability'])} |"
            )
        lines += [
            "",
            f"- **Independent modeled chance ALL legs win:** "
            f"{_p(best['full_win_probability_independent'])}.",
            f"- **Raw theoretical model ROI:** "
            f"{float(best['estimated_roi_independent']):+.1%} "
            "(NOT a verified real-world edge).",
            "- Same bookmaker, at most one selection per game, "
            "same Eastern date, and pretip timestamp gate.",
            "",
        ]

    lines += [
        "## High-usage / bottom-five-position / 90%-season-hit alt props",
        "",
        "Only qualified position evidence (currently **G/F/C**) is allowed. "
        "A player with 90% historical hits is NOT necessarily 90% likely "
        "to hit tonight. **Alt-over thresholds below are historical "
        "statistical levels, NOT confirmed sportsbook offerings.**",
        "",
        "| Player | Game | Position group | Stat | Historical alt OVER | "
        "Season hits | Last 5 | Opp defense rank (most allowed) | Usage | Availability |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    if not alt:
        lines.append("| No fully verified 90%-season-history candidate | — | — | — | — | — | — | — | — | — |")
    for x in alt:
        lines.append(
            f"| {_safe(x['player'])} | {_safe(_market_label(x,matchups))} | "
            f"{x['position_group']} | {x['stat'].upper()} | "
            f"{float(x['alt_over_line']):.1f} | "
            f"{x['season_hits']}/{x['season_games']} "
            f"({_p(x['raw_season_hit_rate'])}) | "
            f"{x['last_five_hits']}/5 | "
            f"{x['opponent_defense']['rank_most_allowed']}/30 | "
            f"{x['estimated_usage_percent']:.1f}% "
            f"(team #{x['team_usage_rank']}) | "
            f"{_safe(x['availability'])} |"
        )
    lines+=["","### Defenses-by-position data quality",""]
    if coverage:
        for pos,details in sorted(coverage["position_coverage"].items()):
            lines.append(
                f"- **{pos}:** {details['valid_defensive_teams']}/"
                f"{details['required_teams']} verified defenses; "
                f"{'30-team rank available' if details['rankable'] else 'ranking withheld for missing coverage'}."
            )
    else:
        lines.append("- No verified defender group coverage for this date.")
    if missing_prior:
        lines.append(
            f"- Missing past-game finals: **{missing_prior}**; "
            "affected-team alt hit-rate claims are excluded, not "
            "replaced with optimistic 90% figures."
        )
    lines+=["","### Alternate-player-prop parlay status",""]
    if not alt_ticket:
        lines += [
            "**NO SOURCE-VERIFIED ALTERNATE-PROP PARLAY.** "
            "A statistical watchlist is not a quoted or placeable ticket.",
            "Missing data: "+(
                "; ".join(alt_report.get("missing_requirements",[]))
                if alt_report.get("missing_requirements") else
                "no two independently priced, suitable player prop legs for this date"
            )+".",
        ]
    else:
        lines += [
            f"**Research-only, uncalibrated source-priced alt parlay** "
            f"({_safe(alt_ticket['book'])}):",
        ]
        for leg in alt_ticket["legs"]:
            lines.append(
                f"- {_safe(leg['player'])}: {leg['stat'].upper()} over "
                f"{leg['alt_over_line']:.1f}; "
                f"{leg['season_hits']}/{leg['season_games']} past games; "
                f"{_p(leg['model_probability_uncalibrated'])} raw model P."
            )
        lines.append(
            f"- **Raw independence-model joint hit estimate:** "
            f"{_p(alt_ticket['raw_model_joint_win_probability_independent'])}; "
            "**NOT** approved as a bet."
        )
    lines+=["","## Postgame settlement and backtesting status",""]
    per_day_grades=[
        x for x in evaluation.get("graded_markets",[])
        if x.get("game_id") in matchups
    ]
    if not per_day_grades:
        lines.append(
            "**No verified final outcome grading for these games yet.** "
            "The report does not use future results in pretip candidate generation."
        )
    else:
        results={}
        for grade in per_day_grades:
            result=grade.get("settlement","NOT_GRADED")
            results[result]=results.get(result,0)+1
        lines.append(
            f"- **Priced market outcomes independently graded:** "
            f"{len(per_day_grades)} ("
            +", ".join(f"{k}: {v}" for k,v in sorted(results.items()))+")."
        )
        lines.append(
            "- Outcome grading is not proof of calibration; "
            "the original forecast and price timestamps remain immutable."
        )
    lines += [
        "",
        "## Detailed game-by-game forecasts and situational breakdown",
        "",
        _insert_daily_detail(daily_markdown),
        "",
        "## Model and data-quality limitations",
        "",
        "- All reported probabilities and apparent EVs are **uncalibrated**; "
        "past hit rates must be assessed out-of-sample.",
        "- Individual positional defender assignments, confirmed starts, "
        "and full-season historical freshness can be incomplete.",
        "- Hashtag Basketball's PG/SG/SF/PF/C DvP view is an external "
        "comparison only, **not the source of the numbers above**.",
        "- Raw provider odds and original sportsbook payloads are "
        "intentionally NOT published in this file.",
        "- No automated wagering, staking recommendations, or guarantee "
        "of an edge. A missing quote means no quote.",
        "",
    ]
    return "\n".join(lines)


def generate(db: Path, daily_dir: Path, market_file: Path,
             parlay_file: Path, alt_file: Path, eval_file: Path,
             *, date_eastern: str | None = None,
             now_utc: str | None = None) -> list[Path]:
    current=datetime.fromisoformat(
        (now_utc or iso(datetime.now(timezone.utc))).replace("Z","+00:00")
    )
    day_list=[date_eastern] if date_eastern else [
        (current.astimezone(ET).date()+timedelta(days=i)).isoformat()
        for i in (0,1)
    ]
    market=json.loads(market_file.read_text(encoding="utf-8"))
    parlay=json.loads(parlay_file.read_text(encoding="utf-8"))
    alt=json.loads(alt_file.read_text(encoding="utf-8"))
    evaluated=json.loads(eval_file.read_text(encoding="utf-8"))
    saved=[]
    with sqlite3.connect(db) as con:
        for day in day_list:
            datetime.strptime(day,"%Y-%m-%d")
            original=daily_dir/f"daily_{day}.md"
            if not original.is_file():
                raise FileNotFoundError(
                    f"Daily original simulation missing for Eastern date {day}"
                )
            report=render_master_report(
                day,original.read_text(encoding="utf-8"),
                market,parlay,alt,evaluated,_lookup(con,day),
                generated_at_utc=now_utc or iso(current)
            )
            destination=daily_dir/f"research_{day}.md"
            destination.write_text(report,encoding="utf-8")
            saved.append(destination)
    return saved


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--db",required=True,type=Path)
    p.add_argument("--report-dir",required=True,type=Path)
    p.add_argument("--asof-report",required=True,type=Path)
    p.add_argument("--parlay-json",required=True,type=Path)
    p.add_argument("--alt-prop-json",required=True,type=Path)
    p.add_argument("--evaluation-json",required=True,type=Path)
    p.add_argument("--date",default=None)
    args=p.parse_args(argv)
    written=generate(
        args.db,args.report_dir,args.asof_report,args.parlay_json,
        args.alt_prop_json,args.evaluation_json,date_eastern=args.date
    )
    print(json.dumps({
        "unified_markdown_reports": [str(x) for x in written],
        "public_report_contains_provider_raw_odds": False,
        "research_only": True,
        "hashtag_dvp_imported": False,
    },sort_keys=True))


if __name__=="__main__":
    main()
