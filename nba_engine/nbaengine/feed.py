"""Data feeds.

* build_games_from_cdn: converts the cdn.nba.com-format play-by-play (2025-26
  archive) to the same per-game table the engine already uses, plus a game date.
* EspnFeed: free public ESPN JSON (scoreboard + game summary). UNOFFICIAL and
  undocumented: check ESPN's terms before relying on it, keep request rates low.
  It could NOT be exercised from the build sandbox (shell egress is blocked), so
  field paths come from inspecting responses through a separate fetch tool.
* ReplayFeed: serves already-downloaded games day by day. Used to test the
  update loop end to end offline.
"""
from __future__ import annotations

import json
import time
import urllib.request
from dataclasses import dataclass
from typing import Protocol

import numpy as np
import pandas as pd

# ESPN abbreviation -> NBA tricode (only the ones that differ)
ESPN_TO_NBA = {"GS": "GSW", "NY": "NYK", "NO": "NOP", "SA": "SAS", "UTAH": "UTA", "WSH": "WAS", "PHX": "PHX"}


def nba_code(espn_abbr: str) -> str:
    return ESPN_TO_NBA.get(espn_abbr, espn_abbr)


# ----------------------------------------------------------------------------
def build_games_from_cdn(csv_path: str, season_label: int) -> pd.DataFrame:
    cols = ["gameId", "actionNumber", "period", "actionType", "subType", "descriptor", "shotResult",
            "teamTricode", "scoreHome", "scoreAway", "timeActual", "description", "personId"]
    d = pd.read_csv(csv_path, usecols=cols, low_memory=False)
    d = d.sort_values(["gameId", "actionNumber"], kind="stable").reset_index(drop=True)
    gid = d["gameId"]
    t = d["actionType"]
    made = d["shotResult"].eq("Made")
    is2, is3 = t.eq("2pt"), t.eq("3pt")
    is_fg = is2 | is3
    tech = d["descriptor"].fillna("").str.contains("technical") | d["subType"].fillna("").str.contains("echnical")
    is_ft = t.eq("freethrow") & ~tech
    ft_n = d["subType"].str.extract(r"(\d) of (\d)").astype("float64")
    ft_last = ft_n[0].eq(ft_n[1])

    # home team = team whose made basket raises scoreHome
    dh = d.groupby("gameId")["scoreHome"].diff().fillna(0)
    home_evt = d[(dh > 0) & d["teamTricode"].notna()]
    home_team = home_evt.groupby("gameId")["teamTricode"].agg(lambda s: s.mode().iat[0])
    teams = d[d["teamTricode"].notna()].groupby("gameId")["teamTricode"].agg(lambda s: sorted(set(s)))
    away_team = pd.Series({g: [x for x in teams[g] if x != home_team[g]][0] for g in home_team.index})

    d["is_home"] = d["teamTricode"].eq(gid.map(home_team))
    d["is_away"] = d["teamTricode"].eq(gid.map(away_team))

    fg_miss = is_fg & ~made
    ft_miss_last = is_ft & ~made & ft_last
    miss_any = fg_miss | (is_ft & ~made)
    d["miss_team"] = d["teamTricode"].where(fg_miss | ft_miss_last)
    d["miss_kind"] = pd.Series(np.where(fg_miss, 1.0, np.where(ft_miss_last, 2.0, np.where(is_ft & ~made, 3.0, np.nan))), index=d.index)
    d["miss_team"] = d.groupby(gid)["miss_team"].ffill()
    d["miss_kind"] = d.groupby(gid)["miss_kind"].ffill()
    d["miss_id"] = miss_any.astype(int).groupby(gid).cumsum()
    reb0 = t.eq("rebound") & d["miss_kind"].isin([1.0, 2.0])
    first = reb0.astype(int).groupby([gid, d["miss_id"]]).cumsum().eq(1)
    reb = reb0 & first
    oreb = reb & d["subType"].eq("offensive")
    d["f_fga"] = is_fg
    d["f_fgm"] = is_fg & made
    d["f_3pa"] = is3
    d["f_3pm"] = is3 & made
    d["f_fta"] = is_ft
    d["f_ftm"] = is_ft & made
    d["f_tov"] = t.eq("turnover")
    d["f_oreb"] = oreb
    d["f_oreb_fg"] = oreb & d["miss_kind"].eq(1.0)
    d["f_oreb_ft"] = oreb & d["miss_kind"].eq(2.0)
    d["f_dreb"] = reb & d["subType"].eq("defensive")

    names = ["fga", "fgm", "3pa", "3pm", "fta", "ftm", "tov", "oreb", "oreb_fg", "oreb_ft", "dreb"]
    out = []
    for side in ("home", "away"):
        sub = d[d[f"is_{side}"]]
        g = sub.groupby("gameId")[[f"f_{n}" for n in names]].sum()
        g.columns = [f"{side}_{n}" for n in names]
        out.append(g)
    g = pd.concat(out, axis=1)
    g["home_pts"] = d.groupby("gameId")["scoreHome"].max().astype(int)   # running score never decreases
    g["away_pts"] = d.groupby("gameId")["scoreAway"].max().astype(int)
    g["n_periods"] = d.groupby("gameId")["period"].max()
    ts = pd.to_datetime(d.groupby("gameId")["timeActual"].min(), utc=True, format="ISO8601")
    g["date"] = ts.dt.tz_convert("America/New_York").dt.strftime("%Y-%m-%d")
    g["home"] = home_team
    g["away"] = away_team
    g["season"] = season_label
    g["playoffs"] = 0
    g = g.reset_index().rename(columns={"gameId": "game_id"})
    g["game_id"] = g["game_id"].astype(int)
    return g


