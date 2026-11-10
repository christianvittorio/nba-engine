# Model vs real DraftKings prop lines (finished games)
32 games, 1792 prop lines with a pre-game ladder, a line and a box score.

Flat 1-unit stakes on every side where (model win prob - book no-vig prob) exceeds the threshold; 'book' rows show what betting everything blindly returns (the vig).

| Selection | Bets | Model p | Book fair p | Hit rate | Units | ROI |
|---|---|---|---|---|---|---|
| every side (blind) | 3584 | 0.500 | 0.500 | 0.500 | -232.1 | -0.065 |
| edge > 3% | 1216 | 0.590 | 0.500 | 0.500 | -79.4 | -0.065 |
| edge > 3%, 52-75% sure | 964 | 0.606 | 0.515 | 0.508 | -75.7 | -0.078 |
| edge > 5% | 912 | 0.607 | 0.499 | 0.471 | -110.8 | -0.122 |
| edge > 5%, 52-75% sure | 764 | 0.613 | 0.509 | 0.482 | -88.8 | -0.116 |
| edge > 8% | 550 | 0.635 | 0.500 | 0.469 | -68.0 | -0.124 |
| edge > 8%, 52-75% sure | 476 | 0.629 | 0.502 | 0.462 | -65.5 | -0.138 |
| edge > 12% | 263 | 0.672 | 0.495 | 0.452 | -41.1 | -0.156 |
| edge > 12%, 52-75% sure | 215 | 0.651 | 0.490 | 0.428 | -39.4 | -0.183 |
| edge > 5%, OVER only | 388 | 0.586 | 0.490 | 0.461 | -48.7 | -0.126 |
| edge > 5%, UNDER only | 524 | 0.622 | 0.506 | 0.479 | -62.1 | -0.119 |

By stat (edge > 5%):

| Stat | Bets | Model p | Book fair p | Hit rate | Units | ROI |
|---|---|---|---|---|---|---|
| ast | 185 | 0.605 | 0.494 | 0.503 | -8.6 | -0.046 |
| blk | 17 | 0.596 | 0.508 | 0.471 | -3.8 | -0.225 |
| pts | 273 | 0.616 | 0.500 | 0.447 | -44.3 | -0.162 |
| reb | 228 | 0.601 | 0.499 | 0.443 | -40.4 | -0.177 |
| stl | 55 | 0.589 | 0.496 | 0.509 | -3.5 | -0.063 |
| tpm | 154 | 0.607 | 0.505 | 0.506 | -10.3 | -0.067 |

Log-loss on over outcomes: model 0.7021, book no-vig 0.6813 (lower is better).
Weight the model earns against the book (0 = trust the book, 1 = trust the model): -0.13 +- 0.13 on 1792 over-lines. Picks use max(0, this) as their blend weight.

Per-stat weight (used weight = estimate minus one standard error, floored at 0):

| Stat | Lines | Weight | SE | Used |
|---|---|---|---|---|
| ast | 324 | -0.01 | 0.29 | 0.00 |
| pts | 467 | -0.20 | 0.23 | 0.00 |
| reb | 433 | -0.50 | 0.28 | 0.00 |
| stl | 148 | 0.24 | 0.61 | 0.00 |
| tpm | 364 | 0.29 | 0.34 | 0.00 |