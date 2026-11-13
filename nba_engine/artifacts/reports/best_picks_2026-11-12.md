# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-13T02:27:15Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| John Collins (DET) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Dean Wade (PHI) UNDER 1.5 3-pointers made | -238 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Ryan Kalkbrenner (CHA) OVER 0.5 Blocks | -230 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |

**Combined probability 19.0%; parlay pays 4.1x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: John Collins (DET) UNDER 1.5 3-pointers made (66%); Kyrie Irving (DAL) UNDER 1.5 Steals (66%); Dean Wade (PHI) UNDER 1.5 3-pointers made (66%). Combined probability 29.1%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cooper Flagg (DAL) UNDER 5.5 Assists | +116 (DraftKings via ESPN) | 4.9 | 62% | 43% | +0.33 |
| Cade Cunningham (DET) UNDER 25.5 Points | -119 (DraftKings via ESPN) | 21.8 | 70% | 51% | +0.28 |

Combined probability 42.7%; parlay pays 4.0x; expected profit per 1 staked +0.70.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cooper Flagg (DAL) UNDER 5.5 Assists | +116 (DraftKings via ESPN) | 4.9 | 62% | 43% | +0.33 |
| Cade Cunningham (DET) UNDER 25.5 Points | -119 (DraftKings via ESPN) | 21.8 | 70% | 51% | +0.28 |
| Joel Embiid (PHI) UNDER 8.5 Rebounds | +102 (DraftKings via ESPN) | 7.4 | 62% | 46% | +0.25 |

Combined probability 26.5%; parlay pays 8.0x; expected profit per 1 staked +1.13.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cooper Flagg (DAL) UNDER 5.5 Assists | +116 (DraftKings via ESPN) | 4.9 | 62% | 43% | +0.33 |
| Cade Cunningham (DET) UNDER 25.5 Points | -119 (DraftKings via ESPN) | 21.8 | 70% | 51% | +0.28 |
| Joel Embiid (PHI) UNDER 8.5 Rebounds | +102 (DraftKings via ESPN) | 7.4 | 62% | 46% | +0.25 |
| Grayson Allen (CHA) UNDER 4.5 Assists | -119 (DraftKings via ESPN) | 3.7 | 67% | 51% | +0.23 |

Combined probability 17.8%; parlay pays 14.8x; expected profit per 1 staked +1.63.

Top single picks by model edge:

- Cooper Flagg (DAL) UNDER 5.5 Assists: model 62% vs book 43%, EV +0.33 at +116 (projection 4.9)
- Jonathan Kuminga (MIN) OVER 2.5 Assists: model 58% vs book 42%, EV +0.31 at +124 (projection 3.0)
- Cade Cunningham (DET) UNDER 25.5 Points: model 70% vs book 51%, EV +0.28 at -119 (projection 21.8)
- Kyrie Irving (DAL) UNDER 2.5 3-pointers made: model 62% vs book 46%, EV +0.26 at +105 (projection 1.9)
- Joel Embiid (PHI) UNDER 8.5 Rebounds: model 62% vs book 46%, EV +0.25 at +102 (projection 7.4)
- Grayson Allen (CHA) UNDER 4.5 Assists: model 67% vs book 51%, EV +0.23 at -119 (projection 3.7)
- Oso Ighodaro (PHX) UNDER 0.5 Steals: model 62% vs book 47%, EV +0.23 at +100 (projection 0.5)
- Oso Ighodaro (PHX) UNDER 0.5 Blocks: model 53% vs book 40%, EV +0.23 at +132 (projection 0.6)
- Naji Marshall (DAL) OVER 8.5 Points: model 66% vs book 51%, EV +0.22 at -118 (projection 11.3)
- Paul Reed (DET) OVER 6.5 Rebounds: model 59% vs book 46%, EV +0.21 at +105 (projection 7.1)
- Trae Young (WAS) UNDER 8.5 Assists: model 72% vs book 55%, EV +0.20 at -146 (projection 6.8)
- John Collins (DET) UNDER 13.5 Points: model 60% vs book 48%, EV +0.20 at -102 (projection 12.6)

