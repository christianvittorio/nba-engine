"""Database immutability, UTC and strict injury/lineup as-of contract tests."""
from datetime import datetime, timezone, timedelta
import json
import sqlite3
import unittest

from gpt_engine.v2.contracts import (
    Availability, FeatureSnapshot, GameContext, Prediction, Provenance,
    display_tip, internal_id, iso, utc)
from gpt_engine.v2.warehouse import (
    connect,register_source,register_team,register_player,upsert_game,
    put_availability,asof_availability,asof_lineup,map_provider_id,
    save_snapshot,save_model_version,save_prediction
)

DAY="2026-11-21"
TIP="2026-11-22T00:30:00Z"
CUTOFF="2026-11-21T19:00:00Z"
PREV="2026-11-21T16:00:00Z"
AFTER="2026-11-22T02:00:00Z"
GAME="game:nba:0022600001"

def seeded():
    c=connect()
    register_source(c,"nba","Official NBA stats")
    register_source(c,"inj","NBA official injury report")
    register_team(c,"team:nba:1","Hawks")
    register_team(c,"team:nba:2","Celtics")
    for i in range(1,4):
        register_player(c,f"player:nba:{i}",f"Player {i}")
    upsert_game(c,GAME,2027,DAY,TIP,"team:nba:1","team:nba:2",
                "scheduled",Provenance("nba",PREV))
    return c

class TestWarehouse(unittest.TestCase):
    def test_utc_and_time_zone(self):
        self.assertEqual(iso("2026-11-21T08:00:00+08:00"),"2026-11-21T00:00:00Z")
        self.assertIn("08:30 AM",display_tip(TIP))
        with self.assertRaises(ValueError):
            iso("2026-11-21T08:00:00")

    def test_provider_mapping_conflict(self):
        c=seeded()
        map_provider_id(c,"player","player:nba:1","nba","123",PREV)
        self.assertEqual(c.execute("SELECT internal_id FROM provider_ids").fetchone()[0],
                         "player:nba:1")
        with self.assertRaises(ValueError):
            map_provider_id(c,"player","player:nba:2","nba","123",PREV)
        with self.assertRaises(KeyError):
            map_provider_id(c,"player","player:nba:99","nba","999",PREV)

    def test_availability_report_time_and_ingest_time_must_both_be_eligible(self):
        c=seeded()
        put_availability(c,"r1",GAME,Availability("player:nba:1","questionable",
            "Questionable",PREV,"inj"),Provenance("inj",PREV))
        put_availability(c,"r2",GAME,Availability("player:nba:1","out",
            "Out",AFTER,"inj"),Provenance("inj",AFTER))
        # Retrospectively downloaded report stamped before cutoff is excluded.
        put_availability(c,"r3",GAME,Availability("player:nba:2","out",
            "Out",PREV,"inj"),Provenance("inj",AFTER))
        statuses=asof_availability(c,GAME,CUTOFF)
        self.assertEqual(len(statuses),1)
        self.assertEqual(statuses[0]["normalized_status"],"questionable")
        self.assertEqual(statuses[0]["source_id"],"inj")

    def test_lineups_do_not_reach_back_in_time(self):
        c=seeded()
        c.execute("INSERT INTO lineup_reports "
            "(lineup_id,game_id,team_id,player_id,lineup_type,confirmation_utc,"
            "source_id,retrieved_at_utc) VALUES(?,?,?,?,?,?,?,?)",
            ("lineup-1",GAME,"team:nba:1","player:nba:1",
             "confirmed_starter",AFTER,"nba",AFTER))
        c.commit()
        self.assertEqual(asof_lineup(c,GAME,CUTOFF),[])

    def test_snapshot_and_prediction_are_immutable_and_pre_tip(self):
        c=seeded()
        snap=FeatureSnapshot(GAME,CUTOFF,"team-feature-v2",
                             {"expected_possessions":99.0},
                             {"injury_missing":True},("nba",))
        sid=save_snapshot(c,snap,max_source_timestamp_utc=PREV,
                          generated_at_utc=CUTOFF)
        save_model_version(c,"v2-test","research",{"seed":7})
        p=Prediction(GAME,sid,"v2-test",CUTOFF,
                     "2026-11-21T19:01:00Z","base",{"p_home":.55})
        pid=save_prediction(c,p)
        self.assertEqual(c.execute("SELECT prediction_id FROM pregame_predictions").fetchone()[0],pid)
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute("UPDATE pregame_predictions SET prediction_json='{}' WHERE prediction_id=?",(pid,))
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute("UPDATE feature_snapshots SET features_json='{}' WHERE snapshot_id=?",(sid,))
        with self.assertRaises(ValueError):
            save_prediction(c,Prediction(GAME,sid,"v2-test",CUTOFF,AFTER,"after",{}))
        with self.assertRaises(ValueError):
            save_snapshot(c,FeatureSnapshot(GAME,CUTOFF,"future",{},{}),
                          max_source_timestamp_utc=AFTER)

    def test_database_rejects_inconsistent_cutoff_even_if_bypassed(self):
        c=seeded()
        sid=save_snapshot(c,FeatureSnapshot(GAME,CUTOFF,"x",{}),
                          generated_at_utc=CUTOFF)
        save_model_version(c,"v2-test","research",{})
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute("INSERT INTO pregame_predictions("
                      "prediction_id,game_id,snapshot_id,model_version,cutoff_utc,"
                      "created_at_utc,prediction_json) VALUES(?,?,?,?,?,?,?)",
                      ("fake",GAME,sid,"v2-test",PREV,PREV,"{}"))

if __name__=="__main__":
    unittest.main()
