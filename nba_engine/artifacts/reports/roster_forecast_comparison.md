# Roster-built team forecast vs Elo vs simulation (2026-11-13)

Test: 7,380 games from 2023-2026 (2,460 with stored simulation forecasts). Team strength built from the players on the floor: each player's value (box-score composite per minute, current season plus half of last season, shrunk to average) times trailing minutes, summed over the top 10. Fit on two seasons, tested on the other two (three splits). Scores are log-loss (lower is better) with the paired standard error. Script: `scripts/roster_forecast_test.py` (`MODE=expected` for the version that does not know tonight's absences).

| Version | All games | First 25 games per team |
|---|---|---|
| Elo (home advantage 45) | 0.6145 | 0.6131 |
| Roster-built alone | 0.6290 (worse by 0.0145 +/- 0.0037) | 0.6361 (worse) |
| Elo + roster, roster = players who played that game | 0.6053 (better by 0.0092 +/- 0.0018) | 0.6100 (better by 0.0032 +/- 0.0030, not significant) |
| Elo + roster, roster = who played in last 3 games (no knowledge of tonight's absences) | 0.6130 (better by 0.0015 +/- 0.0009) | 0.6124 (better by 0.0008 +/- 0.0014) |

With the stored simulation (2024-25): sim 0.6137, Elo 0.6095, Elo + roster 0.6016, sim + Elo + roster 0.6023.

## Reading
- A team forecast built only from the roster is worse than Elo. Do not replace Elo with it.
- The gain from adding it to Elo comes almost entirely from knowing who actually plays that night (availability), not from the quality of the players on the roster. Without tonight's absences the gain is within noise.
- Caveat: "who played" slightly overstates what we know before tip-off (late scratches and garbage-time-only appearances), so 0.009 is an upper bound.

## Decision
Keep Elo (home advantage 45) blended with the simulation as the base, and keep adjusting for current injuries and rest at forecast time, since availability is where the measurable gain is. Do not build a roster-built team forecast. A more useful follow-up would be to price injuries with player values instead of the current flat per-unit rule, and test it on the live season.
