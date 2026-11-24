# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-24T20:00:05Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Anthony Davis (WAS) UNDER 1.5 Steals | -244 (DraftKings via ESPN) | 0.9 | 67% | 67% | -0.06 |
| John Collins (DET) OVER 0.5 3-pointers made | -232 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Zaccharie Risacher (DAL) OVER 0.5 3-pointers made | -228 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |

**Combined probability 28.5%; parlay pays 2.9x; expected profit per 1 staked -0.17.**

Safest 3-leg slate parlay: Anthony Davis (WAS) UNDER 1.5 Steals (67%); John Collins (DET) OVER 0.5 3-pointers made (66%); Zaccharie Risacher (DAL) OVER 0.5 3-pointers made (65%). Combined probability 28.5%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -111 (DraftKings via ESPN) | 5.2 | 72% | 49% | +0.36 |
| Hugo Gonzalez (BOS) UNDER 5.5 Points | -105 (DraftKings via ESPN) | 4.7 | 66% | 48% | +0.28 |

Combined probability 47.2%; parlay pays 3.7x; expected profit per 1 staked +0.75.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -111 (DraftKings via ESPN) | 5.2 | 72% | 49% | +0.36 |
| Hugo Gonzalez (BOS) UNDER 5.5 Points | -105 (DraftKings via ESPN) | 4.7 | 66% | 48% | +0.28 |
| Kyrie Irving (DAL) UNDER 4.5 Assists | +106 (DraftKings via ESPN) | 3.7 | 58% | 45% | +0.19 |

Combined probability 27.2%; parlay pays 7.6x; expected profit per 1 staked +1.08.

Top single picks by model edge:

- Franz Wagner (ORL) UNDER 6.5 Assists: model 72% vs book 49%, EV +0.36 at -111 (projection 5.2)
- Daniss Jenkins (DET) OVER 4.5 Assists: model 66% vs book 46%, EV +0.33 at +102 (projection 5.7)
- Hugo Gonzalez (BOS) UNDER 5.5 Points: model 66% vs book 48%, EV +0.28 at -105 (projection 4.7)
- Cade Cunningham (DET) OVER 7.5 Assists: model 69% vs book 53%, EV +0.23 at -128 (projection 8.2)
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: model 74% vs book 57%, EV +0.22 at -154 (projection 2.5)
- AJ Dybantsa (WAS) UNDER 2.5 Assists: model 55% vs book 43%, EV +0.19 at +117 (projection 2.5)
- Kyrie Irving (DAL) UNDER 4.5 Assists: model 58% vs book 45%, EV +0.19 at +106 (projection 3.7)
- Zaccharie Risacher (DAL) OVER 3.5 Rebounds: model 67% vs book 53%, EV +0.19 at -129 (projection 4.6)
- Ausar Thompson (DET) OVER 4.5 Assists: model 58% vs book 46%, EV +0.19 at +103 (projection 5.2)
- Paul Reed (DET) OVER 9.5 Points: model 66% vs book 53%, EV +0.18 at -128 (projection 12.5)
- Ausar Thompson (DET) OVER 10.5 Points: model 64% vs book 52%, EV +0.16 at -122 (projection 13.0)
- Kyrie Irving (DAL) UNDER 22.5 Points: model 60% vs book 49%, EV +0.15 at -108 (projection 18.2)

## DET at ORL (game 401909314)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| John Collins (DET) OVER 0.5 3-pointers made | -232 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Cade Cunningham (DET) OVER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.9 | 62% | 62% | -0.06 |
| Daniss Jenkins (DET) UNDER 2.5 3-pointers made | -192 (DraftKings via ESPN) | 2.0 | 62% | 62% | -0.06 |

Combined probability 25.0%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- John Collins (DET) OVER 0.5 3-pointers made: 66%, EV -0.06 at -232
- Cade Cunningham (DET) OVER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Daniss Jenkins (DET) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -192
- Franz Wagner (ORL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -182
- Tristan da Silva (ORL) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -168
- Daniss Jenkins (DET) OVER 3.5 Rebounds: 58%, EV -0.06 at -164
- Jalen Suggs (ORL) OVER 3.5 Rebounds: 58%, EV -0.06 at -159
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 57%, EV -0.06 at -155

## BOS at WAS (game 401909315)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Anthony Davis (WAS) UNDER 1.5 Steals | -244 (DraftKings via ESPN) | 0.9 | 67% | 67% | -0.06 |
| Jayson Tatum (BOS) OVER 0.5 Steals | -227 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 Steals | -213 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |

Combined probability 27.6%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Anthony Davis (WAS) UNDER 1.5 Steals: 67%, EV -0.06 at -244
- Anthony Davis (WAS) UNDER 1.5 Blocks: 66%, EV -0.06 at -235
- Jayson Tatum (BOS) OVER 0.5 Steals: 65%, EV -0.06 at -227
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 64%, EV -0.06 at -213
- Trae Young (WAS) UNDER 1.5 Steals: 64%, EV -0.06 at -211
- Derrick White (BOS) OVER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Sam Hauser (BOS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -189
- Payton Pritchard (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187

## DAL at DEN (game 401909316)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zaccharie Risacher (DAL) OVER 0.5 3-pointers made | -228 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Cameron Johnson (DEN) OVER 1.5 3-pointers made | -184 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |
| Aaron Gordon (DEN) UNDER 2.5 Assists | -182 (DraftKings via ESPN) | 2.6 | 60% | 60% | -0.06 |

Combined probability 23.9%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Zaccharie Risacher (DAL) OVER 0.5 3-pointers made: 65%, EV -0.06 at -228
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Aaron Gordon (DEN) UNDER 2.5 Assists: 60%, EV -0.06 at -182
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Naji Marshall (DAL) OVER 2.5 Rebounds: 59%, EV -0.06 at -167
- Nikola Jokic (DEN) UNDER 1.5 Steals: 58%, EV -0.07 at -164
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 58%, EV -0.06 at -162
- Nikola Jokic (DEN) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -160
