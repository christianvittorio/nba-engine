# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-10T16:50:21Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.5 | 66% | 66% | -0.06 |
| Ajay Mitchell (OKC) UNDER 1.5 3-pointers made | -234 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| LeBron James (PHI) UNDER 1.5 3-pointers made | -231 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made | -230 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

**Combined probability 18.7%; parlay pays 4.2x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Bam Adebayo (MIA) UNDER 1.5 3-pointers made (66%); Ajay Mitchell (OKC) UNDER 1.5 3-pointers made (66%); LeBron James (PHI) UNDER 1.5 3-pointers made (66%). Combined probability 28.6%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 23.5 Points | -107 (DraftKings via ESPN) | 19.0 | 74% | 49% | +0.44 |
| Rui Hachimura (LAC) UNDER 15.5 Points | -106 (DraftKings via ESPN) | 10.7 | 73% | 49% | +0.43 |

Combined probability 54.6%; parlay pays 3.8x; expected profit per 1 staked +1.05.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 23.5 Points | -107 (DraftKings via ESPN) | 19.0 | 74% | 49% | +0.44 |
| Rui Hachimura (LAC) UNDER 15.5 Points | -106 (DraftKings via ESPN) | 10.7 | 73% | 49% | +0.43 |
| Tyler Herro (MIL) UNDER 2.5 3-pointers made | +106 (DraftKings via ESPN) | 2.0 | 67% | 45% | +0.39 |

Combined probability 36.8%; parlay pays 7.7x; expected profit per 1 staked +1.85.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 23.5 Points | -107 (DraftKings via ESPN) | 19.0 | 74% | 49% | +0.44 |
| Rui Hachimura (LAC) UNDER 15.5 Points | -106 (DraftKings via ESPN) | 10.7 | 73% | 49% | +0.43 |
| Tyler Herro (MIL) UNDER 2.5 3-pointers made | +106 (DraftKings via ESPN) | 2.0 | 67% | 45% | +0.39 |
| Darryn Peterson (UTA) UNDER 18.5 Points | -109 (DraftKings via ESPN) | 15.4 | 70% | 49% | +0.35 |

Combined probability 25.9%; parlay pays 14.9x; expected profit per 1 staked +2.85.

Top single picks by model edge:

- Tyrese Maxey (PHI) UNDER 23.5 Points: model 74% vs book 49%, EV +0.44 at -107 (projection 19.0)
- Rui Hachimura (LAC) UNDER 15.5 Points: model 73% vs book 49%, EV +0.43 at -106 (projection 10.7)
- Tyrese Maxey (PHI) UNDER 5.5 Assists: model 74% vs book 49%, EV +0.42 at -109 (projection 4.1)
- Tyler Herro (MIL) UNDER 2.5 3-pointers made: model 67% vs book 45%, EV +0.39 at +106 (projection 2.0)
- LeBron James (PHI) UNDER 6.5 Assists: model 71% vs book 49%, EV +0.37 at -108 (projection 4.7)
- Brayden Burries (MIL) UNDER 12.5 Points: model 74% vs book 51%, EV +0.37 at -119 (projection 9.7)
- Darryn Peterson (UTA) UNDER 18.5 Points: model 70% vs book 49%, EV +0.35 at -109 (projection 15.4)
- Jayson Tatum (BOS) UNDER 26.5 Points: model 71% vs book 51%, EV +0.32 at -116 (projection 20.0)
- Isaiah Collier (UTA) UNDER 9.5 Points: model 66% vs book 47%, EV +0.32 at -101 (projection 8.1)
- Domantas Sabonis (SAC) UNDER 5.5 Assists: model 63% vs book 45%, EV +0.31 at +109 (projection 4.4)
- VJ Edgecombe (PHI) UNDER 2.5 Assists: model 61% vs book 44%, EV +0.31 at +115 (projection 2.3)
- Myles Turner (MIL) UNDER 1.5 3-pointers made: model 63% vs book 45%, EV +0.30 at +106 (projection 1.3)

## MIL at NYK (game 401909960)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) UNDER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| OG Anunoby (NYK) UNDER 2.5 3-pointers made | -188 (DraftKings via ESPN) | 2.4 | 61% | 61% | -0.06 |
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -173 (DraftKings via ESPN) | 1.0 | 59% | 59% | -0.06 |

Combined probability 22.6%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -196
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -188
- OG Anunoby (NYK) UNDER 2.5 Assists: 60%, EV -0.06 at -176
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -173
- OG Anunoby (NYK) UNDER 1.5 Steals: 59%, EV -0.06 at -168
- Karl-Anthony Towns (NYK) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Jaime Jaquez Jr. (MIL) OVER 2.5 Assists: 58%, EV -0.06 at -164
- Mikal Bridges (NYK) UNDER 3.5 Rebounds: 58%, EV -0.06 at -161

