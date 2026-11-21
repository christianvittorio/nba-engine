# GPT v2: simulation wiring as of November 21, 2026

This document distinguishes live research, retrospective replay, and modules that exist but are not wired into the main Monte Carlo forecast.

| Layer | Status | Evidence and limitations |
|---|---|---|
| Historical data | Active | NBA team/player box scores back to 2020; corrected archives are not original real-time snapshots |
| Team features | Active | Offensive/defensive rating, opponent adjustments, pace, 5/10/20 trends, home/rest |
| Player minutes and usage | Active, estimated | Prior-game rates, injury exclusions, shared minutes; not officially confirmed starters |
| Injury status | Active when valid source exists | Claude's underlying ESPN collection reused with timestamps and player IDs; unknown status stays uncertain |
| Injury team-strength shift | Research heuristic | Conditional replacement-minute and point adjustment; not yet fitted or validated |
| Scoring simulation | Active | Shared possessions, 2PA, 3PA, free throws, turnovers, rebounds, assists, steals, blocks, OT |
| Coherent player/team totals | Active | Player scoring reconciles to team; 240 regulation minutes per team plus 25 per OT |
| Win probabilities / score distributions | Active | 50/80/90 percentiles, overtime and player thresholds; event probabilities uncalibrated |
| Tracked positional defense and tactical features | Separate experiment | Broad G/F/C evidence and observed team trends, not the default Monte Carlo |
| Elo/Ridge/optional LightGBM | Separate benchmarks | Models exist and can be compared, but the possession simulation does not automatically ensemble them |
| Calibrated probabilities and intervals | Research Ridge challenger only | Platt and conformal values not transferable to the possession simulator without validation |
| Season standings | Separate experiment | Wins and seed proxies; no validated championship bracket odds |

## Injury calibration experiment

The source history contains original Claude ESPN source revisions from October 31 to November 20, 2026. The new injury_effect_fit.py module authenticates both original source generation time and Git commit time before each tipoff. It estimates missing scoring *above a fixed replacement prior* only from earlier player games, then fits one strongly regularized coefficient relative to pregame Elo margin.

Training: dates before Nov 15; validation: Nov 15-17; later diagnostic: Nov 18-20. November 18's outcomes were already examined, so this is **not a pristine untouched holdout**. Unknown/day-to-day reports are never assumed Out and unavailable provider IDs are never invented.

The fit is observational, not a causal proof of injury value. No coefficient is automatically promoted to live forecasting. The resulting analysis must be compared against a zero-injury-effect fallback, with provenance and day-block uncertainty reported.

Run the GitHub workflow: .github/workflows/gpt-v2-injury-effect-research.yml.

## Remaining release gates

1. Expand original point-in-time injury/lineup history and verify player identities.
2. Demonstrate the fitted replacement response improves future margin and probability metrics.
3. Validate player minutes, usage distribution and team-score reconciliation against actual games.
4. Separate model-vs-sportsbook tests using only timely original odds snapshots.
5. Do not assert profit on the strength of an isolated slate.
