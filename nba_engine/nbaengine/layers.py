"""Derived layers built from the stored ESPN game data (nbaengine/gamedata.py). Every function takes a list of game records and returns tidy tables.
Quarter scores, shot zones, lineups and on/off, clutch, officials, closing-line odds and extra team statistics. Only what ESPN publishes; no estimates of
tracking data (touches, pick-and-roll, isolation, defender assignment) because none exists in this source."""
from __future__ import annotations
import re
import numpy as np, pandas as pd

_DIST = re.compile(r"(\d+)-foot")


def _clock_s(c):
    try:
        m, s = str(c).split(":"); return int(m) * 60 + float(s)
    except Exception:
        return np.nan


def _num(x):
    try:
        return float(str(x).replace("o", "").replace("u", "").replace("+", ""))
    except Exception:
        return np.nan


def home_away(rec):
    """-> (home team id, away team id) from the stored team blocks"""
    h = a = None
    for tid, t in rec["teams"].items():
        if t.get("home_away") == "home": h = tid
        elif t.get("home_away") == "away": a = tid
    return h, a


# ------------------------------------------------------------------------------------------------ quarters
def quarters(G) -> pd.DataFrame:
    rows = []
    for r in G:
        h, a = home_away(r)
        if not h or not a:
            continue
        lh, la = r["teams"][h]["linescores"], r["teams"][a]["linescores"]
        if len(lh) < 4 or len(la) < 4:
            continue
        d = {"game_id": r["game_id"], "date": r["date"], "season": r["season"], "home": r["teams"][h]["abbr"], "away": r["teams"][a]["abbr"]}
        for i in range(4):
            d[f"h_q{i+1}"], d[f"a_q{i+1}"] = float(lh[i]), float(la[i])
        d["ot"] = max(len(lh), len(la)) - 4
        rows.append(d)
    D = pd.DataFrame(rows)
    if len(D):
        D["h_h1"], D["a_h1"] = D.h_q1 + D.h_q2, D.a_q1 + D.a_q2
        D["h_h2"], D["a_h2"] = D.h_q3 + D.h_q4, D.a_q3 + D.a_q4
        D["total_reg"] = D[[f"{s}_q{i}" for s in "ha" for i in range(1, 5)]].sum(axis=1)
        D["h1_share"] = (D.h_h1 + D.a_h1) / D.total_reg
        D["q1_share"] = (D.h_q1 + D.a_q1) / D.total_reg
    return D


# ------------------------------------------------------------------------------------------------ shots and zones
def zone(text, typ, xy, is3):
    d = _DIST.search(text or "")
    dist = float(d.group(1)) if d else np.nan
    t = (typ or "").lower()
    if is3:
        x, y = (xy or [np.nan, np.nan])[:2]
        if x is not None and y is not None and (x <= 3 or x >= 47) and y <= 14:
            return "corner three"
        return "above-break three"
    if "layup" in t or "dunk" in t or "tip" in t or "finger roll" in t or dist <= 4:
        return "at rim"
    if dist <= 13:
        return "short (5-13 ft)"
    return "mid-range"


def shots(G) -> pd.DataFrame:
    rows = []
    for r in G:
        h, a = home_away(r)
        for p in r["plays"]:
            if not p.get("shooting") or "Free Throw" in (p.get("type") or ""):
                continue
            t = p.get("text") or ""
            if " blocks " in t:
                continue                              # block lines duplicate the missed-shot line
            is3 = "three point" in t
            made = bool(p.get("scoring"))
            xy = p.get("xy")
            rows.append({"game_id": r["game_id"], "date": r["date"], "team": p.get("team"), "is_home": p.get("team") == h, "player": (p.get("players") or [None])[0],
                         "period": p.get("period"), "made": made, "is3": is3, "zone": zone(t, p.get("type"), xy, is3), "type": p.get("type"),
                         "assisted": "assists" in t, "x": xy[0] if xy else np.nan, "y": xy[1] if xy else np.nan})
    return pd.DataFrame(rows)


def zone_table(S: pd.DataFrame, by="team") -> pd.DataFrame:
    """share of attempts and points per shot by zone, per team (or player)"""
    g = S.groupby([by, "zone"]).agg(att=("made", "size"), fg=("made", "mean")).reset_index()
    g["share"] = g.att / g.groupby(by).att.transform("sum")
    g["pps"] = g.fg * np.where(g.zone.str.contains("three"), 3, 2)
    return g


