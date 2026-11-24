# GPT challenger forecasts — 2026-11-25

Model: gpt-stat-v1.0. **Independent baseline** using historic game results; it does not use Claude's ratings, simulation outputs or player predictions.
Source: completed games in the shared SQLite archives; upcoming schedule from ESPN's unofficial feed.
Each new forecast is saved only before its game starts and is never replaced.
No player predictions or betting edges are claimed by this first release.

Found 9 scheduled games; skipped 0 already tipped-off games; GPT pregame forecasts for this date: 9.

| Game | GPT predicted score | GPT win probability | GPT total | Claude predicted score | Claude win probability |
|---|---:|---:|---:|---:|---:|
| MIA @ PHI | 115-117 | 56.1% home | 232.3 | — | — home |
| CHI @ CHA | 112-115 | 61.8% home | 227.7 | — | — home |
| CLE @ NYK | 111-115 | 65.3% home | 225.2 | — | — home |
| MIN @ OKC | 112-113 | 53.7% home | 225.0 | — | — home |
| LAC @ MEM | 112-117 | 66.5% home | 228.8 | — | — home |
| BKN @ MIL | 114-116 | 56.6% home | 230.5 | — | — home |
| PHX @ HOU | 112-116 | 66.3% home | 228.1 | — | — home |
| SAC @ GSW | 109-116 | 73.3% home | 225.1 | — | — home |
| SAS @ POR | 114-112 | 41.7% home | 225.6 | — | — home |

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
