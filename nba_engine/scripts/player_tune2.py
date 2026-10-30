"""Second tuning round: the first round chose grid-edge values, so extend the grid (still labels <= 2025 only)."""
import json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
from nbaengine.players import PlayerParams
from nbaengine.players_backtest import load_logs, run_pass, MinutesCollector, RateCollector
L = load_logs([2022, 2023, 2024, 2025]); CAL = 2024
out = json.load(open("artifacts/player_tuning.json")); t0 = time.time()
best = (4.772, 6, 36.0)
for hl in (3, 4):
    mc = MinutesCollector(caps=(30, 32, 34, 36, 38))
    run_pass(L, PlayerParams(hl_min=hl), CAL, mc); r = mc.result(); out[f"minutes_hl{hl}"] = r
    print(f"hl_min={hl}: " + ", ".join(f"{k}={v:.3f}" for k, v in r.items()), f"({time.time()-t0:.0f}s)", flush=True)
    for k, v in r.items():
        if k.startswith("cap") and v < best[0]:
            best = (v, hl, float(k[3:]))
print("minutes best", best, flush=True)
bestr = (8.1428, 20, 75)
for hl_rate, k_min in ((10, 75), (20, 40), (10, 40), (30, 75)):
    rc = RateCollector(); run_pass(L, PlayerParams(hl_min=best[1], hl_rate=hl_rate, k_min=k_min), CAL, rc)
    r = rc.result(); out[f"rate_hl{hl_rate}_k{k_min}"] = r
    print(f"hl_rate={hl_rate} k_min={k_min}: dev_total {r['dev_total']:.4f} pts_mae {r['pts_mae_given_minutes']:.3f} ({time.time()-t0:.0f}s)", flush=True)
    if r["dev_total"] < bestr[0]:
        bestr = (r["dev_total"], hl_rate, k_min)
out["chosen"] = {"hl_min": best[1], "cap": best[2], "hl_rate": bestr[1], "k_min": bestr[2]}
json.dump(out, open("artifacts/player_tuning.json", "w"), indent=2)
print("chosen", out["chosen"], flush=True)
