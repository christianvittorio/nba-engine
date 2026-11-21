# NBA historical data foundation (2020 onward)

This is a **data extraction and validation pipeline**, not a prediction model. It leaves the Claude and GPT engine logic unchanged.

### Sources and scope

We use season-partitioned public NBA stats data from [llimllib/nba_data](https://github.com/llimllib/nba_data), available as Parquet at [basketball-data.billmill.org](https://basketball-data.billmill.org/nba/). The archive derives its team and player game logs from the NBA's official stats and advanced box scores. Season `2020` is **2019–20**, and `2026` is **2025–26**.

Each backfill runs for 2019–20 through 2025–26, preserving regular season **and** playoffs/play-in separately. The pandemic seasons have **1059 games (2019–20)** and **1080 games (2020–21)**, not 1230. Every full 82-game regular season from 2021–22 through 2025–26 is expected to have 1230.

### Outputs per season

- `artifacts/teams/YYYY.csv.gz`: full published team game-stat columns, actual and estimated possession counts, pace, eFG, off/def rating, 3PA rate, opponent box-score statistics, rebounds, turnovers, etc.
- `artifacts/players/YYYY.csv.gz`: full published player-game stat columns and NBA-listed seasonal position (not a guess).
- `artifacts/defense_vs_position_game/YYYY.csv.gz`: opposing player production allowed by **season roster position** for each game.
- `artifacts/defense_vs_position_season/YYYY.csv.gz`: opponent production allowed by roster position per game and per 48 position-player minutes, with sample size.
- `artifacts/player_defender_matchups/YYYY.parquet`: observed NBA player-versus-defender matchup rows from SportsDataverse, containing time, partial possessions, assists, potential assists, points and shots.
- `artifacts/tracked_defense_by_position_game/YYYY.csv.gz` and `tracked_defense_by_position_season`: actual tracked matchup-based opponent allowances by the source-listed offensive position, both raw and per 100 tracked possessions.
- `artifacts/coaches/YYYY.csv.gz`: published head/assistant coach staff by season (no fabricated within-season change dates).
- `artifacts/rosters/YYYY.csv.gz`: official historical NBA roster positions G/F/C or hybrids, used to enrich player logs.
- `artifacts/team_style_pregame/YYYY.csv.gz`: prior-20-game team shooting, pace, efficiency, opponent allowances, and other observed style metrics, shifted so the current game never enters its own features.
- `artifacts/manifest.json`: coverage, source URLs, count validation, scoring discrepancies, position quality and remaining unknowns.

A position of `F` or `G-F` remains exactly that: it is **not** silently split into PF/SF or PG/SG. These aggregates measure opponent positional box-score production; they do **not** identify the actual defender or coach's coverage scheme.

### Usage

```bash
python -m pip install duckdb pandas pytest
pytest -q data_foundation/tests
python -m data_foundation.build --seasons 2020 2021
python -m data_foundation.build --seasons 2020 2021 2022 2023 2024 2025 2026
```

The GitHub workflow `data-foundation-backfill` imports actual historical NBA data in pull requests, validating completeness and matchup feed schema, and imports all seasons on merge to main. Any incomplete season or missing team/player game ID raises an error. Data is not represented as complete until the manifest is committed by a successful run.

### What this does NOT supply

- Precise point-guard/shooting-guard/small-forward/power-forward buckets when the source reports only G/F/C or hybrids. This requires independently verified position-by-season or role classifications.
- Coach-to-game dates and tactical coverage schemes (drop/switch/zone), play-type actions; season coach names are available, and primary tracked defender matchup *assignments* exist, but should not be misconstrued as actual coverage on every possession.
- Proprietary tracking (touches, actual defender distances, shot-contest assignment).
- Point-in-time feature snapshots of corrected historical season data: for accurate historical betting backtests, the source as-of-game timestamps and injury statuses must be separately collected.

We will not invent these layers or treat a broad position aggregate as evidence that a specific defender gives up a stat. The data catalog source is public; its license and NBA/ESPN redistribution terms must be checked before commercializing this project.
