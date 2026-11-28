# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-28T03:45:31Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Hart (NYK) UNDER 0.5 Blocks | -338 (DraftKings via ESPN) | 0.2 | 73% | 73% | -0.06 |
| DeMar DeRozan (DEN) UNDER 0.5 3-pointers made | -289 (DraftKings via ESPN) | 0.5 | 70% | 70% | -0.06 |
| Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made | -276 (DraftKings via ESPN) | 0.5 | 69% | 69% | -0.06 |
| Derik Queen (NOP) UNDER 0.5 3-pointers made | -261 (DraftKings via ESPN) | 0.5 | 68% | 68% | -0.06 |

**Combined probability 23.9%; parlay pays 3.3x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Josh Hart (NYK) UNDER 0.5 Blocks (73%); DeMar DeRozan (DEN) UNDER 0.5 3-pointers made (70%); Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made (69%). Combined probability 35.1%; parlay pays 2.4x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zion Williamson (NOP) UNDER 22.5 Points | -107 (DraftKings via ESPN) | 16.4 | 74% | 49% | +0.43 |
| Kris Murray (MEM) UNDER 3.5 Rebounds | -122 (DraftKings via ESPN) | 2.4 | 74% | 51% | +0.35 |

Combined probability 54.8%; parlay pays 3.5x; expected profit per 1 staked +0.93.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zion Williamson (NOP) UNDER 22.5 Points | -107 (DraftKings via ESPN) | 16.4 | 74% | 49% | +0.43 |
| Kris Murray (MEM) UNDER 3.5 Rebounds | -122 (DraftKings via ESPN) | 2.4 | 74% | 51% | +0.35 |
| Luka Doncic (LAL) UNDER 32.5 Points | -107 (DraftKings via ESPN) | 28.6 | 68% | 49% | +0.31 |

Combined probability 37.0%; parlay pays 6.8x; expected profit per 1 staked +1.52.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zion Williamson (NOP) UNDER 22.5 Points | -107 (DraftKings via ESPN) | 16.4 | 74% | 49% | +0.43 |
| Kris Murray (MEM) UNDER 3.5 Rebounds | -122 (DraftKings via ESPN) | 2.4 | 74% | 51% | +0.35 |
| Luka Doncic (LAL) UNDER 32.5 Points | -107 (DraftKings via ESPN) | 28.6 | 68% | 49% | +0.31 |
| Jalen Brunson (NYK) OVER 6.5 Assists | +102 (DraftKings via ESPN) | 7.7 | 64% | 46% | +0.29 |

Combined probability 23.7%; parlay pays 13.8x; expected profit per 1 staked +2.26.

Top single picks by model edge:

- Zion Williamson (NOP) UNDER 22.5 Points: model 74% vs book 49%, EV +0.43 at -107 (projection 16.4)
- Kris Murray (MEM) UNDER 3.5 Rebounds: model 74% vs book 51%, EV +0.35 at -122 (projection 2.4)
- Luka Doncic (LAL) UNDER 32.5 Points: model 68% vs book 49%, EV +0.31 at -107 (projection 28.6)
- Jalen Brunson (NYK) OVER 6.5 Assists: model 64% vs book 46%, EV +0.29 at +102 (projection 7.7)
- Brayden Burries (MIL) UNDER 2.5 Assists: model 62% vs book 45%, EV +0.29 at +107 (projection 2.2)
- Terrence Shannon Jr. (MIN) UNDER 16.5 Points: model 67% vs book 49%, EV +0.28 at -110 (projection 14.1)
- Bones Hyland (MIN) UNDER 3.5 Assists: model 60% vs book 44%, EV +0.28 at +111 (projection 3.1)
- Rudy Gobert (MIN) OVER 8.5 Points: model 64% vs book 48%, EV +0.27 at -102 (projection 11.0)
- Ryan Rollins (MIL) UNDER 3.5 Assists: model 66% vs book 49%, EV +0.27 at -108 (projection 2.5)
- Bones Hyland (MIN) UNDER 12.5 Points: model 67% vs book 50%, EV +0.26 at -113 (projection 10.5)
- Terrence Shannon Jr. (MIN) UNDER 3.5 Rebounds: model 64% vs book 48%, EV +0.26 at -104 (projection 2.9)
- Nikola Jokic (DEN) UNDER 26.5 Points: model 66% vs book 50%, EV +0.24 at -115 (projection 23.5)

## MIA at NYK (game 401909326)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Hart (NYK) UNDER 0.5 Blocks | -338 (DraftKings via ESPN) | 0.2 | 73% | 73% | -0.06 |
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Davion Mitchell (MIA) UNDER 1.5 Steals | -232 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |

Combined probability 31.6%; parlay pays 2.6x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Josh Hart (NYK) UNDER 0.5 Blocks: 73%, EV -0.06 at -338
- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -240
- Davion Mitchell (MIA) UNDER 1.5 Steals: 66%, EV -0.06 at -232
- Bobby Portis (MIA) UNDER 1.5 Assists: 65%, EV -0.06 at -226
- Andrew Wiggins (MIA) OVER 0.5 3-pointers made: 65%, EV -0.06 at -222
- Bobby Portis (MIA) OVER 0.5 3-pointers made: 64%, EV -0.06 at -218
- Josh Hart (NYK) UNDER 1.5 Steals: 61%, EV -0.06 at -191
- Klay Thompson (MIA) UNDER 2.5 Rebounds: 61%, EV -0.06 at -190

