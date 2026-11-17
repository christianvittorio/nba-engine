# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-17T18:13:59Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Ja'Kobe Walter (TOR) OVER 0.5 Steals | -225 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Sidy Cissoko (POR) UNDER 1.5 3-pointers made | -221 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made | -198 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |

**Combined probability 17.0%; parlay pays 4.6x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Victor Wembanyama (SAS) UNDER 1.5 Steals (65%); Ja'Kobe Walter (TOR) OVER 0.5 Steals (65%); Sidy Cissoko (POR) UNDER 1.5 3-pointers made (65%). Combined probability 27.3%; parlay pays 3.0x; expected profit per 1 staked -0.18.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) UNDER 28.5 Points | -109 (DraftKings via ESPN) | 24.1 | 70% | 49% | +0.33 |
| Darryn Peterson (UTA) UNDER 21.5 Points | -108 (DraftKings via ESPN) | 18.3 | 69% | 49% | +0.33 |

Combined probability 47.9%; parlay pays 3.7x; expected profit per 1 staked +0.77.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) UNDER 28.5 Points | -109 (DraftKings via ESPN) | 24.1 | 70% | 49% | +0.33 |
| Darryn Peterson (UTA) UNDER 21.5 Points | -108 (DraftKings via ESPN) | 18.3 | 69% | 49% | +0.33 |
| Luka Doncic (LAL) UNDER 7.5 Rebounds | -108 (DraftKings via ESPN) | 5.4 | 66% | 49% | +0.26 |

Combined probability 31.4%; parlay pays 7.1x; expected profit per 1 staked +1.23.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) UNDER 28.5 Points | -109 (DraftKings via ESPN) | 24.1 | 70% | 49% | +0.33 |
| Darryn Peterson (UTA) UNDER 21.5 Points | -108 (DraftKings via ESPN) | 18.3 | 69% | 49% | +0.33 |
| Luka Doncic (LAL) UNDER 7.5 Rebounds | -108 (DraftKings via ESPN) | 5.4 | 66% | 49% | +0.26 |
| Terrence Shannon Jr. (MIN) UNDER 3.5 Rebounds | -106 (DraftKings via ESPN) | 2.6 | 61% | 48% | +0.19 |

Combined probability 19.2%; parlay pays 13.8x; expected profit per 1 staked +1.65.

Top single picks by model edge:

- Victor Wembanyama (SAS) UNDER 28.5 Points: model 70% vs book 49%, EV +0.33 at -109 (projection 24.1)
- Darryn Peterson (UTA) UNDER 21.5 Points: model 69% vs book 49%, EV +0.33 at -108 (projection 18.3)
- De'Aaron Fox (SAS) UNDER 5.5 Assists: model 72% vs book 51%, EV +0.32 at -119 (projection 3.6)
- Victor Wembanyama (SAS) UNDER 12.5 Rebounds: model 71% vs book 52%, EV +0.27 at -127 (projection 9.8)
- Luka Doncic (LAL) UNDER 7.5 Rebounds: model 66% vs book 49%, EV +0.26 at -108 (projection 5.4)
- Rui Hachimura (LAC) UNDER 13.5 Points: model 61% vs book 47%, EV +0.23 at +100 (projection 12.2)
- Ausar Thompson (DET) UNDER 7.5 Rebounds: model 67% vs book 51%, EV +0.22 at -120 (projection 6.1)
- Paul Reed (DET) OVER 10.5 Points: model 67% vs book 53%, EV +0.20 at -127 (projection 13.8)
- Rui Hachimura (LAC) UNDER 4.5 Rebounds: model 55% vs book 43%, EV +0.20 at +118 (projection 4.2)
- Grayson Allen (CHA) OVER 13.5 Points: model 63% vs book 50%, EV +0.19 at -114 (projection 16.7)
- Terrence Shannon Jr. (MIN) UNDER 3.5 Rebounds: model 61% vs book 48%, EV +0.19 at -106 (projection 2.6)
- Damian Lillard (POR) UNDER 20.5 Points: model 62% vs book 49%, EV +0.18 at -110 (projection 18.7)

