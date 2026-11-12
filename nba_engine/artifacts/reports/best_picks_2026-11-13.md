# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-12T16:29:47Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) OVER 0.5 Steals | -247 (DraftKings via ESPN) | 1.2 | 67% | 67% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -246 (DraftKings via ESPN) | 1.0 | 67% | 67% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -241 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Collin Gillespie (PHX) UNDER 2.5 3-pointers made | -182 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |

**Combined probability 17.9%; parlay pays 4.3x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Tyrese Maxey (PHI) OVER 0.5 Steals (67%); Kyrie Irving (DAL) UNDER 1.5 Steals (67%); AJ Dybantsa (WAS) UNDER 1.5 3-pointers made (66%). Combined probability 29.5%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Miles Bridges (PHX) UNDER 14.5 Points | -101 (DraftKings via ESPN) | 11.8 | 71% | 47% | +0.41 |
| Tyrese Maxey (PHI) UNDER 5.5 Assists | -105 (DraftKings via ESPN) | 4.3 | 72% | 48% | +0.40 |

Combined probability 50.9%; parlay pays 3.9x; expected profit per 1 staked +0.98.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Miles Bridges (PHX) UNDER 14.5 Points | -101 (DraftKings via ESPN) | 11.8 | 71% | 47% | +0.41 |
| Tyrese Maxey (PHI) UNDER 5.5 Assists | -105 (DraftKings via ESPN) | 4.3 | 72% | 48% | +0.40 |
| Cooper Flagg (DAL) UNDER 5.5 Assists | +108 (DraftKings via ESPN) | 4.9 | 62% | 45% | +0.28 |

Combined probability 31.3%; parlay pays 8.1x; expected profit per 1 staked +1.53.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Miles Bridges (PHX) UNDER 14.5 Points | -101 (DraftKings via ESPN) | 11.8 | 71% | 47% | +0.41 |
| Tyrese Maxey (PHI) UNDER 5.5 Assists | -105 (DraftKings via ESPN) | 4.3 | 72% | 48% | +0.40 |
| Cooper Flagg (DAL) UNDER 5.5 Assists | +108 (DraftKings via ESPN) | 4.9 | 62% | 45% | +0.28 |
| Trae Young (WAS) UNDER 7.5 Assists | +106 (DraftKings via ESPN) | 6.8 | 60% | 45% | +0.23 |

Combined probability 18.6%; parlay pays 16.6x; expected profit per 1 staked +2.10.

Top single picks by model edge:

- Miles Bridges (PHX) UNDER 14.5 Points: model 71% vs book 47%, EV +0.41 at -101 (projection 11.8)
- Tyrese Maxey (PHI) UNDER 5.5 Assists: model 72% vs book 48%, EV +0.40 at -105 (projection 4.3)
- Tyrese Maxey (PHI) UNDER 24.5 Points: model 73% vs book 49%, EV +0.40 at -110 (projection 20.2)
- Grayson Allen (CHA) UNDER 4.5 Assists: model 67% vs book 47%, EV +0.34 at +101 (projection 3.7)
- VJ Edgecombe (PHI) UNDER 13.5 Points: model 72% vs book 51%, EV +0.34 at -116 (projection 10.9)
- LeBron James (PHI) UNDER 6.5 Assists: model 70% vs book 49%, EV +0.33 at -110 (projection 5.3)
- Tyrese Maxey (PHI) UNDER 2.5 3-pointers made: model 66% vs book 47%, EV +0.32 at -101 (projection 2.0)
- Jaylen Brown (PHI) UNDER 22.5 Points: model 67% vs book 49%, EV +0.30 at -107 (projection 19.5)
- Cooper Flagg (DAL) UNDER 5.5 Assists: model 62% vs book 45%, EV +0.28 at +108 (projection 4.9)
- VJ Edgecombe (PHI) UNDER 1.5 3-pointers made: model 60% vs book 45%, EV +0.26 at +110 (projection 1.4)
- Jonathan Kuminga (MIN) OVER 2.5 Assists: model 60% vs book 44%, EV +0.26 at +111 (projection 3.1)
- Ryan Kalkbrenner (CHA) OVER 4.5 Rebounds: model 67% vs book 51%, EV +0.24 at -117 (projection 5.7)

