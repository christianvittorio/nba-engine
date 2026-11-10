# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-10T08:44:23Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick White (BOS) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Bam Adebayo (MIA) OVER 0.5 3-pointers made | -234 (DraftKings via ESPN) | 1.5 | 66% | 66% | -0.06 |
| Kenrich Williams (OKC) UNDER 1.5 3-pointers made | -230 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Jase Richardson (ORL) UNDER 1.5 3-pointers made | -209 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

**Combined probability 18.0%; parlay pays 4.3x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Derrick White (BOS) UNDER 1.5 Steals (66%); Bam Adebayo (MIA) OVER 0.5 3-pointers made (66%); Kenrich Williams (OKC) UNDER 1.5 3-pointers made (65%). Combined probability 28.4%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 5.5 Assists | +108 (DraftKings via ESPN) | 4.1 | 74% | 45% | +0.55 |
| Darryn Peterson (UTA) UNDER 4.5 Assists | +110 (DraftKings via ESPN) | 3.8 | 66% | 45% | +0.39 |

Combined probability 49.2%; parlay pays 4.4x; expected profit per 1 staked +1.15.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 5.5 Assists | +108 (DraftKings via ESPN) | 4.1 | 74% | 45% | +0.55 |
| Darryn Peterson (UTA) UNDER 4.5 Assists | +110 (DraftKings via ESPN) | 3.8 | 66% | 45% | +0.39 |
| Ajay Mitchell (OKC) UNDER 3.5 Rebounds | +118 (DraftKings via ESPN) | 3.2 | 58% | 43% | +0.26 |

Combined probability 28.5%; parlay pays 9.5x; expected profit per 1 staked +1.71.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 5.5 Assists | +108 (DraftKings via ESPN) | 4.1 | 74% | 45% | +0.55 |
| Darryn Peterson (UTA) UNDER 4.5 Assists | +110 (DraftKings via ESPN) | 3.8 | 66% | 45% | +0.39 |
| Ajay Mitchell (OKC) UNDER 3.5 Rebounds | +118 (DraftKings via ESPN) | 3.2 | 58% | 43% | +0.26 |
| Zach LaVine (SAC) UNDER 19.5 Points | -120 (DraftKings via ESPN) | 16.6 | 69% | 51% | +0.26 |

Combined probability 19.6%; parlay pays 17.5x; expected profit per 1 staked +2.42.

Top single picks by model edge:

- Tyrese Maxey (PHI) UNDER 5.5 Assists: model 74% vs book 45%, EV +0.55 at +108 (projection 4.1)
- Tyrese Maxey (PHI) UNDER 23.5 Points: model 74% vs book 49%, EV +0.45 at -106 (projection 19.0)
- Jayson Tatum (BOS) UNDER 26.5 Points: model 71% vs book 48%, EV +0.39 at -104 (projection 20.0)
- Darryn Peterson (UTA) UNDER 4.5 Assists: model 66% vs book 45%, EV +0.39 at +110 (projection 3.8)
- LeBron James (PHI) UNDER 6.5 Assists: model 71% vs book 48%, EV +0.38 at -106 (projection 4.7)
- VJ Edgecombe (PHI) UNDER 2.5 Assists: model 61% vs book 41%, EV +0.38 at +127 (projection 2.3)
- Andrew Wiggins (MIA) OVER 3.5 Rebounds: model 58% vs book 42%, EV +0.30 at +123 (projection 4.0)
- Giannis Antetokounmpo (MIA) UNDER 30.5 Points: model 66% vs book 48%, EV +0.29 at -105 (projection 27.0)
- Darryn Peterson (UTA) UNDER 18.5 Points: model 70% vs book 52%, EV +0.29 at -121 (projection 15.4)
- Jayson Tatum (BOS) UNDER 6.5 Assists: model 62% vs book 45%, EV +0.28 at +108 (projection 5.2)
- Ajay Mitchell (OKC) UNDER 3.5 Rebounds: model 58% vs book 43%, EV +0.26 at +118 (projection 3.2)
- Zach LaVine (SAC) UNDER 19.5 Points: model 69% vs book 51%, EV +0.26 at -120 (projection 16.6)

