# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-21T21:16:28Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jrue Holiday (POR) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Devin Vassell (SAS) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Joel Embiid (PHI) OVER 0.5 3-pointers made | -229 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |

**Combined probability 18.9%; parlay pays 4.1x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Jrue Holiday (POR) UNDER 1.5 Steals (66%); Kyrie Irving (DAL) UNDER 1.5 Steals (66%); Devin Vassell (SAS) UNDER 1.5 Steals (66%). Combined probability 28.9%; parlay pays 2.9x; expected profit per 1 staked -0.18.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Taylor Hendricks (MEM) UNDER 4.5 Rebounds | +111 (DraftKings via ESPN) | 3.6 | 67% | 44% | +0.41 |
| Payton Pritchard (BOS) UNDER 21.5 Points | -119 (DraftKings via ESPN) | 16.9 | 75% | 51% | +0.38 |

Combined probability 50.0%; parlay pays 3.9x; expected profit per 1 staked +0.94.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Taylor Hendricks (MEM) UNDER 4.5 Rebounds | +111 (DraftKings via ESPN) | 3.6 | 67% | 44% | +0.41 |
| Payton Pritchard (BOS) UNDER 21.5 Points | -119 (DraftKings via ESPN) | 16.9 | 75% | 51% | +0.38 |
| Tyler Herro (MIL) UNDER 19.5 Points | -106 (DraftKings via ESPN) | 16.5 | 68% | 48% | +0.32 |

Combined probability 33.9%; parlay pays 7.5x; expected profit per 1 staked +1.56.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Taylor Hendricks (MEM) UNDER 4.5 Rebounds | +111 (DraftKings via ESPN) | 3.6 | 67% | 44% | +0.41 |
| Payton Pritchard (BOS) UNDER 21.5 Points | -119 (DraftKings via ESPN) | 16.9 | 75% | 51% | +0.38 |
| Tyler Herro (MIL) UNDER 19.5 Points | -106 (DraftKings via ESPN) | 16.5 | 68% | 48% | +0.32 |
| Josh Hart (NYK) UNDER 7.5 Rebounds | -122 (DraftKings via ESPN) | 5.8 | 72% | 52% | +0.31 |

Combined probability 24.3%; parlay pays 13.7x; expected profit per 1 staked +2.34.

Top single picks by model edge:

- Taylor Hendricks (MEM) UNDER 4.5 Rebounds: model 67% vs book 44%, EV +0.41 at +111 (projection 3.6)
- Cam Spencer (MEM) OVER 5.5 Assists: model 67% vs book 45%, EV +0.40 at +109 (projection 7.1)
- Payton Pritchard (BOS) UNDER 21.5 Points: model 75% vs book 51%, EV +0.38 at -119 (projection 16.9)
- Baylor Scheierman (BOS) UNDER 1.5 3-pointers made: model 65% vs book 46%, EV +0.33 at +104 (projection 1.2)
- Sam Hauser (BOS) UNDER 2.5 3-pointers made: model 66% vs book 46%, EV +0.33 at +102 (projection 2.0)
- Tyler Herro (MIL) UNDER 19.5 Points: model 68% vs book 48%, EV +0.32 at -106 (projection 16.5)
- Josh Hart (NYK) UNDER 7.5 Rebounds: model 72% vs book 52%, EV +0.31 at -122 (projection 5.8)
- Jalen Brunson (NYK) UNDER 28.5 Points: model 67% vs book 48%, EV +0.30 at -106 (projection 25.1)
- Neemias Queta (BOS) UNDER 12.5 Points: model 65% vs book 47%, EV +0.29 at -101 (projection 9.5)
- Rui Hachimura (LAC) UNDER 14.5 Points: model 69% vs book 51%, EV +0.26 at -120 (projection 12.0)
- Max Strus (LAC) UNDER 11.5 Points: model 66% vs book 50%, EV +0.26 at -112 (projection 9.8)
- Payton Pritchard (BOS) UNDER 6.5 Assists: model 75% vs book 56%, EV +0.25 at -150 (projection 4.9)

## MIL at PHI (game 401910023)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Joel Embiid (PHI) OVER 0.5 3-pointers made | -229 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Nate Ament (MIL) UNDER 1.5 3-pointers made | -200 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -199 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |

