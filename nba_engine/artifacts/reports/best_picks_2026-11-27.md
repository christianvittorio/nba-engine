# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-27T18:44:46Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| DeMar DeRozan (DEN) UNDER 0.5 3-pointers made | -377 (DraftKings via ESPN) | 0.5 | 75% | 75% | -0.06 |
| Derik Queen (NOP) UNDER 0.5 3-pointers made | -286 (DraftKings via ESPN) | 0.6 | 70% | 70% | -0.06 |
| Dyson Daniels (ATL) UNDER 0.5 3-pointers made | -275 (DraftKings via ESPN) | 0.6 | 69% | 69% | -0.06 |
| Victor Wembanyama (SAS) OVER 0.5 Steals | -245 (DraftKings via ESPN) | 1.2 | 67% | 67% | -0.06 |

**Combined probability 23.9%; parlay pays 3.3x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: DeMar DeRozan (DEN) UNDER 0.5 3-pointers made (75%); Derik Queen (NOP) UNDER 0.5 3-pointers made (70%); Dyson Daniels (ATL) UNDER 0.5 3-pointers made (69%). Combined probability 35.9%; parlay pays 2.3x; expected profit per 1 staked -0.16.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Hart (NYK) UNDER 9.5 Rebounds | -128 (DraftKings via ESPN) | 7.3 | 74% | 53% | +0.33 |
| Zion Williamson (NOP) UNDER 22.5 Points | -118 (DraftKings via ESPN) | 16.7 | 72% | 51% | +0.33 |

Combined probability 53.5%; parlay pays 3.3x; expected profit per 1 staked +0.76.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Hart (NYK) UNDER 9.5 Rebounds | -128 (DraftKings via ESPN) | 7.3 | 74% | 53% | +0.33 |
| Zion Williamson (NOP) UNDER 22.5 Points | -118 (DraftKings via ESPN) | 16.7 | 72% | 51% | +0.33 |
| Brayden Burries (MIL) UNDER 2.5 Assists | +101 (DraftKings via ESPN) | 2.2 | 62% | 47% | +0.25 |

Combined probability 33.3%; parlay pays 6.6x; expected profit per 1 staked +1.20.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Hart (NYK) UNDER 9.5 Rebounds | -128 (DraftKings via ESPN) | 7.3 | 74% | 53% | +0.33 |
| Zion Williamson (NOP) UNDER 22.5 Points | -118 (DraftKings via ESPN) | 16.7 | 72% | 51% | +0.33 |
| Brayden Burries (MIL) UNDER 2.5 Assists | +101 (DraftKings via ESPN) | 2.2 | 62% | 47% | +0.25 |
| Miles Bridges (PHX) UNDER 13.5 Points | -101 (DraftKings via ESPN) | 12.2 | 62% | 47% | +0.24 |

Combined probability 20.8%; parlay pays 13.2x; expected profit per 1 staked +1.73.

Top single picks by model edge:

- Josh Hart (NYK) UNDER 9.5 Rebounds: model 74% vs book 53%, EV +0.33 at -128 (projection 7.3)
- Zion Williamson (NOP) UNDER 22.5 Points: model 72% vs book 51%, EV +0.33 at -118 (projection 16.7)
- Jeremiah Fears (NOP) UNDER 6.5 Assists: model 73% vs book 54%, EV +0.27 at -137 (projection 5.0)
- Josh Hart (NYK) OVER 10.5 Points: model 62% vs book 47%, EV +0.25 at +102 (projection 13.0)
- Brayden Burries (MIL) UNDER 2.5 Assists: model 62% vs book 47%, EV +0.25 at +101 (projection 2.2)
- Miles Bridges (PHX) UNDER 13.5 Points: model 62% vs book 47%, EV +0.24 at -101 (projection 12.2)
- Ryan Rollins (MIL) UNDER 3.5 Assists: model 66% vs book 50%, EV +0.23 at -115 (projection 2.5)
- Nikola Jokic (DEN) UNDER 26.5 Points: model 66% vs book 51%, EV +0.23 at -117 (projection 23.5)
- Quentin Grimes (LAL) OVER 11.5 Points: model 62% vs book 48%, EV +0.22 at -103 (projection 14.1)
- Quentin Grimes (LAL) OVER 3.5 Rebounds: model 53% vs book 41%, EV +0.21 at +127 (projection 3.8)
- Matisse Thybulle (LAL) OVER 2.5 Rebounds: model 54% vs book 42%, EV +0.19 at +122 (projection 2.8)
- Kel'el Ware (MIL) UNDER 9.5 Points: model 65% vs book 52%, EV +0.18 at -122 (projection 8.3)

## MIA at NYK (game 401909326)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Hart (NYK) UNDER 0.5 Blocks | -242 (DraftKings via ESPN) | 0.2 | 66% | 66% | -0.06 |
| Giannis Antetokounmpo (MIA) OVER 0.5 Blocks | -231 (DraftKings via ESPN) | 0.8 | 65% | 65% | -0.06 |
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -224 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |

