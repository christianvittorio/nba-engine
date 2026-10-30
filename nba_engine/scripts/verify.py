"""Verification: leakage, immutability, reproducibility, MC error, per-season stability, worked example."""
import json, os, sqlite3, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import numpy as np, pandas as pd
from nbaengine import MODEL_VERSION
from nbaengine.data import load_pbp_games
from nbaengine.elo import Elo, EloParams
from nbaengine.sim import TeamProfiles, simulate_game, apply_dispersion, summarize
from nbaengine.store import Store
from nbaengine.backtest import run_backtest, evaluate, metrics

out = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

games, _ = load_pbp_games("data/raw/pbp_extract", [2021, 2022, 2023, 2024], "data/processed")
ep = EloParams(**json.load(open("artifacts/elo_params.json"))["params"])

# 1. immutability
con = sqlite3.connect("artifacts/nba_engine.sqlite")
for stmt in ("UPDATE forecasts SET p_home=0.5 WHERE forecast_id=1", "DELETE FROM forecasts WHERE forecast_id=1"):
    try:
        con.execute(stmt); say("IMMUTABILITY FAIL:", stmt)
    except sqlite3.DatabaseError as e:
        say("immutability OK:", stmt.split()[0], "->", e)

# 2. leakage test: scramble the scores of every game after the first 150 evaluated games; forecasts for the first 150 must not change
def mini(g):
    db = "/tmp/claude-0/leak_%d.sqlite" % id(g)
    if os.path.exists(db): os.remove(db)
    st = Store(db)
    run_backtest(g, st, ep, [2022], 2023, [2024], n_sims=200, calib_sims=200, calib_stride=6, progress=lambda *_: None)
    return pd.read_sql_query("SELECT game_id, model_name, p_home, mean_total FROM forecasts WHERE season=2024 ORDER BY game_id, model_name", st.con)
ev_ids = games[games.season == 2024].game_id.iloc[:150].tolist()
a = mini(games)
g2 = games.copy()
fut = (g2.season == 2024) & (~g2.game_id.isin(ev_ids)) & (g2.game_id > max(ev_ids))
rng = np.random.default_rng(1)
g2.loc[fut, ["home_pts", "away_pts"]] = rng.permutation(g2.loc[fut, ["home_pts", "away_pts"]].values)
b = mini(g2)
ca = a[a.game_id.isin(ev_ids)].reset_index(drop=True); cb = b[b.game_id.isin(ev_ids)].reset_index(drop=True)
same = np.allclose(ca.p_home, cb.p_home) and np.allclose(ca.mean_total.fillna(0), cb.mean_total.fillna(0))
say("leakage test (future scores scrambled, first 150 forecasts x 4 models identical):", "PASS" if same else "FAIL",
    "| later forecasts did change:", not np.allclose(a[~a.game_id.isin(ev_ids)].p_home, b[~b.game_id.isin(ev_ids)].p_home))

# 3. per-season stability from stored forecasts
df = evaluate(Store("artifacts/nba_engine.sqlite"))
for s, d in df.groupby("season"):
    m = metrics(d)[["brier", "log_loss", "accuracy", "total_mae"]]
    say(f"\nseason label {s} (n={len(d)//4})"); say(m.round(4).to_string())
sim = df[df.model_name == "sim_mc"]
say(f"\nOT: mean simulated P(OT) {sim.p_ot.mean():.4f} vs actual OT rate {sim.ot.mean():.4f}")
say(f"home win rate in evaluated games {sim.y.mean():.4f}; mean actual margin {sim.margin.mean():.2f}; mean sim margin {sim.mean_margin.mean():.2f}")
say(f"mean actual total {sim.total.mean():.2f}; mean sim total {sim.mean_total.mean():.2f}")
# paired comparison sim vs elo on log loss
e = df[df.model_name == "elo"].set_index("game_id"); s_ = sim.set_index("game_id")
def ll(p, y): p = p.clip(1e-6, 1 - 1e-6); return -(y * np.log(p) + (1 - y) * np.log(1 - p))
diff = (ll(s_.p_home, s_.y) - ll(e.p_home.reindex(s_.index), s_.y))
say(f"paired log-loss difference sim - elo: mean {diff.mean():+.4f}, standard error {diff.std()/np.sqrt(len(diff)):.4f} (negative favours sim)")

