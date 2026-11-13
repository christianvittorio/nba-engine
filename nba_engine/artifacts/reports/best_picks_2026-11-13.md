# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-13T16:59:54Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dylan Harper (SAS) UNDER 1.5 3-pointers made | -245 (DraftKings via ESPN) | 1.3 | 67% | 67% | -0.06 |
| Cedric Coward (MEM) OVER 0.5 Steals | -242 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Darius Garland (LAC) OVER 0.5 Steals | -234 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Mikal Bridges (NYK) UNDER 1.5 3-pointers made | -232 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |

**Combined probability 19.1%; parlay pays 4.1x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Dylan Harper (SAS) UNDER 1.5 3-pointers made (67%); Cedric Coward (MEM) OVER 0.5 Steals (66%); Darius Garland (LAC) OVER 0.5 Steals (66%). Combined probability 29.1%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Domantas Sabonis (SAC) UNDER 5.5 Assists | +114 (DraftKings via ESPN) | 3.8 | 70% | 44% | +0.49 |
| Rui Hachimura (LAC) UNDER 14.5 Points | -104 (DraftKings via ESPN) | 10.2 | 71% | 48% | +0.39 |

Combined probability 49.3%; parlay pays 4.2x; expected profit per 1 staked +1.07.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Domantas Sabonis (SAC) UNDER 5.5 Assists | +114 (DraftKings via ESPN) | 3.8 | 70% | 44% | +0.49 |
| Rui Hachimura (LAC) UNDER 14.5 Points | -104 (DraftKings via ESPN) | 10.2 | 71% | 48% | +0.39 |
| Nate Ament (MIL) UNDER 8.5 Points | -111 (DraftKings via ESPN) | 6.6 | 71% | 50% | +0.36 |

Combined probability 35.2%; parlay pays 8.0x; expected profit per 1 staked +1.81.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Domantas Sabonis (SAC) UNDER 5.5 Assists | +114 (DraftKings via ESPN) | 3.8 | 70% | 44% | +0.49 |
| Rui Hachimura (LAC) UNDER 14.5 Points | -104 (DraftKings via ESPN) | 10.2 | 71% | 48% | +0.39 |
| Nate Ament (MIL) UNDER 8.5 Points | -111 (DraftKings via ESPN) | 6.6 | 71% | 50% | +0.36 |
| Darryn Peterson (UTA) UNDER 18.5 Points | -107 (DraftKings via ESPN) | 15.4 | 69% | 49% | +0.34 |

Combined probability 24.3%; parlay pays 15.4x; expected profit per 1 staked +2.76.

Top single picks by model edge:

- Domantas Sabonis (SAC) UNDER 5.5 Assists: model 70% vs book 44%, EV +0.49 at +114 (projection 3.8)
- Rui Hachimura (LAC) UNDER 14.5 Points: model 71% vs book 48%, EV +0.39 at -104 (projection 10.2)
- Nate Ament (MIL) UNDER 8.5 Points: model 71% vs book 50%, EV +0.36 at -111 (projection 6.6)
- Darryn Peterson (UTA) UNDER 18.5 Points: model 69% vs book 49%, EV +0.34 at -107 (projection 15.4)
- Reed Sheppard (HOU) UNDER 11.5 Points: model 68% vs book 48%, EV +0.33 at -104 (projection 9.5)
- Giannis Antetokounmpo (MIA) UNDER 29.5 Points: model 71% vs book 51%, EV +0.30 at -120 (projection 24.9)
- Brayden Burries (MIL) UNDER 11.5 Points: model 69% vs book 50%, EV +0.30 at -114 (projection 9.6)
- Rui Hachimura (LAC) UNDER 4.5 Rebounds: model 61% vs book 44%, EV +0.29 at +112 (projection 3.4)
- James Harden (CLE) OVER 17.5 Points: model 65% vs book 48%, EV +0.27 at -104 (projection 21.3)
- Ivica Zubac (IND) UNDER 12.5 Points: model 65% vs book 48%, EV +0.27 at -105 (projection 9.5)
- Jeremiah Fears (NOP) UNDER 5.5 Assists: model 70% vs book 52%, EV +0.26 at -125 (projection 4.4)
- Tyler Herro (MIL) UNDER 4.5 Assists: model 67% vs book 51%, EV +0.24 at -118 (projection 3.3)

