"""Ensure daily GPT v2 reports are honest, readable, and immutable."""
from __future__ import annotations

from datetime import datetime,timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import pytest

from gpt_engine.v2.daily_publish import (
    _append_ledger,read_ledger,render_report,_situation,
    _top_player_lines,_valid_ledger_record
)
from gpt_engine.v2.situational_streaks import add_finished_game_context
from gpt_engine.v2.research import VERSION

def _sim_player(mins,pts,reb,ast,tpm,tov,availability="unknown"):
    return {
        "minutes":{"mean":mins},"pts":{"mean":pts},"reb":{"mean":reb},
        "ast":{"mean":ast},"fg3m":{"mean":tpm},"tov":{"mean":tov},
        "availability":availability
    }

def _example_doc():
    return {
        "game_id":"game:nba:0022600300",
        "game_date_eastern":"2026-11-21",
        "home_team_id":"team:nba:1",
        "away_team_id":"team:nba:2",
        "tip_utc":"2026-11-22T01:00:00Z",
        "cutoff_utc":"2026-11-21T17:00:00Z",
        "model_version":VERSION,
        "prediction_id":"prediction:asof-case",
        "quality_flags":["UNVALIDATED_RESEARCH_MODEL","unconfirmed_lineup"],
        "availability_reports":[{
            "player_id":"player:nba:20","team_id":"team:nba:2",
            "normalized_status":"out","provider_status":"Out",
            "report_utc":"2026-11-21T16:00:00Z","source_id":"espn"
        },{
            "player_id":"player:nba:10","team_id":"team:nba:1",
            "normalized_status":"questionable","provider_status":"Questionable",
            "report_utc":"2026-11-21T16:00:00Z","source_id":"espn"
        }],
        "result":{
            "simulation_count":1000,"seed":20261121,
            "expected_home_score":119.2,"expected_away_score":112.8,
            "home_win_probability":0.665,
            "total":{"mean":232.0,"interval_80":[201,261]},
            "margin":{"mean":6.4,"interval_80":[-16.5,27.0]},
            "overtime_probability":0.049,
            "mc_sampling_error":{"home_win_probability":0.0149},
            "player_statistics":{
                "player:nba:10":_sim_player(34.3,23.8,7.7,6.0,2.4,2.2),
                "player:nba:11":_sim_player(26.2,14.0,3.5,5.0,1.0,1.5),
                "player:nba:20":_sim_player(0,0,0,0,0,0,"out"),
                "player:nba:21":_sim_player(30.1,18,5.0,4.0,2,1.5),
            },
        }
    }

def _teams():
    data=[]
    for i,date in enumerate(["2026-10-24","2026-10-27","2026-10-30"]):
        for tid,home,pts in (("1",True,110),("2",False,99)):
            data.append({"game_id":f"002260{i:04d}",
                "game_date":date,"season":2027,"team_id":tid,
                "team":{"1":"HOM","2":"AWY"}[tid],
                "home":home,"pts":pts,"game_type":"regular_season"})
    return add_finished_game_context(pd.DataFrame(data))

def test_daily_readable_report_has_projected_score_streaks_injuries_players():
    markdown=render_report(
        "2026-11-21",[_example_doc()],
        team_names={"team:nba:1":"HOM","team:nba:2":"AWY"},
        player_names={"player:nba:10":"Starter Example",
                      "player:nba:11":"Second Example",
                      "player:nba:20":"Out Example",
                      "player:nba:21":"Away Example"},
        player_team={"player:nba:10":"team:nba:1",
                     "player:nba:11":"team:nba:1",
                     "player:nba:20":"team:nba:2",
                     "player:nba:21":"team:nba:2"},
        finished=_teams(),generated_at_utc="2026-11-21T18:00:00Z",
        n_scheduled=1
    )
    assert "# GPT v2 NBA daily simulation report" in markdown
    assert "AWY @ HOM" in markdown
    assert "113–119" in markdown
    assert "HOM 66.5%" in markdown
    assert "HOM 119.2" in markdown
    assert "3 prior matching games" not in markdown or "NOT a calibrated probability" in markdown
    assert "Out Example: out" in markdown
    assert "Starter Example †" in markdown
    assert "| Team | Player | Min | PTS | REB | AST | 3PM | TOV |" in markdown
    assert "| HOM | Starter Example † |" in markdown
    assert "23.8" in markdown
    assert "| Out Example" not in markdown
    assert "uncalibrated" in markdown.lower()
    assert "2026-11-21T17:00:00Z UTC" in markdown
    assert "November" not in markdown or "research" in markdown.lower()

def test_streak_report_excludes_current_game_result():
    source=_teams()
    label=_situation(source,"team:nba:1","2026-11-21",2027,"home")
    assert "Rest" not in label or "rest" in label.lower()
    assert "NOT a calibrated probability" in label or "no matching games" in label
    extra=pd.concat([source,pd.DataFrame([
        {"game_id":"0022600999","game_date":"2026-11-21",
         "season":2027,"team_id":"1","home":True,"pts":1,"venue_valid":True,
         "venue":"home","rest_bucket":"2","won":0,"true_rest_days":2},
        {"game_id":"0022600999","game_date":"2026-11-21",
         "season":2027,"team_id":"2","home":False,"pts":123,"venue_valid":True,
         "venue":"away","rest_bucket":"2","won":1,"true_rest_days":2},
    ])],ignore_index=True)
    assert _situation(extra,"team:nba:1","2026-11-21",2027,"home")==label

