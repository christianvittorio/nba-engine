"""Explicit sensitivity analysis for pace, efficiency, home court and lineups.

These ranges are illustrative scenario variations until validated from the
historical distributions. Neither their sizes nor probabilities are asserted
as forecasts.
"""
from __future__ import annotations
from dataclasses import replace

from .players import PlayerProjection
from .simulation import Matchup,simulate_game

def sensitivity_grid(match:Matchup,home:list[PlayerProjection],
                     away:list[PlayerProjection],*,n:int=1000,seed:int=20261121,
                     possession_delta:float=5.0,off_rating_delta:float=4.0)->dict:
    scenarios=[
        ("baseline",match),
        ("slower_pace",replace(match,expected_possessions=max(70,match.expected_possessions-possession_delta))),
        ("faster_pace",replace(match,expected_possessions=min(130,match.expected_possessions+possession_delta))),
        ("home_offense_down",replace(match,home=replace(
            match.home,offense_rating=max(65,match.home.offense_rating-off_rating_delta)))),
        ("home_offense_up",replace(match,home=replace(
            match.home,offense_rating=min(160,match.home.offense_rating+off_rating_delta)))),
        ("neutral_court",replace(match,home_court_points=0.0)),
    ]
    out={}
    for label,scenario in scenarios:
        report=simulate_game(scenario,home,away,n=n,seed=seed)
        out[label]={
            "home_win_probability":report["home_win_probability"],
            "home_expected_score":report["expected_home_score"],
            "away_expected_score":report["expected_away_score"],
            "total_mean":report["total"]["mean"],
            "mc_standard_error":report["mc_sampling_error"]["home_win_probability"],
        }
    base=out["baseline"]
    for label,row in out.items():
        row["delta_home_win_vs_base"]=round(
            row["home_win_probability"]-base["home_win_probability"],5)
        row["delta_total_vs_base"]=round(row["total_mean"]-base["total_mean"],3)
    return {
        "simulation_count_each":n,
        "seed":seed,
        "assumptions":{
            "possession_delta":possession_delta,
            "off_rating_delta":off_rating_delta,
            "scenario_probabilities":None
        },
        "scenarios":out,
        "warning":"Sensitivity is conditional on assumed input shifts; it does not validate the model."
    }