## NYK at IND (game 401909296)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) UNDER 1.5 3-pointers made | -232 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Ivica Zubac (IND) OVER 0.5 Blocks | -227 (DraftKings via ESPN) | 0.6 | 65% | 65% | -0.06 |
| OG Anunoby (NYK) UNDER 1.5 Steals | -224 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |

Combined probability 27.7%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -232
- Ivica Zubac (IND) OVER 0.5 Blocks: 65%, EV -0.06 at -227
- OG Anunoby (NYK) UNDER 1.5 Steals: 65%, EV -0.06 at -224
- Landry Shamet (NYK) UNDER 2.5 Rebounds: 62%, EV -0.06 at -191
- Mikal Bridges (NYK) OVER 1.5 Assists: 61%, EV -0.06 at -185
- Ivica Zubac (IND) OVER 1.5 Assists: 61%, EV -0.06 at -185
- Andrew Nembhard (IND) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- OG Anunoby (NYK) OVER 1.5 3-pointers made: 60%, EV -0.06 at -175

## MIL at ORL (game 401909297)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -189 (DraftKings via ESPN) | 1.0 | 61% | 61% | -0.06 |
| Franz Wagner (ORL) UNDER 1.5 Steals | -187 (DraftKings via ESPN) | 1.3 | 61% | 61% | -0.06 |
| Desmond Bane (ORL) UNDER 3.5 Assists | -176 (DraftKings via ESPN) | 3.2 | 60% | 60% | -0.06 |

