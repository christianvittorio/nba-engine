"""Fair head-to-head on only games with both pre-tip forecasts and final scores."""
from __future__ import annotations

from datetime import datetime, timezone
from .model import evaluate_saved


def pre_tip(row: dict) -> bool:
    try:
        make = datetime.fromisoformat(row["made_at_utc"].replace("Z", "+00:00")).astimezone(timezone.utc)
        tip = datetime.fromisoformat(row["tip_utc"].replace("Z", "+00:00")).astimezone(timezone.utc)
        return make < tip
    except (KeyError, AttributeError, TypeError, ValueError):
        return False


def compare(gpt: list[dict], claude: dict, finals: list) -> dict:
    """Only compare rows whose snapshots existed before the same game began."""
    finished = {(g.season, g.game_id) for g in finals}
    gpt_rows, claude_rows = [], []
    for g in gpt:
        key = (int(g["season"]), int(g["game_id"]))
        c = claude.get(key)
        if key not in finished or c is None or not pre_tip(g) or not pre_tip(c):
            continue
        gpt_rows.append(g)
        claude_rows.append(c)
    return {"gpt": evaluate_saved(gpt_rows, finals),
            "claude": evaluate_saved(claude_rows, finals)}
