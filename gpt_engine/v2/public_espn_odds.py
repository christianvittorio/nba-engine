"""No-login NBA odds research capture from ESPN's public scoreboard.

Research-only, noncommercial, at most two day-scoped requests per run.
ESPN's feed is undocumented and may offer only a single named bookmaker
or no prices; no five-book completeness claim. Source prices are not
redistributed to public GitHub. Failure is visible and fail-closed.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

from .contracts import canonical_json, iso, utc
from .odds_ingest import append_odds_ledger
from .odds_map import abbreviation, map_provider_events
from .market_value import _validate_quote

URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
VERSION = "gpt-v2-public-scoreboard-odds-research-0.1"
EASTERN = ZoneInfo("America/New_York")


def american_to_decimal(value) -> float | None:
    """Only signed American odds are accepted, not fake default prices."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value,str):
        value=value.strip().replace(",","")
        if value.casefold() in ("even","evens","ev"):
            return 2.0
        if not re.fullmatch(r"[+-]?\d+(?:\.0+)?",value):
            return None
    try:
        number=float(value)
    except (ValueError,TypeError,OverflowError):
        return None
    if number == 0 or not 100 <= abs(number) < 10000:
        return None
    return round(1 + (number/100 if number>0 else 100/-number), 8)


def fetch_public_scoreboard(day: str, *, timeout: int = 15) -> tuple[dict,str]:
    """One unauthenticated request; record actual completion timestamp."""
    if not re.fullmatch(r"\d{8}",day):
        raise ValueError("ESPN date must be YYYYMMDD")
    url=URL+"?"+urlencode({"dates":day,"limit":100})
    try:
        request=Request(url,headers={
            "Accept":"application/json",
            "User-Agent":"nba-engine-research/0.1 (low-frequency, read-only)",
        })
        with urlopen(request,timeout=timeout) as response:
            data=json.loads(response.read().decode("utf-8"))
    except (HTTPError,URLError,TimeoutError) as ex:
        status=getattr(ex,"code","network")
        raise RuntimeError(
            f"Public NBA scoreboard unavailable (HTTP {status}); "
            "no sportsbook odds inferred"
        ) from None
    if not isinstance(data,dict) or not isinstance(data.get("events"),list):
        raise ValueError("Unexpected public scoreboard format")
    return data,iso(datetime.now(timezone.utc))


def _team_info(comp: dict) -> tuple[str,str] | None:
    home=away=None
    for side in comp.get("competitors",[]):
        name=(side.get("team") or {}).get("displayName")
        if not name:
            continue
        if side.get("homeAway")=="home":
            home=name
        elif side.get("homeAway")=="away":
            away=name
    return (home,away) if home and away and home!=away else None


def _favorite_home_line(price: dict, home: str, away: str) -> float | None:
    """Infer handicap sign ONLY from a verified favorite or exact details."""
    h=price.get("homeTeamOdds") or {}
    a=price.get("awayTeamOdds") or {}
    if h.get("spread") is not None and a.get("spread") is not None:
        try:
            hs=float(h["spread"]);avs=float(a["spread"])
            if 0 < abs(hs)<100 and abs(hs+avs)<1e-8:
                return hs
        except (ValueError,TypeError,OverflowError):
            return None
    try:
        raw=abs(float(price["spread"]))
    except (KeyError,TypeError,ValueError,OverflowError):
        return None
    if not 0 < raw < 100:
        return None
    if h.get("favorite") is True and a.get("favorite") is False:
        return -raw
    if a.get("favorite") is True and h.get("favorite") is False:
        return raw
    # The published details are sometimes "BOS -6.5"; this establishes
    # the favorite orientation without guessing from a market mean.
    details=str(price.get("details","")).strip().upper()
    match=re.fullmatch(r"([A-Z]{2,4})\s+(-?\d+(?:\.\d+)?)",details)
    if match and abs(abs(float(match.group(2)))-raw)<1e-8:
        code=match.group(1)
        if code==abbreviation(home):
            return -raw if float(match.group(2))<0 else raw
        if code==abbreviation(away):
            return raw if float(match.group(2))<0 else -raw
    return None


