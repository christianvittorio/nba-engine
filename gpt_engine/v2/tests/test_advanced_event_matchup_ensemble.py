"""Prior-only event/matchup and calibrated ensemble experiment tests."""
from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from gpt_engine.v2.simulation import Matchup,TeamSettings,simulate_game
from gpt_engine.v2.players import PlayerProjection,allocate_minutes
from gpt_engine.v2.event_rate_eval import (
    RATE_SPEC,candidate_event_rate,validate_event_rates
)
from gpt_engine.v2.ensemble_eval import blend,choose_blend
from gpt_engine.v2.feature_ablation import (
    append_opponent_event_cross_features,rolling_team_features,BASE_PRIORS,
    EVENT_CROSS_FEATURES
)

def _players(team,three_specialist=False):
    players=[]
    for i in range(8):
        minutes=(34 if i<5 else 25)
        fg3a=(.32 if i==0 else .02) if three_specialist else .13
        rate={"pts":.44,"reb":.13,"ast":.10,"stl":.02,"blk":.015,
              "tov":.05,"fgm":.15,"fga":.37,"fg3m":fg3a*.35,
              "fg3a":fg3a,"ftm":.08,"fta":.10}
        players.append(PlayerProjection(
            player_id=f"{team}:p{i}",team_id=team,
            minutes=minutes,minutes_sd=5,
            usage_weight=.36, rates_per_min=rate,
            field_goal_pct=.46,three_point_pct=.35,
            free_throw_pct=.79,sample_games=30,
            availability="confirmed_available"
        ))
    return allocate_minutes(players)

def _match():
    return Matchup(TeamSettings("home",113,113,.40,.13,.26),
                   TeamSettings("away",113,113,.35,.13,.27),
                   98,2)

def test_player_shot_style_is_opt_in_and_preserves_baseline():
    home=_players("home",three_specialist=True)
    away=_players("away")
    baseline=simulate_game(_match(),home,away,n=90,seed=42)
    explicit=simulate_game(_match(),home,away,n=90,seed=42,
                           event_model="baseline")
    assert baseline==explicit
    alternate=simulate_game(_match(),home,away,n=90,seed=42,
                            event_model="player_shot_mix",include_samples=True)
    assert alternate["event_model"]=="player_shot_mix"
    assert alternate["experimental_player_shot_mix"]
    target="home:p0"
    assert alternate["player_statistics"][target]["fg3a"]["mean"] > (
        baseline["player_statistics"][target]["fg3a"]["mean"]*1.45
    )
    for i,row in enumerate(alternate["_samples"]):
        home_min=sum(alternate["_player_samples"][p.player_id]["minutes"][i]
                     for p in home)
        away_min=sum(alternate["_player_samples"][p.player_id]["minutes"][i]
                     for p in away)
        assert abs(home_min-(240+row[4]*25))<1e-3
        assert abs(away_min-(240+row[4]*25))<1e-3
        for player in home+away:
            d={k:v[i] for k,v in alternate["_player_samples"][player.player_id].items()}
            assert d["pts"]==2*d["fgm"]+d["fg3m"]+d["ftm"]
            assert d["fg3m"]<=d["fg3a"]<=d["fga"]
            assert d["oreb"]+d["dreb"]==d["reb"]
    with pytest.raises(ValueError,match="research"):
        simulate_game(_match(),home,away,n=55,event_model="future_unvalidated_model")

def test_event_blend_falls_back_to_prespecified_league_prior():
    a=candidate_event_rate(
        [np.nan,.2,.9],[.30,np.nan,.25],.5,
        league_prior=.37,limits=(.12,.68))
    assert np.allclose(a,[.335,.285,.575])
    with pytest.raises(ValueError,match="weight"):
        candidate_event_rate([.2],[.3],1.1,league_prior=.37,limits=(0,1))

def _fake_event_frame():
    rng=np.random.default_rng(88)
    rows=[]
    groups=[
        ("2024-01-01",110),
        ("2024-10-02",110),
        ("2025-02-01",110),
        ("2025-10-01",110),
    ]
    for date,n in groups:
        for i in range(n):
            row={"game_id":f"{date}-{i}",
                 "game_date":(pd.Timestamp(date)+pd.Timedelta(days=i)).strftime("%Y-%m-%d")}
            for event,spec in RATE_SPEC.items():
                own=spec["prior"]+rng.normal(0,.027)
                opp=spec["prior"]+rng.normal(0,.025)
                actual=.60*own+.40*opp+rng.normal(0,.006)
                row[event+"_own_prior"]=own
                row[event+"_opponent_prior"]=opp
                row[event+"_actual"]=actual
            rows.append(row)
    return pd.DataFrame(rows)

