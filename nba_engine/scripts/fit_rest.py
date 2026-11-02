"""Fit the back-to-back margin effect from walk-forward projections (seasons 2023-2026) and save artifacts/rest_fit.json.
Effect = change in the home team's margin versus the model's projection when the home team / the away team is on the second
night of a back-to-back. Also reports an honest out-of-sample check (fit 2023-24, score 2025-26)."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import numpy as np
from scipy.stats import norm
from nbaengine import trends as T

p = T.load_projected(); t = T.team_games(p, T.load_warmup_games())
h = t[(t.home == 1) & t.proj_margin.notna()].copy()
h["resid"] = h.margin - h.proj_margin
h["hb"] = (h.rest == 0).astype(float); h["ab"] = (h.opp_rest == 0).astype(float)
X = lambda d: np.column_stack([np.ones(len(d)), d.hb, d.ab])
def fit(d):
    b = np.linalg.lstsq(X(d), d.resid.to_numpy(), rcond=None)[0]
    res = d.resid.to_numpy() - X(d) @ b
    return b, np.sqrt(res.var() * np.diag(np.linalg.inv(X(d).T @ X(d)))), res.std()
b, se, sd = fit(h)
tr, te = h[h.season <= 2024], h[h.season >= 2025]
b2, _, sd2 = fit(tr)
def ll(pm, y): pm = np.clip(pm, 1e-4, 1 - 1e-4); return float(-(y * np.log(pm) + (1 - y) * np.log(1 - pm)).mean())
y = te.win.to_numpy(); m0 = te.proj_margin.to_numpy()
sd0 = (tr.resid - tr.resid.mean()).std()
oos = {"fit_on": "2023-24", "scored_on": "2025-26", "log_loss_before": ll(norm.cdf(m0 / sd0), y),
       "log_loss_after": ll(norm.cdf((m0 + X(te) @ b2) / sd2), y), "mae_before": float(np.abs(te.margin - m0).mean()),
       "mae_after": float(np.abs(te.margin - (m0 + X(te) @ b2)).mean())}
out = {"home_b2b": float(b[1]), "away_b2b": float(b[2]), "se_home_b2b": float(se[1]), "se_away_b2b": float(se[2]),
       "fit_seasons": "2023-2026", "n_games": int(len(h)), "out_of_sample_check": oos,
       "note": "Margin points added to the HOME team's projected margin. Fitted on projections that did not use rest."}
json.dump(out, open(os.path.join(ROOT, "artifacts/rest_fit.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
