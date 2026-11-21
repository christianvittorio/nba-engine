"""Verified NBA statistical data backfill. No predictions and no edits to Claude's DB.

Data source: https://github.com/llimllib/nba_data (public, sourced from NBA stats).
Direct season files: https://basketball-data.billmill.org/nba/stats/<dataset>/season=<YYYY>/data.parquet
Season labels are the END year: 2020 is the 2019-20 NBA season.

Usage:
  python -m data_foundation.build --seasons 2020 2021
  python -m data_foundation.build --seasons 2020 2021 2022 2023 2024 2025 2026
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import sys

import pandas as pd

from .style import build_style_snapshots

BASE = "https://basketball-data.billmill.org/nba/stats"
PROJECT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT / "data_foundation" / "artifacts"
BOXSCORE = ("pts", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "oreb", "dreb",
            "reb", "ast", "tov", "stl", "blk")
ADVANCED = ("off_rating", "def_rating", "net_rating", "pace", "poss", "efg_pct",
            "ts_pct", "tm_tov_pct", "ast_pct", "ast_to", "ast_ratio", "oreb_pct",
            "dreb_pct", "reb_pct", "e_off_rating", "e_def_rating", "e_net_rating",
            "team_oreb")
EXPECTED_REGULAR = {2020: 1059, 2021: 1080, 2022: 1230, 2023: 1230,
                    2024: 1230, 2025: 1230, 2026: 1230}
GAME_TYPES = {"002": "regular_season", "004": "playoffs",
              "005": "play_in", "006": "cup_final"}
SOURCE = "llimllib/nba_data NBA stats archive"


def season_url(dataset: str, season: int) -> str:
    if not re.fullmatch(r"[a-z_]+", dataset) or not 1997 <= season <= 2100:
        raise ValueError("Invalid dataset or season")
    return f"{BASE}/{dataset}/season={season}/data.parquet"


def read_season(con, dataset: str, season: int) -> pd.DataFrame:
    """DuckDB uses HTTP range requests to fetch one public source season."""
    url = season_url(dataset, season)
    try:
        df = con.execute("SELECT * FROM read_parquet(?)", [url]).df()
    except Exception as exc:
        raise RuntimeError(f"Failed to read {dataset} for {season}: {url}: {exc}") from exc
    if df.empty:
        raise ValueError(f"Zero rows in {url}")
    df.columns = [str(x).lower() for x in df.columns]
    return df


def classify_game(game_id: str) -> str:
    return GAME_TYPES.get(str(game_id).zfill(10)[:3], "other")


def required(df: pd.DataFrame, columns: tuple[str, ...], dataset: str):
    missing = sorted(set(columns) - set(df.columns))
    if missing:
        raise ValueError(f"{dataset} missing required fields: {missing}")


def full_stats(df: pd.DataFrame, sample_cols: tuple[str, ...]):
    """Convert published numeric columns to numbers while preserving nulls."""
    for c in sample_cols:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def normalize_teams(raw: pd.DataFrame, meta: pd.DataFrame, season: int) -> pd.DataFrame:
    required(raw, ("game_id", "team_id", "opp_team_id", "game_date", "pts",
                   "fga", "fgm", "fg3a", "fg3m", "fta", "ftm", "oreb", "dreb",
                   "ast", "tov", "home"), "team_game_logs")
    required(meta, ("team_id", "nba_abbrev"), "team_seasons")
    data = raw.copy()
    data["season"] = season
    data["game_id"] = data.game_id.astype(str).str.zfill(10)
    data["game_type"] = data.game_id.map(classify_game)
    data = data[data.game_type.isin(GAME_TYPES.values())].copy()
    data["team_id"] = data.team_id.astype(str)
    data["opp_team_id"] = data.opp_team_id.astype(str)
    ids = meta[["team_id", "nba_abbrev"]].drop_duplicates(subset=["team_id"])
    data = data.merge(ids.rename(columns={"nba_abbrev": "team"}), on="team_id",
                      how="left", validate="many_to_one")
    data = data.merge(ids.rename(columns={"team_id": "opp_team_id",
                                          "nba_abbrev": "opp"}), on="opp_team_id",
                      how="left", validate="many_to_one")
    if data[["team", "opp"]].isna().any().any():
        raise ValueError("Unknown team_id in official team game logs")
    if data.duplicated(["season", "game_id", "team_id"]).any():
        raise ValueError("Duplicate team/game records")
    counts = data.groupby("game_id").size()
    if (counts != 2).any():
        raise ValueError(f"Expected exactly two team rows per NBA game: {counts[counts != 2].to_dict()}")
    for c in ("home",):
        data[c] = data[c].astype("boolean")
    for col in BOXSCORE + ADVANCED:
        if col in data:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    data["efg_recalc"] = (data.fgm + .5 * data.fg3m) / data.fga.replace(0, float("nan"))
    data["three_point_rate"] = data.fg3a / data.fga.replace(0, float("nan"))
    data["estimated_possessions"] = data.fga - data.oreb + data.tov + .44 * data.fta
    data["fta_rate"] = data.fta / data.fga.replace(0, float("nan"))
    # Explicit opponent columns let the matchup engine compare shooting/allowed rates.
    allowed_cols = [x for x in BOXSCORE + ADVANCED if x in data.columns]
    opp = data[["game_id", "team_id"] + allowed_cols].copy()
    opp = opp.rename(columns={"team_id": "opp_team_id",
                              **{x: "opp_" + x for x in allowed_cols}})
    data = data.merge(opp, on=["game_id", "opp_team_id"], how="left",
                      validate="one_to_one")
    if data[["opp_pts", "opp_fg3a", "opp_ast"]].isna().any().any():
        raise ValueError("Missing opponent stats after team-game join")
    return data.sort_values(["game_date", "game_id", "team"]).reset_index(drop=True)


def normalize_players(raw: pd.DataFrame, meta: pd.DataFrame,
                      teams: pd.DataFrame, season: int) -> pd.DataFrame:
    required(raw, ("game_id", "player_id", "team_id", "opp_team_id", "pts",
                   "ast", "reb", "min"), "player_game_logs")
    required(meta, ("player_id",), "player_seasons")
    data = raw.copy()
    data["season"] = season
    data["game_id"] = data.game_id.astype(str).str.zfill(10)
    data["game_type"] = data.game_id.map(classify_game)
    data = data[data.game_type.isin(GAME_TYPES.values())].copy()
    data["player_id"] = data.player_id.astype(str)
    data["team_id"] = data.team_id.astype(str)
    data["opp_team_id"] = data.opp_team_id.astype(str)
    original_n = len(data)
    positions = meta[["player_id"] + (["position"] if "position" in meta else [])].copy()
    if "position" not in positions:
        positions["position"] = "UNKNOWN"  # older NBA archive has no position: never invent one
    positions["player_id"] = positions.player_id.astype(str)
    positions = positions.drop_duplicates(subset=["player_id"])
    data = data.merge(positions, on="player_id", how="left",
                      validate="many_to_one", suffixes=("", "_source"))
    if "position_source" in data:
        data["position"] = data["position"].fillna(data.position_source)
        data = data.drop(columns=["position_source"])
    if len(data) != original_n:
        raise ValueError("Player join altered row count")
    data["position"] = data.position.fillna("UNKNOWN").astype(str).str.strip().str.upper()
    data["position"] = data.position.replace({"": "UNKNOWN", "NAN": "UNKNOWN"})
    # Do NOT mislabel a generic NBA 'F' as SF or a generic 'G' as PG.
    data["position_quality"] = data.position.map(
        lambda p: "five_position" if p in {"PG", "SG", "SF", "PF", "C"}
        else ("broad_or_hybrid" if p in {"G", "F", "G-F", "F-G", "F-C", "C-F", "G/F", "F/C", "C"}
              else "unclassified")
    )
    all_team_games = teams[["game_id", "team_id", "team", "opp"]].drop_duplicates()
    data = data.merge(all_team_games, on=["game_id", "team_id"], how="left",
                      validate="many_to_one")
    if data[["team", "opp"]].isna().any().any():
        raise ValueError("Player logs contain games or teams absent from team logs")
    if data.duplicated(["season", "game_id", "player_id", "team_id"]).any():
        raise ValueError("Duplicate player/game rows")
    stat_fields = [c for c in BOXSCORE + ("min", "usg_pct", "pace", "poss")
                   if c in data]
    return full_stats(data, tuple(stat_fields)).sort_values(
        ["game_id", "team", "player_id"]).reset_index(drop=True)


def defense_vs_position(players: pd.DataFrame, season: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Actual opposing box-score production by PUBLISHED player position.

    This is a positional aggregate, not individual defender attribution.
    A hybrid 'G-F' remains its own category rather than being double-counted.
    """
    dims = ["game_id", "game_type", "opp_team_id", "opp", "position", "position_quality"]
    measures = [s for s in ("min", "pts", "reb", "ast", "fg3m", "fg3a", "stl",
                            "blk", "tov", "fga", "fta") if s in players]
    data = players[dims + measures].copy()
    data["season"] = season
    group = ["season"] + dims
    agg = {s: "sum" for s in measures}
    agg["position_quality"] = "first"
    group.remove("position_quality")
    games = data.groupby(group, dropna=False, as_index=False).agg(agg)
    games = games.rename(columns={"opp_team_id": "defense_team_id",
                                  "opp": "defense_team"})
    games["players_observed"] = data.groupby(group, dropna=False).size().values
    summary_g = ["season", "game_type", "defense_team_id", "defense_team",
                 "position", "position_quality"]
    agg2 = {s: "sum" for s in measures}
    agg2["game_id"] = "nunique"
    agg2["players_observed"] = "sum"
    season_rows = games.groupby(summary_g, dropna=False, as_index=False).agg(agg2)
    season_rows = season_rows.rename(columns={"game_id": "sample_games"})
    for stat in (s for s in measures if s != "min"):
        season_rows[stat + "_allowed_per_game"] = (
            season_rows[stat] / season_rows["sample_games"]
        )
        season_rows[stat + "_allowed_per_48_position_minutes"] = (
            48 * season_rows[stat] / season_rows["min"].replace(0, float("nan"))
        )
    return games, season_rows


