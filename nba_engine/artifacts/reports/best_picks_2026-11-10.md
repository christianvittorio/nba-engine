# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-11T01:44:48Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ajay Mitchell (OKC) OVER 0.5 3-pointers made | -241 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| LeBron James (PHI) OVER 0.5 Steals | -243 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Jalen Green (PHX) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks | -238 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |

**Combined probability 19.3%; parlay pays 4.0x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Ajay Mitchell (OKC) OVER 0.5 3-pointers made (66%); LeBron James (PHI) OVER 0.5 Steals (66%); Jalen Green (PHX) UNDER 1.5 Steals (66%). Combined probability 29.3%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 5.5 Assists | -110 (DraftKings via ESPN) | 4.1 | 74% | 49% | +0.41 |
| Jayson Tatum (BOS) UNDER 26.5 Points | -107 (DraftKings via ESPN) | 20.1 | 70% | 49% | +0.36 |

Combined probability 51.9%; parlay pays 3.7x; expected profit per 1 staked +0.92.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 5.5 Assists | -110 (DraftKings via ESPN) | 4.1 | 74% | 49% | +0.41 |
| Jayson Tatum (BOS) UNDER 26.5 Points | -107 (DraftKings via ESPN) | 20.1 | 70% | 49% | +0.36 |
| Miles Bridges (PHX) UNDER 16.5 Points | -115 (DraftKings via ESPN) | 13.9 | 70% | 50% | +0.30 |

Combined probability 36.3%; parlay pays 6.9x; expected profit per 1 staked +1.50.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 5.5 Assists | -110 (DraftKings via ESPN) | 4.1 | 74% | 49% | +0.41 |
| Jayson Tatum (BOS) UNDER 26.5 Points | -107 (DraftKings via ESPN) | 20.1 | 70% | 49% | +0.36 |
| Miles Bridges (PHX) UNDER 16.5 Points | -115 (DraftKings via ESPN) | 13.9 | 70% | 50% | +0.30 |
| Shai Gilgeous-Alexander (OKC) UNDER 32.5 Points | -106 (DraftKings via ESPN) | 28.6 | 67% | 49% | +0.29 |

Combined probability 24.1%; parlay pays 13.4x; expected profit per 1 staked +2.24.

Top single picks by model edge:

- Darryn Peterson (UTA) UNDER 5.5 Assists: model 74% vs book 49%, EV +0.41 at -110 (projection 4.1)
- Jayson Tatum (BOS) UNDER 26.5 Points: model 70% vs book 49%, EV +0.36 at -107 (projection 20.1)
- Josh Okogie (UTA) UNDER 7.5 Points: model 72% vs book 50%, EV +0.35 at -114 (projection 5.9)
- Tyrese Maxey (PHI) UNDER 22.5 Points: model 70% vs book 49%, EV +0.34 at -109 (projection 19.0)
- Sam Hauser (BOS) OVER 2.5 Rebounds: model 64% vs book 46%, EV +0.31 at +104 (projection 3.3)
- Miles Bridges (PHX) UNDER 16.5 Points: model 70% vs book 50%, EV +0.30 at -115 (projection 13.9)
- Isaiah Collier (UTA) UNDER 6.5 Assists: model 75% vs book 54%, EV +0.29 at -136 (projection 4.7)
- Shai Gilgeous-Alexander (OKC) UNDER 32.5 Points: model 67% vs book 49%, EV +0.29 at -106 (projection 28.6)
- Jaime Jaquez Jr. (MIL) UNDER 14.5 Points: model 68% vs book 49%, EV +0.29 at -110 (projection 12.5)
- VJ Edgecombe (PHI) UNDER 2.5 Assists: model 61% vs book 44%, EV +0.29 at +112 (projection 2.3)
- Oso Ighodaro (PHX) UNDER 6.5 Points: model 67% vs book 49%, EV +0.28 at -109 (projection 5.5)
- Darryn Peterson (UTA) UNDER 19.5 Points: model 69% vs book 51%, EV +0.28 at -116 (projection 16.5)

## MIL at NYK (game 401909960)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nate Ament (MIL) OVER 0.5 3-pointers made | -233 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -229 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| AJ Green (MIL) UNDER 2.5 Rebounds | -185 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |

Combined probability 26.2%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Nate Ament (MIL) OVER 0.5 3-pointers made: 66%, EV -0.06 at -233
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -229
- AJ Green (MIL) UNDER 2.5 Rebounds: 61%, EV -0.06 at -185
- AJ Green (MIL) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -176
- Ryan Rollins (MIL) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Karl-Anthony Towns (NYK) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Jaime Jaquez Jr. (MIL) UNDER 3.5 Assists: 58%, EV -0.06 at -162

## BOS at PHI (game 401909961)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| LeBron James (PHI) OVER 0.5 Steals | -243 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Derrick White (BOS) UNDER 1.5 Steals | -238 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Neemias Queta (BOS) OVER 0.5 Blocks | -236 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |

Combined probability 28.9%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- LeBron James (PHI) OVER 0.5 Steals: 66%, EV -0.06 at -243
- Derrick White (BOS) UNDER 1.5 Steals: 66%, EV -0.06 at -238
- Neemias Queta (BOS) OVER 0.5 Blocks: 66%, EV -0.06 at -236
- Jaylen Brown (PHI) OVER 0.5 Steals: 66%, EV -0.06 at -233
- LeBron James (PHI) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -205
- Jayson Tatum (BOS) OVER 0.5 Steals: 62%, EV -0.06 at -199
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 62%, EV -0.06 at -197
- Derrick White (BOS) OVER 1.5 3-pointers made: 62%, EV -0.06 at -193

## LAC at PHX (game 401909962)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Green (PHX) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Collin Gillespie (PHX) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Keaton Wagler (LAC) OVER 0.5 3-pointers made | -217 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

Combined probability 28.2%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jalen Green (PHX) UNDER 1.5 Steals: 66%, EV -0.06 at -243
- Collin Gillespie (PHX) UNDER 1.5 Steals: 66%, EV -0.06 at -239
- Keaton Wagler (LAC) OVER 0.5 3-pointers made: 64%, EV -0.06 at -217
- Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -207
- Darius Garland (LAC) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Brook Lopez (LAC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -201
- Dillon Brooks (PHX) UNDER 2.5 Assists: 62%, EV -0.06 at -195
- Rui Hachimura (LAC) OVER 1.5 3-pointers made: 62%, EV -0.06 at -193

## MIA at UTA (game 401909963)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks | -238 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Darryn Peterson (UTA) OVER 0.5 Steals | -238 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Josh Okogie (UTA) OVER 0.5 3-pointers made | -222 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 28.2%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks: 66%, EV -0.06 at -238
- Darryn Peterson (UTA) OVER 0.5 Steals: 66%, EV -0.06 at -238
- Josh Okogie (UTA) OVER 0.5 3-pointers made: 65%, EV -0.06 at -222
- Pelle Larsson (MIA) UNDER 1.5 Steals: 64%, EV -0.06 at -217
- Pelle Larsson (MIA) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -212
- Giannis Antetokounmpo (MIA) UNDER 1.5 Steals: 62%, EV -0.06 at -198
- Darryn Peterson (UTA) UNDER 0.5 Blocks: 62%, EV -0.06 at -195
- Ace Bailey (UTA) UNDER 2.5 Assists: 61%, EV -0.06 at -186

## ORL at SAC (game 401909964)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darius Acuff Jr. (SAC) OVER 0.5 Steals | -232 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Precious Achiuwa (SAC) UNDER 1.5 Assists | -215 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |
| Jase Richardson (ORL) UNDER 1.5 3-pointers made | -182 (DraftKings via ESPN) | 1.3 | 61% | 61% | -0.06 |

Combined probability 25.4%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Darius Acuff Jr. (SAC) OVER 0.5 Steals: 66%, EV -0.06 at -232
- Precious Achiuwa (SAC) UNDER 1.5 Assists: 64%, EV -0.06 at -215
- Precious Achiuwa (SAC) OVER 0.5 Blocks: 61%, EV -0.06 at -186
- Jase Richardson (ORL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -182
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 60%, EV -0.06 at -180
- Jase Richardson (ORL) OVER 2.5 Assists: 60%, EV -0.06 at -176
- Desmond Bane (ORL) UNDER 1.5 Steals: 60%, EV -0.06 at -176
- De'Andre Hunter (SAC) UNDER 1.5 Assists: 59%, EV -0.06 at -171

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
- Jrue Holiday (POR) OVER 3.5 Rebounds: 58%, EV -0.06 at -160
- Ajay Mitchell (OKC) UNDER 1.5 Steals: 57%, EV -0.06 at -159
