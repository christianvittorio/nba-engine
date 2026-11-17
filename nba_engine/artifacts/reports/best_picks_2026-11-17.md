# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-17T22:01:24Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Sidy Cissoko (POR) UNDER 1.5 3-pointers made | -229 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Ja'Kobe Walter (TOR) OVER 0.5 Steals | -225 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -222 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

**Combined probability 18.2%; parlay pays 4.3x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Darryn Peterson (UTA) UNDER 1.5 Steals (66%); Sidy Cissoko (POR) UNDER 1.5 3-pointers made (65%); Ja'Kobe Walter (TOR) OVER 0.5 Steals (65%). Combined probability 28.2%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Green (UTA) UNDER 0.5 Steals | +119 (DraftKings via ESPN) | 0.4 | 71% | 43% | +0.56 |
| Victor Wembanyama (SAS) UNDER 12.5 Rebounds | -119 (DraftKings via ESPN) | 9.8 | 71% | 51% | +0.31 |

Combined probability 50.5%; parlay pays 4.0x; expected profit per 1 staked +1.03.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Green (UTA) UNDER 0.5 Steals | +119 (DraftKings via ESPN) | 0.4 | 71% | 43% | +0.56 |
| Victor Wembanyama (SAS) UNDER 12.5 Rebounds | -119 (DraftKings via ESPN) | 9.8 | 71% | 51% | +0.31 |
| Ayo Dosunmu (MIN) OVER 3.5 Assists | +126 (DraftKings via ESPN) | 4.0 | 57% | 41% | +0.29 |

Combined probability 28.7%; parlay pays 9.1x; expected profit per 1 staked +1.62.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Green (UTA) UNDER 0.5 Steals | +119 (DraftKings via ESPN) | 0.4 | 71% | 43% | +0.56 |
| Victor Wembanyama (SAS) UNDER 12.5 Rebounds | -119 (DraftKings via ESPN) | 9.8 | 71% | 51% | +0.31 |
| Ayo Dosunmu (MIN) OVER 3.5 Assists | +126 (DraftKings via ESPN) | 4.0 | 57% | 41% | +0.29 |
| Luka Doncic (LAL) UNDER 7.5 Rebounds | -114 (DraftKings via ESPN) | 5.4 | 66% | 50% | +0.23 |

Combined probability 18.8%; parlay pays 17.1x; expected profit per 1 staked +2.22.

Top single picks by model edge:

- Josh Green (UTA) UNDER 0.5 Steals: model 71% vs book 43%, EV +0.56 at +119 (projection 0.4)
- Mo Bamba (UTA) UNDER 0.5 Steals: model 66% vs book 46%, EV +0.32 at +101 (projection 0.4)
- Victor Wembanyama (SAS) UNDER 12.5 Rebounds: model 71% vs book 51%, EV +0.31 at -119 (projection 9.8)
- Victor Wembanyama (SAS) UNDER 28.5 Points: model 70% vs book 50%, EV +0.30 at -114 (projection 24.1)
- Ayo Dosunmu (MIN) OVER 3.5 Assists: model 57% vs book 41%, EV +0.29 at +126 (projection 4.0)
- De'Aaron Fox (SAS) UNDER 5.5 Assists: model 72% vs book 52%, EV +0.28 at -126 (projection 3.6)
- Mo Bamba (UTA) UNDER 10.5 Points: model 66% vs book 50%, EV +0.26 at -112 (projection 8.9)
- Darryn Peterson (UTA) UNDER 20.5 Points: model 63% vs book 48%, EV +0.24 at -104 (projection 18.3)
- Damian Lillard (POR) UNDER 21.5 Points: model 66% vs book 50%, EV +0.23 at -114 (projection 18.7)
- Luka Doncic (LAL) UNDER 7.5 Rebounds: model 66% vs book 50%, EV +0.23 at -114 (projection 5.4)
- Josh Green (UTA) UNDER 2.5 Rebounds: model 71% vs book 54%, EV +0.23 at -136 (projection 1.8)
- Terrence Shannon Jr. (MIN) UNDER 3.5 Rebounds: model 61% vs book 47%, EV +0.21 at -101 (projection 2.6)

