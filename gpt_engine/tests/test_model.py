"""Offline safety tests for the independent GPT lane."""
import json
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from gpt_engine.model import Game, TeamModel, build_model, evaluate_saved, history_before, load_games
from gpt_engine.run import existing_forecasts, markdown_report


class TestModel(unittest.TestCase):
    def test_deterministic_and_valid_probabilities(self):
        games = [
            Game(2025, 1, "BOS", "ATL", 115, 98),
            Game(2025, 2, "ATL", "BOS", 99, 108),
        ]
        model = build_model(games, 2026, "2026-11-21")
        p = model.predict("BOS", "ATL")
        self.assertEqual(p, model.predict("BOS", "ATL"))
        self.assertGreater(p["p_home"], 0)
        self.assertLess(p["p_home"], 1)
        self.assertAlmostEqual(p["mean_home"] + p["mean_away"], p["mean_total"], delta=0.002)
        self.assertAlmostEqual(p["mean_home"] - p["mean_away"], p["mean_margin"], delta=0.002)

    def test_same_day_and_future_scores_are_never_learned(self):
        old = Game(2025, 1, "BOS", "ATL", 110, 100)
        yesterday = Game(2026, 2, "ATL", "BOS", 105, 99, "2026-11-20")
        today = Game(2026, 3, "BOS", "ATL", 45, 140, "2026-11-21")
        future = Game(2026, 4, "BOS", "ATL", 30, 160, "2026-11-22")
        unknown = Game(2026, 5, "BOS", "ATL", 30, 160)
        history = history_before([old, yesterday, today, future, unknown], 2026, "2026-11-21")
        self.assertEqual(history, [old, yesterday])
        p1 = build_model([old, yesterday], 2026, "2026-11-21").predict("BOS", "ATL")
        p2 = build_model([old, yesterday, today, future, unknown], 2026, "2026-11-21").predict("BOS", "ATL")
        self.assertEqual(p1, p2)

    def test_result_union_and_conflict_detection(self):
        with TemporaryDirectory() as folder:
            p = Path(folder) / "one.sqlite"
            q = Path(folder) / "two.sqlite"
            for path, pts in ((p, 111), (q, 111)):
                con = sqlite3.connect(path)
                con.executescript(
                    "CREATE TABLE games(season INTEGER, game_id INTEGER, home TEXT, away TEXT);"
                    "CREATE TABLE results(season INTEGER, game_id INTEGER, home_pts INTEGER, away_pts INTEGER);"
                    "CREATE TABLE game_dates(season INTEGER, game_id INTEGER, date TEXT);"
                    "INSERT INTO games VALUES(2026, 100, 'BOS', 'ATL');"
                    f"INSERT INTO results VALUES(2026, 100, {pts}, 99);"
                    "INSERT INTO game_dates VALUES(2026, 100, '2026-11-20');"
                )
                con.commit()
                con.close()
            games = load_games([p, q])
            self.assertEqual(len(games), 1)
            self.assertEqual(games[0].date, "2026-11-20")
            con = sqlite3.connect(q)
            con.execute("UPDATE results SET home_pts=115")
            con.commit()
            con.close()
            with self.assertRaises(ValueError):
                load_games([p, q])

    def test_only_forecasts_made_before_tip_are_graded(self):
        games = [Game(2026, 101, "BOS", "ATL", 110, 100, "2026-11-20")]
        base = dict(season=2026, game_id=101, p_home=0.75,
                    mean_margin=5, mean_total=210,
                    tip_utc="2026-11-20T23:00:00Z")
        past = dict(base, made_at_utc="2026-11-20T20:00:00Z")
        future = dict(base, made_at_utc="2026-11-21T20:00:00Z")
        self.assertEqual(evaluate_saved([past], games)["n"], 1)
        self.assertEqual(evaluate_saved([future], games)["n"], 0)

    def test_report_does_not_repeat_previous_day(self):
        report = markdown_report("2026-11-21", [], {}, {"n": 0}, 0, 0)
        self.assertIn("No valid pregame GPT forecasts", report)
        self.assertNotIn("2026-11-20", report)


if __name__ == "__main__":
    unittest.main()
