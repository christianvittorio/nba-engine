# GPT v2 priorities 3–5 — research implementation (Nov 21, 2026)

The historical evaluations do **not** automatically replace the daily possession simulator. Player-team identity, minutes, and shot-profile validation remain essential before research features can be promoted.

## P3 — Possession events and player shot allocation

The default simulation remains event_model="baseline", with unchanged RNG
and seed behavior. An explicit opt-in event_model="player_shot_mix" now
assigns 2PA, 3PA and FT attempts using each player's prior-game 2PA/3PA/FTA
per-minute rates, shrunk toward league priors. It preserves exact joint
player/team scoring accounting and 240 regulation minutes per team.
There is no automatic production switch, and no new factual claim about
confirmed starting lineups.

The event_rate_eval.py experiment fits opponent-aware 3PA/FGA, FTA/FGA,
turnover probability and OREB probability from the team's 20-game prior
and the opponent's 20-game defensive allowed rate. It selects only a
bounded weight among 0, .2, .4, .6, .8, 1 on a separate validation period.
It evaluates out-of-time event-rate MAE and signed bias against each
team's own 20-game rates. This is not yet a simulation accuracy test.

## P4 — Offensive/defensive opponent events

feature_ablation.py now derives defense's allowed 3PA/FGA, FTA/FGA,
forced turnover rate and offensive rebound allowance from official
prior game source columns, never from current-day outcomes.
Eight directional cross features join the home and away contexts.
The new groups core+shot_possession_matchups and core+all_matchup_cross
are independently evaluated in the existing five-season Ridge ablation.
There is no assertion of observed schemes/coach tactics.

## P5 — Elo and Ridge calibrated ensemble

ensemble_eval.py blends day-safe Elo with a frozen previously selected
matchup Ridge component (alpha 100), selecting the blend weight exclusively
on the chronological selection period. Platt calibration and conformal
50/80/90-percent score intervals use a separate later period. The
2025–26 historical period is graded only after choices are frozen.

Reports compare Elo, Ridge, raw ensemble, calibrated ensemble, log loss,
Brier, win accuracy, score and margin MAE, probability reliability and
observed coverage. This calibrates the **Elo/Ridge ensemble only** — it
does not calibrate the full possession simulator and is never
automatically deployed.

## Run

GitHub Actions: .github/workflows/gpt-v2-priority-345-eval.yml

Install dependencies: python -m pip install -r gpt_engine/v2/requirements-test.txt

Unit tests: python -m pytest -q gpt_engine/v2/tests/test_advanced_event_matchup_ensemble.py

Rate experiment: python -m gpt_engine.v2.event_rate_eval --output /tmp/events.json

Ensemble: python -m gpt_engine.v2.ensemble_eval --output /tmp/ensemble.json

## Promotion standard

Require correct as-of rosters, realistic player rates, independent
future-period gains over the baseline and interval coverage close to
nominal. Our 2025–26 retrospective test has been examined in prior work;
a fresh prospective season is essential before making external claims.
Winning every game or every player prop is not a realistic promise.
