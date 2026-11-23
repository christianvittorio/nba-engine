# GPT challenger forecasts — 2026-11-23

Model: gpt-stat-v1.0. **Independent baseline** using historic game results; it does not use Claude's ratings, simulation outputs or player predictions.
Source: completed games in the shared SQLite archives; upcoming schedule from ESPN's unofficial feed.
Each new forecast is saved only before its game starts and is never replaced.
No player predictions or betting edges are claimed by this first release.

Found 10 scheduled games; skipped 0 already tipped-off games; GPT pregame forecasts for this date: 10.

| Game | GPT predicted score | GPT win probability | GPT total | Claude predicted score | Claude win probability |
|---|---:|---:|---:|---:|---:|
| MEM @ CHA | 112-112 | 51.5% home | 224.5 | 110-112 | 52.9% home |
| POR @ PHI | 113-115 | 55.5% home | 227.9 | 113-113 | 51.7% home |
| OKC @ IND | 116-110 | 27.7% home | 225.8 | 117-108 | 26.5% home |
| MIL @ TOR | 110-117 | 75.4% home | 227.2 | 105-115 | 75.4% home |
| BKN @ MIN | 108-118 | 82.4% home | 225.9 | 102-116 | 84.8% home |
| CLE @ CHI | 118-115 | 36.6% home | 232.6 | 123-116 | 34.0% home |
| PHX @ NOP | 117-113 | 37.7% home | 229.8 | 115-112 | 40.3% home |
| LAC @ HOU | 110-118 | 76.4% home | 228.2 | 107-114 | 68.8% home |
| UTA @ LAL | 109-119 | 80.0% home | 228.1 | 110-121 | 78.5% home |
| SAS @ SAC | 118-107 | 17.7% home | 225.1 | 119-105 | 15.0% home |

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
