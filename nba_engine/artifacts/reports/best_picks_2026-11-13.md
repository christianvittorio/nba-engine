# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-13T20:46:36Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) UNDER 0.5 Blocks | -249 (DraftKings via ESPN) | 0.4 | 67% | 67% | -0.06 |
| Dylan Harper (SAS) OVER 0.5 3-pointers made | -241 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Cedric Coward (MEM) UNDER 1.5 Steals | -238 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Darius Garland (LAC) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |

**Combined probability 19.3%; parlay pays 4.0x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Mikal Bridges (NYK) UNDER 0.5 Blocks (67%); Dylan Harper (SAS) OVER 0.5 3-pointers made (66%); Cedric Coward (MEM) UNDER 1.5 Steals (66%). Combined probability 29.3%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ajay Mitchell (OKC) UNDER 18.5 Points | -116 (DraftKings via ESPN) | 13.0 | 74% | 51% | +0.37 |
| Nate Ament (MIL) UNDER 8.5 Points | -110 (DraftKings via ESPN) | 6.6 | 71% | 49% | +0.36 |

Combined probability 52.5%; parlay pays 3.6x; expected profit per 1 staked +0.87.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ajay Mitchell (OKC) UNDER 18.5 Points | -116 (DraftKings via ESPN) | 13.0 | 74% | 51% | +0.37 |
| Nate Ament (MIL) UNDER 8.5 Points | -110 (DraftKings via ESPN) | 6.6 | 71% | 49% | +0.36 |
| Giannis Antetokounmpo (MIA) UNDER 29.5 Points | -111 (DraftKings via ESPN) | 24.9 | 71% | 50% | +0.34 |

Combined probability 37.1%; parlay pays 6.8x; expected profit per 1 staked +1.51.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ajay Mitchell (OKC) UNDER 18.5 Points | -116 (DraftKings via ESPN) | 13.0 | 74% | 51% | +0.37 |
| Nate Ament (MIL) UNDER 8.5 Points | -110 (DraftKings via ESPN) | 6.6 | 71% | 49% | +0.36 |
| Giannis Antetokounmpo (MIA) UNDER 29.5 Points | -111 (DraftKings via ESPN) | 24.9 | 71% | 50% | +0.34 |
| Darryn Peterson (UTA) UNDER 18.5 Points | -116 (DraftKings via ESPN) | 15.4 | 69% | 51% | +0.29 |

Combined probability 25.7%; parlay pays 12.6x; expected profit per 1 staked +2.23.

Top single picks by model edge:

- Ajay Mitchell (OKC) UNDER 18.5 Points: model 74% vs book 51%, EV +0.37 at -116 (projection 13.0)
- Nate Ament (MIL) UNDER 8.5 Points: model 71% vs book 49%, EV +0.36 at -110 (projection 6.6)
- Rui Hachimura (LAC) UNDER 14.5 Points: model 71% vs book 49%, EV +0.35 at -110 (projection 10.2)
- Brayden Burries (MIL) UNDER 2.5 Assists: model 67% vs book 46%, EV +0.35 at +102 (projection 2.0)
- Giannis Antetokounmpo (MIA) UNDER 29.5 Points: model 71% vs book 50%, EV +0.34 at -111 (projection 24.9)
- Brayden Burries (MIL) UNDER 11.5 Points: model 69% vs book 49%, EV +0.32 at -109 (projection 9.6)
- Andrew Wiggins (MIA) UNDER 11.5 Points: model 66% vs book 48%, EV +0.30 at -103 (projection 9.9)
- Rui Hachimura (LAC) UNDER 4.5 Rebounds: model 61% vs book 44%, EV +0.30 at +113 (projection 3.4)
- Darryn Peterson (UTA) UNDER 18.5 Points: model 69% vs book 51%, EV +0.29 at -116 (projection 15.4)
- Reed Sheppard (HOU) UNDER 11.5 Points: model 68% vs book 50%, EV +0.29 at -111 (projection 9.5)
- Ivica Zubac (IND) UNDER 9.5 Rebounds: model 67% vs book 49%, EV +0.27 at -111 (projection 6.7)
- Tyler Herro (MIL) UNDER 4.5 Assists: model 67% vs book 50%, EV +0.26 at -115 (projection 3.3)

