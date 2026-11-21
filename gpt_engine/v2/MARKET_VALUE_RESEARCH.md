# GPT v2 — sportsbook market value research lane

## FREE default: no paid API needed (added November 21, 2026)

The NBA Engine's **default odds workflow now uses HoopsAPI's permanent
€0 Free tier**. Published offer (November 21, 2026): 10 API requests
per rolling day, NBA moneylines/spreads/totals, bookmaker refresh
roughly every 10 minutes, no credit card. The free API key requires
a one-time **free account registration**; it cannot be obtained or
invented by this project. Configure the GitHub Actions secret
`HOOPSAPI_KEY` or an environment variable with the same name.
**We do not call any paid API in the default workflow.**

### Five bookmakers available without payment

- FanDuel
- 1xBet
- Betway
- Pinnacle
- Unibet

Other books (Smarkets/Cloudbet) may appear if the provider's actual
response contains them. **Stake, MelBet and bet365 are NOT part of this
free provider feed.** The original requested five-book board can still
show those names but leaves their cells missing, never substituting
another sportsbook's prices. A separate five-book **free-provider**
board lists the five above when they have valid pretip quotations.

### Free API setup (no credit card)

1. Open https://hoopsapi.com/sign-up and obtain a free account/API key.
2. In the GitHub repo open **Settings → Secrets and variables → Actions**.
3. Create a repository secret named `HOOPSAPI_KEY` with that key.
4. After this PR passes tests and is merged, the existing pretip daily
   schedule calls the free API once per run (up to 3 scheduled requests
   on weekdays; below the published free quota).
5. Alternatively, run locally using environment `HOOPSAPI_KEY` and:

```bash
python -m gpt_engine.v2.hoopsapi_free \
  --nba-db /tmp/gpt-v2-daily.sqlite \
  --ledger /tmp/gpt-v2-odds-log.jsonl \
  --report /tmp/gpt-v2-free-odds-capture.json
```

The program rejects provider prices retrieved after tip, validates
per-book `captured_at` timestamps, matches actual official NBA
team IDs/tips in the warehouse, preserves exact decimal market prices
and applies the same no-lookahead EV gates as the paid prototype.

Offline mode uses an original API response (JSON with `games` array)
and its REAL retrieval timestamp:

```bash
python -m gpt_engine.v2.hoopsapi_free \
  --nba-db /tmp/gpt-v2-daily.sqlite \
  --source-json /tmp/captured_hoopsapi_response.json \
  --retrieved-at-utc 2026-11-21T20:05:00Z \
  --ledger /tmp/frozen_free_odds.jsonl \
  --report /tmp/free_odds_report.json
```

Use the `--book-set free` option to produce the free five-book
side-by-side report from `five_book_board.py`:

```bash
python -m gpt_engine.v2.five_book_board \
  --asof-report /tmp/gpt-v2-market-asof-latest.json \
  --book-set free \
  --output-json /tmp/gpt-v2-free-five-book.json \
  --output-md /tmp/gpt-v2-free-five-book.md
```

No actual authenticated HoopsAPI request or CI smoke run has yet
been verified here. Free-tier use has restrictions: its Terms prohibit
raw odds redistribution and operating a competing odds aggregation
service. This pipeline is research-only, never publishes the raw
sportsbook data in the public GitHub repository, and requires license
review before any commercial product release.

Provider documentation:
- https://hoopsapi.com/leagues/nba
- https://hoopsapi.com/docs
- https://hoopsapi.com/legal/terms

---


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

## New v0.2 pipeline implementation — November 21, 2026

The research implementation now includes:
- `odds_map.py`: strict NBA team+tip canonical mapping using the existing
  `games`/`teams` warehouse tables. All 30 NBA teams are recognized by
  approved full-name/abbreviation aliases; ambiguous or swapped games are
  skipped. No player ID is guessed.
- `odds_ingest.py`: opt-in The Odds API v4 live client, source- and
  retrieval-timestamp verification, known market normalization and a
  quote-ID-keyed append-only JSONL ledger. Default markets are featured
  `h2h`, `spreads`, `totals`. Props (`player_points`,
  `player_rebounds`, `player_assists`, `player_threes`) require the
  event-specific API and an explicit provider-player-to-NBA-ID map.