def normalize_public_scoreboards(
    responses: list[tuple[dict,str]], connection: sqlite3.Connection
) -> dict:
    """Strict explicit scoreboard event, provider and pretip capture evidence."""
    events,proposed,skipped=[],[],[]
    for payload,captured_raw in responses:
        captured=iso(captured_raw)
        if not isinstance(payload,dict) or not isinstance(payload.get("events"),list):
            raise ValueError("Unexpected scoreboard payload")
        for e in payload["events"]:
            if not isinstance(e,dict) or not e.get("id") or not e.get("date"):
                continue
            comps=e.get("competitions") or []
            if len(comps)!=1 or not isinstance(comps[0],dict):
                skipped.append({"event":str(e.get("id")),"reason":"AMBIGUOUS_COMPETITION"})
                continue
            comp=comps[0]
            identity=_team_info(comp)
            if identity is None:
                skipped.append({"event":str(e["id"]),"reason":"UNKNOWN_HOME_AWAY"})
                continue
            home,away=identity
            status=(e.get("status") or {}).get("type") or {}
            if status.get("state")!="pre" or utc(e["date"])<=utc(captured):
                skipped.append({"event":str(e["id"]),"reason":"NOT_PREGAME"})
                continue
            event_id=str(e["id"])
            events.append({"id":event_id,"home_team":home,
                           "away_team":away,"commence_time":e["date"]})
            raw_odds=comp.get("odds") or []
            if isinstance(raw_odds,dict):
                raw_odds=[raw_odds]
            for data in raw_odds:
                if not isinstance(data,dict):
                    continue
                provider=data.get("provider") or {}
                book=(provider.get("name") or provider.get("displayName")
                      if isinstance(provider,dict) else "")
                if not book or not str(book).strip():
                    skipped.append({"event":event_id,"reason":"UNNAMED_BOOKMAKER"})
                    continue
                source_update=data.get("lastModified") or data.get("lastUpdate")
                if source_update:
                    try:
                        if utc(source_update)>utc(captured):
                            raise ValueError()
                    except (ValueError,TypeError):
                        skipped.append({"event":event_id,"book":str(book),
                                        "reason":"INVALID_BOOK_TIMESTAMP"})
                        continue
                h=data.get("homeTeamOdds") or {}
                a=data.get("awayTeamOdds") or {}
                if not isinstance(h,dict) or not isinstance(a,dict):
                    continue
                proposed.append((event_id,captured,source_update,
                                 str(book).strip(),data,home,away))

    # One-to-one official team/time mapping (not date alone).
    mapped=map_provider_events(events,connection)
    skipped.extend(mapped["skipped"])
    output=[]
    for eid,captured,source_update,book,data,home,away in proposed:
        target=mapped["events"].get(eid)
        if target is None:
            continue
        tip=target["tip_utc"]
        h=data["homeTeamOdds"];a=data["awayTeamOdds"]
        groups=[]
        hml=american_to_decimal(h.get("moneyLine"))
        aml=american_to_decimal(a.get("moneyLine"))
        if hml is not None and aml is not None:
            groups.append(("game:moneyline","moneyline",None,[
                ("home",None,hml),("away",None,aml)
            ]))
        hspread=american_to_decimal(h.get("spreadOdds"))
        aspread=american_to_decimal(a.get("spreadOdds"))
        home_line=_favorite_home_line(data,home,away)
        if home_line is not None and hspread is not None and aspread is not None:
            groups.append((f"game:spread:home:{home_line:+g}","spread",home_line,[
                ("home",home_line,hspread),("away",-home_line,aspread)
            ]))
        try:
            total=float(data["overUnder"])
        except (KeyError,TypeError,ValueError,OverflowError):
            total=None
        over=american_to_decimal(data.get("overOdds"))
        under=american_to_decimal(data.get("underOdds"))
        if total is not None and 100<total<400 and over is not None and under is not None:
            groups.append((f"game:total:{total:g}","total",total,[
                ("over",total,over),("under",total,under)
            ]))
        if not groups:
            skipped.append({"event":eid,"book":book,"reason":"NO_COMPLETE_PRICED_MARKET"})
        for market_id,kind,_,selections in groups:
            for selection,line,decimal in selections:
                q={
                    "game_id":target["game_id"], "tip_utc":tip,
                    "provider":"espn-public-scoreboard",
                    "provider_event_id":eid,"book":book,
                    "market_id":market_id,"market_type":kind,
                    "selection":selection,"line":line,
                    "decimal_odds":decimal,
                    # This is the time WE directly observed the quote.
                    # It is not a claim about the provider's update time.
                    "observed_at_utc":captured,
                    "retrieved_at_utc":captured,
                    "provider_last_modified_utc":(
                        iso(source_update) if source_update else None
                    ),
                    "timestamp_quality":(
                        "retrieval_observed;source_modified_known"
                        if source_update else
                        "retrieval_observed;source_modified_unknown"
                    ),
                    "usage":"personal_research_only",
                }
                _validate_quote(q)
                unique={k:v for k,v in q.items() if k!="retrieved_at_utc"}
                q["quote_id"]="odds:"+hashlib.sha256(
                    canonical_json(unique).encode("utf-8")
                ).hexdigest()[:24]
                output.append(q)
    return {
        "version":VERSION,"research_only":True,"requires_api_key":False,
        "verified_bookmakers":sorted({x["book"] for x in output}),
        "mapped_games":len(mapped["events"]),
        "quotes":output,"skipped":skipped,
        "attribution":{"provider":"ESPN public scoreboard",
                       "url":"https://www.espn.com/nba/scoreboard"},
        "limitations":[
            "Undocumented public feed; access and available books can change.",
            "Usually a single ESPN-named bookmaker, not five guaranteed books.",
            "Only complete markets with actual odds are recorded.",
            "Source-side update timestamp is optional; captured_at is our observation.",
            "Raw odds are kept off public GitHub; no commercial redistribution.",
        ]
    }


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--nba-db",type=Path,required=True)
    parser.add_argument("--ledger",type=Path,required=True)
    parser.add_argument("--report",type=Path,required=True)
    parser.add_argument("--date",default="",
                        help="Optional one US Eastern day YYYY-MM-DD")
    parser.add_argument("--source-json",type=Path,
                        help="Offline fixture: one raw scoreboard response")
    parser.add_argument("--retrieved-at-utc",
                        help="Actual capture time for offline fixture")
    parser.add_argument("--strict-network",action="store_true")
    args=parser.parse_args(argv)
    if args.source_json:
        if not args.retrieved_at_utc:
            parser.error("Offline fixture requires original --retrieved-at-utc")
        payload=json.loads(args.source_json.read_text(encoding="utf-8"))
        responses=[(payload,args.retrieved_at_utc)]
    else:
        if args.retrieved_at_utc:
            parser.error("--retrieved-at-utc applies only to offline mode")
        if args.date:
            day=datetime.strptime(args.date,"%Y-%m-%d").date()
            dates=[day]
        else:
            day=datetime.now(EASTERN).date()
            dates=[day,day+timedelta(days=1)]
        responses=[]
        errors=[]
        for day in dates[:2]:
            try:
                responses.append(fetch_public_scoreboard(day.strftime("%Y%m%d")))
            except (RuntimeError,ValueError) as ex:
                errors.append(str(ex))
        if errors and args.strict_network:
            raise RuntimeError("; ".join(errors))
    with sqlite3.connect(args.nba_db) as con:
        report=normalize_public_scoreboards(responses,con)
    if not args.source_json:
        report["network_errors"]=errors
    saved=append_odds_ledger(args.ledger,report["quotes"])
    summary={k:v for k,v in report.items() if k!="quotes"}
    summary.update(saved)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(summary,indent=2,allow_nan=False)+"\n",
                           encoding="utf-8")
    print(json.dumps({
        "no_login":True,"no_payment":True,
        "mapped_games":summary["mapped_games"],
        "captured_quotes":len(report["quotes"]),
        "bookmakers":summary["verified_bookmakers"],
        "network_errors":summary.get("network_errors",[]),
    },sort_keys=True))


if __name__=="__main__":
    main()
