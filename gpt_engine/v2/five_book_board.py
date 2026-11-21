"""Read-only five-book side-by-side NBA market board (research, no wagering).

Input is already normalized, frozen, pretip as-of JSON from market_run.py.
Never fabricate missing prices or conflate different lines/bookmakers.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

from .odds_api_io import BOOKS
from .hoopsapi_free import FREE_BOOKS

VERSION = "gpt-v2-five-book-side-by-side-0.1"


def build_board(report: dict, *, books: tuple[str,...] = BOOKS) -> dict:
    if not books or len(books)!=len(set(books)):
        raise ValueError("Require unique comparison book names")
    groups = defaultdict(dict)
    for row in report.get("markets",[]):
        book = row.get("book")
        if book not in books:
            continue
        key = (row["game_id"], row["market_id"], row["market_type"],
               row["selection"], row.get("line"), row.get("player_id"))
        if book in groups[key]:
            # Duplicates should already have been collapsed in as-of reports.
            raise ValueError(f"Duplicate book quote for frozen contract {key}")
        groups[key][book] = row
    markets = []
    for key,books in groups.items():
        gid,market_id,mtype,selection,line,pid=key
        available = {
            book: {
                "decimal_odds":round(float(row["decimal_odds"]),5),
                "expected_roi_research":row.get("expected_roi"),
                "no_vig_probability":row.get("no_vig_market_probability"),
                "decision":row.get("decision"),
                "observed_at_utc":row["observed_at_utc"],
            } if (row:=books.get(book)) else None
            for book in books
        }
        best_price = max(
            (float(r["decimal_odds"]) for r in books.values()),
            default=None,
        )
        best_books = [name for name in books
                      if name in books and
                      float(books[name]["decimal_odds"])==best_price]
        probabilities = {
            float(r["model_probability"])
            for r in books.values() if r.get("model_probability") is not None
        }
        # Same outcome/line MUST have one model probability regardless of book.
        if len(probabilities)>1:
            raise ValueError("Inconsistent model probability for exact market")
        markets.append({
            "game_id":gid, "market_id":market_id,
            "market_type":mtype,"selection":selection,
            "line":line,"player_id":pid,
            "model_probability_uncalibrated":(
                next(iter(probabilities)) if probabilities else None
            ),
            "books":available, "best_decimal_odds":best_price,
            "books_tied_for_best_price":best_books,
            "available_book_count":sum(v is not None for v in available.values())
        })
    markets.sort(key=lambda x:(
        x["game_id"],x["market_type"],x["market_id"],x["selection"]
    ))
    return {
        "version":VERSION,
        "research_only":True,
        "books":list(books),
        "market_count":len(markets),
        "markets":markets,
        "notes":[
            "Every price is the same game's exact market, side and point line.",
            "An em dash means that sportsbook had no eligible captured price.",
            "Prices are only those observed and retrieved before the model cutoff.",
            "Model probabilities and raw EV are uncalibrated research, not verified edges.",
            "Provider coverage is not equivalent to availability at every sportsbook.",
        ]
    }


def to_markdown(board: dict) -> str:
    books=board["books"]
    columns=" | ".join(books)
    lines=[
        "# NBA GPT v2 — Five Sportsbooks vs Model",
        "",
        "**UNVALIDATED MODEL RESEARCH — NOT LIVE BETTING SIGNALS**",
        "",
        "Bookmakers: "+", ".join(books)+".",
        "",
        "| NBA game | Market | Selection | Line | Model P* | "+
            columns+" | Best available |",
        "|---|---|---|---:|---:|"+("---:|"*len(books))+"---|",
    ]
    for row in board["markets"]:
        model = row["model_probability_uncalibrated"]
        prob = f"{model:.1%}" if model is not None else "—"
        prices = [
            (f"{row['books'][book]['decimal_odds']:.2f}"
             if row["books"][book] is not None else "—")
            for book in books
        ]
        best=(f"{row['best_decimal_odds']:.2f} "
              + ", ".join(row["books_tied_for_best_price"])
              if row["best_decimal_odds"] is not None else "—")
        line=(f"{row['line']:+g}" if row["line"] is not None else "—")
        lines.append("| "+" | ".join([
            row["game_id"],row["market_type"]+" / "+row["market_id"],
            row["selection"],line,prob,*prices,best
        ])+" |")
    if not board["markets"]:
        lines.append("| No five-book odds captured at the forecast cutoff | — | — | — | — | — | — | — | — | — | — |")
    lines.extend(["","*Model P is experimental and uncalibrated. Missing prices "
                  "cannot be substituted from other bookmakers or later timestamps.*",
                  ""])
    return "\n".join(lines)


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--asof-report",type=Path,required=True)
    ap.add_argument("--book-set",choices=("requested","free"),default="requested",
                    help="requested=FanDuel/Stake/MelBet/1xbet/Bet365; free=HoopsAPI five")
    ap.add_argument("--output-json",type=Path,required=True)
    ap.add_argument("--output-md",type=Path,required=True)
    a=ap.parse_args(argv)
    report=json.loads(a.asof_report.read_text(encoding="utf-8"))
    books=FREE_BOOKS if a.book_set=="free" else BOOKS
    board=build_board(report,books=books)
    a.output_json.parent.mkdir(parents=True,exist_ok=True)
    a.output_md.parent.mkdir(parents=True,exist_ok=True)
    a.output_json.write_text(json.dumps(board,indent=2,allow_nan=False)+"\n",
                             encoding="utf-8")
    a.output_md.write_text(to_markdown(board),encoding="utf-8")
    print(json.dumps({"markets":board["market_count"],
                      "five_book_research":True}))


if __name__=="__main__":
    main()
