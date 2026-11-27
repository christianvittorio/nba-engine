# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-27T22:29:26Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| DeMar DeRozan (DEN) UNDER 0.5 3-pointers made | -316 (DraftKings via ESPN) | 0.5 | 72% | 72% | -0.06 |
| Derik Queen (NOP) UNDER 0.5 3-pointers made | -265 (DraftKings via ESPN) | 0.6 | 68% | 68% | -0.06 |
| Dyson Daniels (ATL) UNDER 0.5 Blocks | -247 (DraftKings via ESPN) | 0.4 | 67% | 67% | -0.06 |
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -243 (DraftKings via ESPN) | 1.3 | 67% | 67% | -0.06 |

**Combined probability 21.7%; parlay pays 3.6x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: DeMar DeRozan (DEN) UNDER 0.5 3-pointers made (72%); Derik Queen (NOP) UNDER 0.5 3-pointers made (68%); Dyson Daniels (ATL) UNDER 0.5 Blocks (67%). Combined probability 32.6%; parlay pays 2.5x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zion Williamson (NOP) UNDER 22.5 Points | -112 (DraftKings via ESPN) | 16.7 | 72% | 50% | +0.36 |
| Bones Hyland (MIN) UNDER 3.5 Assists | +120 (DraftKings via ESPN) | 3.1 | 60% | 43% | +0.33 |

Combined probability 43.4%; parlay pays 4.2x; expected profit per 1 staked +0.81.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zion Williamson (NOP) UNDER 22.5 Points | -112 (DraftKings via ESPN) | 16.7 | 72% | 50% | +0.36 |
| Bones Hyland (MIN) UNDER 3.5 Assists | +120 (DraftKings via ESPN) | 3.1 | 60% | 43% | +0.33 |
| Miles Bridges (PHX) UNDER 14.5 Points | -113 (DraftKings via ESPN) | 12.2 | 69% | 50% | +0.29 |

Combined probability 29.8%; parlay pays 7.8x; expected profit per 1 staked +1.34.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zion Williamson (NOP) UNDER 22.5 Points | -112 (DraftKings via ESPN) | 16.7 | 72% | 50% | +0.36 |
| Bones Hyland (MIN) UNDER 3.5 Assists | +120 (DraftKings via ESPN) | 3.1 | 60% | 43% | +0.33 |
| Miles Bridges (PHX) UNDER 14.5 Points | -113 (DraftKings via ESPN) | 12.2 | 69% | 50% | +0.29 |
| Brayden Burries (MIL) UNDER 2.5 Assists | +107 (DraftKings via ESPN) | 2.2 | 62% | 45% | +0.29 |

Combined probability 18.6%; parlay pays 16.2x; expected profit per 1 staked +2.02.

Top single picks by model edge:

- Zion Williamson (NOP) UNDER 22.5 Points: model 72% vs book 50%, EV +0.36 at -112 (projection 16.7)
- Bones Hyland (MIN) UNDER 3.5 Assists: model 60% vs book 43%, EV +0.33 at +120 (projection 3.1)
- Kris Murray (MEM) UNDER 3.5 Rebounds: model 73% vs book 52%, EV +0.32 at -125 (projection 2.4)
- Terrence Shannon Jr. (MIN) UNDER 3.5 Rebounds: model 64% vs book 46%, EV +0.31 at +104 (projection 2.9)
- Miles Bridges (PHX) UNDER 14.5 Points: model 69% vs book 50%, EV +0.29 at -113 (projection 12.2)
- Brayden Burries (MIL) UNDER 2.5 Assists: model 62% vs book 45%, EV +0.29 at +107 (projection 2.2)
- Bones Hyland (MIN) UNDER 13.5 Points: model 72% vs book 52%, EV +0.28 at -126 (projection 10.5)
- Terrence Shannon Jr. (MIN) UNDER 16.5 Points: model 67% vs book 50%, EV +0.28 at -111 (projection 14.1)
- Luka Doncic (LAL) UNDER 32.5 Points: model 65% vs book 49%, EV +0.27 at -106 (projection 28.9)
- Bones Hyland (MIN) UNDER 2.5 3-pointers made: model 70% vs book 52%, EV +0.27 at -123 (projection 1.8)
- Cooper Flagg (DAL) UNDER 6.5 Assists: model 66% vs book 49%, EV +0.26 at -112 (projection 5.5)
- Rudy Gobert (MIN) OVER 8.5 Points: model 64% vs book 49%, EV +0.24 at -107 (projection 11.0)

