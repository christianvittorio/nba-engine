"""Availability adjustment: shift the expected margin when rotation players are listed out.

Fitted on 2023-2025 walk-forward data (artifacts documented in BLUEPRINT.md section 6b): the margin a rating-only model
over- or under-predicted was regressed on (home missing value - away missing value), where
    missing value = sum over rotation players who did not play of  usual_minutes * max(0, quality_per_minute - 0.32)
and quality_per_minute is a shrunk Game-Score-per-minute from the player model. Coefficient: -0.307 points per unit,
same sign and similar size in every season (t between -6 and -10). Tested on 2025-26 without refitting: margin MAE 11.47 -> 11.27,
log loss 0.6003 -> 0.5932 (95% interval of the change includes zero), so it is stored as SEPARATE forecasts and scored alongside.
"""
from __future__ import annotations

BETA = -0.3067        # points of home-minus-away margin per unit of (home - away) missing value
Q_REPL = 0.32         # replacement-level Game Score per minute
Q_LEAGUE = 0.38       # league-average Game Score per minute (shrinkage target)
CAP = 10.0            # never move a game by more than this many points


def quality_per_min(st: dict) -> float:
    S = st["S"]
    pts = 2 * S["m2m"] + 3 * S["tpm"] + S["ftm"]
    fgm = S["m2m"] + S["tpm"]
    gs = (pts + 0.4 * fgm - 0.7 * S["fga"] - 0.4 * (S["fta"] - S["ftm"]) + 0.43 * S["reb"] + S["stl"]
          + 0.7 * S["ast"] + 0.7 * S["blk"] - S["tov"])
    return (gs + 100 * Q_LEAGUE) / (S["min"] + 100)


def missing_value(pm, team: str, out_ids) -> tuple[float, list]:
    """Only players in the team's recent rotation pool count (long-term absentees are already in the team's rating)."""
    pool = set(pm.pool(team))
    total, who = 0.0, []
    for pid in out_ids:
        if pid in pool and pid in pm.pl:
            v = (pm.ewm_min(pid) or 0.0) * max(0.0, quality_per_min(pm.pl[pid]) - Q_REPL)
            total += v
            who.append((pm.names.get(pid, str(pid)), round(v, 2)))
    return total, who


def make_injury_fn(pm, availability: dict):
    """Returns f(home, away) -> (shift_points, detail) using players ESPN lists as Out. None if no availability data."""
    teams = (availability or {}).get("teams") or {}
    if not teams:
        return None

    def out_ids(team):
        t = teams.get(team) or {}
        return [i["nba_id"] for i in t.get("injuries", []) if i.get("nba_id") is not None and "out" in str(i.get("status", "")).lower()]

    def fn(home: str, away: str):
        if home not in teams or away not in teams:
            return None
        mh, wh = missing_value(pm, home, out_ids(home))
        ma, wa = missing_value(pm, away, out_ids(away))
        shift = max(-CAP, min(CAP, BETA * (mh - ma)))
        return shift, {"home_missing_value": round(mh, 2), "away_missing_value": round(ma, 2), "home_out": wh, "away_out": wa,
                       "beta": BETA, "generated_utc": availability.get("generated_utc")}
    return fn


# ---------------------------------------------------------------------------------------------------------------------------------
# Availability INSIDE the simulation (v0.8). The margin shift above moves only the margin. This version converts missing rotation value
# into a change of each team's shooting efficiency (logit shift of 2- and 3-point make probability, no new random draws), so scores, totals,
# team box scores, ranges and win probability all respond. Coefficients: scripts/fit_availability.py -> artifacts/availability_fit.json.
import json as _json
import os as _os

_FIT = None


def _fit():
    global _FIT
    if _FIT is None:
        p = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "artifacts/availability_fit.json")
        _FIT = _json.load(open(p))
    return _FIT


CAP_PTS = 8.0


def availability_shifts(mv_home: float, mv_away: float) -> tuple[float, float, float, float]:
    """(home points shift, away points shift, home logit shift, away logit shift) from each team's missing value, relative to the typical amount."""
    f = _fit()
    a, b, m0, k = f["own_pts_per_unit"], f["opp_pts_per_unit"], f["typical_missing_value"], f["pts_per_logit"]
    ph = max(-CAP_PTS, min(CAP_PTS, a * (mv_home - m0) + b * (mv_away - m0)))
    pa = max(-CAP_PTS, min(CAP_PTS, a * (mv_away - m0) + b * (mv_home - m0)))
    return ph, pa, ph / k, pa / k


def make_avail_fn(pm, availability: dict):
    """Returns f(ug) -> (shift_home_logit, shift_away_logit, detail) from players ESPN lists as Out. None if no availability data."""
    teams = (availability or {}).get("teams") or {}
    if not teams:
        return None

    def out_ids(team):
        t = teams.get(team) or {}
        return [i["nba_id"] for i in t.get("injuries", []) if i.get("nba_id") is not None and "out" in str(i.get("status", "")).lower()]

    def fn(ug):
        if ug.home not in teams or ug.away not in teams:
            return None
        mh, wh = missing_value(pm, ug.home, out_ids(ug.home))
        ma, wa = missing_value(pm, ug.away, out_ids(ug.away))
        ph, pa, lh, la = availability_shifts(mh, ma)
        return lh, la, {"home_missing_value": round(mh, 2), "away_missing_value": round(ma, 2), "home_out": wh, "away_out": wa,
                        "home_pts_shift": round(ph, 2), "away_pts_shift": round(pa, 2), "generated_utc": availability.get("generated_utc")}
    return fn