Combined probability 25.5%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Joel Embiid (PHI) OVER 0.5 3-pointers made: 65%, EV -0.06 at -229
- Nate Ament (MIL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -200
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -199
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -182
- Anfernee Simons (PHI) UNDER 2.5 Rebounds: 60%, EV -0.06 at -180
- VJ Edgecombe (PHI) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 59%, EV -0.07 at -171

## POR at NYK (game 401910024)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jrue Holiday (POR) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Toumani Camara (POR) UNDER 1.5 Steals | -219 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Sidy Cissoko (POR) UNDER 1.5 3-pointers made | -204 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jrue Holiday (POR) UNDER 1.5 Steals: 66%, EV -0.06 at -243
- Toumani Camara (POR) UNDER 1.5 Steals: 64%, EV -0.06 at -219
- Sidy Cissoko (POR) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -204
- Sidy Cissoko (POR) OVER 1.5 Assists: 61%, EV -0.06 at -183
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -182
- Josh Hart (NYK) UNDER 1.5 Steals: 60%, EV -0.06 at -178
- Damian Lillard (POR) UNDER 3.5 3-pointers made: 60%, EV -0.06 at -174
- Jrue Holiday (POR) OVER 1.5 3-pointers made: 58%, EV -0.06 at -164

## LAC at DAL (game 401910025)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Keaton Wagler (LAC) UNDER 1.5 3-pointers made | -222 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -210 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |

Combined probability 27.2%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Kyrie Irving (DAL) UNDER 1.5 Steals: 66%, EV -0.06 at -239
- Keaton Wagler (LAC) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -222
- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 64%, EV -0.06 at -210
- Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -199
- Brook Lopez (LAC) UNDER 2.5 Assists: 61%, EV -0.06 at -190
- Max Strus (LAC) UNDER 3.5 Assists: 59%, EV -0.06 at -173
- Kris Dunn (LAC) OVER 2.5 Assists: 58%, EV -0.06 at -165
- Max Strus (LAC) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -164

## MEM at MIN (game 401910026)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) UNDER 1.5 Steals | -195 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| Taylor Hendricks (MEM) UNDER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 1.0 | 61% | 61% | -0.06 |
| Ayo Dosunmu (MIN) UNDER 2.5 3-pointers made | -185 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |

Combined probability 23.1%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Cedric Coward (MEM) UNDER 1.5 Steals: 62%, EV -0.06 at -195
- Taylor Hendricks (MEM) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Cedric Coward (MEM) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Ayo Dosunmu (MIN) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- Jaden McDaniels (MIN) UNDER 3.5 Assists: 59%, EV -0.06 at -168
- Cam Spencer (MEM) OVER 2.5 Rebounds: 59%, EV -0.06 at -166
- Terrence Shannon Jr. (MIN) OVER 2.5 Rebounds: 57%, EV -0.06 at -158
- Jaylen Wells (MEM) UNDER 3.5 Rebounds: 57%, EV -0.06 at -156

## NOP at SAS (game 401910027)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Devin Vassell (SAS) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Jeremiah Fears (NOP) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| De'Aaron Fox (SAS) OVER 0.5 Steals | -235 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |

Combined probability 28.6%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Devin Vassell (SAS) UNDER 1.5 Steals: 66%, EV -0.06 at -236
- Jeremiah Fears (NOP) OVER 0.5 Steals: 66%, EV -0.06 at -236
- De'Aaron Fox (SAS) OVER 0.5 Steals: 66%, EV -0.06 at -235
- Victor Wembanyama (SAS) OVER 0.5 Steals: 66%, EV -0.06 at -234
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -200
- Victor Wembanyama (SAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -188
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Herbert Jones (NOP) UNDER 2.5 Assists: 60%, EV -0.06 at -175

## BOS at SAC (game 401910028)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zach LaVine (SAC) UNDER 3.5 Rebounds | -174 (DraftKings via ESPN) | 2.8 | 60% | 60% | -0.06 |
| Payton Pritchard (BOS) OVER 2.5 3-pointers made | -174 (DraftKings via ESPN) | 2.8 | 59% | 59% | -0.06 |
| Sam Hauser (BOS) UNDER 4.5 Rebounds | -160 (DraftKings via ESPN) | 2.8 | 58% | 58% | -0.06 |

Combined probability 20.4%; parlay pays 4.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Zach LaVine (SAC) UNDER 3.5 Rebounds: 60%, EV -0.06 at -174
- Payton Pritchard (BOS) OVER 2.5 3-pointers made: 59%, EV -0.06 at -174
- Sam Hauser (BOS) UNDER 4.5 Rebounds: 58%, EV -0.06 at -160
- Darius Acuff Jr. (SAC) OVER 2.5 3-pointers made: 57%, EV -0.06 at -156
- Domantas Sabonis (SAC) OVER 4.5 Assists: 57%, EV -0.06 at -155
- Darius Acuff Jr. (SAC) OVER 5.5 Assists: 56%, EV -0.06 at -151
- Payton Pritchard (BOS) UNDER 6.5 Assists: 56%, EV -0.06 at -150
- Baylor Scheierman (BOS) UNDER 5.5 Rebounds: 56%, EV -0.06 at -148