## NYK at TOR (game 401910002)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ja'Kobe Walter (TOR) OVER 0.5 Steals | -225 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Collin Murray-Boyles (TOR) UNDER 1.5 Blocks | -213 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| OG Anunoby (NYK) UNDER 1.5 Steals | -209 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |

Combined probability 26.2%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ja'Kobe Walter (TOR) OVER 0.5 Steals: 65%, EV -0.06 at -225
- Collin Murray-Boyles (TOR) UNDER 1.5 Blocks: 64%, EV -0.06 at -213
- OG Anunoby (NYK) UNDER 1.5 Steals: 63%, EV -0.06 at -209
- Mikal Bridges (NYK) OVER 0.5 3-pointers made: 62%, EV -0.06 at -195
- Landry Shamet (NYK) UNDER 2.5 Rebounds: 61%, EV -0.06 at -188
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -186
- Jalen Brunson (NYK) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -161
- Ja'Kobe Walter (TOR) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -157

## POR at MIN (game 401910003)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Sidy Cissoko (POR) UNDER 1.5 3-pointers made | -229 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Damian Lillard (POR) OVER 0.5 Steals | -220 (DraftKings via ESPN) | 0.8 | 64% | 64% | -0.06 |
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -197 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |

Combined probability 26.2%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Sidy Cissoko (POR) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -229
- Damian Lillard (POR) OVER 0.5 Steals: 64%, EV -0.06 at -220
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 62%, EV -0.06 at -197
- Donovan Clingan (POR) OVER 1.5 Blocks: 62%, EV -0.06 at -195
- Toumani Camara (POR) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Jrue Holiday (POR) OVER 1.5 3-pointers made: 59%, EV -0.06 at -174
- Scoot Henderson (POR) UNDER 2.5 Rebounds: 59%, EV -0.06 at -174
- Donovan Clingan (POR) OVER 1.5 Assists: 59%, EV -0.06 at -170

## DET at SAS (game 401910004)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -222 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |
| Dylan Harper (SAS) UNDER 1.5 3-pointers made | -188 (DraftKings via ESPN) | 1.2 | 61% | 61% | -0.06 |

Combined probability 24.5%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Victor Wembanyama (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -222
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Dylan Harper (SAS) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Kevin Huerter (DET) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- Cade Cunningham (DET) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -183
- Julian Champagnie (SAS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -182
- John Collins (DET) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Victor Wembanyama (SAS) OVER 2.5 Assists: 59%, EV -0.06 at -171

## CHA at LAL (game 401910005)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Naz Reid (CHA) UNDER 2.5 3-pointers made | -187 (DraftKings via ESPN) | 2.5 | 61% | 61% | -0.06 |
| Jake LaRavia (LAL) OVER 0.5 3-pointers made | -187 (DraftKings via ESPN) | 1.2 | 61% | 61% | -0.06 |
| Sandro Mamukelashvili (LAL) OVER 1.5 Assists | -186 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |

Combined probability 22.7%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Naz Reid (CHA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -187
- Jake LaRavia (LAL) OVER 0.5 3-pointers made: 61%, EV -0.06 at -187
- Sandro Mamukelashvili (LAL) OVER 1.5 Assists: 61%, EV -0.06 at -186
- Jake LaRavia (LAL) UNDER 2.5 Assists: 61%, EV -0.06 at -185
- Matisse Thybulle (LAL) OVER 1.5 Steals: 60%, EV -0.07 at -181
- Coby White (CHA) OVER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Sion James (CHA) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -160
- Sion James (CHA) OVER 3.5 Rebounds: 57%, EV -0.06 at -158

## UTA at LAC (game 401910006)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Darius Garland (LAC) OVER 0.5 Steals | -230 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Derrick Jones Jr. (LAC) OVER 0.5 Steals | -210 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |

Combined probability 27.5%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Darryn Peterson (UTA) UNDER 1.5 Steals: 66%, EV -0.06 at -242
- Darius Garland (LAC) OVER 0.5 Steals: 65%, EV -0.06 at -230
- Derrick Jones Jr. (LAC) OVER 0.5 Steals: 63%, EV -0.06 at -210
- Brook Lopez (LAC) UNDER 1.5 Blocks: 63%, EV -0.06 at -208
- Keyonte George (UTA) OVER 0.5 Steals: 63%, EV -0.06 at -207
- Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Rui Hachimura (LAC) OVER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Keyonte George (UTA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -189