## MIL at DET (game 401909327)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Daniss Jenkins (DET) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -233 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Ausar Thompson (DET) OVER 0.5 Blocks | -208 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 27.6%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Daniss Jenkins (DET) UNDER 1.5 Steals: 66%, EV -0.06 at -243
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -233
- Ausar Thompson (DET) OVER 0.5 Blocks: 63%, EV -0.06 at -208
- Kevin Huerter (DET) UNDER 1.5 Steals: 61%, EV -0.06 at -189
- Kevin Huerter (DET) OVER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184
- John Collins (DET) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Paul Reed (DET) UNDER 2.5 Assists: 60%, EV -0.06 at -175

## PHI at IND (game 401909328)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kelly Oubre Jr. (IND) UNDER 1.5 Assists | -242 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Tyrese Maxey (PHI) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| LeBron James (PHI) OVER 0.5 Steals | -225 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

Combined probability 28.0%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Kelly Oubre Jr. (IND) UNDER 1.5 Assists: 66%, EV -0.06 at -242
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 65%, EV -0.06 at -226
- LeBron James (PHI) OVER 0.5 Steals: 65%, EV -0.06 at -225
- LeBron James (PHI) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Anfernee Simons (PHI) OVER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Aaron Nesmith (IND) OVER 1.5 Assists: 58%, EV -0.06 at -165
- Obi Toppin (IND) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -165

## BKN at TOR (game 401909329)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made | -276 (DraftKings via ESPN) | 0.5 | 69% | 69% | -0.06 |
| Noah Clowney (BKN) UNDER 1.5 Assists | -240 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Scottie Barnes (TOR) OVER 0.5 3-pointers made | -237 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |

Combined probability 30.3%; parlay pays 2.7x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made: 69%, EV -0.06 at -276
- Noah Clowney (BKN) UNDER 1.5 Assists: 66%, EV -0.06 at -240
- Day'Ron Sharpe (BKN) OVER 0.5 Blocks: 66%, EV -0.06 at -241
- Scottie Barnes (TOR) OVER 0.5 3-pointers made: 66%, EV -0.06 at -237
- Michael Porter Jr. (BKN) OVER 0.5 Steals: 64%, EV -0.06 at -218
- Jakob Poeltl (TOR) UNDER 2.5 Assists: 62%, EV -0.06 at -194
- Collin Murray-Boyles (TOR) UNDER 2.5 Assists: 62%, EV -0.06 at -191
- Danny Wolf (BKN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185

## ATL at BOS (game 401909330)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dyson Daniels (ATL) UNDER 0.5 Blocks | -243 (DraftKings via ESPN) | 0.4 | 66% | 66% | -0.06 |
| Sam Hauser (BOS) UNDER 1.5 Assists | -231 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Jayson Tatum (BOS) UNDER 1.5 Steals | -229 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 28.5%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dyson Daniels (ATL) UNDER 0.5 Blocks: 66%, EV -0.06 at -243
- Sam Hauser (BOS) UNDER 1.5 Assists: 66%, EV -0.06 at -231
- Jayson Tatum (BOS) UNDER 1.5 Steals: 65%, EV -0.06 at -229
- Luguentz Dort (ATL) UNDER 1.5 Assists: 65%, EV -0.06 at -221
- Derrick White (BOS) OVER 0.5 Steals: 64%, EV -0.06 at -219
- Nickeil Alexander-Walker (ATL) UNDER 0.5 Blocks: 64%, EV -0.06 at -218
- Baylor Scheierman (BOS) OVER 0.5 3-pointers made: 63%, EV -0.06 at -209
- Dyson Daniels (ATL) UNDER 0.5 3-pointers made: 63%, EV -0.06 at -203

## MEM at MIN (game 401909331)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bones Hyland (MIN) UNDER 2.5 Rebounds | -188 (DraftKings via ESPN) | 1.7 | 61% | 61% | -0.06 |
| Cedric Coward (MEM) UNDER 2.5 3-pointers made | -188 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |
| Ayo Dosunmu (MIN) UNDER 2.5 3-pointers made | -174 (DraftKings via ESPN) | 2.4 | 59% | 59% | -0.06 |

Combined probability 22.3%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Bones Hyland (MIN) UNDER 2.5 Rebounds: 61%, EV -0.06 at -188
- Cedric Coward (MEM) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -188
- Ayo Dosunmu (MIN) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -174
- Cedric Coward (MEM) UNDER 3.5 Assists: 58%, EV -0.06 at -162
- Jaylen Wells (MEM) UNDER 3.5 Rebounds: 57%, EV -0.06 at -156
- Cam Spencer (MEM) UNDER 2.5 Rebounds: 56%, EV -0.06 at -150
- Bones Hyland (MIN) OVER 3.5 Assists: 56%, EV -0.06 at -146
- Kris Murray (MEM) OVER 0.5 3-pointers made: 56%, EV -0.06 at -146

## DAL at PHX (game 401909332)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Collin Gillespie (PHX) UNDER 1.5 Steals | -220 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Jalen Green (PHX) OVER 0.5 Steals | -217 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Zaccharie Risacher (DAL) UNDER 1.5 3-pointers made | -206 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |

Combined probability 26.1%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Collin Gillespie (PHX) UNDER 1.5 Steals: 64%, EV -0.06 at -220
- Jalen Green (PHX) OVER 0.5 Steals: 64%, EV -0.06 at -217
- Zaccharie Risacher (DAL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Zaccharie Risacher (DAL) UNDER 1.5 Assists: 63%, EV -0.06 at -203
- Daniel Gafford (DAL) OVER 1.5 Assists: 62%, EV -0.06 at -194
- Devin Booker (PHX) OVER 0.5 Steals: 62%, EV -0.06 at -194
- Collin Gillespie (PHX) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -190
- Dillon Brooks (PHX) OVER 1.5 Assists: 60%, EV -0.06 at -182

## LAL at SAS (game 401909333)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) OVER 0.5 Steals | -221 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Collin Sexton (LAL) OVER 0.5 3-pointers made | -206 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |
| Matisse Thybulle (LAL) UNDER 2.5 Rebounds | -173 (DraftKings via ESPN) | 2.7 | 59% | 59% | -0.06 |

Combined probability 24.2%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Victor Wembanyama (SAS) OVER 0.5 Steals: 65%, EV -0.06 at -221
- Collin Sexton (LAL) OVER 0.5 3-pointers made: 63%, EV -0.06 at -206
- Victor Wembanyama (SAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Matisse Thybulle (LAL) UNDER 2.5 Rebounds: 59%, EV -0.06 at -173
- Collin Sexton (LAL) UNDER 2.5 Assists: 59%, EV -0.06 at -171
- Victor Wembanyama (SAS) OVER 2.5 Blocks: 59%, EV -0.06 at -170
- Victor Wembanyama (SAS) OVER 2.5 Assists: 59%, EV -0.06 at -167
- Walker Kessler (LAL) OVER 0.5 Steals: 58%, EV -0.07 at -167

## DEN at UTA (game 401909334)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| DeMar DeRozan (DEN) UNDER 0.5 3-pointers made | -289 (DraftKings via ESPN) | 0.5 | 70% | 70% | -0.06 |
| Jamal Murray (DEN) OVER 0.5 Steals | -197 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |
| Josh Green (UTA) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 0.9 | 62% | 62% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- DeMar DeRozan (DEN) UNDER 0.5 3-pointers made: 70%, EV -0.06 at -289
- Jamal Murray (DEN) OVER 0.5 Steals: 62%, EV -0.06 at -197
- Josh Green (UTA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Svi Mykhailiuk (UTA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Darryn Peterson (UTA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Keyonte George (UTA) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181

## NOP at LAC (game 401909335)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derik Queen (NOP) UNDER 0.5 3-pointers made | -261 (DraftKings via ESPN) | 0.5 | 68% | 68% | -0.06 |
| Derrick Jones Jr. (LAC) OVER 0.5 3-pointers made | -233 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 Steals | -217 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

Combined probability 28.7%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Derik Queen (NOP) UNDER 0.5 3-pointers made: 68%, EV -0.06 at -261
- Derrick Jones Jr. (LAC) OVER 0.5 3-pointers made: 66%, EV -0.06 at -233
- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 65%, EV -0.06 at -229
- Herbert Jones (NOP) UNDER 1.5 Steals: 64%, EV -0.06 at -217
- Keaton Wagler (LAC) OVER 0.5 3-pointers made: 63%, EV -0.06 at -203
- Jeremiah Fears (NOP) UNDER 1.5 Steals: 63%, EV -0.06 at -202
- Yves Missi (NOP) UNDER 1.5 Assists: 62%, EV -0.06 at -194
- Derik Queen (NOP) UNDER 2.5 Assists: 61%, EV -0.06 at -185

## GSW at POR (game 401909336)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Toumani Camara (POR) UNDER 1.5 Steals | -228 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Sidy Cissoko (POR) UNDER 1.5 Steals | -203 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |
| Draymond Green (GSW) OVER 0.5 3-pointers made | -195 (DraftKings via ESPN) | 0.8 | 62% | 62% | -0.06 |

Combined probability 25.3%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Toumani Camara (POR) UNDER 1.5 Steals: 65%, EV -0.06 at -228
- Sidy Cissoko (POR) UNDER 1.5 Steals: 63%, EV -0.06 at -203
- Draymond Green (GSW) OVER 0.5 3-pointers made: 62%, EV -0.06 at -195
- De'Anthony Melton (GSW) OVER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Sidy Cissoko (POR) OVER 1.5 Assists: 61%, EV -0.06 at -186
- Gui Santos (GSW) OVER 0.5 3-pointers made: 61%, EV -0.06 at -183
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 61%, EV -0.06 at -183
- Donovan Clingan (POR) OVER 1.5 Assists: 61%, EV -0.06 at -182
