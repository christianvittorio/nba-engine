# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-10T20:43:35Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Giannis Antetokounmpo (MIA) UNDER 0.5 3-pointers made | -269 (DraftKings via ESPN) | 0.8 | 69% | 69% | -0.06 |
| Jayson Tatum (BOS) OVER 0.5 Steals | -247 (DraftKings via ESPN) | 0.7 | 67% | 67% | -0.06 |
| Darius Acuff Jr. (SAC) OVER 0.5 Steals | -242 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -238 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |

**Combined probability 20.1%; parlay pays 3.9x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Giannis Antetokounmpo (MIA) UNDER 0.5 3-pointers made (69%); Jayson Tatum (BOS) OVER 0.5 Steals (67%); Darius Acuff Jr. (SAC) OVER 0.5 Steals (66%). Combined probability 30.4%; parlay pays 2.7x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Isaiah Collier (UTA) UNDER 6.5 Assists | +110 (DraftKings via ESPN) | 4.7 | 75% | 45% | +0.57 |
| Tyrese Maxey (PHI) UNDER 23.5 Points | -104 (DraftKings via ESPN) | 19.0 | 74% | 48% | +0.46 |

Combined probability 55.5%; parlay pays 4.1x; expected profit per 1 staked +1.29.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Isaiah Collier (UTA) UNDER 6.5 Assists | +110 (DraftKings via ESPN) | 4.7 | 75% | 45% | +0.57 |
| Tyrese Maxey (PHI) UNDER 23.5 Points | -104 (DraftKings via ESPN) | 19.0 | 74% | 48% | +0.46 |
| Brayden Burries (MIL) UNDER 12.5 Points | -109 (DraftKings via ESPN) | 9.7 | 74% | 49% | +0.42 |

Combined probability 41.2%; parlay pays 7.9x; expected profit per 1 staked +2.26.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Isaiah Collier (UTA) UNDER 6.5 Assists | +110 (DraftKings via ESPN) | 4.7 | 75% | 45% | +0.57 |
| Tyrese Maxey (PHI) UNDER 23.5 Points | -104 (DraftKings via ESPN) | 19.0 | 74% | 48% | +0.46 |
| Brayden Burries (MIL) UNDER 12.5 Points | -109 (DraftKings via ESPN) | 9.7 | 74% | 49% | +0.42 |
| Rui Hachimura (LAC) UNDER 15.5 Points | -110 (DraftKings via ESPN) | 10.7 | 74% | 49% | +0.41 |

Combined probability 30.6%; parlay pays 15.1x; expected profit per 1 staked +3.61.

Top single picks by model edge:

- Isaiah Collier (UTA) UNDER 6.5 Assists: model 75% vs book 45%, EV +0.57 at +110 (projection 4.7)
- Giannis Antetokounmpo (MIA) OVER 0.5 3-pointers made: model 52% vs book 31%, EV +0.56 at +200 (projection 0.8)
- Tyrese Maxey (PHI) UNDER 23.5 Points: model 74% vs book 48%, EV +0.46 at -104 (projection 19.0)
- Isaiah Collier (UTA) UNDER 2.5 Rebounds: model 64% vs book 42%, EV +0.43 at +121 (projection 2.0)
- Brayden Burries (MIL) UNDER 12.5 Points: model 74% vs book 49%, EV +0.42 at -109 (projection 9.7)
- Darryn Peterson (UTA) UNDER 20.5 Points: model 74% vs book 49%, EV +0.42 at -107 (projection 16.5)
- Rui Hachimura (LAC) UNDER 15.5 Points: model 74% vs book 49%, EV +0.41 at -110 (projection 10.7)
- VJ Edgecombe (PHI) UNDER 2.5 Assists: model 61% vs book 41%, EV +0.38 at +127 (projection 2.3)
- Myles Turner (MIL) UNDER 9.5 Points: model 70% vs book 49%, EV +0.35 at -109 (projection 7.7)
- Jayson Tatum (BOS) UNDER 26.5 Points: model 71% vs book 50%, EV +0.34 at -112 (projection 20.0)
- Anthony Black (ORL) UNDER 4.5 Assists: model 62% vs book 43%, EV +0.34 at +117 (projection 3.6)
- Ajay Mitchell (OKC) UNDER 18.5 Points: model 71% vs book 50%, EV +0.34 at -114 (projection 15.3)

## MIL at NYK (game 401909960)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -179 (DraftKings via ESPN) | 1.0 | 60% | 60% | -0.06 |
| Mikal Bridges (NYK) UNDER 1.5 3-pointers made | -177 (DraftKings via ESPN) | 1.4 | 60% | 60% | -0.06 |
| OG Anunoby (NYK) UNDER 2.5 3-pointers made | -168 (DraftKings via ESPN) | 2.4 | 59% | 59% | -0.06 |

Combined probability 21.2%; parlay pays 3.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -177
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -168
- Karl-Anthony Towns (NYK) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -162
- OG Anunoby (NYK) UNDER 1.5 Steals: 58%, EV -0.06 at -161
- Jaime Jaquez Jr. (MIL) OVER 2.5 Assists: 58%, EV -0.06 at -159
- Brayden Burries (MIL) UNDER 3.5 Assists: 57%, EV -0.06 at -158
- Landry Shamet (NYK) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -155

