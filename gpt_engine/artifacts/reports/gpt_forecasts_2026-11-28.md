# GPT challenger forecasts — 2026-11-28

Model: gpt-stat-v1.0. **Independent baseline** using historic game results; it does not use Claude's ratings, simulation outputs or player predictions.
Source: completed games in the shared SQLite archives; upcoming schedule from ESPN's unofficial feed.
Each new forecast is saved only before its game starts and is never replaced.
No player predictions or betting edges are claimed by this first release.

Found 5 scheduled games; skipped 0 already tipped-off games; GPT pregame forecasts for this date: 5.

| Game | GPT predicted score | GPT win probability | GPT total | Claude predicted score | Claude win probability |
|---|---:|---:|---:|---:|---:|
| ORL @ WAS | 114-112 | 42.7% home | 225.4 | — | — home |
| BKN @ CHA | 110-115 | 70.3% home | 224.9 | — | — home |
| IND @ CHI | 114-117 | 61.4% home | 231.3 | — | — home |
| OKC @ MIL | 117-110 | 26.4% home | 227.5 | — | — home |
| PHI @ HOU | 112-116 | 65.0% home | 228.5 | — | — home |

## GPT performance on completed, timestamp-validated forecasts

- Graded games: 34
- Win Brier score: 0.2316
- Win log-loss: 0.6528
- Winner accuracy: 55.9%
- Margin MAE: 9.39 points
- Total MAE: 17.59 points

## Fair head-to-head on matched completed games

Matched games (both forecasts pre-tip): 34

| Metric | GPT challenger | Claude existing |
|---|---:|---:|
| Win log-loss (lower better) | 0.6528 | 0.6861 |
| Winner accuracy | 55.9% | 52.9% |
| Margin MAE (lower better) | 9.39 | 9.79 |
| Total MAE (lower better) | 17.59 | 16.85 |

For a fair head-to-head, compare the same completed games, forecast lead times, and consistent pregame injury/lineup information. This report is informational, not a betting recommendation.