def test_current_conditional_run_excludes_nonmatching_games_and_future():
    games=_teams()
    # Two previous home games after exactly 2 full days' rest are both wins.
    label=_situation(games,"team:nba:1","2026-11-02",2027,"home")
    assert "2–0" in label
    assert "last 2 qualifying games: WIN outcomes in a row among MATCHING games only" in label
    assert "2026-10-30 (W)" in label
    assert "2026-10-27 (W)" in label
    # Include a future loss: as-of date report must remain unchanged.
    poisoned=pd.concat([games,pd.DataFrame([{
        "game_id":"0022699999","game_date":"2026-11-02",
        "season":2027,"team_id":"1","home":True,"pts":12,
        "venue_valid":True,"venue":"home","rest_bucket":"2",
        "won":0,"true_rest_days":2
    },{
        "game_id":"0022699999","game_date":"2026-11-02",
        "season":2027,"team_id":"2","home":False,"pts":111,
        "venue_valid":True,"venue":"away","rest_bucket":"2",
        "won":1,"true_rest_days":2
    }])],ignore_index=True)
    assert _situation(poisoned,"team:nba:1","2026-11-02",2027,"home")==label


def test_last_five_one_four_can_coexist_with_dated_matching_wins():
    # Last five matches: 1 W, 4 L. Genuine CURRENT overall streak: L4.
    # Last two home games following exactly two full days off: both W.
    dates=["2026-10-01","2026-10-04","2026-10-05",
           "2026-10-07","2026-10-10","2026-10-11",
           "2026-10-13","2026-10-15","2026-10-17"]
    winners=["A","A","B","B","A","B","B","B","B"]
    home_dates={"2026-10-01","2026-10-04","2026-10-10"}
    rows=[]
    for i,(date,winner) in enumerate(zip(dates,winners)):
        for team in ("A","B"):
            rows.append({
                "game_id":f"002260{i:04d}", "game_date":date,
                "season":2027, "team_id":team,
                "home":((date in home_dates)==(team=="A")),
                "pts":114 if team==winner else 97,
            })
    finished=add_finished_game_context(pd.DataFrame(rows))
    from gpt_engine.v2.daily_publish import _recent_form
    form=_recent_form(finished,"team:nba:A","2026-10-20")
    assert "last 5: 1–4" in form
    assert "current overall streak (uninterrupted games): **L4**" in form
    situation=_situation(finished,"team:nba:A","2026-10-20",2027,"home")
    assert "exactly 2 full rest days" in situation
    assert "**2–0**" in situation
    assert "2026-10-10 (W)" in situation
    assert "2026-10-04 (W)" in situation
    assert "not an overall streak" in situation
    assert "NOT a calibrated probability" in situation


def test_append_only_ledger_no_future_issued_forecasts():
    row={"game_id":"game:nba:0022600300",
         "game_date_eastern":"2026-11-21","tip_utc":"2026-11-22T01:00:00Z",
         "cutoff_utc":"2026-11-21T17:00:00Z","model_version":VERSION,
         "prediction_id":"prediction:source-evidence",
         "file":"gpt_engine/v2/artifacts/reports/file.json"}
    with TemporaryDirectory() as folder:
        p=Path(folder)/"forecast_log.jsonl"
        _append_ledger(p,[],[row])
        assert read_ledger(p)==[row]
        before=p.read_bytes()
        with pytest.raises(ValueError,match="already issued"):
            _append_ledger(p,read_ledger(p),[row])
        assert p.read_bytes()==before
        with pytest.raises(ValueError,match="after-tip"):
            _valid_ledger_record({**row,"cutoff_utc":"2026-11-22T01:30:00Z"})
        with pytest.raises(ValueError,match="after-tip"):
            _valid_ledger_record({**row,"cutoff_utc":"2026-11-22T01:00:00Z"})

def test_unknown_and_out_projections_not_mislabeled_as_confident():
    stats=_example_doc()["result"]["player_statistics"]
    result=_top_player_lines(
        stats,"team:nba:2",
        {"player:nba:20":"Definitely Out","player:nba:21":"Uncertain"},
        {"player:nba:20":"team:nba:2","player:nba:21":"team:nba:2"}
    )
    assert len(result)==1
    assert result[0][0]=="Uncertain †"
    assert result[0][2]=="18.0"

def test_missing_data_is_not_filled_with_imaginary_matchups():
    report=render_report("2026-11-21",[],
        team_names={},player_names={},player_team={},
        finished=None,generated_at_utc="2026-11-21T10:00:00Z",
        n_scheduled=0)
    assert "No valid pre-tip GPT v2 forecasts recorded" in report
    assert "0 games" in report
