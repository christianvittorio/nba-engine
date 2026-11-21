"""Explicit, *conditional* injury/lineup forecasts. No made-up scenario odds."""
from __future__ import annotations

from dataclasses import replace
from typing import Any

from .players import PlayerProjection, allocate_minutes, conditional_rotation
from .simulation import Matchup, TeamSettings, simulate_game

def _expected_points(players:list[PlayerProjection]):
    return sum(p.minutes*p.rates_per_min.get("pts",0) for p in players)

def _adjusted_team(base:TeamSettings, old:list[PlayerProjection],
                   revised:list[PlayerProjection], possessions:float)->TeamSettings:
    delta=_expected_points(revised)-_expected_points(old)
    # Conservative point-equivalent adjustment; a fitted replacement-value
    # estimate must eventually replace this heuristic.
    change=max(-10.0,min(10.0,50.0*delta/max(70.0,possessions)))
    return replace(base,offense_rating=float(max(70,min(155,base.offense_rating+change))))

def conditional_scenarios(match:Matchup, home:list[PlayerProjection],
                          away:list[PlayerProjection],
                          definitions:list[dict[str,Any]],
                          *, n:int=1000,seed:int=20261121) -> list[dict]:
    """Each definition is {label, available:{player_id:status}, minutes:{...}}.

    The same seed and simulation count are used for all scenarios to reduce
    side-by-side Monte Carlo noise. Scenario probabilities remain None.
    """
    if not definitions:
        raise ValueError("At least one scenario required")
    baseline_h=allocate_minutes(home)
    baseline_a=allocate_minutes(away)
    result=[]
    labels=set()
    for spec in definitions:
        label=str(spec.get("label","")).strip()
        if not label or label in labels:
            raise ValueError("Distinct non-empty scenario labels required")
        labels.add(label)
        statuses=spec.get("availability",{})
        minutes=spec.get("minutes",{})
        h=conditional_rotation(baseline_h,statuses,minutes_overrides=minutes)
        a=conditional_rotation(baseline_a,statuses,minutes_overrides=minutes)
        new_match=replace(match,
            home=_adjusted_team(match.home,baseline_h,h,match.expected_possessions),
            away=_adjusted_team(match.away,baseline_a,a,match.expected_possessions))
        sim=simulate_game(new_match,h,a,n=n,seed=seed)
        result.append({
            "label":label,
            "condition":statuses,
            "minutes_overrides":minutes,
            "probability":None,
            "source_timestamp":spec.get("source_timestamp"),
            "source_id":spec.get("source_id"),
            "scenario_adjusted_home_off_rating":round(new_match.home.offense_rating,3),
            "scenario_adjusted_away_off_rating":round(new_match.away.offense_rating,3),
            "home_win_probability":sim["home_win_probability"],
            "expected_home_score":sim["expected_home_score"],
            "expected_away_score":sim["expected_away_score"],
            "player_statistics":sim["player_statistics"],
            "warnings":sim["warnings"]+[
                "Injury replacement impact is a research heuristic; not fit on historical substitutions.",
                "These are CONDITIONAL projections, not outcome-weighted estimates.",
            ],
        })
    return result