## MIA at NYK (game 401909326)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -243 (DraftKings via ESPN) | 1.3 | 67% | 67% | -0.06 |
| Josh Hart (NYK) UNDER 0.5 Blocks | -244 (DraftKings via ESPN) | 0.2 | 67% | 67% | -0.06 |
| Giannis Antetokounmpo (MIA) OVER 0.5 Blocks | -236 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |

Combined probability 29.2%; parlay pays 2.8x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 67%, EV -0.06 at -243
- Josh Hart (NYK) UNDER 0.5 Blocks: 67%, EV -0.06 at -244
- Giannis Antetokounmpo (MIA) OVER 0.5 Blocks: 66%, EV -0.06 at -236
- Andrew Wiggins (MIA) OVER 0.5 3-pointers made: 65%, EV -0.06 at -222
- Davion Mitchell (MIA) OVER 0.5 Steals: 64%, EV -0.06 at -220
- Bobby Portis (MIA) UNDER 1.5 Assists: 64%, EV -0.06 at -217
- Bobby Portis (MIA) OVER 0.5 3-pointers made: 63%, EV -0.06 at -203
- Giannis Antetokounmpo (MIA) UNDER 0.5 3-pointers made: 62%, EV -0.06 at -196

## MIL at DET (game 401909327)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ausar Thompson (DET) OVER 0.5 Blocks | -228 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -225 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Daniss Jenkins (DET) UNDER 1.5 Steals | -224 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |

Combined probability 27.4%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ausar Thompson (DET) OVER 0.5 Blocks: 65%, EV -0.06 at -228
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -225
- Daniss Jenkins (DET) UNDER 1.5 Steals: 65%, EV -0.06 at -224
- John Collins (DET) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Paul Reed (DET) OVER 1.5 Assists: 61%, EV -0.06 at -190
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Kevin Huerter (DET) UNDER 1.5 Steals: 59%, EV -0.06 at -169
- Daniss Jenkins (DET) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -166

## PHI at IND (game 401909328)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 1.5 Steals | -229 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| LeBron James (PHI) OVER 0.5 Steals | -218 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made | -178 (DraftKings via ESPN) | 1.3 | 60% | 60% | -0.06 |

Combined probability 25.1%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Tyrese Maxey (PHI) UNDER 1.5 Steals: 65%, EV -0.06 at -229
- LeBron James (PHI) OVER 0.5 Steals: 64%, EV -0.06 at -218
- LeBron James (PHI) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -208
- Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -166
- Anfernee Simons (PHI) OVER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Ivica Zubac (IND) OVER 1.5 Assists: 58%, EV -0.06 at -163
- VJ Edgecombe (PHI) UNDER 4.5 Assists: 58%, EV -0.06 at -161

## BKN at TOR (game 401909329)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) OVER 0.5 Blocks | -241 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Scottie Barnes (TOR) OVER 0.5 3-pointers made | -237 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Michael Porter Jr. (BKN) OVER 0.5 Steals | -218 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |

