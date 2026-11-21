"""Publish human-readable GPT v2 daily Markdown to GitHub, with append-only JSONL.

Unlike Claude's existing daily reports, GPT v2 reports contain only the
independent experimental possession model's *own* outputs. No LLM invents
predictions, no bookmaker odds are guessed, and pre-tip model forecasts
are never overwritten with post-tip calculations.

Usage after data ingestion:
  python -m gpt_engine.v2.ingest --seasons 2020 2021 2022 2023 2024 2025 2026 2027 --output /tmp/gpt-v2-daily.sqlite
  python -m gpt_engine.v2.daily_publish --db /tmp/gpt-v2-daily.sqlite --date 2026-11-22 --n 1000
  python -m gpt_engine.v2.daily_publish --db /tmp/gpt-v2-daily.sqlite --n 1000
Without --date, the two most relevant Eastern calendar dates are reported.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sqlite3
from zoneinfo import ZoneInfo

import pandas as pd

from .contracts import iso, utc, display_tip
from .feature_ablation import load_teams
from .research import ROOT, REPORTS, VERSION, run_day
from .situational_streaks import (
    add_finished_game_context, matchup_record_asof,
    season_from_eastern_date
)

OUT=ROOT/"gpt_engine"/"v2"/"artifacts"
LEDGER=OUT/"forecast_log.jsonl"
NEW_YORK=ZoneInfo("America/New_York")
MODEL_NOTE=("Experimental GPT v2 possession simulator. Win probabilities and "
            "player-stat estimates are NOT yet calibrated against the NBA "
            "market or approved for betting.")

def _short_id(team_id:str)->str:
    return str(team_id).split(":")[-1]

def _valid_ledger_record(row:dict) -> None:
    required={"game_id","game_date_eastern","tip_utc","cutoff_utc",
              "model_version","prediction_id","file"}
    missing=required-set(row)
    if missing:raise ValueError("Ledger missing fields: "+str(sorted(missing)))
    if utc(row["cutoff_utc"])>=utc(row["tip_utc"]):
        raise ValueError("No after-tip forecast entries allowed")
    if row["model_version"]!=VERSION:
        raise ValueError("This v2 ledger must not mix model versions")

def read_ledger(path:Path=LEDGER)->list[dict]:
    if not path.exists():return []
    records=[]
    seen=set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():continue
        row=json.loads(line)
        _valid_ledger_record(row)
        key=(row["model_version"],row["game_id"])
        if key in seen:
            raise ValueError("Duplicate immutable daily prediction "+str(key))
        seen.add(key)
        records.append(row)
    return records

def _append_ledger(path:Path,old:list[dict],new:list[dict]):
    existing={(x["model_version"],x["game_id"]) for x in old}
    fresh=set()
    for x in new:
        _valid_ledger_record(x)
        key=(x["model_version"],x["game_id"])
        if key in existing or key in fresh:
            raise ValueError("Cannot replace an already issued forecast: "+str(key))
        fresh.add(key)
    if not new:return
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as f:
        for row in new:
            f.write(json.dumps(row,sort_keys=True,allow_nan=False)+"\n")

def _forecast_filename(day:str,game_id:str)->Path:
    return REPORTS/(day+"_"+game_id.replace(":","-")+".json")

def _load_saved_details(records:list[dict])->list[dict]:
    documents=[]
    for row in records:
        source=ROOT/row["file"]
        if not source.is_file():
            raise FileNotFoundError("Saved immutable forecast missing: "+str(source))
        doc=json.loads(source.read_text(encoding="utf-8"))
        if (doc["game_id"]!=row["game_id"] or
            doc["prediction_id"]!=row["prediction_id"] or
            doc["cutoff_utc"]!=row["cutoff_utc"]):
            raise ValueError("Forecast evidence disagrees with immutable ledger")
        if utc(doc["cutoff_utc"])>=utc(doc["tip_utc"]):
            raise ValueError("Saved forecast was created after tip")
        documents.append(doc)
    return documents

def _team_and_player_names(con:sqlite3.Connection)->tuple[dict,dict,dict]:
    teams={str(r["team_id"]):str(r["current_name"] or _short_id(r["team_id"]))
           for r in con.execute("SELECT team_id,current_name FROM teams")}
    players={str(r["player_id"]):str(r["canonical_name"] or
                  ("NBA ID "+_short_id(r["player_id"])))
             for r in con.execute("SELECT player_id,canonical_name FROM players")}
    # Real projected players are sourced from an actual prior team roster.
    latest={}
    query=("SELECT s.player_id,s.team_id,g.game_date_eastern,s.game_id "
           "FROM player_game_stats s JOIN games g USING(game_id) "
           "WHERE g.status='final' ORDER BY g.game_date_eastern,s.game_id")
    for r in con.execute(query):
        latest[str(r["player_id"])]=str(r["team_id"])
    return teams,players,latest

def _rest_asof(finished:pd.DataFrame,team_id:str,day:str,season:int):
    d=finished[
        (finished.team_id.astype(str)==_short_id(team_id))&
        (finished.season.astype(int)==season)&
        (finished.game_date.astype(str)<day)
    ].sort_values(["game_date","game_id"])
    if d.empty:return None
    prev=datetime.strptime(str(d.iloc[-1].game_date),"%Y-%m-%d").date()
    target=datetime.strptime(day,"%Y-%m-%d").date()
    return (target-prev).days-1

def _situation(finished:pd.DataFrame,team_id:str,day:str,
               season:int,venue:str)->str:
    rest=_rest_asof(finished,team_id,day,season)
    if rest is None:
        return "Rest not established from a prior current-season game"
    record=matchup_record_asof(
        finished,_short_id(team_id),day,season,venue,rest
    )
    wins=record["wins"]; losses=record["losses"]
    wording=(f"exactly {rest} full rest day"+("" if rest==1 else "s"))
    if rest>=3:
        wording=f"{rest} full rest days (historical comparison: 3+ days)"
    if record["sample"]==0:
        return f"{venue.title()}, {wording}: no matching games in three-season sample"
    sample_note="; small sample" if record["low_sample"] else ""
    return (f"{venue.title()}, {wording}: **{wins}–{losses}** "
            f"in {record['sample']} prior matching games "
            f"({100*wins/record['sample']:.1f}% raw; "
            f"{100*record['shrunk_win_rate']:.1f}% shrunk descriptive rate"
            f"{sample_note}). NOT a calibrated probability")

def _recent_form(finished:pd.DataFrame,team_id:str,day:str)->str:
    previous=finished[(finished.team_id.astype(str)==_short_id(team_id))&
                      (finished.game_date.astype(str)<day)].sort_values(
                          ["game_date","game_id"]).tail(5)
    if previous.empty:return "no prior results"
    won=int(previous.won.sum()); n=len(previous)
    return f"last {n}: {won}–{n-won}"

def _injuries(doc:dict,team_id:str,name_lookup:dict)->str:
    statuses=[]
    for item in doc.get("availability_reports",[]):
        pid=item["player_id"]
        if item["normalized_status"] not in (
            "out","doubtful","questionable","probable"
        ) and (item["normalized_status"]!="unknown" or
                 item["provider_status"]=="not_listed_in_injury_feed"):
            continue
        # Player-to-team identity for reports is from the game's prior roster,
        # not a latest all-time identity (trades are possible).
        if item.get("team_id") and item["team_id"]!=team_id:
            continue
        if not item.get("team_id"):
            continue
        name=name_lookup.get(pid,"NBA ID "+_short_id(pid))
        statuses.append(
            f"{name}: {item['normalized_status'].replace('_',' ')} "
            f"({item['provider_status']}, observed {item['report_utc']} UTC)")
    return "; ".join(statuses[:7]) if statuses else "No mapped material reports in captured snapshot; not proof everyone is available"

def _top_player_lines(stats:dict,team_id:str,player_names:dict,
                      player_team:dict,*,max_players:int=5)->list[list[str]]:
    rows=[]
    for pid,p in stats.items():
        if player_team.get(pid)!=team_id:
            continue
        if p.get("availability")=="out":
            continue
        mins=float(p["minutes"]["mean"])
        if mins<5:continue
        uncertain=p.get("availability") in ("unknown","questionable","doubtful")
        name=player_names.get(pid,"NBA ID "+_short_id(pid))+(" †" if uncertain else "")
        rows.append([
            name,
            f"{mins:.1f}",f'{float(p["pts"]["mean"]):.1f}',
            f'{float(p["reb"]["mean"]):.1f}',
            f'{float(p["ast"]["mean"]):.1f}',
            f'{float(p["fg3m"]["mean"]):.1f}',
            f'{float(p["tov"]["mean"]):.1f}',
        ])
    return sorted(rows,key=lambda r:-float(r[2]))[:max_players]

def render_report(day:str,docs:list[dict],*,team_names:dict[str,str],
                  player_names:dict[str,str],player_team:dict[str,str],
                  finished:pd.DataFrame|None,
                  generated_at_utc:str,skip_count:int=0,n_scheduled:int=0)->str:
    lines=[
        f"# GPT v2 NBA daily simulation report — {day} (US Eastern)",
        "",
        "**Status:** RESEARCH / UNCALIBRATED — separate from Claude's engine.",
        f"**Report generated:** {generated_at_utc} UTC",
        f"**Model:** {VERSION} | **Schedule:** {n_scheduled} games, "
        f"**first-issue forecasts:** {len(docs)}; {skip_count} not forecast "
        "(already tipped, insufficient history, or otherwise ineligible).",
        "",
        MODEL_NOTE,
        "A forecast is logged once, before tip-off. Daily reruns never "
        "replace that prediction or silently use a newer injury report.",
        "",
        "## Slate at a glance",
        "",
        "| Matchup (away @ home) | Projected score (away–home) | "
        "Simulated winner | Expected total |",
        "|---|---|---|---:|"
    ]
    sorted_docs=sorted(docs,key=lambda d:(d["tip_utc"],d["game_id"]))
    for doc in sorted_docs:
        home=doc["home_team_id"];away=doc["away_team_id"]
        a=team_names.get(away,_short_id(away));h=team_names.get(home,_short_id(home))
        sim=doc["result"]
        prob=float(sim["home_win_probability"])
        winner=h if prob>=0.5 else a
        pickp=max(prob,1-prob)
        lines.append(f'| {a} @ {h} | {round(float(sim["expected_away_score"]))}–'
                     f'{round(float(sim["expected_home_score"]))} | '
                     f'**{winner} {pickp:.1%}** | {float(sim["total"]["mean"]):.1f} |')
    if not sorted_docs:
        lines.append("| No valid pre-tip GPT v2 forecasts recorded | — | — | — |")
    lines+=["","## Game-by-game breakdown","",
            "Situational streaks and player-stat tables are included only "
            "when a valid pre-tip forecast exists; none is invented for "
            "games already underway or without sufficient evidence.",
            ""]
    if finished is None:
        finished=pd.DataFrame()
    for doc in sorted_docs:
        home=doc["home_team_id"];away=doc["away_team_id"]
        a=team_names.get(away,_short_id(away));h=team_names.get(home,_short_id(home))
        sim=doc["result"]
        prob=float(sim["home_win_probability"])
        winner=h if prob>=0.5 else a
        season=season_from_eastern_date(day)
        lines+=[
            f"### {a} @ {h}",
            "",
            f"**Projected score:** {a} {float(sim['expected_away_score']):.1f} — "
            f"{h} {float(sim['expected_home_score']):.1f} "
            f"({winner} {max(prob,1-prob):.1%} simulated win probability)",
            "",
            f"- **Tip-off (Philippines):** {display_tip(doc['tip_utc'])}",
            f"- **Pregame information cutoff:** {doc['cutoff_utc']} UTC",
            f"- **Monte Carlo:** {int(sim['simulation_count']):,} simulations; "
            f"seed {sim['seed']}; win sampling SE "
            f"±{100*float(sim['mc_sampling_error']['home_win_probability']):.2f} percentage points",
            f"- **Expected total:** {float(sim['total']['mean']):.1f} points; "
            f"central 80% interval {sim['total']['interval_80'][0]:.0f}–"
            f"{sim['total']['interval_80'][1]:.0f}",
            f"- **Expected home margin:** {float(sim['margin']['mean']):+.1f}; "
            f"80% interval {sim['margin']['interval_80'][0]:+.0f} to "
            f"{sim['margin']['interval_80'][1]:+.0f}",
            f"- **Overtime chance:** {100*float(sim['overtime_probability']):.1f}%",
            "",
            "**Current situational streaks (context, not predictive adjustments):**",
            "",
        ]
        if finished.empty:
            lines+=["- Historical streak source unavailable for this run.", ""]
        else:
            lines+=[
                f"- **{a}** ({_recent_form(finished,away,day)}): "
                +_situation(finished,away,day,season,"away"),
                f"- **{h}** ({_recent_form(finished,home,day)}): "
                +_situation(finished,home,day,season,"home"),
                "",
            ]
        lines+=["**Source-observed player availability:**",""]
        for team_id,code in ((away,a),(home,h)):
            lines.append(f"- **{code}:** "+_injuries(doc,team_id,player_names))
        lines+=["","**Projected player box-score means (conditional on playing):**",
                "",
                "| Player | Min | PTS | REB | AST | 3PM | TOV |",
                "|---|---:|---:|---:|---:|---:|---:|"]
        for team_id,code in ((away,a),(home,h)):
            rows=_top_player_lines(sim["player_statistics"],team_id,
                                   player_names,player_team)
            if not rows:
                lines.append(f"| {code}: insufficient mapped player history | — | — | — | — | — | — |")
            else:
                lines.extend("| "+" | ".join(row)+" |" for row in rows)
        lines+=["",
                "† Unconfirmed playing time; treat this as a **conditional** projection, "
                "not a confident player prop.",
                "",
                f"**Data quality:** {', '.join(doc.get('quality_flags',[])[:12]) or 'not supplied'}",
                "",
                "**Interpretation:** Rest/venue records are historical descriptions. "
                "An impressive record (such as 18–2) does **not** establish "
                "an 90% future win probability, and it does not modify this "
                "game's simulated win percentage.",
                "",
                "---",""]
    lines+=["## Reproducibility and known limitations","",
            "- Model projections come from the GPT v2 Python possession simulator, "
            "not from an LLM-generated estimate or Claude's forecasts.",
            "- Roster candidates are prior participants, not verified starting lineups.",
            "- Injury data comes from timestamped ESPN observations when fresh; "
            "unlisted and unknown statuses are not proof of availability.",
            "- Player-stat means and win probabilities are experimental and uncalibrated.",
            "- Situation records exclude the current game and future dates. "
            "Three-season history may cover different rosters and coaches.",
            "- This Markdown is a human-readable view of per-game JSON and "
            "an immutable forecast ledger; it is **not** a sportsbook betting recommendation.",
            ""]
    return "\n".join(lines)

def publish(db_path:str,dates:list[str],*,simulations:int=1000,
            seed:int=20261121,ledger:Path=LEDGER,
            report_folder:Path=REPORTS)->dict:
    if simulations<50:raise ValueError("At least 50 simulations per game")
    saved=read_ledger(ledger)
    con=sqlite3.connect(db_path)
    con.row_factory=sqlite3.Row
    names,players,player_team=_team_and_player_names(con)
    timestamp=iso(datetime.now(timezone.utc))
    existing={(x["model_version"],x["game_id"]) for x in saved}
    reports=[]
    # Use final historical source records as-of each target date strictly
    # for descriptive venue/rest patterns; NEVER same-day final game data.
    earliest=min(dates)
    season=season_from_eastern_date(earliest)
    years=list(range(max(2020,season-3),season+1))
    finished=add_finished_game_context(load_teams(years))
    for day in dates:
        schedule=con.execute(
            "SELECT game_id,tip_utc,status FROM games WHERE game_date_eastern=? "
            "AND game_type='regular_season' ORDER BY tip_utc",
            (day,)
        ).fetchall()
        before=len([x for x in saved if x["game_date_eastern"]==day])
        added=run_day(db_path,day,n=simulations,seed=seed,
                      skip_game_ids={gid for model,gid in existing if model==VERSION})
        additions=[]
        for item in added:
            file=_forecast_filename(day,item["game_id"])
            doc=json.loads(file.read_text(encoding="utf-8"))
            # Source report is the immutable source of this row, and may
            # never be post-tip or have a mismatched recorded model.
            ledger_row={
                "game_id":item["game_id"],
                "game_date_eastern":day,
                "tip_utc":doc["tip_utc"],
                "cutoff_utc":doc["cutoff_utc"],
                "model_version":doc["model_version"],
                "prediction_id":doc["prediction_id"],
                "file":str(file.relative_to(ROOT)),
                "simulation_count":int(doc["result"]["simulation_count"]),
            }
            _valid_ledger_record(ledger_row)
            if (ledger_row["model_version"],ledger_row["game_id"]) in existing:
                raise ValueError("Same game newly calculated after already logged")
            additions.append(ledger_row)
            existing.add((ledger_row["model_version"],ledger_row["game_id"]))
        _append_ledger(ledger,saved,additions)
        saved.extend(additions)
        day_rows=[x for x in saved if x["game_date_eastern"]==day]
        docs=_load_saved_details(day_rows)
        skipped=max(0,len(schedule)-len(docs))
        markdown=render_report(
            day,docs,team_names=names,player_names=players,
            player_team=player_team,finished=finished,
            generated_at_utc=timestamp,skip_count=skipped,
            n_scheduled=len(schedule))
        report_folder.mkdir(parents=True,exist_ok=True)
        target=report_folder/f"daily_{day}.md"
        # The view may be regenerated, but the forecast and its original
        # source cutoff JSON are never updated.
        target.write_text(markdown,encoding="utf-8")
        reports.append({
            "date_eastern":day,"report":str(target.relative_to(ROOT)),
            "forecasted_games":len(docs),"new_predictions":len(additions),
            "scheduled_games":len(schedule),"already_logged_before":before,
            "skipped_or_unavailable_games":skipped
        })
    con.close()
    return {"model_version":VERSION,"research_only":True,
            "generated_utc":timestamp,"days":reports}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--db",required=True)
    p.add_argument("--date",default="")
    p.add_argument("--n",type=int,default=1000)
    p.add_argument("--seed",type=int,default=20261121)
    args=p.parse_args(argv)
    if args.date:
        # Explicit CLI dates remain US Eastern (never local Manila date).
        dates=[datetime.strptime(args.date,"%Y-%m-%d").date().isoformat()]
    else:
        today=datetime.now(NEW_YORK).date()
        dates=[(today+timedelta(days=i)).isoformat() for i in (0,1)]
    print(json.dumps(publish(args.db,dates,simulations=args.n,seed=args.seed),
                     indent=2),flush=True)

if __name__=="__main__":
    main()
