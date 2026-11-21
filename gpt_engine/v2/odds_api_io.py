"""Five-book NBA sportsbook snapshot adapter for Odds-API.io v3.

Selected: FanDuel, Stake, MelBet, 1xbet, Bet365.
This adapter does not place bets or perform browser scraping. It maps only
confirmed upcoming NBA fixtures and source-timestamped full-game two-way
ML/spread/totals. Other/three-way or unverified markets are rejected.
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
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .contracts import canonical_json, iso, utc
from .odds_ingest import append_odds_ledger, normalize_provider_events
from .odds_map import map_provider_events

API_ROOT = "https://api.odds-api.io/v3"
BOOKS = ("FanDuel", "Stake", "MelBet", "1xbet", "Bet365")
MARKETS = ("ML", "Spread", "Totals")
VERSION = "gpt-v2-five-sportsbooks-odds-api-io-0.1"


def _request(endpoint: str, params: dict, *, timeout: int = 20):
    key = os.getenv("ODDS_API_IO_KEY", "").strip()
    if not key:
        raise ValueError("ODDS_API_IO_KEY is required for live five-book retrieval")
    if not endpoint.startswith("/") or "?" in endpoint:
        raise ValueError("Invalid endpoint")
    args = {"apiKey": key, **params}
    try:
        url = API_ROOT + endpoint + "?" + urlencode(args)
        with urlopen(Request(url,headers={"Accept":"application/json"}),
                     timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError,URLError,TimeoutError) as ex:
        # URLs can contain the API key. Never echo exception/url.
        code = getattr(ex,"code","network")
        raise RuntimeError(f"Odds-API.io request failed (HTTP {code})") from None


def _is_nba(event: dict) -> bool:
    league = event.get("league", {})
    if isinstance(league,dict):
        slug = str(league.get("slug") or "").strip().casefold()
        name = str(league.get("name") or "").strip().casefold()
    else:
        slug = str(league).strip().casefold()
        name = slug
    # Provider docs have used both usa-nba and nba-regular-season.
    # Summer League / All-Star are deliberately excluded.
    return (slug in ("nba","usa-nba","nba-regular-season",
                     "nba-playoffs","nba-finals")
            or name in ("nba","nba regular season","nba playoffs","nba finals"))


def _event_id(event: dict) -> str:
    return str(event.get("id","")).strip()


def _canonical_event(event: dict) -> dict:
    return {
        "id":_event_id(event),
        "home_team":event.get("home",""),
        "away_team":event.get("away",""),
        "commence_time":event.get("date",""),
    }


def _odds_price(v):
    try:
        value = float(v)
        return value if 1 < value < 10001 else None
    except (TypeError,ValueError,OverflowError):
        return None


def _flatten_one_market(name: str, rows: list) -> tuple[list[dict],list[str]]:
    """Build only verified full-game, two-sided contracts.

    In the Odds-API.io format hdp is signed HOME handicap; away is -hdp.
    The max field on totals is the over/under point line.
    """
    outcomes, reasons = [], []
    if not isinstance(rows,list):
        return [], ["INVALID_MARKET_ROWS"]
    for item in rows:
        if not isinstance(item,dict):
            reasons.append("INVALID_MARKET_ROW")
            continue
        if name == "ML":
            # A listed draw implies three-way regulation-only settlement;
            # this project simulates full game including OT, so skip.
            if item.get("draw") not in (None,"",0,"0"):
                reasons.append("THREE_WAY_MONEYLINE_UNSUPPORTED")
                continue
            if (_odds_price(item.get("home")) is None or
                    _odds_price(item.get("away")) is None):
                reasons.append("INCOMPLETE_TWO_WAY_MONEYLINE")
                continue
            outcomes += [
                {"name":"__HOME__","price":float(item["home"])},
                {"name":"__AWAY__","price":float(item["away"])},
            ]
        elif name == "Spread":
            try:
                line = float(item["hdp"])
                if not -100 < line < 100:
                    raise ValueError()
            except (KeyError,TypeError,ValueError,OverflowError):
                reasons.append("INVALID_HOME_HANDICAP")
                continue
            if (_odds_price(item.get("home")) is None or
                    _odds_price(item.get("away")) is None):
                reasons.append("INCOMPLETE_SPREAD_PAIR")
                continue
            outcomes += [
                {"name":"__HOME__","point":line,"price":float(item["home"])},
                {"name":"__AWAY__","point":-line,"price":float(item["away"])},
            ]
        elif name == "Totals":
            try:
                line = float(item["max"])
                if not 100 < line < 400:
                    raise ValueError()
            except (KeyError,TypeError,ValueError,OverflowError):
                reasons.append("INVALID_TOTAL_LINE")
                continue
            if (_odds_price(item.get("over")) is None or
                    _odds_price(item.get("under")) is None):
                reasons.append("INCOMPLETE_TOTAL_PAIR")
                continue
            outcomes += [
                {"name":"Over","point":line,"price":float(item["over"])},
                {"name":"Under","point":line,"price":float(item["under"])},
            ]
    return outcomes,reasons


def normalize_five_book_events(events: list[dict], odds: list[dict],
                               con: sqlite3.Connection, *,
                               retrieved_at_utc: str) -> dict:
    """Return canonical quote records and auditable coverage/missing reasons."""
    stamp = iso(retrieved_at_utc)
    eligible = {}
    skipped = []
    for event in events:
        eid = _event_id(event)
        if not eid or not _is_nba(event):
            continue
        if event.get("status") != "pending":
            skipped.append({"provider_event_id":eid,"reason":"EVENT_NOT_PENDING"})
            continue
        eligible[eid] = event
    # An empty odds object for a book is not an invented quote.
    mapping_events = [_canonical_event(e) for e in eligible.values()]
    mapped = map_provider_events(mapping_events,con)
    for entry in mapped["skipped"]:
        skipped.append(entry)
    canonical = []
    returned_books = set()
    for response in odds:
        if not isinstance(response,dict):
            skipped.append({"reason":"INVALID_PROVIDER_ODDS_RESPONSE"})
            continue
        eid = _event_id(response)
        event = eligible.get(eid)
        if not event or eid not in mapped["events"]:
            skipped.append({"provider_event_id":eid,
                            "reason":"ODDS_EVENT_NOT_ELIGIBLE_OR_MAPPED"})
            continue
        if response.get("status") != "pending":
            skipped.append({"provider_event_id":eid,"reason":"ODDS_NOT_PREMATCH"})
            continue
        sourcebooks = response.get("bookmakers",{})
        if not isinstance(sourcebooks,dict):
            skipped.append({"provider_event_id":eid,"reason":"INVALID_BOOKMAKER_PAYLOAD"})
            continue
        converted_books = []
        for book in BOOKS:
            if book not in sourcebooks:
                continue
            returned_books.add(book)
            groups = sourcebooks[book]
            if not isinstance(groups,list):
                skipped.append({"provider_event_id":eid,"book":book,
                                "reason":"INVALID_MARKET_GROUPS"})
                continue
            converted_markets = []
            for group in groups:
                if not isinstance(group,dict):
                    continue
                name = group.get("name")
                if name not in MARKETS:
                    continue
                observed = group.get("updatedAt")
                if not observed:
                    skipped.append({"provider_event_id":eid,"book":book,
                                    "market":name,"reason":"NO_ODDS_UPDATED_AT"})
                    continue
                parts,issues = _flatten_one_market(name,group.get("odds",[]))
                for issue in issues:
                    skipped.append({"provider_event_id":eid,"book":book,
                                    "market":name,"reason":issue})
                for part in parts:
                    if part["name"]=="__HOME__":
                        part["name"] = event["home"]
                    if part["name"]=="__AWAY__":
                        part["name"] = event["away"]
                if parts:
                    converted_markets.append({
                        "key":{"ML":"h2h","Spread":"spreads",
                               "Totals":"totals"}[name],
                        "last_update":observed,
                        "outcomes":parts
                    })
            if converted_markets:
                converted_books.append({"key":book,"markets":converted_markets})
        canonical.append({
            "id":eid, "home_team":event.get("home"),
            "away_team":event.get("away"), "commence_time":event.get("date"),
            "bookmakers":converted_books
        })
    normalized = normalize_provider_events(
        canonical,mapped,retrieved_at_utc=stamp
    )
    # Rewrite provenance and quote ID to this provider, not the previous
    # The Odds API adapter identity. Preserve all timestamp and line checks.
    for q in normalized["quotes"]:
        q["provider"] = "odds-api-io"
        ident = {k:v for k,v in q.items()
                 if k not in ("retrieved_at_utc","quote_id")}
        q["quote_id"] = "odds:" + hashlib.sha256(
            canonical_json(ident).encode("utf-8")
        ).hexdigest()[:24]
    skipped.extend(normalized["skipped"])
    available = {
        book:sum(q["book"]==book for q in normalized["quotes"])
        for book in BOOKS
    }
    return {
        "version":VERSION, "retrieved_at_utc":stamp,
        "bookmakers_requested":list(BOOKS),
        "eligible_nba_events":len(eligible),
        "mapped_nba_events":len(mapped["events"]),
        "quote_counts_by_bookmaker":available,
        "books_with_at_least_one_quote":[b for b in BOOKS if available[b]>0],
        "missing_bookmakers":[b for b in BOOKS if available[b]==0],
        "quotes":normalized["quotes"], "skipped":skipped,
    }


def fetch_five_book_snapshots() -> tuple[list[dict],list[dict],str]:
    events = _request("/events",{"sport":"basketball","league":"usa-nba",
                                  "status":"pending","limit":100})
    if not isinstance(events,list):
        raise ValueError("Provider event list must be an array")
    selected = [e for e in events if _is_nba(e) and
                e.get("status")=="pending" and _event_id(e)]
    responses = []
    # 10 events per batch, and 5 requested bookies in one response.
    for start in range(0,len(selected),10):
        batch=selected[start:start+10]
        result=_request("/odds/multi",{
            "eventIds":",".join(_event_id(e) for e in batch),
            "bookmakers":",".join(BOOKS),
            "markets":",".join(MARKETS)
        })
        if not isinstance(result,list):
            raise ValueError("Provider /odds/multi did not return an array")
        responses.extend(result)
    return events,responses,iso(datetime.now(timezone.utc))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--nba-db",type=Path,required=True)
    ap.add_argument("--ledger",type=Path,required=True)
    ap.add_argument("--report",type=Path,required=True)
    ap.add_argument("--fixture-json",type=Path,
                    help="Offline {events:[],odds:[]} payload; does not call API")
    ap.add_argument("--retrieved-at-utc",
                    help="Actual capture time required for offline fixture mode")
    args=ap.parse_args(argv)
    if args.fixture_json:
        if not args.retrieved_at_utc:
            ap.error("Offline replay requires original --retrieved-at-utc")
        payload=json.loads(args.fixture_json.read_text(encoding="utf-8"))
        events,odds = payload["events"],payload["odds"]
        stamp=args.retrieved_at_utc
    else:
        if args.retrieved_at_utc:
            ap.error("--retrieved-at-utc is only for offline replay")
        events,odds,stamp=fetch_five_book_snapshots()
    with sqlite3.connect(args.nba_db) as con:
        result=normalize_five_book_events(
            events,odds,con,retrieved_at_utc=stamp
        )
    saved=append_odds_ledger(args.ledger,result["quotes"])
    summary={k:v for k,v in result.items() if k!="quotes"}
    summary.update(saved)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(summary,indent=2,allow_nan=False)+"\n",
                           encoding="utf-8")
    print(json.dumps({
        "mapped_games":result["mapped_nba_events"],
        "quote_counts_by_bookmaker":result["quote_counts_by_bookmaker"],
        "new_quotes":saved["new_quotes"],
        "research_only":True,
    },sort_keys=True))


if __name__ == "__main__":
    main()
