"""Verified basketball tendencies, tracked defender-matchup evidence and careful labels.

This module never labels a coach 'switch-heavy' or 'drop-heavy' without
trusted scheme annotations. Player-position comparisons use the published
G/F/C/hybrid label; PG/SG/SF/PF/C labels cannot be assumed from a name.
"""
from __future__ import annotations
import math
import pandas as pd

def tracked_matchup_feature(tracked_by_game:pd.DataFrame,game_date:str,
                            defense_team_id:str,off_position:str,
                            *,min_possessions:float=150.0,
                            max_games:int=25)->dict:
    need={"game_date","def_team_id","off_position","partial_possessions",
          "matchup_assists","matchup_potential_assists","game_id"}
    if not need <= set(tracked_by_game):
        raise ValueError(f"Missing tracked matchup fields {sorted(need-set(tracked_by_game))}")
    df=tracked_by_game.copy()
    df["game_date"]=df.game_date.astype(str).str[:10]
    df=df[(df.game_date<game_date)&
          (df.def_team_id.astype(str)==str(defense_team_id))&
          (df.off_position.astype(str).str.upper()==str(off_position).upper())]
    if df.empty:
        return {"available":False,"reason":"No pregame matchup history","position":off_position}
    df=df.sort_values(["game_date","game_id"]).tail(max_games)
    n=float(pd.to_numeric(df.partial_possessions,errors="coerce").sum())
    ast=float(pd.to_numeric(df.matchup_assists,errors="coerce").sum())
    potential=float(pd.to_numeric(df.matchup_potential_assists,errors="coerce").sum())
    if not math.isfinite(n) or n<=0:
        return {"available":False,"reason":"No valid tracked possessions","position":off_position}
    # A prior 150 matchup possessions at a 0.13 assist / possession rate.
    # This is a transparent regularization prior, not a claimed NBA average.
    prior_assists_per_poss=.13
    shrunk=(ast+min_possessions*prior_assists_per_poss)/(n+min_possessions)
    return {
        "available":True,
        "defense_team_id":str(defense_team_id),
        "offensive_position_label":str(off_position),
        "matchup_games":int(df.game_id.nunique()),
        "matchup_possessions":round(n,2),
        "observed_assists_per_100_matchup_possessions":round(100*ast/n,3),
        "shrunk_assists_per_100_matchup_possessions":round(100*shrunk,3),
        "observed_potential_assists_per_100_matchup_possessions":round(100*potential/n,3),
        "uncertainty_flag":n<min_possessions,
        "interpretation":"Observed tracked player-vs-defender assignments; not exclusive matchup causality",
        "quality":"broad_position_label" if off_position in ("G","F","C","G-F","F-C") else "source_position_only",
    }

def observed_tactics(team_features:dict)->dict:
    """Only observable metrics: not a coach's verified system or play calls."""
    accepted={
        "pace":"rolling20_pace",
        "three_attempt_rate":"rolling20_three_point_rate",
        "offensive_rebounding_rate":"rolling20_oreb_pct",
        "turnover_rate":"rolling20_tm_tov_pct",
        "effective_field_goal_rate":"rolling20_efg_pct",
        "opponent_three_point_attempts_allowed":"rolling20_opp_fg3a",
        "assists_allowed":"rolling20_opp_ast",
        "defensive_efficiency":"rolling20_def_rating",
    }
    return {
        "observed_statistical_style":{
            friendly:round(float(team_features[key]),5)
            for friendly,key in accepted.items()
            if key in team_features and team_features[key] is not None
        },
        "coach_identity":None,
        "coach_tenure_utc":None,
        "verified_defensive_coverages":None,
        "verified_pick_and_roll_system":None,
        "verified_transition_frequency":None,
        "evidence_type":"Historical prior-game observational team rates, not coach causality",
    }

def evidence_only_explanation(model_output:dict,feature_snapshot:dict)->dict:
    """A structured factual explanation; LLM output is not used to generate numbers."""
    required={"home_win_probability","expected_home_score","expected_away_score"}
    if not required<=set(model_output):
        raise ValueError("Explanations must start from numeric model output")
    return {
        "model_numbers":{
            key:float(model_output[key]) for key in sorted(required)
        },
        "observed":{
            "home":observed_tactics(feature_snapshot.get("home",{})),
            "away":observed_tactics(feature_snapshot.get("away",{})),
        },
        "uncertainties":{
            "injury_report_available":bool(feature_snapshot.get("availability")),
            "lineup_confirmation_available":bool(feature_snapshot.get("lineup")),
            "tactical_coverage_verified":False,
        },
        "explanation_policy":[
            "Quote model values exactly; never invent or overwrite numeric probabilities.",
            "Keep observed data, estimates, and qualitative claims in separate fields.",
            "Do not assert coach tactics without timestamped supporting records.",
        ]
    }
