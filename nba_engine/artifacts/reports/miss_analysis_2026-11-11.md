# Miss analysis and improvement plan (2026-11-11)

Question: why does the engine miss games, and which misses are fixable? Evidence: 2,460 stored walk-forward forecasts (2024 and 2025 seasons), 4,920 walk-forward games in the calibration report, 6,150 modern games (2022-2026) for an Elo retune, and the 83 live games of 2026-27 that have stored forecasts.

## 1. Most misses are noise, not error
- Margin error of the sim has a standard deviation of about 14.3 points. If errors were pure noise of that size, 29% of games would miss by 15 or more. The sim actually misses by 15+ in 27.8% of games and by 20+ in 14.8%. That is what the noise level predicts, so a 20-point miss in a single game is not evidence that the model is broken.
- Favourites win more often than we say in every confidence band (predicted 55/65/75/84/92%, observed 57/68/78/89/100%), so we are slightly under-confident, not over-confident.
- The 80% margin interval covers 77.7% of games (74.9% in 2025-26, 73% in the last 300 games), so the tails are a little too narrow. Overtime is under-predicted: 2.3% predicted against 5.1% actual.
- On the live 83 games the sim's typical margin miss is 11.6 points, against 11.8 for Elo. Against the DraftKings closing line the book was closer on margins (see the backtest: our blend weight against the book is about zero).

## 2. What can actually be improved (tested, out-of-sample)
| # | Finding | Evidence | Expected gain |
|---|---|---|---|
| 1 | **Elo home-court setting is wrong for the modern game.** It is 80 Elo points (tuned on 1996-2015). Modern home win rate is 54-55%; at equal ratings Elo says 61%. Mean Elo home probability in the stored forecasts is 0.597 against 0.543 actual. | Walk-forward retune on 6,150 games: home advantage 40-50 beats 80 in every season (log-loss 2024 0.618 to 0.612, 2025 0.615 to 0.607, 2026 0.600 to 0.595). Tuned on 2023-24, tested on 2025-26: 0.6078 to 0.6037. | About 0.004 log-loss, the largest single fix found |
| 2 | **Sim win probabilities are not stretched enough.** Fitted slope 1.2 to 1.36 on logit(p). | Fit on one season, tested on the other, both directions: log-loss improves 0.0010 to 0.0040. | Small but free |
| 3 | **Blend sim and Elo.** A 50/50 average beats either alone. | 2025: sim 0.6162, Elo 0.6145, blend 0.6118. 2024: 0.6163, 0.6176, 0.6136. | About 0.003 |
| 4 | **Predicted margins are compressed.** Actual margin = 1.12 x predicted margin (sim) and 1.2 x (Elo), both seasons. | RMSE gain out of sample only 0.01 to 0.1 points, so this is minor. | Minimal |
| 5 | **Players: points over-projected by about 1.1 per player-game, assists about 0.2.** | z-scores very large over the season (daily review). | Direct fix for over/under picks |
| 6 | **Overtime under-predicted.** | 2.3% against 5.1% | Affects totals tails and the 80% range |

## 3. What the daily misses teach (11-09 sample)
- Wrong-winner games came from shooting variance (CHA 23 threes against 16 expected, 2 standard deviations above the binomial expectation) and blowout dynamics (CLE stars sat out a 27-point 4th-quarter deficit). Neither is predictable pre-game.
- Several of the 11-09 misses were over 40 points (GSW by 51), which fall into garbage time. A margin-capped or ranked-by-win scoring would not penalise them as heavily as raw margin error does.
- Availability errors are small: players rated 80%+ to play who did not, and players rated under 50% who did, were a handful per day.

## 4. What not to chase
- More matchup stats: tested twice against box-score results with no measurable gain; per-game noise (SD 14 points) swamps team-style effects of 1 to 2 points.
- Roster-strength (RAPM): +0.04 only.
- Fitting the model to single-day misses: a 15+ point miss is a normal one-in-three-games event.

## 5. Plan, in order
1. Re-fit Elo on modern data (home advantage about 45, keep K 20, carryover 0.6 to 0.7), then rerun the walk-forward and the sim on top of it. Gate: log-loss improves in every held-out season.
2. Stretch the sim win probability (slope about 1.2) and blend with the corrected Elo; check on 2024 and 2025 held-out.
3. Widen the sim's tails slightly and raise the overtime rate to about 5%; check that 80% coverage reaches 80%.
4. Apply the per-stat player bias correction (points -1.1, assists -0.2), then check the ladder calibration again.
5. Keep grading every pick and tracking the closing-line comparison; only act on a bias when its z-score holds up over many games.
