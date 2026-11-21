# GPT v2: independently tested matchup layers and calibration

This is an independent research extension in the NBA engine. It does **not**
modify the existing Claude or GPT v1 prediction workflows.

## Why GPT previously missed available injury data

Claude already runs ESPN roster and injury collection in
nba_engine/nbaengine/availability.py, saved to
nba_engine/artifacts/availability.json.

Claude's player_live.py explicitly runs its projections in **unconfirmed**
lineup mode. It does **not** have automatically confirmed starting fives.
Claude's refresh_forecast.py can recompute even after tip for review,
which must never be passed off as a historically available pre-tip forecast.

shared_availability.py reuses **source data**, not Claude's predicted scores,
player projections or injury adjustment coefficients. It maps official NBA
athlete IDs conservatively, preserves ESPN provider-native injury dates
separately from actual snapshot generation, and requires the snapshot to
exist before the intended cutoff. Unknown ESPN status terms such as
Day-To-Day remain UNKNOWN, not magically confirmed or Questionable.
Negative placeholder athlete IDs are not treated as real NBA provider IDs.

Fresh snapshot capture runs through independent
.github/workflows/gpt-v2-availability-snapshots.yml after Claude's usual
daily fetches. The archived records are timestamped and immutable.
Invalid or stale source data is rejected. Existing confirmed-lineup tables
remain empty until a trustworthy confirmation feed is ingested. A roster
listing by itself is not a confirmed starting five.

This does not retroactively create real November 18 pregame injury reports:
the repository's November 20 injury snapshot was captured two days later.
For that older slate, original availability is unknown.

## 4. Test matchup evidence independently

feature_ablation.py builds only from earlier completed game dates:

- Core: 5/10/20-game team strength, pace, rest and multi-season priors.
- Core + shooting: eFG, TS, attempts and 3P defense.
- Core + rebounding/turnovers.
- Core + *observed* tactical indicators (pace and passing trends; no invented coach actions).
- Core + offense-vs-defense interaction features.
- Core + tracked broad G/F/C defender position allowed points, assists and potential assists, normalized for observed matchup possessions and with sample size.
- All observed layers together.

Every additional group is tested *against core only*. A group is not selected
because it seems conceptually attractive, or because it matched one slate.
Tracked position labels are usually G, F or C. They do not substantiate exact
PG, SG, SF, PF and C splits, nor direct matchup causality.

## 5. Calibrate win probabilities and score intervals

ablation_eval.py uses strictly ordered NBA Eastern-date partitions:

| Stage | Dates | Allowed purpose |
|---|---|---|
| Train | Before Oct 1, 2024 | Fit two Ridge targets, margin and total |
| Feature selection | Oct 1, 2024–Jan 29, 2025 | Pick the feature group and alpha |
| Calibration | Jan 30–Jun 30, 2025 | Regularized Platt win probabilities and split-conformal 50/80/90% intervals |
| Untouched test | Oct 1, 2025–Jun 30, 2026 | Report loss, Brier, margin/total MAE and interval coverage, with paired bootstrap intervals |

Compared baselines: Elo, core-only Ridge, selected raw and selected calibrated.
The 2025–26 outcome labels are not read by feature selection or calibration.

The underlying historical NBA archive is retrospective corrected data, not a
complete series of originally collected live snapshots.

**Important:** this calibration applies to the separately fitted Ridge
research challenger. It does **not** automatically calibrate every player
prop or the existing possession simulator. The live betting engine is not
automatically replaced, and no bookmaker edge is claimed.

## Run locally or via Actions

    python -m pip install -r gpt_engine/v2/requirements-test.txt
    python -m pytest -q gpt_engine/v2/tests
    python -m gpt_engine.v2.ablation_eval --years 2022 2023 2024 2025 2026 --output /tmp/gpt-v2-evidence.json
    python -m gpt_engine.v2.capture_shared --max-age-hours 12

GitHub Action gpt-v2-matchup-ablation-calibration publishes the actual JSON
holdout results as an artifact and checks the release gate stays disabled.
This is evidence gathering, not a declaration of profitability.
