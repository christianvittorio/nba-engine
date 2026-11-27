# GPT challenger forecasts — 2026-11-27

Model: gpt-stat-v1.0. **Independent baseline** using historic game results; it does not use Claude's ratings, simulation outputs or player predictions.
Source: completed games in the shared SQLite archives; upcoming schedule from ESPN's unofficial feed.
Each new forecast is saved only before its game starts and is never replaced.
No player predictions or betting edges are claimed by this first release.

Found 11 scheduled games; skipped 0 already tipped-off games; GPT pregame forecasts for this date: 11.

| Game | GPT predicted score | GPT win probability | GPT total | Claude predicted score | Claude win probability |
|---|---:|---:|---:|---:|---:|
| MIA @ NYK | 111-115 | 66.2% home | 226.2 | 109-116 | 67.5% home |
| MIL @ DET | 107-119 | 84.6% home | 226.6 | 102-117 | 86.5% home |
| PHI @ IND | 116-112 | 34.8% home | 228.6 | 116-113 | 43.3% home |
| BKN @ TOR | 110-117 | 72.8% home | 227.3 | 104-113 | 76.3% home |
| ATL @ BOS | 110-114 | 64.3% home | 223.3 | 107-113 | 65.6% home |
| MEM @ MIN | 111-115 | 66.8% home | 226.4 | 110-118 | 68.5% home |
| DAL @ PHX | 112-115 | 62.1% home | 227.0 | 110-114 | 60.6% home |
| LAL @ SAS | 111-116 | 66.2% home | 227.0 | 111-115 | 60.7% home |
| DEN @ UTA | 116-111 | 29.8% home | 227.1 | 121-113 | 28.5% home |
| NOP @ LAC | 114-116 | 60.2% home | 229.7 | 111-117 | 64.5% home |
| GSW @ POR | 110-115 | 68.1% home | 225.3 | 109-113 | 60.1% home |

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
