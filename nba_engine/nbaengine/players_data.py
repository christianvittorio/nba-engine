"""Player game logs rebuilt from cdn-format play-by-play.

One row per (game, team, player) with minutes and box-score counts.

Minutes come from on-court tracking:
* period-1 starters are inferred lazily: any player who acts (shot, rebound, turnover, assist, steal, block,
  non-technical foul) before being subbed in is treated as on the court from the start of the period;
* later periods start from the previous period's closing lineup;
* an unexpected substitution-out of a player we did not have on the court credits him from the start of that period.

Known limitations (validated in `validate_player_logs`): a player who stays on the court a whole period without
a single event can be missed in period 1, and technical-foul free throws / bench technicals are ignored for
inference. Heaves are team events with no shooter in this source and are not attributed to players.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

COLS = ["gameId", "actionNumber", "orderNumber", "period", "clock", "actionType", "subType", "descriptor", "personId",
        "teamTricode", "shotResult", "assistPersonId", "foulDrawnPersonId", "playerNameI"]
STAT_COLS = ["pts", "reb", "oreb", "ast", "stl", "blk", "tov", "fgm", "fga", "tpm", "tpa", "ftm", "fta"]
INFER_TYPES = {"2pt", "3pt", "rebound", "turnover", "steal", "block", "freethrow", "foul"}


def _period_bounds(p: int) -> tuple[float, float]:
    if p <= 4:
        s = 720.0 * (p - 1)
        return s, s + 720.0
    s = 2880.0 + 300.0 * (p - 5)
    return s, s + 300.0


def build_player_logs(csv_path: str, season_label: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (player_games, team_checks). team_checks has per-team-game minute totals and period counts."""
    d = pd.read_csv(csv_path, usecols=COLS, low_memory=False)
    d = d.sort_values(["gameId", "orderNumber", "actionNumber"], kind="stable").reset_index(drop=True)   # actionNumber is NOT chronological
    d = d[d["actionType"].isin(INFER_TYPES | {"substitution", "period"})].copy()
    rem = d["clock"].str[2:4].astype(float) * 60 + d["clock"].str[5:10].astype(float)
    plen = np.where(d["period"] <= 4, 720.0, 300.0)
    pstart = np.where(d["period"] <= 4, 720.0 * (d["period"] - 1), 2880.0 + 300.0 * (d["period"] - 5))
    d["gt"] = pstart + (plen - rem)
    d["pstart"] = pstart
    d["pend"] = pstart + plen
    sub = d["subType"].fillna("")
    desc = d["descriptor"].fillna("")
    d["technicalish"] = (sub.str.contains("technical|delay") | desc.str.contains("technical|delay")) & d["actionType"].isin(["foul", "freethrow"])

    names, rows, checks = {}, [], []
    arrs = {c: d[c].to_numpy() for c in ["gameId", "period", "actionType", "subType", "personId", "teamTricode", "shotResult",
                                         "assistPersonId", "foulDrawnPersonId", "gt", "pstart", "pend", "technicalish", "playerNameI"]}
    n = len(d)
    i = 0
    while i < n:
        gid = arrs["gameId"][i]
        j = i
        while j < n and arrs["gameId"][j] == gid:
            j += 1
        oncourt: dict[str, dict[int, float]] = {}      # team -> {player: in_time}
        prev_end: dict[str, set] = {}
        stats: dict[tuple[str, int], dict] = {}
        started: set = set()
        entered: set = set()                           # players subbed in during the current period
        cur_period = 0
        period_open = False
        teams_seen: list[str] = []
        period_end_t = 0.0

        def st(team, p):
            k = (team, p)
            if k not in stats:
                stats[k] = {c: 0 for c in STAT_COLS}
                stats[k]["sec"] = 0.0
            return stats[k]

        def credit(team, p, t_now):
            """Close a stint for player p."""
            t_in = oncourt[team].pop(p)
            st(team, p)["sec"] += max(0.0, t_now - t_in)

        def ensure_on(team, p, t_now, pstart_t, period):
            if p == 0 or p is None or (isinstance(p, float) and np.isnan(p)):
                return
            p = int(p)
            if p in oncourt.setdefault(team, {}):
                return
            if p in entered:                       # subbed in earlier this period, then left: cannot act
                return
            oncourt[team][p] = pstart_t            # inferred as on court since the start of the period
            if period == 1:
                started.add((team, p))

        for r in range(i, j):
            at, ty = arrs["actionType"][r], arrs["subType"][r]
            team = arrs["teamTricode"][r]
            per = int(arrs["period"][r])
            t = float(arrs["gt"][r])
            if isinstance(team, str) and team not in teams_seen:
                teams_seen.append(team)
            if at == "period":
                if ty == "start":
                    cur_period = per
                    period_open = True
                    entered = set()
                    for tm in teams_seen:
                        oncourt.setdefault(tm, {})
                        if per > 1:
                            oncourt[tm] = {p: arrs["pstart"][r] for p in prev_end.get(tm, set())}
                        else:
                            oncourt[tm] = {}
                elif ty == "end":
                    period_open = False
                    for tm in list(oncourt):
                        prev_end[tm] = set(oncourt[tm])
                        for p in list(oncourt[tm]):
                            credit(tm, p, float(arrs["pend"][r]))
                    period_end_t = float(arrs["pend"][r])
                continue
            if not isinstance(team, str):
                continue
            pid = arrs["personId"][r]
            pid = 0 if pd.isna(pid) else int(pid)
            if pid and arrs["playerNameI"][r] == arrs["playerNameI"][r]:
                names[pid] = arrs["playerNameI"][r]
            ps = float(arrs["pstart"][r])
            if at == "substitution" and not period_open:
                # logged between periods: change the closing lineup, no minutes involved
                pe = prev_end.setdefault(team, set())
                if ty == "out":
                    pe.discard(pid)
                elif ty == "in":
                    pe.add(pid)
                continue
            if not period_open:
                continue
            if at == "substitution":
                oncourt.setdefault(team, {})
                if ty == "out":
                    if pid not in oncourt[team]:
                        oncourt[team][pid] = ps if pid not in entered else t
                        if per == 1 and pid not in entered:
                            started.add((team, pid))
                    credit(team, pid, t)
                elif ty == "in":
                    if pid not in oncourt[team]:
                        oncourt[team][pid] = t
                    entered.add(pid)
                continue
            # --- actors (lazy on-court inference) and box-score counts
            oncourt.setdefault(team, {})
            if at in INFER_TYPES and not arrs["technicalish"][r] and pid:
                ensure_on(team, pid, t, ps, per)
            if at in ("2pt", "3pt"):
                s = st(team, pid) if pid else None
                made = arrs["shotResult"][r] == "Made"
                if s is not None:
                    s["fga"] += 1
                    s["fgm"] += int(made)
                    if at == "3pt":
                        s["tpa"] += 1
                        s["tpm"] += int(made)
                    if made:
                        s["pts"] += 3 if at == "3pt" else 2
                ap = arrs["assistPersonId"][r]
                if made and not pd.isna(ap):
                    ensure_on(team, int(ap), t, ps, per)
                    st(team, int(ap))["ast"] += 1
            elif at == "freethrow" and pid:
                made = arrs["shotResult"][r] == "Made"
                s = st(team, pid)
                s["fta"] += 1
                s["ftm"] += int(made)
                s["pts"] += int(made)
            elif at == "rebound" and pid:
                s = st(team, pid)
                s["reb"] += 1
                s["oreb"] += int(ty == "offensive")
            elif at == "turnover" and pid:
                st(team, pid)["tov"] += 1
            elif at == "steal" and pid:
                st(team, pid)["stl"] += 1
            elif at == "block" and pid:
                st(team, pid)["blk"] += 1
        # close anything still open at the end of the game data
        for tm in list(oncourt):
            for p in list(oncourt[tm]):
                credit(tm, p, period_end_t)
        for (tm, p), s in stats.items():
            rows.append({"game_id": int(gid), "season": season_label, "team": tm, "player_id": p,
                         "name": names.get(p, ""), "start": int((tm, p) in started), "min": s["sec"] / 60.0,
                         **{c: s[c] for c in STAT_COLS}, "n_periods": int(d["period"].iloc[j - 1])})
        i = j
    pg = pd.DataFrame(rows)
    return pg


