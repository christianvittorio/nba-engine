# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-11T00:30:34Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Green (PHX) OVER 0.5 Steals | -244 (DraftKings via ESPN) | 0.8 | 67% | 67% | -0.06 |
| Ajay Mitchell (OKC) OVER 0.5 3-pointers made | -241 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| LeBron James (PHI) OVER 0.5 Steals | -243 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Pelle Larsson (MIA) UNDER 1.5 3-pointers made | -238 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |

**Combined probability 19.4%; parlay pays 4.0x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Jalen Green (PHX) OVER 0.5 Steals (67%); Ajay Mitchell (OKC) OVER 0.5 3-pointers made (66%); LeBron James (PHI) OVER 0.5 Steals (66%). Combined probability 29.3%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 7.5 Assists | +112 (DraftKings via ESPN) | 5.9 | 72% | 44% | +0.53 |
| Isaiah Collier (UTA) UNDER 6.5 Assists | -103 (DraftKings via ESPN) | 4.7 | 75% | 47% | +0.47 |

Combined probability 53.9%; parlay pays 4.2x; expected profit per 1 staked +1.25.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 7.5 Assists | +112 (DraftKings via ESPN) | 5.9 | 72% | 44% | +0.53 |
| Isaiah Collier (UTA) UNDER 6.5 Assists | -103 (DraftKings via ESPN) | 4.7 | 75% | 47% | +0.47 |
| Tyrese Maxey (PHI) UNDER 23.5 Points | -124 (DraftKings via ESPN) | 19.0 | 74% | 52% | +0.34 |

Combined probability 40.1%; parlay pays 7.5x; expected profit per 1 staked +2.02.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 7.5 Assists | +112 (DraftKings via ESPN) | 5.9 | 72% | 44% | +0.53 |
| Isaiah Collier (UTA) UNDER 6.5 Assists | -103 (DraftKings via ESPN) | 4.7 | 75% | 47% | +0.47 |
| Tyrese Maxey (PHI) UNDER 23.5 Points | -124 (DraftKings via ESPN) | 19.0 | 74% | 52% | +0.34 |
| Jaime Jaquez Jr. (MIL) UNDER 14.5 Points | -104 (DraftKings via ESPN) | 12.5 | 68% | 48% | +0.33 |

Combined probability 27.1%; parlay pays 14.8x; expected profit per 1 staked +3.01.

Top single picks by model edge:

- Franz Wagner (ORL) UNDER 7.5 Assists: model 72% vs book 44%, EV +0.53 at +112 (projection 5.9)
- Isaiah Collier (UTA) UNDER 6.5 Assists: model 75% vs book 47%, EV +0.47 at -103 (projection 4.7)
- Darryn Peterson (UTA) UNDER 5.5 Assists: model 74% vs book 49%, EV +0.41 at -110 (projection 4.1)
- Giannis Antetokounmpo (MIA) OVER 0.5 3-pointers made: model 52% vs book 35%, EV +0.38 at +166 (projection 0.8)
- Tyrese Maxey (PHI) UNDER 23.5 Points: model 74% vs book 52%, EV +0.34 at -124 (projection 19.0)
- Isaiah Collier (UTA) UNDER 10.5 Points: model 70% vs book 49%, EV +0.34 at -109 (projection 8.6)
- Darryn Peterson (UTA) UNDER 20.5 Points: model 74% vs book 52%, EV +0.33 at -123 (projection 16.5)
- Jaime Jaquez Jr. (MIL) UNDER 14.5 Points: model 68% vs book 48%, EV +0.33 at -104 (projection 12.5)
- Jayson Tatum (BOS) UNDER 26.5 Points: model 70% vs book 50%, EV +0.32 at -114 (projection 20.1)
- Anthony Black (ORL) UNDER 4.5 Assists: model 62% vs book 44%, EV +0.31 at +113 (projection 3.6)
- Shai Gilgeous-Alexander (OKC) UNDER 33.5 Points: model 70% vs book 52%, EV +0.29 at -121 (projection 28.6)
- VJ Edgecombe (PHI) UNDER 2.5 Assists: model 61% vs book 44%, EV +0.29 at +112 (projection 2.3)

## MIL at NYK (game 401909960)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -201 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| AJ Green (MIL) UNDER 2.5 Rebounds | -185 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| Ryan Rollins (MIL) UNDER 2.5 3-pointers made | -176 (DraftKings via ESPN) | 1.4 | 60% | 60% | -0.06 |

Combined probability 22.8%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -201
- AJ Green (MIL) UNDER 2.5 Rebounds: 61%, EV -0.06 at -185
- AJ Green (MIL) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -176
- Ryan Rollins (MIL) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -176
- Karl-Anthony Towns (NYK) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Jaime Jaquez Jr. (MIL) UNDER 3.5 Assists: 58%, EV -0.06 at -162
- OG Anunoby (NYK) UNDER 1.5 Steals: 58%, EV -0.07 at -160

