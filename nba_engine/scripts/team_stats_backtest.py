"""Walk-forward check of the simulator's TEAM STAT predictions (not just points): FG%, 3PA, 3PM, FTA, TOV, OREB, pace, for two
profile variants. Each game is predicted from state that has only seen earlier games, then ingested.
Usage: python scripts/team_stats_backtest.py <season> [n_sims] [limit]   -> data/processed/team_stats_bt_<season>.csv
Variants: base = current matchup rule; def = defence also moves the 3-point attempt rate and free-throw rate."""
import os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
import numpy as np, pandas as pd
from nbaengine.sim import TeamProfiles, ProfileParams, simulate_game

FILES = {s: f"games_cdn_{s}.csv" for s in (2022, 2023, 2024, 2025, 2026)}
KEYS = ("fga", "fgm", "fg3a", "fg3m", "fta", "ftm", "tov", "oreb")
VARIANTS = {"base": ProfileParams(), "s3": ProfileParams(def_effect=("s3",)),
            "lg400": ProfileParams(def_effect=("s3",), league_half_life_games=400.0),
            "lg700": ProfileParams(def_effect=("s3",), league_half_life_games=700.0)}
if os.environ.get("VSET") == "hl":        # recency of the team profiles
    VARIANTS = {"s3": ProfileParams(def_effect=("s3",)), "hl25": ProfileParams(def_effect=("s3",), half_life_games=25.0),
                "hl60": ProfileParams(def_effect=("s3",), half_life_games=60.0), "hl90": ProfileParams(def_effect=("s3",), half_life_games=90.0)}
if os.environ.get("VSET") == "hl2":
    VARIANTS = {"hl12": ProfileParams(def_effect=("s3",), half_life_games=12.0), "hl18": ProfileParams(def_effect=("s3",), half_life_games=18.0),
                "hl25r": ProfileParams(def_effect=("s3",), half_life_games=25.0, season_rollover=0.4),
                "hl25q": ProfileParams(def_effect=("s3",), half_life_games=25.0, season_rollover=0.8)}
SUFFIX = {"hl": "_hl", "hl2": "_hl2"}.get(os.environ.get("VSET"), "")


def main(season, n_sims=200, limit=None):
    prof = {k: TeamProfiles(v) for k, v in VARIANTS.items()}
    rows, t0 = [], time.time()
    for s in sorted(FILES):
        if s > season:
            break
        g = pd.read_csv(os.path.join(ROOT, "data/processed", FILES[s])).sort_values("game_id")
        for gd in g.to_dict("records"):
            gid = int(gd["game_id"])
            for p in prof.values():
                p.new_season(s)
            if s == season and (limit is None or len(rows) < limit):
                rec = {"season": s, "game_id": gid, "date": gd["date"], "home": gd["home"], "away": gd["away"], "n_periods": gd["n_periods"]}
                for name, p in prof.items():
                    sim = simulate_game(p, gd["home"], gd["away"], n_sims, 20261017 + gid, 0.0, track=True)
                    rec[f"{name}_poss"] = float(sim["n_poss"].mean())
                    for side in ("home", "away"):
                        box = sim["box_" + side]
                        for k in KEYS:
                            rec[f"{name}_{side}_{k}"] = float(box[k].mean())
                        rec[f"{name}_{side}_pts_reg"] = float(2 * (box["fgm"] - box["fg3m"]).mean() + 3 * box["fg3m"].mean() + box["ftm"].mean())
                rows.append(rec)
                if len(rows) % 200 == 0:
                    print(season, len(rows), f"{time.time() - t0:.0f}s", flush=True)
            for p in prof.values():
                pp = p.expected_poss(gd["home"], gd["away"])
                p.record_pace_residual(pp, gd); p.update(gd)
    out = os.path.join(ROOT, "data/processed", f"team_stats_bt_{season}{SUFFIX}.csv")
    pd.DataFrame(rows).to_csv(out, index=False)
    print("wrote", out, len(rows), f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 200, int(sys.argv[3]) if len(sys.argv) > 3 else None)