## NYK at IND (game 401909296)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) UNDER 0.5 Blocks | -249 (DraftKings via ESPN) | 0.4 | 67% | 67% | -0.06 |
| OG Anunoby (NYK) UNDER 1.5 Steals | -212 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Ivica Zubac (IND) OVER 0.5 Blocks | -210 (DraftKings via ESPN) | 0.6 | 64% | 64% | -0.06 |

Combined probability 27.0%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Mikal Bridges (NYK) UNDER 0.5 Blocks: 67%, EV -0.06 at -249
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -228
- OG Anunoby (NYK) UNDER 1.5 Steals: 64%, EV -0.06 at -212
- Ivica Zubac (IND) OVER 0.5 Blocks: 64%, EV -0.06 at -210
- Aaron Nesmith (IND) OVER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Landry Shamet (NYK) UNDER 2.5 Rebounds: 62%, EV -0.06 at -191
- Andrew Nembhard (IND) OVER 0.5 Steals: 61%, EV -0.06 at -191
- Andrew Nembhard (IND) OVER 1.5 3-pointers made: 60%, EV -0.06 at -180

## MIL at ORL (game 401909297)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 1.5 Steals | -197 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -178 (DraftKings via ESPN) | 1.0 | 60% | 60% | -0.06 |
| Nate Ament (MIL) UNDER 1.5 3-pointers made | -178 (DraftKings via ESPN) | 0.8 | 60% | 60% | -0.06 |