# ------------------------------------------------------------------------------------------------ stints, lineups, on/off, bench
def stints(G):
    """Walk each game's play-by-play, tracking the five players on court per team from the starters and substitution plays.
    Returns (stint table, game-level bench summary). A stint ends at every substitution or period boundary."""
    rows = []
    for r in G:
        starters = {}
        for p in r.get("players", []):
            if p.get("starter"):
                starters.setdefault(p["team"], set()).add(p["id"])
        if len(starters) != 2 or any(len(v) != 5 for v in starters.values()):
            continue
        tids = list(starters)
        on = {t: set(starters[t]) for t in tids}
        last = {"t": 0.0, "h": 0, "a": 0, "per": 1}
        h, a = home_away(r)
        plays = [p for p in r["plays"] if p.get("period") and p.get("period") <= 4]
        def flush(now, hs, as_, per):
            dur = last["t"] - now
            if dur > 0:
                for t in tids:
                    is_home = t == h
                    pf = (hs - last["h"]) if is_home else (as_ - last["a"]); pa = (as_ - last["a"]) if is_home else (hs - last["h"])
                    rows.append({"game_id": r["game_id"], "date": r["date"], "team": t, "is_home": is_home, "lineup": tuple(sorted(on[t])), "sec": dur, "pf": pf, "pa": pa, "period": per})
        last = {"t": 720.0, "h": 0, "a": 0, "per": 1}
        for p in plays:
            per, now = p["period"], _clock_s(p["clock"])
            if per != last["per"]:
                flush(0.0, last["h"], last["a"], last["per"])
                last = {"t": 720.0, "h": last["h"], "a": last["a"], "per": per}
            if p.get("type") == "Substitution" and len(p.get("players") or []) == 2 and now == now:
                inn, out = p["players"]
                tm = next((t for t in tids if out in on[t]), None)
                if tm is None:
                    continue
                flush(now, p.get("home") or last["h"], p.get("away") or last["a"], per)
                last.update({"t": now, "h": p.get("home") if p.get("home") is not None else last["h"], "a": p.get("away") if p.get("away") is not None else last["a"]})
                on[tm].discard(out); on[tm].add(inn)
            else:
                if p.get("home") is not None: last["h_seen"] = p["home"]
                if p.get("away") is not None: last["a_seen"] = p["away"]
        flush(0.0, last.get("h_seen", last["h"]), last.get("a_seen", last["a"]), last["per"])
    return pd.DataFrame(rows)


def lineup_table(S: pd.DataFrame, min_minutes=15) -> pd.DataFrame:
    g = S.groupby(["team", "lineup"]).agg(min=("sec", lambda x: x.sum() / 60), pf=("pf", "sum"), pa=("pa", "sum"), games=("game_id", "nunique")).reset_index()
    g["net_per48"] = (g.pf - g.pa) / g["min"] * 48
    return g[g["min"] >= min_minutes].sort_values("net_per48", ascending=False)


def on_off(S: pd.DataFrame, min_on=60) -> pd.DataFrame:
    """player on/off: team net points per 48 minutes with the player on vs off the floor (raw, no adjustment for teammates or opponents)"""
    rows = []
    for team, g in S.groupby("team"):
        tot_sec, tot_net = g.sec.sum(), (g.pf - g.pa).sum()
        for pid in set(i for lu in g.lineup for i in lu):
            on = g[g.lineup.map(lambda lu: pid in lu)]
            sec_on, net_on = on.sec.sum(), (on.pf - on.pa).sum()
            sec_off, net_off = tot_sec - sec_on, tot_net - net_on
            if sec_on / 60 >= min_on and sec_off / 60 >= 20:
                rows.append({"team": team, "player": pid, "min_on": sec_on / 60, "net_on_48": net_on / sec_on * 2880, "net_off_48": net_off / sec_off * 2880})
    D = pd.DataFrame(rows)
    if len(D):
        D["on_off"] = D.net_on_48 - D.net_off_48
    return D


def bench_summary(G) -> pd.DataFrame:
    """bench (non-starter) points, minutes share and unit sizes per team-game from the box-score player lines"""
    rows = []
    for r in G:
        for t in {p["team"] for p in r.get("players", [])}:
            pl = [p for p in r["players"] if p["team"] == t and p.get("stats")]
            if not pl:
                continue
            def pt(p):
                try: return float(p["stats"][-1])
                except Exception: return np.nan
            def mn(p):
                try: return float(p["stats"][0])
                except Exception: return np.nan
            bp = sum(pt(p) for p in pl if not p["starter"]); tp = sum(pt(p) for p in pl)
            bm = sum(mn(p) for p in pl if not p["starter"]); tm = sum(mn(p) for p in pl)
            rows.append({"game_id": r["game_id"], "team": t, "bench_pts": bp, "bench_pts_share": bp / tp if tp else np.nan, "bench_min_share": bm / tm if tm else np.nan,
                         "players_used": sum(1 for p in pl if mn(p) > 0)})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ clutch
