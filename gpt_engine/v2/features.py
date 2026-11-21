"""Leakage-safe team matchup features from historical *completed* game rows.

Works with data_foundation/artifacts/teams/{season}.csv.gz.
No current-date box scores, retroactive injuries, future games or market odds
are read. Historical corrected NBA stats can support retrospective evaluation,
but are labeled as a reconstructed dataset (not real as-of-time snapshots).
"""
from __future__ import annotations

from datetime import date
import math
from typing import Any

import numpy as np
import pandas as pd

from .contracts import GameContext, FeatureSnapshot, iso, utc

VERSION = "feature-v2.1"
BASIC = ("off_rating", "def_rating", "net_rating", "pace", "poss",
         "efg_pct", "ts_pct", "three_point_rate", "fta_rate", "ast",
         "tov", "oreb", "dreb", "opp_fg3a", "opp_fg3m", "opp_ast",
         "opp_efg_pct", "tm_tov_pct", "oreb_pct", "dreb_pct")

def _number(value: Any, fallback: float) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return fallback
    return v if math.isfinite(v) else fallback

def _weighted_prior(value: float | None, n: int, league: float,
                    strength: int = 12) -> tuple[float, float]:
    n = max(0,n)
    raw = league if value is None or not math.isfinite(value) else value
    w = n / (n + strength)
    return (w * raw + (1-w)*league, w)

def _hist_group(frame: pd.DataFrame, season: int, team_id: str,
                prior_day: str) -> pd.DataFrame:
    return frame[
        (frame["team_id"].astype(str) == str(team_id)) &
        (frame["game_date"].astype(str).str[:10] < prior_day) &
        (pd.to_numeric(frame["season"], errors="coerce") <= season) &
        (frame["game_type"].astype(str) == "regular_season")
    ].sort_values(["game_date","game_id"])

def _safe_mean(data: pd.DataFrame, key: str, default: float) -> float:
    if key not in data or data.empty:
        return default
    col = pd.to_numeric(data[key], errors="coerce")
    m = col.mean()
    return _number(m, default)

def _robust_season_mean(data: pd.DataFrame, key: str, season: int,
                        prior_day: str, fallback: float) -> float:
    """Use past three seasons, exponentially downweight older years."""
    z = data[(data.game_date.astype(str).str[:10] < prior_day) &
             (data.season <= season) & (data.season >= season-3)]
    if z.empty or key not in z:
        return fallback
    values = pd.to_numeric(z[key], errors="coerce")
    decay = np.power(0.55, season-z.season.to_numpy(dtype=float))
    good = np.isfinite(values.to_numpy(dtype=float))
    if not np.any(good):
        return fallback
    return float(np.average(values.to_numpy(dtype=float)[good],
                            weights=decay[good]))

