"""Conservative per-minute player priors and coherent conditional rotations.

No historical per-game logs for a player means wide intervals and a strong
prior, not an invented confident prop. Unknown/Questionable statuses require
separately labelled scenarios; no arbitrary probability assignment.
"""
from __future__ import annotations
from dataclasses import dataclass, replace, field
from datetime import date
import math

import numpy as np
import pandas as pd

STATS=("pts","reb","ast","stl","blk","tov","fgm","fga","fg3m","fg3a","ftm","fta")
LEAGUE_PER_MIN={
    "pts":.42,"reb":.16,"ast":.105,"stl":.025,"blk":.017,
    "tov":.055,"fgm":.15,"fga":.32,"fg3m":.048,"fg3a":.13,
    "ftm":.08,"fta":.1
}
UNKNOWN={"unknown","questionable","doubtful"}
OUT={"out"}
WARNING="Availability/playing time uncertain: report separate conditional scenarios; no confident props."

@dataclass(frozen=True)
class PlayerProjection:
    player_id: str
    team_id: str
    minutes: float
    minutes_sd: float
    usage_weight: float
    rates_per_min: dict[str,float]
    field_goal_pct: float
    three_point_pct: float
    free_throw_pct: float
    sample_games: int
    availability: str = "unknown"
    position: str = "UNKNOWN"
    evidence_asof_date: str = ""
    flags: tuple[str,...] = ()
    def __post_init__(self):
        if self.minutes < 0 or self.minutes>48.1:
            raise ValueError("Implausible regulation minutes")
        if self.usage_weight<0:
            raise ValueError("Invalid usage")
        if any(x<0 or not math.isfinite(x) for x in self.rates_per_min.values()):
            raise ValueError("Bad player per-minute rate")
    def stats_mean(self):
        return {k:round(self.minutes*self.rates_per_min.get(k,0),3) for k in STATS}

def _numeric(data:pd.DataFrame,name:str,default:float=0) -> pd.Series:
    if name not in data:
        return pd.Series(default,index=data.index,dtype=float)
    return pd.to_numeric(data[name],errors="coerce").fillna(default)

def estimate_player(history: pd.DataFrame, player_id: str, team_id: str,
                    target_date: str, *, season: int | None=None,
                    availability="unknown", role_multiplier=1.0,
                    position="UNKNOWN") -> PlayerProjection:
    if availability not in ("confirmed_available","probable",
                            "questionable","doubtful","out","unknown"):
        raise ValueError("Provider availability status must be normalized first")
    if "game_date" not in history or "player_id" not in history:
        raise ValueError("Player history needs game_date and player_id")
    df=history.copy()
    df["game_date"]=df.game_date.astype(str).str[:10]
    df=df[(df.player_id.astype(str)==str(player_id)) &
          (df.game_date<str(target_date))].sort_values(["game_date","game_id"])
    if season is not None and "season" in df:
        df=df[pd.to_numeric(df.season)<=season]
    # Exclude DNP rows and missing minutes from per-minute rate calculations.
    mins=_numeric(df,"min",0)
    df=df[mins>0].copy()
    mins=mins.loc[df.index]
    n=len(df)
    recent=df.tail(10)
    recent_min=_numeric(recent,"min")
    long_mean=float(_numeric(df.tail(60),"min").mean()) if n else 0
    rec_mean=float(recent_min.mean()) if n else 0
    baseline=25.0 if n==0 else (n/(n+8))*rec_mean+(8/(n+8))*long_mean
    minutes=float(np.clip((baseline if n else 24.0)*role_multiplier,0,43))
    min_sd=float(max(4.5, (recent_min.std(ddof=0) if n>=2 else 9.0)))
    rates={}
    # Total observed minutes are the denominator for Poisson-rate shrinkage.
    sample=df.tail(40)
    time=float(_numeric(sample,"min").sum())
    for stat in STATS:
        hits=float(_numeric(sample,stat).sum())
        league=LEAGUE_PER_MIN[stat]
        # 100 prior player-minutes; rookies/new roles get much larger shrinkage.
        estimated=(hits+100*league)/max(1,time+100)
        # Recent 10-game component, mildly weighted until enough evidence exists.
        rec_time=float(_numeric(recent,"min").sum())
        rec_hits=float(_numeric(recent,stat).sum())
        rec=(rec_hits+55*estimated)/(rec_time+55)
        rates[stat]=round(float(.65*estimated+.35*rec),7)
    def shooting(made,attempt,prior,strength):
        a=float(_numeric(sample,attempt).sum())
        m=float(_numeric(sample,made).sum())
        return float(np.clip((m+strength*prior)/(a+strength),.05,.95))
    fg=shooting("fgm","fga",.47,70)
    three=shooting("fg3m","fg3a",.36,55)
    ft=shooting("ftm","fta",.78,45)
    # Avoid impossible shooting-rate relationship: outcome engine uses
    # *probabilities*; rates are only priors/usage information.
    usage=max(.01,rates["fga"]+0.55*rates["fta"]+rates["tov"])
    flags=[]
    if n<10: flags.append("low_sample_minutes_and_stat_rates")
    if availability in UNKNOWN: flags.append("availability_scenario_required")
    if not n: flags.append("league_prior_only_no_player_history")
    if availability=="out": minutes=0.0
    return PlayerProjection(str(player_id),str(team_id),minutes,min_sd,usage,
                            rates,fg,three,ft,n,availability,position,
                            str(df.game_date.max()) if n else "",
                            tuple(flags))

