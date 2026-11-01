# NBA Intelligence Engine: Implementation Blueprint (v0.1)

Status legend: **[built]** implemented and run in this session, **[designed]** specified here but not implemented.

## 1. Data sources and limitations

Audited from this workspace on 2026-10-17 (egress goes through an allowlisting proxy).

| Source | Reachable? | What it gives | Limitations |
|---|---|---|---|
| FiveThirtyEight `nbaallelo.csv` (raw.githubusercontent.com) | yes | Game results 1947-2015 | Ends in 2015. Used **only** for tuning Elo hyper-parameters. |
| `shufinskiy/nba_data` play-by-play archives (public GitHub repo, cloned) | yes | stats.nba.com play-by-play, one file per season; 2021-22 to 2024-25 used | No calendar dates (games ordered by GAME_ID), no lineups/injuries/odds, box scores must be rebuilt from events. 27 of 4,920 rebuilt games do not reconcile to the final score (0.5%). Repo snapshot covers `nbastats` through 2024-25; its `cdnnba_2025` file was not inspected. |
| stats.nba.com, basketball-reference.com | **no** (proxy 403) | Official stats, injury reports, schedules | Blocked from this environment. |
| api.github.com | no (403) | n/a | n/a |
| Official injury report, odds feeds, live schedule | **not tested** | Needed for pre-game use | Required before any real 2026-27 forecast. |

Consequence: this version can backtest on four completed seasons but **cannot yet forecast upcoming 2026-27 games**, because no current rosters, injuries or schedule are reachable.

## 2. Required fields and schema [built: SQLite]

- `data_sources(name, url, retrieved_at_utc, season_coverage, sha256, reliability, limitations)`
- `games(season, game_id, seq, home, away, n_periods)` and `results(season, game_id, home_pts, away_pts, ingested_at_utc)`
- `forecasts(season, game_id, model_name, model_version, made_at_utc, data_cutoff, seed, n_sims, p_home, mean_home, mean_away, mean_margin, mean_total, p_ot, q_margin_json, q_total_json, details_json)`, unique per (game, model, version), with triggers that **abort any UPDATE or DELETE**
- `model_versions(model_name, model_version, params_json)` and `evaluations(model_name, scope, metric, value, n)`
- Per-game ingredients extracted from play-by-play (per side): FGA, FGM, 3PA, 3PM, FTA, FTM, TOV, offensive rebounds after FG misses and after last-FT misses, defensive rebounds, periods played.
- [designed] `players`, `player_games(minutes, usage, box stats)`, `lineups`, `injury_reports(published_at, status)`, `odds(book, ts, line)`.

## 3. Software architecture [built: modules; designed: services]

`nbaengine/data.py` ingestion and validation, `elo.py` baseline, `sim.py` profiles and Monte Carlo, `store.py` persistence, `backtest.py` walk-forward and metrics, `scripts/` runners. Python, NumPy, pandas, SciPy, SQLite only; nothing else was needed. [designed] FastAPI and Streamlit dashboard, PostgreSQL, scheduler.

## 4. Baseline model [built]

Margin-of-victory Elo (538 form). Hyper-parameters (K=20, home advantage 80, season carry-over 0.70) were tuned by walk-forward log loss on 1996-2015 only. Reference baseline: running home-win rate, mean margin and mean total.

## 5. Possession-level simulation [built, documented approximation]

Exponentially weighted (half-life 40 games), shrunk team offense/defense profiles give matchup rates for turnover, free-throw trip, 3PA share, 2P%, 3P%, FT%, and offensive-rebound probabilities, using side-specific league baselines for home advantage. Each simulated possession ends in a turnover, a free-throw trip, or a shot chain with offensive-rebound retries; shared per-game possession count; overtime simulated until the tie breaks. Output: win probability, mean/median/modal score, margin and total quantiles, OT probability, threshold probabilities, Monte Carlo standard error.

Known approximations: no players, minutes, fouls/bonus, and-ones, end-game fouling or fatigue; FT trips use a 2-or-3-attempt approximation. Independent possessions over-disperse margins by roughly 20% relative to real games, so a documented shrinkage (`apply_dispersion`, fitted on a held-out warm-up season) is applied; the uncalibrated raw version is stored and scored alongside it.

## 6. Player projection methodology [built, v0.4; not yet reconciled to the team simulation]

`nbaengine/players.py`. Player game logs are rebuilt from play-by-play (`players_data.py`), minutes from substitution events (validated against 240 minutes per team and final scores).