def validate(teams: pd.DataFrame, players: pd.DataFrame, season: int) -> dict:
    regular = teams.loc[teams.game_type == "regular_season"]
    n_games = int(regular.game_id.nunique())
    expected = EXPECTED_REGULAR.get(season)
    if expected and n_games != expected:
        raise ValueError(f"{season}: expected {expected} regular games, found {n_games}")
    # Also verify final points in opponent row and scoring identity, not only row count.
    calc = 2 * teams.fgm + teams.fg3m + teams.ftm
    different = (calc != teams.pts).fillna(True)
    scoring_mismatch = int(different.sum())
    # Missing game IDs/score rows are fatal; minor source boxscore anomalies are disclosed.
    completed_ids = set(regular.game_id)
    player_ids = set(players.loc[players.game_type == "regular_season", "game_id"])
    missing_player_games = completed_ids - player_ids
    if missing_player_games:
        raise ValueError(f"{season}: missing player logs for {len(missing_player_games)} regular games: "
                         f"{sorted(missing_player_games)[:8]}")
    if teams["team"].nunique() < 30 or players.player_id.nunique() < 300:
        raise ValueError(f"{season}: suspiciously low team/player coverage")
    return {
        "season": season,
        "season_label": f"{season-1}-{season % 100:02d}",
        "expected_regular_games": expected,
        "regular_games_found": n_games,
        "all_games_found": int(teams.game_id.nunique()),
        "all_team_game_rows": len(teams),
        "player_game_rows": len(players),
        "distinct_players": int(players.player_id.nunique()),
        "teams": int(regular.team.nunique()),
        "team_box_score_identity_mismatches": scoring_mismatch,
        "position_counts": {str(k): int(v) for k, v in
                            players.position.value_counts(dropna=False).items()},
        "fully_labeled_five_position_share": round(
            float((players.position_quality == "five_position").mean()), 4),
        "positions_are_actual_defenders": False,
        "coach_identity_coverage": "not yet sourced",
        "source": SOURCE,
        "source_urls": {name: season_url(name, season) for name in
                        ("team_game_logs", "player_game_logs", "team_seasons",
                         "player_seasons")},
    }


