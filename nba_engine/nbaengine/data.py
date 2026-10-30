"""Data ingestion and validation.

Two sources are used (see BLUEPRINT.md section 1 for limitations):

1. FiveThirtyEight `nbaallelo.csv` (1947-2015 game results) - used ONLY to tune
   Elo hyper-parameters, so the 2021-25 evaluation seasons are never touched
   during tuning.
2. shufinskiy/nba_data `nbastats_<year>` play-by-play archives (stats.nba.com
   play-by-play) - used to rebuild one box-score-like row per game, including
   the possession ingredients (FGA, 3PA, FTA, TOV, OREB) that the simulator needs.

Known limitation: the play-by-play files carry no calendar date, so games are
ordered by GAME_ID within a season (GAME_ID is assigned in schedule order).
Rest days / back-to-backs cannot be derived from this source.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

PBP_COLS = ["GAME_ID", "EVENTMSGTYPE", "PERIOD", "HOMEDESCRIPTION",
            "VISITORDESCRIPTION", "SCORE", "PERSON1TYPE",
            "PLAYER1_TEAM_ABBREVIATION", "PLAYER1_TEAM_ID"]


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ----------------------------------------------------------------------------
# 538 historical results (Elo tuning only)
# ----------------------------------------------------------------------------
def load_538_games(path: str) -> pd.DataFrame:
    d = pd.read_csv(path)
    d = d[(d["_iscopy"] == 0) & (d["lg_id"] == "NBA")].copy()
    d["date"] = pd.to_datetime(d["date_game"], format="%m/%d/%Y")
    # In _iscopy==0 rows, team_id is the "first" team; use game_location to
    # map to home/away. Neutral-site games are dropped.
    d = d[d["game_location"].isin(["H", "A"])]
    home_first = d["game_location"] == "H"
    out = pd.DataFrame({
        "game_id": d["game_id"],
        "season": d["year_id"],
        "date": d["date"],
        "home": np.where(home_first, d["team_id"], d["opp_id"]),
        "away": np.where(home_first, d["opp_id"], d["team_id"]),
        "home_pts": np.where(home_first, d["pts"], d["opp_pts"]),
        "away_pts": np.where(home_first, d["opp_pts"], d["pts"]),
        "playoffs": d["is_playoffs"].astype(int),
    })
    return out.sort_values(["date", "game_id"]).reset_index(drop=True)


# ----------------------------------------------------------------------------
# Play-by-play -> one row per game
# ----------------------------------------------------------------------------
def _side(person1type: pd.Series) -> pd.Series:
    """PERSON1TYPE: 2/4 = home team/player, 3/5 = visitor team/player."""
    s = pd.Series(np.nan, index=person1type.index, dtype="float64")
    s[person1type.isin([2, 4])] = 0.0   # 0 = home
    s[person1type.isin([3, 5])] = 1.0   # 1 = away
    return s


def build_games_from_pbp(csv_path: str, season_start_year: int) -> pd.DataFrame:
    """Aggregate a play-by-play CSV to one row per game (home & away box ingredients)."""
    d = pd.read_csv(csv_path, usecols=PBP_COLS, low_memory=False)
    d = d.sort_values(["GAME_ID", "PERIOD"], kind="stable")  # keep file order inside game
    d["desc"] = d["HOMEDESCRIPTION"].fillna("") + "|" + d["VISITORDESCRIPTION"].fillna("")
    d["side"] = _side(d["PERSON1TYPE"])
    t = d["EVENTMSGTYPE"]

    fga = t.isin([1, 2])
    d["is_fgm"] = (t == 1)
    d["is_3pa"] = fga & d["desc"].str.contains("3PT", regex=False)
    d["is_3pm"] = d["is_3pa"] & (t == 1)
    d["is_fta"] = (t == 3) & ~d["desc"].str.contains("Technical", regex=False)
    d["is_ftm"] = d["is_fta"] & ~d["desc"].str.contains("MISS", regex=False)
    d["is_tov"] = (t == 5)
    d["is_fga"] = fga

    # offensive vs defensive rebound: compare the rebounder's side with the side
    # of the last missed FG or missed LAST free throw of a trip. Misses on
    # non-final free throws are followed by a recorded dead-ball "team rebound"
    # that does not extend a possession, so they are excluded (kind 3).
    ft_n = d["desc"].str.extract(r"Free Throw (?:Flagrant |Clear Path )?(\d) of (\d)").astype("float64")
    ft_last = (ft_n[0] == ft_n[1])
    ft_miss = (t == 3) & d["desc"].str.contains("MISS", regex=False) & ~d["desc"].str.contains("Technical", regex=False)
    fg_miss = (t == 2)
    d["last_miss_side"] = d["side"].where(fg_miss | ft_miss)
    d["last_miss_side"] = d.groupby("GAME_ID")["last_miss_side"].ffill()
    kind = np.where(fg_miss, 1.0, np.where(ft_miss & ft_last, 2.0, np.where(ft_miss, 3.0, np.nan)))
    d["last_miss_kind"] = pd.Series(kind, index=d.index).groupby(d["GAME_ID"]).ffill()
    # only the FIRST rebound event after a miss counts (later stray team-rebound
    # records would otherwise be matched against a stale miss)
    d["miss_id"] = (fg_miss | ft_miss).astype(int).groupby(d["GAME_ID"]).cumsum()
    reb0 = (t == 4) & d["last_miss_kind"].isin([1.0, 2.0])
    reb = reb0 & (reb0.astype(int).groupby([d["GAME_ID"], d["miss_id"]]).cumsum() == 1)
    d["is_oreb"] = reb & (d["side"] == d["last_miss_side"])
    d["is_oreb_fg"] = d["is_oreb"] & (d["last_miss_kind"] == 1.0)
    d["is_oreb_ft"] = d["is_oreb"] & (d["last_miss_kind"] == 2.0)
    d["is_dreb"] = reb & (d["side"] != d["last_miss_side"])

    # points from scoring events (for validation against the final SCORE)
    ft_made_any = (t == 3) & ~d["desc"].str.contains("MISS", regex=False)  # incl. technical FTs
    d["pts_calc"] = np.where(d["is_fgm"], np.where(d["is_3pa"], 3, 2), 0) + ft_made_any.astype(int)

    flags = ["is_fga", "is_fgm", "is_3pa", "is_3pm", "is_fta", "is_ftm",
             "is_tov", "is_oreb", "is_oreb_fg", "is_oreb_ft", "is_dreb"]
    rows = []
    for side_val, label in [(0.0, "home"), (1.0, "away")]:
        sub = d[d["side"] == side_val]
        g = sub.groupby("GAME_ID")[flags + ["pts_calc"]].sum()
        g.columns = [f"{label}_{c.replace('is_', '')}" for c in g.columns]
        rows.append(g)
    g = pd.concat(rows, axis=1)

    # final score: last non-null SCORE per game ("visitor - home")
    sc = d[d["SCORE"].notna()].groupby("GAME_ID")["SCORE"].last().str.split(" - ", expand=True)
    g["away_pts"] = pd.to_numeric(sc[0]).reindex(g.index)
    g["home_pts"] = pd.to_numeric(sc[1]).reindex(g.index)
    g["n_periods"] = d.groupby("GAME_ID")["PERIOD"].max()

    # team identities from player events
    hm = d[(d["side"] == 0.0) & d["PLAYER1_TEAM_ABBREVIATION"].notna()].groupby("GAME_ID")["PLAYER1_TEAM_ABBREVIATION"].agg(lambda s: s.mode().iat[0])
    aw = d[(d["side"] == 1.0) & d["PLAYER1_TEAM_ABBREVIATION"].notna()].groupby("GAME_ID")["PLAYER1_TEAM_ABBREVIATION"].agg(lambda s: s.mode().iat[0])
    g["home"] = hm
    g["away"] = aw
    g["season"] = season_start_year + 1  # season label = year the season ends
    g = g.reset_index().rename(columns={"GAME_ID": "game_id"})
    g["game_id"] = g["game_id"].astype(int)
    g["playoffs"] = 0
    return g


def load_pbp_games(extract_root: str, years: list[int], cache_dir: str) -> tuple[pd.DataFrame, list[dict]]:
    """Build (and cache) the per-game table for the given season start years."""
    os.makedirs(cache_dir, exist_ok=True)
    frames, manifest = [], []
    for y in years:
        csv = glob.glob(os.path.join(extract_root, str(y), "*.csv"))[0]
        cache = os.path.join(cache_dir, f"games_{y}.csv")
        if not os.path.exists(cache):
            build_games_from_pbp(csv, y).to_csv(cache, index=False)
        g = pd.read_csv(cache)
        frames.append(g)
        manifest.append({"season_start": y, "source_file": os.path.basename(csv),
                         "source_sha256": sha256(csv), "games": int(len(g))})
    games = pd.concat(frames, ignore_index=True)
    games = games.sort_values(["season", "game_id"]).reset_index(drop=True)
    games["order"] = np.arange(len(games))
    return games, manifest


# ----------------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------------
@dataclass
class ValidationReport:
    ok: bool
    checks: dict

    def to_json(self) -> str:
        return json.dumps({"ok": self.ok, "checks": self.checks}, indent=2, default=str)


def validate_games(games: pd.DataFrame) -> ValidationReport:
    c = {}
    c["rows"] = int(len(games))
    c["duplicate_game_ids"] = int(games.duplicated(["season", "game_id"]).sum())
    c["null_scores"] = int(games[["home_pts", "away_pts"]].isna().any(axis=1).sum())
    c["null_teams"] = int(games[["home", "away"]].isna().any(axis=1).sum())
    c["ties"] = int((games["home_pts"] == games["away_pts"]).sum())
    c["score_out_of_range"] = int(((games["home_pts"] < 50) | (games["home_pts"] > 200) |
                                   (games["away_pts"] < 50) | (games["away_pts"] > 200)).sum())
    c["games_per_season"] = games.groupby("season").size().to_dict()
    c["teams_per_season"] = games.groupby("season").apply(
        lambda x: len(set(x["home"]).union(x["away"])), include_groups=False).to_dict()
    if "home_pts_calc" in games.columns:
        mism = (games["home_pts_calc"] != games["home_pts"]) | (games["away_pts_calc"] != games["away_pts"])
        c["pbp_points_reconcile_mismatch_games"] = int(mism.sum())
    ok = (c["duplicate_game_ids"] == 0 and c["null_scores"] == 0 and c["null_teams"] == 0
          and c["ties"] == 0 and c["score_out_of_range"] == 0)
    return ValidationReport(ok, c)
