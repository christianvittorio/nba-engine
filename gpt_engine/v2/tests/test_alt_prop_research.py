"""Strict 90% season-hit alternate props: sourced usage, broad DvP,
sampling uncertainty, no fabricated sportsbook ladders or same-game parlays.
"""
import json
import sqlite3

import pytest

from gpt_engine.v2.alt_prop_research import (
    highest_90pct_line, wilson_lower_bound, defense_ranks,
    _quote_candidates, _team_usage, _positions, build_alt_prop_research,
)

TIP="2026-11-22T01:00:00Z"
NOW="2026-11-21T16:10:00Z"
PID="player:nba:111"
GID="game:nba:0022600999"


def test_alt_ladder_has_true_90pct_season_and_recent_sample():
    values=[17]*11+[9] # 11/12 at 16.5; last five 4/5
    line=highest_90pct_line(values,"pts")
    assert line["line"]==16.5
    assert line["hits"]==11
    assert line["games"]==12
    assert line["raw_season_hit_rate"]==pytest.approx(11/12)
    assert line["last_five_hits"]==4
    assert line["wilson_95pct_lower_descriptive"]<.90
    assert line["not_a_future_probability"]


def test_90pct_must_use_all_played_season_games_not_last_ten_subset():
    assert highest_90pct_line([13]*10+[0,0],"pts") is None
    assert highest_90pct_line([13]*9,"pts") is None
    # 12/12 with the most recent five including three misses is not allowed.
    assert highest_90pct_line([20]*10+[0,0],"pts") is None
    with pytest.raises(ValueError):
        highest_90pct_line([20]*12,"steals")
    assert 0<wilson_lower_bound(12,12)<1


def test_assists_rebounds_half_point_ladders_have_meaningful_floors():
    assert highest_90pct_line([5]*12,"ast")["line"]==4.5
    assert highest_90pct_line([7]*12,"reb")["line"]==6.5
    assert highest_90pct_line([2]*12,"ast") is None
    assert highest_90pct_line([3]*12,"reb") is None


def row(game,defense,pos,pts,stat_minutes=20,player_id=None):
    return {
        "game_id":str(game),"opponent_id":str(defense),
        "team_id":"attacking-team","player_id":player_id or "p-"+str(pos),
        "min":stat_minutes, "stats":{"pts":pts,"reb":5,"ast":3},
    }


def test_defense_bottom_five_requires_all_thirty_team_positions():
    teams={"def-"+str(i) for i in range(30)}
    positions={("p-G","attacking-team"):"G"}
    records=[row(f"{team}-game-{i}",team,"G",12 if team!="def-0" else 30)
             for team in teams for i in range(12)]
    ranks,coverage=defense_ranks(records,positions,teams)
    assert coverage["G"]["rankable"]
    assert ranks[("def-0","G","pts")]["rank_most_allowed"]==1
    assert ranks[("def-0","G","pts")]["rank_out_of"]==30
    assert ("def-0","F","pts") not in ranks
    records=[r for r in records if not r["game_id"].startswith("def-1-game-")]
    ranks,coverage=defense_ranks(records,positions,teams)
    assert not coverage["G"]["rankable"]
    assert ("def-0","G","pts") not in ranks


def test_defense_ranks_ignore_hybrid_positions_without_guessing():
    teams={"def-"+str(i) for i in range(30)}
    records=[row(f"{team}-game-{i}",team,"G",20,player_id="swing")
             for team in teams for i in range(12)]
    pos={("swing","attacking-team"):"G-F"}
    ranks,quality=defense_ranks(records,pos,teams)
    assert not ranks
    assert quality["G"]["valid_defensive_teams"]==0


