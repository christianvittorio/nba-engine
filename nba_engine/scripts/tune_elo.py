"""Tune Elo hyper-parameters on 1996-2015 regular-season games (538 data only).
The 2021-25 evaluation seasons are never used here."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dataclasses import asdict
from nbaengine.data import load_538_games
from nbaengine.elo import EloParams, tune_elo

g = load_538_games("data/raw/nbaallelo.csv")
g = g[(g.playoffs == 0) & (g.season >= 1996) & (g.season <= 2015)].reset_index(drop=True)
grid = [EloParams(k=k, home_adv=h, carryover=c, mov_scale=1.0)
        for k in (15, 20, 25) for h in (70, 80, 90) for c in (0.5, 0.6, 0.7, 0.8)]
res = tune_elo(g, grid, burn_in_seasons=3)
best, ll = res[0]
print("best", best, "walk-forward log loss", round(ll, 5), "(scored 1999-2015)")
for p, l in res[:5]:
    print(" ", p.k, p.home_adv, p.carryover, round(l, 5))
json.dump({"params": asdict(best), "tuning_log_loss": ll, "tuned_on": "538 nbaallelo 1996-2015 regular season",
           "n_games": int(len(g))}, open("artifacts/elo_params.json", "w"), indent=2)
