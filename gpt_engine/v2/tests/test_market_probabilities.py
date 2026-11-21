"""Only empirical frozen Monte Carlo PMFs can price exact NBA lines."""
import pytest

from gpt_engine.v2.market_probabilities import exact_line_probabilities

TIP="2026-11-22T01:00:00Z"
ASOF="2026-11-21T20:10:00Z"
GID="game:nba:demo"


def doc():
    return {
        "game_id":GID,"tip_utc":TIP,"cutoff_utc":ASOF,
        "model_version":"uncalibrated-test",
        "result":{
            "simulation_count":100, "home_win_probability":.60,
            "player_statistics":{
                "player:nba:1":{"availability":"confirmed_available",
                                "pts":{"mean":24.6}}
            },
            "market_distributions":{
                "sample_count":100,
                "calibration_status":"uncalibrated",
                "settlement_scope":"full_game_including_overtime",
                "home_margin_counts":{"5":60,"-2":40},
                "game_total_counts":{"221":50,"220":50},
                "player_counts":{
                    "player:nba:1":{"pts":{"25":60,"24":40}}
                }
            }
        }
    }


def quote(kind, selection, line, market, *, player=None):
    return {
        "game_id":GID,"tip_utc":TIP,
        "book":"fixture","market_type":kind,
        "market_id":market, "selection":selection,
        "line":line, "player_id":player,
        "decimal_odds":1.95,
        "observed_at_utc":"2026-11-21T20:00:00Z",
        "retrieved_at_utc":"2026-11-21T20:05:00Z",
    }


def test_spread_exact_line_and_true_push_mass():
    h=exact_line_probabilities(
        quote("spread","home",-5,"game:spread:home:-5"),doc())
    assert h["probability"] == 0
    assert h["push_probability"] == pytest.approx(.6)
    a=exact_line_probabilities(
        quote("spread","away",5,"game:spread:home:-5"),doc())
    assert a["probability"] == pytest.approx(.4)
    assert a["push_probability"] == pytest.approx(.6)


def test_total_and_player_prop_exact_probabilities():
    total=exact_line_probabilities(
        quote("total","over",220,"game:total:220"),doc())
    assert total["probability"] == pytest.approx(.5)
    assert total["push_probability"] == pytest.approx(.5)
    prop=exact_line_probabilities(
        quote("player_prop","over",24.5,"player:pts:player:nba:1:24.5",
              player="player:nba:1"),doc())
    assert prop["probability"] == pytest.approx(.6)
    assert prop["push_probability"] == 0
    assert prop["calibration_status"] == "uncalibrated"


def test_wrong_data_must_not_generate_fictitious_probs():
    base=doc()
    nohist={**base,"result":{**base["result"]}}
    del nohist["result"]["market_distributions"]
    quote_total=quote("total","over",220,"game:total:220")
    assert exact_line_probabilities(quote_total,nohist) is None
    invalid=doc()
    invalid["result"]["market_distributions"]["game_total_counts"]["220"]=49
    with pytest.raises(ValueError,match="sample count"):
        exact_line_probabilities(quote_total,invalid)
    absent_player=quote("player_prop","over",24.5,
                        "player:pts:player:nba:99:24.5",player="player:nba:99")
    assert exact_line_probabilities(absent_player,doc()) is None
