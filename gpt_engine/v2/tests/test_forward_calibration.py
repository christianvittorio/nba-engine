"""Calibration research gates: no retrospective artifact promoted as validated."""
from datetime import datetime, timedelta, timezone

import pytest

from gpt_engine.v2.forward_calibration import evaluate_time_split


def observations():
    start = datetime(2026,10,20,0,tzinfo=timezone.utc)
    hold = datetime(2026,11,2,0,tzinfo=timezone.utc)
    rows = []
    for i in range(100):
        t = start + timedelta(hours=i)
        rows.append({
            "game_id":f"game:nba:cal{i}",
            "model_version":"same-frozen-model",
            "cutoff_utc":t.isoformat(),
            "tip_utc":(t+timedelta(hours=1)).isoformat(),
            "outcome_retrieved_at_utc":(t+timedelta(hours=4)).isoformat(),
            "probability": .55 if i % 2 else .45,
            "home_won":int(i % 2 == 1),
        })
    for i in range(120):
        t = hold + timedelta(hours=i)
        rows.append({
            "game_id":f"game:nba:held{i}",
            "model_version":"same-frozen-model",
            "cutoff_utc":t.isoformat(),
            "tip_utc":(t+timedelta(hours=1)).isoformat(),
            "outcome_retrieved_at_utc":(t+timedelta(hours=4)).isoformat(),
            "probability": .55 if i%2 else .45,
            "home_won":int(i%2 == 1),
        })
    return rows


def evaluate(rows, stamp="2026-10-30T00:00:00Z"):
    return evaluate_time_split(
        rows, calibration_before="2026-11-01T00:00:00Z",
        holdout_from="2026-11-02T00:00:00Z",
        holdout_before="2026-12-01T00:00:00Z",
        trained_at_utc=stamp
    )


def test_strictly_split_and_explicit_forward_status():
    result = evaluate(observations())
    assert result["calibration_games"] == 100
    assert result["holdout_games"] == 120
    assert result["training_completed_before_holdout_predictions"] is True
    assert result["calibrated_holdout"]["log_loss"] < (
        result["raw_holdout"]["log_loss"]
    )
    assert result["promotion_gate"]["automatic_promotion"] is False
    assert result["promotion_gate"]["approved_for_live_value_decisions"] is False
    assert sum(b["n"] for b in result["reliability_buckets"]) == 120


def test_retrofit_after_holdout_cannot_be_called_prospective():
    result = evaluate(observations(), stamp="2026-11-20T00:00:00Z")
    assert result["training_completed_before_holdout_predictions"] is False
    assert result["promotion_gate"]["prospectively_trained"] is False
    assert not result["promotion_gate"]["approved_for_live_value_decisions"]


def test_unseen_holdout_required_and_no_model_mixing():
    rows = observations()
    rows[101]["model_version"] = "different"
    with pytest.raises(ValueError,match="Different model versions"):
        evaluate(rows)
    with pytest.raises(ValueError,match="overlap"):
        evaluate_time_split(
            observations(),calibration_before="2026-11-10T00:00:00Z",
            holdout_from="2026-11-02T00:00:00Z",
            holdout_before="2026-12-01T00:00:00Z"
        )


def test_requires_80_games_each_status_and_retrieved_labels():
    rows = observations()
    with pytest.raises(ValueError,match="80"):
        evaluate(rows[50:])
    with pytest.raises(ValueError,match="predates"):
        evaluate(rows,stamp="2026-10-01T00:00:00Z")