- `market_run.py`: pre-cutoff quote selection, strict frozen prediction
  joining, experimental moneyline implied-return comparison, separate
  projected spread/total/player-stat point differences. **No EV is inferred
  from point means without a line-specific probability distribution.**
- `market_results.py`: source-backed, postgame warehouse outcome export.
  Only reconciled team boxscores are eligible; unresolved player
  appearances are never treated as verified DNPs.
- `market_grade.py`: after-game settlement, hypothetical paper ROI,
  per-game Brier/log loss, optional pre-specified reference-book no-vig
  comparison, and same-book same-line *actually captured pretip* CLV.
- `forward_calibration.py`: chronological Platt probability research with
  explicit artifact-issuance vs holdout-forecast chronology. Results remain
  research-only even if the historical error improves.
- A GitHub Actions CI regression suite and optional integration into the
  independent GPT v2 daily GitHub workflow.

**These new steps have not been promoted to production**, and do not
retroactively create prices or calibration that were never captured.

### Credentials and API costs

Set the GitHub repository Actions secret `THE_ODDS_API_KEY` or export the
same environment variable to use live ingestion. **Never commit the key**.
Without it, no request is made. The API uses quota-based billing; the
scheduled feature only requests NBA h2h/spreads/totals in `us` region.
Event-level prop queries require a separate explicit run and may cost more.

Official provider documentation:
- https://the-odds-api.com/liveapi/guides/v4/
- https://the-odds-api.com/terms-and-conditions.html

Provider terms presently permit derived research and analytic products
under conditions, but not resale as a competing raw odds feed. Confirm
current service terms and local legal requirements before distributing
a commercial version. Do not claim all bookmakers are available to
people in a particular country.

### End-to-end manual run

Run from repository root after building an NBA SQLite warehouse as
documented in `DAILY_REPORTS.md`. For a real API run, supply the key
through the environment and use:

```bash
python -m gpt_engine.v2.odds_ingest \
  --nba-db /tmp/gpt-v2-daily.sqlite \
  --ledger /tmp/gpt-v2-odds-log.jsonl \
  --report /tmp/odds_ingest_report.json \
  --markets h2h,spreads,totals --region us

python -m gpt_engine.v2.daily_publish \
  --db /tmp/gpt-v2-daily.sqlite --n 1000

python -m gpt_engine.v2.market_run \
  --forecast-ledger gpt_engine/v2/artifacts/forecast_log.jsonl \
  --root . \
  --odds-ledger /tmp/gpt-v2-odds-log.jsonl \
  --output-json /tmp/nba_market_asof.json \
  --output-md /tmp/nba_market_asof.md

python -m gpt_engine.v2.market_results \
  --db /tmp/gpt-v2-daily.sqlite --output /tmp/nba_verified_finals.json

python -m gpt_engine.v2.market_grade \
  --asof-report /tmp/nba_market_asof.json \
  --odds-ledger /tmp/gpt-v2-odds-log.jsonl \
  --finals-json /tmp/nba_verified_finals.json \
  --output /tmp/nba_market_grades.json
```

**Order is essential**: the odds must be fetched and locally captured
before the forecast cutoff. Historical quotes merely timestamped before
a forecast but first retrieved afterwards are ineligible at that
forecast cutoff. On repeat runs, new odds snapshots can become useful
for a later new model version, or closing-line analysis, but cannot
overwrite the original forecast or be injected into its as-of EV report.

### Offline / no-key source replay

Save a **genuinely captured** The Odds API JSON response to
`/tmp/provider_saved.json`. In offline mode, explicitly provide the
timestamp when it was actually retrieved; do not invent a capture time.

```bash
python -m gpt_engine.v2.odds_ingest \
  --source-json /tmp/provider_saved.json \
  --retrieved-at-utc 2026-11-21T20:05:00Z \
  --nba-db /tmp/gpt-v2-daily.sqlite \
  --ledger /tmp/nba_odds_test_ledger.jsonl \
  --report /tmp/nba_odds_test_report.json
```

For a stable fixture/mapped-player experiment, supply `--event-map`
with `{"events":{"<provider_event_id>":{...}}}`. Required mapped
fields: `game_id`, `home_team`, `away_team`, `tip_utc`, and
`settlement_scope:"full_game_including_ot"`. Optional `players`
maps exact provider player names to preverified canonical NBA player IDs.

### Forward model-calibration evaluation