## BOS at PHI (game 401909961)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| LeBron James (PHI) OVER 0.5 Steals | -243 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Derrick White (BOS) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Neemias Queta (BOS) UNDER 1.5 Blocks | -240 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |

Combined probability 29.2%; parlay pays 2.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- LeBron James (PHI) OVER 0.5 Steals: 66%, EV -0.06 at -243
- Derrick White (BOS) UNDER 1.5 Steals: 66%, EV -0.06 at -241
- Neemias Queta (BOS) UNDER 1.5 Blocks: 66%, EV -0.06 at -240
- Jaylen Brown (PHI) OVER 0.5 Steals: 66%, EV -0.06 at -233
- LeBron James (PHI) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -205
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 63%, EV -0.06 at -203
- Joel Embiid (PHI) OVER 0.5 3-pointers made: 62%, EV -0.06 at -192
- Jayson Tatum (BOS) OVER 0.5 Steals: 62%, EV -0.06 at -193

## LAC at PHX (game 401909962)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Green (PHX) OVER 0.5 Steals | -244 (DraftKings via ESPN) | 0.8 | 67% | 67% | -0.06 |
| Collin Gillespie (PHX) OVER 0.5 Steals | -240 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made | -216 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 28.3%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jalen Green (PHX) OVER 0.5 Steals: 67%, EV -0.06 at -244
- Collin Gillespie (PHX) OVER 0.5 Steals: 66%, EV -0.06 at -240
- Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -216
- Brook Lopez (LAC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -208
- Darius Garland (LAC) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Keaton Wagler (LAC) OVER 0.5 3-pointers made: 63%, EV -0.06 at -202
- Dillon Brooks (PHX) UNDER 2.5 Assists: 62%, EV -0.06 at -192
- Brook Lopez (LAC) UNDER 1.5 Blocks: 61%, EV -0.06 at -188

## MIA at UTA (game 401909963)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Pelle Larsson (MIA) UNDER 1.5 3-pointers made | -238 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks | -240 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Darryn Peterson (UTA) UNDER 1.5 Steals | -228 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

Combined probability 28.5%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Pelle Larsson (MIA) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -238
- Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks: 66%, EV -0.06 at -240
- Darryn Peterson (UTA) UNDER 1.5 Steals: 65%, EV -0.06 at -228
- Giannis Antetokounmpo (MIA) UNDER 0.5 3-pointers made: 65%, EV -0.06 at -222
- Bam Adebayo (MIA) OVER 0.5 3-pointers made: 65%, EV -0.06 at -222
- Pelle Larsson (MIA) UNDER 1.5 Steals: 63%, EV -0.06 at -209
- Darryn Peterson (UTA) UNDER 0.5 Blocks: 63%, EV -0.06 at -202
- Giannis Antetokounmpo (MIA) UNDER 1.5 Steals: 62%, EV -0.06 at -199

## ORL at SAC (game 401909964)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darius Acuff Jr. (SAC) OVER 0.5 Steals | -232 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Precious Achiuwa (SAC) UNDER 1.5 Assists | -207 (DraftKings via ESPN) | 1.5 | 63% | 63% | -0.06 |
| Jase Richardson (ORL) UNDER 1.5 3-pointers made | -205 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 26.2%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Darius Acuff Jr. (SAC) OVER 0.5 Steals: 66%, EV -0.06 at -232
- Precious Achiuwa (SAC) UNDER 1.5 Assists: 63%, EV -0.06 at -207
- Jase Richardson (ORL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -205
- Precious Achiuwa (SAC) OVER 0.5 Blocks: 61%, EV -0.06 at -186
- Desmond Bane (ORL) OVER 2.5 3-pointers made: 60%, EV -0.06 at -176
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 59%, EV -0.06 at -172
- De'Andre Hunter (SAC) UNDER 1.5 Assists: 59%, EV -0.06 at -171
- Desmond Bane (ORL) UNDER 3.5 Assists: 58%, EV -0.06 at -165

## OKC at POR (game 401909965)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ajay Mitchell (OKC) OVER 0.5 3-pointers made | -241 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -200 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |
| Scoot Henderson (POR) UNDER 2.5 Assists | -170 (DraftKings via ESPN) | 2.6 | 59% | 59% | -0.06 |

Combined probability 24.5%; parlay pays 3.4x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Ajay Mitchell (OKC) OVER 0.5 3-pointers made: 66%, EV -0.06 at -241
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 63%, EV -0.06 at -200
- Scoot Henderson (POR) UNDER 2.5 Assists: 59%, EV -0.06 at -170
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 59%, EV -0.07 at -170
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -164
- Shai Gilgeous-Alexander (OKC) OVER 3.5 Rebounds: 58%, EV -0.06 at -163
- Ajay Mitchell (OKC) UNDER 1.5 Steals: 57%, EV -0.06 at -159
- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -158