def bare_db():
    db=sqlite3.connect(":memory:")
    db.row_factory=sqlite3.Row
    db.executescript("""
    CREATE TABLE games(game_id TEXT PRIMARY KEY, season INT,game_date_eastern TEXT,
        tip_utc TEXT,home_team_id TEXT,away_team_id TEXT,
        status TEXT,game_type TEXT);
    CREATE TABLE team_game_stats(game_id TEXT,team_id TEXT,stats_json TEXT,source_id TEXT);
    CREATE TABLE player_game_stats(game_id TEXT,player_id TEXT,team_id TEXT,
        stats_json TEXT,source_id TEXT);
    CREATE TABLE players(player_id TEXT,canonical_name TEXT);
    CREATE TABLE roster_assignments(player_id TEXT,team_id TEXT,
        published_position TEXT,season INT,source_id TEXT);
    CREATE TABLE availability_reports(game_id TEXT,player_id TEXT,
        normalized_status TEXT,report_utc TEXT,retrieved_at_utc TEXT);
    """)
    db.execute("INSERT INTO players VALUES (?,?)",(PID,"Fixture Star"))
    db.execute("INSERT INTO roster_assignments VALUES (?,?,?,?,?)",
               (PID,"team-attack","G",2027,"sportsdataverse"))
    for i in range(12):
        gid="old"+str(i)
        day=f"2026-11-{i+1:02}"
        db.execute("INSERT INTO games VALUES (?,?,?,?,?,?,?,?)",
                   (gid,2027,day,f"{day}T20:00:00Z",
                    "team-attack","team-def","final","regular_season"))
        box={"min":35,"pts":22,"ast":7,"reb":6,
             "fga":18,"fta":7,"tov":2,"usg_pct":30}
        db.execute("INSERT INTO player_game_stats VALUES (?,?,?,?,?)",
                   (gid,PID,"team-attack",json.dumps(box),"nba_stats_archive"))
        team={"fga":82,"fta":20,"tov":10}
        db.execute("INSERT INTO team_game_stats VALUES (?,?,?,?)",
                   (gid,"team-attack",json.dumps(team),"nba_stats_archive"))
    db.execute("INSERT INTO games VALUES (?,?,?,?,?,?,?,?)",
               (GID,2027,"2026-11-21",TIP,"team-def","team-attack",
                "scheduled","regular_season"))
    db.commit()
    return db


def test_fixture_rejects_90pct_prop_without_30_team_defensive_evidence():
    db=bare_db()
    result=build_alt_prop_research(db,now_utc=NOW,date_eastern="2026-11-21")
    assert result["games_reviewed"]==1
    assert result["candidates"]==[]
    assert result["same_book_parlay"] is None
    assert result["status"]=="NO_VERIFIED_90_PERCENT_MATCHUP"
    assert result["exclusion_counts"].get("DVP_RANK_UNVERIFIED",0)>0
    assert result["betting_recommendation"] is None


def test_no_future_or_same_day_game_leakage_in_player_history():
    db=bare_db()
    # A bad boxscore artificially attached to today's game must not
    # enter any season rate or usage calculation.
    db.execute("INSERT INTO player_game_stats VALUES (?,?,?,?,?)",
               (GID,PID,"team-attack",json.dumps({
                   "min":36,"pts":0,"ast":0,"reb":0,"usg_pct":4
               }),"nba_stats_archive"))
    result=build_alt_prop_research(db,now_utc=NOW,date_eastern="2026-11-21")
    assert result["games_reviewed"]==1
    assert result["candidates"]==[]


def test_usage_can_be_sourced_or_derived_but_never_invented():
    r={"game_id":"g","team_id":"t","min":30,
       "stats":{"usg_pct":0.31,"fga":18,"fta":5,"tov":2}}
    assert _team_usage(r,{})==pytest.approx(31)
    del r["stats"]["usg_pct"]
    assert _team_usage(r,{}) is None
    assert _team_usage(r,{("g","t"):{"fga":80,"fta":20,"tov":11}})>0


def test_published_broad_position_only_and_hybrid_not_assigned():
    db=bare_db()
    assert _positions(db,2027)[(PID,"team-attack")]=="G"
    db.execute("INSERT INTO roster_assignments VALUES (?,?,?,?,?)",
               ("player:nba:777","team-attack","G-F",2027,"sportsdataverse"))
    assert ("player:nba:777","team-attack") not in _positions(db,2027)


def quote(side, *, book="DraftKings", observed="2026-11-21T16:05:00Z",
          market="player:pts:player:nba:111:10.5",provider_market_key="player_points_alternate"):
    return {
        "game_id":GID,"tip_utc":TIP,"observed_at_utc":observed,
        "retrieved_at_utc":observed,"book":book,"market_id":market,
        "market_type":"player_prop","selection":side,"line":10.5,
        "player_id":PID,"provider_market_key":provider_market_key,
        "decimal_odds":1.36 if side=="over" else 3.3,
    }


def forecast():
    return {
        "game_id":GID,"tip_utc":TIP,
        "cutoff_utc":"2026-11-21T16:08:00Z",
        "model_version":"research-v2",
        "result":{
            "simulation_count":100,
            "player_statistics":{PID:{"availability":"probable"}},
            "market_distributions":{
                "calibration_status":"uncalibrated",
                "settlement_scope":"full_game_including_overtime",
                "sample_count":100,
                "player_counts":{PID:{"pts":{"20":90,"10":10}}},
            }
        },
    }


