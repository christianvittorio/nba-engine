"""Chronological feature and model selection tests, including future outcome injection."""
import unittest
import pandas as pd
import numpy as np

from gpt_engine.v2.contracts import GameContext
from gpt_engine.v2.features import build_team_features,flatten_team_features
from gpt_engine.v2.models import Elo,chronological_split,train_candidates
from gpt_engine.v2.tactics import tracked_matchup_feature,evidence_only_explanation

GAME=GameContext("game:nba:900",2027,"2026-11-21","2026-11-22T01:00:00Z",
                 "1","2")
CUTOFF="2026-11-21T16:00:00Z"

def dummy_history():
    rows=[]
    for i in range(65):
        day=str((pd.Timestamp("2026-09-01")+pd.Timedelta(days=i)).date())
        for team,opp in (("1","2"),("2","1")):
            rows.append({
                "season":2027,"game_id":f"game:nba:{i}",
                "game_date":day,"game_type":"regular_season",
                "team_id":team,"opp_team_id":opp,
                "off_rating":110+i%9+(3 if team=="1" else 0),
                "def_rating":108+i%7-(2 if team=="1" else 0),
                "net_rating":5 if team=="1" else -5,
                "pace":96+i%8,"poss":96+i%8,
                "efg_pct":.51+i%6*.005,
                "ts_pct":.55,"three_point_rate":.39,
                "fta_rate":.25,"ast":25,"tov":12,
                "oreb":12,"dreb":34,
                "opp_fg3a":35,"opp_fg3m":12,"opp_ast":24,
                "opp_efg_pct":.52,"tm_tov_pct":.13,
                "oreb_pct":.27,"dreb_pct":.74,
            })
    # Include future and current date scores as an obvious poison.
    rows.extend([{
        **dict(rows[-1]),
        "game_id":f"game:nba:poison-{offset}","game_date":day,
        "off_rating":1000.0,"def_rating":20.0,"pace":700.0,
        "efg_pct":.99
    } for offset,day in enumerate(["2026-11-21","2026-11-22"])])
    return pd.DataFrame(rows)

class TestFeatures(unittest.TestCase):
    def test_current_day_and_future_are_never_features(self):
        df=dummy_history()
        snap1=build_team_features(df,GAME,CUTOFF)
        snap2=build_team_features(df[~df.game_id.str.contains("poison")],GAME,CUTOFF)
        self.assertEqual(snap1.features,snap2.features)
        self.assertLess(snap1.features["expected_possessions"],110)
        flat=flatten_team_features(snap1)
        self.assertIn("home__rolling20_efg_pct",flat)
        self.assertIn("home__strength_of_schedule",flat)

    def test_post_tip_cutoff_and_future_report_refused(self):
        df=dummy_history()
        with self.assertRaises(ValueError):
            build_team_features(df,GAME,"2026-11-22T02:00:00Z")
        with self.assertRaises(ValueError):
            build_team_features(df,GAME,CUTOFF,availability=[{
                "report_utc":"2026-11-22T01:01:00Z",
                "normalized_status":"out"
            }])
        with self.assertRaises(ValueError):
            build_team_features(df,GAME,CUTOFF,lineup=[{
                "confirmation_utc":"2026-11-22T01:01:00Z"
            }])

    def test_observed_tactics_do_not_claim_coach_scheme(self):
        snap=build_team_features(dummy_history(),GAME,CUTOFF)
        formatted=evidence_only_explanation({
            "home_win_probability":.56,"expected_home_score":115,
            "expected_away_score":110
        },snap.features)
        self.assertIsNone(formatted["observed"]["home"]["verified_defensive_coverages"])
        self.assertFalse(formatted["uncertainties"]["tactical_coverage_verified"])

    def test_defender_matchup_uses_only_previous_games(self):
        source=pd.DataFrame([
            {"game_date":"2026-11-18","game_id":"1","def_team_id":"2",
             "off_position":"F","partial_possessions":100,
             "matchup_assists":14,"matchup_potential_assists":22},
            {"game_date":"2026-11-21","game_id":"2","def_team_id":"2",
             "off_position":"F","partial_possessions":100,
             "matchup_assists":1000,"matchup_potential_assists":1000},
        ])
        evidence=tracked_matchup_feature(source,"2026-11-21","2","F")
        self.assertEqual(evidence["matchup_games"],1)
        self.assertEqual(evidence["observed_assists_per_100_matchup_possessions"],14.0)
        self.assertEqual(evidence["quality"],"broad_position_label")

class TestModels(unittest.TestCase):
    def test_elo_forecast_is_day_before_score_update(self):
        games=pd.DataFrame([
            {"season":2027,"game_date":"2026-11-19","game_id":"a",
             "home_team_id":"1","away_team_id":"2",
             "home_score":100,"away_score":95},
            {"season":2027,"game_date":"2026-11-20","game_id":"b",
             "home_team_id":"1","away_team_id":"2",
             "home_score":120,"away_score":60},
            {"season":2027,"game_date":"2026-11-20","game_id":"c",
             "home_team_id":"1","away_team_id":"2",
             "home_score":130,"away_score":50},
        ])
        first=Elo().pregame_series(games)
        altered=games.copy()
        altered.loc[altered.game_id=="b","home_score"]=50
        second=Elo().pregame_series(altered)
        for game in ("b","c"):
            self.assertEqual(
                float(first.loc[first.game_id==game,"home_win_probability"].iloc[0]),
                float(second.loc[second.game_id==game,"home_win_probability"].iloc[0]))

    def test_ordered_splits_and_ridge_selection(self):
        rng=np.random.default_rng(2)
        days=pd.date_range("2024-01-01",periods=120)
        X=rng.normal(size=120)
        frames=pd.DataFrame({
            "game_date":days.strftime("%Y-%m-%d"),
            "momentum":X,"home_score":115+5*X+rng.normal(0,3,120),
            "away_score":109-2*X+rng.normal(0,3,120)
        })
        tr,v,te=chronological_split(frames,"2024-03-01","2024-04-01")
        self.assertLess(tr.game_date.max(),v.game_date.min())
        self.assertLess(v.game_date.max(),te.game_date.min())
        result=train_candidates(frames,["momentum"],"2024-03-01","2024-04-01")
        self.assertFalse(result["uses_test_to_select"])
        self.assertEqual(result["train_n"],60)
        self.assertGreater(result["test_n"],0)
        self.assertLess(result["test_metrics"]["total_mae"],20)
        predicted=result["candidate"].predict({"momentum":0.3})
        self.assertAlmostEqual(predicted.margin,predicted.home_mean-predicted.away_mean)

if __name__=="__main__":
    unittest.main()
