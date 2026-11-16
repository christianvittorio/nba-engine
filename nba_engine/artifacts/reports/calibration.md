# Calibration report

Generated 2026-11-16T23:12:26Z. Team layer: 4920 walk-forward games (2022-23 to 2025-26, each projected only from earlier games) plus the live season. Player layer: 2025-26 frozen-parameter evaluation plus live games as they accumulate.

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

126 live games with stored pre-game forecasts and results (small sample: treat as a smoke test, not a verdict).

| metric | value |
|---|---|
| n | 126.000 |
| sim_log_loss | 0.571 |
| elo_log_loss | 0.559 |
| sim_brier | 0.194 |
| margin_bias | 1.251 |
| margin_mae | 11.534 |
| total_bias | -1.743 |
| total_bias_se | 1.698 |
| total_mae | 14.913 |
| margin_cov80 | 0.762 |
| total_cov80 | 0.786 |
| ot_pred | 0.022 |
| ot_actual | 0.056 |
| home_win_pred | 0.522 |
| home_win_actual | 0.532 |

**Total score:** live games are totalling -1.7 points versus the projection (standard error 1.7). Part of this is that the scoring-level correction learned at the end of 2025-26 (about +6 points) was carried into the new season while scoring dropped. From 2026-11-04 the level restarts at 0 each season and tracks faster for the first 60 games (walk-forward history shows no loss from this: total MAE 14.773 vs 14.774 for all games; forecasts already stored are not touched).

Variants on the same live games (each only for games that had that variant stored):

| model | n | log_loss | margin_mae |
|---|---|---|---|
| sim_mc | 126.0 | 0.5705 | 11.53 |
| sim_mc_rest | 105.0 | 0.5528 | 11.25 |
| sim_mc_sit | 90.0 | 0.5380 | 11.34 |
| sim_mc_inj | 105.0 | 0.5514 | 11.47 |
| sim_mc_full | 105.0 | 0.5538 | 11.49 |
| sim_mc_all | 90.0 | 0.5308 | 11.41 |

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

### Live 2026-27 (90 games, 2158 player rows)

| stat | n | mean_forecast | mean_actual | bias | mae | cov50 | cov80 | cov90 |
|---|---|---|---|---|---|---|---|---|
| min | 2158 | 18.64 | 19.20 | +0.562 | 6.82 | 56.4% | 84.4% | 94.2% |
| pts | 2158 | 9.19 | 9.11 | -0.078 | 4.84 | 62.1% | 87.5% | 95.4% |
| reb | 2158 | 3.41 | 3.46 | +0.055 | 1.96 | 68.0% | 90.0% | 96.3% |
| ast | 2158 | 2.11 | 2.14 | +0.023 | 1.34 | 74.2% | 91.5% | 96.4% |
| stl | 2158 | 0.64 | 0.61 | -0.030 | 0.63 | 85.5% | 95.1% | 97.5% |
| blk | 2158 | 0.38 | 0.41 | +0.026 | 0.47 | 85.3% | 94.0% | 97.1% |
| tov | 2158 | 1.12 | 1.10 | -0.014 | 0.87 | 80.0% | 93.9% | 97.5% |
| tpm | 2158 | 1.05 | 1.09 | +0.033 | 0.88 | 80.1% | 93.4% | 96.9% |
| fgm | 2158 | 3.31 | 3.22 | -0.088 | 1.80 | 68.8% | 91.0% | 96.5% |
| fga | 2158 | 7.05 | 7.01 | -0.039 | 3.09 | 66.3% | 89.2% | 96.2% |
| ftm | 2158 | 1.51 | 1.57 | +0.066 | 1.29 | 75.8% | 91.0% | 95.4% |
| fta | 2158 | 1.92 | 1.98 | +0.054 | 1.57 | 72.2% | 90.6% | 95.6% |
| pra | 2158 | 14.70 | 14.70 | +0.000 | 6.66 | 60.1% | 85.9% | 94.9% |

## 5. What this does not cover

Player lines are projected one team at a time and are not reconciled with the team simulation. Win-probability recalibration, margin/total scale and team-specific bias are reported, not applied. Betting-line calibration is impossible without sportsbook lines in the data.