def candidate():
    return {
        "game_id":GID,"player_id":PID,"stat":"pts",
        "alt_over_line":10.5,"date_eastern":"2026-11-21",
    }


def test_price_gate_requires_both_actual_alt_sides_and_pretip_forecast():
    c=[candidate()]
    f={GID:forecast()}
    assert not _quote_candidates(c,[],f,__import__("datetime").datetime.fromisoformat(NOW.replace("Z","+00:00")))
    now=__import__("datetime").datetime.fromisoformat(NOW.replace("Z","+00:00"))
    assert not _quote_candidates(c,[quote("over")],f,now)
    rows=_quote_candidates(c,[quote("over"),quote("under")],f,now)
    assert len(rows)==1
    assert rows[0]["model_probability_uncalibrated"]==pytest.approx(.90)
    assert rows[0]["modeled_roi_uncalibrated"]==pytest.approx(.90*1.36-1)
    assert not rows[0]["actionable"]


def test_reject_stale_or_after_forecast_alt_price_and_wrong_market():
    now=__import__("datetime").datetime.fromisoformat(NOW.replace("Z","+00:00"))
    c=[candidate()]
    f={GID:forecast()}
    late=[quote("over",observed="2026-11-21T16:09:00Z"),
          quote("under",observed="2026-11-21T16:09:00Z")]
    assert not _quote_candidates(c,late,f,now)
    wrong=[quote("over",provider_market_key="player_points"),
           quote("under",provider_market_key="player_points")]
    assert not _quote_candidates(c,wrong,f,now)
    # Changes to the named offered threshold cannot be treated as same price.
    o=quote("over")
    o["line"]=11.5
    assert not _quote_candidates(c,[o,quote("under")],f,now)


def test_hypothetical_alt_no_odds_does_not_masquerade_as_book_price():
    db=bare_db()
    result=build_alt_prop_research(db,now_utc=NOW,date_eastern="2026-11-21")
    assert result["priced_alternate_legs"]==[]
    assert "NO_SOURCE_VERIFIED_ALT_PLAYER_PROP_ODDS_AND_MODEL_PRICE_MATCH" in result["missing_requirements"]


def test_future_placeholder_team_id_not_ranked_as_31st_nba_defense():
    db=bare_db()
    db.execute("INSERT INTO games VALUES (?,?,?,?,?,?,?,?)",(
        "future-extra",2027,"2026-11-22","2026-11-23T01:00:00Z",
        "placeholder-future-team","team-def","scheduled","regular_season"))
    report=build_alt_prop_research(db,now_utc=NOW,date_eastern="2026-11-21")
    coverage=report["defense_coverage"][0]["position_coverage"]
    # Only teams with ACTUAL observed final player/team boxes enter the pool;
    # teams listed solely in future source schedules are never counted.
    assert coverage["G"]["required_teams"]==1
    assert coverage["G"]["rankable"] is False


def test_missing_latest_completed_team_game_blocks_false_twelve_of_twelve():
    db=bare_db()
    # The statistical archive may be from before last night's boxscore.
    # A game with tip more than 4 hours ago is still scheduled in the
    # warehouse: 12/12 must NOT be represented as complete season form.
    db.execute("INSERT INTO games VALUES (?,?,?,?,?,?,?,?)",(
        "unsettled-yesterday",2027,"2026-11-20","2026-11-21T01:00:00Z",
        "team-attack","team-def","scheduled","regular_season"))
    report=build_alt_prop_research(db,now_utc=NOW,date_eastern="2026-11-21")
    assert report["prior_final_freshness"][0]["missing_due_final_games"]==1
    assert report["prior_final_freshness"][0][
        "candidate_teams_with_unsettled_past_game"]["team-attack"]==1
    assert report["exclusion_counts"]["UNSETTLED_PRIOR_GAME_MISSING_FINAL_BOXSCORE"]>0
    assert report["candidates"]==[]
    assert report["same_book_parlay"] is None


def test_not_yet_completed_tip_does_not_count_as_stale_final():
    db=bare_db()
    db.execute("INSERT INTO games VALUES (?,?,?,?,?,?,?,?)",(
        "too-fresh-to-call-final",2027,"2026-11-20","2026-11-21T15:00:00Z",
        "team-attack","team-def","scheduled","regular_season"))
    report=build_alt_prop_research(db,now_utc=NOW,date_eastern="2026-11-21")
    assert report["prior_final_freshness"][0]["missing_due_final_games"]==0
    assert report["exclusion_counts"].get(
       "UNSETTLED_PRIOR_GAME_MISSING_FINAL_BOXSCORE",0
    )==0
