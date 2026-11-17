# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-17T04:21:56Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| LaMelo Ball (MIN) UNDER 0.5 Blocks | -378 (DraftKings via ESPN) | 0.1 | 75% | 75% | -0.06 |
| Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made | -319 (DraftKings via ESPN) | 0.5 | 72% | 72% | -0.06 |
| Trae Young (WAS) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Franz Wagner (ORL) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |

**Combined probability 23.4%; parlay pays 3.3x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: LaMelo Ball (MIN) UNDER 0.5 Blocks (75%); Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made (72%); Trae Young (WAS) UNDER 1.5 Steals (66%). Combined probability 35.5%; parlay pays 2.3x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tari Eason (HOU) UNDER 13.5 Points | -105 (DraftKings via ESPN) | 10.9 | 70% | 48% | +0.38 |
| Anfernee Simons (PHI) UNDER 10.5 Points | -118 (DraftKings via ESPN) | 7.9 | 73% | 51% | +0.35 |

Combined probability 51.5%; parlay pays 3.6x; expected profit per 1 staked +0.86.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tari Eason (HOU) UNDER 13.5 Points | -105 (DraftKings via ESPN) | 10.9 | 70% | 48% | +0.38 |
| Anfernee Simons (PHI) UNDER 10.5 Points | -118 (DraftKings via ESPN) | 7.9 | 73% | 51% | +0.35 |
| Cam Spencer (MEM) UNDER 13.5 Points | -112 (DraftKings via ESPN) | 10.6 | 71% | 50% | +0.35 |

Combined probability 36.6%; parlay pays 6.8x; expected profit per 1 staked +1.50.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tari Eason (HOU) UNDER 13.5 Points | -105 (DraftKings via ESPN) | 10.9 | 70% | 48% | +0.38 |
| Anfernee Simons (PHI) UNDER 10.5 Points | -118 (DraftKings via ESPN) | 7.9 | 73% | 51% | +0.35 |
| Cam Spencer (MEM) UNDER 13.5 Points | -112 (DraftKings via ESPN) | 10.6 | 71% | 50% | +0.35 |
| Al Horford (GSW) UNDER 4.5 Rebounds | -120 (DraftKings via ESPN) | 3.2 | 72% | 51% | +0.31 |

Combined probability 26.3%; parlay pays 12.5x; expected profit per 1 staked +2.29.

Top single picks by model edge:

- Tari Eason (HOU) UNDER 13.5 Points: model 70% vs book 48%, EV +0.38 at -105 (projection 10.9)
- Anfernee Simons (PHI) UNDER 10.5 Points: model 73% vs book 51%, EV +0.35 at -118 (projection 7.9)
- Cam Spencer (MEM) UNDER 13.5 Points: model 71% vs book 50%, EV +0.35 at -112 (projection 10.6)
- Tyrese Maxey (PHI) UNDER 25.5 Points: model 74% vs book 51%, EV +0.35 at -120 (projection 20.9)
- Al Horford (GSW) UNDER 4.5 Rebounds: model 72% vs book 51%, EV +0.31 at -120 (projection 3.2)
- Michael Porter Jr. (BKN) UNDER 21.5 Points: model 69% vs book 50%, EV +0.31 at -111 (projection 16.1)
- VJ Edgecombe (PHI) UNDER 13.5 Points: model 70% vs book 51%, EV +0.31 at -116 (projection 11.0)
- Jonathan Kuminga (MIN) OVER 12.5 Points: model 69% vs book 50%, EV +0.31 at -112 (projection 16.4)
- Sam Hauser (BOS) UNDER 1.5 3-pointers made: model 58% vs book 42%, EV +0.31 at +124 (projection 1.4)
- Josh Giddey (CHI) OVER 1.5 3-pointers made: model 53% vs book 38%, EV +0.31 at +145 (projection 1.8)
- Cam Spencer (MEM) UNDER 7.5 Assists: model 67% vs book 48%, EV +0.30 at -106 (projection 6.1)
- Giannis Antetokounmpo (MIA) OVER 0.5 3-pointers made: model 53% vs book 39%, EV +0.28 at +140 (projection 0.8)

