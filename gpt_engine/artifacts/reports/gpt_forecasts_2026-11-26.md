# GPT challenger forecasts — 2026-11-26

Model: gpt-stat-v1.0. **Independent baseline** using historic game results; it does not use Claude's ratings, simulation outputs or player predictions.
Source: completed games in the shared SQLite archives; upcoming schedule from ESPN's unofficial feed.
Each new forecast is saved only before its game starts and is never replaced.
No player predictions or betting edges are claimed by this first release.

Found 0 scheduled games; skipped 0 already tipped-off games; GPT pregame forecasts for this date: 0.

**No valid pregame GPT forecasts for this date.** We do not reuse earlier slates.

## GPT performance on completed, timestamp-validated forecasts

- Graded games: 25
- Win Brier score: 0.2374
- Win log-loss: 0.6649
- Winner accuracy: 56.0%
- Margin MAE: 9.48 points
- Total MAE: 19.47 points

## Fair head-to-head on matched completed games

Matched games (both forecasts pre-tip): 25

| Metric | GPT challenger | Claude existing |
|---|---:|---:|
| Win log-loss (lower better) | 0.6649 | 0.6976 |
| Winner accuracy | 56.0% | 52.0% |
| Margin MAE (lower better) | 9.48 | 9.88 |
| Total MAE (lower better) | 19.47 | 19.20 |

For a fair head-to-head, compare the same completed games, forecast lead times, and consistent pregame injury/lineup information. This report is informational, not a betting recommendation.
