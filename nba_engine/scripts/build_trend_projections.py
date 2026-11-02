"""Walk-forward projections for every regular-season game 2023-2026, used by the trend finder.

For each game the projection is made from state that has seen ONLY earlier games (chronological pass, game_id
order), then the result is ingested. Season 2022 is warm-up only (no projections). Elo and the possession
simulator are the same classes the live engine uses.

Stored per game: raw simulator mean home/away points, calibrated-spread win probability, Elo win probability and
expected margin. The online league-scoring-level correction (level_delta) is applied afterwards by
trends.add_level_correction(), because it only depends on earlier results.

Usage: python scripts/build_trend_projections.py <season> [n_sims]   (run once per season; seasons are independent
workers, each advancing state through earlier seasons without simulating).
"""
import json, os, sys, time
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from nbaengine.elo import Elo, EloParams
from nbaengine.sim import TeamProfiles, ProfileParams, simulate_game, apply_dispersion, summarize

FILES = {2022: "games_cdn_2022.csv", 2023: "games_cdn_2023.csv", 2024: "games_cdn_2024.csv",
         2025: "games_cdn_2025.csv", 2026: "games_cdn_2026.csv"}
KAPPA_M, KAPPA_T = 0.7839391839831196, 0.9209561875321809      # fitted once on the 2023 season (stored in nba_engine.sqlite)
SEED0 = 20261017


def main(season: int, n_sims: int):
    ep = json.load(open(os.path.join(ROOT, "artifacts/elo_params.json")))["params"]
    elo, prof = Elo(EloParams(**ep)), TeamProfiles(ProfileParams())
    rows, t0 = [], time.time()
    for s in sorted(FILES):
        if s > season:
            break
        g = pd.read_csv(os.path.join(ROOT, "data/processed", FILES[s])).sort_values("game_id")
        for i, gd in enumerate(g.to_dict("records")):
            h, a, gid = gd["home"], gd["away"], int(gd["game_id"])
            elo.new_season(s); prof.new_season(s)
            pred_poss = prof.expected_poss(h, a)
            if s == season and s > 2022:
                e = elo.predict(h, a)
                sim = simulate_game(prof, h, a, n_sims, SEED0 + gid, 0.0)
                raw = summarize(sim)
                cal = summarize(apply_dispersion(sim, KAPPA_M, KAPPA_T, 0.0))
                rows.append({"season": s, "game_id": gid, "date": gd["date"], "home": h, "away": a,
                             "home_pts": gd["home_pts"], "away_pts": gd["away_pts"], "n_periods": gd["n_periods"],
                             "sim_home": raw["mean_home"], "sim_away": raw["mean_away"],
                             "sim_p_home": cal["p_home"], "elo_p_home": e["p_home"], "elo_margin": e["exp_margin"]})
                if len(rows) % 300 == 0:
                    print(season, len(rows), f"{time.time() - t0:.0f}s", flush=True)
            elo.update(h, a, gd["home_pts"], gd["away_pts"])
            prof.record_pace_residual(pred_poss, gd)
            prof.update(gd)
    out = os.path.join(ROOT, "data/processed", f"trend_proj_{season}.csv")
    pd.DataFrame(rows).to_csv(out, index=False)
    print("wrote", out, len(rows), f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 1000)