def _write(df: pd.DataFrame, subfolder: str, season: int) -> Path:
    where = OUTPUT / subfolder
    where.mkdir(parents=True, exist_ok=True)
    path = where / f"{season}.csv.gz"
    df.to_csv(path, index=False, compression={"method": "gzip", "compresslevel": 6})
    return path


def run(seasons: list[int], out_dir: Path = OUTPUT) -> dict:
    import duckdb

    global OUTPUT
    OUTPUT = Path(out_dir)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("SET enable_http_metadata_cache = true")
    done = []
    for season in seasons:
        print(f"[data-foundation] processing NBA season ending {season}", flush=True)
        teams_raw = read_season(con, "team_game_logs", season)
        players_raw = read_season(con, "player_game_logs", season)
        teams_meta = read_season(con, "team_seasons", season)
        players_meta = read_season(con, "player_seasons", season)
        teams = normalize_teams(teams_raw, teams_meta, season)
        players = normalize_players(players_raw, players_meta, teams, season)
        dvp_game, dvp_season = defense_vs_position(players, season)
        style = build_style_snapshots(teams)
        audit = validate(teams, players, season)
        _write(teams, "teams", season)
        _write(players, "players", season)
        _write(dvp_game, "defense_vs_position_game", season)
        _write(dvp_season, "defense_vs_position_season", season)
        _write(style, "team_style_pregame", season)
        done.append(audit)
        print(f"  validated {audit['regular_games_found']} regular games, "
              f"{audit['player_game_rows']} player-game rows", flush=True)
    report = {
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "seasons": done,
        "overall": {
            "verified_regular_games": sum(x["regular_games_found"] for x in done),
            "total_player_rows": sum(x["player_game_rows"] for x in done),
            "all_expected_seasons_present": all(
                x["regular_games_found"] == x["expected_regular_games"] for x in done
                if x["expected_regular_games"] is not None),
            "limitations": [
                "Published positions may be G/F/C or hybrids; PG/SG/SF/PF/C coverage is measured, not assumed.",
                "Defense-vs-position denotes opponent production, not specific defender assignments.",
                "Coaching identity and defensive scheme are not sourced or inferred from these tables.",
                "Historical data may reflect corrected end-of-season NBA stats, not knowledge available before tip.",
            ],
        },
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seasons", nargs="+", type=int,
                        default=[2020, 2021, 2022, 2023, 2024, 2025, 2026])
    parser.add_argument("--out", default=str(OUTPUT))
    args = parser.parse_args()
    result = run(sorted(set(args.seasons)), Path(args.out))
    print(json.dumps(result["overall"], indent=2))


if __name__ == "__main__":
    main()