Combined probability 28.2%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Josh Hart (NYK) UNDER 0.5 Blocks: 66%, EV -0.06 at -242
- Giannis Antetokounmpo (MIA) OVER 0.5 Blocks: 65%, EV -0.06 at -231
- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -224
- Andrew Wiggins (MIA) OVER 0.5 3-pointers made: 64%, EV -0.06 at -218
- Giannis Antetokounmpo (MIA) UNDER 0.5 3-pointers made: 64%, EV -0.06 at -212
- Bobby Portis (MIA) OVER 0.5 3-pointers made: 63%, EV -0.06 at -208
- Davion Mitchell (MIA) OVER 0.5 Steals: 62%, EV -0.06 at -199
- Mikal Bridges (NYK) OVER 0.5 Steals: 61%, EV -0.06 at -191

## MIL at DET (game 401909327)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ausar Thompson (DET) OVER 0.5 Blocks | -228 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -225 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| John Collins (DET) UNDER 1.5 3-pointers made | -203 (DraftKings via ESPN) | 1.6 | 63% | 63% | -0.06 |

Combined probability 26.6%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Ausar Thompson (DET) OVER 0.5 Blocks: 65%, EV -0.06 at -228
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -225
- John Collins (DET) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Paul Reed (DET) OVER 1.5 Assists: 62%, EV -0.06 at -191
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Daniss Jenkins (DET) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -177
- Kevin Huerter (DET) OVER 1.5 3-pointers made: 58%, EV -0.06 at -166
- Tyler Herro (MIL) UNDER 4.5 Assists: 57%, EV -0.06 at -157

## PHI at IND (game 401909328)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| LeBron James (PHI) OVER 0.5 Steals | -212 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made | -171 (DraftKings via ESPN) | 1.4 | 59% | 59% | -0.06 |

Combined probability 24.8%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Tyrese Maxey (PHI) UNDER 1.5 Steals: 66%, EV -0.06 at -237
- LeBron James (PHI) OVER 0.5 Steals: 64%, EV -0.06 at -212
- LeBron James (PHI) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -201
- Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -169
- Ivica Zubac (IND) OVER 1.5 Assists: 59%, EV -0.06 at -168
- Pascal Siakam (IND) UNDER 3.5 Assists: 58%, EV -0.06 at -161
- VJ Edgecombe (PHI) UNDER 4.5 Assists: 57%, EV -0.06 at -156

## BKN at TOR (game 401909329)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Scottie Barnes (TOR) UNDER 1.5 3-pointers made | -242 (DraftKings via ESPN) | 1.1 | 67% | 67% | -0.06 |
| Noah Clowney (BKN) UNDER 1.5 Assists | -241 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Collin Murray-Boyles (TOR) OVER 1.5 Assists | -193 (DraftKings via ESPN) | 1.9 | 62% | 62% | -0.06 |