def test_opponent_event_weights_use_validation_not_later_results():
    df=_fake_event_frame()
    report=validate_event_rates(df)
    assert report["counts"]["selection"]==110
    assert all(0<=v["chosen_on_validation_only"]<=1
               for v in report["results"].values())
    assert any(v["chosen_on_validation_only"]>0
               for v in report["results"].values())
    poisoned=df.copy()
    mask=poisoned.game_date>="2025-10-01"
    for event in RATE_SPEC:
        poisoned.loc[mask,event+"_actual"]+=.15
    alternate=validate_event_rates(poisoned)
    assert {k:v["chosen_on_validation_only"] for k,v in report["results"].items()}=={
        k:v["chosen_on_validation_only"] for k,v in alternate["results"].items()}
    assert report["results"]["three_point_rate"]["frozen_holdout"] != (
        alternate["results"]["three_point_rate"]["frozen_holdout"])

def test_opponent_crossmatchups_only_use_previously_finished_game():
    data=[]
    for i in range(13):
        date=(pd.Timestamp("2024-10-01")+pd.Timedelta(days=i)).strftime("%Y-%m-%d")
        for team,opp,home in (("1","2",True),("2","1",False)):
            row=dict(BASE_PRIORS)
            row.update({
                "game_id":f"002240{i:04d}","team_id":team,
                "opp_team_id":opp,"game_date":date,"season":2025,
                "game_type":"regular_season","home":home,
                "three_point_rate":.29+(i+.5*int(team=="2"))/110,
                "opp_3pa_rate_allowed":.27+(i+.4*int(team=="2"))/130,
                "pts":110
            })
            data.append(row)
    raw=pd.DataFrame(data)
    def matchup(frame):
        rolled=rolling_team_features(frame)
        h=rolled[rolled.home].copy()
        a=rolled[~rolled.home].copy()
        towide=h[["game_id"]+
           [f"rolling20_{x}" for x in (
               "three_point_rate","fta_rate","tm_tov_pct","oreb_pct",
               "opp_3pa_rate_allowed","opp_fta_rate_allowed",
               "opp_tov_rate_forced","opp_oreb_rate_allowed")]].copy()
        keys=[c for c in towide if c!="game_id"]
        towide=towide.rename(columns={c:"home__"+c for c in keys})
        other=a[["game_id"]+keys].rename(columns={c:"away__"+c for c in keys})
        return append_opponent_event_cross_features(towide.merge(other,on="game_id"))
    before=matchup(raw)
    changed=raw.copy()
    changed.loc[changed.game_date=="2024-10-07",
                ["three_point_rate","opp_3pa_rate_allowed"]]=.98
    after=matchup(changed)
    key="home_3pa_pressure_vs_away_3pa_allowed"
    assert key in EVENT_CROSS_FEATURES
    x=before[before.game_id=="0022400006"][key].iloc[0]
    y=after[after.game_id=="0022400006"][key].iloc[0]
    assert x==y
    nx=before[before.game_id=="0022400007"][key].iloc[0]
    ny=after[after.game_id=="0022400007"][key].iloc[0]
    assert nx!=ny

def test_ensemble_weight_selected_without_historical_holdout():
    rng=np.random.default_rng(4)
    y=rng.integers(0,2,220)
    elo=np.where(y, .82,.18)
    bad=np.where(y,.33,.67)
    em=np.where(y,13.,-13.)
    rm=np.where(y,-12.,12.)
    total=np.full(len(y),225.)
    chosen=choose_blend(elo,bad,em,rm,total,y,em)
    assert chosen["selected"]["elo_weight"]==1.0
    assert len(chosen["candidates"])==5
    p,margin,t=blend(elo,bad,em,rm,total,1)
    assert np.allclose(p,elo)
    assert np.allclose(margin,em)
    assert np.allclose(t,total)
    with pytest.raises(ValueError):
        blend(elo,bad[:-1],em,rm,total,.5)
    with pytest.raises(ValueError):
        blend(elo,bad,em,rm,total,-.01)
