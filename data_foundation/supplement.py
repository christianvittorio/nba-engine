"""Read official NBA roster/coach tables published by SportsDataverse.

Release catalog: https://github.com/sportsdataverse/sportsdataverse-data/releases
Data is season-level, *not* proof of which coach ran a specific game.
"""
from __future__ import annotations

import pandas as pd

OWNER = "https://github.com/sportsdataverse/sportsdataverse-data/releases/download"
TAGS = {
    "rosters": "nba_stats_rosters",
    "coaches": "nba_stats_coaches",
}


def release_url(kind: str, season: int) -> str:
    if kind not in TAGS or not 1997 <= season <= 2100:
        raise ValueError("Invalid NBA supplemental dataset")
    return f"{OWNER}/{TAGS[kind]}/{kind}_{season}.csv"


def read_supplement(kind: str, season: int) -> pd.DataFrame:
    url = release_url(kind, season)
    try:
        data = pd.read_csv(url, dtype=str)
    except Exception as exc:
        raise RuntimeError(f"Cannot fetch published {kind} for {season}: {url}: {exc}") from exc
    if data.empty:
        raise ValueError(f"Empty NBA release {url}")
    data.columns = [str(c).strip().lower() for c in data.columns]
    needed = {"team_id", "season"}
    needed |= {"player_id", "position"} if kind == "rosters" else {"coach_name", "coach_type"}
    missing = needed - set(data.columns)
    if missing:
        raise ValueError(f"{kind} for {season} lacks required columns {sorted(missing)}")
    data["team_id"] = data.team_id.str.strip().str.replace(r"\.0$", "", regex=True)
    data["season"] = season  # Release asset year is checked; keep year authoritative.
    return data


def position_lookup(rosters: pd.DataFrame) -> tuple[dict[str, str], dict]:
    """Only copy observed NBA roster positions. Ambiguous players remain unknown."""
    if rosters.empty:
        return {}, {"players": 0, "mapped": 0, "ambiguous": 0}
    r = rosters.copy()
    r["player_id"] = r.player_id.astype(str).str.replace(r"\.0$", "", regex=True)
    r["position"] = r.position.fillna("").astype(str).str.strip().str.upper()
    grouped = r.groupby("player_id")["position"].agg(
        lambda x: sorted({v for v in x if v and v not in {"NAN", "NONE"}})
    )
    out = {str(pid): positions[0] for pid, positions in grouped.items()
           if len(positions) == 1}
    return out, {
        "players": len(grouped),
        "mapped": len(out),
        "ambiguous": sum(len(v) > 1 for v in grouped),
    }


def coach_coverage(coaches: pd.DataFrame, team_ids: set[str]) -> dict:
    """Season-level head-coach presence, with changes/multiple heads disclosed."""
    h = coaches[coaches.coach_type.astype(str).str.contains(
        "head coach", case=False, na=False)].copy()
    h = h[h.team_id.isin(team_ids)]
    counts = h.groupby("team_id")["coach_name"].nunique()
    return {
        "teams_with_head_coach": int(len(counts)),
        "teams_with_multiple_head_coaches": int((counts > 1).sum()),
        "head_coaches_total": int(h.coach_name.nunique()),
        "per_game_coach_identity_verified": False,
    }