Combined probability 27.3%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Scottie Barnes (TOR) UNDER 1.5 3-pointers made: 67%, EV -0.06 at -242
- Noah Clowney (BKN) UNDER 1.5 Assists: 66%, EV -0.06 at -241
- Noah Clowney (BKN) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -208
- Collin Murray-Boyles (TOR) OVER 1.5 Assists: 62%, EV -0.06 at -193
- Jakob Poeltl (TOR) UNDER 2.5 Assists: 61%, EV -0.06 at -187
- Danny Wolf (BKN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -182
- Ja'Kobe Walter (TOR) OVER 1.5 Assists: 60%, EV -0.06 at -176
- Mikel Brown Jr. (BKN) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -168

## ATL at BOS (game 401909330)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dyson Daniels (ATL) UNDER 0.5 3-pointers made | -275 (DraftKings via ESPN) | 0.6 | 69% | 69% | -0.06 |
| Luguentz Dort (ATL) UNDER 1.5 Assists | -232 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Derrick White (BOS) OVER 0.5 Steals | -229 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 29.5%; parlay pays 2.8x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dyson Daniels (ATL) UNDER 0.5 3-pointers made: 69%, EV -0.06 at -275
- Dyson Daniels (ATL) UNDER 0.5 Blocks: 67%, EV -0.06 at -247
- Luguentz Dort (ATL) UNDER 1.5 Assists: 66%, EV -0.06 at -232
- Derrick White (BOS) OVER 0.5 Steals: 65%, EV -0.06 at -229
- Sam Hauser (BOS) UNDER 1.5 Assists: 64%, EV -0.06 at -217
- Baylor Scheierman (BOS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -217
- Nickeil Alexander-Walker (ATL) UNDER 0.5 Blocks: 64%, EV -0.06 at -218
- Jayson Tatum (BOS) UNDER 1.5 Steals: 64%, EV -0.06 at -215

## DAL at PHX (game 401909332)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Caleb Martin (DAL) OVER 0.5 3-pointers made | -227 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Collin Gillespie (PHX) UNDER 2.5 3-pointers made | -192 (DraftKings via ESPN) | 1.9 | 62% | 62% | -0.06 |
| Zaccharie Risacher (DAL) OVER 0.5 3-pointers made | -176 (DraftKings via ESPN) | 1.1 | 60% | 60% | -0.06 |

Combined probability 24.0%; parlay pays 3.4x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Caleb Martin (DAL) OVER 0.5 3-pointers made: 65%, EV -0.06 at -227
- Collin Gillespie (PHX) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -192
- Zaccharie Risacher (DAL) OVER 0.5 3-pointers made: 60%, EV -0.06 at -176
- Collin Gillespie (PHX) UNDER 3.5 Rebounds: 59%, EV -0.06 at -173
- Jordan Goodwin (PHX) UNDER 2.5 Assists: 59%, EV -0.06 at -171
- Daniel Gafford (DAL) OVER 1.5 Assists: 59%, EV -0.06 at -167
- Dillon Brooks (PHX) OVER 1.5 Assists: 58%, EV -0.06 at -164
- Naji Marshall (DAL) OVER 2.5 Rebounds: 58%, EV -0.06 at -160

## LAL at SAS (game 401909333)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) OVER 0.5 Steals | -245 (DraftKings via ESPN) | 1.2 | 67% | 67% | -0.06 |
| Collin Sexton (LAL) OVER 0.5 3-pointers made | -199 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |
| Walker Kessler (LAL) OVER 0.5 Steals | -171 (DraftKings via ESPN) | 0.8 | 59% | 59% | -0.07 |

Combined probability 24.5%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Victor Wembanyama (SAS) OVER 0.5 Steals: 67%, EV -0.06 at -245
- Collin Sexton (LAL) OVER 0.5 3-pointers made: 62%, EV -0.06 at -199
- Victor Wembanyama (SAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Victor Wembanyama (SAS) UNDER 3.5 Assists: 59%, EV -0.06 at -173
- Walker Kessler (LAL) OVER 0.5 Steals: 59%, EV -0.07 at -171
- Quentin Grimes (LAL) UNDER 3.5 Rebounds: 59%, EV -0.06 at -168
- Matisse Thybulle (LAL) OVER 1.5 Steals: 58%, EV -0.07 at -167
- Victor Wembanyama (SAS) UNDER 3.5 Blocks: 58%, EV -0.07 at -164

## DEN at UTA (game 401909334)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| DeMar DeRozan (DEN) UNDER 0.5 3-pointers made | -377 (DraftKings via ESPN) | 0.5 | 75% | 75% | -0.06 |
| Aaron Gordon (DEN) UNDER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Jamal Murray (DEN) OVER 0.5 Steals | -197 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |

Combined probability 28.8%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- DeMar DeRozan (DEN) UNDER 0.5 3-pointers made: 75%, EV -0.06 at -377
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Jamal Murray (DEN) OVER 0.5 Steals: 62%, EV -0.06 at -197
- Cameron Johnson (DEN) UNDER 2.5 Assists: 62%, EV -0.06 at -192
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Keyonte George (UTA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -184
- Darryn Peterson (UTA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 59%, EV -0.06 at -172

## NOP at LAC (game 401909335)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derik Queen (NOP) UNDER 0.5 3-pointers made | -286 (DraftKings via ESPN) | 0.6 | 70% | 70% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 Steals | -240 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -217 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |

Combined probability 29.7%; parlay pays 2.8x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Derik Queen (NOP) UNDER 0.5 3-pointers made: 70%, EV -0.06 at -286
- Herbert Jones (NOP) UNDER 1.5 Steals: 66%, EV -0.06 at -240
- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 64%, EV -0.06 at -217
- Jeremiah Fears (NOP) UNDER 1.5 Steals: 64%, EV -0.06 at -214
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -212
- Derrick Jones Jr. (LAC) OVER 0.5 3-pointers made: 64%, EV -0.06 at -211
- Rui Hachimura (LAC) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Saddiq Bey (NOP) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181

## GSW at POR (game 401909336)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Clingan (POR) UNDER 1.5 3-pointers made | -227 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Draymond Green (GSW) OVER 0.5 3-pointers made | -195 (DraftKings via ESPN) | 0.8 | 62% | 62% | -0.06 |
| De'Anthony Melton (GSW) UNDER 2.5 3-pointers made | -191 (DraftKings via ESPN) | 1.8 | 62% | 62% | -0.06 |

Combined probability 24.9%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Donovan Clingan (POR) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -227
- Draymond Green (GSW) OVER 0.5 3-pointers made: 62%, EV -0.06 at -195
- De'Anthony Melton (GSW) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -191
- Sidy Cissoko (POR) OVER 1.5 Assists: 61%, EV -0.06 at -187
- Donovan Clingan (POR) OVER 1.5 Assists: 61%, EV -0.06 at -184
- Gui Santos (GSW) OVER 0.5 3-pointers made: 61%, EV -0.06 at -184
- Gui Santos (GSW) OVER 1.5 Assists: 60%, EV -0.06 at -178
- Draymond Green (GSW) OVER 4.5 Assists: 57%, EV -0.06 at -158