def clutch(G) -> pd.DataFrame:
    """last 5 minutes of the 4th quarter (or overtime) with the score within 5: team points for/against and the seconds played"""
    rows = []
    for r in G:
        h, a = home_away(r)
        prev_t, prev_h, prev_a = None, 0, 0
        sec = pf_h = pf_a = 0.0
        for p in r["plays"]:
            per, now = p.get("period"), _clock_s(p.get("clock"))
            hs, as_ = p.get("home"), p.get("away")
            if per is None or now != now or hs is None or as_ is None:
                continue
            in_win = per >= 4 and now <= 300 and abs(prev_h - prev_a) <= 5
            if in_win and prev_t is not None and prev_t[0] == per:
                sec += max(prev_t[1] - now, 0); pf_h += hs - prev_h; pf_a += as_ - prev_a
            prev_t, prev_h, prev_a = (per, now), hs, as_
        if sec > 0:
            rows.append({"game_id": r["game_id"], "date": r["date"], "home": r["teams"][h]["abbr"] if h else None, "away": r["teams"][a]["abbr"] if a else None,
                         "clutch_sec": sec, "home_pts": pf_h, "away_pts": pf_a})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ officials, odds, team extras
def officials(G) -> pd.DataFrame:
    rows = []
    for r in G:
        names = [o.get("displayName") or o.get("fullName") for o in (r.get("officials") or [])]
        fouls = sum(1 for p in r["plays"] if (p.get("type") or "").endswith("Foul") or "Foul" in (p.get("type") or ""))
        fts = sum(1 for p in r["plays"] if "Free Throw" in (p.get("type") or ""))
        rows.append({"game_id": r["game_id"], "date": r["date"], "season": r["season"], "crew": tuple(sorted(n for n in names if n)), "fouls": fouls, "free_throws": fts,
                     "technicals": sum(1 for p in r["plays"] if "Technical" in (p.get("type") or ""))})
    return pd.DataFrame(rows)


def odds(G) -> pd.DataFrame:
    """closing and opening spread (home perspective, negative = home favourite), total and moneyline from the first listed book"""
    rows = []
    for r in G:
        o = (r.get("odds") or r.get("pickcenter") or [None])
        o = o[0] if isinstance(o, list) and o else None
        if not isinstance(o, dict):
            continue
        ps = o.get("pointSpread") or {}; tot = o.get("total") or {}; ml = o.get("moneyline") or {}
        def g(d, *k):
            for x in k:
                d = (d or {}).get(x) if isinstance(d, dict) else None
            return d
        rows.append({"game_id": r["game_id"], "date": r["date"], "book": o.get("provider") if isinstance(o.get("provider"), str) else (o.get("provider") or {}).get("name"),
                     "spread_close": _num(g(ps, "home", "close", "line")), "spread_open": _num(g(ps, "home", "open", "line")),
                     "total_close": _num(g(tot, "over", "close", "line")), "total_open": _num(g(tot, "over", "open", "line")),
                     "ml_home_close": _num(g(ml, "home", "close", "odds")), "ml_home_open": _num(g(ml, "home", "open", "odds")),
                     "ml_away_close": _num(g(ml, "away", "close", "odds"))})
    D = pd.DataFrame(rows)
    if len(D):
        D["spread_move"] = D.spread_close - D.spread_open; D["total_move"] = D.total_close - D.total_open
    return D


def _p(ml):
    ml = np.where(np.isfinite(ml) & (ml != 0), ml, np.nan)
    return np.where(ml < 0, -ml / (-ml + 100), 100 / (ml + 100))


def implied_home_prob(D: pd.DataFrame) -> pd.Series:
    """no-vig home win probability from the closing moneyline pair"""
    ph, pa = _p(D.ml_home_close.to_numpy()), _p(D.ml_away_close.to_numpy())
    return pd.Series(ph / (ph + pa), index=D.index)


def team_extras(G) -> pd.DataFrame:
    rows = []
    for r in G:
        for t in r.get("team_stats") or []:
            d = {s["name"]: s["value"] for s in t["stats"]}
            def f(k):
                try: return float(str(d.get(k)).split("-")[0])
                except Exception: return np.nan
            tid = t["team"]; tm = r["teams"].get(tid, {})
            rows.append({"game_id": r["game_id"], "date": r["date"], "team_id": tid, "team": tm.get("abbr"), "home": tm.get("home_away") == "home",
                         "fast_break_pts": f("fastBreakPoints"), "paint_pts": f("pointsInPaint"), "tov_pts": f("turnoverPoints"), "fouls": f("fouls"), "steals": f("steals"),
                         "blocks": f("blocks"), "assists": f("assists"), "largest_lead": f("largestLead"), "lead_changes": f("leadChanges")})
    return pd.DataFrame(rows)
