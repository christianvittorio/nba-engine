"""Line-specific research probabilities from frozen exact Monte Carlo histograms.

Unlike projecting just a mean or 80% interval, an empirical PMF provides
win/loss/push mass for the EXACT offered line. This is still uncalibrated.
"""
from __future__ import annotations

from .market_value import _validate_quote
from .odds_ingest import PROPS

VERSION = "gpt-v2-exact-line-simulation-probabilities-0.1"


def _validated_counts(hist: dict, n: int) -> dict[int,int]:
    if not isinstance(hist, dict) or not hist:
        raise ValueError("Missing discrete simulation histogram")
    parsed = {}
    for key, count in hist.items():
        if isinstance(count,bool) or not isinstance(count,int) or count < 0:
            raise ValueError("Invalid discrete simulation histogram count")
        try:
            value = int(str(key))
        except (TypeError,ValueError) as ex:
            raise ValueError("Histogram outcome must be an integer") from ex
        if str(value) != str(key) or value in parsed:
            raise ValueError("Duplicate or noncanonical histogram outcome")
        parsed[value] = count
    if sum(parsed.values()) != n:
        raise ValueError("Histogram sample count does not reconcile")
    return parsed


def exact_line_probabilities(quote: dict, doc: dict) -> dict | None:
    """Return line-specific raw probability or None if no frozen PMF exists."""
    q = _validate_quote(quote)
    sim = doc["result"]
    data = sim.get("market_distributions")
    if not data:
        return None
    if data.get("calibration_status") != "uncalibrated":
        raise ValueError("Unexpected market histogram calibration label")
    if data.get("settlement_scope") != "full_game_including_overtime":
        raise ValueError("Incompatible market settlement scope")
    n = data.get("sample_count")
    if isinstance(n,bool) or not isinstance(n,int) or n<50:
        raise ValueError("Invalid market distribution sample size")
    if n != sim["simulation_count"]:
        raise ValueError("Market distribution does not match frozen simulation")
    if q["game_id"] != doc["game_id"] or q["tip_utc"] != doc["tip_utc"]:
        raise ValueError("Market and frozen game identities disagree")
    kind = q["market_type"]
    if kind == "moneyline":
        return None  # Home/away probability already saved in the first-issue result
    if kind == "spread":
        hist = data["home_margin_counts"]
        def result(v):
            return (v + q["line"] if q["selection"] == "home"
                    else -v + q["line"])
    elif kind == "total":
        hist = data["game_total_counts"]
        def result(v):
            delta = v - q["line"]
            return delta if q["selection"] == "over" else -delta
    elif kind == "player_prop":
        pid = q.get("player_id")
        stats = sim.get("player_statistics",{}).get(pid)
        if not stats or stats.get("availability") == "out":
            return None
        key = q.get("provider_market_key")
        stat = PROPS.get(key) if key else None
        if stat is None:
            parts = str(q["market_id"]).split(":")
            stat = parts[1] if len(parts)>3 and parts[0]=="player" else None
        if stat not in ("pts","reb","ast","fg3m"):
            return None
        hist = data.get("player_counts",{}).get(pid,{}).get(stat)
        if not hist:
            return None
        def result(v):
            delta = v - q["line"]
            return delta if q["selection"] == "over" else -delta
    else:
        return None
    counts = _validated_counts(hist,n)
    wins = sum(c for v,c in counts.items() if result(v) > 1e-9)
    pushes = sum(c for v,c in counts.items() if abs(result(v)) <= 1e-9)
    if wins+pushes>n:
        raise AssertionError("Win/push histogram accounting invalid")
    extra = {}
    if kind == "player_prop":
        extra["availability_note"] = (
            "Conditional on estimated minutes/availability; lineup unconfirmed"
            if stats.get("availability") != "confirmed_available" else
            "Player modeled available; lineup still needs confirmation"
        )
    return {
        "game_id":q["game_id"], "market_id":q["market_id"],
        "market_type":kind, "selection":q["selection"], "line":q["line"],
        "player_id":q.get("player_id"),
        "tip_utc":doc["tip_utc"], "asof_utc":doc["cutoff_utc"],
        "model_version":doc["model_version"],
        "calibration_status":"uncalibrated",
        "probability":wins/n, "push_probability":pushes/n,
        "simulation_count":n,
        "win_count":wins, "push_count":pushes,
        "distribution_version":VERSION,
        **extra,
    }
