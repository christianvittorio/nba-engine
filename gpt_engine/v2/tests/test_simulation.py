"""End-to-end basketball accounting, player minutes, injury scenario and odds guards."""
import unittest
import numpy as np
import pandas as pd

from gpt_engine.v2.players import (
    PlayerProjection,allocate_minutes,conditional_rotation,estimate_player,
    probability_at_least)
from gpt_engine.v2.simulation import TeamSettings,Matchup,simulate_game,check_convergence
from gpt_engine.v2.scenarios import conditional_scenarios
from gpt_engine.v2.season import simulate_season
from gpt_engine.v2.evaluation import evaluate,paired_compare,odds_edge

def sample_roster(team):
    vals=[]
    for i,minutes in enumerate([41,38,35,32,29,25,22,18]):
        rate={"pts":(.75 if i==0 else .42),"reb":.14,"ast":.105,"stl":.024,
              "blk":.015,"tov":.055,"fgm":.17,"fga":.34,
              "fg3m":.065,"fg3a":.15,"ftm":.09,"fta":.11}
        vals.append(PlayerProjection(
            player_id=f"{team}:player:{i}",team_id=team,minutes=minutes,
            minutes_sd=5,usage_weight=.35+i*.025,rates_per_min=rate,
            field_goal_pct=.47,three_point_pct=.37,free_throw_pct=.79,
            sample_games=65,availability="confirmed_available"))
    return allocate_minutes(vals)

def sample_game():
    home=TeamSettings("home",116,113,.40,.13,.28)
    away=TeamSettings("away",113,115,.34,.14,.26)
    return Matchup(home,away,100,2.0)

