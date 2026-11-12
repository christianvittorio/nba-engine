# Roster-change prior test (2026-11-13)

Question: does knowing who joined or left a team before the season improve early-season forecasts over Elo alone?

Method: for seasons 2023-2026, each team's roster change = (strength of the roster that played its first 10 games, using each player's prior-season minutes and value) minus (strength of last season's roster). Two player-value measures were tried: a ridge regression of game margin on minute shares, and a box-score composite per minute (shrunk by minutes played). The roster change was added to a logistic model of home wins next to the Elo gap (home advantage 45), faded out over the season (time constants of 10, 20 and 40 games). Fit on two seasons, tested on the other two, three different splits, scored on the first 25 games per team and on the whole season. Script: `scripts/roster_prior_test.py` (`METRIC=gs` for the composite).

Result: no reliable gain.
- Ridge measure: gain between -0.005 and +0.002 log-loss, coefficient changes sign between splits.
- Box-score composite: coefficient positive in all splits, but gain only -0.0004 to +0.0016 log-loss (typical +0.001).
- Typical yearly roster changes are small: the spread of the roster-change measure is about 0.06 (composite units), so the signal is weak next to game-to-game noise.

Current rosters (composite measure): Philadelphia +0.097 (the biggest gain in the league, above any team-season in the test sample, whose max was 0.13), Toronto +0.074, Denver +0.092, Utah +0.088. Applied with the fitted coefficient and a 20-game fade, Philadelphia's bump is worth roughly 1 point of margin. It would not turn Philadelphia into a blowout favourite.

Decision: not wired into the engine. Revisit if more seasons of data (or lineup data) become available.
