# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-24T23:24:34Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Anthony Davis (WAS) OVER 0.5 Steals | -245 (DraftKings via ESPN) | 0.9 | 67% | 67% | -0.06 |
| John Collins (DET) UNDER 1.5 3-pointers made | -234 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Zaccharie Risacher (DAL) OVER 0.5 3-pointers made | -228 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |

**Combined probability 28.6%; parlay pays 2.9x; expected profit per 1 staked -0.17.**

Safest 3-leg slate parlay: Anthony Davis (WAS) OVER 0.5 Steals (67%); John Collins (DET) UNDER 1.5 3-pointers made (66%); Zaccharie Risacher (DAL) OVER 0.5 3-pointers made (65%). Combined probability 28.6%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -115 (DraftKings via ESPN) | 5.2 | 72% | 50% | +0.34 |
| Cooper Flagg (DAL) UNDER 6.5 Assists | -115 (DraftKings via ESPN) | 5.5 | 67% | 50% | +0.25 |

Combined probability 47.8%; parlay pays 3.5x; expected profit per 1 staked +0.67.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -115 (DraftKings via ESPN) | 5.2 | 72% | 50% | +0.34 |
| Cooper Flagg (DAL) UNDER 6.5 Assists | -115 (DraftKings via ESPN) | 5.5 | 67% | 50% | +0.25 |
| Hugo Gonzalez (BOS) UNDER 5.5 Points | -122 (DraftKings via ESPN) | 4.7 | 66% | 52% | +0.20 |

Combined probability 31.5%; parlay pays 6.4x; expected profit per 1 staked +1.00.

Top single picks by model edge:

- Franz Wagner (ORL) UNDER 6.5 Assists: model 72% vs book 50%, EV +0.34 at -115 (projection 5.2)
- Daniss Jenkins (DET) OVER 4.5 Assists: model 66% vs book 49%, EV +0.27 at -108 (projection 5.7)
- Cooper Flagg (DAL) UNDER 6.5 Assists: model 67% vs book 50%, EV +0.25 at -115 (projection 5.5)
- Kyrie Irving (DAL) UNDER 4.5 Assists: model 58% vs book 44%, EV +0.22 at +111 (projection 3.7)
- Cade Cunningham (DET) OVER 8.5 Assists: model 58% vs book 45%, EV +0.21 at +109 (projection 8.2)
- Ausar Thompson (DET) OVER 4.5 Assists: model 58% vs book 45%, EV +0.21 at +107 (projection 5.2)
- Cooper Flagg (DAL) UNDER 24.5 Points: model 62% vs book 48%, EV +0.21 at -104 (projection 22.6)
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: model 74% vs book 58%, EV +0.20 at -162 (projection 2.5)
- Zaccharie Risacher (DAL) OVER 3.5 Rebounds: model 67% vs book 52%, EV +0.20 at -126 (projection 4.6)
- Hugo Gonzalez (BOS) UNDER 5.5 Points: model 66% vs book 52%, EV +0.20 at -122 (projection 4.7)
- Paul Reed (DET) OVER 9.5 Points: model 66% vs book 52%, EV +0.20 at -125 (projection 12.5)
- Ausar Thompson (DET) OVER 10.5 Points: model 64% vs book 51%, EV +0.18 at -118 (projection 13.0)

## DET at ORL (game 401909314)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| John Collins (DET) UNDER 1.5 3-pointers made | -234 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Daniss Jenkins (DET) OVER 1.5 3-pointers made | -191 (DraftKings via ESPN) | 2.0 | 62% | 62% | -0.06 |
| Cade Cunningham (DET) OVER 1.5 3-pointers made | -188 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |

Combined probability 24.8%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- John Collins (DET) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -234
- Daniss Jenkins (DET) OVER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Cade Cunningham (DET) OVER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Franz Wagner (ORL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Tristan da Silva (ORL) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -168
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: 58%, EV -0.06 at -162
- Jalen Suggs (ORL) UNDER 4.5 Rebounds: 58%, EV -0.06 at -161
- Tristan da Silva (ORL) UNDER 1.5 Assists: 56%, EV -0.06 at -150

## BOS at WAS (game 401909315)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Anthony Davis (WAS) OVER 0.5 Steals | -245 (DraftKings via ESPN) | 0.9 | 67% | 67% | -0.06 |
| Jayson Tatum (BOS) OVER 0.5 Steals | -234 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Derrick White (BOS) OVER 0.5 Steals | -230 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 28.6%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Anthony Davis (WAS) OVER 0.5 Steals: 67%, EV -0.06 at -245
- Anthony Davis (WAS) UNDER 1.5 Blocks: 66%, EV -0.06 at -243
- Jayson Tatum (BOS) OVER 0.5 Steals: 66%, EV -0.06 at -234
- Derrick White (BOS) OVER 0.5 Steals: 65%, EV -0.06 at -230
- Trae Young (WAS) UNDER 1.5 Steals: 64%, EV -0.06 at -218
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 64%, EV -0.06 at -213
- Derrick White (BOS) OVER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Neemias Queta (BOS) UNDER 1.5 Blocks: 62%, EV -0.06 at -196

## DAL at DEN (game 401909316)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zaccharie Risacher (DAL) OVER 0.5 3-pointers made | -228 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Aaron Gordon (DEN) UNDER 2.5 Assists | -182 (DraftKings via ESPN) | 2.6 | 60% | 60% | -0.06 |
| Cameron Johnson (DEN) OVER 1.5 3-pointers made | -178 (DraftKings via ESPN) | 1.8 | 60% | 60% | -0.06 |

Combined probability 23.7%; parlay pays 3.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Zaccharie Risacher (DAL) OVER 0.5 3-pointers made: 65%, EV -0.06 at -228
- Aaron Gordon (DEN) UNDER 2.5 Assists: 60%, EV -0.06 at -182
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Naji Marshall (DAL) OVER 0.5 3-pointers made: 59%, EV -0.06 at -174
- Naji Marshall (DAL) UNDER 3.5 Rebounds: 59%, EV -0.06 at -169
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 58%, EV -0.06 at -164
- Nikola Jokic (DEN) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -164
