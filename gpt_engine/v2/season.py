"""Correlated season win distributions from an *explicit* remaining schedule.

This produces wins and conference seeding proxies. It deliberately does
not manufacture a real NBA playoff bracket, play-in result, NBA Cup effect,
or championship probability without a bracket/series simulator.
"""
from __future__ import annotations

from math import exp,log
from collections import defaultdict
import numpy as np

def simulate_season(games:list[dict], conference_by_team:dict[str,str] | None,
                    n:int=10000,seed:int=20261121) -> dict:
    if n<50: raise ValueError("At least 50 simulations")
    if not games: raise ValueError("Require a source-backed season schedule")
    teams=sorted({str(g["home_team_id"]) for g in games}|
                 {str(g["away_team_id"]) for g in games})
    if len(set(g["game_id"] for g in games))!=len(games):
        raise ValueError("Duplicate game IDs in remaining schedule")
    known={k:v for k,v in (conference_by_team or {}).items() if v in ("East","West")}
    rng=np.random.default_rng(seed)
    win_arr={t:np.zeros(n,dtype=np.int16) for t in teams}
    direct={t:0 for t in teams}
    playin={t:0 for t in teams}
    seed_counts={t:defaultdict(int) for t in teams}
    completed=0
    for g in games:
        home=str(g["home_team_id"]);away=str(g["away_team_id"])
        if "actual_home_score" in g and g["actual_home_score"] is not None:
            if g.get("actual_away_score") is None:
                raise ValueError("Partially populated actual score")
            if g["actual_home_score"]==g["actual_away_score"]:
                raise ValueError("NBA final score cannot be tied")
            win_arr[home if g["actual_home_score"]>g["actual_away_score"] else away]+=1
            completed+=1
        elif not 0<float(g.get("p_home",0))<1:
            raise ValueError(f"Unmodeled future game {g['game_id']} lacks probability")
    # Latent team-season strength is shared across all of a simulation's
    # remaining games, inducing realistic positive game-to-game dependence.
    shocks={t:rng.normal(0,.12,size=n) for t in teams}
    for g in games:
        if g.get("actual_home_score") is not None:
            continue
        home=str(g["home_team_id"]);away=str(g["away_team_id"])
        p=float(g["p_home"])
        logit=log(p/(1-p))
        shifted=np.clip(logit+shocks[home]-shocks[away],-30,30)
        chance=1/(1+np.exp(-shifted))
        h_win=rng.random(n)<chance
        win_arr[home]+=h_win
        win_arr[away]+=(~h_win)
    if known:
        by_conf=defaultdict(list)
        for team in teams:
            if team not in known:
                raise ValueError(f"Missing conference for team {team}; refuse seed forecast")
            by_conf[known[team]].append(team)
        for conference, ids in by_conf.items():
            for i in range(n):
                # Random tie breaks: do NOT assert real head-to-head tiebreak rules.
                ordered=sorted(ids,key=lambda x:(-win_arr[x][i],rng.random()))
                for seed_no,team in enumerate(ordered,start=1):
                    seed_counts[team][seed_no]+=1
                    if seed_no<=6:direct[team]+=1
                    if seed_no<=10:playin[team]+=1
    output={}
    for team in teams:
        vals=win_arr[team].astype(float)
        output[team]={
            "wins_mean":round(float(vals.mean()),3),
            "wins_q10":float(np.quantile(vals,.1)),
            "wins_q50":float(np.quantile(vals,.5)),
            "wins_q90":float(np.quantile(vals,.9)),
            "top6_seed_proxy_probability":round(direct[team]/n,5) if known else None,
            "top10_playin_proxy_probability":round(playin[team]/n,5) if known else None,
            "seed_distribution":{str(k):v/n for k,v in sorted(seed_counts[team].items())},
            "playoffs_probability":None,
            "finals_probability":None,
            "championship_probability":None
        }
    # Each played game always awards exactly one win.
    total_wins=sum(sum(win_arr[t]) for t in teams)
    if total_wins!=n*len(games):
        raise AssertionError("Season win accounting error")
    return {
        "season_simulation_count":n,"seed":seed,"completed_games":completed,
        "scheduled_games":len(games),"team_count":len(teams),
        "teams":output,
        "warnings":[
            "Playoff/finals/title probabilities unavailable until an official bracket model exists.",
            "Top-six and top-ten are *seeding proxies*, not actual playoff qualification.",
            "Tied standings are resolved with random tie breaks, NOT official NBA rules.",
            "Season latent-strength correlation is a research assumption awaiting backtesting.",
        ]
    }
