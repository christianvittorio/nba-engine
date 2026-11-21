# GPT NBA Engine v2 — experimental quantitative architecture

This is a **separate model lane**, under gpt_engine/v2/. It does not modify the
existing Claude engine, existing GPT v1 baseline, or their daily workflows.
**Not production-calibrated; not an actionable betting recommendation.**

## Proven inputs

The existing data_foundation archive now has official-source:
- NBA team traditional + advanced game logs (2019–20 through 2026–27).
- Player-game stats, season rosters and coaching staff.
- Tracked player-versus-defender assignments, partial possessions, assists,
  potential assists and shooting, from SportsDataverse.
- As of the November 21, 2026 manifest: 8,515 regular-season games and
  195,249 player-game rows across complete historical and partial current
  seasons. Source position labels are **mostly G/F/C**, not precise PG/SG/SF/PF/C.
- Source-backed official NBA tip-off times are fetched from the NBA schedule
  archive at ingest time rather than estimated from the game date.

The new warehouse never treats backfilled historical records as genuine
contemporaneous injury/lineup or bookmaker snapshots. For those to be
historically available, both observation and retrieval timestamps must
precede the forecast cutoff. The previous game day is used for the earliest
admissible prior box-score result.

## C. Database and types

schema.sql has source catalogs, teams, players, coach tenure, roster membership,
games, all box scores, PBP, tracking, injuries, lineup reports, rotation stints,
immutable snapshots, model versions/experiments, pregame forecasts, simulations,
actuals/metrics, optional odds, and season distributions. provider_ids provides
explicit cross-provider entity matching. Unknown precise roster dates and
coaching changes remain NULL with source-quality flags.

contracts.py enforces real offset-aware UTC values and displays in selectable
IANA timezones (default Asia/Manila). warehouse.py provides as-of lookups and
refuses to store a newly created forecast after a known NBA tip time.
Corrections become new source records or new forecasts, never a rewrite of
past pregame claims.

ingest.py materializes source-backed team/player/roster/coach/game/actual rows
into SQLite. It fetches historical schedule UTC tips (including neutral-site
identity). The full raw archives remain in compressed Parquet/CSV; very large
game tracking records are ingested into SQLite only on request.

events.py can materialize selected game-level play-by-play and rotations
from the NBA public parquet source. Action clock time is not claimed to be
an actual UTC instant.

## D. Point-in-time features

features.py:
- Offensive/defensive/net efficiency, eFG, TS, three-point volume and opponent
  three-point percentage allowed, rebounds, turnovers, assists, FTA rate.
- Rolling 5, 10, and 20 games with sample shrinkage and multi-season baselines.
- Strength of schedule, opponent-adjusted offense, expected possessions.
- Rest days, back-to-backs, home or neutral venue.
- Cutoff checks for real availability, confirmations, and published evidence.
- Missingness and source flags. All current-day/future results are excluded.

tactics.py adds tracked defender-matchup evidence, uncertainty and labelled
observed team style. Real coach play calls, drop/switch/zone, transition, and
individual role classification remain UNVERIFIED.

## E. Progressive predictors

models.py:
- Home/neutral adjusted Elo with time-correct game-day updates.
- Ridge regression with independent margin and total targets.
- Optional LightGBM challenger (requires separate lightgbm installation).
- Disjoint chronological training, validation, and test partitions;
  hyperparameter and probability-calibration selection only on validation.
- Baseline fallback retained even if a challenger looks stronger.
- All margin/total forecasts reconcile to home and away scores.

experiments.py supports historical retrospective fitting and Elo comparisons.
It never enters invented historical forecasts into pregame_predictions.
**Not implemented yet:** a fitted hierarchical player model, a
holdout-demonstrated calibrated ensemble, and unbiased live market evaluation.
They must earn their place using experiment results.

## F/G. Possession Monte Carlo and players

simulation.py:
- Min 50 simulations, default 10,000 with configurable seed and batch size.
- Regulation possessions, shots, 3PA, FTs, TOV, rebounds, scoring, AST, STL, BLK.
- Jointly sampled player usage/minutes and shared team shooting fluctuations.
- Ties enter 5-minute overtime, repeated until someone wins.
- Team points equal exactly the points assigned to players; each individual
  score equals 2 * FG made + 3P made + FT made.
