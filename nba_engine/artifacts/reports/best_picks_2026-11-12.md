# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-12T23:51:25Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| John Collins (DET) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Dean Wade (PHI) UNDER 1.5 3-pointers made | -237 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Trey Lyles (MIN) OVER 0.5 3-pointers made | -230 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Ryan Kalkbrenner (CHA) OVER 0.5 Blocks | -217 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |

**Combined probability 18.4%; parlay pays 4.2x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: John Collins (DET) UNDER 1.5 3-pointers made (66%); Dean Wade (PHI) UNDER 1.5 3-pointers made (66%); Trey Lyles (MIN) OVER 0.5 3-pointers made (65%). Combined probability 28.7%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jonathan Kuminga (MIN) OVER 2.5 Assists | +120 (DraftKings via ESPN) | 3.1 | 60% | 43% | +0.31 |
| Cade Cunningham (DET) UNDER 25.5 Points | -119 (DraftKings via ESPN) | 21.8 | 70% | 51% | +0.28 |

Combined probability 41.4%; parlay pays 4.0x; expected profit per 1 staked +0.67.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jonathan Kuminga (MIN) OVER 2.5 Assists | +120 (DraftKings via ESPN) | 3.1 | 60% | 43% | +0.31 |
| Cade Cunningham (DET) UNDER 25.5 Points | -119 (DraftKings via ESPN) | 21.8 | 70% | 51% | +0.28 |
| Oso Ighodaro (PHX) UNDER 0.5 Steals | +104 (DraftKings via ESPN) | 0.5 | 62% | 46% | +0.26 |

Combined probability 25.5%; parlay pays 8.3x; expected profit per 1 staked +1.10.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jonathan Kuminga (MIN) OVER 2.5 Assists | +120 (DraftKings via ESPN) | 3.1 | 60% | 43% | +0.31 |
| Cade Cunningham (DET) UNDER 25.5 Points | -119 (DraftKings via ESPN) | 21.8 | 70% | 51% | +0.28 |
| Oso Ighodaro (PHX) UNDER 0.5 Steals | +104 (DraftKings via ESPN) | 0.5 | 62% | 46% | +0.26 |
| Joel Embiid (PHI) UNDER 8.5 Rebounds | +102 (DraftKings via ESPN) | 7.4 | 62% | 46% | +0.25 |

Combined probability 15.8%; parlay pays 16.7x; expected profit per 1 staked +1.64.

Top single picks by model edge:

- Jonathan Kuminga (MIN) OVER 2.5 Assists: model 60% vs book 43%, EV +0.31 at +120 (projection 3.1)
- Cade Cunningham (DET) UNDER 25.5 Points: model 70% vs book 51%, EV +0.28 at -119 (projection 21.8)
- Kyrie Irving (DAL) UNDER 2.5 3-pointers made: model 62% vs book 46%, EV +0.26 at +104 (projection 1.9)
- Oso Ighodaro (PHX) UNDER 0.5 Steals: model 62% vs book 46%, EV +0.26 at +104 (projection 0.5)
- Joel Embiid (PHI) UNDER 8.5 Rebounds: model 62% vs book 46%, EV +0.25 at +102 (projection 7.4)
- Cooper Flagg (DAL) UNDER 6.5 Assists: model 75% vs book 56%, EV +0.25 at -149 (projection 4.9)
- Naji Marshall (DAL) OVER 8.5 Points: model 66% vs book 50%, EV +0.25 at -112 (projection 11.3)
- Trae Young (WAS) UNDER 7.5 Assists: model 60% vs book 45%, EV +0.23 at +107 (projection 6.8)
- Cooper Flagg (DAL) UNDER 24.5 Points: model 62% vs book 48%, EV +0.22 at -104 (projection 22.1)
- Grayson Allen (CHA) UNDER 4.5 Assists: model 67% vs book 52%, EV +0.21 at -125 (projection 3.7)
- Oso Ighodaro (PHX) UNDER 0.5 Blocks: model 53% vs book 41%, EV +0.20 at +127 (projection 0.6)
- Ryan Kalkbrenner (CHA) OVER 4.5 Rebounds: model 67% vs book 53%, EV +0.19 at -128 (projection 5.7)