1. **Minutes**: exponentially weighted minutes (half-life 3 games, tuned on calibration data only), allocated across the active players by water-filling to the team total of 241 minutes with a 36-minute cap; empirical residual draws by minutes bucket.
2. **Rates**: per-minute rates (shots, free throws, rebounds, assists, steals, blocks, turnovers) shrunk toward league rates for the player's minutes bucket, with separate shrinkage for 3-point share, 3P%, 2P% and FT%.
3. **Availability**: the user marks who is out. Absent players' usual minutes (as a share of 240, capped at 60%) raise the remaining players' rates by a fitted coefficient per stat, and minutes are redistributed by the allocation above. Unconfirmed mode uses a fitted probability that a player does not play, by minutes bucket and recent misses.
4. **Box score draw**: negative-binomial counts given minutes; binomial shots so points, makes and attempts are consistent; a shooting-form shock (sigma 0.1) widens intervals.

Evaluated walk-forward on 2025-26 (parameters fitted on earlier data only; 26,545 confirmed-lineup player-games, 37,269 unconfirmed): points MAE 4.45 (model median) vs 4.68 for a 10-game-average baseline; 80% interval coverage 83% (points). The gain over the baseline is modest and consistent across roles. See `artifacts/player_fit_eval_log.txt`.

Not built: player totals are not constrained to the team simulation; no injury information is read automatically (Rotowire and similar sites prohibit automated access in their terms, so the user supplies availability); team strength does not yet change when stars are out (an injury-adjusted team test is the next experiment: keep it only if it improves out-of-sample log loss).

## 6b. Availability adjustment (experimental) [built, v0.5]

Question tested: does a team do worse than its rating predicts when rotation players do not play? Method: walk-forward over 2022-2026 regular seasons (6,150 games). Before each game, using only earlier information, a rating-only (Elo) margin prediction and, for each team, the players in its recent rotation pool who then did not play. Each missing player's weight is `usual minutes x max(0, quality per minute - 0.32)`, with quality a shrunk Game-Score-per-minute from the player model. The margin the Elo model got wrong was regressed on (home missing value - away missing value).

Result: coefficient -0.307 points per unit, fitted on 2023-2025 (t = -10.7), with the same sign and similar size in each season on its own (-0.27 to -0.37, t between -6 and -10). Applied to 2025-26 without refitting: margin MAE 11.47 -> 11.27 points, log loss 0.6003 -> 0.5932, Brier 0.2062 -> 0.2036. The 95% bootstrap interval of the log-loss change (-0.0175 to +0.0032) includes zero, so the evidence is encouraging but not conclusive.

Caveats: the test counted everyone who did not play (injuries plus coach decisions), while live use counts only players ESPN lists as out, an unofficial and possibly late list. It was tested on the rating-only model; the simulator version shifts the simulated margin by the same amount and is untested. Because of this the adjustment is stored as separate forecasts (`sim_mc_inj`, `elo_inj`) next to the unchanged ones, so future games can show which is better. It applies only to players in the recent rotation pool, and the shift is capped at 10 points. Adjusted forecasts are made only when a game is first forecast; games already forecast are not revised.

## 7. Backtesting methodology [built]

Single chronological pass; every forecast is written to SQLite **before** the result is ingested and state updated. Seasons: 2021-22 warm-up, 2022-23 calibration (dispersion), 2023-24 and 2024-25 evaluated (2,460 games). Metrics: Brier, log loss, accuracy, calibration bins, margin and total MAE/RMSE, 50/80/90% interval coverage, OT Brier. Comparators: constant home baseline and Elo. Not yet done: season-to-date net rating baseline, gradient-boosted model, playoffs, preseason.

## 8. Compute

Laptop-class. 2,000 simulations per game for the backtest (about 0.2 s/game); 10,000 per game is about 1 s/game, so a 15-game night takes seconds.

## 9. Complexity estimate

Built here: roughly 1,000 lines. Remaining for the full spec, rough engineering estimate: player/minutes engine 3-4 weeks, injury/lineup scenarios 1-2 weeks, ingestion of live sources 2 weeks (blocked on access), dashboard 2 weeks, season/playoff simulation 1-2 weeks, gradient-boosted/Bayesian ensemble 2-3 weeks.

## 10. Step-by-step plan

1. [built] Source audit, schema, validation, Elo baseline.
2. [built] Possession Monte Carlo, immutable store, walk-forward evaluation.
3. Obtain current-season data access (schedule, injuries, rosters); add dates for rest/back-to-back features.
4. Add benchmarks (net-rating regression, GBM) and decide by out-of-sample log loss whether the simulator earns its complexity.
5. Player minutes and box-score layer inside the simulator; injury scenario engine (conditional results, no invented probabilities).
6. Automation, dashboard, monitoring; then live, season and playoff simulation.
