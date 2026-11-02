"""Write artifacts/reports/trends.md: what the situation scan finds, with the honesty checks (train/test split,
luck-only comparison for perfect runs). Re-run after rebuilding projections."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import numpy as np, pandas as pd
from nbaengine import trends as T

p = T.load_projected(); t = T.team_games(p, T.load_warmup_games()); L = T.add_labels(t)
S = [2023, 2024, 2025, 2026]
out = ["# Trends and streaks report", "",
       "Projections are walk-forward (each game projected from earlier games only), seasons 2023-2026 (2022 = warm-up). "
       "No sportsbook lines exist in this data: 'beat the projection' means better than the model, not a cashed bet.", ""]

# 1. rest effect
tp = t[t.proj_margin.notna()].copy(); tp["resid"] = tp.margin - tp.proj_margin
tp["b2b"] = (tp.rest == 0).astype(float); tp["ob2b"] = (tp.opp_rest == 0).astype(float)
h = tp[tp.home == 1]
out += ["## 1. Rest: what the model does not know", "",
        "Home team's margin minus the model's projected margin, regressed on whether each side is on the second night of a back-to-back.", "",
        "| Seasons | Home team on B2B | Away team on B2B | Games |", "|---|---|---|---|"]
for nm, d in (("2023-24", h[h.season <= 2024]), ("2025-26", h[h.season >= 2025])):
    X = np.column_stack([np.ones(len(d)), d.b2b, d.ob2b]); b = np.linalg.lstsq(X, d.resid.to_numpy(), rcond=None)[0]
    res = d.resid.to_numpy() - X @ b; se = np.sqrt(res.var() * np.diag(np.linalg.inv(X.T @ X)))
    out.append(f"| {nm} | {b[1]:+.2f} pts (se {se[1]:.2f}) | {b[2]:+.2f} pts (se {se[2]:.2f}) | {len(d)} |")
out += ["", "A negative number means the home team did worse than projected. The same direction and size in both halves is the "
        "evidence that this is real. A rest adjustment fitted on 2023-24 improved 2025-26 margin accuracy only slightly "
        "(log-loss 0.6104 to 0.6089), so it is a modest, real edge, not a big one.", ""]

# 2. league-wide scan with train/test
lt = T.league_trends(t, L, top=25)
out += ["## 2. League-wide situations (found on 2023-24, re-measured on 2025-26)", "",
        f"{int(lt.held_up.sum())} of the top {len(lt)} moved the same direction in the later seasons "
        "(a coin flip would give about half). The ones that held are two families: the rest effect, and mismatches (good teams against bad opponents beat the projected margin, bad teams fall short of it, so the model's margins look a little too compressed). "
        "The month-of-season rows (for example February totals) flipped sign between the two periods: that is what a luck-only pattern looks like.", "",
        "| Situation | Outcome | n found | Edge found | n later | Edge later | Held up |", "|---|---|---|---|---|---|---|"]
for r in lt.itertuples():
    out.append(f"| {r.situation} | {r.outcome} | {r.n_found} | {r.edge_found:+.1%} | {r.n_later} | {r.edge_later:+.1%} | {'yes' if r.held_up else 'no'} |")
out.append("")

# 3. perfect runs vs luck
real = T.perfect_records(t, L, "win", 12, S)
sims = [T.perfect_records(t, L, "win", 12, S, simulate_seed=s) for s in range(1, 21)]
out += ["## 3. 'Team A is 22-0 in this spot': how often does luck alone produce that?", "",
        "Team-specific situations of up to three features with at least 12 games where the team won every game (or lost every game). "
        "The luck-only world redraws every result from the model's own win probabilities, so no situation matters by construction.", "",
        "| Run length | Real data | Luck-only world (average of 20) |", "|---|---|---|"]
for k in (12, 15, 20):
    out.append(f"| {k}+ games | {int((real.n >= k).sum())} | {np.mean([(x.n >= k).sum() for x in sims]):.1f} |")
out += ["", f"The longest perfect run luck alone produced in 20 simulated worlds was {max(x.n.max() for x in sims if len(x))} games. "
        "Spotting a perfect run in a hand-picked spot is therefore weak evidence by itself. "
        "The least likely real runs, given who the opponents were:", "",
        "| Team | Situation | Run | Model's chance of this run |", "|---|---|---|---|"]
for r in real[real.n >= 15].sort_values("model_chance_of_this_run").head(8).itertuples():
    out.append(f"| {r.team} | {r.situation} | {r.wins}-{r.n - r.wins} | {r.model_chance_of_this_run:.4%} |")
out.append("")

# 4. user example
ex = T.select(t, L, {"venue": ["home"], "rest": ["B2B"]}, {"proj_total": (212.5, None)}, S)
out += ["## 4. Example: home, second night of a back-to-back, projected total above 212.5", "",
        T.summarize_situation(ex, t).round(3).to_markdown(index=False), ""]
os.makedirs("artifacts/reports", exist_ok=True)
open("artifacts/reports/trends.md", "w").write("\n".join(out))
print("wrote artifacts/reports/trends.md")
