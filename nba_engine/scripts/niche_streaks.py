"""Active niche streaks for a slate of upcoming games -> artifacts/reports/niche_streaks_<date>.md.
For each team: situations that describe TODAY's game, the team's record in that situation since 2023 and the run it is on.
Usage: python scripts/niche_streaks.py [YYYY-MM-DD]   (default: latest date that has forecasts but no results)
Also called (best effort) by daily_update.py."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import numpy as np, pandas as pd
from nbaengine import trends as T

PHRASE = {"win": ("has won {k} straight", "has lost {k} straight"),
          "beat_margin": ("has beaten the model's margin {k} straight", "has fallen short of the model's margin {k} straight"),
          "over_total": ("has seen the game total go over the projection {k} straight", "has seen the game total stay under the projection {k} straight"),
          "over_team": ("has scored over its projection {k} straight", "has scored under its projection {k} straight")}


def latest_open_date(db):
    import sqlite3, json
    con = sqlite3.connect(db)
    f = pd.read_sql_query("SELECT season, game_id, details_json FROM forecasts WHERE model_name='sim_mc'", con)
    done = set(map(tuple, pd.read_sql_query("SELECT season, game_id FROM results", con).values))
    con.close()
    d = [json.loads(x).get("date") for x, k in zip(f.details_json, zip(f.season, f.game_id)) if k not in done]
    return max(d) if d else None


def build(db, date, out_path=None, per_team=3, min_run=6):
    up = T.upcoming_extra(db, date)
    if up.empty:
        return None
    p = T.load_projected(extra=pd.concat([T.live_extra(db), up], ignore_index=True))
    t = T.team_games(p, T.load_warmup_games()); L = T.add_labels(t)
    gids = up.game_id.tolist()
    df = T.niche_streaks(t, L, gids, min_run=min_run)
    luck = T.luck_counts(t, L, gids, min_run=min_run, worlds=6)
    lines = [f"# Active niche streaks for {date}", "",
             "Each line is a situation that describes tonight's game for that team, the team's record in the same situation since the "
             "2022-23 season (projection-based angles start in 2023), and the run it is currently on (most recent matching games). "
             "'Chance' is how likely that run was under the model's own expectations; smaller = more unusual.", "",
             f"**Reality check:** {luck['real']} unusual runs (6+ in a row) exist for tonight's games. A luck-only world, where results are redrawn from "
             f"the model's probabilities, produces about {luck['luck_only_avg']:.0f} (max {luck['luck_only_max']} in {luck['worlds']} worlds). "
             "So most of these are what chance produces when thousands of situations are scanned. In the 2023-24 vs 2025-26 test, "
             "team-specific niche trends did not carry over to later seasons. Treat these as descriptions of recent history, not predictions.", ""]
    for g in up.itertuples():
        lines.append(f"## {g.away} at {g.home}")
        for tm in (g.away, g.home):
            d = df[(df.team == tm) & (df.game_id == g.game_id)]
            if d.empty:
                lines.append(f"- **{tm}**: no active run of {min_run}+ in a matching situation."); continue
            # best (most unusual) per outcome, at most per_team lines, favour win / margin streaks first
            pick = d.sort_values(["model_chance_of_run"]).groupby("outcome").head(1)
            pick = pick.sort_values("model_chance_of_run").head(per_team)
            for r in pick.itertuples():
                k, run = abs(r.run), r.run
                verb = PHRASE[r.outcome][0 if run > 0 else 1].format(k=k)
                lines.append(f"- **{tm}**: {verb} when {r.situation.replace('&', 'and')} "
                             f"({r.hits}-{r.n - r.hits} in {r.n} such games; chance of run {r.model_chance_of_run:.3%}).")
        lines.append("")
    text = "\n".join(lines)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        open(out_path, "w").write(text)
    return text


if __name__ == "__main__":
    db = os.path.join(ROOT, "artifacts/live.sqlite")
    date = sys.argv[1] if len(sys.argv) > 1 else latest_open_date(db)
    print(build(db, date, os.path.join(ROOT, f"artifacts/reports/niche_streaks_{date}.md"))[:3000])