## BOS at PHI (game 401909961)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jayson Tatum (BOS) OVER 0.5 Steals | -247 (DraftKings via ESPN) | 0.7 | 67% | 67% | -0.06 |
| Derrick White (BOS) OVER 0.5 Steals | -244 (DraftKings via ESPN) | 0.9 | 67% | 67% | -0.06 |
| Neemias Queta (BOS) UNDER 1.5 Blocks | -238 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |

Combined probability 29.3%; parlay pays 2.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jayson Tatum (BOS) OVER 0.5 Steals: 67%, EV -0.06 at -247
- Derrick White (BOS) OVER 0.5 Steals: 67%, EV -0.06 at -244
- Neemias Queta (BOS) UNDER 1.5 Blocks: 66%, EV -0.06 at -238
- LeBron James (PHI) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -222
- Joel Embiid (PHI) OVER 0.5 3-pointers made: 62%, EV -0.06 at -196
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 62%, EV -0.06 at -197
- Payton Pritchard (BOS) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181
- VJ Edgecombe (PHI) UNDER 1.5 Steals: 60%, EV -0.06 at -176

## LAC at PHX (game 401909962)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Keaton Wagler (LAC) OVER 0.5 3-pointers made | -221 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Jalen Green (PHX) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 0.8 | 64% | 64% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made | -208 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 26.2%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Keaton Wagler (LAC) OVER 0.5 3-pointers made: 65%, EV -0.06 at -221
- Jalen Green (PHX) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -208
- Darius Garland (LAC) UNDER 1.5 Steals: 63%, EV -0.06 at -208
- Brook Lopez (LAC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -199
- Brook Lopez (LAC) UNDER 1.5 Blocks: 62%, EV -0.06 at -198
- Rui Hachimura (LAC) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -194
- Collin Gillespie (PHX) UNDER 1.5 Steals: 62%, EV -0.06 at -193

## MIA at UTA (game 401909963)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Giannis Antetokounmpo (MIA) UNDER 0.5 3-pointers made | -269 (DraftKings via ESPN) | 0.8 | 69% | 69% | -0.06 |
| Darryn Peterson (UTA) UNDER 0.5 Blocks | -244 (DraftKings via ESPN) | 0.7 | 67% | 67% | -0.06 |
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -238 (DraftKings via ESPN) | 1.5 | 66% | 66% | -0.06 |

Combined probability 30.2%; parlay pays 2.7x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Giannis Antetokounmpo (MIA) UNDER 0.5 3-pointers made: 69%, EV -0.06 at -269
- Darryn Peterson (UTA) UNDER 0.5 Blocks: 67%, EV -0.06 at -244
- Darryn Peterson (UTA) UNDER 1.5 Steals: 66%, EV -0.06 at -241
- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -238
- Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks: 66%, EV -0.06 at -236
- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -211
- Pelle Larsson (MIA) UNDER 1.5 Steals: 63%, EV -0.06 at -209
- Andrew Wiggins (MIA) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -202

## ORL at SAC (game 401909964)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darius Acuff Jr. (SAC) OVER 0.5 Steals | -242 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Jase Richardson (ORL) UNDER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| Desmond Bane (ORL) OVER 2.5 3-pointers made | -175 (DraftKings via ESPN) | 2.3 | 60% | 60% | -0.06 |

Combined probability 24.6%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Darius Acuff Jr. (SAC) OVER 0.5 Steals: 66%, EV -0.06 at -242
- Jase Richardson (ORL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Desmond Bane (ORL) OVER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 59%, EV -0.06 at -172
- Zach LaVine (SAC) OVER 2.5 Rebounds: 59%, EV -0.06 at -171
- De'Andre Hunter (SAC) OVER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Desmond Bane (ORL) UNDER 1.5 Steals: 58%, EV -0.06 at -165
- Desmond Bane (ORL) UNDER 3.5 Assists: 58%, EV -0.06 at -160

## OKC at POR (game 401909965)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -238 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Ajay Mitchell (OKC) UNDER 1.5 3-pointers made | -236 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Jrue Holiday (POR) OVER 1.5 3-pointers made | -192 (DraftKings via ESPN) | 2.1 | 62% | 62% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Donovan Clingan (POR) OVER 0.5 3-pointers made: 66%, EV -0.06 at -238
- Ajay Mitchell (OKC) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -236
- Jrue Holiday (POR) OVER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Shai Gilgeous-Alexander (OKC) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Jared McCain (OKC) UNDER 3.5 Rebounds: 59%, EV -0.06 at -172
- Jared McCain (OKC) OVER 1.5 3-pointers made: 59%, EV -0.06 at -170
- Ajay Mitchell (OKC) UNDER 1.5 Steals: 58%, EV -0.06 at -165
- Scoot Henderson (POR) UNDER 2.5 Assists: 58%, EV -0.06 at -164
