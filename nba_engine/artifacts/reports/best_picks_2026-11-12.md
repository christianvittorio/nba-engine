# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-12T21:19:05Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 1.5 Steals | -244 (DraftKings via ESPN) | 1.0 | 67% | 67% | -0.06 |
| Dean Wade (PHI) UNDER 1.5 3-pointers made | -237 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| John Collins (DET) OVER 0.5 3-pointers made | -232 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Collin Gillespie (PHX) OVER 0.5 Steals | -216 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

**Combined probability 18.5%; parlay pays 4.2x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Kyrie Irving (DAL) UNDER 1.5 Steals (67%); Dean Wade (PHI) UNDER 1.5 3-pointers made (66%); John Collins (DET) OVER 0.5 3-pointers made (66%). Combined probability 28.8%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 2.5 3-pointers made | +122 (DraftKings via ESPN) | 1.9 | 62% | 42% | +0.37 |
| Ryan Kalkbrenner (CHA) OVER 4.5 Rebounds | -107 (DraftKings via ESPN) | 5.7 | 67% | 48% | +0.30 |

Combined probability 41.3%; parlay pays 4.3x; expected profit per 1 staked +0.78.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 2.5 3-pointers made | +122 (DraftKings via ESPN) | 1.9 | 62% | 42% | +0.37 |
| Ryan Kalkbrenner (CHA) OVER 4.5 Rebounds | -107 (DraftKings via ESPN) | 5.7 | 67% | 48% | +0.30 |
| Tyrese Maxey (PHI) UNDER 5.5 Assists | +112 (DraftKings via ESPN) | 4.9 | 61% | 44% | +0.29 |

Combined probability 25.2%; parlay pays 9.1x; expected profit per 1 staked +1.30.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 2.5 3-pointers made | +122 (DraftKings via ESPN) | 1.9 | 62% | 42% | +0.37 |
| Ryan Kalkbrenner (CHA) OVER 4.5 Rebounds | -107 (DraftKings via ESPN) | 5.7 | 67% | 48% | +0.30 |
| Tyrese Maxey (PHI) UNDER 5.5 Assists | +112 (DraftKings via ESPN) | 4.9 | 61% | 44% | +0.29 |
| Trae Young (WAS) UNDER 7.5 Assists | +112 (DraftKings via ESPN) | 6.8 | 60% | 44% | +0.26 |

Combined probability 15.0%; parlay pays 19.3x; expected profit per 1 staked +1.90.

Top single picks by model edge:

- Kyrie Irving (DAL) UNDER 2.5 3-pointers made: model 62% vs book 42%, EV +0.37 at +122 (projection 1.9)
- Ryan Kalkbrenner (CHA) OVER 4.5 Rebounds: model 67% vs book 48%, EV +0.30 at -107 (projection 5.7)
- Tyrese Maxey (PHI) UNDER 5.5 Assists: model 61% vs book 44%, EV +0.29 at +112 (projection 4.9)
- Cooper Flagg (DAL) UNDER 5.5 Assists: model 62% vs book 45%, EV +0.29 at +110 (projection 4.9)
- Trae Young (WAS) UNDER 7.5 Assists: model 60% vs book 44%, EV +0.26 at +112 (projection 6.8)
- Cade Cunningham (DET) UNDER 25.5 Points: model 70% vs book 52%, EV +0.26 at -124 (projection 21.8)
- Jonathan Kuminga (MIN) OVER 2.5 Assists: model 60% vs book 45%, EV +0.25 at +110 (projection 3.1)
- Tyrese Maxey (PHI) UNDER 25.5 Points: model 64% vs book 49%, EV +0.23 at -110 (projection 22.7)
- Anfernee Simons (PHI) UNDER 10.5 Points: model 64% vs book 50%, EV +0.21 at -111 (projection 9.2)
- Oso Ighodaro (PHX) UNDER 6.5 Points: model 66% vs book 52%, EV +0.21 at -121 (projection 5.6)
- P.J. Washington (DAL) UNDER 1.5 3-pointers made: model 56% vs book 44%, EV +0.21 at +114 (projection 1.5)
- Grayson Allen (CHA) UNDER 4.5 Assists: model 67% vs book 52%, EV +0.21 at -125 (projection 3.7)

