"""Stage-wise tuning of the player model on warm-up (2022-23) + calibration (2024-25) seasons ONLY (labels <= 2025)."""
import json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
from dataclasses import replace
from nbaengine.players import PlayerParams
from nbaengine.players_backtest import load_logs, run_pass, MinutesCollector, RateCollector

L = load_logs([2022, 2023, 2024, 2025])        # NOTE: 2026 (evaluation season) is not loaded here
CAL = 2024                                      # first calibration label; 2022-23 are warm-up
out = {}
t0 = time.time()
print("stage 1: minutes half-life, cap")
best = None
for hl in (6, 12, 24):
    mc = MinutesCollector(caps=(36, 38, 40, 42, 48))
    run_pass(L, PlayerParams(hl_min=hl), CAL, mc)
    r = mc.result(); out[f"minutes_hl{hl}"] = r
    print(f"  hl_min={hl}: " + ", ".join(f"{k}={v:.3f}" for k, v in r.items()), f"({time.time()-t0:.0f}s)")
    key = min(v for k, v in r.items() if k.startswith("cap"))
    if best is None or key < best[0]:
        best = (key, hl, min((k for k in r if k.startswith("cap")), key=lambda k: r[k]))
hl_min, cap = best[1], float(best[2][3:])
print("  chosen hl_min", hl_min, "cap", cap)

print("stage 2: rate half-life and shrinkage")
bestr = None
for hl_rate in (20, 40, 80):
    for k_min in (75, 150, 300):
        rc = RateCollector()
        run_pass(L, PlayerParams(hl_min=hl_min, hl_rate=hl_rate, k_min=k_min), CAL, rc)
        r = rc.result(); out[f"rate_hl{hl_rate}_k{k_min}"] = r
        print(f"  hl_rate={hl_rate} k_min={k_min}: dev_total {r['dev_total']:.4f} pts_mae {r['pts_mae_given_minutes']:.3f} (last10 per-min baseline {r['pts_mae_last10_per_min']:.3f}) ({time.time()-t0:.0f}s)")
        if bestr is None or r["dev_total"] < bestr[0]:
            bestr = (r["dev_total"], hl_rate, k_min)
out["chosen"] = {"hl_min": hl_min, "cap": cap, "hl_rate": bestr[1], "k_min": bestr[2]}
json.dump(out, open("artifacts/player_tuning.json", "w"), indent=2)
print("chosen", out["chosen"])