- Exact total team minutes = 240 + 25 per overtime (max 48 + 5 per overtime
  per player); every miss has exactly one offensive or defensive rebound.
- Means/medians, 50/80/90 percentiles, winner/OT probabilities, per-player
  stat distributions, attempt-conditioned percentages and threshold probabilities.
- Standard errors for sampling and a reproducible 1k/5k/10k convergence
  demonstration in convergence.py.

Player baselines and minutes are shrunk according to sample size
(players.py); they are NOT a validated hierarchical player model.
Per-possession event probabilities and minute-selection rules are **initial
research assumptions**, not an empirically proven basketball engine.
Increased Monte Carlo runs reduce simulation sampling noise, not bias.

## H/I. Scenarios and tactics

Availability and lineup states are timestamped, source-labeled, and queried
as of a cutoff; retroactive updates are rejected by as-of helpers.
scenarios.py recalculates player minutes, availability, team offense and
scores conditionally with NO invented scenario probabilities. Uncertain
availability causes a clear warning and disables betting claims.

tactics.py deliberately distinguishes observed prior-game team rates from
unverified coaching schemes. LLM prose must quote, never modify, the numeric
predictions; evidence_only_explanation returns immutable numeric model
values separately from qualitative interpretation.

## Evaluation, season outcomes and sensitivity

evaluation.py reports winner accuracy, Brier, log-loss, score/margin/total MAE,
and matched-game comparisons. It rejects purported pre-tip forecasts created
after the tip or odds retrieved after the cutoff. It does not assert any
positive return from unvalidated edge estimates.

season.py simulates correlated regular-season wins and standings seed
proxies, not actual NBA play-in tiebreaks or championship probabilities.
sensitivity.py shows conditional swings from pace, efficiency and home
advantage; no scenario odds are invented.

## How to run

From the repository root, install dependencies:

    python -m pip install -r gpt_engine/v2/requirements-test.txt
    python -m pytest -q gpt_engine/v2/tests

Populate only the current season's source records in a temporary database:

    python -m gpt_engine.v2.ingest --seasons 2027 --output /tmp/nba-v2.sqlite

Populate multi-season history:

    python -m gpt_engine.v2.ingest --seasons 2020 2021 2022 2023 2024 2025 2026 2027 --output /tmp/nba-v2.sqlite

Optional tracked records and selected play-by-play:

    python -m gpt_engine.v2.ingest --seasons 2027 --include-tracking --output /tmp/nba-v2.sqlite
    python -m gpt_engine.v2.events --db /tmp/nba-v2.sqlite --season 2027 --game-ids 0022600001

Generate research-only future game forecasts. Only games with sourced tip-off
times later than now can produce immutable pregame rows:

    python -m gpt_engine.v2.research --db /tmp/nba-v2.sqlite --date 2026-11-21 --n 1000

Run historic retrospective validation (do not call this a live historical
backtest). This requires multi-season data and real source tip times:

    python -m gpt_engine.v2.experiments --db /tmp/nba-v2.sqlite --train-before 2024-10-01 --validation-before 2025-10-01

Verify sampling convergence independent of NBA forecast accuracy:

    python -m gpt_engine.v2.convergence

The v2 pull-request CI checks SQL integrity, UTC/source mappings, strict
cutoffs, same-day and future-result poisoning, model splits, possession and
player-stat accounting, scenarios, random-seed reproducibility, source
ingestion and 1k/5k/10k Monte Carlo convergence.

## Release gates before betting use

1. Fitted baseline and LightGBM holdout performance across multiple seasons.
2. Verified live injuries, starting lineups, exact team/roster assignment dates.
3. Actual role-aware minutes/usage and robust position classification, plus
   matchup data normalized for possessions and team strength.
4. NBA-game simulation calibration for score errors, possessions, 3PA, fouls,
   rebounds, assists, OT rate and player statistical distributions.
5. Validation-fitted ensemble; independent locked test and live walk-forward
   pretip forecasts with immutable timestamped source snapshots.
6. Only then: model-vs-market calibration and pretip odds ROI/closing lines,
   including sportsbook vig, selection bias and uncertainty.
7. License review: do not scrape proprietary FantasyPros data without
   permission or assume public NBA data can automatically be commercialized.

A full SQLite database with historical PBP and tracking can exceed GitHub's
file limits. Keep generated warehouses out of the Git repository and publish
only compressed, permission-cleared data and small validation summaries.
