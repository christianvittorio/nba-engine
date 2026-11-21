"""Nov 20 2026 9-game spoiler-free research report with original pretip injuries."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from .contracts import iso
from .replay import historical_source_csv
from .replay_injuries import replay_with_claude_injury
from .daily_publish import render_report
from .shared_availability import normalize_status
from .situational_streaks import add_finished_game_context

DATE="2026-11-20"
CUTOFF="2026-11-20T22:00:00Z"

def generate(source_path,commit,n=1000):
    source=json.loads(Path(source_path).read_text(encoding="utf-8"))
    if len(source.get("teams",{}))!=30 or source.get("problems"):
        raise ValueError("Archived ESPN source incomplete")
    if iso(source["generated_utc"])>=CUTOFF:
        raise ValueError("Post-cutoff injury capture prohibited")
    replay=replay_with_claude_injury(
        DATE,CUTOFF,source_path,commit,simulations=n,seed=20261120,
        include_player_statistics=True)
    if replay["game_count"]!=9:
        raise ValueError("Expected nine regular-season games")
    teams={};names={};player_team={};docs=[];audit=[]
    for game in replay["games"]:
        for side in ("home","away"):
            team_id="team:nba:"+game[side+"_team_id"]
            code=game[side]
            teams[team_id]=code
            for p in source["teams"][code].get("roster",[]):
                pid=p.get("nba_id")
                if pid and int(pid)>0:
                    key="player:nba:"+str(pid)
                    player_team[key]=team_id
                    names[key]=str(p.get("name") or "NBA ID "+str(pid))
        sim=game["asof_claude_injury"]
        stats={}
        for pid,s in game["injury_adjusted_player_stats"].items():
            key="player:nba:"+str(pid)
            stats[key]={k:{"mean":s[k]} for k in
                        ("minutes","pts","reb","ast","fg3m","tov")}
            stats[key]["availability"]=s["availability"]
            stats[key]["sample_games"]=s["sample_games"]
        injuries=[]
        for side in ("home","away"):
            team_id="team:nba:"+game[side+"_team_id"]
            for inj in source["teams"][game[side]].get("injuries",[]):
                pid=inj.get("nba_id")
                if not pid or int(pid)<=0:continue
                injuries.append({
                    "player_id":"player:nba:"+str(pid),
                    "team_id":team_id,
                    "provider_status":str(inj.get("status") or "unknown"),
                    "normalized_status":normalize_status(inj.get("status")),
                    "report_utc":source["generated_utc"],
                    "source_id":"espn_unofficial_shared_feed",
                })
        doc={
            "game_id":game["game_id"],"game_date_eastern":DATE,
            "home_team_id":"team:nba:"+game["home_team_id"],
            "away_team_id":"team:nba:"+game["away_team_id"],
            "tip_utc":game["tip_utc"],"cutoff_utc":CUTOFF,
            "model_version":game["model_version"],
            "quality_flags":["historical_reconstruction",
                            "genuine_pretip_espn_snapshot",
                            "uncalibrated_injury_minutes","unconfirmed_starters"],
            "availability_reports":injuries,
            "result":{
                "simulation_count":n,"seed":game["simulation_seed"],
                "home_win_probability":sim["home_win_probability"],
                "expected_home_score":sim["home_expected_score"],
                "expected_away_score":sim["away_expected_score"],
                "total":{"mean":sim["expected_total"],
                         "interval_80":sim["total_80pct_interval"]},
                "margin":{"mean":sim["expected_margin"],
                          "interval_80":sim["margin_80pct_interval"]},
                "overtime_probability":sim["overtime_probability"],
                "mc_sampling_error":{
                    "home_win_probability":sim["mc_win_probability_standard_error"]},
                "player_statistics":stats,
            },
        }
        docs.append(doc)
        audit.append({
            "matchup":game["away"]+" @ "+game["home"],
            "before_injuries":game["base_model"],
            "after_injuries":sim,
            "injury_labels_applied":game["injury_labels_applied"],
            "source_timestamp":game["source_capture_utc"]
        })
    history=historical_source_csv("teams",[2025,2026,2027])
    history=history[(history.game_date.astype(str)<DATE)&
                    (history.game_type.astype(str)=="regular_season")].copy()
    if not (history.game_date.astype(str)<DATE).all():
        raise AssertionError("Future stats leaked")
    finished=add_finished_game_context(history)
    markdown=render_report(
        DATE,docs,team_names=teams,player_names=names,player_team=player_team,
        finished=finished,generated_at_utc=CUTOFF,n_scheduled=9,skip_count=0)
    markdown=markdown.replace(
        "**Report generated:** "+CUTOFF+" UTC",
        "**Original source cutoff, not original publication time:** "+CUTOFF+" UTC\n"
        "**Retrospective reconstruction.** Original ESPN injuries were captured "
        "before tip-off. No actual November 20 game outcomes were used. "
        "All stats and streaks exclude November 20 games.")
    return markdown,{"date_eastern":DATE,"cutoff_utc":CUTOFF,
                     "source_generated_utc":source["generated_utc"],
                     "source_commit":commit,"games":audit,
                     "actual_scores_used":False,"simulation_count_each":n}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--source-commit",required=True)
    p.add_argument("--n",type=int,default=1000)
    p.add_argument("--output",required=True)
    p.add_argument("--audit",required=True)
    args=p.parse_args()
    md,audit=generate(args.source,args.source_commit,args.n)
    Path(args.output).write_text(md,encoding="utf-8")
    Path(args.audit).write_text(json.dumps(audit,indent=2,allow_nan=False)+"\n")
    print("PRETIP_9GAME_REPORT "+json.dumps({
        "date":DATE,"games":len(audit["games"]),
        "source":audit["source_generated_utc"],"md_lines":len(md.splitlines())}))
    print("PRETIP_MATCHUPS "+json.dumps(audit["games"],separators=(",",":")))

if __name__=="__main__":main()