# 4. worked example: forecast and evaluate the last completed game with 10,000 simulations
target = games[games.season == 2025].iloc[-1]
prof, elo = TeamProfiles(), Elo(ep)
for g in games.itertuples(index=False):
    gd = g._asdict()
    if gd["season"] == target.season and gd["game_id"] == target.game_id: break
    elo.new_season(gd["season"]); prof.new_season(gd["season"])
    elo.update(gd["home"], gd["away"], gd["home_pts"], gd["away_pts"])
    prof.record_pace_residual(prof.expected_poss(gd["home"], gd["away"]), gd); prof.update(gd)
prof.new_season(2025)
mv = json.loads(con.execute("SELECT params_json FROM model_versions WHERE model_name='sim_mc'").fetchone()[0])
ld = json.loads(con.execute("SELECT details_json FROM forecasts WHERE model_name='sim_mc' AND game_id=?", (int(target.game_id),)).fetchone()[0])["level_delta"]
seed = 20261017 + int(target.game_id)
raw = simulate_game(prof, target.home, target.away, 10000, seed, 0.0)
cal = apply_dispersion(raw, mv["kappa_margin"], mv["kappa_total"], ld)
S = summarize(cal, thresholds={"home 110+": ("home", ">=", 110), "total over 225.5": ("total", ">", 225.5), "home wins by 10+": ("margin", ">=", 10)})
rerun = summarize(apply_dispersion(simulate_game(prof, target.home, target.away, 10000, seed, 0.0), mv["kappa_margin"], mv["kappa_total"], ld))
say(f"\nWORKED EXAMPLE: {target.away} at {target.home}, game_id {int(target.game_id)} (season label {int(target.season)}), 10,000 sims")
say(f"  reproducible with same seed: {rerun['p_home'] == S['p_home'] and rerun['mean_total'] == S['mean_total']}")
say(f"  P(home win) {S['p_home']:.3f} (Monte Carlo SE {S['mc_se_p_home']:.4f}); Elo P(home) {elo.predict(target.home, target.away)['p_home']:.3f}")
say(f"  mean score {S['mean_home']:.1f}-{S['mean_away']:.1f}, median {S['median_home']:.0f}-{S['median_away']:.0f}, most frequent exact score {S['modal_score_home']}-{S['modal_score_away']} (only {S['modal_score_prob']:.1%} of sims)")
say(f"  margin 50% interval [{S['q_margin']['25']:.1f}, {S['q_margin']['75']:.1f}], 90% [{S['q_margin']['5']:.1f}, {S['q_margin']['95']:.1f}]; total 80% [{S['q_total']['10']:.1f}, {S['q_total']['90']:.1f}]")
say(f"  P(OT) {S['p_ot']:.3f}; thresholds {json.dumps({k: round(v, 3) for k, v in S['thresholds'].items()})}")
say(f"  ACTUAL: {int(target.home_pts)}-{int(target.away_pts)} (home margin {int(target.home_pts - target.away_pts):+d}, total {int(target.home_pts + target.away_pts)}); periods {int(target.n_periods)}")
st = con.execute("SELECT p_home, mean_home, mean_away, n_sims FROM forecasts WHERE model_name='sim_mc' AND game_id=?", (int(target.game_id),)).fetchone()
say(f"  stored backtest forecast for this game (2,000 sims): p_home {st[0]:.3f}, mean {st[1]:.1f}-{st[2]:.1f}")

# 5. Monte Carlo error vs simulation count (same game, 12 seeds each)
say("\nMonte Carlo sampling error of P(home win), same game, 12 different seeds:")
for n in (100, 1000, 10000):
    ps = [summarize(apply_dispersion(simulate_game(prof, target.home, target.away, n, 1000 + k, 0.0), mv["kappa_margin"], mv["kappa_total"], ld))["p_home"] for k in range(12)]
    say(f"  n_sims={n:>6}: spread (sd) across seeds {np.std(ps):.4f}, theoretical {np.sqrt(S['p_home']*(1-S['p_home'])/n):.4f}")
say("  (more simulations shrink sampling noise only; they do not improve the model's real-world accuracy)")
open("artifacts/verification.txt", "w").write("\n".join(out))
