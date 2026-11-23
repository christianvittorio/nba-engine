# GPT challenger forecasts — 2026-11-24

Model: gpt-stat-v1.0. **Independent baseline** using historic game results; it does not use Claude's ratings, simulation outputs or player predictions.
Source: completed games in the shared SQLite archives; upcoming schedule from ESPN's unofficial feed.
Each new forecast is saved only before its game starts and is never replaced.
No player predictions or betting edges are claimed by this first release.

Found 3 scheduled games; skipped 0 already tipped-off games; GPT pregame forecasts for this date: 3.

| Game | GPT predicted score | GPT win probability | GPT total | Claude predicted score | Claude win probability |
|---|---:|---:|---:|---:|---:|
| DET @ ORL | 114-111 | 36.9% home | 224.6 | — | — home |
| BOS @ WAS | 115-108 | 25.4% home | 222.6 | — | — home |
| DAL @ DEN | 111-117 | 71.1% home | 228.1 | — | — home |

## GPT performance on completed, timestamp-validated forecasts

- Graded games: 12
- Win Brier score: 0.2385
- Win log-loss: 0.6707
- Winner accuracy: 58.3%
- Margin MAE: 7.66 points
- Total MAE: 25.14 points

## Fair head-to-head on matched completed games

Matched games (both forecasts pre-tip): 12

| Metric | GPT challenger | Claude existing |
|---|---:|---:|
| Win log-loss (lower better) | 0.6707 | 0.7264 |
| Winner accuracy | 58.3% | 50.0% |
| Margin MAE (lower better) | 7.66 | 8.86 |
| Total MAE (lower better) | 25.14 | 22.30 |

For a fair head-to-head, compare the same completed games, forecast lead times, and consistent pregame injury/lineup information. This report is informational, not a betting recommendation.
