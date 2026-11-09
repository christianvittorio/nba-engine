"""Add market ladders (P over x.5 for every stat incl. 2PM/2PA and combos) to ALREADY STORED player forecasts, without changing them.
For each stored game: load the player state as committed by the daily run that made the forecast (git history), rebuild the projection for exactly the
players that were stored, with the same seed, then CHECK the rebuilt means against the stored ones. Exact reproduction is impossible (the original pool had more than the 12 stored players, which changes the
team-points reconciliation, and the random draws differ), so a game is augmented when the rebuilt mean points per player agree with the stored ones to
within 0.8 on average, and the ladder is tagged "ladder_src" = re-simulated from the state commit. Ladders use 4,000 draws. player_fc (immutable) is never touched: ladders go to the separate table player_ladder.
Usage: python scripts/player_ladder_backfill.py [YYYY-MM-DD ...]   (default: every date with player forecasts)"""
import os, sys, json, sqlite3, subprocess, tempfile
from datetime import datetime, timezone
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from nbaengine.players import PlayerModel, sample_players
from nbaengine.player_live import _ladders, KEEP
import pandas as pd
REPO = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=ROOT, text=True).strip()
REL = os.path.relpath(f"{ROOT}/artifacts/player_state.json", REPO)
live = sqlite3.connect(f"{ROOT}/artifacts/live.sqlite"); pl = sqlite3.connect(f"{ROOT}/artifacts/player_live.sqlite")
commits = [l.split(" ", 1) for l in subprocess.check_output(["git", "log", "--format=%H %cI", "--", REL], cwd=REPO, text=True).splitlines()]
commits = sorted(((datetime.fromisoformat(t), h) for h, t in commits))          # oldest first
_cache = {}
def model_at(made_at: str):
    t = datetime.strptime(made_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    h = next((h for ct, h in commits if ct >= t), commits[-1][1])               # the commit written by the run that made this forecast
    if h not in _cache:
        f = tempfile.NamedTemporaryFile(suffix=".json", delete=False); f.write(subprocess.check_output(["git", "show", f"{h}:{REL}"], cwd=REPO)); f.close()
        _cache[h] = PlayerModel.load(f.name)
    return _cache[h], h
pl.execute("CREATE TABLE IF NOT EXISTS player_ladder(game_id INTEGER, player_id INTEGER, team TEXT, src TEXT, ladder_json TEXT, PRIMARY KEY(game_id, player_id))")
dates = sys.argv[1:] or [r[0] for r in live.execute("select distinct date from game_dates order by date")]
done = skipped = 0
for day in dates:
    for gid, in live.execute("select game_id from game_dates where date=?", (day,)).fetchall():
        rows = pl.execute("select team,player_id,made_at_utc,details_json from player_fc where game_id=?", (gid,)).fetchall()
        if not rows or all("ov" in (json.loads(r[3]).get("pts") or {}) for r in rows) or pl.execute("select 1 from player_ladder where game_id=? limit 1", (gid,)).fetchone(): continue
        sm = live.execute("select details_json, mean_home, mean_away from forecasts where game_id=? and model_name='sim_mc'", (gid,)).fetchone()
        d = json.loads(sm[0]); h, a = d["home"], d["away"]
        pm, commit = model_at(rows[0][2]); ok, upd, diffs = True, [], []
        for ti, team in enumerate((h, a)):
            mine = [r for r in rows if r[0] == team]
            if not mine: continue
            pr = pm.project_team(team, mode="unconfirmed", pool_ids=[r[1] for r in mine], team_pts={h: sm[1], a: sm[2]}[team], opp_team=(a if team == h else h))
            pr = pr.sort_values("base_min", ascending=False).head(12).reset_index(drop=True)
            lad = _ladders(sample_players(pr, pm.p, 4000, 20261021 + gid * 100 + ti, "unconfirmed"))
            stored = {r[1]: json.loads(r[3]) for r in mine}
            for pid, L in zip(pr.player_id, lad):
                s_ = stored.get(int(pid))
                if s_ is None: ok = False; break
                diffs.append(abs(L["pts"]["m"] - s_["pts"]["m"]))
                upd.append((int(pid), team, L, s_))
        ok = ok and bool(diffs) and sum(diffs) / len(diffs) < 0.8
        if not ok or not upd:
            skipped += 1; print("skip", gid, day, "(rebuild does not reproduce the stored forecast)"); continue
        for pid, team, L, s_ in upd:
            pl.execute("INSERT OR REPLACE INTO player_ladder VALUES(?,?,?,?,?)", (gid, pid, team, f"re-simulated from state {commit[:7]}, 4000 draws", json.dumps(L)))
        pl.commit(); done += 1
print("augmented", done, "games; skipped", skipped)
