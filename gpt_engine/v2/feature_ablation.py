"""Point-in-time NBA matchup feature ablation on *source-backed finished games*.

Only games BEFORE each forecast's Eastern date contribute to features.
No final season team rating, injury outcomes, today's box scores, same-day
matchup records, or postgame tracking can enter that game's predictors.

Grouping deliberately separates broad opponent G/F/C matchup evidence from
precise PG/SG/SF/PF/C claims (which this archive does not substantiate).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd

from .situational_streaks import append_pregame_situational_features

REPO=Path(__file__).resolve().parents[2]
SOURCE=REPO/"data_foundation"/"artifacts"
ROLLING=(5,10,20)
BASE_PRIORS={
    "off_rating":114.0,"def_rating":114.0,"net_rating":0.0,"pace":99.0,
    "efg_pct":.535,"ts_pct":.57,"three_point_rate":.37,
    "opp_three_pct_allowed":.36,"opp_fg3a":34.0,"opp_ast":24.0,
    "oreb_pct":.26,"dreb_pct":.74,"tm_tov_pct":.13,
    "fta_rate":.25,"ast":25.0,"tov":13.0,"oreb":10.0,
    "dreb":33.0,"opp_oreb":10.0,
}
FEATURE_GROUPS={
    "core":[
        "rolling5_off_rating","rolling10_off_rating","rolling20_off_rating",
        "rolling5_def_rating","rolling10_def_rating","rolling20_def_rating",
        "rolling20_net_rating","rolling20_pace",
        "multi_off_rating","multi_def_rating",
        "season_games_before","rest_days","back_to_back"
    ],
    "shooting":[
        "rolling20_efg_pct","rolling20_ts_pct","rolling20_three_point_rate",
        "rolling20_opp_three_pct_allowed","rolling20_opp_fg3a",
        "rolling20_fta_rate",
    ],
    "rebounding_turnovers":[
        "rolling20_oreb_pct","rolling20_dreb_pct",
        "rolling20_tm_tov_pct","rolling20_oreb",
        "rolling20_dreb","rolling20_tov",
    ],
    "observed_tactics":[
        "rolling5_pace","rolling10_pace","rolling5_three_point_rate",
        "rolling10_three_point_rate","rolling5_opp_ast",
        "rolling20_opp_ast","rolling20_opp_oreb",
        "rolling20_ast",
    ],
    "tracked_defender_matchups":[
        f"tracked_{position}_{stat}" for position in ("G","F","C")
        for stat in ("assists_per100","potential_assists_per100",
                     "points_per100","matchup_possessions","sample_games")
    ],
    "situational_streaks":[
        "situation_rest_days",
        "situation_venue_games","situation_venue_prior",
        "situation_sample","situation_shrunk_win_rate",
        "situation_edge","situation_low_sample",
    ],
}
CROSS_FEATURES=(
    "home_3pa_vs_away_3pa_allowed",
    "away_3pa_vs_home_3pa_allowed",
    "home_efg_vs_away_allowed",
    "away_efg_vs_home_allowed",
    "home_ast_vs_away_ast_allowed",
    "away_ast_vs_home_ast_allowed",
)

def read_season_csv(name:str,year:int)->pd.DataFrame:
    if name not in ("teams","tracked_defense_by_position_game"):
        raise ValueError("Unsupported source group")
    p=SOURCE/name/f"{year}.csv.gz"
    if not p.exists():raise FileNotFoundError(p)
    headers=pd.read_csv(p,nrows=0,compression="gzip").columns
    ids={key:str for key in ("game_id","team_id","opp_team_id","def_team_id")
         if key in headers}
    d=pd.read_csv(p,compression="gzip",dtype=ids,low_memory=False)
    if "season" not in d:d["season"]=year
    d["season"]=pd.to_numeric(d.season,errors="raise").astype(int)
    d["game_date"]=d.game_date.astype(str).str[:10]
    return d

def load_teams(years:list[int])->pd.DataFrame:
    d=pd.concat([read_season_csv("teams",year) for year in sorted(years)],
                ignore_index=True)
    d=d[d.game_type.astype(str)=="regular_season"].copy()
    if d.empty:raise ValueError("No regular-season rows")
    if d.duplicated(["game_id","team_id"]).any():
        raise ValueError("Duplicate NBA team-game records")
    if d.duplicated(["team_id","game_date"]).any():
        raise ValueError("Two team games on one Eastern date: cannot safely use shift-based features")
    if (d.groupby("game_id").size()!=2).any():
        raise ValueError("Every scheduled final must have two team boxscores")
    for c in set(BASE_PRIORS)-{"opp_three_pct_allowed"}:
        if c not in d:d[c]=np.nan
        d[c]=pd.to_numeric(d[c],errors="coerce")
    d["opp_three_pct_allowed"]=(
        pd.to_numeric(d.opp_fg3m,errors="coerce")/
        pd.to_numeric(d.opp_fg3a,errors="coerce").replace(0,np.nan)
    )
    d["home"]=d.home.astype(str).str.lower().isin(("true","1"))
    return d.sort_values(["game_date","game_id","team_id"]).reset_index(drop=True)

def rolling_team_features(teams:pd.DataFrame)->pd.DataFrame:
    d=teams.copy()
    d=d.sort_values(["team_id","game_date","game_id"]).reset_index(drop=True)
    groups=d.groupby("team_id",sort=False)
    season_groups=d.groupby(["season","team_id"],sort=False)
    d["games_before"]=groups.cumcount().astype(float)
    d["season_games_before"]=season_groups.cumcount().astype(float)
    dt=pd.to_datetime(d.game_date)
    prev_day=groups.game_date.shift(1)
    rest=(dt-pd.to_datetime(prev_day)).dt.days-1
    d["rest_days"]=rest.clip(lower=0,upper=12).fillna(5).astype(float)
    d["back_to_back"]=(rest==0).astype(float)
    for stat,prior in BASE_PRIORS.items():
        if stat not in d:
            d[stat]=np.nan
        d[stat]=pd.to_numeric(d[stat],errors="coerce")
        grp=d.groupby("team_id",sort=False)[stat]
        prior_values=grp.shift(1)
        for w in ROLLING:
            mean=prior_values.groupby(d.team_id,sort=False).transform(
                lambda v:v.rolling(window=w,min_periods=1).mean())
            weight=d.games_before.clip(upper=w)/(
                d.games_before.clip(upper=w)+8.0)
            d[f"rolling{w}_{stat}"]=weight*mean.fillna(prior)+(1-weight)*prior
        previous_multi=prior_values.groupby(d.team_id,sort=False).transform(
            lambda v:v.rolling(150,min_periods=1).mean())
        weight_multi=d.games_before.clip(upper=150)/(
            d.games_before.clip(upper=150)+20.0)
        d[f"multi_{stat}"]=weight_multi*previous_multi.fillna(prior)+(1-weight_multi)*prior
    return d

def load_tracking(years:list[int])->pd.DataFrame:
    raw=pd.concat([
        read_season_csv("tracked_defense_by_position_game",year)
        for year in sorted(years)
    ],ignore_index=True)
    raw=raw[(raw.game_type.astype(str)=="regular_season")&
            raw.off_position.astype(str).isin(("G","F","C"))].copy()
    raw=raw.rename(columns={"def_team_id":"team_id"})
    need={"season","team_id","game_date","game_id","off_position",
          "partial_possessions","matchup_assists","matchup_potential_assists",
          "player_points"}
    if not need<=set(raw):
        raise ValueError("Tracking source missing: "+str(need-set(raw)))
    for x in ("partial_possessions","matchup_assists",
              "matchup_potential_assists","player_points"):
        raw[x]=pd.to_numeric(raw[x],errors="coerce")
    if raw.duplicated(["season","team_id","off_position","game_date"]).any():
        raise ValueError("Duplicate defender position/date observations")
    return raw

def append_tracked_features(teams:pd.DataFrame,tracking:pd.DataFrame)->pd.DataFrame:
    d=teams.copy()
    d["game_dt"]=pd.to_datetime(d.game_date)
    for pos in ("G","F","C"):
        hist=tracking[tracking.off_position==pos].copy()
        hist["game_dt"]=pd.to_datetime(hist.game_date)
        hist=hist.sort_values(["season","team_id","game_dt"])
        grouping=hist.groupby(["season","team_id"],sort=False)
        for col in ("partial_possessions","matchup_assists",
                    "matchup_potential_assists","player_points"):
            hist["last20_"+col]=grouping[col].transform(
                lambda s:s.rolling(20,min_periods=1).sum())
        hist["last20_n"]=grouping.cumcount().clip(upper=19)+1
        # A per-position tracked observation from date D is only available to
        # predictions on a *later* date (strict merge_asof inequality).
        for name,col,prior in (
            ("assists_per100","matchup_assists",.13),
            ("potential_assists_per100","matchup_potential_assists",.22),
            ("points_per100","player_points",.44),
        ):
            num=hist["last20_"+col]+150*prior
            den=hist["last20_partial_possessions"]+150
            hist[f"tracked_{pos}_{name}"]=100*num/den
        hist[f"tracked_{pos}_matchup_possessions"]=hist["last20_partial_possessions"]
        hist[f"tracked_{pos}_sample_games"]=hist["last20_n"]
        cols=FEATURE_GROUPS["tracked_defender_matchups"]
        these=[c for c in cols if c.startswith(f"tracked_{pos}_")]
        right=hist[["game_dt","team_id","season"]+these].sort_values("game_dt")
        left=d[["game_dt","team_id","season"]].copy().reset_index().sort_values("game_dt")
        joined=pd.merge_asof(left,right,on="game_dt",by=["season","team_id"],
                             direction="backward",allow_exact_matches=False)
        joined=joined.set_index("index").reindex(d.index)
        for col in these:
            d[col]=pd.to_numeric(joined[col],errors="coerce")
    return d.drop(columns=["game_dt"])

def game_feature_frame(years:list[int],*,with_tracking=True)->pd.DataFrame:
    teams=rolling_team_features(load_teams(years))
    # Exact venue/rest conditional records calculated using earlier games
    # only; postgame team scores are never seen by the current row's feature.
    teams=append_pregame_situational_features(teams)
    if with_tracking:
        tracking=load_tracking(years)
        teams=append_tracked_features(teams,tracking)
    h=teams[teams.home].copy()
    a=teams[~teams.home].copy()
    # Neutral site games occasionally have no home flag; skip rather than guess.
    valid=set(h.game_id)&set(a.game_id)
    h=h[h.game_id.isin(valid)]
    a=a[a.game_id.isin(valid)]
    if h.duplicated(["game_id"]).any() or a.duplicated(["game_id"]).any():
        raise ValueError("More than one home or away row")
    fields=set(sum(FEATURE_GROUPS.values(),[])) if with_tracking else set(
        sum([v for k,v in FEATURE_GROUPS.items() if k!="tracked_defender_matchups"],[]))
    fields=sorted(fields)
    for col in fields:
        if col not in h:h[col]=np.nan
        if col not in a:a[col]=np.nan
    shared=["game_id","season","game_date"]
    home=h[shared+["team_id","pts"]+fields].rename(
        columns={"team_id":"home_team_id","pts":"home_score",
                 **{f:"home__"+f for f in fields}})
    away=a[["game_id","team_id","pts"]+fields].rename(
        columns={"team_id":"away_team_id","pts":"away_score",
                 **{f:"away__"+f for f in fields}})
    out=home.merge(away,on="game_id",validate="one_to_one",sort=False)
    out["home_court_advantage"]=1.0
    # Explicit offense-vs-defense interactions, all based on *prior games*.
    pairs={
       "home_3pa_vs_away_3pa_allowed":(
            "home__rolling20_three_point_rate","away__rolling20_opp_fg3a"),
       "away_3pa_vs_home_3pa_allowed":(
            "away__rolling20_three_point_rate","home__rolling20_opp_fg3a"),
       "home_efg_vs_away_allowed":(
            "home__rolling20_efg_pct","away__rolling20_opp_three_pct_allowed"),
       "away_efg_vs_home_allowed":(
            "away__rolling20_efg_pct","home__rolling20_opp_three_pct_allowed"),
       "home_ast_vs_away_ast_allowed":(
            "home__rolling20_ast","away__rolling20_opp_ast"),
       "away_ast_vs_home_ast_allowed":(
            "away__rolling20_ast","home__rolling20_opp_ast"),
    }
    for name,(left,right) in pairs.items():
        out[name]=out[left]*out[right]
    out["winner_home"]=(out.home_score>out.away_score).astype(int)
    out["margin"]=out.home_score-out.away_score
    out["total"]=out.home_score+out.away_score
    if out[["home_score","away_score"]].isna().any().any():
        raise ValueError("Missing score labels")
    return out.sort_values(["game_date","game_id"]).reset_index(drop=True)

def ablation_feature_sets(frame:pd.DataFrame)->dict[str,list[str]]:
    core=["home_court_advantage"] + [
        f"{side}__{col}" for side in ("home","away")
        for col in FEATURE_GROUPS["core"]
    ]
    if any(c not in frame for c in core):
        raise ValueError("Core prior-game columns missing")
    sets={"core":core}
    for group in ("shooting","rebounding_turnovers","observed_tactics",
                  "tracked_defender_matchups","situational_streaks"):
        extra=[f"{side}__{col}" for side in ("home","away")
               for col in FEATURE_GROUPS[group]]
        sets["core+"+group]=core+extra
    sets["core+offense_defense_crossmatchups"]=core+list(CROSS_FEATURES)
    sets["all_evidence"]=list(dict.fromkeys(
        core+sum([v for k,v in sets.items() if k!="core"],[])
    ))
    # Reject any accidental outcome columns or current-game totals as features.
    forbidden={"home_score","away_score","winner_home","margin","total"}
    for name,columns in sets.items():
        if forbidden.intersection(columns):
            raise ValueError("Outcome leakage in feature set "+name)
        if any(c not in frame.columns for c in columns):
            raise ValueError("Missing ablation columns: "+name)
    return sets
