# NBA Intelligence Engine v0.4 (team forecasts + player projections)

What exists and has been run: data loading and validation, Elo baseline, possession-level Monte Carlo,
an immutable SQLite forecast store, and a leakage-safe walk-forward evaluation on 2,460 completed games
(2023-24 and 2024-25 regular seasons). What does not exist yet: player projections, injury scenarios,
current-season (2026-27) data, dashboard, automation. See `BLUEPRINT.md`.

## Reproduce
```
# data (as run): git clone --depth 1 https://github.com/shufinskiy/nba_data ; extract datasets/nbastats_{2021..2024}.tar.xz
#   into data/raw/pbp_extract/<year>/ ; download nbaallelo.csv from fivethirtyeight/data (nba-elo) into data/raw/
python3 scripts/tune_elo.py      # Elo hyper-parameters, 1996-2015 data only
N_SIMS=2000 python3 scripts/run_demo.py   # backtest, ~7 min; writes artifacts/nba_engine.sqlite
python3 scripts/verify.py        # leakage / immutability / reproducibility / worked example
```

## Results (2,460 games, forecasts stored before each result was ingested)
| | home_const | Elo | sim (calibrated) | sim (raw) |
|---|---|---|---|---|
| Brier | 0.2484 | 0.2143 | 0.2140 | 0.2152 |
| Log loss | 0.6899 | 0.6161 | 0.6162 | 0.6196 |
| Accuracy | 54.4% | 65.4% | 66.0% | 66.0% |
| Margin MAE | 12.53 | 11.11 | 11.12 | 11.12 |
| Total MAE | 16.03 | n/a | 14.70 | 14.83 |
| 50/80/90% margin interval coverage | 49/80/89 | 51/80/90 | 51/78/88 | 61/88/94 |

Simulator vs Elo on win probability is a statistical tie (paired log-loss difference +0.0002, SE 0.0034).
The simulator's value over Elo is the score, total and interval forecasts, not better winner picks.

## Known defects and limits
- P(overtime): simulated 2.3% vs actual 4.8%. Independent possessions under-produce late-game closeness. Not fixed.
- Raw simulated margins are about 20% too dispersed; the calibrated version applies a documented shrinkage fitted on 2022-23
  (after which final scores are no longer the exact sum of simulated events).
- Calibration: Elo is overconfident in the 0.5-0.8 band (e.g. predicted 0.75, observed 0.68); the simulator is closer there but under-confident at the extremes (predicted 0.24 vs observed 0.18 in the lowest bin).
- League scoring jumps between seasons are not predictable at season start; an online level correction handles it in-season.
- No dates in the source: rest, back-to-backs and travel are not modelled. Games are ordered by GAME_ID.
- Elo hyper-parameters were tuned on 1996-2015; simulator half-life, shrinkage priors and dispersion were set once and not tuned.
- Regular season only; no playoffs or preseason evaluation.

## Self-updating pipeline (v0.2)
`scripts/bootstrap.py` (once) -> `artifacts/state.json` (Elo, team profiles, online corrections; plain JSON).
`scripts/daily_update.py` (daily) -> ingests yesterday's finals, updates state, forecasts today's slate (immutable, once, only
before tip-off), writes `artifacts/reports/forecasts_<date>.md`, records every run (success or failure) in `runs`.
`.github/workflows/daily.yml` runs it free on GitHub Actions at 14:00 UTC and commits state, database and report back.

Tested offline only: `scripts/replay_test.py` replays all of 2025-26 (a season never used for tuning or calibration) day by day
through the same loop, including a simulated outage day and periodic state reloads. Result: 1,228 of 1,230 games forecast
(the 2 on the outage day were missed, as designed, but their results were still ingested later), 0 duplicate forecasts.

| 2025-26 replay (1,228 games) | home_const | Elo | sim (calibrated) |
|---|---|---|---|
| Log loss | 0.6873 | 0.6001 | 0.6086 |
| Brier | 0.2471 | 0.2060 | 0.2097 |
| Accuracy | 55.5% | 68.2% | 68.3% |
| Total MAE | 16.09 | n/a | 15.08 |

Elo beat the simulator on win probability here (paired log-loss difference +0.0084, SE 0.0049; the gap sits in the second half of
the season). Elo's average home-win probability was 0.598 against 0.555 actual, so its home-court term looks too high, yet it still
separated teams better. The monitor flags this; nothing is retuned automatically.

NOT verified: the live ESPN calls (`EspnFeed`). The sandbox cannot reach any live feed, so parsing was tested against fixtures built from
response fields inspected through a separate fetch tool. ESPN's JSON is unofficial: check its terms, and expect it to change without notice.
Other gaps: no injury/lineup data, no rest/travel features, ESPN gives no FG-vs-FT offensive-rebound split (2% assumed),
regular season only, nothing retrains itself.

## Dashboard
Windows: double-click `run_dashboard.bat`. Mac/Linux: `./run_dashboard.sh`. Opens in your browser (http://localhost:8501).
Tabs: Forecasts (a day's slate with a per-game margin-range chart), How accurate is it? (scorecard, rolling log loss, calibration),
Team ratings, Run status. Shows labeled demo data (the 2025-26 replay) until the first live `daily_update.py` run produces forecasts.
To update data: double-click `run_daily_update.bat` (or let the GitHub Actions workflow do it), then press "Reload data" in the sidebar.


## Player projections (v0.4)

Dashboard tab **Players**: choose a team, mark who is out, and get projected minutes and box-score lines (mean, 10-90% range, a rounded line with P(over)) for the remaining players, plus the minutes change caused by the absences. Availability is entered by you; nothing is scraped.

Rebuild the player layer: `python scripts/build_player_logs.py` then `python scripts/player_fit_eval.py` (writes `artifacts/player_state.json`, `player_fit.json`, `player_backtest.sqlite`; about 5 minutes).

Limits: player lines are not forced to sum to the team forecast; the player state is as of the end of the 2025-26 data and is **not** updated by the daily job (ESPN player box-score parsing is unverified); players who changed teams in the 2026 offseason still appear under their old team and must be marked out; rookies and new arrivals have no history.

## Making it update itself (GitHub Actions, free)

1. Create a new empty repository on github.com (private is fine).
2. Unzip this project and upload everything, including the hidden `.github` folder (GitHub's "uploading an existing file" page accepts a dragged folder; or use `git push`).
3. Repository Settings > Actions > General > Workflow permissions: choose "Read and write permissions".
4. Actions tab > "nba-daily" > Run workflow. The first run catches up on the last 21 days of results, then it runs by itself every day at 14:00 UTC and commits the new state to the repo.
5. Download `artifacts/` from the repo (or `git pull`) and run the dashboard to see live forecasts.

This has not been run against the live ESPN feed. If the first run fails, the Actions log shows the error.
