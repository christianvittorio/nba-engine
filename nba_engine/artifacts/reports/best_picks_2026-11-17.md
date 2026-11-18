# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-18T03:22:30Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Stephon Castle (SAS) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Darryn Peterson (UTA) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Collin Murray-Boyles (TOR) UNDER 1.5 Blocks | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Sidy Cissoko (POR) OVER 0.5 3-pointers made | -236 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |

**Combined probability 19.3%; parlay pays 4.0x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Stephon Castle (SAS) UNDER 1.5 Steals (66%); Darryn Peterson (UTA) UNDER 1.5 Steals (66%); Collin Murray-Boyles (TOR) UNDER 1.5 Blocks (66%). Combined probability 29.2%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Green (UTA) UNDER 0.5 Steals | +119 (DraftKings via ESPN) | 0.4 | 71% | 43% | +0.56 |
| Sandro Mamukelashvili (LAL) UNDER 5.5 Rebounds | +107 (DraftKings via ESPN) | 4.1 | 71% | 45% | +0.47 |

Combined probability 50.6%; parlay pays 4.5x; expected profit per 1 staked +1.29.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Green (UTA) UNDER 0.5 Steals | +119 (DraftKings via ESPN) | 0.4 | 71% | 43% | +0.56 |
| Sandro Mamukelashvili (LAL) UNDER 5.5 Rebounds | +107 (DraftKings via ESPN) | 4.1 | 71% | 45% | +0.47 |
| Victor Wembanyama (SAS) UNDER 28.5 Points | -107 (DraftKings via ESPN) | 24.1 | 70% | 49% | +0.34 |

Combined probability 35.2%; parlay pays 8.8x; expected profit per 1 staked +2.09.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Green (UTA) UNDER 0.5 Steals | +119 (DraftKings via ESPN) | 0.4 | 71% | 43% | +0.56 |
| Sandro Mamukelashvili (LAL) UNDER 5.5 Rebounds | +107 (DraftKings via ESPN) | 4.1 | 71% | 45% | +0.47 |
| Victor Wembanyama (SAS) UNDER 28.5 Points | -107 (DraftKings via ESPN) | 24.1 | 70% | 49% | +0.34 |
| Jamal Shead (TOR) OVER 4.5 Assists | -109 (DraftKings via ESPN) | 5.8 | 67% | 49% | +0.28 |

Combined probability 23.6%; parlay pays 16.8x; expected profit per 1 staked +2.96.

Top single picks by model edge:

- Josh Green (UTA) UNDER 0.5 Steals: model 71% vs book 43%, EV +0.56 at +119 (projection 0.4)
- Sandro Mamukelashvili (LAL) UNDER 5.5 Rebounds: model 71% vs book 45%, EV +0.47 at +107 (projection 4.1)
- Victor Wembanyama (SAS) UNDER 28.5 Points: model 70% vs book 49%, EV +0.34 at -107 (projection 24.1)
- Mo Bamba (UTA) UNDER 10.5 Points: model 66% vs book 48%, EV +0.29 at -106 (projection 8.9)
- De'Aaron Fox (SAS) UNDER 5.5 Assists: model 72% vs book 52%, EV +0.29 at -125 (projection 3.6)
- Jamal Shead (TOR) OVER 4.5 Assists: model 67% vs book 49%, EV +0.28 at -109 (projection 5.8)
- Victor Wembanyama (SAS) UNDER 12.5 Rebounds: model 71% vs book 52%, EV +0.27 at -126 (projection 9.8)
- Mo Bamba (UTA) UNDER 0.5 Steals: model 66% vs book 49%, EV +0.26 at -109 (projection 0.4)
- Luka Doncic (LAL) UNDER 7.5 Rebounds: model 66% vs book 49%, EV +0.25 at -110 (projection 5.4)
- Keldon Johnson (SAS) OVER 9.5 Points: model 61% vs book 47%, EV +0.24 at +102 (projection 11.8)
- Josh Green (UTA) UNDER 2.5 Rebounds: model 71% vs book 54%, EV +0.23 at -136 (projection 1.8)
- Trey Lyles (MIN) UNDER 4.5 Rebounds: model 64% vs book 49%, EV +0.23 at -110 (projection 3.6)

## NYK at TOR (game 401910002)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Collin Murray-Boyles (TOR) UNDER 1.5 Blocks | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Ja'Kobe Walter (TOR) OVER 0.5 Steals | -215 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Jamal Shead (TOR) OVER 0.5 3-pointers made | -206 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |

Combined probability 26.7%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Collin Murray-Boyles (TOR) UNDER 1.5 Blocks: 66%, EV -0.06 at -239
- Ja'Kobe Walter (TOR) OVER 0.5 Steals: 64%, EV -0.06 at -215
- Jamal Shead (TOR) OVER 0.5 3-pointers made: 63%, EV -0.06 at -206
- Landry Shamet (NYK) UNDER 2.5 Rebounds: 61%, EV -0.06 at -190
- OG Anunoby (NYK) OVER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Mikal Bridges (NYK) OVER 0.5 3-pointers made: 60%, EV -0.06 at -180
- OG Anunoby (NYK) UNDER 1.5 Steals: 60%, EV -0.06 at -180
- Jalen Brunson (NYK) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -166

## POR at MIN (game 401910003)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Sidy Cissoko (POR) OVER 0.5 3-pointers made | -236 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Damian Lillard (POR) OVER 0.5 Steals | -198 (DraftKings via ESPN) | 0.8 | 62% | 62% | -0.06 |
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -197 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |

Combined probability 25.5%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Sidy Cissoko (POR) OVER 0.5 3-pointers made: 66%, EV -0.06 at -236
- Damian Lillard (POR) OVER 0.5 Steals: 62%, EV -0.06 at -198
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 62%, EV -0.06 at -197
- Toumani Camara (POR) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -194
- Scoot Henderson (POR) UNDER 2.5 Rebounds: 61%, EV -0.06 at -188
- Donovan Clingan (POR) OVER 1.5 Blocks: 61%, EV -0.06 at -185
- Donovan Clingan (POR) UNDER 2.5 Assists: 61%, EV -0.06 at -183
- Bones Hyland (MIN) UNDER 2.5 Rebounds: 60%, EV -0.06 at -180

## DET at SAS (game 401910004)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Stephon Castle (SAS) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -233 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |

Combined probability 28.9%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Stephon Castle (SAS) UNDER 1.5 Steals: 66%, EV -0.06 at -243
- Victor Wembanyama (SAS) UNDER 1.5 Steals: 66%, EV -0.06 at -239
- De'Aaron Fox (SAS) UNDER 1.5 Steals: 66%, EV -0.06 at -233
- Cade Cunningham (DET) UNDER 1.5 Steals: 65%, EV -0.06 at -229
- Kevin Huerter (DET) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -196
- Dylan Harper (SAS) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -195
- John Collins (DET) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -189
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -186

## CHA at LAL (game 401910005)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jake LaRavia (LAL) OVER 0.5 3-pointers made | -177 (DraftKings via ESPN) | 1.2 | 60% | 60% | -0.06 |
| Coby White (CHA) OVER 1.5 3-pointers made | -174 (DraftKings via ESPN) | 1.8 | 59% | 59% | -0.06 |
| Naz Reid (CHA) UNDER 2.5 3-pointers made | -172 (DraftKings via ESPN) | 2.5 | 59% | 59% | -0.06 |

Combined probability 21.1%; parlay pays 3.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jake LaRavia (LAL) OVER 0.5 3-pointers made: 60%, EV -0.06 at -177
- Coby White (CHA) OVER 1.5 3-pointers made: 59%, EV -0.06 at -174
- Naz Reid (CHA) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -172
- Sion James (CHA) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -169
- Matisse Thybulle (LAL) OVER 1.5 Steals: 58%, EV -0.06 at -166
- Sandro Mamukelashvili (LAL) OVER 1.5 Assists: 58%, EV -0.06 at -166
- Sion James (CHA) UNDER 4.5 Rebounds: 58%, EV -0.06 at -164
- Jake LaRavia (LAL) UNDER 2.5 Assists: 58%, EV -0.06 at -162

## UTA at LAC (game 401910006)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Darius Garland (LAC) OVER 0.5 Steals | -210 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |
| Keyonte George (UTA) OVER 0.5 Steals | -207 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |

Combined probability 26.6%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Darryn Peterson (UTA) UNDER 1.5 Steals: 66%, EV -0.06 at -242
- Darius Garland (LAC) OVER 0.5 Steals: 63%, EV -0.06 at -210
- Keyonte George (UTA) OVER 0.5 Steals: 63%, EV -0.06 at -207
- Brook Lopez (LAC) UNDER 1.5 Blocks: 62%, EV -0.06 at -199
- Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Keyonte George (UTA) OVER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Derrick Jones Jr. (LAC) OVER 0.5 Steals: 62%, EV -0.06 at -193
- Rui Hachimura (LAC) UNDER 1.5 Assists: 62%, EV -0.06 at -191