Once there are **80 or more** independently recorded frozen forecast
outcomes with both home wins and away wins in the calibration window,
and a separate later holdout, run:

```bash
python -m gpt_engine.v2.forward_calibration \
  --forecast-ledger gpt_engine/v2/artifacts/forecast_log.jsonl \
  --root . --finals-json /tmp/nba_verified_finals.json \
  --calibration-before 2027-02-01T00:00:00Z \
  --holdout-from 2027-02-15T00:00:00Z \
  --holdout-before 2027-06-01T00:00:00Z \
  --output /tmp/nba_forward_calibration_research.json
```

Those dates illustrate the *format only*. Do not choose or change
cutoffs after seeing holdout results. A calibrator fitted retrospectively
after those holdout predictions were issued is marked **NOT
PROSPECTIVELY TRAINED**, regardless of score improvements. No automatic
deployment follows a successful historical test.

### Daily GitHub Actions behavior

The existing `gpt-v2-daily-report.yml` workflow now:
1. Builds the NBA source warehouse as before;
2. Fetches pretip odds only when a FREE `HOOPSAPI_KEY` exists
   (no money spent or odds invented on missing key);
3. Generates immutable first-issue pretip forecasts as before;
4. Publishes a *separate* model-vs-market Markdown/JSON with no EV on
   markets where the exact-line probabilities are unavailable;
5. Exports verified finals and grades captured market records for the
   **same workflow run**, writing paper-only grading output in /tmp; and
6. Pushes only the original forecast artifacts, **never** raw sportsbook
   snapshots or complete bookmaker tables to our public GitHub repository.

Scheduled runs only execute this workflow after the PR is reviewed and
merged to the default branch. Default simulation, separate Claude
reports and core model parameters are unchanged.

### Release gates still missing

- A real key and verified live provider access (none assumed).
- Forward sample sizes, locked holdout dates and reproducible evaluation
  showing calibrated probabilities outperform a market baseline after costs.
- Live exact-line spread/total/prop probabilities and their push mass;
  means or central prediction intervals alone cannot provide these.
- Timestamped lineup/availability changes and a model reforecast
  ledger that never overwrites the first issued forecast.
- Independently verified settlement/scoring, including any historical
  score-identity failures and special bookmaker prop void rules.
- Market access, country-level availability, product terms and legal review.
- GitHub Actions CI/polling smoke run verification. No success is
  claimed until actual runs are inspected.

### CRITICAL: public-repository and provider-license safeguard

`christianvittorio/nba-engine` is a **public repository**. The daily
GitHub workflow therefore keeps provider raw quotes, full per-book
comparisons and grading details in the *ephemeral runner filesystem*
(`/tmp`) and **does not commit or upload them**. Only a small
non-price summary is printed to workflow logs. A standalone user may
use a secure private local ledger, but must not `git add` that raw
provider file to the public repository.

This safety-first behavior means later scheduled runs **do not currently
share one durable odds history**. Multi-run opening/closing snapshots,
paper results and full CLV require a separately approved access-
controlled storage target and appropriate terms review. Do not
describe cross-run CLV as operating automatically yet.

If we later choose a persistent destination (e.g. a private database),
the same ingestion/compare/grade modules support reuse of the
append-only JSONL ledger without altering immutable forecasts.

### Line-specific research probabilities (new)

The default simulator's RNG and physical possession mechanics remain
unchanged. Newly issued GPT v2 forecast JSON can optionally preserve
histograms of **actual sampled score margins, full-game totals, and
individual PTS/REB/AST/3PM**; this is enabled only for new first-issue
forecasts in `research.run_day`.

`market_probabilities.py` counts win, loss and (for whole-number
lines) push outcomes at each bookmaker's **exact offered line**. The
probability is an empirical Monte Carlo frequency, **not a calibrated
market edge**. Uncertain player minutes remain conditional research.

Older immutable forecasts without these histograms are not rerun or
backfilled. The new `market_run` computes research-only EV for all
supported markets when a histogram exists; otherwise it displays point
differences only, explicitly reporting that a line-specific probability
is unavailable. `market_grade` evaluates categorical WIN/PUSH/LOSS
probability scoring without counting multiple bookmakers as
independent model predictions.


## Five named sportsbooks: FanDuel, Stake, MelBet, 1xbet, Bet365