## TOR at PHI (game 401909976)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dean Wade (PHI) UNDER 1.5 3-pointers made | -237 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Jamal Shead (TOR) OVER 0.5 3-pointers made | -218 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Ja'Kobe Walter (TOR) UNDER 1.5 Steals | -212 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

Combined probability 27.1%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dean Wade (PHI) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -237
- Jamal Shead (TOR) OVER 0.5 3-pointers made: 64%, EV -0.06 at -218
- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 64%, EV -0.06 at -212
- VJ Edgecombe (PHI) UNDER 1.5 Steals: 64%, EV -0.06 at -210
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 62%, EV -0.06 at -197
- Collin Murray-Boyles (TOR) OVER 1.5 Assists: 60%, EV -0.06 at -175
- RJ Barrett (TOR) OVER 3.5 Assists: 59%, EV -0.06 at -169
- VJ Edgecombe (PHI) UNDER 3.5 Assists: 59%, EV -0.06 at -166

## DET at WAS (game 401909977)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| John Collins (DET) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -216 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Trae Young (WAS) UNDER 2.5 3-pointers made | -187 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |

Combined probability 26.0%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- John Collins (DET) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -240
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -216
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 63%, EV -0.06 at -202
- Trae Young (WAS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -187
- Alex Sarr (WAS) UNDER 1.5 Blocks: 61%, EV -0.06 at -187
- John Collins (DET) UNDER 1.5 Assists: 61%, EV -0.06 at -184
- Kyshawn George (WAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Cade Cunningham (DET) UNDER 1.5 Steals: 60%, EV -0.07 at -180

## DAL at MIN (game 401909978)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Trey Lyles (MIN) OVER 0.5 3-pointers made | -230 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Rudy Gobert (MIN) UNDER 1.5 Blocks | -217 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Caleb Martin (DAL) UNDER 0.5 3-pointers made | -215 (DraftKings via ESPN) | 0.4 | 64% | 64% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Trey Lyles (MIN) OVER 0.5 3-pointers made: 65%, EV -0.06 at -230
- Rudy Gobert (MIN) UNDER 1.5 Blocks: 64%, EV -0.06 at -217
- Caleb Martin (DAL) UNDER 0.5 3-pointers made: 64%, EV -0.06 at -215
- Kyrie Irving (DAL) UNDER 1.5 Steals: 64%, EV -0.06 at -211
- Caleb Martin (DAL) UNDER 1.5 Assists: 62%, EV -0.06 at -191
- Jaylen Clark (MIN) UNDER 2.5 Rebounds: 60%, EV -0.06 at -179
- Daniel Gafford (DAL) UNDER 1.5 Assists: 59%, EV -0.06 at -173
- Jaden McDaniels (MIN) UNDER 3.5 Assists: 59%, EV -0.06 at -171

## CHA at PHX (game 401909979)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ryan Kalkbrenner (CHA) OVER 0.5 Blocks | -217 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |
| Devin Booker (PHX) UNDER 0.5 Blocks | -215 (DraftKings via ESPN) | 0.2 | 64% | 64% | -0.06 |
| Collin Gillespie (PHX) OVER 0.5 Steals | -213 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 26.2%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ryan Kalkbrenner (CHA) OVER 0.5 Blocks: 64%, EV -0.06 at -217
- Devin Booker (PHX) UNDER 0.5 Blocks: 64%, EV -0.06 at -215
- Collin Gillespie (PHX) OVER 0.5 Steals: 64%, EV -0.06 at -213
- Grayson Allen (CHA) OVER 0.5 Steals: 63%, EV -0.06 at -208
- Dillon Brooks (PHX) OVER 0.5 Steals: 62%, EV -0.06 at -192
- Devin Booker (PHX) OVER 0.5 Steals: 60%, EV -0.07 at -181
- Collin Gillespie (PHX) OVER 1.5 3-pointers made: 59%, EV -0.06 at -173
- Devin Booker (PHX) OVER 1.5 3-pointers made: 59%, EV -0.06 at -172
