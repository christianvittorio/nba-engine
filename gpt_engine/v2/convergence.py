"""Sampling-noise convergence diagnostic: 1,000 / 5,000 / 10,000.

A deterministic laboratory fixture, not historical NBA calibration.
  python -m gpt_engine.v2.convergence
"""
from __future__ import annotations
import json
from .players import PlayerProjection,allocate_minutes
from .simulation import TeamSettings,Matchup,check_convergence

def example_roster(team:str):
    minutes=(40,37,35,32,29,26,23,18)
    out=[]
    for i,m in enumerate(minutes):
        rate={"pts":.58 if i==0 else .40,"reb":.14,"ast":.11,"stl":.025,
              "blk":.015,"tov":.05,"fgm":.16,"fga":.33,
              "fg3m":.06,"fg3a":.15,"ftm":.07,"fta":.09}
        out.append(PlayerProjection(f"{team}:p{i}",team,m,5.0,.4+i*.01,rate,
                                    .48,.36,.8,60,"confirmed_available"))
    return allocate_minutes(out)

def demo(counts=(1000,5000,10000),seed=20261121):
    match=Matchup(
        TeamSettings("BOS",116,110,.42,.13,.28),
        TeamSettings("DEN",115,112,.39,.125,.27),
        100.0,2.0
    )
    data=check_convergence(match,example_roster("BOS"),
                           example_roster("DEN"),seed,counts)
    return {
        "test_type":"synthetic_sampling_convergence_not_accuracy",
        "model":"possession-events-v2.0",
        "seed":seed,
        "rows":data,
        "comment":"10k sampling reduces Monte Carlo standard error; it does not fix biased assumptions."
    }

if __name__=="__main__":
    print(json.dumps(demo(),indent=2))
