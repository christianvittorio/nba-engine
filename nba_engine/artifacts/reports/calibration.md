# Calibration report

Generated 2026-11-05T20:56:09Z. Team layer: 4920 walk-forward games (2022-23 to 2025-26, each projected only from earlier games) plus the live season. Player layer: 2025-26 frozen-parameter evaluation plus live games as they accumulate.

## 1. Team layer on past games

| games | n | log-loss sim | log-loss Elo | home win actual/pred | margin bias | margin MAE | total bias | total MAE | 80% margin cov | 80% total cov | OT pred/actual |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2022-23 | 1230 | 0.6499 | 0.6481 | 0.580/0.558 | +0.25 | 10.28 | +0.24 | 14.63 | 81.7% | 77.5% | 0.023/0.064 |
| 2023-24 | 1230 | 0.6179 | 0.6176 | 0.543/0.553 | +0.06 | 11.13 | -0.29 | 14.69 | 76.8% | 78.7% | 0.023/0.048 |
| 2024-25 | 1230 | 0.6160 | 0.6145 | 0.544/0.551 | -0.39 | 11.13 | +0.09 | 14.71 | 77.4% | 78.4% | 0.022/0.049 |
| 2025-26 | 1230 | 0.6086 | 0.5986 | 0.554/0.544 | +0.01 | 11.49 | +0.28 | 15.07 | 74.9% | 77.6% | 0.022/0.044 |
| last 600 (end of 2025-26) | 600 | 0.5836 | 0.5671 | 0.548/0.551 | -0.20 | 12.08 | +0.87 | 14.64 | 73.2% | 79.3% | 0.022/0.035 |
| last 300 (end of 2025-26) | 300 | 0.5482 | 0.5066 | 0.593/0.550 | +1.32 | 11.95 | +1.92 | 14.99 | 73.0% | 80.0% | 0.022/0.043 |
| all | 4920 | 0.6231 | 0.6197 | 0.555/0.551 | -0.02 | 11.01 | +0.08 | 14.77 | 77.7% | 78.0% | 0.023/0.051 |

Reading it: a perfectly calibrated model has bias near 0, 80% coverage near 80%, and predicted = actual in the last column. The first season (2022-23) is the weakest because the model had only one season of history; the later seasons are the fair test.

### Win probability reliability (last 1230 games)

| bin | n | predicted | observed | gap |
|---|---|---|---|---|
| (-0.001, 0.15] | 7 | 0.110 | 0.000 | -0.110 |
| (0.15, 0.25] | 50 | 0.213 | 0.140 | -0.073 |
| (0.25, 0.35] | 110 | 0.307 | 0.300 | -0.007 |
| (0.35, 0.45] | 194 | 0.407 | 0.361 | -0.046 |
| (0.45, 0.55] | 288 | 0.501 | 0.521 | +0.020 |
| (0.55, 0.65] | 247 | 0.599 | 0.640 | +0.041 |
| (0.65, 0.75] | 170 | 0.697 | 0.776 | +0.079 |
| (0.75, 0.85] | 129 | 0.796 | 0.814 | +0.017 |
| (0.85, 1.0] | 35 | 0.887 | 0.771 | -0.115 |

### Total score by projected total (last 2460 games)

| projected total | n | projected | actual | bias | over_rate |
|---|---|---|---|---|---|
| <220 | 266 | 216.4 | 216.7 | +0.28 | 50.4% |
| 220-226 | 511 | 223.3 | 224.2 | +0.96 | 50.7% |
| 226-232 | 788 | 229.1 | 229.6 | +0.54 | 51.1% |
| 232-238 | 635 | 234.7 | 234.4 | -0.31 | 49.8% |
| 238+ | 260 | 241.2 | 239.9 | -1.27 | 44.2% |

### Slopes (actual vs projected)

Margin slope 1.33 +/- 0.09 and total slope 1.17 +/- 0.11 over the last 600 games of the walk-forward data (end of 2025-26; 1.00 = ideal). All four seasons: margin 1.06, total 0.92.

## 2. Recalibration

* **Overtime:** over the last two seasons the simulator said 2.2% of games go to overtime; 4.6% actually did. The daily report now multiplies the simulator's P(OT) by 2.08.
* **Margin range:** over the last 1230 games the 80% range covers 74.9% of results (should be 80%). Refitting the spread on the last 1230 games gives kappa 0.884 vs 0.784 in use; on the 300 newest games held out the refit improved the log-likelihood by 0.60%. Displayed margin ranges are widened by x1.13.
* **Total range:** coverage 77.6%; spread refit 0.975 vs 0.921 (held-out gain 0.06%). Displayed total ranges x1.06.
* **Not changed:** projected means and win probabilities. A Platt-style sharpening of win probabilities improved log-loss by about 0.0015 in the last two seasons but hurt in 2023-24, and a margin/total scale refit moved MAE by under 0.1 point, so neither is applied.

## 3. Team layer on the live season

50 live games with stored pre-game forecasts and results (small sample: treat as a smoke test, not a verdict).

| metric | value |
|---|---|
| n | 50.000 |
| sim_log_loss | 0.627 |
| elo_log_loss | 0.631 |
| sim_brier | 0.221 |
| margin_bias | 0.867 |
| margin_mae | 11.130 |
| total_bias | -7.862 |
| total_bias_se | 2.777 |
| total_mae | 16.394 |
| margin_cov80 | 0.800 |
| total_cov80 | 0.680 |
| ot_pred | 0.022 |
| ot_actual | 0.060 |
| home_win_pred | 0.552 |
| home_win_actual | 0.540 |