def _team_vector(hist: pd.DataFrame, league: dict[str,float], season: int,
                 prior_day: str) -> dict:
    n_total = len(hist)
    current = hist[hist.season == season]
    n_season = len(current)
    last = hist.tail(20)
    out = {"n_season":n_season,"n_total":n_total,
           "short_sample":int(n_season<10)}
    for key in BASIC:
        prior = league[key]
        multi = _robust_season_mean(hist,key,season,prior_day,prior)
        multi, _ = _weighted_prior(multi,len(hist),prior,20)
        out["multi_"+key] = round(multi,5)
        season_avg, w = _weighted_prior(
            _safe_mean(current,key,float("nan")) if not current.empty else None,
            n_season,multi,12)
        out["season_"+key] = round(season_avg,5)
        for window in (5,10,20):
            recent = hist.tail(window)
            raw = _safe_mean(recent,key,float("nan"))
            adjusted,_ = _weighted_prior(raw,len(recent),season_avg,
                                         max(4,12-window//3))
            out[f"rolling{window}_{key}"] = round(adjusted,5)
        out[f"season_shrink_weight_{key}"] = round(w,4)
    if n_total:
        last_date = date.fromisoformat(str(hist.iloc[-1]["game_date"])[:10])
        gap=(date.fromisoformat(prior_day)-last_date).days
        out["rest_days"] = max(0,gap-1)
        out["b2b"] = int(gap == 1)
        out["three_in_four"] = int(
            (date.fromisoformat(prior_day) -
             date.fromisoformat(str(hist.iloc[-3]["game_date"])[:10])).days <= 4
        ) if n_total >= 3 else 0
    else:
        out.update(rest_days=None,b2b=None,three_in_four=None)
    out["expected_pace"] = out["rolling20_pace"]
    out["effective_games"] = min(20,n_total)
    return out

def build_team_features(team_games: pd.DataFrame, game: GameContext,
                        cutoff_utc: str, *,
                        coach_history: list[dict] | None = None,
                        availability: list[dict] | None = None,
                        lineup: list[dict] | None = None) -> FeatureSnapshot:
    cutoff = iso(cutoff_utc)
    if utc(cutoff) >= utc(game.tip_utc):
        raise ValueError("Features require an information cutoff before tip")
    required = {"season","game_id","game_date","team_id","game_type",
                "off_rating","def_rating","pace","efg_pct"}
    missing = required - set(team_games.columns)
    if missing:
        raise ValueError(f"Missing critical team-game fields: {sorted(missing)}")
    df = team_games.copy()
    df["game_date"] = df.game_date.astype(str).str[:10]
    df["season"] = pd.to_numeric(df.season)
    # Day gate is stricter than timestamp: no current-date or later result,
    # even for a game that tipped earlier on the same Eastern day.
    prior = df[(df.game_date < game.game_date_eastern) &
               (df.season <= game.season) &
               (df.game_type == "regular_season")].copy()
    if prior.empty:
        raise ValueError("No verified prior-game history; refuse prediction")
    # Optional historical tip_utc protects from malformed source dates.
    if "tip_utc" in prior:
        verified = prior.tip_utc.map(lambda x:
            pd.isna(x) or (utc(str(x)) < utc(cutoff)))
        if not bool(verified.all()):
            raise ValueError("Historical feature set contains future tip times")
    global_prior = {}
    for key in BASIC:
        global_prior[key] = _safe_mean(prior,key,{
            "off_rating":114.0,"def_rating":114.0,"net_rating":0.0,
            "pace":99.0,"poss":100.0,"efg_pct":0.54,
            "ts_pct":0.57,"three_point_rate":0.38,"fta_rate":0.24,
            "ast":25.0,"tov":13.0,"oreb":10.0,"dreb":33.0,
            "opp_fg3a":34.0,"opp_fg3m":12.0,"opp_ast":25.0,
            "opp_efg_pct":0.54,"tm_tov_pct":0.13,"oreb_pct":0.25,
            "dreb_pct":0.75
        }[key])
    h=_hist_group(prior,game.season,game.home_team_id,game.game_date_eastern)
    a=_hist_group(prior,game.season,game.away_team_id,game.game_date_eastern)
    home=_team_vector(h,global_prior,game.season,game.game_date_eastern)
    away=_team_vector(a,global_prior,game.season,game.game_date_eastern)

    # Opponent-adjusted efficiency: subtract the strength of the opponents
    # actually faced in completed games, not a future or season-end rating.
    def opp_adjusted(team_hist: pd.DataFrame, baseline: dict) -> float:
        if team_hist.empty or "opp_team_id" not in team_hist:
            return baseline["rolling20_off_rating"]
        opponents = []
        for opp in team_hist.tail(20).opp_team_id.astype(str).tolist():
            oh = _hist_group(prior, game.season, opp,game.game_date_eastern)
            opponents.append(_weighted_prior(
                _safe_mean(oh,"def_rating",float("nan")),len(oh),
                global_prior["def_rating"],12)[0])
        # If team faced strong (low-def-rating) opponents, adjust upward.
        return baseline["rolling20_off_rating"] + (
            global_prior["def_rating"]-float(np.mean(opponents))
        )
    home["opponent_adjusted_off_rating"] = round(opp_adjusted(h,home),4)
    away["opponent_adjusted_off_rating"] = round(opp_adjusted(a,away),4)

    def strength_of_schedule(hist: pd.DataFrame) -> float:
        if hist.empty or "opp_team_id" not in hist:
            return 0.0
        vals=[]
        for opponent in hist.tail(20).opp_team_id.astype(str).tolist():
            z=_hist_group(prior,game.season,opponent,game.game_date_eastern)
            vals.append(_weighted_prior(_safe_mean(z,"net_rating",float("nan")),
                                        len(z),0.0,12)[0])
        return float(np.mean(vals)) if vals else 0.0
    home["strength_of_schedule"] = round(strength_of_schedule(h),4)
    away["strength_of_schedule"] = round(strength_of_schedule(a),4)

    # These are transparent heuristics and should be learned on validation later.
    pace=(home["rolling20_pace"]+away["rolling20_pace"])/2
    home_off=home["opponent_adjusted_off_rating"]
    away_off=away["opponent_adjusted_off_rating"]
    home_def=home["rolling20_def_rating"]
    away_def=away["rolling20_def_rating"]
    # Efficiency rated per 100 possessions.
    exp_h_pp100=global_prior["off_rating"] + .5*(home_off-global_prior["off_rating"]) \
           + .5*(away_def-global_prior["def_rating"])
    exp_a_pp100=global_prior["off_rating"] + .5*(away_off-global_prior["off_rating"]) \
           + .5*(home_def-global_prior["def_rating"])
    home_adv=0.0 if game.neutral_site else 2.0
    mu_h=(pace/100)*exp_h_pp100+home_adv/2
    mu_a=(pace/100)*exp_a_pp100-home_adv/2

    def guard_timestamp(rows: list[dict] | None, keys: tuple[str,...]):
        for row in rows or []:
            for field in keys:
                if row.get(field) is not None and utc(row[field])>utc(cutoff):
                    raise ValueError(f"Leaked post-cutoff {field} in a feature record")
    guard_timestamp(availability,("report_utc","retrieved_at_utc"))
    guard_timestamp(lineup,("confirmation_utc","retrieved_at_utc"))
    guard_timestamp(coach_history,("retrieved_at_utc",))
    flags=["historical_corrected_archive_not_proof_of_original_asof"]
    missingness={
        "home_prior_games":len(h),"away_prior_games":len(a),
        "lineups_unknown":not bool(lineup),
        "availability_unknown":not bool(availability),
        "coach_tactics_unknown":True,
        "roster_change_dates_unknown":not bool(coach_history),
    }
    if len(h)<8 or len(a)<8:
        flags.append("small_sample_shrunken_to_league_prior")
    if not availability:
        flags.append("availability_unknown_do_not_price_props")
    if not lineup:
        flags.append("lineups_unconfirmed")
    features={
        "home":home,"away":away,"league":global_prior,
        "expected_possessions":round(pace,3),
        "home_court_points":home_adv,
        "baseline_home_score":round(mu_h,3),
        "baseline_away_score":round(mu_a,3),
        "baseline_margin":round(mu_h-mu_a,3),
        "baseline_total":round(mu_h+mu_a,3),
        "availability":availability or [],
        "lineup":lineup or [],
        "coach_evidence":coach_history or [],
        "source_game_ids_max_date":str(prior.game_date.max()),
        "data_class":"retrospectively_reconstructed_from_completed_games",
    }
    return FeatureSnapshot(game.game_id,cutoff,VERSION,features,missingness,
                           ("nba_stats_archive",),tuple(flags))

def flatten_team_features(snap: FeatureSnapshot) -> dict[str,float]:
    f=snap.features
    out={
      "home_court_points":float(f["home_court_points"]),
      "expected_possessions":float(f["expected_possessions"]),
    }
    for group in ("home","away"):
        for key,value in f[group].items():
            if isinstance(value,(float,int,np.number)) and math.isfinite(float(value)):
                out[group+"__"+key]=float(value)
    return out
