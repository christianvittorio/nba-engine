"""Licensed-provider-ready The Odds API v4 NBA ingestion, without auto wagers.

Live requests require THE_ODDS_API_KEY. JSON fixture mode makes no network
calls and must supply an explicit retrieval timestamp. No arbitrary team or
player fuzzy matching; unmapped events or props are skipped and audited.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from .contracts import iso, utc, canonical_json
from .market_value import _validate_quote

SPORT = "basketball_nba"
ODDS_URL = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"
EVENT_URL = f"https://api.the-odds-api.com/v4/sports/{SPORT}/events"
FEATURED = frozenset({"h2h", "spreads", "totals"})
PROPS = {"player_points": "pts", "player_rebounds": "reb",
         "player_assists": "ast", "player_threes": "fg3m"}
VERSION = "gpt-v2-odds-ingestion-0.1"


def fetch_live_odds(*, region="us", markets=("h2h", "spreads", "totals"),
                    event_id=None, timeout=15) -> list[dict]:
    """Fetch API data; never persist API keys, raw authenticated URLs or headers."""
    key = os.environ.get("THE_ODDS_API_KEY", "").strip()
    if not key:
        raise ValueError("THE_ODDS_API_KEY must be set for live API requests")
    if region not in ("us", "us2", "uk", "eu", "au"):
        raise ValueError("Unsupported odds region")
    allowed = FEATURED | set(PROPS)
    if not markets or not set(markets) <= allowed:
        raise ValueError("Unsupported market key")
    if not event_id and not set(markets) <= FEATURED:
        raise ValueError("Player props require --event-id and single-event endpoint")
    if event_id and not str(event_id).isalnum():
        raise ValueError("Provider event ID contains invalid characters")
    base = (f"{EVENT_URL}/{event_id}/odds" if event_id else ODDS_URL)
    query = urlencode({"apiKey": key, "regions": region,
                       "markets": ",".join(markets),
                       "oddsFormat": "decimal", "dateFormat": "iso"})
    try:
        with urlopen(Request(base + "?" + query,
                             headers={"Accept": "application/json"}),
                     timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as ex:
        # Never include the request URL, which contains the secret key.
        status = getattr(ex, "code", None)
        raise RuntimeError(f"Odds provider request failed (HTTP {status or 'network'})") from None
    if not isinstance(data, (dict, list)):
        raise ValueError("Unexpected provider odds payload type")
    return [data] if isinstance(data, dict) else data


def _canonical(value) -> str:
    return " ".join(str(value).casefold().split())


def _read_event_mapping(mappings: dict, event_id: str) -> dict | None:
    rows = mappings.get("events", {})
    if not isinstance(rows, dict):
        raise ValueError("events must be an object keyed by provider event ID")
    return rows.get(event_id)


def _price(value):
    try:
        v = float(value)
        if not 1 < v < 10001:
            return None
        return v
    except (TypeError, ValueError, OverflowError):
        return None


def _market_outcome(event: dict, market: dict, outcome: dict,
                    mapping: dict) -> dict | None:
    key = market["key"]
    home = event["home_team"]
    away = event["away_team"]
    name = str(outcome.get("name", ""))
    point = outcome.get("point")
    if key == "h2h":
        if name not in (home, away):
            return None
        return {"market_id": "game:moneyline", "market_type": "moneyline",
                "selection": "home" if name == home else "away",
                "line": None}
    if key == "spreads":
        if name not in (home, away) or point is None:
            return None
        line = float(point)
        home_line = line if name == home else -line
        return {"market_id": f"game:spread:home:{home_line:+g}",
                "market_type": "spread",
                "selection": "home" if name == home else "away",
                "line": line}
    if key == "totals":
        if name not in ("Over", "Under") or point is None:
            return None
        line = float(point)
        return {"market_id": f"game:total:{line:g}",
                "market_type": "total", "selection": name.lower(),
                "line": line}
    if key in PROPS:
        if name not in ("Over", "Under") or point is None:
            return None
        # The Odds API supplies player identity as the outcome description;
        # never invent a player ID from a name collision.
        player_name = str(outcome.get("description", ""))
        players = mapping.get("players", {})
        player_id = players.get(player_name)
        if not player_id:
            return None
        line = float(point)
        stat = PROPS[key]
        return {"market_id": f"player:{stat}:{player_id}:{line:g}",
                "market_type": "player_prop", "selection": name.lower(),
                "player_id": player_id, "line": line}
    return None


def normalize_provider_events(payload: list[dict], mappings: dict, *,
                              retrieved_at_utc: str) -> dict:
    """Resolve only explicitly mapped provider events to canonical NBA games."""
    retrieved = iso(retrieved_at_utc)
    if not isinstance(payload, list):
        raise ValueError("Expected a list of provider events")
    quotes, skipped = [], []
    for event in payload:
        event_id = str(event.get("id", ""))
        mapping = _read_event_mapping(mappings, event_id)
        if mapping is None:
            skipped.append({"provider_event_id": event_id,
                            "reason": "UNMAPPED_EVENT"})
            continue
        try:
            home, away = event["home_team"], event["away_team"]
            if home == away or not mapping.get("game_id"):
                raise ValueError("invalid team or canonical game identity")
            if (_canonical(home) != _canonical(mapping["home_team"])
                    or _canonical(away) != _canonical(mapping["away_team"])):
                raise ValueError("provider team names differ from explicit mapping")
            tip = iso(mapping["tip_utc"])
            provider_tip = iso(event["commence_time"])
            if abs((utc(tip)-utc(provider_tip)).total_seconds()) > 30*60:
                raise ValueError("tip time differs from canonical game by >30m")
            if utc(retrieved) >= min(utc(tip), utc(provider_tip)):
                raise ValueError("retrieved after earliest known scheduled tip")
            if not mapping.get("settlement_scope") == "full_game_including_ot":
                raise ValueError("unverified full-game including-OT market scope")
        except (KeyError, ValueError, TypeError) as ex:
            skipped.append({"provider_event_id": event_id,
                            "reason": "UNVERIFIED_EVENT_MAPPING",
                            "detail": str(ex)})
            continue
        for book in event.get("bookmakers", []):
            book_key = str(book.get("key", "")).strip()
            if not book_key:
                continue
            for market in book.get("markets", []):
                market_key = market.get("key")
                if market_key not in FEATURED | set(PROPS):
                    continue
                updated = market.get("last_update") or book.get("last_update")
                if not updated:
                    skipped.append({"provider_event_id": event_id,
                                    "book": book_key, "market": market_key,
                                    "reason": "MISSING_SOURCE_TIMESTAMP"})
                    continue
                try:
                    observed = iso(updated)
                    if utc(observed) > utc(retrieved):
                        raise ValueError("provider timestamp is in the future")
                    if utc(observed) >= min(utc(tip), utc(provider_tip)):
                        raise ValueError("provider odds updated after tip")
                except ValueError as ex:
                    skipped.append({"provider_event_id": event_id,
                                    "book": book_key, "market": market_key,
                                    "reason": "INVALID_SOURCE_TIMESTAMP",
                                    "detail": str(ex)})
                    continue
                for outcome in market.get("outcomes", []):
                    price = _price(outcome.get("price"))
                    if price is None:
                        skipped.append({"provider_event_id": event_id,
                                        "book": book_key, "market": market_key,
                                        "reason": "INVALID_PRICE"})
                        continue
                    try:
                        selection = _market_outcome(event, market, outcome, mapping)
                    except (ValueError, OverflowError, TypeError):
                        selection = None
                    if selection is None:
                        skipped.append({"provider_event_id": event_id,
                                        "book": book_key, "market": market_key,
                                        "reason": "UNRESOLVED_SELECTION_OR_PLAYER"})
                        continue
                    q = {
                        "game_id": mapping["game_id"], "tip_utc": tip,
                        "book": book_key, "provider": "the-odds-api",
                        "provider_event_id": event_id,
                        "provider_market_key": market_key,
                        "observed_at_utc": observed,
                        "retrieved_at_utc": retrieved,
                        "decimal_odds": price,
                        **selection,
                    }
                    try:
                        _validate_quote(q)
                    except (KeyError, ValueError) as ex:
                        skipped.append({"provider_event_id": event_id,
                                        "book": book_key, "market": market_key,
                                        "reason": "INVALID_NORMALIZED_QUOTE",
                                        "detail": str(ex)})
                        continue
                    identity = {k: v for k, v in q.items()
                                if k != "retrieved_at_utc"}
                    q["quote_id"] = "odds:" + hashlib.sha256(
                        canonical_json(identity).encode("utf-8")
                    ).hexdigest()[:24]
                    quotes.append(q)
    return {"version": VERSION, "retrieved_at_utc": retrieved,
            "quotes": quotes, "skipped": skipped}


def append_odds_ledger(path: Path, quotes: list[dict]) -> dict:
    """Append-only JSONL; byte-preserving on repeated provider snapshots."""
    prior = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            q = json.loads(line)
            qid = q["quote_id"]
            if qid in prior and prior[qid] != q:
                raise ValueError("Contradictory historical quote ID")
            prior[qid] = q
    additions, pending = [], {}
    for q in quotes:
        _validate_quote(q)
        if not str(q.get("quote_id", "")).strip():
            raise ValueError("quote_id missing")
        qid = q["quote_id"]
        if qid in prior:
            # Re-polling must not rewrite the original retrieval timestamp.
            if {k:v for k,v in prior[qid].items() if k != "retrieved_at_utc"} != {
                k:v for k,v in q.items() if k != "retrieved_at_utc"
            }:
                raise ValueError("Conflicting same-ID odds history")
            continue
        if qid in pending:
            if pending[qid] != q:
                raise ValueError("Conflicting duplicate in current batch")
            continue
        pending[qid] = q
        additions.append(q)
    if additions:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            for q in additions:
                f.write(json.dumps(q, sort_keys=True, allow_nan=False)+"\n")
    return {"previous_quotes": len(prior), "new_quotes": len(additions),
            "total_quotes": len(prior)+len(additions), "path": str(path)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event-map", type=Path, required=True,
                        help="Explicit provider-ID to NBA-ID mapping with confirmed teams and tip")
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--source-json", type=Path,
                        help="Offline source API response; no network")
    parser.add_argument("--retrieved-at-utc",
                        help="Required time evidence for offline captured data")
    parser.add_argument("--region", default="us")
    parser.add_argument("--markets", default="h2h,spreads,totals")
    parser.add_argument("--event-id", default="")
    args = parser.parse_args(argv)
    mapping = json.loads(args.event_map.read_text(encoding="utf-8"))
    if args.source_json:
        if not args.retrieved_at_utc:
            parser.error("--retrieved-at-utc required with --source-json")
        data = json.loads(args.source_json.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        payload = [data] if isinstance(data, dict) else data
        stamp = args.retrieved_at_utc
    else:
        if args.retrieved_at_utc:
            parser.error("--retrieved-at-utc is only for saved source data")
        payload = fetch_live_odds(region=args.region,
                                  markets=tuple(args.markets.split(",")),
                                  event_id=args.event_id or None)
        stamp = iso(datetime.now(timezone.utc))
    result = normalize_provider_events(payload, mapping, retrieved_at_utc=stamp)
    saved = append_odds_ledger(args.ledger, result["quotes"])
    report = {k:v for k,v in result.items() if k != "quotes"}
    report.update(saved)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n",
                           encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="skipped"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
