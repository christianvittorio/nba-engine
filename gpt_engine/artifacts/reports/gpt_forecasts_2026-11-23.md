# GPT challenger forecasts — 2026-11-23

Model: gpt-stat-v1.0. **Independent baseline** using historic game results; it does not use Claude's ratings, simulation outputs or player predictions.
Source: completed games in the shared SQLite archives; upcoming schedule from ESPN's unofficial feed.
Each new forecast is saved only before its game starts and is never replaced.
No player predictions or betting edges are claimed by this first release.

Found 10 scheduled games; skipped 0 already tipped-off games; GPT pregame forecasts for this date: 10.

| Game | GPT predicted score | GPT win probability | GPT total | Claude predicted score | Claude win probability |
|---|---:|---:|---:|---:|---:|
| MEM @ CHA | 112-112 | 51.5% home | 224.5 | — | — home |
| POR @ PHI | 113-115 | 55.5% home | 227.9 | — | — home |
| OKC @ IND | 116-110 | 27.7% home | 225.8 | — | — home |
| MIL @ TOR | 110-117 | 75.4% home | 227.2 | — | — home |
| BKN @ MIN | 108-118 | 82.4% home | 225.9 | — | — home |
| CLE @ CHI | 118-115 | 36.6% home | 232.6 | — | — home |
| PHX @ NOP | 117-113 | 37.7% home | 229.8 | — | — home |
| LAC @ HOU | 110-118 | 76.4% home | 228.2 | — | — home |
| UTA @ LAL | 109-119 | 80.0% home | 228.1 | — | — home |
| SAS @ SAC | 118-107 | 17.7% home | 225.1 | — | — home |

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