## TOR at PHI (game 401909976)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dean Wade (PHI) UNDER 1.5 3-pointers made | -237 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Ja'Kobe Walter (TOR) UNDER 1.5 Steals | -214 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Jamal Shead (TOR) OVER 0.5 3-pointers made | -212 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dean Wade (PHI) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -237
- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 64%, EV -0.06 at -214
- Jamal Shead (TOR) OVER 0.5 3-pointers made: 64%, EV -0.06 at -212
- VJ Edgecombe (PHI) UNDER 1.5 Steals: 64%, EV -0.06 at -211
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 62%, EV -0.06 at -197
- Jakob Poeltl (TOR) UNDER 2.5 Assists: 61%, EV -0.06 at -183
- Collin Murray-Boyles (TOR) OVER 1.5 Assists: 60%, EV -0.06 at -181
- Anfernee Simons (PHI) OVER 1.5 3-pointers made: 60%, EV -0.06 at -180

## DET at WAS (game 401909977)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| John Collins (DET) OVER 0.5 3-pointers made | -232 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -215 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Alex Sarr (WAS) UNDER 1.5 Blocks | -191 (DraftKings via ESPN) | 1.4 | 61% | 61% | -0.06 |

Combined probability 25.8%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- John Collins (DET) OVER 0.5 3-pointers made: 66%, EV -0.06 at -232
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -215
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 62%, EV -0.06 at -199
- Alex Sarr (WAS) UNDER 1.5 Blocks: 61%, EV -0.06 at -191
- Trae Young (WAS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -188
- Cade Cunningham (DET) UNDER 1.5 Steals: 60%, EV -0.06 at -179
- John Collins (DET) UNDER 1.5 Assists: 60%, EV -0.06 at -177
- Kyshawn George (WAS) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177

## DAL at MIN (game 401909978)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 1.5 Steals | -244 (DraftKings via ESPN) | 1.0 | 67% | 67% | -0.06 |
| Rudy Gobert (MIN) UNDER 1.5 Blocks | -217 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Trey Lyles (MIN) OVER 0.5 3-pointers made | -206 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 27.0%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Kyrie Irving (DAL) UNDER 1.5 Steals: 67%, EV -0.06 at -244
- Rudy Gobert (MIN) UNDER 1.5 Blocks: 64%, EV -0.06 at -217
- Trey Lyles (MIN) OVER 0.5 3-pointers made: 63%, EV -0.06 at -206
- P.J. Washington (DAL) OVER 0.5 Blocks: 63%, EV -0.06 at -203
- Caleb Martin (DAL) UNDER 0.5 3-pointers made: 61%, EV -0.06 at -183
- Cooper Flagg (DAL) UNDER 1.5 Steals: 60%, EV -0.06 at -180
- Cooper Flagg (DAL) OVER 0.5 Blocks: 60%, EV -0.06 at -179
- Naji Marshall (DAL) UNDER 3.5 Rebounds: 59%, EV -0.06 at -171

## CHA at PHX (game 401909979)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Collin Gillespie (PHX) OVER 0.5 Steals | -216 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Dillon Brooks (PHX) OVER 1.5 Assists | -175 (DraftKings via ESPN) | 1.7 | 60% | 60% | -0.06 |
| Devin Booker (PHX) UNDER 3.5 Rebounds | -172 (DraftKings via ESPN) | 3.0 | 59% | 59% | -0.06 |

Combined probability 22.6%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Collin Gillespie (PHX) OVER 0.5 Steals: 64%, EV -0.06 at -216
- Dillon Brooks (PHX) OVER 1.5 Assists: 60%, EV -0.06 at -175
- Collin Gillespie (PHX) OVER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Devin Booker (PHX) UNDER 3.5 Rebounds: 59%, EV -0.06 at -172
- Jalen Green (PHX) OVER 2.5 Assists: 59%, EV -0.06 at -169
- Devin Booker (PHX) OVER 1.5 3-pointers made: 59%, EV -0.06 at -166
- Oso Ighodaro (PHX) UNDER 2.5 Assists: 58%, EV -0.06 at -163
- Grayson Allen (CHA) UNDER 3.5 Rebounds: 58%, EV -0.06 at -160
