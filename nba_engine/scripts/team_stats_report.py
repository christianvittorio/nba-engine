"""Team box-score / advanced-stat report for the live season: per-team table plus how well the simulator predicted each team stat.
Usage: python scripts/team_stats_report.py [db] [out.md]"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
import pandas as pd
from nbaengine.teamstats import load_box, advanced_table, predicted_vs_actual, accuracy_table


def build(db=None, out=None):
    db = db or os.path.join(ROOT, "artifacts/live.sqlite"); out = out or os.path.join(ROOT, "artifacts/reports/team_stats.md")
    box = load_box(db)
    if box.empty:
        open(out, "w").write("# Team stats\n\nNo team box scores stored yet (they are saved as games are ingested).\n"); return
    cur = box[box.season == box.season.max()]
    T = advanced_table(cur).round(3).reset_index()
    md = lambda d: "\n".join(["| " + " | ".join(map(str, d.columns)) + " |", "|" + "---|" * len(d.columns)] + ["| " + " | ".join(map(str, r)) + " |" for r in d.itertuples(index=False)])
    L = [f"# Team stats, {int(cur.season.max()) - 1}-{str(int(cur.season.max()))[2:]} season: {cur.game_id.nunique()} games", "",
         "Ratings are per 100 possessions (possessions = FGA - OREB + TOV + 0.44 FTA). 'opp' columns are what the team allows. ORB% is the share of available offensive rebounds, DRB% of defensive ones.", "",
         md(T), ""]
    M = predicted_vs_actual(db)
    if len(M):
        A = accuracy_table(M).round(3)
        L += ["## How well the simulator predicted team stats", "",
              f"{M.game_id.nunique()} regulation games whose forecast stored a predicted box score (predicted before tip-off, never edited).", "", md(A), ""]
    open(out, "w").write("\n".join(L)); print("wrote", out)


if __name__ == "__main__":
    build(*(sys.argv[1:3]))
