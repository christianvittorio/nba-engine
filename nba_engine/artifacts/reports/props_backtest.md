# Model vs real DraftKings prop lines (finished games)
25 games, 1424 prop lines with a pre-game ladder, a line and a box score.

Flat 1-unit stakes on every side where (model win prob - book no-vig prob) exceeds the threshold; 'book' rows show what betting everything blindly returns (the vig).

| Selection | Bets | Model p | Book fair p | Hit rate | Units | ROI |
|---|---|---|---|---|---|---|
| every side (blind) | 2848 | 0.500 | 0.500 | 0.500 | -185.2 | -0.065 |
| edge > 3% | 954 | 0.590 | 0.499 | 0.484 | -88.6 | -0.093 |
| edge > 3%, 52-75% sure | 749 | 0.607 | 0.515 | 0.491 | -81.6 | -0.109 |
| edge > 5% | 722 | 0.607 | 0.499 | 0.452 | -114.2 | -0.158 |
| edge > 5%, 52-75% sure | 601 | 0.614 | 0.510 | 0.459 | -94.6 | -0.157 |
| edge > 8% | 435 | 0.636 | 0.500 | 0.437 | -79.2 | -0.182 |
| edge > 8%, 52-75% sure | 377 | 0.629 | 0.502 | 0.427 | -75.6 | -0.200 |
| edge > 12% | 210 | 0.674 | 0.497 | 0.448 | -33.9 | -0.162 |
| edge > 12%, 52-75% sure | 173 | 0.652 | 0.491 | 0.416 | -34.9 | -0.202 |
| edge > 5%, OVER only | 309 | 0.587 | 0.491 | 0.440 | -50.6 | -0.164 |
| edge > 5%, UNDER only | 413 | 0.622 | 0.506 | 0.460 | -63.5 | -0.154 |

By stat (edge > 5%):

| Stat | Bets | Model p | Book fair p | Hit rate | Units | ROI |
|---|---|---|---|---|---|---|
| ast | 146 | 0.601 | 0.491 | 0.486 | -9.8 | -0.067 |
| blk | 15 | 0.586 | 0.498 | 0.400 | -5.0 | -0.334 |
| pts | 214 | 0.618 | 0.501 | 0.421 | -45.6 | -0.213 |
| reb | 179 | 0.603 | 0.498 | 0.430 | -35.4 | -0.198 |
| stl | 49 | 0.586 | 0.493 | 0.449 | -9.0 | -0.183 |
| tpm | 119 | 0.611 | 0.510 | 0.504 | -9.4 | -0.079 |

Log-loss on over outcomes: model 0.7048, book no-vig 0.6809 (lower is better).
Weight the model earns against the book (0 = trust the book, 1 = trust the model): -0.23 +- 0.15 on 1424 over-lines. Picks use max(0, this) as their blend weight.