## BOS at PHI (game 401909961)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| LeBron James (PHI) UNDER 1.5 3-pointers made | -231 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Neemias Queta (BOS) UNDER 1.5 Blocks | -215 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Tyrese Maxey (PHI) UNDER 1.5 Steals | -214 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 26.7%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- LeBron James (PHI) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -231
- Neemias Queta (BOS) UNDER 1.5 Blocks: 64%, EV -0.06 at -215
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 64%, EV -0.06 at -214
- Derrick White (BOS) UNDER 1.5 Steals: 63%, EV -0.06 at -208
- Payton Pritchard (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -185
- VJ Edgecombe (PHI) UNDER 1.5 Steals: 60%, EV -0.06 at -176
- Payton Pritchard (BOS) OVER 2.5 Rebounds: 58%, EV -0.06 at -165
- Paul George (BOS) UNDER 5.5 Rebounds: 57%, EV -0.06 at -159

## LAC at PHX (game 401909962)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made | -230 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Brook Lopez (LAC) UNDER 1.5 3-pointers made | -222 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |
| Jalen Green (PHX) UNDER 1.5 Steals | -223 (DraftKings via ESPN) | 0.8 | 65% | 65% | -0.06 |

Combined probability 27.4%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -230
- Brook Lopez (LAC) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -222
- Jalen Green (PHX) UNDER 1.5 Steals: 65%, EV -0.06 at -223
- Darius Garland (LAC) UNDER 1.5 Steals: 64%, EV -0.06 at -214
- Dillon Brooks (PHX) OVER 1.5 Assists: 62%, EV -0.06 at -196
- Brook Lopez (LAC) UNDER 1.5 Blocks: 61%, EV -0.06 at -191
- Collin Gillespie (PHX) OVER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Keaton Wagler (LAC) OVER 0.5 3-pointers made: 61%, EV -0.06 at -186

## MIA at UTA (game 401909963)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.5 | 66% | 66% | -0.06 |
| Bobby Portis (MIA) UNDER 1.5 3-pointers made | -234 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Josh Green (UTA) UNDER 1.5 3-pointers made | -213 (DraftKings via ESPN) | 0.9 | 64% | 64% | -0.06 |

Combined probability 27.9%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -240
- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -234
- Josh Green (UTA) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -213
- Andrew Wiggins (MIA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Klay Thompson (MIA) UNDER 2.5 Rebounds: 61%, EV -0.06 at -188
- Pelle Larsson (MIA) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Josh Green (UTA) UNDER 2.5 Rebounds: 59%, EV -0.06 at -174
- Davion Mitchell (MIA) OVER 1.5 3-pointers made: 59%, EV -0.06 at -170

## ORL at SAC (game 401909964)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made | -202 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |
| Jase Richardson (ORL) UNDER 1.5 3-pointers made | -174 (DraftKings via ESPN) | 1.1 | 59% | 59% | -0.06 |
| Zach LaVine (SAC) UNDER 3.5 Rebounds | -173 (DraftKings via ESPN) | 2.8 | 59% | 59% | -0.06 |

Combined probability 22.2%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 63%, EV -0.06 at -202
- Jase Richardson (ORL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -174
- Zach LaVine (SAC) UNDER 3.5 Rebounds: 59%, EV -0.06 at -173
- Desmond Bane (ORL) UNDER 3.5 Assists: 59%, EV -0.06 at -172
- Anthony Black (ORL) OVER 1.5 3-pointers made: 59%, EV -0.06 at -168
- De'Andre Hunter (SAC) OVER 1.5 3-pointers made: 58%, EV -0.06 at -161
- Desmond Bane (ORL) UNDER 4.5 Rebounds: 57%, EV -0.06 at -159
- Franz Wagner (ORL) UNDER 1.5 Steals: 57%, EV -0.06 at -158

## OKC at POR (game 401909965)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ajay Mitchell (OKC) UNDER 1.5 3-pointers made | -234 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Kenrich Williams (OKC) OVER 0.5 3-pointers made | -232 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -224 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

Combined probability 28.1%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Ajay Mitchell (OKC) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -234
- Kenrich Williams (OKC) OVER 0.5 3-pointers made: 66%, EV -0.06 at -232
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 65%, EV -0.06 at -224
- Jrue Holiday (POR) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -196
- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -187
- Scoot Henderson (POR) UNDER 2.5 Assists: 60%, EV -0.06 at -181
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 58%, EV -0.06 at -166
- Ajay Mitchell (OKC) UNDER 1.5 Steals: 58%, EV -0.06 at -162
