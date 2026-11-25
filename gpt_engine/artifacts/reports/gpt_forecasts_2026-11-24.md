# GPT challenger forecasts — 2026-11-24

Model: gpt-stat-v1.0. **Independent baseline** using historic game results; it does not use Claude's ratings, simulation outputs or player predictions.
Source: completed games in the shared SQLite archives; upcoming schedule from ESPN's unofficial feed.
Each new forecast is saved only before its game starts and is never replaced.
No player predictions or betting edges are claimed by this first release.

Found 2 scheduled games; skipped 0 already tipped-off games; GPT pregame forecasts for this date: 3.

| Game | GPT predicted score | GPT win probability | GPT total | Claude predicted score | Claude win probability |
|---|---:|---:|---:|---:|---:|
| DET @ ORL | 114-111 | 36.9% home | 224.6 | 111-107 | 39.5% home |
| BOS @ WAS | 115-108 | 25.4% home | 222.6 | 115-103 | 19.6% home |
| DAL @ DEN | 111-117 | 71.1% home | 228.1 | 112-120 | 71.4% home |

## GPT performance on completed, timestamp-validated forecasts

- Graded games: 22
- Win Brier score: 0.2377
- Win log-loss: 0.6649
- Winner accuracy: 54.5%
- Margin MAE: 8.62 points
- Total MAE: 19.13 points

## Fair head-to-head on matched completed games

Matched games (both forecasts pre-tip): 22

| Metric | GPT challenger | Claude existing |
|---|---:|---:|
| Win log-loss (lower better) | 0.6649 | 0.7031 |
| Winner accuracy | 54.5% | 50.0% |
| Margin MAE (lower better) | 8.62 | 9.23 |
| Total MAE (lower better) | 19.13 | 18.68 |

For a fair head-to-head, compare the same completed games, forecast lead times, and consistent pregame injury/lineup information. This report is informational, not a betting recommendation.
