# The 49 proposed inputs: what happened to each (2026-11-07)

Method: every input was checked on walk-forward 2025-26 player forecasts (26,500 player-games, confirmed lineups), regression of the forecast error on the input, robust t-statistics, same sign in both halves, about 100 tests so |t| above 3 is the bar. Inputs that passed were then tested out of sample (fit on the first half, scored on the second) and only kept if the held-out error fell. `scripts/feature_signal_test.py`, results in `artifacts/feature_signal_test.csv`.

## Built or tested now
| # | Input | Result |
|---|---|---|
| 1 | Home/away splits | No player-level signal (home flag t about 1.8 on points, not stable). Home advantage stays in the team layer. |
| 2 | Bounce-back rates | Real, but it is momentum, not reversal: a player who beat the forecast last game tends to beat it again (t 4 to 15, both halves). Size is small: about 5% of last game's error carries forward. Only the minutes part improves held-out error, so only that was built. |
| 3, 26 | Situational history, rest and back-to-back matrix | Team back-to-back is already a margin adjustment (`*_sit`). At player level, no signal (t under 1). |
| 6, 29, 46 | Fatigue, workload, player rest days | Signal on minutes only: players returning after 3+ missed team games play about 1.5 minutes fewer than forecast (t about -10); heavy recent minutes predict more minutes. Built (minutes momentum 0.136, return -1.45): minutes MAE 4.676 to 4.633, points-rebounds-assists 5.878 to 5.860, unconfirmed minutes 7.569 to 7.458. |
| 11 | Blowout probability | No effect on minutes (t about -0.6). Small unexplained positive link to assists. Not used. |
| 48 | Travel and time zone | No stable signal (assists t -2.6 in one half only). Not used. |
| 12, 27 | Pace, points per possession | Already the core of the simulator. |
| 19 | EWMA | Already used for player rates and minutes, team profiles (25-game half-life). |
| 32 | PRA composite | Already forecast. |
| 16, 18, 22 | USG%, true shooting, PER | Computable from box scores but redundant: the model already uses the underlying rates. Descriptive only. |
| 45 | Opponent last-5 defensive rating | Tested faster defence memory (10 to 15 games): no better than 25. |
| 9, 10 | Potential vs actual output, gap | Over/under-performers are listed in the replay report (forecast vs actual per player). |
| 20, 31 | Sigma / variance per player | Not built yet. Worth doing: a player's recent spread correlates 0.2 to 0.39 with the size of the next error. |
| 33, 34 | Triple-double probability, bench surge | Not built. Triple-double probability can be read from the existing simulated player lines. |

## Needs data the GitHub job can collect (ESPN play-by-play, odds, officials); no history on disk
24 clutch stats, 25 substitution patterns, 17 on/off net rating, 21 lineup net rating, 23 RAPM, 38 second-unit matchup, 47 timeout patterns, 30 first-half model and 36 quarter-by-quarter (quarter scores), 35 shot zones and 41 corner-three rate (shot coordinates), 14 referee tendencies (officials), 13 and 49 closing line and line movement (game odds snapshot only; no prop lines).

## Not available from free sources
4 player vs player, 5 defensive scheme, 8 touches, 28 shot type vs defender, 37 defender assignment, 39 pick-and-roll frequency, 40 isolation frequency, 43 paint touches, 44 transition frequency, sharp money. These need tracking or paid data.

## Not applicable in the regular season
3 (elimination), 7 series context and momentum. 15 coaching adjustment risk has no data definition.
