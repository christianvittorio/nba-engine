# GPT challenger forecasts — 2026-11-22

Model: gpt-stat-v1.0. **Independent baseline** using historic game results; it does not use Claude's ratings, simulation outputs or player predictions.
Source: completed games in the shared SQLite archives; upcoming schedule from ESPN's unofficial feed.
Each new forecast is saved only before its game starts and is never replaced.
No player predictions or betting edges are claimed by this first release.

Found 7 scheduled games; skipped 0 already tipped-off games; GPT pregame forecasts for this date: 7.

| Game | GPT predicted score | GPT win probability | GPT total | Claude predicted score | Claude win probability |
|---|---:|---:|---:|---:|---:|
| DET @ ATL | 114-113 | 45.5% home | 227.9 | 114-112 | 43.4% home |
| OKC @ MIA | 115-114 | 46.3% home | 229.7 | 117-113 | 39.0% home |
| ORL @ WAS | 115-112 | 37.1% home | 226.6 | 115-109 | 35.4% home |
| DEN @ CHI | 117-113 | 32.8% home | 230.3 | 122-115 | 32.4% home |
| DAL @ UTA | 114-112 | 44.9% home | 226.0 | 117-115 | 45.4% home |
| IND @ NYK | 107-117 | 80.7% home | 223.6 | 104-115 | 79.4% home |
| BOS @ GSW | 114-110 | 34.4% home | 224.1 | 110-105 | 35.3% home |

## GPT performance on completed, timestamp-validated forecasts

- Graded games: 5
- Win Brier score: 0.2208
- Win log-loss: 0.6448
- Winner accuracy: 80.0%
- Margin MAE: 7.34 points
- Total MAE: 26.71 points

## Fair head-to-head on matched completed games

Matched games (both forecasts pre-tip): 5

| Metric | GPT challenger | Claude existing |
|---|---:|---:|
| Win log-loss (lower better) | 0.6448 | 0.7267 |
| Winner accuracy | 80.0% | 60.0% |
| Margin MAE (lower better) | 7.34 | 8.25 |
| Total MAE (lower better) | 26.71 | 25.08 |

For a fair head-to-head, compare the same completed games, forecast lead times, and consistent pregame injury/lineup information. This report is informational, not a betting recommendation.