Combined probability 28.1%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Day'Ron Sharpe (BKN) OVER 0.5 Blocks: 66%, EV -0.06 at -241
- Scottie Barnes (TOR) OVER 0.5 3-pointers made: 66%, EV -0.06 at -237
- Michael Porter Jr. (BKN) OVER 0.5 Steals: 64%, EV -0.06 at -218
- Jakob Poeltl (TOR) OVER 1.5 Assists: 61%, EV -0.06 at -188
- Allen Graves (TOR) UNDER 1.5 Assists: 61%, EV -0.06 at -188
- Danny Wolf (BKN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Noah Clowney (BKN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Collin Murray-Boyles (TOR) OVER 1.5 Assists: 59%, EV -0.06 at -170

## ATL at BOS (game 401909330)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dyson Daniels (ATL) UNDER 0.5 Blocks | -247 (DraftKings via ESPN) | 0.4 | 67% | 67% | -0.06 |
| Luguentz Dort (ATL) UNDER 1.5 Assists | -232 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Derrick White (BOS) OVER 0.5 Steals | -229 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 28.6%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dyson Daniels (ATL) UNDER 0.5 Blocks: 67%, EV -0.06 at -247
- Luguentz Dort (ATL) UNDER 1.5 Assists: 66%, EV -0.06 at -232
- Derrick White (BOS) OVER 0.5 Steals: 65%, EV -0.06 at -229
- Baylor Scheierman (BOS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -221
- Nickeil Alexander-Walker (ATL) UNDER 0.5 Blocks: 64%, EV -0.06 at -218
- Sam Hauser (BOS) UNDER 1.5 Assists: 64%, EV -0.06 at -215
- Jayson Tatum (BOS) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- Dyson Daniels (ATL) UNDER 0.5 3-pointers made: 64%, EV -0.06 at -211

## MEM at MIN (game 401909331)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) UNDER 2.5 3-pointers made | -186 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| Ayo Dosunmu (MIN) UNDER 2.5 3-pointers made | -167 (DraftKings via ESPN) | 2.4 | 59% | 59% | -0.06 |
| Bones Hyland (MIN) UNDER 2.5 Rebounds | -158 (DraftKings via ESPN) | 1.7 | 57% | 57% | -0.06 |

Combined probability 20.5%; parlay pays 4.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Cedric Coward (MEM) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -186
- Cedric Coward (MEM) UNDER 3.5 Assists: 59%, EV -0.06 at -173
- Ayo Dosunmu (MIN) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -167
- Bones Hyland (MIN) UNDER 2.5 Rebounds: 57%, EV -0.06 at -158
- Bones Hyland (MIN) OVER 3.5 Assists: 57%, EV -0.06 at -158
- Cam Spencer (MEM) OVER 4.5 Assists: 57%, EV -0.06 at -155
- Ayo Dosunmu (MIN) OVER 4.5 Assists: 57%, EV -0.06 at -153
- Jaden McDaniels (MIN) OVER 3.5 Assists: 56%, EV -0.06 at -150

## DAL at PHX (game 401909332)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Collin Gillespie (PHX) UNDER 1.5 Steals | -228 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Caleb Martin (DAL) UNDER 1.5 3-pointers made | -198 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |
| Jalen Green (PHX) OVER 0.5 Steals | -197 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |

Combined probability 25.2%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Collin Gillespie (PHX) UNDER 1.5 Steals: 65%, EV -0.06 at -228
- Caleb Martin (DAL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Jalen Green (PHX) OVER 0.5 Steals: 62%, EV -0.06 at -197
- Dillon Brooks (PHX) OVER 1.5 Assists: 62%, EV -0.06 at -195
- Collin Gillespie (PHX) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Zaccharie Risacher (DAL) OVER 0.5 3-pointers made: 61%, EV -0.06 at -189
- Devin Booker (PHX) OVER 0.5 Steals: 61%, EV -0.06 at -187
- Naji Marshall (DAL) OVER 0.5 3-pointers made: 60%, EV -0.06 at -181

## LAL at SAS (game 401909333)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) OVER 0.5 Steals | -231 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Collin Sexton (LAL) OVER 0.5 3-pointers made | -197 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Walker Kessler (LAL) OVER 0.5 Steals | -170 (DraftKings via ESPN) | 0.8 | 59% | 59% | -0.06 |

Combined probability 24.0%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Victor Wembanyama (SAS) OVER 0.5 Steals: 65%, EV -0.06 at -231
- Collin Sexton (LAL) OVER 0.5 3-pointers made: 62%, EV -0.06 at -197
- Victor Wembanyama (SAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Victor Wembanyama (SAS) UNDER 3.5 Blocks: 59%, EV -0.07 at -173
- Walker Kessler (LAL) OVER 0.5 Steals: 59%, EV -0.06 at -170
- Quentin Grimes (LAL) OVER 2.5 Rebounds: 58%, EV -0.06 at -165
- Victor Wembanyama (SAS) OVER 2.5 Assists: 58%, EV -0.06 at -165
- Quentin Grimes (LAL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -160

## DEN at UTA (game 401909334)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| DeMar DeRozan (DEN) UNDER 0.5 3-pointers made | -316 (DraftKings via ESPN) | 0.5 | 72% | 72% | -0.06 |
| Jamal Murray (DEN) OVER 0.5 Steals | -197 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |
| Aaron Gordon (DEN) UNDER 1.5 3-pointers made | -186 (DraftKings via ESPN) | 1.2 | 61% | 61% | -0.06 |

Combined probability 27.1%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- DeMar DeRozan (DEN) UNDER 0.5 3-pointers made: 72%, EV -0.06 at -316
- Jamal Murray (DEN) OVER 0.5 Steals: 62%, EV -0.06 at -197
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Keyonte George (UTA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Darryn Peterson (UTA) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Nikola Jokic (DEN) UNDER 1.5 Steals: 58%, EV -0.06 at -165

## NOP at LAC (game 401909335)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derik Queen (NOP) UNDER 0.5 3-pointers made | -265 (DraftKings via ESPN) | 0.6 | 68% | 68% | -0.06 |
| Derrick Jones Jr. (LAC) OVER 0.5 3-pointers made | -232 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 Steals | -224 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |

Combined probability 29.0%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Derik Queen (NOP) UNDER 0.5 3-pointers made: 68%, EV -0.06 at -265
- Derrick Jones Jr. (LAC) OVER 0.5 3-pointers made: 66%, EV -0.06 at -232
- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 66%, EV -0.06 at -231
- Herbert Jones (NOP) UNDER 1.5 Steals: 65%, EV -0.06 at -224
- Jeremiah Fears (NOP) UNDER 1.5 Steals: 63%, EV -0.06 at -209
- Saddiq Bey (NOP) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -190
- Derik Queen (NOP) UNDER 2.5 Assists: 61%, EV -0.06 at -186
- Brook Lopez (LAC) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -180

## GSW at POR (game 401909336)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Toumani Camara (POR) UNDER 1.5 Steals | -238 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Sidy Cissoko (POR) UNDER 1.5 Steals | -202 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |
| Draymond Green (GSW) OVER 0.5 3-pointers made | -195 (DraftKings via ESPN) | 0.8 | 62% | 62% | -0.06 |

Combined probability 25.6%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Toumani Camara (POR) UNDER 1.5 Steals: 66%, EV -0.06 at -238
- Sidy Cissoko (POR) UNDER 1.5 Steals: 63%, EV -0.06 at -202
- Draymond Green (GSW) OVER 0.5 3-pointers made: 62%, EV -0.06 at -195
- De'Anthony Melton (GSW) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -192
- Donovan Clingan (POR) UNDER 2.5 Assists: 62%, EV -0.06 at -191
- Gui Santos (GSW) OVER 0.5 3-pointers made: 61%, EV -0.06 at -190
- Sidy Cissoko (POR) UNDER 2.5 Assists: 61%, EV -0.06 at -188
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 61%, EV -0.06 at -183
