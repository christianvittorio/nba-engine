"""Zero-cost NBA odds adapter: HoopsAPI free plan (10 calls/day, key needed).

One GET /api/v1/games?competition=NBA yields multiple bookmakers' full-game
ML/spread/totals. Only as-of, source-captured quotes with verified NBA game
identity are written; no scraper, no bets, no line fabrication.

Free book availability varies. Stake, MelBet and bet365 are not listed in
HoopsAPI's current feed; NEVER attribute another book's odds to them.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .contracts import canonical_json, iso, utc
from .odds_map import map_provider_events
from .odds_ingest import append_odds_ledger, normalize_provider_events

BASE_URL = "https://hoopsapi.com/api/v1/games?competition=NBA"
VERSION = "gpt-v2-hoopsapi-free-odds-0.1"
# Free plan advertises these providers. Return only what is in actual data.
BOOK_ALIASES = {
    "fanduel": "FanDuel",
    "1xbet": "1xbet",
    "betway": "Betway",
    "pinnacle": "Pinnacle",
    "unibet": "Unibet",
    "smarkets": "Smarkets",
    "cloudbet": "Cloudbet",
}
FREE_BOOKS = ("FanDuel", "1xbet", "Betway", "Pinnacle", "Unibet")
ORIGINAL_REQUESTED = ("FanDuel", "Stake", "MelBet", "1xbet", "Bet365")


def fetch_free_nba_odds(*, timeout=20) -> tuple[dict,str]:
    """One authenticated free-tier API call, no charges or bypass."""
    key = os.getenv("HOOPSAPI_KEY","").strip()
    if not key:
        raise ValueError(
            "HOOPSAPI_KEY required; provider has a free, no-card API key"
        )
    try:
        with urlopen(Request(
            BASE_URL,headers={"Authorization":"Bearer "+key,
                              "Accept":"application/json"}
        ),timeout=timeout) as response:
            payload=json.loads(response.read().decode("utf-8"))
    except (HTTPError,URLError,TimeoutError) as ex:
        # Never include request/header credentials in logs.
        code=getattr(ex,"code","network")
        raise RuntimeError(
            f"HoopsAPI free-tier request failed (HTTP {code}); "
            "do not retry repeatedly, check remaining free quota"
        ) from None
    if not isinstance(payload,dict) or not isinstance(payload.get("games"),list):
        raise ValueError("Expected HoopsAPI games[] response")
    return payload,iso(datetime.now(timezone.utc))


def _price(x) -> float | None:
    try:
        if isinstance(x,bool):
            return None
        value=float(x)
        return value if 1.0<value<10001.0 else None
    except (ValueError,TypeError,OverflowError):
        return None


def _pair(market:dict, *fields:str) -> bool:
    return isinstance(market,dict) and all(
        _price(market.get(key)) is not None for key in fields
    )


def _event(row:dict) -> dict:
    return {
        "id":str(row["game_id"]),
        "home_team":row["home"],
        "away_team":row["away"],
        "commence_time":row["start_time"],
    }


def normalize_hoopsapi(payload:dict, con:sqlite3.Connection, *,
                       retrieved_at_utc:str) -> dict:
    stamp=iso(retrieved_at_utc)
    if not isinstance(payload,dict) or not isinstance(payload.get("games"),list):
        raise ValueError("Expected games array")
    eligible,skipped=[],[]
    for g in payload["games"]:
        if not isinstance(g,dict):
            continue
        if str(g.get("competition","")).strip().upper()!="NBA":
            continue
        if not all(g.get(x) is not None for x in
                   ("game_id","home","away","start_time")):
            skipped.append({"reason":"MISSING_PROVIDER_GAME_IDENTITY"})
            continue
        try:
            if utc(g["start_time"])<=utc(stamp):
                skipped.append({"provider_game_id":g["game_id"],
                                "reason":"NOT_PREGAME"})
                continue
        except (ValueError,TypeError):
            skipped.append({"provider_game_id":g["game_id"],
                            "reason":"INVALID_PROVIDER_TIP"})
            continue
        eligible.append(g)
    mapping=map_provider_events([_event(e) for e in eligible],con)
    skipped.extend(mapping["skipped"])
    converted=[]
    for g in eligible:
        eid=str(g["game_id"])
        if eid not in mapping["events"]:
            continue
        periods=g.get("periods",{})
        ft=periods.get("ft",{}) if isinstance(periods,dict) else {}
        if not isinstance(ft,dict):
            skipped.append({"provider_game_id":eid,
                            "reason":"NO_FULL_GAME_MARKETS"})
            continue
        provider_captures=g.get("providers",{})
        if not isinstance(provider_captures,dict):
            provider_captures={}
        bookmakers=[]
        for raw_book,markets in ft.items():
            canonical=BOOK_ALIASES.get(str(raw_book).strip().lower())
            if canonical is None:
                continue
            if not isinstance(markets,dict):
                continue
            provider_meta=provider_captures.get(raw_book,{})
            if not isinstance(provider_meta,dict):
                provider_meta={}
            # NO use of game updated_at: it is the latest price change
            # across all books and not source evidence for this book.
            observed=provider_meta.get("captured_at")
            if not observed:
                skipped.append({"provider_game_id":eid,"book":canonical,
                                "reason":"NO_BOOK_CAPTURE_TIMESTAMP"})
                continue
            try:
                if not utc(observed)<=utc(stamp)<utc(g["start_time"]):
                    raise ValueError("After-cutoff or post-tip collection")
            except (ValueError,TypeError):
                skipped.append({"provider_game_id":eid,"book":canonical,
                                "reason":"INVALID_BOOK_CAPTURE_TIMESTAMP"})
                continue
            home,away=g["home"],g["away"]
            groups=[]
            ml=markets.get("moneyline")
            if _pair(ml,"home","away"):
                groups.append({"key":"h2h","last_update":observed,
                               "outcomes":[
                    {"name":home,"price":float(ml["home"])},
                    {"name":away,"price":float(ml["away"])},
                ]})
            spread=markets.get("spread")
            if _pair(spread,"home","away") and spread.get("line") is not None:
                try:
                    line=float(spread["line"])
                    if not -100<line<100:raise ValueError()
                    groups.append({"key":"spreads","last_update":observed,
                                   "outcomes":[
                        {"name":home,"price":float(spread["home"]),"point":line},
                        {"name":away,"price":float(spread["away"]),"point":-line},
                    ]})
                except (TypeError,ValueError,OverflowError):
                    skipped.append({"provider_game_id":eid,"book":canonical,
                                    "reason":"INVALID_SPREAD_LINE"})
            total=markets.get("total")
            if _pair(total,"over","under") and total.get("line") is not None:
                try:
                    line=float(total["line"])
                    if not 100<line<400:raise ValueError()
                    groups.append({"key":"totals","last_update":observed,
                                   "outcomes":[
                        {"name":"Over","price":float(total["over"]),"point":line},
                        {"name":"Under","price":float(total["under"]),"point":line},
                    ]})
                except (TypeError,ValueError,OverflowError):
                    skipped.append({"provider_game_id":eid,"book":canonical,
                                    "reason":"INVALID_TOTAL_LINE"})
            if groups:
                bookmakers.append({"key":canonical,"markets":groups})
        converted.append({
            "id":eid,
            "home_team":g["home"],"away_team":g["away"],
            "commence_time":g["start_time"],
            "bookmakers":bookmakers,
        })
    normalized=normalize_provider_events(
        converted,mapping,retrieved_at_utc=stamp
    )
    for q in normalized["quotes"]:
        q["provider"]="hoopsapi-free"
        stable={k:v for k,v in q.items()
                if k not in ("retrieved_at_utc","quote_id")}
        q["quote_id"]="odds:"+hashlib.sha256(
            canonical_json(stable).encode("utf-8")
        ).hexdigest()[:24]
    skipped.extend(normalized["skipped"])
    counts={book:sum(q["book"]==book for q in normalized["quotes"])
            for book in BOOK_ALIASES.values()}
    return {
        "version":VERSION, "retrieved_at_utc":stamp,
        "free_tier":True, "free_requests_per_day":10,
        "requested_original_books":list(ORIGINAL_REQUESTED),
        "provider_supported_books":list(BOOK_ALIASES.values()),
        "mapped_nba_games":len(mapping["events"]),
        "quotes":normalized["quotes"],
        "quote_counts_by_book":counts,
        "missing_original_books":[b for b in ORIGINAL_REQUESTED
                                  if counts.get(b,0)==0],
        "skipped":skipped,
        "warning":(
            "Prices depend on actual free-tier bookmaker coverage; "
            "do not invent missing Stake/MelBet/Bet365 odds."
        )
    }


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--nba-db",type=Path,required=True)
    ap.add_argument("--ledger",type=Path,required=True)
    ap.add_argument("--report",type=Path,required=True)
    ap.add_argument("--source-json",type=Path,
                    help="Offline captured HoopsAPI response; no API request")
    ap.add_argument("--retrieved-at-utc",
                    help="Original retrieval time, required in offline mode")
    args=ap.parse_args(argv)
    if args.source_json:
        if not args.retrieved_at_utc:
            ap.error("Offline source JSON requires original retrieval timestamp")
        payload=json.loads(args.source_json.read_text(encoding="utf-8"))
        stamp=args.retrieved_at_utc
    else:
        if args.retrieved_at_utc:
            ap.error("retrieved-at-utc only applies to offline mode")
        payload,stamp=fetch_free_nba_odds()
    with sqlite3.connect(args.nba_db) as con:
        result=normalize_hoopsapi(payload,con,retrieved_at_utc=stamp)
    counts=append_odds_ledger(args.ledger,result["quotes"])
    summary={k:v for k,v in result.items() if k!="quotes"}
    summary.update(counts)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(summary,indent=2,allow_nan=False)+"\n",
                           encoding="utf-8")
    print(json.dumps({
        "free_tier":True,"mapped_games":result["mapped_nba_games"],
        "quote_counts_by_book":result["quote_counts_by_book"],
        "new_quotes":counts["new_quotes"],
        "missing_original_books":result["missing_original_books"],
    },sort_keys=True))


if __name__=="__main__":
    main()
