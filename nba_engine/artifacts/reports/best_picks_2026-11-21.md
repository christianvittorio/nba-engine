# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-21T16:39:30Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) OVER 0.5 Steals | -247 (DraftKings via ESPN) | 1.1 | 67% | 67% | -0.06 |
| Joel Embiid (PHI) OVER 0.5 3-pointers made | -240 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Toumani Camara (POR) UNDER 1.5 Steals | -228 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Keaton Wagler (LAC) UNDER 1.5 3-pointers made | -223 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |

**Combined probability 18.7%; parlay pays 4.1x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Victor Wembanyama (SAS) OVER 0.5 Steals (67%); Joel Embiid (PHI) OVER 0.5 3-pointers made (66%); Toumani Camara (POR) UNDER 1.5 Steals (65%). Combined probability 28.8%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cam Spencer (MEM) OVER 5.5 Assists | +111 (DraftKings via ESPN) | 7.1 | 68% | 44% | +0.43 |
| Tyler Herro (MIL) UNDER 20.5 Points | -122 (DraftKings via ESPN) | 16.5 | 73% | 52% | +0.33 |

Combined probability 49.4%; parlay pays 3.8x; expected profit per 1 staked +0.90.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cam Spencer (MEM) OVER 5.5 Assists | +111 (DraftKings via ESPN) | 7.1 | 68% | 44% | +0.43 |
| Tyler Herro (MIL) UNDER 20.5 Points | -122 (DraftKings via ESPN) | 16.5 | 73% | 52% | +0.33 |
| Paul George (BOS) UNDER 5.5 Rebounds | +105 (DraftKings via ESPN) | 3.9 | 64% | 46% | +0.31 |

Combined probability 31.6%; parlay pays 7.9x; expected profit per 1 staked +1.49.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cam Spencer (MEM) OVER 5.5 Assists | +111 (DraftKings via ESPN) | 7.1 | 68% | 44% | +0.43 |
| Tyler Herro (MIL) UNDER 20.5 Points | -122 (DraftKings via ESPN) | 16.5 | 73% | 52% | +0.33 |
| Paul George (BOS) UNDER 5.5 Rebounds | +105 (DraftKings via ESPN) | 3.9 | 64% | 46% | +0.31 |
| Max Strus (LAC) UNDER 11.5 Points | -110 (DraftKings via ESPN) | 9.8 | 66% | 49% | +0.27 |

Combined probability 21.0%; parlay pays 15.0x; expected profit per 1 staked +2.16.

Top single picks by model edge:

- Cam Spencer (MEM) OVER 5.5 Assists: model 68% vs book 44%, EV +0.43 at +111 (projection 7.1)
- Taylor Hendricks (MEM) UNDER 4.5 Rebounds: model 66% vs book 45%, EV +0.37 at +107 (projection 3.6)
- Tyler Herro (MIL) UNDER 20.5 Points: model 73% vs book 52%, EV +0.33 at -122 (projection 16.5)
- Paul George (BOS) UNDER 5.5 Rebounds: model 64% vs book 46%, EV +0.31 at +105 (projection 3.9)
- Max Strus (LAC) UNDER 11.5 Points: model 66% vs book 49%, EV +0.27 at -110 (projection 9.8)
- Josh Hart (NYK) UNDER 7.5 Rebounds: model 72% vs book 53%, EV +0.27 at -131 (projection 5.8)
- Jalen Brunson (NYK) UNDER 28.5 Points: model 67% vs book 50%, EV +0.26 at -113 (projection 25.1)
- Cam Spencer (MEM) OVER 10.5 Points: model 62% vs book 48%, EV +0.24 at -102 (projection 13.2)
- Rui Hachimura (LAC) UNDER 14.5 Points: model 69% vs book 53%, EV +0.23 at -126 (projection 12.0)
- Jonathan Kuminga (MIN) OVER 2.5 Assists: model 61% vs book 46%, EV +0.23 at +102 (projection 2.8)
- Kyrie Irving (DAL) UNDER 4.5 Assists: model 60% vs book 46%, EV +0.23 at +105 (projection 3.6)
- Domantas Sabonis (SAC) UNDER 4.5 Assists: model 57% vs book 44%, EV +0.23 at +114 (projection 4.3)

## MIL at PHI (game 401910023)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Joel Embiid (PHI) OVER 0.5 3-pointers made | -240 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 1.2 | 61% | 61% | -0.06 |
| VJ Edgecombe (PHI) OVER 1.5 3-pointers made | -183 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |

Combined probability 24.7%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Joel Embiid (PHI) OVER 0.5 3-pointers made: 66%, EV -0.06 at -240
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -190
- VJ Edgecombe (PHI) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Anfernee Simons (PHI) OVER 1.5 Assists: 59%, EV -0.06 at -174
- Brayden Burries (MIL) UNDER 3.5 Assists: 59%, EV -0.06 at -171
- Jaime Jaquez Jr. (MIL) OVER 2.5 Assists: 58%, EV -0.06 at -165
- Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -156

## POR at NYK (game 401910024)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Toumani Camara (POR) UNDER 1.5 Steals | -228 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Josh Hart (NYK) UNDER 1.5 Steals | -223 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Jrue Holiday (POR) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 0.9 | 64% | 64% | -0.06 |