def validate_player_logs(pg: pd.DataFrame, games: pd.DataFrame) -> dict:
    """Reconcile player logs to the team-level game table (points, minutes, starters)."""
    g = games.set_index("game_id")
    tm = pg.groupby(["game_id", "team"]).agg(min=("min", "sum"), pts=("pts", "sum"), starters=("start", "sum"),
                                              n_players=("player_id", "size"), n_periods=("n_periods", "first")).reset_index()
    tm["is_home"] = tm["team"].values == g.loc[tm["game_id"], "home"].values
    tm["team_pts"] = np.where(tm["is_home"], g.loc[tm["game_id"], "home_pts"].values, g.loc[tm["game_id"], "away_pts"].values)
    tm["exp_min"] = 240 + 25 * (tm["n_periods"] - 4)
    tm["min_gap"] = tm["min"] - tm["exp_min"]
    return {
        "team_games": int(len(tm)),
        "minutes_within_1": float((tm["min_gap"].abs() <= 1.0).mean()),
        "minutes_within_5": float((tm["min_gap"].abs() <= 5.0).mean()),
        "minutes_mean_gap": float(tm["min_gap"].mean()),
        "minutes_worst": float(tm["min_gap"].abs().max()),
        "points_exact": float((tm["pts"] == tm["team_pts"]).mean()),
        "points_within_3": float(((tm["pts"] - tm["team_pts"]).abs() <= 3).mean()),
        "points_mean_gap": float((tm["pts"] - tm["team_pts"]).mean()),
        "starters_eq_5": float((tm["starters"] == 5).mean()),
        "starters_ge_5": float((tm["starters"] >= 5).mean()),
        "avg_players_per_team_game": float(tm["n_players"].mean()),
    }, tm