**Total score:** live games are totalling -7.9 points versus the projection (standard error 2.8). Part of this is that the scoring-level correction learned at the end of 2025-26 (about +6 points) was carried into the new season while scoring dropped. From 2026-11-04 the level restarts at 0 each season and tracks faster for the first 60 games (walk-forward history shows no loss from this: total MAE 14.773 vs 14.774 for all games; forecasts already stored are not touched).

Variants on the same live games (each only for games that had that variant stored):

| model | n | log_loss | margin_mae |
|---|---|---|---|
| sim_mc | 50.0 | 0.6268 | 11.13 |
| sim_mc_rest | 29.0 | 0.5906 | 9.88 |
| sim_mc_sit | 14.0 | 0.5889 | 9.62 |
| sim_mc_inj | 29.0 | 0.6312 | 10.41 |
| sim_mc_full | 29.0 | 0.6243 | 10.59 |
| sim_mc_all | 14.0 | 0.6074 | 9.76 |

## 4. Player layer

### 2025-26, lineup unknown (what the daily job stores)

| stat | n | mean_forecast | mean_actual | bias | mae | cov50 | cov80 | cov90 |
|---|---|---|---|---|---|---|---|---|
| min | 37269 | 15.67 | 15.65 | -0.018 | 7.30 | 61.7% | 85.4% | 93.9% |
| pts | 37269 | 7.46 | 7.51 | +0.048 | 4.74 | 65.4% | 86.9% | 94.6% |
| reb | 37269 | 2.86 | 2.84 | -0.021 | 1.90 | 70.7% | 90.0% | 95.9% |
| ast | 37269 | 1.72 | 1.74 | +0.020 | 1.26 | 76.1% | 91.7% | 96.1% |
| stl | 37269 | 0.54 | 0.55 | +0.005 | 0.59 | 85.4% | 93.8% | 97.0% |
| blk | 37269 | 0.32 | 0.31 | -0.004 | 0.40 | 88.1% | 94.9% | 97.3% |
| tov | 37269 | 0.89 | 0.89 | +0.005 | 0.78 | 81.7% | 93.5% | 96.8% |
| tpm | 37269 | 0.86 | 0.86 | +0.001 | 0.78 | 82.2% | 93.5% | 96.7% |
| fgm | 37269 | 2.72 | 2.73 | +0.009 | 1.77 | 70.5% | 89.6% | 95.7% |
| fga | 37269 | 5.77 | 5.78 | +0.010 | 3.20 | 67.6% | 87.9% | 95.2% |
| ftm | 37269 | 1.16 | 1.19 | +0.029 | 1.13 | 79.1% | 91.3% | 95.1% |
| fta | 37269 | 1.49 | 1.52 | +0.034 | 1.40 | 76.1% | 90.4% | 94.6% |
| pra | 37269 | 12.04 | 12.08 | +0.047 | 6.84 | 63.2% | 85.2% | 94.0% |

Per-player means are unbiased (bias is a few hundredths of a unit). Coverage of the discrete stats (steals, blocks, turnovers, threes) reads high because counts take whole values and a range edge on a whole number counts as inside; points, minutes and points+rebounds+assists are the informative rows, and they sit at or slightly above nominal. In the last fifth of the season points were under-projected by about 0.25 per player (+3%), a drift worth watching.

### Live 2026-27 (14 games, 335 player rows)

| stat | n | mean_forecast | mean_actual | bias | mae | cov50 | cov80 | cov90 |
|---|---|---|---|---|---|---|---|---|
| min | 335 | 18.83 | 19.53 | +0.708 | 6.90 | 59.1% | 84.2% | 94.9% |
| pts | 335 | 9.25 | 9.16 | -0.098 | 4.73 | 63.9% | 89.3% | 97.0% |
| reb | 335 | 3.47 | 3.63 | +0.161 | 2.05 | 69.9% | 90.1% | 96.1% |
| ast | 335 | 2.13 | 2.09 | -0.041 | 1.28 | 77.6% | 93.1% | 97.3% |
| stl | 335 | 0.66 | 0.59 | -0.062 | 0.63 | 87.5% | 96.1% | 97.9% |
| blk | 335 | 0.39 | 0.45 | +0.063 | 0.49 | 83.0% | 92.5% | 96.1% |
| tov | 335 | 1.13 | 1.12 | -0.003 | 0.86 | 77.9% | 94.9% | 97.6% |
| tpm | 335 | 1.05 | 1.01 | -0.043 | 0.85 | 82.4% | 93.4% | 98.2% |
| fgm | 335 | 3.35 | 3.21 | -0.139 | 1.73 | 70.1% | 92.8% | 98.2% |
| fga | 335 | 7.11 | 7.15 | +0.047 | 3.16 | 66.3% | 89.3% | 97.0% |
| ftm | 335 | 1.50 | 1.72 | +0.224 | 1.35 | 76.7% | 91.9% | 95.2% |
| fta | 335 | 1.92 | 2.20 | +0.277 | 1.66 | 73.7% | 88.7% | 94.9% |
| pra | 335 | 14.86 | 14.88 | +0.022 | 6.61 | 63.3% | 87.5% | 97.3% |

## 5. What this does not cover

Player lines are projected one team at a time and are not reconciled with the team simulation. Win-probability recalibration, margin/total scale and team-specific bias are reported, not applied. Betting-line calibration is impossible without sportsbook lines in the data.