## TOR at PHI (game 401909976)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) OVER 0.5 Steals | -247 (DraftKings via ESPN) | 1.2 | 67% | 67% | -0.06 |
| LeBron James (PHI) OVER 0.5 Steals | -246 (DraftKings via ESPN) | 1.1 | 67% | 67% | -0.06 |
| VJ Edgecombe (PHI) UNDER 1.5 Steals | -214 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |

Combined probability 28.4%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Tyrese Maxey (PHI) OVER 0.5 Steals: 67%, EV -0.06 at -247
- LeBron James (PHI) OVER 0.5 Steals: 67%, EV -0.06 at -246
- VJ Edgecombe (PHI) UNDER 1.5 Steals: 64%, EV -0.06 at -214
- Jakob Poeltl (TOR) UNDER 2.5 Assists: 60%, EV -0.06 at -178
- Ja'Kobe Walter (TOR) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -174
- RJ Barrett (TOR) OVER 3.5 Assists: 59%, EV -0.06 at -168
- VJ Edgecombe (PHI) UNDER 3.5 Assists: 58%, EV -0.06 at -164
- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 58%, EV -0.07 at -164

## DET at WAS (game 401909977)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -241 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| John Collins (DET) OVER 0.5 3-pointers made | -230 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Trae Young (WAS) OVER 1.5 3-pointers made | -189 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |

Combined probability 26.6%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -241
- John Collins (DET) OVER 0.5 3-pointers made: 65%, EV -0.06 at -230
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 65%, EV -0.06 at -225
- Trae Young (WAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Cade Cunningham (DET) UNDER 1.5 Steals: 61%, EV -0.06 at -188
- John Collins (DET) UNDER 1.5 Assists: 61%, EV -0.06 at -182
- AJ Dybantsa (WAS) UNDER 2.5 Assists: 60%, EV -0.06 at -175
- Kyshawn George (WAS) OVER 1.5 3-pointers made: 60%, EV -0.06 at -175

## DAL at MIN (game 401909978)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 1.5 Steals | -246 (DraftKings via ESPN) | 1.0 | 67% | 67% | -0.06 |
| Cooper Flagg (DAL) UNDER 1.5 Steals | -194 (DraftKings via ESPN) | 1.5 | 62% | 62% | -0.06 |
| Naji Marshall (DAL) UNDER 3.5 Rebounds | -162 (DraftKings via ESPN) | 3.4 | 58% | 58% | -0.06 |

Combined probability 23.8%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Kyrie Irving (DAL) UNDER 1.5 Steals: 67%, EV -0.06 at -246
- Cooper Flagg (DAL) UNDER 1.5 Steals: 62%, EV -0.06 at -194
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -169
- Cooper Flagg (DAL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -164
- Naji Marshall (DAL) UNDER 3.5 Rebounds: 58%, EV -0.06 at -162
- Kyrie Irving (DAL) UNDER 4.5 Assists: 57%, EV -0.06 at -159
- Jaden McDaniels (MIN) OVER 2.5 Assists: 57%, EV -0.06 at -157
- LaMelo Ball (MIN) UNDER 1.5 Steals: 57%, EV -0.06 at -154

## CHA at PHX (game 401909979)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Collin Gillespie (PHX) UNDER 2.5 3-pointers made | -182 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |
| Dillon Brooks (PHX) OVER 1.5 Assists | -168 (DraftKings via ESPN) | 1.7 | 59% | 59% | -0.06 |
| Devin Booker (PHX) UNDER 3.5 Rebounds | -161 (DraftKings via ESPN) | 3.0 | 58% | 58% | -0.06 |

Combined probability 20.6%; parlay pays 4.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Collin Gillespie (PHX) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -182
- Dillon Brooks (PHX) OVER 1.5 Assists: 59%, EV -0.06 at -168
- Collin Gillespie (PHX) UNDER 3.5 Assists: 58%, EV -0.06 at -163
- Devin Booker (PHX) UNDER 3.5 Rebounds: 58%, EV -0.06 at -161
- Jalen Green (PHX) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -157
- Sion James (CHA) OVER 2.5 Assists: 57%, EV -0.06 at -154
- Devin Booker (PHX) OVER 1.5 3-pointers made: 56%, EV -0.06 at -150
- Sion James (CHA) OVER 3.5 Rebounds: 56%, EV -0.06 at -150