## TOR at PHI (game 401909976)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dean Wade (PHI) UNDER 1.5 3-pointers made | -238 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Jamal Shead (TOR) OVER 0.5 3-pointers made | -218 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| VJ Edgecombe (PHI) UNDER 1.5 Steals | -210 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |

Combined probability 27.0%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dean Wade (PHI) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -238
- Jamal Shead (TOR) OVER 0.5 3-pointers made: 64%, EV -0.06 at -218
- VJ Edgecombe (PHI) UNDER 1.5 Steals: 64%, EV -0.06 at -210
- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 63%, EV -0.06 at -204
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 62%, EV -0.06 at -197
- RJ Barrett (TOR) OVER 3.5 Assists: 58%, EV -0.06 at -163
- Joel Embiid (PHI) OVER 0.5 3-pointers made: 57%, EV -0.06 at -156
- Ja'Kobe Walter (TOR) OVER 3.5 Rebounds: 57%, EV -0.06 at -156

## DET at WAS (game 401909977)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| John Collins (DET) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Ausar Thompson (DET) OVER 0.5 Blocks | -235 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -216 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 28.0%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- John Collins (DET) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -240
- Ausar Thompson (DET) OVER 0.5 Blocks: 66%, EV -0.06 at -235
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -216
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 63%, EV -0.06 at -203
- Alex Sarr (WAS) UNDER 1.5 Blocks: 62%, EV -0.06 at -193
- AJ Dybantsa (WAS) UNDER 2.5 Assists: 61%, EV -0.06 at -186
- Cade Cunningham (DET) UNDER 1.5 Steals: 61%, EV -0.06 at -186
- John Collins (DET) UNDER 1.5 Assists: 61%, EV -0.06 at -184

## DAL at MIN (game 401909978)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Caleb Martin (DAL) UNDER 0.5 3-pointers made | -233 (DraftKings via ESPN) | 0.4 | 66% | 66% | -0.06 |
| Trey Lyles (MIN) UNDER 1.5 Assists | -225 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |

Combined probability 28.3%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Kyrie Irving (DAL) UNDER 1.5 Steals: 66%, EV -0.06 at -241
- Caleb Martin (DAL) UNDER 0.5 3-pointers made: 66%, EV -0.06 at -233
- Trey Lyles (MIN) UNDER 1.5 Assists: 65%, EV -0.06 at -225
- Jaden McDaniels (MIN) OVER 0.5 Steals: 64%, EV -0.06 at -219
- Trey Lyles (MIN) OVER 0.5 3-pointers made: 64%, EV -0.06 at -212
- P.J. Washington (DAL) OVER 0.5 Steals: 62%, EV -0.06 at -194
- Caleb Martin (DAL) UNDER 1.5 Assists: 61%, EV -0.06 at -189
- Ayo Dosunmu (MIN) OVER 0.5 Steals: 61%, EV -0.06 at -190

## CHA at PHX (game 401909979)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ryan Kalkbrenner (CHA) OVER 0.5 Blocks | -230 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |
| Collin Gillespie (PHX) OVER 0.5 Steals | -228 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Devin Booker (PHX) UNDER 0.5 Blocks | -208 (DraftKings via ESPN) | 0.2 | 63% | 63% | -0.06 |

Combined probability 27.0%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ryan Kalkbrenner (CHA) OVER 0.5 Blocks: 65%, EV -0.06 at -230
- Collin Gillespie (PHX) OVER 0.5 Steals: 65%, EV -0.06 at -228
- Devin Booker (PHX) UNDER 0.5 Blocks: 63%, EV -0.06 at -208
- Grayson Allen (CHA) OVER 0.5 Steals: 63%, EV -0.06 at -204
- Dillon Brooks (PHX) OVER 0.5 Steals: 62%, EV -0.06 at -193
- Naz Reid (CHA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -184
- Collin Gillespie (PHX) OVER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Devin Booker (PHX) OVER 0.5 Steals: 60%, EV -0.07 at -181
