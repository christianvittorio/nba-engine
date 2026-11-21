"""Usage + opponent defense-vs-position + season 90% alternate prop research.

Only published broad G/F/C role labels are supported by the current
sportsdataverse roster feed. PG/SG/SF/PF attribution is NEVER fabricated.
The 90% threshold describes past observed season box scores, not a calibrated
future hit probability. This module does not buy odds or place a bet.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
import json
from math import isfinite, prod, sqrt
from pathlib import Path
import sqlite3
from zoneinfo import ZoneInfo

from .contracts import iso, utc
from .market_probabilities import exact_line_probabilities
from .market_value import _validate_quote

VERSION = "gpt-v2-usage-dvp-90-alt-props-0.1"
ET = ZoneInfo("America/New_York")
POSITIONS = frozenset({"G", "F", "C"})
STATS = ("pts", "ast", "reb")
ALTS = {
    "pts": "player_points_alternate",
    "ast": "player_assists_alternate",
    "reb": "player_rebounds_alternate",
}
# Meaningful lower bounds; don't call a 0.5-point ladder high-value research.
STARTS = {"pts": 9.5, "ast": 2.5, "reb": 3.5}


def _num(x):
    if isinstance(x, bool) or x is None:
        return None
    try:
        v = float(x)
        return v if isfinite(v) else None
    except (ValueError, TypeError, OverflowError):
        return None


def wilson_lower_bound(hits: int, games: int, z: float = 1.96) -> float:
    """Descriptive 95% binomial lower bound, NOT a predictive calibration."""
    if games <= 0 or not 0 <= hits <= games:
        raise ValueError("Invalid history counts")
    p = hits / games
    return (p+z*z/(2*games)-z*sqrt((p*(1-p)+z*z/(4*games))/games)) / (
        1+z*z/games
    )


def highest_90pct_line(values: list[float], stat: str, *,
                        minimum_games: int = 12,
                        target_rate: float = .90,
                        minimum_last_five_rate: float = .80) -> dict | None:
    """Pick highest half-point over line observed in >=90% of season games.

    A hit means game stat > line; no integer pushes at half-point lines.
    No post-selection correction: the 90% in-sample percentage is optimistic.
    """
    if stat not in STATS or minimum_games < 1 or not 0 < target_rate <= 1:
        raise ValueError("Invalid stat or hit-rate constraints")
    if not 0 <= minimum_last_five_rate <= 1:
        raise ValueError("Invalid recent-form requirement")
    if len(values) < minimum_games or any(
        _num(v) is None or float(v) < 0 for v in values
    ):
        return None
    recent = values[-5:]
    largest = int(max(values))
    for whole in range(largest, int(STARTS[stat]), -1):
        line = whole-.5
        if line < STARTS[stat]:
            break
        hits = sum(v>line for v in values)
        hit_last_five = sum(v>line for v in recent)
        if (hits/len(values) >= target_rate
                and hit_last_five/len(recent) >= minimum_last_five_rate):
            return {
                "line": line, "hits": hits, "games": len(values),
                "raw_season_hit_rate": hits/len(values),
                "last_five_hits": hit_last_five,
                "raw_last_five_hit_rate": hit_last_five/len(recent),
                "wilson_95pct_lower_descriptive": wilson_lower_bound(hits,len(values)),
                "not_a_future_probability": True,
            }
    return None


def _positions(con: sqlite3.Connection, season: int) -> dict[tuple[str,str],str]:
    observed = defaultdict(set)
    for pid, tid, position in con.execute(
        "SELECT player_id,team_id,published_position FROM roster_assignments "
        "WHERE season=? AND source_id='sportsdataverse'", (season,)
    ):
        pos=str(position or "").strip().upper()
        if pos:
            observed[(str(pid),str(tid))].add(pos)
    # Retain only one documented unambiguous broad position; hybrid
    # G-F/F-C are NOT assigned arbitrarily to either role.
    return {key:next(iter(labels)) for key,labels in observed.items()
            if len(labels)==1 and next(iter(labels)) in POSITIONS}


def _history(con: sqlite3.Connection, season: int, day: str) -> tuple[list[dict],dict]:
    # Strict prior date: no same-day outcomes, in-progress games, playoffs,
    # or post-tip source observations masquerading as pregame facts.
    team = {}
    for gid,tid,raw in con.execute(
        "SELECT t.game_id,t.team_id,t.stats_json FROM team_game_stats t "
        "JOIN games g ON g.game_id=t.game_id "
        "WHERE g.season=? AND g.game_date_eastern<? "
        "AND g.game_type='regular_season' AND g.status='final' "
        "AND t.source_id='nba_stats_archive'",
        (season,day),
    ):
        team[(str(gid),str(tid))]=json.loads(raw)
    rows=[]
    query=(
        "SELECT p.game_id,p.player_id,p.team_id,players.canonical_name,"
        "g.game_date_eastern,g.home_team_id,g.away_team_id,p.stats_json "
        "FROM player_game_stats p JOIN games g ON g.game_id=p.game_id "
        "JOIN players ON players.player_id=p.player_id "
        "WHERE g.season=? AND g.game_date_eastern<? "
        "AND g.game_type='regular_season' AND g.status='final' "
        "AND p.source_id='nba_stats_archive' "
        "ORDER BY g.game_date_eastern,p.game_id,p.player_id"
    )
    for gid,pid,tid,name,date,home,away,raw in con.execute(query,(season,day)):
        v=json.loads(raw)
        minute=_num(v.get("min"))
        if minute is None or minute<=0:
            continue
        if str(tid)==str(home):
            opponent=str(away)
        elif str(tid)==str(away):
            opponent=str(home)
        else:
            raise ValueError("Player history team absent from verified game")
        rows.append({
            "game_id":str(gid),"player_id":str(pid),"team_id":str(tid),
            "player":str(name or ""),"day":str(date),"opponent_id":opponent,
            "min":minute,"stats":v,
        })
    return rows,team


def _team_usage(row: dict, team_stats: dict) -> float | None:
    """Use NBA season published USG% when available; otherwise a transparent
    boxscore estimate using 48 regulation team minutes per game.
    """
    pct = _num(row["stats"].get("usg_pct"))
    if pct is not None:
        pct = pct*100 if 0<pct<=1 else pct
        if 0<pct<70:
            return pct
    t = team_stats.get((row["game_id"],row["team_id"]))
    if not t:
        return None
    fga,fta,tov=(_num(row["stats"].get(k)) for k in ("fga","fta","tov"))
    tfga,tfta,ttov=(_num(t.get(k)) for k in ("fga","fta","tov"))
    if None in (fga,fta,tov,tfga,tfta,ttov):
        return None
    denominator=tfga+.44*tfta+ttov
    if denominator<=0 or row["min"]<=0:
        return None
    estimate=100*48*(fga+.44*fta+tov)/(row["min"]*denominator)
    return estimate if 0<estimate<70 else None


def defense_ranks(rows: list[dict], positions: dict, team_ids: set[str], *,
                  minimum_defense_games: int = 10,
                  minimum_position_minutes: float = 150) -> tuple[dict,dict]:
    """Ranks MOST permissive defenses (rank 1 = most allowed).

    Uses opponent box-score counting stats per 48 documented position-group
    minutes, not individual defender attribution, not PG/SG role guesses.
    Require a sufficiently complete all-30-team comparison for each stat.
    """
    allowed=defaultdict(lambda:{"minutes":0.0, "games":set(),
                                "pts":0.0,"ast":0.0,"reb":0.0})
    for x in rows:
        pos=positions.get((x["player_id"],x["team_id"]))
        if pos not in POSITIONS:
            continue
        key=(x["opponent_id"],pos)
        item=allowed[key]
        item["minutes"]+=x["min"]
        item["games"].add(x["game_id"])
        for stat in STATS:
            v=_num(x["stats"].get(stat))
            if v is not None and v>=0:
                item[stat]+=v
    ranks={}
    coverage={}
    for position in sorted(POSITIONS):
        entries=[]
        for team_id in sorted(team_ids):
            obj=allowed.get((team_id,position))
            if (not obj or len(obj["games"])<minimum_defense_games
                    or obj["minutes"]<minimum_position_minutes):
                continue
            entries.append((team_id,obj))
        coverage[position]={
            "valid_defensive_teams":len(entries), "required_teams":len(team_ids),
            "rankable":len(team_ids)==30 and len(entries)==30,
        }
        if len(team_ids)!=30 or len(entries)!=30:
            continue
        for stat in STATS:
            scores=sorted(
                ((tid,48*float(x[stat])/x["minutes"],len(x["games"]))
                 for tid,x in entries), key=lambda z:(-z[1],z[0])
            )
            for idx,(tid,score,ngames) in enumerate(scores,1):
                ranks[(tid,position,stat)]={
                    "rank_most_allowed":idx,
                    "rank_out_of":30,
                    "allowed_per_48_group_minutes":round(score,3),
                    "defense_games":ngames,
                    "position_group":position,
                    "stat":stat,
                    "definition":"opposing_players_boxscore_per_48_published_role_minutes",
                }
    return ranks,coverage


def _quote_candidates(candidates: list[dict], quotes: list[dict],
                      forecasts: dict, now: datetime) -> list[dict]:
    """No fake alt prices. Evaluate only original exact two-sided book quotes."""
    base={}
    for raw in quotes:
        try:
            q=_validate_quote(raw)
        except (KeyError,ValueError,TypeError):
            continue
        if q["market_type"]!="player_prop" or q["selection"] not in ("over","under"):
            continue
        if q.get("provider_market_key") not in ALTS.values():
            continue
        retrieval=q.get("retrieved_at_utc")
        if (not retrieval or utc(retrieval)>now or
                utc(retrieval)>utc(q["tip_utc"])):
            continue
        key=(q["game_id"],q["book"],q["market_id"],q.get("player_id"),q["line"])
        base.setdefault(key,{})[q["selection"]]=q
    verified=[]
    for c in candidates:
        doc=forecasts.get(c["game_id"])
        if doc is None or utc(doc["cutoff_utc"])>=utc(doc["tip_utc"]):
            continue
        for (gid,book,mid,pid,line),pair in base.items():
            if gid!=c["game_id"] or pid!=c["player_id"] or line!=c["alt_over_line"]:
                continue
            if not all(side in pair for side in ("over","under")):
                continue
            over,under=pair["over"],pair["under"]
            if (over["provider_market_key"] != ALTS[c["stat"]]
                    or under["provider_market_key"] != ALTS[c["stat"]]):
                continue
            if any(utc(q["retrieved_at_utc"])>utc(doc["cutoff_utc"])
                   or q["tip_utc"]!=doc["tip_utc"] for q in (over,under)):
                continue
            # Full-time player stat histogram from the frozen simulation.
            try:
                exact=exact_line_probabilities(over,doc)
            except (KeyError,TypeError,ValueError):
                continue
            if exact is None:
                continue
            modeled=exact["probability"]
            push=exact["push_probability"]
            odds=over["decimal_odds"]
            roi=modeled*odds+push-1
            if roi<0.001:
                continue
            verified.append({
                **c,"book":book,"decimal_odds":odds,
                "model_probability_uncalibrated":modeled,
                "modeled_roi_uncalibrated":roi,
                "quote_retrieved_at_utc":over["retrieved_at_utc"],
                "source_verified":True,"actionable":False,
            })
    return verified


def build_alt_prop_research(con: sqlite3.Connection, *,
                            now_utc: str | None = None,
                            date_eastern: str | None = None,
                            minimum_season_games: int = 12,
                            minimum_usage_percent: float = 24,
                            max_team_usage_rank: int = 2,
                            min_defense_games: int = 10,
                            minimum_recent_minutes: float = 20,
                            odds_quotes: list[dict] | None = None,
                            forecasts: list[dict] | None = None) -> dict:
    """Research-only alt-prop watchlist and optional SOURCE-PRICED same-book
    parlay. Hit rate >=90% is strictly observed current-season history.
    """
    if minimum_season_games<10 or not 0<=minimum_usage_percent<100:
        raise ValueError("Minimum season sample is ten and usage threshold valid")
    if not 1<=max_team_usage_rank<=5 or min_defense_games<1:
        raise ValueError("Invalid usage ranking or defense sample")
    now=utc(now_utc) if now_utc else datetime.now(timezone.utc)
    if date_eastern:
        datetime.strptime(date_eastern,"%Y-%m-%d")
    games=[dict(r) for r in con.execute(
        "SELECT game_id,season,game_date_eastern,tip_utc,"
        "home_team_id,away_team_id FROM games "
        "WHERE game_type='regular_season' AND status='scheduled' "
        "AND tip_utc IS NOT NULL ORDER BY tip_utc,game_id"
    ) if utc(r["tip_utc"])>now and (
       date_eastern is None or r["game_date_eastern"]==date_eastern)]
    # A default daily run covers the local Eastern current/next day, not
    # distant future fixtures when there are no imminent games.
    if date_eastern is None:
        today=now.astimezone(ET).date()
        valid_dates={today.isoformat(),__import__("datetime").timedelta(days=1).__radd__(today).isoformat()}
        games=[g for g in games if g["game_date_eastern"] in valid_dates]
    if not games:
        return {
            "version":VERSION,"research_only":True,
            "status":"NO_UPCOMING_PRETIP_GAMES","candidates":[],
            "priced_alternate_legs":[],"same_book_parlay":None,
            "missing_requirements":["NO_UPCOMING_PRETIP_GAMES"],
            "limitations":["No bets or calibrated predictions."],
        }
    forecast_by_game={x["game_id"]:x for x in (forecasts or [])}
    candidates=[]
    coverage_reports=[]
    excluded=defaultdict(int)
    teams={r[0] for r in con.execute(
        "SELECT DISTINCT home_team_id FROM games WHERE season=? "
        "UNION SELECT DISTINCT away_team_id FROM games WHERE season=?",
        (games[0]["season"],games[0]["season"])
    )}
    cache={}
    for g in games:
        season=int(g["season"]);day=g["game_date_eastern"]
        key=(season,day)
        if key not in cache:
            history, teamstats=_history(con,season,day)
            pos=_positions(con,season)
            rankings,coverage=defense_ranks(
                history,pos,teams,minimum_defense_games=min_defense_games
            )
            cache[key]=(history,teamstats,pos,rankings,coverage)
            coverage_reports.append({"asof_date_eastern":day,"season":season,
                                     "position_coverage":coverage})
        history,teamstats,pos,rankings,coverage=cache[key]
        grouped=defaultdict(list)
        for x in history:
            if x["team_id"] in (g["home_team_id"],g["away_team_id"]):
                grouped[(x["player_id"],x["team_id"])].append(x)
        qualified=[]
        for (pid,tid),records in grouped.items():
            if len(records)<minimum_season_games:
                excluded["INSUFFICIENT_PLAYER_SEASON_GAMES"]+=1
                continue
            if pos.get((pid,tid)) not in POSITIONS:
                excluded["NO_EXACT_BROAD_ROLE_LABEL"]+=1
                continue
            avg_mins=sum(r["min"] for r in records)/len(records)
            recent_mins=sum(r["min"] for r in records[-5:])/min(5,len(records))
            if avg_mins<20 or recent_mins<minimum_recent_minutes:
                excluded["INSUFFICIENT_RECENT_PLAYING_TIME"]+=1
                continue
            usages=[]
            for r in records:
                u=_team_usage(r,teamstats)
                if u is not None:
                    usages.append((u,r["min"]))
            if len(usages)<minimum_season_games-2:
                excluded["NO_RELIABLE_USAGE_EVIDENCE"]+=1
                continue
            u=sum(u*m for u,m in usages)/sum(m for _,m in usages)
            if u<minimum_usage_percent:
                excluded["LOW_USAGE"]+=1
                continue
            qualified.append((pid,tid,records,u,avg_mins,recent_mins))
        byteam=defaultdict(list)
        for item in qualified:
            byteam[item[1]].append(item)
        top={}
        for tid,items in byteam.items():
            for rank,item in enumerate(sorted(
                items,key=lambda x:(-x[3],x[0])),1):
                top[(tid,item[0])]=rank
        for pid,tid,records,usage,avg_mins,recent_mins in qualified:
            rank=top[(tid,pid)]
            if rank>max_team_usage_rank:
                excluded["NOT_TOP_TEAM_USAGE"]+=1
                continue
            opponent=(g["away_team_id"] if tid==g["home_team_id"]
                      else g["home_team_id"])
            position=pos[(pid,tid)]
            source_status="unknown"
            status_data=con.execute(
                "SELECT normalized_status FROM availability_reports "
                "WHERE game_id=? AND player_id=? AND report_utc<=? "
                "AND retrieved_at_utc<=? ORDER BY report_utc DESC LIMIT 1",
                (g["game_id"],pid,iso(now),iso(now)),
            ).fetchone()
            if status_data is not None:
                source_status=status_data[0]
            if source_status in ("out","doubtful","questionable"):
                excluded["UNSAFE_AVAILABILITY_STATUS"]+=1
                continue
            for stat in STATS:
                definfo=rankings.get((opponent,position,stat))
                if definfo is None:
                    excluded["DVP_RANK_UNVERIFIED"]+=1
                    continue
                if definfo["rank_most_allowed"]>5:
                    excluded["OPPONENT_NOT_BOTTOM_FIVE"]+=1
                    continue
                values=[_num(r["stats"].get(stat)) for r in records]
                if any(v is None for v in values):
                    excluded["INCOMPLETE_PLAYER_STAT_HISTORY"]+=1
                    continue
                ladder=highest_90pct_line(values,stat,
                                          minimum_games=minimum_season_games)
                if ladder is None:
                    excluded["NO_MEANINGFUL_90PCT_ALT_THRESHOLD"]+=1
                    continue
                h2h=[r for r in records if r["opponent_id"]==opponent]
                h2h_hits=sum((_num(r["stats"].get(stat)) or 0)>ladder["line"]
                             for r in h2h)
                candidates.append({
                    "game_id":g["game_id"],"tip_utc":g["tip_utc"],
                    "date_eastern":day,"player_id":pid,
                    "player":next((r["player"] for r in reversed(records)
                                   if r["player"]),"NBA ID "+pid.split(":")[-1]),
                    "team_id":tid,"opponent_team_id":opponent,
                    "position_group":position, "stat":stat,
                    "team_usage_rank":rank,
                    "estimated_usage_percent":round(usage,2),
                    "avg_minutes_season":round(avg_mins,1),
                    "avg_minutes_last_five":round(recent_mins,1),
                    "availability":"UNCONFIRMED" if source_status=="unknown"
                        else source_status,
                    "opponent_defense":definfo,
                    "alt_over_line":ladder["line"],
                    "season_hits":ladder["hits"],
                    "season_games":ladder["games"],
                    "raw_season_hit_rate":ladder["raw_season_hit_rate"],
                    "last_five_hits":ladder["last_five_hits"],
                    "wilson_95pct_lower_descriptive":ladder[
                        "wilson_95pct_lower_descriptive"],
                    "same_opponent_hits":h2h_hits,
                    "same_opponent_games":len(h2h),
                    "same_opponent_rate_not_sufficiently_sampled":len(h2h)<5,
                    "line_is_statistical_threshold_not_book_offer":True,
                    "actionable":False,
                })
    candidates.sort(key=lambda x:(
        -x["raw_season_hit_rate"],-x["estimated_usage_percent"],
        x["opponent_defense"]["rank_most_allowed"],
        -x["alt_over_line"],x["game_id"],x["player_id"],x["stat"]
    ))
    priced=_quote_candidates(candidates,odds_quotes or [],forecast_by_game,now)
    priced.sort(key=lambda x:(
        -x["model_probability_uncalibrated"],
        -x["modeled_roi_uncalibrated"],x["player_id"],x["game_id"]
    ))
    # Same bookmaker, separate games, same US Eastern calendar day only;
    # don't assume two player legs from one game are independent.
    evaluated=[]
    for a,b in combinations(priced,2):
        if (a["book"]!=b["book"] or a["game_id"]==b["game_id"]
                or a["date_eastern"]!=b["date_eastern"]):
            continue
        joint=a["model_probability_uncalibrated"]*b["model_probability_uncalibrated"]
        estimated=(1+a["modeled_roi_uncalibrated"])*(
            1+b["modeled_roi_uncalibrated"])-1
        evaluated.append({
            "book":a["book"],"legs":[a,b],
            "raw_model_joint_win_probability_independent":joint,
            "raw_model_estimated_roi_independent":estimated,
            "uncalibrated":True,"actionable":False,
        })
    evaluated.sort(key=lambda x:(
        -x["raw_model_joint_win_probability_independent"],
        -x["raw_model_estimated_roi_independent"],
    ))
    missing=[]
    if not candidates:
        missing.append("NO_VERIFIED_BOTTOM5_HIGH_USAGE_90PCT_HIT_COMBINATION")
    if not priced:
        missing.append("NO_SOURCE_VERIFIED_ALT_PLAYER_PROP_ODDS_AND_MODEL_PRICE_MATCH")
    if not evaluated:
        missing.append("NO_TWO_DISTINCT_GAMES_SAME_BOOK_WITH_ELIGIBLE_PRICED_ALT_LINES")
    return {
        "version":VERSION,"research_only":True,"actionable":False,
        "betting_recommendation":None,"generated_at_utc":iso(now),
        "games_reviewed":len(games),
        "season_hit_threshold":0.9,"minimum_season_games":minimum_season_games,
        "usage_filter":{"minimum_usage_percent":minimum_usage_percent,
                        "max_team_usage_rank":max_team_usage_rank},
        "position_scope":"published_G_F_C_only_no_invented_PG_SG_SF_PF",
        "dvp_rank_direction":"1=most_position_group_stats_allowed_per_48",
        "defense_coverage":coverage_reports,
        "candidates":candidates,
        "priced_alternate_legs":priced,
        "same_book_parlay":evaluated[0] if evaluated else None,
        "missing_requirements":missing,
        "exclusion_counts":dict(sorted(excluded.items())),
        "status":("PRICED_RESEARCH_PARLAY_AVAILABLE" if evaluated else
                  "STATISTICAL_WATCHLIST_ONLY" if candidates else
                  "NO_VERIFIED_90_PERCENT_MATCHUP"),
        "limitations":[
            "90% is in-sample season hit frequency, NOT 90% future win probability.",
            "Wilson lower bound illustrates uncertainty; selection over many alt lines increases optimistic bias.",
            "Only broad published G/F/C categories; not actual defensive assignments.",
            "Bottom-five is stat-specific positional allowed per 48 role minutes, not an individual opponent defender.",
            "No game day / future results or after-cutoff pricing used.",
            "Actual sportsbook alt prop odds not present in anonymous ESPN game-only feed.",
            "Player availability may be unconfirmed; no lineup certainty or validated player-prop model.",
            "Same-opponent matchups are separately counted; 1-2 meetings cannot establish 90% H2H probability.",
            "No source price means watchlist only, never a fabricated line or parlay.",
        ]
    }


def render_markdown(report: dict) -> str:
    out=["# NBA Engine — 90% Season-Hit High-Usage Alternate Player Props","",
         "**RESEARCH ONLY / UNCALIBRATED / NOT A BETTING RECOMMENDATION**","",
         f"Status: **{report['status']}**.",
         f"Games reviewed: {report.get('games_reviewed',0)}.",
         "",
         "## High-usage players vs bottom-5 defenses at VERIFIED G/F/C role",
         "",
         "| Player | Game | Role | Stat | Hypothetical alt over | "
         "Season hit | Last 5 | Defense rank | Est. usage |",
         "|---|---|---|---|---:|---:|---:|---:|---:|"]
    for x in report.get("candidates",[]):
        out.append(
            f"| {x['player']} | {x['game_id']} | {x['position_group']} | "
            f"{x['stat'].upper()} | {x['alt_over_line']:.1f} | "
            f"{x['season_hits']}/{x['season_games']} "
            f"({x['raw_season_hit_rate']:.1%}) | "
            f"{x['last_five_hits']}/5 | "
            f"{x['opponent_defense']['rank_most_allowed']}/30 "
            f"(most allowed) | {x['estimated_usage_percent']:.1f}% |"
        )
    if not report.get("candidates"):
        out.append("| No sourced statistical watchlist candidates | — | — | — | — | — | — | — | — |")
    out.extend(["",
        "These alt numbers are derived from previous box scores; they are "
        "**NOT confirmed quoted sportsbook lines**.",
        "",
        "## Source-priced parlay",
        "",
        "No priced parlay can be asserted unless the same sportsbook offers "
        "the exact alt lines before the frozen forecast cutoff, with "
        "independently calibrated probabilities. Current model remains "
        "uncalibrated.",
        ""])
    if report.get("same_book_parlay"):
        out.append("A research-only mathematical combination exists; "
                   "not approved for staking or claims of profitability.")
    else:
        out.append("**NO SOURCE-VERIFIED ALTERNATE-PROP PARLAY.**")
    out.extend(["","## Missing evidence",""])
    out.extend("- "+x for x in report.get("missing_requirements",[]))
    out.extend(["","## Limitations",""])
    out.extend("- "+x for x in report.get("limitations",[]))
    out.append("")
    return "\n".join(out)


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--db",required=True,type=Path)
    ap.add_argument("--date",default=None)
    ap.add_argument("--odds-ledger",type=Path,default=None)
    ap.add_argument("--forecast-ledger",type=Path,default=None)
    ap.add_argument("--root",type=Path,default=Path("."))
    ap.add_argument("--output-json",required=True,type=Path)
    ap.add_argument("--output-md",required=True,type=Path)
    args=ap.parse_args(argv)
    odds=[]
    if args.odds_ledger and args.odds_ledger.is_file():
        from .market_run import read_jsonl
        odds=read_jsonl(args.odds_ledger)
    forecasts=[]
    if args.forecast_ledger and args.forecast_ledger.is_file():
        from .market_run import read_frozen_forecasts
        forecasts=read_frozen_forecasts(args.forecast_ledger,args.root)
    with sqlite3.connect(args.db) as con:
        con.row_factory=sqlite3.Row
        report=build_alt_prop_research(
            con,date_eastern=args.date,odds_quotes=odds,forecasts=forecasts
        )
    args.output_json.parent.mkdir(parents=True,exist_ok=True)
    args.output_md.parent.mkdir(parents=True,exist_ok=True)
    args.output_json.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    args.output_md.write_text(render_markdown(report))
    print(json.dumps({
        "alt_prop_research":True,"status":report["status"],
        "games":report.get("games_reviewed",0),
        "watchlist_candidates":len(report["candidates"]),
        "priced_alt_legs":len(report["priced_alternate_legs"]),
        "priced_parlay_exists":report["same_book_parlay"] is not None,
        "missing":report["missing_requirements"],
    },sort_keys=True))


if __name__=="__main__":
    main()
