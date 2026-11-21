# GPT v2 — accuracy-first and commercial-readiness roadmap
Updated: 2026-11-21. Research architecture, not a claim of betting profitability.

## Non-negotiable gates before expanding the paid product
- First-issued, immutable pretip forecasts and all source timestamps persisted by tip.
- Accurate game/team/player IDs across trades; 100% of published player rows
  join to the correct as-of team and roster. Missing identity is an explicit
  omission, never a made-up lineup or player.
- Accurate historical as-of official injury status, expected active players,
  starters and probable minutes. Treat unknown and questionable as scenarios.
- Compare all new layers with existing simple Elo and core Ridge baselines
  using disjoint rolling chronological windows and a never-tuned test window.
- Report probability log-loss and Brier; score/margin/total MAE and signed bias;
  coverage vs nominal for 50/80/90% score intervals; player-stat MAE, coverage,
  and scoring/attempt distribution checks. Include uncertainty and sample sizes.
- No model promoted solely because one impressive conditional winning record
  or an individual 9/9 night happened.
- Licensing for every feed and redistribution right verified before charging
  for data-driven content. NBA.com's standard Terms of Use currently restrict
  use/publication of NBA Statistics to legitimate news reporting or private,
  noncommercial purposes and bar several commercial and gambling uses.
  Consult counsel/provider licensing before selling access.

## Order of engineering investment

### P0 — Data correctness, stronger QA, auditable availability (first)
**Current evidence:** an actual November report projected several unusual
player-team mappings, extreme starter minutes, and questionable shot-type
rates. Fix those before training increasingly complex models.

1. Maintain versioned (game date, team ID, player NBA ID, roster tenure)
   relationship records; flag duplicate provider IDs, traded players, missing
   athletes, unmatched injury aliases, and orphan projected players.
2. Collect genuine timestamped official NBA injury reports and lineup
   announcements; preserve collection time, player status and version. Do
   not confuse date attached to an old injury with capture time.
3. Flag infeasible rotations (e.g. all five starters >40 projected minutes),
   minute sums, shot/three-point attempt assumptions and all player/team
   box-score reconciliation invariants. Add model-output reasonableness tests.
4. Release gate: critical data QA errors zero on public sample; source
   lineage and status shown alongside each predicted player.

### P1 — Minutes, usage and rotation scenarios
1. Estimate minutes with calibrated uncertainty, position depth charts,
   substitution roles, foul/injury limits and coach rotation changes.
2. Fit player on/off effects for usage, potential assists and shot location
   from multi-season pretip-provenance datasets; avoid a one-coefficient
   scoring subtraction and avoid using future lineup outcomes as features.
3. Run separate healthy/questionable-out/confirmed-out scenarios and report
   probability-weighted or conditional projections, clearly labeled.
4. Release gate: player MIN/PTS/REB/AST errors and intervals beat the
   existing recent-games baseline on untouched future dates.

### P2 — Better team pace, possessions and possession event probabilities
1. Model offense-v-defense possessions at team, lineup, and home/rest levels.
2. Fit 2PT/3PT attempt choice, FT drawing, turnover, OREB, shooting
   probabilities and foul rates with calibration and proper tail behavior.
3. Reconcile resulting player/team box scores and OT draws; use joint
   correlated simulation for players sharing minutes and possessions.
4. Release gate: signed score/total/margin errors near zero over large
   forward holdouts, intervals have target coverage, log-loss improves.

### P3 — Opponent and lineup-aware matchups
1. Opponent shot zones, rim protection, switch/drop/zone coverage only when
   reliable tracking data exists; do not infer coach schemes from box scores.
2. Rebounding, matchup pace and G/F/C/positional allowances normalized for
   opportunities, opponent strength and lineup minutes.
3. Ablate features individually; require repeatedly verified forward gains
   before incorporation into the Monte Carlo model.

### P4 — Forecast ensemble, calibration and market comparison
1. Independently predict margin/total/winner using Elo, regularized
   statistical models and a well-tuned gradient booster; combine with
   the possession model using a stacker fit on a separate historical window.
2. Calibrate the **final simulation/ensemble** probability (not just a
   separate Ridge model) on nonoverlapping chronological calibration games.
3. Test home-vs-away reliability, overconfidence, underdog/favorite buckets,
   schedule regimes, player-prop interval coverage and drift.
4. Compare forecasts against archived, timestamped sportsbook pretip
   markets; measure line/odds quality after vig and errors, not just winners.
   No positive expected value or market edge without prospective evidence.

### P5 — Situational patterns, clearly segregated
- Current: predeclared team x venue x 0/1/2/3+ rest condition records.
- Report separate *last five form*, uninterrupted overall current streak,
  and actual **dated last two matching-condition games**. A 2-0
  qualifying sequence does not imply two consecutive overall wins.
- New candidates (one group at a time): opponent rest disadvantage,
  altitude/travel and timezone, 3-in-4/4-in-6 games, previous overtime,
  opponent pace/style, repeat matchup and playoff intensity.
- Every candidate must beat an ablation baseline after multiple-comparison
  controls and temporal splits. Descriptive streaks are not win odds.

## Prospective launch proof, not a fixed percentage
1. Daily pretip forecasts timestamped and frozen for the whole league.
2. Months of automatically scored, publicly inspectable forecasts, with
   skipped games and complete denominators, not cherry-picked winners.
3. Strong results across winners, score/total/spread, and player-prop
   calibration vs simple baselines and original pretip market prices.
4. Monitor confidence drift and re-training leakage; publish model versions,
   data-source descriptions, corrections and limitations.
5. Resolve all commercial sports-data redistribution and local legal
   issues before selling analytics/subscriptions or betting advice.

**Definition of success:** trustworthy, reproducible and well-calibrated
forecasts that genuinely improve future outcomes. Winning 100% of games
(or hitting all stat lines) is not attainable as a reliable model promise.