Combined probability 22.3%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Franz Wagner (ORL) UNDER 1.5 Steals: 62%, EV -0.06 at -197
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Nate Ament (MIL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Desmond Bane (ORL) OVER 2.5 Assists: 59%, EV -0.06 at -166
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -160
- Anthony Black (ORL) OVER 4.5 Rebounds: 57%, EV -0.06 at -152
- Myles Turner (MIL) OVER 1.5 Assists: 56%, EV -0.06 at -152
- Myles Turner (MIL) UNDER 5.5 Rebounds: 56%, EV -0.06 at -149

## CLE at MIA (game 401909298)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Peyton Watson (CLE) UNDER 1.5 Blocks | -227 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -214 (DraftKings via ESPN) | 1.5 | 64% | 64% | -0.06 |
| Mario Hezonja (CLE) UNDER 1.5 3-pointers made | -208 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |

Combined probability 26.3%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Peyton Watson (CLE) UNDER 1.5 Blocks: 65%, EV -0.06 at -227
- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -214
- Mario Hezonja (CLE) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -208
- Tyrese Proctor (CLE) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -204
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 63%, EV -0.06 at -201
- Klay Thompson (MIA) UNDER 2.5 Rebounds: 62%, EV -0.06 at -191
- Klay Thompson (MIA) OVER 1.5 Assists: 61%, EV -0.06 at -187
- Peyton Watson (CLE) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184

## ATL at CHI (game 401909299)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nickeil Alexander-Walker (ATL) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 1.5 | 64% | 64% | -0.06 |
| Kingston Flemings (ATL) OVER 0.5 3-pointers made | -189 (DraftKings via ESPN) | 0.9 | 61% | 61% | -0.06 |
| Matas Buzelis (CHI) UNDER 2.5 Assists | -181 (DraftKings via ESPN) | 2.4 | 60% | 60% | -0.06 |

Combined probability 23.7%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Nickeil Alexander-Walker (ATL) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- Kingston Flemings (ATL) OVER 0.5 3-pointers made: 61%, EV -0.06 at -189
- Matas Buzelis (CHI) UNDER 2.5 Assists: 60%, EV -0.06 at -181
- Matas Buzelis (CHI) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -176
- Isaac Okoro (CHI) OVER 0.5 3-pointers made: 59%, EV -0.06 at -170
- Aaron Wiggins (ATL) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -166
- Jalen Smith (CHI) OVER 1.5 3-pointers made: 57%, EV -0.06 at -158
- Dyson Daniels (ATL) UNDER 0.5 3-pointers made: 57%, EV -0.06 at -155

## MEM at NOP (game 401909300)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) UNDER 1.5 Steals | -238 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Karlo Matkovic (NOP) OVER 0.5 3-pointers made | -214 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |

Combined probability 26.2%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Cedric Coward (MEM) UNDER 1.5 Steals: 66%, EV -0.06 at -238
- Karlo Matkovic (NOP) OVER 0.5 3-pointers made: 64%, EV -0.06 at -214
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Saddiq Bey (NOP) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Jaylen Wells (MEM) OVER 2.5 Rebounds: 59%, EV -0.06 at -170
- Zion Williamson (NOP) UNDER 3.5 Assists: 59%, EV -0.06 at -167
- Cameron Boozer (MEM) OVER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Cam Spencer (MEM) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -163

## UTA at HOU (game 401909301)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jaxson Hayes (UTA) UNDER 1.5 Blocks | -232 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Josh Green (UTA) OVER 0.5 3-pointers made | -207 (DraftKings via ESPN) | 0.8 | 63% | 63% | -0.06 |
| Tari Eason (HOU) UNDER 1.5 3-pointers made | -206 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |

Combined probability 26.2%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jaxson Hayes (UTA) UNDER 1.5 Blocks: 66%, EV -0.06 at -232
- Josh Green (UTA) OVER 0.5 3-pointers made: 63%, EV -0.06 at -207
- Tari Eason (HOU) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Fred VanVleet (HOU) UNDER 1.5 Steals: 63%, EV -0.06 at -204
- Keyonte George (UTA) OVER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Josh Green (UTA) UNDER 2.5 Rebounds: 61%, EV -0.06 at -190
- Amen Thompson (HOU) UNDER 1.5 Steals: 60%, EV -0.06 at -178
- Ace Bailey (UTA) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -174

## GSW at SAS (game 401909302)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dylan Harper (SAS) OVER 0.5 3-pointers made | -241 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Stephon Castle (SAS) UNDER 1.5 Steals | -231 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 28.6%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Dylan Harper (SAS) OVER 0.5 3-pointers made: 66%, EV -0.06 at -241
- Victor Wembanyama (SAS) UNDER 1.5 Steals: 66%, EV -0.06 at -237
- Stephon Castle (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -231
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Draymond Green (GSW) OVER 0.5 Steals: 62%, EV -0.06 at -197
- De'Anthony Melton (GSW) OVER 1.5 3-pointers made: 62%, EV -0.06 at -193
- De'Aaron Fox (SAS) UNDER 1.5 Steals: 61%, EV -0.06 at -191
- Yaxel Lendeborg (GSW) OVER 0.5 Steals: 60%, EV -0.07 at -180

## POR at SAC (game 401909303)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Toumani Camara (POR) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -205 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |
| Scoot Henderson (POR) UNDER 2.5 Assists | -189 (DraftKings via ESPN) | 2.7 | 61% | 61% | -0.06 |

Combined probability 25.2%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Toumani Camara (POR) UNDER 1.5 Steals: 65%, EV -0.06 at -226
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 63%, EV -0.06 at -205
- Scoot Henderson (POR) UNDER 2.5 Assists: 61%, EV -0.06 at -189
- Scoot Henderson (POR) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Scoot Henderson (POR) UNDER 2.5 Rebounds: 61%, EV -0.06 at -183
- Sidy Cissoko (POR) UNDER 2.5 Assists: 61%, EV -0.06 at -183
- Deni Avdija (POR) OVER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Donovan Clingan (POR) OVER 1.5 Assists: 60%, EV -0.06 at -175

## OKC at LAC (game 401909304)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darius Garland (LAC) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Brook Lopez (LAC) UNDER 1.5 Blocks | -225 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Rui Hachimura (LAC) UNDER 1.5 Assists | -205 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Darius Garland (LAC) UNDER 1.5 Steals: 66%, EV -0.06 at -236
- Brook Lopez (LAC) UNDER 1.5 Blocks: 65%, EV -0.06 at -225
- Brook Lopez (LAC) UNDER 1.5 Assists: 64%, EV -0.06 at -218
- Rui Hachimura (LAC) UNDER 1.5 Assists: 63%, EV -0.06 at -205
- Ajay Mitchell (OKC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -200
- Alex Caruso (OKC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 61%, EV -0.07 at -191