## MIL at NYK (game 401909960)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| OG Anunoby (NYK) UNDER 2.5 Assists | -181 (DraftKings via ESPN) | 2.4 | 60% | 60% | -0.06 |
| Landry Shamet (NYK) OVER 1.5 3-pointers made | -176 (DraftKings via ESPN) | 2.1 | 60% | 60% | -0.06 |
| Mikal Bridges (NYK) UNDER 1.5 3-pointers made | -163 (DraftKings via ESPN) | 1.4 | 58% | 58% | -0.06 |

Combined probability 21.0%; parlay pays 3.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- OG Anunoby (NYK) UNDER 2.5 Assists: 60%, EV -0.06 at -181
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -179
- Landry Shamet (NYK) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -163
- Mikal Bridges (NYK) OVER 2.5 Assists: 56%, EV -0.06 at -151
- Jalen Brunson (NYK) UNDER 2.5 3-pointers made: 56%, EV -0.06 at -146
- Jalen Brunson (NYK) UNDER 3.5 Rebounds: 55%, EV -0.06 at -143

## BOS at PHI (game 401909961)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick White (BOS) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Neemias Queta (BOS) UNDER 1.5 Blocks | -233 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Joel Embiid (PHI) OVER 0.5 3-pointers made | -224 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

Combined probability 28.0%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Derrick White (BOS) UNDER 1.5 Steals: 66%, EV -0.06 at -236
- Neemias Queta (BOS) UNDER 1.5 Blocks: 66%, EV -0.06 at -233
- Joel Embiid (PHI) OVER 0.5 3-pointers made: 65%, EV -0.06 at -224
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 65%, EV -0.06 at -221
- LeBron James (PHI) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Payton Pritchard (BOS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- VJ Edgecombe (PHI) UNDER 1.5 Steals: 60%, EV -0.07 at -177
- VJ Edgecombe (PHI) OVER 2.5 Assists: 59%, EV -0.06 at -169

## MIA at UTA (game 401909963)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bam Adebayo (MIA) OVER 0.5 3-pointers made | -234 (DraftKings via ESPN) | 1.5 | 66% | 66% | -0.06 |
| Bobby Portis (MIA) UNDER 1.5 3-pointers made | -203 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |
| Pelle Larsson (MIA) OVER 0.5 3-pointers made | -201 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |

Combined probability 25.9%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Bam Adebayo (MIA) OVER 0.5 3-pointers made: 66%, EV -0.06 at -234
- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Pelle Larsson (MIA) OVER 0.5 3-pointers made: 63%, EV -0.06 at -201
- Klay Thompson (MIA) OVER 1.5 Assists: 61%, EV -0.06 at -190
- Andrew Wiggins (MIA) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Darryn Peterson (UTA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Klay Thompson (MIA) UNDER 2.5 Rebounds: 60%, EV -0.06 at -175
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -175

## ORL at SAC (game 401909964)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jase Richardson (ORL) UNDER 1.5 3-pointers made | -209 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |
| Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made | -174 (DraftKings via ESPN) | 1.1 | 60% | 60% | -0.06 |
| Zach LaVine (SAC) OVER 2.5 Rebounds | -171 (DraftKings via ESPN) | 2.8 | 59% | 59% | -0.06 |

Combined probability 22.3%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jase Richardson (ORL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -209
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 60%, EV -0.06 at -174
- Zach LaVine (SAC) OVER 2.5 Rebounds: 59%, EV -0.06 at -171
- Franz Wagner (ORL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Anthony Black (ORL) OVER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Tristan da Silva (ORL) OVER 2.5 3-pointers made: 58%, EV -0.06 at -165
- Desmond Bane (ORL) OVER 2.5 Assists: 58%, EV -0.06 at -164
- Tristan da Silva (ORL) UNDER 4.5 Rebounds: 57%, EV -0.06 at -158

## OKC at POR (game 401909965)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kenrich Williams (OKC) UNDER 1.5 3-pointers made | -230 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Ajay Mitchell (OKC) UNDER 1.5 3-pointers made | -203 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |
| Jrue Holiday (POR) UNDER 2.5 3-pointers made | -192 (DraftKings via ESPN) | 2.1 | 62% | 62% | -0.06 |

Combined probability 25.4%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -230
- Ajay Mitchell (OKC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Jrue Holiday (POR) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -192
- Scoot Henderson (POR) UNDER 2.5 Assists: 61%, EV -0.06 at -186
- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181
- Jared McCain (OKC) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Jared McCain (OKC) UNDER 3.5 Rebounds: 59%, EV -0.06 at -167
- Damian Lillard (POR) UNDER 4.5 Assists: 58%, EV -0.06 at -163
