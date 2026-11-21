"""Possession-based, correlated team/player Monte Carlo for the GPT v2 research lane.

A single sampled game state drives ALL outputs: total, margin, winner, shots,
assists, and each player's box-score events. No independent player-point
draws. Stochastic parameters are research priors, not yet fitted or validated
against an unseen holdout. Recalibrate before using for market decisions.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
from typing import Any

import numpy as np

from .models import TeamForecast
from .players import PlayerProjection, STATS, role_distribution_warning, probability_at_least

BASKETBALL_RULES_VERSION="possession-events-v2.0"
STAT_COLS=("pts","reb","ast","stl","blk","tov","fgm","fga",
           "fg3m","fg3a","ftm","fta","oreb","dreb")


@dataclass(frozen=True)
class TeamSettings:
    team_id: str
    offense_rating: float
    defense_rating: float
    three_attempt_rate: float
    turnover_probability: float
    offensive_rebound_probability: float
    free_throw_trip_probability: float = 0.13
    def __post_init__(self):
        for name in ("three_attempt_rate","turnover_probability",
                     "offensive_rebound_probability","free_throw_trip_probability"):
            v=getattr(self,name)
            if not 0 <= v < 1:
                raise ValueError(f"{name} must be a probability")
        if not 65 <= self.offense_rating <= 160 or not 65 <= self.defense_rating <= 160:
            raise ValueError("Rating is implausible")


@dataclass(frozen=True)
class Matchup:
    home: TeamSettings
    away: TeamSettings
    expected_possessions: float
    home_court_points: float=2.0
    rest_effect_home: float=0.0
    rest_effect_away: float=0.0
    def __post_init__(self):
        if self.home.team_id == self.away.team_id:
            raise ValueError("Same team on both sides")
        if not 70 <= self.expected_possessions <= 130:
            raise ValueError("Implausible possession estimate")

def _safe_share(x:float, low:float,high:float):
    return float(np.clip(x,low,high))

def _weighted_pick(rng, weights: np.ndarray) -> int:
    r=rng.random()*float(np.sum(weights))
    return min(len(weights)-1,int(np.searchsorted(np.cumsum(weights),r,side="right")))

def _minutes_draw(rng,players:list[PlayerProjection],overtimes:int=0) -> np.ndarray:
    """Positive correlated minute share allocation, exact total; max floor game time."""
    target=240.0+25.0*overtimes
    cap=48.0+5.0*overtimes
    eligible=np.array([p.availability!="out" for p in players])
    if int(np.sum(eligible))*cap<target-1e-6:
        raise ValueError("Not enough players to field a lineup")
    means=np.array([max(p.minutes,0) if e else 0 for p,e in zip(players,eligible)],
                   dtype=float)
    if means.sum()<1:
        means[eligible]=1
    noise=np.array([rng.normal(0,min(.40,p.minutes_sd/max(p.minutes,8)))
                    for p in players])
    weights=means*np.exp(noise)
    result=np.zeros(len(players))
    active=set(int(i) for i in np.flatnonzero(eligible))
    for _ in range(len(players)+2):
        if not active:break
        indices=sorted(active)
        total_weight=sum(weights[i] for i in indices)
        remain=target-float(result.sum())
        if remain<0:
            raise ValueError("Rotation allocation overshot")
        trials={i:remain*(weights[i]/total_weight if total_weight else 1/len(indices))
                for i in indices}
        capped=[i for i in indices if trials[i]>cap+1e-8]
        if not capped:
            for i in indices:result[i]=trials[i]
            break
        for i in capped:
            result[i]=cap
            active.remove(i)
    if abs(result.sum()-target)>1e-3 or np.max(result)>cap+1e-3:
        raise AssertionError("Rotation minutes do not reconcile")
    return result

def _player_arrays(players:list[PlayerProjection],mins:np.ndarray):
    usage=np.array([max(.001,p.usage_weight*m) for p,m in zip(players,mins)])
    ast=np.array([max(.001,p.rates_per_min.get("ast",.05)*m)
                  for p,m in zip(players,mins)])
    steals=np.array([max(.001,p.rates_per_min.get("stl",.02)*m)
                     for p,m in zip(players,mins)])
    blocks=np.array([max(.001,p.rates_per_min.get("blk",.01)*m)
                     for p,m in zip(players,mins)])
    rebounds=np.array([max(.001,p.rates_per_min.get("reb",.1)*m)
                       for p,m in zip(players,mins)])
    # Optional v3 candidate: distribute three-point/two-point attempts
    # across players using THEIR prior attempts, not one team-wide 3PA mix
    # indiscriminately applied to every shooter. Shot totals remain driven
    # by the same possession events; only assignment among eligible players
    # changes. Shrink uncertain per-minute rates toward league priors.
    three=np.asarray([
        .70*max(0,p.rates_per_min.get("fg3a",.13))+.30*.13 for p in players])
    fga=np.asarray([
        .70*max(.001,p.rates_per_min.get("fga",.32))+.30*.32
        for p in players])
    frac=np.clip(three/np.maximum(fga,.01),.02,.90)
    two=np.maximum(.02,1-frac)
    shots_three=usage*np.clip(frac/.37,.18,2.8)
    shots_two=usage*np.clip(two/.63,.18,2.8)
    ft_rate=np.asarray([
        .70*max(0,p.rates_per_min.get("fta",.10))+.30*.10 for p in players])
    ft_takers=usage*np.clip(ft_rate/.10,.18,2.8)
    for arr in (usage,ast,steals,blocks,rebounds,
                shots_three,shots_two,ft_takers):
        arr[mins<=0]=0
    return {"usage":usage,"assists":ast,"steals":steals,
            "blocks":blocks,"rebounds":rebounds,
            "three_point_shooters":shots_three,
            "two_point_shooters":shots_two,
            "free_throw_shooters":ft_takers}

def _empty_box(players:list[PlayerProjection],mins:np.ndarray):
    return {p.player_id:{"minutes":float(m),**{key:0 for key in STAT_COLS}}
            for p,m in zip(players,mins)}

def _attempt(rng,attacking:TeamSettings,defending:TeamSettings,
             attack:list[PlayerProjection],defense:list[PlayerProjection],
             aw:dict,dw:dict,ab:dict,db:dict, team_state:dict,
             opponent_state:dict, location_advantage:float=0,
             event_model:str="baseline"):
    """One possession with possible ORB retries; only explicit shot/FT events score."""
    usage=aw["usage"]
    if usage.sum()<1e-12: raise ValueError("No eligible attackers")
    efficiency=(attacking.offense_rating+defending.defense_rating)/2.0
    # Shared offensive shock across possessions induces score and player
    # correlation; matchups alter shooting via explicit team ratings.
    bump=_safe_share((efficiency-113)/240.0 + location_advantage/150.0+
                     team_state["shooting_shock"]-opponent_state["defensive_shock"],
                     -.14,.14)
    if rng.random() < attacking.turnover_probability:
        lost=_weighted_pick(rng,usage)
        ab[attack[lost].player_id]["tov"]+=1
        if rng.random()<.48:
            taker=_weighted_pick(rng,dw["steals"])
            db[defense[taker].player_id]["stl"]+=1
        return
    for second_chance in range(4):
        # Baseline is intentionally unchanged for existing published
        # forecasts. The research-only candidate uses shot-type-dependent
        # prior player volume, not uniform team 3PA specialization.
        shooter=_weighted_pick(rng,usage)
        p=attack[shooter]
        box=ab[p.player_id]
        if rng.random()<attacking.free_throw_trip_probability:
            if event_model=="player_shot_mix":
                shooter=_weighted_pick(rng,aw["free_throw_shooters"])
                p=attack[shooter]
                box=ab[p.player_id]
            # Free throw trip: two attempts, or rarely three on a 3PA foul.
            three_foul=(rng.random()<attacking.three_attempt_rate*.11)
            attempts=3 if three_foul else 2
            missed_last=False
            for shot_number in range(attempts):
                box["fta"]+=1
                made=rng.random()<_safe_share(p.free_throw_pct,.50,.96)
                if made:
                    box["ftm"]+=1
                    box["pts"]+=1
                if shot_number==attempts-1 and not made:
                    missed_last=True
            if missed_last:
                # Live last-FT misses create exactly one rebound, as missed
                # field goals do. An offensive board continues the possession.
                if rng.random()<attacking.offensive_rebound_probability:
                    rebounder=_weighted_pick(rng,aw["rebounds"])
                    rr=ab[attack[rebounder].player_id]
                    rr["reb"]+=1
                    rr["oreb"]+=1
                    if second_chance<3:
                        continue
                    ab[attack[_weighted_pick(rng,usage)].player_id]["tov"]+=1
                else:
                    defender=_weighted_pick(rng,dw["rebounds"])
                    rr=db[defense[defender].player_id]
                    rr["reb"]+=1
                    rr["dreb"]+=1
            return
        is_three=(rng.random()<attacking.three_attempt_rate)
        if event_model=="player_shot_mix":
            shooter=_weighted_pick(rng,aw[
                "three_point_shooters" if is_three else "two_point_shooters"
            ])
            p=attack[shooter]
            box=ab[p.player_id]
        box["fga"]+=1
        box["fg3a"]+=int(is_three)
        p_make=(p.three_point_pct if is_three else
                (p.field_goal_pct*p.rates_per_min.get("fga",.3) -
                 p.three_point_pct*p.rates_per_min.get("fg3a",.12)) /
                max(.08, p.rates_per_min.get("fga",.3) -
                          p.rates_per_min.get("fg3a",.12)))
        # The estimated 2P formula above is approximate; bound by plausible
        # scoring domain and let validation tune it.
        probability=_safe_share(p_make+bump,.23,.77 if not is_three else .65)
        if rng.random()<probability:
            box["fgm"]+=1
            box["fg3m"]+=int(is_three)
            box["pts"]+=3 if is_three else 2
            assist_chance=.71 if is_three else .50
            if rng.random()<assist_chance:
                help_weight=aw["assists"].copy()
                help_weight[shooter]=0
                if help_weight.sum()>0:
                    passer=_weighted_pick(rng,help_weight)
                    ab[attack[passer].player_id]["ast"]+=1
            return
        # Defensive block on a miss. Assumed probability, not a fitted stat.
        if rng.random()<(0.028 if is_three else .085):
            defender=_weighted_pick(rng,dw["blocks"])
            db[defense[defender].player_id]["blk"]+=1
        # One rebound per missed FG including ORB and defensive board.
        is_orb=rng.random()<attacking.offensive_rebound_probability
        if is_orb:
            rebounder=_weighted_pick(rng,aw["rebounds"])
            r=ab[attack[rebounder].player_id]
            r["reb"]+=1;r["oreb"]+=1
            if second_chance<3:
                continue
            # Fourth chance cap: possession ends on a team turnover.
            ab[attack[_weighted_pick(rng,usage)].player_id]["tov"]+=1
            return
        defender=_weighted_pick(rng,dw["rebounds"])
        r=db[defense[defender].player_id]
        r["reb"]+=1;r["dreb"]+=1
        return

def _roll_single(rng,match:Matchup,home:list[PlayerProjection],
                 away:list[PlayerProjection],overrides:dict[str,dict]|None=None,
                 event_model:str="baseline"):
    hp=_minutes_draw(rng,home)
    ap=_minutes_draw(rng,away)
    H=_empty_box(home,hp);A=_empty_box(away,ap)
    hw=_player_arrays(home,hp);aw=_player_arrays(away,ap)
    shared=rng.normal(0,.018)
    h_state={"shooting_shock":shared+rng.normal(0,.018),
             "defensive_shock":rng.normal(0,.009)}
    a_state={"shooting_shock":shared+rng.normal(0,.018),
             "defensive_shock":rng.normal(0,.009)}
    n=int(np.clip(round(rng.normal(match.expected_possessions,5.0)),65,135))
    # Both teams share the same latent pace and game scoring environment.
    def period(possessions,pace_factor=1.0):
        for _ in range(possessions):
            _attempt(rng,match.home,match.away,home,away,hw,aw,H,A,h_state,a_state,
                     (match.home_court_points/2+match.rest_effect_home),
                     event_model=event_model)
            _attempt(rng,match.away,match.home,away,home,aw,hw,A,H,a_state,h_state,
                     (-match.home_court_points/2+match.rest_effect_away),
                     event_model=event_model)
    period(n)
    def score(box):
        return sum(r["pts"] for r in box.values())
    ot=0
    while score(H)==score(A):
        ot+=1
        if ot>5:
            # Exceptionally rare long OT; continue with possession sudden death
            # instead of inventing a tie or assigning arbitrary winning points.
            for _ in range(1000):
                period(1)
                if score(H)!=score(A):break
            if score(H)==score(A):
                raise RuntimeError("Unable to resolve overtime tie")
            break
        extra=int(np.clip(round(n*5/48+rng.normal(0,1.0)),6,17))
        period(extra)
    if ot:
        # Re-draw a plausible minutes allocation INCLUDING actual OT minutes.
        # The shot participation shares were regulation approximations, and
        # this per-game extension conserves the total team minute sum.
        for p,m in zip(home,_minutes_draw(rng,home,ot)):
            H[p.player_id]["minutes"]=float(m)
        for p,m in zip(away,_minutes_draw(rng,away,ot)):
            A[p.player_id]["minutes"]=float(m)
    hscore=score(H);ascore=score(A)
    assert hscore!=ascore
    assert abs(sum(v["minutes"] for v in H.values())-(240+25*ot))<1e-3
    assert abs(sum(v["minutes"] for v in A.values())-(240+25*ot))<1e-3
    for box,total in ((H,hscore),(A,ascore)):
        assert sum(v["pts"] for v in box.values())==total
        assert all(v["pts"] == 2*v["fgm"]+v["fg3m"]+v["ftm"] for v in box.values())
        assert all(v["fg3m"]<=v["fg3a"] and v["fg3m"]<=v["fgm"]<=v["fga"]
                   and v["ftm"]<=v["fta"] for v in box.values())
        assert all(v["oreb"]+v["dreb"]==v["reb"] for v in box.values())
        assert sum(v["ast"] for v in box.values())<=sum(v["fgm"] for v in box.values())
    return {"home_score":hscore,"away_score":ascore,
            "total":hscore+ascore,"margin":hscore-ascore,"overtimes":ot,
            "home":H,"away":A,"regulation_possessions_per_team":n}

def _quantile(data:np.ndarray,q:float):
    return float(np.quantile(data,q))

def _distribution(data:np.ndarray):
    return {
        "mean":round(float(np.mean(data)),4),
        "median":round(float(np.median(data)),4),
        "interval_50":[round(_quantile(data,.25),2),round(_quantile(data,.75),2)],
        "interval_80":[round(_quantile(data,.10),2),round(_quantile(data,.90),2)],
        "interval_90":[round(_quantile(data,.05),2),round(_quantile(data,.95),2)]
    }

def simulate_game(matchup:Matchup,home:list[PlayerProjection],
                  away:list[PlayerProjection],n:int=10000,
                  seed:int=20261121,batch_size:int=500,
                  thresholds:dict[str,dict[str,list[float]]]|None=None,
                  include_samples:bool=False,
                  event_model:str="baseline",
                  include_market_distributions:bool=False) -> dict:
    if event_model not in ("baseline","player_shot_mix"):
        raise ValueError("Only baseline or research player_shot_mix supported")
    if not isinstance(n,int) or n<50:
        raise ValueError("At least 50 simulations required")
    if not isinstance(batch_size,int) or batch_size<=0:
        raise ValueError("Positive batch size required")
    if {p.team_id for p in home}!={matchup.home.team_id} or \
       {p.team_id for p in away}!={matchup.away.team_id}:
        raise ValueError("Projected player teams must match the game")
    if any(p.player_id in {q.player_id for q in away} for p in home):
        raise ValueError("Player on both teams")
    if not 5<=len(home)<=20 or not 5<=len(away)<=20:
        raise ValueError("Expected full 5-20 player rotation for each side")
    # Preserve one RNG stream so batch-size changes do not alter predictions.
    rng=np.random.default_rng(seed)
    all_rows=[]
    per_player={p.player_id:{key:[] for key in ("minutes",)+STAT_COLS}
                for p in home+away}
    for start in range(0,n,batch_size):
        for _ in range(min(batch_size,n-start)):
            r=_roll_single(rng,matchup,home,away,event_model=event_model)
            all_rows.append((r["home_score"],r["away_score"],
                             r["total"],r["margin"],r["overtimes"]))
            for box in (r["home"],r["away"]):
                for pid,stats in box.items():
                    for stat,value in stats.items():
                        per_player[pid][stat].append(value)
    arr=np.asarray(all_rows,dtype=float)
    h=arr[:,0];a=arr[:,1];p=float(np.mean(h>a))
    out={
        "simulation_version":BASKETBALL_RULES_VERSION,
        "event_model":event_model,
        "experimental_player_shot_mix":event_model=="player_shot_mix",
        "seed":seed,"simulation_count":n,"batch_size":batch_size,
        "home_team_id":matchup.home.team_id,"away_team_id":matchup.away.team_id,
        "home_win_probability":round(p,5),
        "away_win_probability":round(1-p,5),
        "expected_home_score":round(float(h.mean()),3),
        "expected_away_score":round(float(a.mean()),3),
        "home_score":_distribution(h),"away_score":_distribution(a),
        "total":_distribution(arr[:,2]),"margin":_distribution(arr[:,3]),
        "overtime_probability":round(float(np.mean(arr[:,4]>0)),5),
        "mc_sampling_error":{
            "home_win_probability":round(sqrt(p*(1-p)/n),6),
            "expected_home_score":round(float(np.std(h,ddof=1)/sqrt(n)),4),
            "expected_away_score":round(float(np.std(a,ddof=1)/sqrt(n)),4),
            "expected_total":round(float(np.std(arr[:,2],ddof=1)/sqrt(n)),4),
            "expected_margin":round(float(np.std(arr[:,3],ddof=1)/sqrt(n)),4),
        },
        "player_statistics":{},
        "warnings":role_distribution_warning(home+away)+[
            "Simulation parameters are initial physical priors, NOT holdout-calibrated.",
            "Larger simulation counts reduce Monte Carlo noise, not model bias.",
            "Shot/role selection and overtime allocations are approximate, not full clock-and-lineup tracking."
        ]+([
            "Research-only player-specific 2PA/3PA/FTA assignment; not tuned or holdout validated; daily baseline unchanged."
        ] if event_model=="player_shot_mix" else []),
    }
    for player in home+away:
        raw=per_player[player.player_id]
        p_stats={k:_distribution(np.asarray(v,dtype=float)) for k,v in raw.items()}
        # Shooting percentages are meaningful only in simulations with an
        # actual attempt. Conditioning prevents 0/0 from becoming a made-up 0%.
        for label,made,attempt in (
            ("field_goal_percentage","fgm","fga"),
            ("three_point_percentage","fg3m","fg3a"),
            ("free_throw_percentage","ftm","fta")
        ):
            made_values=np.asarray(raw[made],dtype=float)
            attempted=np.asarray(raw[attempt],dtype=float)
            eligible=attempted>0
            p_stats[label]={
                "eligible_simulations":int(np.sum(eligible)),
                "ratio_of_expected_totals":round(
                    float(np.sum(made_values)/np.sum(attempted)),4)
                    if np.sum(attempted)>0 else None,
                "conditional_distribution":_distribution(
                    made_values[eligible]/attempted[eligible])
                    if np.any(eligible) else None,
            }
        p_stats["availability"]=player.availability
        p_stats["sample_games"]=player.sample_games
        p_stats["quality_flags"]=list(player.flags)
        t=(thresholds or {}).get(player.player_id,{})
        p_stats["threshold_probabilities"]={
            stat:{str(th):probability_at_least(raw[stat],th) for th in values}
            for stat,values in t.items() if stat in raw
        }
        out["player_statistics"][player.player_id]=p_stats
    if include_market_distributions:
        # Exact empirical point-mass distributions from the same correlated
        # possession Monte Carlo. These are NOT calibrated betting odds.
        # Histograms keep frozen predictions compact and allow later
        # line-specific evaluations without replaying a stochastic model.
        def histogram(values):
            values=np.asarray(values,dtype=float)
            if (len(values)!=n or not np.all(np.isfinite(values))
                    or not np.all(values==np.round(values))):
                raise ValueError("Invalid integer-valued market simulation samples")
            unique,counts=np.unique(values.astype(np.int64),return_counts=True)
            result={str(int(v)):int(c) for v,c in zip(unique,counts)}
            if sum(result.values()) != n:
                raise AssertionError("Incomplete market distribution")
            return result
        out["market_distributions"]={
            "sample_count":n,
            "home_margin_counts":histogram(arr[:,3]),
            "game_total_counts":histogram(arr[:,2]),
            "player_counts":{
                pid:{stat:histogram(stats[stat])
                     for stat in ("pts","reb","ast","fg3m")}
                for pid,stats in per_player.items()
            },
            "calibration_status":"uncalibrated",
            "source":"same_correlated_possession_draws",
            "settlement_scope":"full_game_including_overtime",
        }
    if include_samples:
        out["_samples"]=all_rows
        out["_player_samples"]=per_player
    return out

def check_convergence(matchup:Matchup,home:list[PlayerProjection],
                      away:list[PlayerProjection],seed:int=20261121,
                      counts=(1000,5000,10000)) -> list[dict]:
    """Same random seed makes smaller draws prefixes of larger runs."""
    if tuple(counts)!=tuple(sorted(set(counts))) or min(counts)<50:
        raise ValueError("Use sorted unique counts >= 50")
    rows=[]
    for n in counts:
        report=simulate_game(matchup,home,away,n=n,seed=seed,batch_size=500)
        rows.append({
            "simulations":n,
            "home_win_probability":report["home_win_probability"],
            "expected_total":report["total"]["mean"],
            "mc_standard_error_win":report["mc_sampling_error"]["home_win_probability"],
            "mc_standard_error_total":report["mc_sampling_error"]["expected_total"],
        })
    return rows