# ----------------------------------------------------------------------------
@dataclass
class FinalGame:
    game_id: int
    season: int
    date: str
    home: str
    away: str
    home_pts: int
    away_pts: int
    n_periods: int
    box: dict          # per-side counts in the engine's *_fga/_fgm/... form


@dataclass
class UpcomingGame:
    game_id: int
    season: int
    date: str
    tip_utc: str
    home: str
    away: str
    market: dict | None = None     # optional odds snapshot, stored for later comparison only


class Feed(Protocol):
    def scoreboard(self, yyyymmdd: str) -> tuple[list[FinalGame], list[UpcomingGame]]: ...


class ReplayFeed:
    """Serves a historical games table as if it were live, date by date."""

    def __init__(self, games: pd.DataFrame):
        self.g = games

    def scoreboard(self, yyyymmdd: str):
        day = f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:]}"
        rows = self.g[self.g["date"] == day]
        fin = [FinalGame(int(r.game_id), int(r.season), r.date, r.home, r.away, int(r.home_pts), int(r.away_pts),
                         int(r.n_periods), {k: int(getattr(r, k)) for k in r._fields if k.startswith(("home_", "away_"))
                                            and k not in ("home_pts", "away_pts")}) for r in rows.itertuples()]
        up = [UpcomingGame(int(r.game_id), int(r.season), r.date, "", r.home, r.away) for r in rows.itertuples()]
        return fin, up


# ----------------------------------------------------------------------------
class EspnFeed:
    BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"

    def __init__(self, pause_s: float = 1.0, timeout: int = 20, user_agent: str = "nba-engine/0.1 (personal research)"):
        self.pause, self.timeout, self.ua = pause_s, timeout, user_agent
        self.summaries: dict = {}      # event id -> (date, season, summary JSON) for every final fetched; used by the player update

    def _get(self, url: str) -> dict:
        req = urllib.request.Request(url, headers={"User-Agent": self.ua})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
        time.sleep(self.pause)
        return data

    @staticmethod
    def _stat(team_stats: list[dict], name: str) -> str | None:
        for s in team_stats:
            if s.get("name") == name:
                return s.get("displayValue")
        return None

    def _box(self, event_id: str) -> tuple[dict, dict]:
        """Team box ingredients from the summary endpoint. Returns (per-side counts, extras)."""
        js = self._get(f"{self.BASE}/summary?event={event_id}")
        self._last_summary = js
        out, ids = {}, {}
        for t in js["boxscore"]["teams"]:
            side = t["homeAway"]
            st = t["statistics"]
            fgm, fga = map(int, self._stat(st, "fieldGoalsMade-fieldGoalsAttempted").split("-"))
            m3, a3 = map(int, self._stat(st, "threePointFieldGoalsMade-threePointFieldGoalsAttempted").split("-"))
            ftm, fta = map(int, self._stat(st, "freeThrowsMade-freeThrowsAttempted").split("-"))
            tov = int(self._stat(st, "turnovers"))
            oreb = int(self._stat(st, "offensiveRebounds"))
            dreb = int(self._stat(st, "defensiveRebounds") or 0)
            # ESPN does not split offensive rebounds by FG-miss vs last-FT-miss: assume ~2% of oreb come from FTs
            # (the 2021-26 play-by-play averages ~0.3 of ~14 per team-game).
            oreb_ft = round(0.02 * oreb)
            out.update({f"{side}_fga": fga, f"{side}_fgm": fgm, f"{side}_3pa": a3, f"{side}_3pm": m3,
                        f"{side}_fta": fta, f"{side}_ftm": ftm, f"{side}_tov": tov, f"{side}_oreb": oreb,
                        f"{side}_oreb_fg": oreb - oreb_ft, f"{side}_oreb_ft": oreb_ft, f"{side}_dreb": dreb})
        return out, ids

    def scoreboard(self, yyyymmdd: str):
        js = self._get(f"{self.BASE}/scoreboard?dates={yyyymmdd}&limit=100")
        fin, up = [], []
        for ev in js.get("events", []):
            comp = ev["competitions"][0]
            if ev.get("season", {}).get("type") != 2:      # regular season only in v0.2
                continue
            cs = {c["homeAway"]: c for c in comp["competitors"]}
            home, away = nba_code(cs["home"]["team"]["abbreviation"]), nba_code(cs["away"]["team"]["abbreviation"])
            date = ev["date"][:10]
            name = ev["status"]["type"]["name"]
            season = int(ev["season"]["year"])
            if name == "STATUS_FINAL":
                box, _ = self._box(ev["id"])
                self.summaries[str(ev["id"])] = (yyyymmdd[:4] + "-" + yyyymmdd[4:6] + "-" + yyyymmdd[6:], season, self._last_summary)
                n_per = int(ev["status"].get("period", 4))
                fin.append(FinalGame(int(ev["id"]), season, yyyymmdd[:4] + "-" + yyyymmdd[4:6] + "-" + yyyymmdd[6:],
                                     home, away, int(cs["home"]["score"]), int(cs["away"]["score"]), max(4, n_per), box))
            elif name == "STATUS_SCHEDULED":
                odds = (comp.get("odds") or [None])[0]
                up.append(UpcomingGame(int(ev["id"]), season, yyyymmdd[:4] + "-" + yyyymmdd[4:6] + "-" + yyyymmdd[6:],
                                       ev["date"], home, away,
                                       {"source": "espn/" + str((odds or {}).get("provider", {}).get("name")),
                                        "snapshot": odds} if odds else None))
        return fin, up