## ORL at BOS (game 401909994)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Neemias Queta (BOS) UNDER 1.5 Blocks | -233 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Jayson Tatum (BOS) OVER 0.5 Steals | -199 (DraftKings via ESPN) | 0.9 | 62% | 62% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Franz Wagner (ORL) UNDER 1.5 Steals: 66%, EV -0.06 at -237
- Neemias Queta (BOS) UNDER 1.5 Blocks: 66%, EV -0.06 at -233
- Jayson Tatum (BOS) OVER 0.5 Steals: 62%, EV -0.06 at -199
- Derrick White (BOS) OVER 0.5 Steals: 62%, EV -0.06 at -192
- Payton Pritchard (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Derrick White (BOS) OVER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -167
- Payton Pritchard (BOS) OVER 2.5 Rebounds: 59%, EV -0.06 at -166

## CHI at CLE (game 401909995)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Isaac Okoro (CHI) OVER 0.5 3-pointers made | -226 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Mario Hezonja (CLE) UNDER 1.5 3-pointers made | -223 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -204 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |

Combined probability 26.5%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Isaac Okoro (CHI) OVER 0.5 3-pointers made: 65%, EV -0.06 at -226
- Mario Hezonja (CLE) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -223
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 63%, EV -0.06 at -204
- Josh Giddey (CHI) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -193
- Matas Buzelis (CHI) UNDER 2.5 Assists: 61%, EV -0.06 at -183
- Matas Buzelis (CHI) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -183
- Meleek Thomas (CLE) OVER 1.5 3-pointers made: 58%, EV -0.06 at -166
- Tyrese Proctor (CLE) OVER 1.5 3-pointers made: 58%, EV -0.06 at -159

## MEM at WAS (game 401909996)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Trae Young (WAS) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| AJ Dybantsa (WAS) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Anthony Davis (WAS) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

Combined probability 28.4%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Trae Young (WAS) UNDER 1.5 Steals: 66%, EV -0.06 at -242
- AJ Dybantsa (WAS) OVER 0.5 Steals: 66%, EV -0.06 at -236
- AJ Dybantsa (WAS) OVER 0.5 3-pointers made: 66%, EV -0.06 at -231
- Anthony Davis (WAS) UNDER 1.5 Steals: 65%, EV -0.06 at -226
- Cam Spencer (MEM) UNDER 1.5 Steals: 64%, EV -0.06 at -211
- Kyshawn George (WAS) OVER 0.5 Blocks: 63%, EV -0.06 at -208
- Alex Sarr (WAS) OVER 0.5 3-pointers made: 63%, EV -0.06 at -204
- Taylor Hendricks (MEM) OVER 0.5 3-pointers made: 63%, EV -0.06 at -202

## PHI at BKN (game 401909997)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made | -319 (DraftKings via ESPN) | 0.5 | 72% | 72% | -0.06 |
| Jaylen Brown (PHI) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Danny Wolf (BKN) UNDER 1.5 3-pointers made | -204 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |

Combined probability 29.9%; parlay pays 2.8x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made: 72%, EV -0.06 at -319
- Jaylen Brown (PHI) UNDER 1.5 Steals: 66%, EV -0.06 at -241
- Day'Ron Sharpe (BKN) OVER 0.5 Blocks: 64%, EV -0.06 at -218
- Danny Wolf (BKN) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -204
- VJ Edgecombe (PHI) UNDER 1.5 Steals: 63%, EV -0.06 at -203
- Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Anfernee Simons (PHI) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -180

## HOU at MIA (game 401909998)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) OVER 0.5 Steals | -220 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Bam Adebayo (MIA) OVER 0.5 3-pointers made | -219 (DraftKings via ESPN) | 1.5 | 64% | 64% | -0.06 |
| Fred VanVleet (HOU) UNDER 1.5 Steals | -220 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |

Combined probability 26.8%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Alperen Sengun (HOU) OVER 0.5 Steals: 64%, EV -0.06 at -220
- Bam Adebayo (MIA) OVER 0.5 3-pointers made: 64%, EV -0.06 at -219
- Fred VanVleet (HOU) UNDER 1.5 Steals: 64%, EV -0.06 at -220
- Andrew Wiggins (MIA) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -205
- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -199
- Giannis Antetokounmpo (MIA) UNDER 0.5 3-pointers made: 61%, EV -0.06 at -186
- Davion Mitchell (MIA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Amen Thompson (HOU) UNDER 1.5 Steals: 60%, EV -0.06 at -176

## POR at MIN (game 401909999)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| LaMelo Ball (MIN) UNDER 0.5 Blocks | -378 (DraftKings via ESPN) | 0.1 | 75% | 75% | -0.06 |
| Jaden McDaniels (MIN) OVER 0.5 Steals | -241 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Damian Lillard (POR) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |

Combined probability 32.5%; parlay pays 2.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- LaMelo Ball (MIN) UNDER 0.5 Blocks: 75%, EV -0.06 at -378
- Jaden McDaniels (MIN) OVER 0.5 Steals: 66%, EV -0.06 at -241
- Damian Lillard (POR) OVER 0.5 Steals: 66%, EV -0.06 at -236
- Ayo Dosunmu (MIN) UNDER 1.5 Steals: 66%, EV -0.06 at -234
- Jrue Holiday (POR) OVER 0.5 Steals: 63%, EV -0.06 at -208
- Jonathan Kuminga (MIN) OVER 0.5 Steals: 63%, EV -0.06 at -208
- Toumani Camara (POR) UNDER 1.5 Steals: 63%, EV -0.06 at -202
- Jaden McDaniels (MIN) OVER 0.5 Blocks: 62%, EV -0.06 at -200

## GSW at NOP (game 401910000)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| De'Anthony Melton (GSW) OVER 0.5 Steals | -229 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Brandin Podziemski (GSW) UNDER 1.5 Steals | -225 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -217 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

Combined probability 27.2%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- De'Anthony Melton (GSW) OVER 0.5 Steals: 65%, EV -0.06 at -229
- Brandin Podziemski (GSW) UNDER 1.5 Steals: 65%, EV -0.06 at -225
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -217
- Herbert Jones (NOP) UNDER 1.5 Steals: 62%, EV -0.06 at -195
- Al Horford (GSW) UNDER 2.5 Assists: 61%, EV -0.06 at -190
- Herbert Jones (NOP) OVER 1.5 Assists: 60%, EV -0.06 at -177
- Yaxel Lendeborg (GSW) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -174
- De'Anthony Melton (GSW) OVER 1.5 3-pointers made: 59%, EV -0.06 at -173

## PHX at DEN (game 401910001)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cameron Johnson (DEN) UNDER 2.5 3-pointers made | -195 (DraftKings via ESPN) | 1.9 | 62% | 62% | -0.06 |
| Nikola Jokic (DEN) UNDER 1.5 3-pointers made | -193 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| Christian Braun (DEN) UNDER 2.5 Assists | -185 (DraftKings via ESPN) | 2.4 | 61% | 61% | -0.06 |

Combined probability 23.3%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Cameron Johnson (DEN) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -195
- Nikola Jokic (DEN) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -193
- Cameron Johnson (DEN) OVER 1.5 Assists: 61%, EV -0.06 at -187
- Christian Braun (DEN) UNDER 2.5 Assists: 61%, EV -0.06 at -185
- Aaron Gordon (DEN) UNDER 2.5 Assists: 59%, EV -0.06 at -170
- Dillon Brooks (PHX) OVER 1.5 Assists: 59%, EV -0.06 at -167
- Nikola Jokic (DEN) UNDER 1.5 Steals: 58%, EV -0.06 at -166
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -163
