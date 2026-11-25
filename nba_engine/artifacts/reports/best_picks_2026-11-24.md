# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-25T04:48:04Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jayson Tatum (BOS) OVER 0.5 Steals | -245 (DraftKings via ESPN) | 0.9 | 67% | 67% | -0.06 |
| Zaccharie Risacher (DAL) OVER 0.5 3-pointers made | -238 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| John Collins (DET) UNDER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |

**Combined probability 27.3%; parlay pays 3.0x; expected profit per 1 staked -0.17.**

Safest 3-leg slate parlay: Jayson Tatum (BOS) OVER 0.5 Steals (67%); Zaccharie Risacher (DAL) OVER 0.5 3-pointers made (66%); John Collins (DET) UNDER 1.5 3-pointers made (62%). Combined probability 27.3%; parlay pays 3.0x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -137 (DraftKings via ESPN) | 5.2 | 72% | 54% | +0.24 |
| Hugo Gonzalez (BOS) UNDER 5.5 Points | -122 (DraftKings via ESPN) | 4.7 | 66% | 52% | +0.20 |

Combined probability 47.2%; parlay pays 3.1x; expected profit per 1 staked +0.49.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -137 (DraftKings via ESPN) | 5.2 | 72% | 54% | +0.24 |
| Hugo Gonzalez (BOS) UNDER 5.5 Points | -122 (DraftKings via ESPN) | 4.7 | 66% | 52% | +0.20 |
| Cooper Flagg (DAL) UNDER 6.5 Assists | -127 (DraftKings via ESPN) | 5.5 | 67% | 52% | +0.19 |

Combined probability 31.5%; parlay pays 5.6x; expected profit per 1 staked +0.77.

Top single picks by model edge:

- Franz Wagner (ORL) UNDER 6.5 Assists: model 72% vs book 54%, EV +0.24 at -137 (projection 5.2)
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: model 74% vs book 58%, EV +0.20 at -161 (projection 2.5)
- Hugo Gonzalez (BOS) UNDER 5.5 Points: model 66% vs book 52%, EV +0.20 at -122 (projection 4.7)
- Cooper Flagg (DAL) UNDER 6.5 Assists: model 67% vs book 52%, EV +0.19 at -127 (projection 5.5)
- Sam Hauser (BOS) UNDER 2.5 3-pointers made: model 68% vs book 54%, EV +0.19 at -135 (projection 1.9)
- Franz Wagner (ORL) UNDER 6.5 Rebounds: model 61% vs book 48%, EV +0.19 at -105 (projection 5.7)
- Kevin Huerter (DET) OVER 3.5 Assists: model 54% vs book 43%, EV +0.18 at +119 (projection 3.9)
- Ausar Thompson (DET) OVER 11.5 Points: model 65% vs book 53%, EV +0.17 at -126 (projection 14.5)
- Paul Reed (DET) OVER 11.5 Points: model 60% vs book 49%, EV +0.16 at -109 (projection 13.8)
- Neemias Queta (BOS) UNDER 11.5 Points: model 61% vs book 50%, EV +0.15 at -113 (projection 8.9)
- AJ Dybantsa (WAS) UNDER 2.5 Assists: model 55% vs book 45%, EV +0.15 at +110 (projection 2.5)
- Anthony Black (ORL) UNDER 4.5 Assists: model 60% vs book 49%, EV +0.15 at -110 (projection 4.0)

## DET at ORL (game 401909314)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| John Collins (DET) UNDER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| Franz Wagner (ORL) UNDER 1.5 3-pointers made | -189 (DraftKings via ESPN) | 1.4 | 61% | 61% | -0.06 |
| Tristan da Silva (ORL) UNDER 2.5 3-pointers made | -170 (DraftKings via ESPN) | 1.9 | 59% | 59% | -0.06 |

Combined probability 22.4%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- John Collins (DET) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Franz Wagner (ORL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Tristan da Silva (ORL) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -170
- Daniss Jenkins (DET) OVER 1.5 3-pointers made: 59%, EV -0.06 at -169
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: 58%, EV -0.06 at -161
- Kevin Huerter (DET) UNDER 3.5 Assists: 57%, EV -0.06 at -157
- Kevin Huerter (DET) OVER 1.5 3-pointers made: 57%, EV -0.06 at -153
- Tristan da Silva (ORL) UNDER 1.5 Assists: 56%, EV -0.06 at -151

## BOS at WAS (game 401909315)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jayson Tatum (BOS) OVER 0.5 Steals | -245 (DraftKings via ESPN) | 0.9 | 67% | 67% | -0.06 |
| Anthony Davis (WAS) OVER 0.5 Steals | -242 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Derrick White (BOS) OVER 0.5 Steals | -238 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |

Combined probability 29.2%; parlay pays 2.8x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jayson Tatum (BOS) OVER 0.5 Steals: 67%, EV -0.06 at -245
- Anthony Davis (WAS) OVER 0.5 Steals: 66%, EV -0.06 at -242
- Derrick White (BOS) OVER 0.5 Steals: 66%, EV -0.06 at -238
- Anthony Davis (WAS) UNDER 1.5 Blocks: 66%, EV -0.06 at -232
- Trae Young (WAS) UNDER 1.5 Steals: 64%, EV -0.06 at -218
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 63%, EV -0.06 at -209
- Neemias Queta (BOS) UNDER 1.5 Blocks: 62%, EV -0.06 at -198
- Payton Pritchard (BOS) OVER 1.5 3-pointers made: 62%, EV -0.06 at -196

## DAL at DEN (game 401909316)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zaccharie Risacher (DAL) OVER 0.5 3-pointers made | -238 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Aaron Gordon (DEN) UNDER 2.5 Assists | -181 (DraftKings via ESPN) | 2.6 | 60% | 60% | -0.06 |
| Nikola Jokic (DEN) UNDER 1.5 3-pointers made | -179 (DraftKings via ESPN) | 1.4 | 60% | 60% | -0.06 |

Combined probability 24.0%; parlay pays 3.4x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Zaccharie Risacher (DAL) OVER 0.5 3-pointers made: 66%, EV -0.06 at -238
- Aaron Gordon (DEN) UNDER 2.5 Assists: 60%, EV -0.06 at -181
- Nikola Jokic (DEN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 59%, EV -0.06 at -170
- Daniel Gafford (DAL) OVER 1.5 Assists: 59%, EV -0.06 at -167
- Naji Marshall (DAL) OVER 2.5 Rebounds: 58%, EV -0.06 at -164
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 58%, EV -0.06 at -163