class TestSimulation(unittest.TestCase):
    def test_ball_and_minute_accounting(self):
        h=sample_roster("home")
        a=sample_roster("away")
        r=simulate_game(sample_game(),h,a,n=55,seed=79,batch_size=6,
                        include_samples=True,thresholds={
                        "home:player:0":{"pts":[20,30],"ast":[5]}})
        self.assertEqual(r["simulation_count"],55)
        self.assertEqual(len(r["_samples"]),55)
        self.assertEqual(len(r["player_statistics"]),16)
        for i,row in enumerate(r["_samples"]):
            h_pts=sum(r["_player_samples"][p.player_id]["pts"][i] for p in h)
            a_pts=sum(r["_player_samples"][p.player_id]["pts"][i] for p in a)
            h_min=sum(r["_player_samples"][p.player_id]["minutes"][i] for p in h)
            a_min=sum(r["_player_samples"][p.player_id]["minutes"][i] for p in a)
            self.assertEqual(h_pts,row[0])
            self.assertEqual(a_pts,row[1])
            self.assertEqual(row[2],row[0]+row[1])
            self.assertEqual(row[3],row[0]-row[1])
            self.assertAlmostEqual(h_min,240+25*row[4],places=2)
            self.assertAlmostEqual(a_min,240+25*row[4],places=2)
            for player in h+a:
                stat=r["_player_samples"][player.player_id]
                fgm=stat["fgm"][i];fg3m=stat["fg3m"][i];ftm=stat["ftm"][i]
                self.assertEqual(stat["pts"][i],2*fgm+fg3m+ftm)
                self.assertLessEqual(fgm,stat["fga"][i])
                self.assertLessEqual(fg3m,stat["fg3a"][i])
                self.assertEqual(stat["reb"][i],stat["oreb"][i]+stat["dreb"][i])
        self.assertGreaterEqual(r["home_win_probability"],0)
        self.assertLessEqual(r["home_win_probability"],1)
        self.assertEqual(r["total"]["interval_80"].__len__(),2)
        self.assertIn("20",r["player_statistics"]["home:player:0"]["threshold_probabilities"]["pts"])
        shooting=r["player_statistics"]["home:player:0"]["field_goal_percentage"]
        self.assertGreater(shooting["eligible_simulations"],0)
        self.assertGreaterEqual(shooting["ratio_of_expected_totals"],0)
        self.assertLessEqual(shooting["ratio_of_expected_totals"],1)

    def test_market_histograms_are_exact_and_do_not_change_original_draws(self):
        h=sample_roster("home");a=sample_roster("away")
        original=simulate_game(sample_game(),h,a,n=55,seed=93,
                               include_samples=True)
        saved=simulate_game(sample_game(),h,a,n=55,seed=93,
                            include_samples=True,
                            include_market_distributions=True)
        self.assertEqual(saved["_samples"],original["_samples"])
        self.assertEqual(saved["home_win_probability"],
                         original["home_win_probability"])
        self.assertEqual(saved["expected_home_score"],
                         original["expected_home_score"])
        dist=saved["market_distributions"]
        self.assertEqual(sum(dist["home_margin_counts"].values()),55)
        self.assertEqual(sum(dist["game_total_counts"].values()),55)
        for p in h+a:
            for stat in ("pts","reb","ast","fg3m"):
                self.assertEqual(sum(dist["player_counts"][p.player_id][stat].values()),55)
        for i,row in enumerate(original["_samples"]):
            self.assertGreater(dist["home_margin_counts"][str(int(row[3]))],0)
            self.assertGreater(dist["game_total_counts"][str(int(row[2]))],0)

    def test_reproducible_across_batch_sizes(self):
        h=sample_roster("home");a=sample_roster("away")
        one=simulate_game(sample_game(),h,a,50,123,7)
        two=simulate_game(sample_game(),h,a,50,123,20)
        self.assertEqual(one["home_win_probability"],two["home_win_probability"])
        self.assertEqual(one["expected_home_score"],two["expected_home_score"])
        self.assertEqual(one["player_statistics"],two["player_statistics"])

    def test_required_minimum_and_roster_size(self):
        h=sample_roster("home");a=sample_roster("away")
        with self.assertRaises(ValueError):
            simulate_game(sample_game(),h,a,49)
        with self.assertRaises(ValueError):
            allocate_minutes(h[:4])

    def test_conditional_injury_changes_minutes_and_recomputes_all(self):
        h=sample_roster("home");a=sample_roster("away")
        out=conditional_rotation(h,{"home:player:0":"out"})
        self.assertEqual(out[0].minutes,0)
        self.assertAlmostEqual(sum(x.minutes for x in out),240,places=3)
        cases=conditional_scenarios(sample_game(),h,a,[
            {"label":"all-play","availability":{},"source_id":"official"},
            {"label":"star-out","availability":{"home:player:0":"out"},
             "source_id":"official","source_timestamp":"2026-11-21T18:00:00Z"},
        ],n=50,seed=5)
        self.assertEqual(len(cases),2)
        self.assertIsNone(cases[0]["probability"])
        self.assertIsNone(cases[1]["probability"])
        self.assertEqual(cases[1]["player_statistics"]["home:player:0"]["minutes"]["mean"],0)
        self.assertNotEqual(cases[0]["scenario_adjusted_home_off_rating"],
                            cases[1]["scenario_adjusted_home_off_rating"])

    def test_player_projection_is_prior_game_only(self):
        base=[{"game_id":f"{i}","player_id":"X","game_date":f"2026-10-{i+1:02d}",
               "min":30,"pts":15,"ast":5,"fga":12,"fgm":6,"fg3a":4,
               "fg3m":2,"fta":3,"ftm":2} for i in range(10)]
        poison={**base[-1],"game_id":"future","game_date":"2026-11-21",
                "pts":1000,"ast":500,"min":48}
        d1=pd.DataFrame(base)
        d2=pd.DataFrame(base+[poison])
        p1=estimate_player(d1,"X","home","2026-11-21",
                           availability="confirmed_available")
        p2=estimate_player(d2,"X","home","2026-11-21",
                           availability="confirmed_available")
        self.assertEqual(p1.stats_mean(),p2.stats_mean())

    def test_probabilities_are_calculated_not_asserted(self):
        p=probability_at_least([1,2,2,3,4],3)
        self.assertEqual(p["p_at_least"],.4)

    def test_season_wins_and_missing_bracket_truth(self):
        schedule=[
            {"game_id":"a","home_team_id":"1","away_team_id":"2",
             "actual_home_score":103,"actual_away_score":90},
            {"game_id":"b","home_team_id":"1","away_team_id":"2","p_home":.6},
            {"game_id":"c","home_team_id":"2","away_team_id":"1","p_home":.55},
        ]
        r=simulate_season(schedule,{"1":"East","2":"East"},100,7)
        self.assertEqual(r["scheduled_games"],3)
        self.assertEqual(r["completed_games"],1)
        self.assertAlmostEqual(sum(x["wins_mean"] for x in r["teams"].values()),3,places=3)
        self.assertIsNone(r["teams"]["1"]["championship_probability"])

class TestEvaluation(unittest.TestCase):
    def test_only_real_pregame_forecasts_and_odds(self):
        game={"game_id":"g","tip_utc":"2026-11-21T21:00:00Z"}
        pred={"game_id":"g","model_version":"v2","cutoff_utc":"2026-11-21T19:00:00Z",
              "created_at_utc":"2026-11-21T19:01:00Z",
              "expected_home_score":108,"expected_away_score":104,
              "home_win_probability":.60}
        final={"home_score":110,"away_score":102}
        m=evaluate([pred],{"g":game},{"g":final})
        self.assertEqual(m["n"],1)
        self.assertLess(m["brier"],1)
        matched=paired_compare([pred],[dict(pred,model_version="other")],
                               {"g":game},{"g":final})
        self.assertEqual(matched["matched_games"],1)
        with self.assertRaises(ValueError):
            evaluate([dict(pred,created_at_utc="2026-11-21T21:01:00Z")],
                     {"g":game},{"g":final})
        market={"game_id":"g","observed_at_utc":"2026-11-21T18:00:00Z",
                "retrieved_at_utc":"2026-11-21T18:01:00Z","decimal_odds":2.0}
        self.assertGreater(odds_edge(pred,market,game,"home")["expected_net_return_per_unit"],0)
        with self.assertRaises(ValueError):
            odds_edge(pred,dict(market,retrieved_at_utc="2026-11-22T10:00:00Z"),
                      game,"home")

if __name__=="__main__":
    unittest.main()