def allocate_minutes(players: list[PlayerProjection],target:float=240.0,
                     max_minutes=48.0) -> list[PlayerProjection]:
    """Capped proportional allocation: exactly 240 team-minutes in regulation."""
    if target<=0 or max_minutes<=0:
        raise ValueError("Invalid target minutes")
    if not players:
        raise ValueError("No player rotations")
    seen=set()
    for p in players:
        if p.player_id in seen:
            raise ValueError("Player assigned to rotation twice")
        seen.add(p.player_id)
    eligible=[i for i,p in enumerate(players) if p.availability!="out"]
    if len(eligible)*max_minutes < target-1e-5:
        raise ValueError("Insufficient eligible players for valid 240-minute rotation")
    weights=np.array([max(0,p.minutes) if p.availability!="out" else 0
                       for p in players],dtype=float)
    if weights.sum()<1:
        for i in eligible:
            weights[i]=1
    alloc=np.zeros(len(players))
    remaining=target
    active=set(eligible)
    for _ in range(len(players)+2):
        if not active: break
        norm=sum(weights[i] for i in active)
        if norm<=0: norm=float(len(active))
        capped=[]
        for i in sorted(active):
            weight=(weights[i]/norm) if norm!=len(active) or sum(weights[j] for j in active)>0 else (1/norm)
            suggestion=remaining*weight
            if suggestion>max_minutes+1e-8:
                alloc[i]=max_minutes
                capped.append(i)
        if not capped:
            for i in active:
                alloc[i]=remaining*(weights[i]/norm if sum(weights[j] for j in active)>0 else 1/norm)
            remaining=0
            break
        for i in capped:
            active.remove(i)
        remaining=target-float(np.sum(alloc))
    if abs(sum(alloc)-target)>1e-4 or any(a>max_minutes+1e-5 for a in alloc):
        raise ValueError("Failed to allocate exact team minutes")
    return [replace(p,minutes=round(float(v),6)) for p,v in zip(players,alloc)]

def conditional_rotation(players:list[PlayerProjection],status_overrides:dict[str,str],
                         *, minutes_overrides:dict[str,float]|None=None) -> list[PlayerProjection]:
    changed=[]
    for p in players:
        status=status_overrides.get(p.player_id,p.availability)
        if status not in ("confirmed_available","probable","questionable",
                          "doubtful","out","unknown"):
            raise ValueError(f"Unknown scenario status for {p.player_id}")
        m=(minutes_overrides or {}).get(p.player_id,p.minutes)
        flags=list(p.flags)
        if status in UNKNOWN and "availability_scenario_required" not in flags:
            flags.append("availability_scenario_required")
        changed.append(replace(p,minutes=0 if status=="out" else m,
                               availability=status,flags=tuple(flags)))
    return allocate_minutes(changed)

def role_distribution_warning(players:list[PlayerProjection]) -> list[str]:
    reasons=[]
    missing=[p.player_id for p in players if p.availability in UNKNOWN]
    if missing:
        reasons.append(WARNING+" Players: "+", ".join(missing))
    low=[p.player_id for p in players if p.sample_games<10]
    if low:
        reasons.append("Limited (<10 games) historical sample: "+", ".join(low))
    return reasons

def probability_at_least(simulated:list[float]|np.ndarray,threshold:float) -> dict:
    values=np.asarray(simulated,dtype=float)
    if not len(values) or not np.all(np.isfinite(values)):
        raise ValueError("Requires finite player-stat simulation samples")
    p=float(np.mean(values>=threshold))
    n=len(values)
    return {"threshold":float(threshold),"p_at_least":round(p,5),
            "mc_standard_error":round(float(np.sqrt(p*(1-p)/n)),5),
            "sample_count":n}
