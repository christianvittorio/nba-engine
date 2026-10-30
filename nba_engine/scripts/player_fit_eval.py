"""Fit remaining parameters on calibration seasons (2024-25 labels), then evaluate on 2025-26 (label 2026), never seen before."""
import json, os, sys, time
from dataclasses import asdict, replace
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import numpy as np, pandas as pd
from nbaengine import MODEL_VERSION
from nbaengine.players import PlayerParams
from nbaengine.players_store import PlayerStore
from nbaengine.players_backtest import (load_logs, run_pass, FitCollector, fit_params, fit_sigma_shoot, EvalCollector,
                                        load_player_forecasts, attach_actuals, player_metrics)

N_SIMS = int(os.environ.get("N_SIMS", 600))
DB = os.environ.get("PDB", "artifacts/player_backtest.sqlite")
ch = json.load(open("artifacts/player_tuning.json"))["chosen"]
print("tuned (calibration data only):", ch, flush=True)
base = PlayerParams(hl_min=ch["hl_min"], cap=ch["cap"], hl_rate=ch["hl_rate"], k_min=ch["k_min"])
L = load_logs([2022, 2023, 2024, 2025, 2026])
t0 = time.time()

fc = FitCollector()
model = run_pass(L[L.season <= 2025], base, 2024, fc)                       # state now = end of 2024-25
params, diag = fit_params(base, fc)
sig, sig_res = fit_sigma_shoot(params, pd.DataFrame(fc.conf))
params = replace(params, sigma_shoot=sig)
diag["sigma_shoot"], diag["sigma_search"] = sig, {str(k): v for k, v in sig_res.items()}
print("fitted on", diag["conf_rows"], "calibration player-games", f"({time.time()-t0:.0f}s)")
print(json.dumps({k: diag[k] for k in ("beta_raw", "nb_k", "min_resid_sd", "p_play", "sigma_shoot")}, indent=1, default=float), flush=True)
for k, v in sig_res.items():
    print("  sigma", k, {a: round(b, 3) for a, b in v["coverage"].items()}, "miss", round(v["miss"], 3))

if os.path.exists(DB): os.remove(DB)
store = PlayerStore(DB)
model.p = params                                                          # freeze fitted parameters
ec = EvalCollector(store, params, N_SIMS, 20261021, MODEL_VERSION)
run_pass(L[L.season == 2026], params, 2026, ec, model=model)
store.commit()
print(f"evaluation pass done: {ec.count} stored player forecasts ({time.time()-t0:.0f}s)", flush=True)
model.save("artifacts/player_state.json")
json.dump({"diag": diag, "params": {k: v for k, v in asdict(params).items() if k != "min_resid"}}, open("artifacts/player_fit.json", "w"), indent=1, default=float)

F = load_player_forecasts(DB, MODEL_VERSION)
M = attach_actuals(F, L[L.season == 2026])
M.to_pickle("artifacts/player_eval_frame.pkl")
res = player_metrics(M)
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 40)
for mode in ("confirmed", "unconfirmed"):
    print(f"\n===== {mode.upper()} =====")
    print(res[mode][["n", "mae_model_median", "mae_model_mean", "mae_baseline10", "rmse_model", "rmse_baseline10", "cov50", "cov80", "cov90"]].round(3).to_string())
    print("by role:\n", res[f"{mode}_by_role"].to_string())
    print("threshold calibration (P(over half-line)), Brier", round(res[f"{mode}_brier_threshold"], 4), "\n", res[f"{mode}_threshold"].to_string())
print("\nconfirmed, by how many regulars were out:\n", res["confirmed_by_absence"].to_string())
print("\nDNP calibration (unconfirmed):\n", res["dnp_calibration"].to_string())
pd.to_pickle(res, "artifacts/player_metrics.pkl")