## NYK at TOR (game 401910002)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ja'Kobe Walter (TOR) OVER 0.5 Steals | -225 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| OG Anunoby (NYK) UNDER 1.5 Steals | -214 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Collin Murray-Boyles (TOR) UNDER 1.5 Blocks | -213 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 26.4%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ja'Kobe Walter (TOR) OVER 0.5 Steals: 65%, EV -0.06 at -225
- OG Anunoby (NYK) UNDER 1.5 Steals: 64%, EV -0.06 at -214
- Collin Murray-Boyles (TOR) UNDER 1.5 Blocks: 64%, EV -0.06 at -213
- Mikal Bridges (NYK) OVER 0.5 3-pointers made: 62%, EV -0.06 at -195
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -187
- Landry Shamet (NYK) UNDER 2.5 Rebounds: 59%, EV -0.06 at -172
- Jalen Brunson (NYK) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -161
- OG Anunoby (NYK) OVER 1.5 Assists: 58%, EV -0.06 at -160

## POR at MIN (game 401910003)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Sidy Cissoko (POR) UNDER 1.5 3-pointers made | -221 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Damian Lillard (POR) OVER 0.5 Steals | -216 (DraftKings via ESPN) | 0.7 | 64% | 64% | -0.06 |
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -195 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |

Combined probability 25.6%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Sidy Cissoko (POR) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -221
- Damian Lillard (POR) OVER 0.5 Steals: 64%, EV -0.06 at -216
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 62%, EV -0.06 at -195
- Scoot Henderson (POR) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Toumani Camara (POR) OVER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Donovan Clingan (POR) UNDER 2.5 Blocks: 61%, EV -0.06 at -183
- Damian Lillard (POR) UNDER 3.5 3-pointers made: 60%, EV -0.06 at -177
- Ayo Dosunmu (MIN) OVER 2.5 Assists: 59%, EV -0.06 at -167

## DET at SAS (game 401910004)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |
| Julian Champagnie (SAS) OVER 1.5 3-pointers made | -179 (DraftKings via ESPN) | 1.8 | 60% | 60% | -0.06 |

Combined probability 24.2%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Victor Wembanyama (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -226
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Julian Champagnie (SAS) OVER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Dylan Harper (SAS) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Daniss Jenkins (DET) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Julian Champagnie (SAS) UNDER 1.5 Assists: 59%, EV -0.06 at -173
- Cade Cunningham (DET) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -168
- Victor Wembanyama (SAS) OVER 1.5 3-pointers made: 59%, EV -0.06 at -168

## CHA at LAL (game 401910005)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Naz Reid (CHA) OVER 1.5 3-pointers made | -184 (DraftKings via ESPN) | 2.5 | 61% | 61% | -0.06 |
| Sion James (CHA) UNDER 1.5 3-pointers made | -180 (DraftKings via ESPN) | 1.6 | 60% | 60% | -0.06 |
| Coby White (CHA) OVER 1.5 3-pointers made | -171 (DraftKings via ESPN) | 1.8 | 59% | 59% | -0.06 |

Combined probability 21.6%; parlay pays 3.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Naz Reid (CHA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Sion James (CHA) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Coby White (CHA) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Grayson Allen (CHA) OVER 2.5 Rebounds: 59%, EV -0.06 at -169
- Jake LaRavia (LAL) OVER 0.5 3-pointers made: 59%, EV -0.06 at -167
- Matisse Thybulle (LAL) OVER 1.5 Steals: 58%, EV -0.07 at -164
- Sion James (CHA) OVER 2.5 Assists: 57%, EV -0.06 at -157
- Jake LaRavia (LAL) UNDER 4.5 Rebounds: 56%, EV -0.06 at -147

## UTA at LAC (game 401910006)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made | -198 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| Rui Hachimura (LAC) OVER 1.5 3-pointers made | -189 (DraftKings via ESPN) | 1.7 | 61% | 61% | -0.06 |
| Keyonte George (UTA) OVER 1.5 3-pointers made | -184 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |

Combined probability 23.2%; parlay pays 3.6x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Rui Hachimura (LAC) OVER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Keyonte George (UTA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Rui Hachimura (LAC) UNDER 1.5 Assists: 61%, EV -0.06 at -183
- Max Strus (LAC) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Keaton Wagler (LAC) OVER 2.5 Assists: 60%, EV -0.06 at -175
- Darius Garland (LAC) OVER 2.5 Rebounds: 59%, EV -0.06 at -168
- Keaton Wagler (LAC) UNDER 3.5 Rebounds: 58%, EV -0.06 at -163
