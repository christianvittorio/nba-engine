# GPT v2 — daily human-readable GitHub reports

GPT v2 reports are separate from Claude and GPT v1. They use independently
simulated possession/game/player results, earlier completed NBA games,
and only timestamp-valid pregame ESPN injury/roster observations.

## Where to find the dated reports

- gpt_engine/v2/artifacts/reports/daily_YYYY-MM-DD.md
- gpt_engine/v2/artifacts/reports/YYYY-MM-DD_game-nba-<id>.json
- gpt_engine/v2/artifacts/forecast_log.jsonl

The Markdown contains a slate overview, predicted score and win odds,
expected total, Manila tip-off time, simulation intervals, source injuries,
prior-five record, three-season venue/rest situational records, and top
projected player minutes, PTS, REB, AST, 3PM and TOV.

## Automatic GitHub Actions workflow

See .github/workflows/gpt-v2-daily-report.yml.

Scheduled daily at 10:30 and 17:30 UTC, plus 22:30 UTC on weekdays.
Also supports a manual workflow dispatch with Eastern date and sample count.
Builds its own historical SQLite, runs at least 50 (default 1,000)
independent Monte Carlo draws per future game, then commits reports.
Does not overwrite original game simulations or Claude's reports.

Run locally:

    python -m pip install -r gpt_engine/v2/requirements-test.txt
    python -m gpt_engine.v2.ingest --seasons 2024 2025 2026 2027 --output /tmp/gpt-v2.sqlite
    python -m gpt_engine.v2.daily_publish --db /tmp/gpt-v2.sqlite --n 1000

## Interpret with caution

Full possession-model win odds and player projections remain UNCALIBRATED
research predictions, not sportsbook betting advice. Prior-game situational
records describe the past and are not automatic changes to win probabilities.
ESPN roster entries are NOT confirmed starters. Unknown playing time is
labeled uncertain. If no valid pretip source evidence exists, the game is
skipped or the report explicitly states that none was predicted.

Predictions are first-issued and append-only per game/model version.
Repeated runs may add not-yet-forecast games, but never overwrite an earlier
pretip prediction with updated injuries or postgame information.
Later injury-sensitive forecast revisions would require a separate
versioned ledger that also preserves the initial prediction.
