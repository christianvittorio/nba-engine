# GPT v2 — sportsbook market value research lane

This component compares **actual timestamped bookmaker quotes** with
**separately supplied line-specific probability estimates**. It computes
break-even probabilities, a two-sided proportional no-vig benchmark, raw
expected return per unit wager, and conservative expected return where
a lower uncertainty bound was provided. It does **not** scrape prices,
automatically choose a sportsbook, place bets, or claim that the current
GPT v2 possession simulator has been calibrated for betting.

## How this connects to the NBA engine

1. Existing `daily_publish.py` writes immutable pre-tip per-game forecasts
   and `forecast_log.jsonl` entries. **Do not replace or rewrite these.**
2. A separate market-odds adapter (future work) captures licensed/live
   pre-tip prices with sportsbook, market identity, both sides where
   available, observed UTC timestamp and source provenance.
3. A probability adapter (future work) produces probabilities for each
   exact market/outcome/line from a calibrated and independently tested model.
   It must not silently treat research-only Monte Carlo frequencies as
   forward-validated probabilities.
4. `market_value.py` joins snapshots by game, market ID, selection,
   exact handicap/total line and player ID, then evaluates matched prices.
5. An independent follow-up evaluator must retain opening/closing odds,
   timestamped availability, final outcomes, closing-line value (CLV),
   Brier/log loss, calibration by market and time, slippage and realized
   settlement results. Never backfill historical prices with current lines.

**Why a separate file?** Initial game forecasts are immutable. Market
quotes can change many times before tip, so store them in a separate
append-only market snapshot ledger and tie each snapshot to the original
prediction ID and timestamps. Do not mix source cutoffs.

## Input contracts

A quote JSON file has `{"quotes":[...]}`; a probability file has
`{"predictions":[...]}`. Every row must include:
- `game_id`, `market_id`, `market_type`, `selection`, `tip_utc`;
- quote: `book`, `observed_at_utc`, `decimal_odds`;
- prediction: `asof_utc`, `model_version`, `probability`,
  `calibration_status`.

For handicaps/totals/props also include the **exact numeric line**.
For player props, include stable `player_id`. Use identical
`market_id` for both sides of the exact two-way contract. The
`spread` market records selection `home` at its signed line and
`away` at the opposite signed line; the `total` and `player_prop`
markets use selections `over`/`under` at the same line.
A multi-outcome or odds-boost contract must not masquerade as a
two-way moneyline contract.

Model statuses:
- `uncalibrated`: current possession simulation and other unvalidated outputs.
- `research_calibrated`: calibrated historical research challenger only.
- `forward_validated`: externally demonstrated prospective validation,
  documented with `validation_reference`. This module does not verify
  the evidence independently. Also provide `probability_lower`, a
  defensible uncertainty bound, to obtain a REVIEW signal.

### Synthetic example (NOT REAL ODDS OR PREDICTIONS)

```json
{
  "quotes": [
    {
      "game_id": "game:nba:EXAMPLE", "market_id": "example:moneyline",
      "market_type": "moneyline", "selection": "home", "line": null,
      "book": "DEMO-BOOK", "decimal_odds": 2.00,
      "tip_utc": "2026-12-01T01:00:00Z",
      "observed_at_utc": "2026-11-30T21:05:00Z"
    },
    {
      "game_id": "game:nba:EXAMPLE", "market_id": "example:moneyline",
      "market_type": "moneyline", "selection": "away", "line": null,
      "book": "DEMO-BOOK", "decimal_odds": 1.80,
      "tip_utc": "2026-12-01T01:00:00Z",
      "observed_at_utc": "2026-11-30T21:05:00Z"
    }
  ]
}
```

```json
{
  "predictions": [
    {
      "game_id": "game:nba:EXAMPLE", "market_id": "example:moneyline",
      "market_type": "moneyline", "selection": "home", "line": null,
      "model_version": "DEMO-UNVALIDATED",
      "asof_utc": "2026-11-30T21:00:00Z",
      "tip_utc": "2026-12-01T01:00:00Z",
      "probability": 0.58, "probability_lower": null,
      "calibration_status": "uncalibrated"
    }
  ]
}
```

Run with prepared JSON inputs:

```bash
python -m gpt_engine.v2.market_value --quotes /tmp/odds.json --predictions /tmp/probabilities.json --output /tmp/value.json
python -m pytest -q gpt_engine/v2/tests/test_market_value.py
```

## Interpretation and safeguards

- Decimal odds `O` imply a break-even chance of `1/O`.
- Without pushes, estimated ROI is `p_win * O - 1`. For whole-number
  spreads, totals or props that can settle as pushes (stake returned),
  **explicitly supply** `push_probability` from the same scenario model;
  estimated ROI becomes `p_win * O + p_push - 1`. If missing, an integer
  line is flagged `MISSING_PUSH_PROBABILITY` and cannot produce a review
  signal. The raw `1/O` break-even rate is **conditional on no push**;
  the unconditional win-probability threshold is `(1-p_push)/O`.
  These figures are **before** costs, slippage, tax or limit constraints.
- Two opposing quotes from **the same book, observed time, and exact
  market line** produce no-vig probabilities `(1/O_side) / sum(1/O)`.
  The no-vig baseline is not itself the true underlying probability;
  proportional de-vig is only one possible method.
- A positive raw ROI estimate is **never** promoted directly into a
  validated betting recommendation. Today's live simulator is
  uncalibrated and will show `RESEARCH_ONLY`.
- Conservative lower-bound EV credits no pushes unless uncertainty
  in push probability has itself been validated, preventing optimistic
  edge labeling.
- `REVIEW_POSITIVE_EV` requires externally documented forward validation,
  a probability lower bound, snapshot proximity and a lower-bound ROI of
  at least 2% (a research screening parameter, not a profitable strategy).
- Market quotes and predictions more than 30 minutes apart are
  `STALE_COMPARISON`; even within this window, new injury or roster news
  may invalidate comparison and needs human review.
- Do not use outcomes, closing odds or post-tip information to construct
  a pre-tip model probability. Do not grade bookmaker value performance
  until the source and time-stamped odds history are sufficient.

## Next production gates

- Select a licensed odds provider and document its sports-data rights,
  permitted caching and distribution conditions for the Philippines and
  any intended future markets.
- Map bookmaker team/player IDs, spread orientation, regulation vs OT,
  prop settlement/void rules, opening/current/closing price identity,
  and injury announcement times to canonical contracts.
- Independently validate win/spread/total/prop probability calibration,
  scoring distributions and posterior/empirical uncertainty by market.
- Record what prices were *actually available* at the forecast cutoff,
  compare CLV and outcomes, and log both paper-tracked and executable-price
  discrepancies across a meaningful prospective sample.
- Add measured net returns and risk limits only after external prospective
  validation. No automatic wagering.