An additional provider adapter, `odds_api_io.py`, targets Odds-API.io
v3 because its November 2026 coverage list explicitly includes all five
books in a single API. This is a **separate provider** from
`odds_ingest.py` (The Odds API). We do not blend bookmaker prices
without preserved provider provenance and timestamps.

Current requested books (case-sensitive API names):
`FanDuel,Stake,MelBet,1xbet,Bet365`.

The official /v3/events + /v3/odds/multi workflow uses up to 10
events per request, with `ML,Spread,Totals` markets. Player props
are currently supported only when explicitly mapped and available;
the v3 five-book adapter deliberately does not infer generic "Player
Props" into player/market identities.

The adapter:
- Restricts to pending NBA league events and verifies the NBA warehouse
  home/away teams and UTC tipoff, never guessing from city/date alone;
- Excludes already-live events, three-way regulation-only ML, invalid
  prices, incomplete 2-sided spread/total pairs and missing quote
  source timestamps;
- Maps source home handicap (`hdp`) and total line (`max`) into
  exact signed handicaps and totals;
- Records every named sportsbook independently, leaving absent books
  empty instead of inventing odds;
- Reuses the immutable quote ledger, frozen forecast comparison and
  research EV evaluator;
- Produces `five_book_board.py` reports with one column per sportsbook
  plus actual best available price, without mixing different markets
  or point lines.

### Live five-book data

The API key **must be supplied externally**, and is never written into
source code or GitHub commits. For local or securely deployed runs:

```bash
export ODDS_API_IO_KEY="KEY_FROM_PROVIDER"
python -m gpt_engine.v2.odds_api_io \
  --nba-db /tmp/gpt-v2-daily.sqlite \
  --ledger /tmp/gpt-v2-odds-log.jsonl \
  --report /tmp/gpt-v2-five-book-capture.json

python -m gpt_engine.v2.market_run \
  --forecast-ledger gpt_engine/v2/artifacts/forecast_log.jsonl \
  --root . \
  --odds-ledger /tmp/gpt-v2-odds-log.jsonl \
  --output-json /tmp/gpt-v2-market-asof-latest.json \
  --output-md /tmp/gpt-v2-market-asof-latest.md

python -m gpt_engine.v2.five_book_board \
  --asof-report /tmp/gpt-v2-market-asof-latest.json \
  --output-json /tmp/gpt-v2-five-book-board.json \
  --output-md /tmp/gpt-v2-five-book-board.md
```

**Historical note:** The paid five-book `odds_api_io.py` adapter
remains available as an inactive research option, but the scheduled
workflow no longer uses it or requests its key. Free `HOOPSAPI_KEY`
is now the only scheduled odds source. Price data and details stay in
/tmp, never uploaded to this public repository.

Pricing and terms, which may change, must be reviewed before subscribing:
https://docs.odds-api.io/ (5-bookmaker Starter currently advertised as
£99/month). There is no new free API key plan presently advertised.
Check each book and basketball NBA league market availability against
actual authenticated API responses; listed provider support is not
proof that every book quotes every game.

The official source references:
- https://docs.odds-api.io/quickstart
- https://docs.odds-api.io/guides/fetching-odds
- https://odds-api.io/sportsbooks/fanduel
- https://odds-api.io/sportsbooks/stake
- https://odds-api.io/sportsbooks/melbet
- https://odds-api.io/sportsbooks/1xbet
- https://odds-api.io/sportsbooks/bet365

### Offline five-book test

For a genuine saved provider response, create a JSON file containing
`{"events":[...],"odds":[...]}`, preserving the original
time of retrieval. Provide a correct, verified NBA warehouse and run:

```bash
python -m gpt_engine.v2.odds_api_io \
  --nba-db /tmp/gpt-v2-daily.sqlite \
  --fixture-json /tmp/saved_five_book_api.json \
  --retrieved-at-utc 2026-11-21T20:05:00Z \
  --ledger /tmp/five_book_offline.jsonl \
  --report /tmp/five_book_offline_report.json

python -m pytest -q \
  gpt_engine/v2/tests/test_odds_api_io.py \
  gpt_engine/v2/tests/test_five_book_board.py
```

The offline tests use **synthetic NBA game and price fixtures**. They
prove normalization and safeguards only, not that a live authenticated
five-book request succeeded, or that the model's EV is profitable.