Combined probability 27.0%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Toumani Camara (POR) UNDER 1.5 Steals: 65%, EV -0.06 at -228
- Josh Hart (NYK) UNDER 1.5 Steals: 65%, EV -0.06 at -223
- Jrue Holiday (POR) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- Sidy Cissoko (POR) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -204
- Sidy Cissoko (POR) OVER 1.5 Assists: 61%, EV -0.06 at -183
- Damian Lillard (POR) OVER 2.5 3-pointers made: 59%, EV -0.06 at -173
- Jrue Holiday (POR) OVER 1.5 3-pointers made: 58%, EV -0.06 at -164
- Jrue Holiday (POR) UNDER 4.5 Assists: 58%, EV -0.06 at -160

## LAC at DAL (game 401910025)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Keaton Wagler (LAC) UNDER 1.5 3-pointers made | -223 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -221 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -202 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |

Combined probability 26.2%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Keaton Wagler (LAC) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -223
- Kyrie Irving (DAL) UNDER 1.5 Steals: 65%, EV -0.06 at -221
- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 63%, EV -0.06 at -202
- Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -202
- Brook Lopez (LAC) UNDER 2.5 Assists: 61%, EV -0.06 at -190
- Max Strus (LAC) UNDER 3.5 Assists: 59%, EV -0.06 at -172
- P.J. Washington (DAL) UNDER 1.5 Assists: 59%, EV -0.06 at -166
- Max Strus (LAC) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -162

## MEM at MIN (game 401910026)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) UNDER 1.5 Steals | -195 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| Ayo Dosunmu (MIN) UNDER 2.5 3-pointers made | -192 (DraftKings via ESPN) | 2.0 | 62% | 62% | -0.06 |
| Taylor Hendricks (MEM) UNDER 1.5 3-pointers made | -187 (DraftKings via ESPN) | 1.0 | 61% | 61% | -0.06 |

Combined probability 23.3%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Cedric Coward (MEM) UNDER 1.5 Steals: 62%, EV -0.06 at -195
- Ayo Dosunmu (MIN) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -192
- Cedric Coward (MEM) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Taylor Hendricks (MEM) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Jaden McDaniels (MIN) UNDER 3.5 Assists: 59%, EV -0.06 at -168
- Terrence Shannon Jr. (MIN) OVER 2.5 Rebounds: 59%, EV -0.06 at -167
- LaMelo Ball (MIN) UNDER 5.5 Rebounds: 57%, EV -0.06 at -158
- Cam Spencer (MEM) OVER 2.5 Rebounds: 57%, EV -0.06 at -158

## NOP at SAS (game 401910027)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) OVER 0.5 Steals | -247 (DraftKings via ESPN) | 1.1 | 67% | 67% | -0.06 |
| De'Aaron Fox (SAS) OVER 0.5 Steals | -245 (DraftKings via ESPN) | 1.0 | 67% | 67% | -0.06 |
| Devin Vassell (SAS) UNDER 1.5 Steals | -235 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |

Combined probability 29.2%; parlay pays 2.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Victor Wembanyama (SAS) OVER 0.5 Steals: 67%, EV -0.06 at -247
- De'Aaron Fox (SAS) OVER 0.5 Steals: 67%, EV -0.06 at -245
- Devin Vassell (SAS) UNDER 1.5 Steals: 66%, EV -0.06 at -235
- Jeremiah Fears (NOP) UNDER 1.5 Steals: 65%, EV -0.06 at -231
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -211
- Victor Wembanyama (SAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Devin Vassell (SAS) UNDER 4.5 Rebounds: 58%, EV -0.06 at -164
- Jeremiah Fears (NOP) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -158

## BOS at SAC (game 401910028)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zach LaVine (SAC) UNDER 3.5 Rebounds | -176 (DraftKings via ESPN) | 2.8 | 60% | 60% | -0.06 |
| Derrick White (BOS) UNDER 2.5 3-pointers made | -171 (DraftKings via ESPN) | 2.2 | 59% | 59% | -0.06 |
| Jayson Tatum (BOS) OVER 2.5 3-pointers made | -158 (DraftKings via ESPN) | 3.0 | 57% | 57% | -0.06 |

Combined probability 20.3%; parlay pays 4.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Zach LaVine (SAC) UNDER 3.5 Rebounds: 60%, EV -0.06 at -176
- Derrick White (BOS) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -171
- Jayson Tatum (BOS) OVER 2.5 3-pointers made: 57%, EV -0.06 at -158
- Derrick White (BOS) OVER 4.5 Assists: 57%, EV -0.06 at -156
- Zach LaVine (SAC) UNDER 2.5 Assists: 57%, EV -0.06 at -155
- Domantas Sabonis (SAC) OVER 4.5 Assists: 56%, EV -0.06 at -151
- Darius Acuff Jr. (SAC) UNDER 3.5 Rebounds: 56%, EV -0.06 at -150
- Darius Acuff Jr. (SAC) OVER 2.5 3-pointers made: 56%, EV -0.06 at -150