Combined probability 22.3%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Franz Wagner (ORL) UNDER 1.5 Steals: 61%, EV -0.06 at -187
- Desmond Bane (ORL) UNDER 3.5 Assists: 60%, EV -0.06 at -176
- Nate Ament (MIL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Brayden Burries (MIL) UNDER 3.5 Assists: 59%, EV -0.06 at -173
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -169
- Myles Turner (MIL) UNDER 5.5 Rebounds: 56%, EV -0.06 at -149
- Anthony Black (ORL) UNDER 1.5 Steals: 56%, EV -0.06 at -147

## CLE at MIA (game 401909298)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Peyton Watson (CLE) UNDER 1.5 Blocks | -226 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Tyrese Proctor (CLE) UNDER 1.5 3-pointers made | -215 (DraftKings via ESPN) | 1.6 | 64% | 64% | -0.06 |
| Pelle Larsson (MIA) UNDER 1.5 3-pointers made | -209 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 26.4%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Peyton Watson (CLE) UNDER 1.5 Blocks: 65%, EV -0.06 at -226
- Tyrese Proctor (CLE) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -215
- Pelle Larsson (MIA) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -209
- Mario Hezonja (CLE) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -197
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 62%, EV -0.06 at -193
- Meleek Thomas (CLE) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -190
- Peyton Watson (CLE) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Davion Mitchell (MIA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185

## ATL at CHI (game 401909299)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nickeil Alexander-Walker (ATL) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 1.5 | 64% | 64% | -0.06 |
| Kingston Flemings (ATL) OVER 0.5 3-pointers made | -188 (DraftKings via ESPN) | 0.9 | 61% | 61% | -0.06 |
| Matas Buzelis (CHI) UNDER 2.5 Assists | -181 (DraftKings via ESPN) | 2.4 | 60% | 60% | -0.06 |

Combined probability 23.7%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Nickeil Alexander-Walker (ATL) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- Kingston Flemings (ATL) OVER 0.5 3-pointers made: 61%, EV -0.06 at -188
- Matas Buzelis (CHI) UNDER 2.5 Assists: 60%, EV -0.06 at -181
- Aaron Wiggins (ATL) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Isaac Okoro (CHI) OVER 0.5 3-pointers made: 59%, EV -0.06 at -170
- Matas Buzelis (CHI) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -170
- Dyson Daniels (ATL) UNDER 0.5 3-pointers made: 58%, EV -0.06 at -162
- Jalen Smith (CHI) OVER 1.5 3-pointers made: 57%, EV -0.06 at -158

## MEM at NOP (game 401909300)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) OVER 0.5 Steals | -242 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Dejounte Murray (NOP) OVER 0.5 3-pointers made | -218 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |
| Cam Spencer (MEM) UNDER 1.5 3-pointers made | -163 (DraftKings via ESPN) | 1.4 | 58% | 58% | -0.06 |

Combined probability 24.9%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Cedric Coward (MEM) OVER 0.5 Steals: 66%, EV -0.06 at -242
- Dejounte Murray (NOP) OVER 0.5 3-pointers made: 64%, EV -0.06 at -218
- Cam Spencer (MEM) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -163
- Zion Williamson (NOP) OVER 2.5 Assists: 58%, EV -0.06 at -160
- Ty Jerome (MEM) UNDER 3.5 Rebounds: 57%, EV -0.06 at -156
- Saddiq Bey (NOP) OVER 1.5 3-pointers made: 57%, EV -0.06 at -154
- Saddiq Bey (NOP) OVER 3.5 Rebounds: 57%, EV -0.06 at -152
- Ty Jerome (MEM) UNDER 5.5 Assists: 56%, EV -0.06 at -152

## UTA at HOU (game 401909301)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Green (UTA) OVER 0.5 3-pointers made | -232 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Jaxson Hayes (UTA) UNDER 1.5 Blocks | -232 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Tari Eason (HOU) UNDER 1.5 3-pointers made | -211 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

Combined probability 27.4%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Josh Green (UTA) OVER 0.5 3-pointers made: 66%, EV -0.06 at -232
- Jaxson Hayes (UTA) UNDER 1.5 Blocks: 66%, EV -0.06 at -232
- Tari Eason (HOU) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -211
- Fred VanVleet (HOU) UNDER 1.5 Steals: 63%, EV -0.06 at -204
- Keyonte George (UTA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Ace Bailey (UTA) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -180
- Darryn Peterson (UTA) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -177
- Amen Thompson (HOU) UNDER 1.5 Steals: 60%, EV -0.06 at -178

## GSW at SAS (game 401909302)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dylan Harper (SAS) UNDER 1.5 3-pointers made | -245 (DraftKings via ESPN) | 1.3 | 67% | 67% | -0.06 |
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -229 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Stephon Castle (SAS) UNDER 1.5 Steals | -221 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 28.1%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dylan Harper (SAS) UNDER 1.5 3-pointers made: 67%, EV -0.06 at -245
- Victor Wembanyama (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -229
- Stephon Castle (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -221
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -218
- Draymond Green (GSW) OVER 0.5 Steals: 62%, EV -0.06 at -198
- De'Anthony Melton (GSW) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -194
- De'Aaron Fox (SAS) UNDER 1.5 Steals: 61%, EV -0.06 at -189
- Yaxel Lendeborg (GSW) OVER 0.5 Steals: 60%, EV -0.06 at -182

## POR at SAC (game 401909303)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Toumani Camara (POR) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -205 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |
| Scoot Henderson (POR) UNDER 1.5 3-pointers made | -204 (DraftKings via ESPN) | 1.5 | 63% | 63% | -0.06 |

Combined probability 25.8%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Toumani Camara (POR) UNDER 1.5 Steals: 65%, EV -0.06 at -226
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 63%, EV -0.06 at -205
- Scoot Henderson (POR) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -204
- Scoot Henderson (POR) UNDER 2.5 Rebounds: 61%, EV -0.06 at -185
- Scoot Henderson (POR) UNDER 2.5 Assists: 61%, EV -0.06 at -184
- Donovan Clingan (POR) OVER 1.5 Assists: 60%, EV -0.06 at -181
- Sidy Cissoko (POR) UNDER 2.5 Assists: 60%, EV -0.06 at -176
- Deni Avdija (POR) OVER 1.5 3-pointers made: 59%, EV -0.06 at -173

## OKC at LAC (game 401909304)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darius Garland (LAC) OVER 0.5 Steals | -234 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Brook Lopez (LAC) UNDER 1.5 Assists | -218 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |
| Rui Hachimura (LAC) UNDER 1.5 Assists | -205 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |

Combined probability 26.6%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Darius Garland (LAC) OVER 0.5 Steals: 66%, EV -0.06 at -234
- Brook Lopez (LAC) UNDER 1.5 Assists: 64%, EV -0.06 at -218
- Brook Lopez (LAC) UNDER 1.5 Blocks: 64%, EV -0.06 at -218
- Rui Hachimura (LAC) UNDER 1.5 Assists: 63%, EV -0.06 at -205
- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 62%, EV -0.06 at -197
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Max Strus (LAC) UNDER 2.5 Assists: 61%, EV -0.06 at -184
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 61%, EV -0.06 at -184
