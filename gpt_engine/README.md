# GPT Independent NBA Engine (v1)

This is a **separate, experimental team-prediction challenger**, developed independently of the existing Claude-created NBA engine. It does **not** run GPT-6 at prediction time and does **not** call any paid AI API. The code is deterministic Python and uses a separate statistical model.

## What is shared vs independent

- **Read-only shared inputs:** completed NBA scores from `nba_engine/artifacts/*.sqlite`, and the ESPN scoreboard adapter in `nba_engine/nbaengine/feed.py`. The data source is unofficial and can fail or change.
- **Independent features/model:** Elo-like team ratings with 45-point home advantage, recency-weighted team points scored/allowed, shrunk estimates, and transparent combined score and win-probability forecasts. Current weights are initial hypotheses, **not independently tuned or proven superior**.
- **Independent outputs:** `gpt_engine/artifacts/forecast_log.jsonl` (append-only, first forecast wins), `gpt_engine/artifacts/scorecard.json`, and `gpt_engine/artifacts/reports/gpt_forecasts_YYYY-MM-DD.md`.
- **Comparison only:** existing Claude `sim_mc` forecasts are read from its SQLite archive for the side-by-side report. They never feed the GPT forecast model.
- **Not included in v1:** player props, reliable injury scenarios, sportsbook odds, or profitability claims. The point is an independently scored baseline to build on.

## Run

From the repository root:

```bash
python -m pip install numpy pandas
python -m unittest discover -s gpt_engine/tests -v
python -m gpt_engine.run                       # US Eastern today + tomorrow
python -m gpt_engine.run --date 2026-11-21     # a particular US Eastern date
```

The independent GitHub Action is `.github/workflows/gpt-independent.yml`. It runs at 12:15 and 16:15 UTC, plus manually. The existing Claude jobs in `.github/workflows/daily.yml` remain unchanged. Only GPT output files are committed by the GPT workflow.

## Integrity rules

1. Every forecast is saved only if the game is still scheduled and its tip-off is later than the job timestamp.
2. The feature builder trains only on earlier completed game days. Unknown dates in the target season are discarded, preventing inadvertent same-day or future-result leakage.
3. Repeat runs never overwrite saved predictions. Historical results arriving after tip-off can score existing predictions but cannot create a retroactive forecast.
4. Predictions with no available slate are *empty*, not copied from the previous day.
5. The scorecard scores only logged forecasts whose timestamp precedes tip-off.
6. Tests run for every proposed change to the GPT code; no Claude scripts or workflow were modified.

## Next research steps

Evaluate the GPT and Claude models on identical, timestamp-eligible completed games before asserting improved accuracy. Add independent player logs, rotation and injury modeling, lead-time-matched probabilities, and proper out-of-time model selection. Pricing bets is a separate problem: even a lower forecast error than a baseline does not establish positive expected return after the sportsbook margin.
