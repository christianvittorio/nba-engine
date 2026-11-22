# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-22T16:57:14Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Onyeka Okongwu (ATL) UNDER 1.5 Blocks | -244 (DraftKings via ESPN) | 1.1 | 67% | 67% | -0.06 |
| Anthony Davis (WAS) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Brandin Podziemski (GSW) OVER 0.5 Steals | -243 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -225 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

**Combined probability 19.0%; parlay pays 4.1x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Onyeka Okongwu (ATL) UNDER 1.5 Blocks (67%); Anthony Davis (WAS) UNDER 1.5 Steals (66%); Brandin Podziemski (GSW) OVER 0.5 Steals (66%). Combined probability 29.3%; parlay pays 2.8x; expected profit per 1 staked -0.18.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Suggs (ORL) OVER 4.5 Assists | +125 (DraftKings via ESPN) | 4.5 | 61% | 42% | +0.38 |
| Daniss Jenkins (DET) OVER 5.5 Assists | +123 (DraftKings via ESPN) | 6.4 | 60% | 42% | +0.35 |

Combined probability 37.1%; parlay pays 5.0x; expected profit per 1 staked +0.86.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Suggs (ORL) OVER 4.5 Assists | +125 (DraftKings via ESPN) | 4.5 | 61% | 42% | +0.38 |
| Daniss Jenkins (DET) OVER 5.5 Assists | +123 (DraftKings via ESPN) | 6.4 | 60% | 42% | +0.35 |
| Baylor Scheierman (BOS) UNDER 7.5 Points | -126 (DraftKings via ESPN) | 5.4 | 75% | 53% | +0.34 |

Combined probability 27.7%; parlay pays 9.0x; expected profit per 1 staked +1.50.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Suggs (ORL) OVER 4.5 Assists | +125 (DraftKings via ESPN) | 4.5 | 61% | 42% | +0.38 |
| Daniss Jenkins (DET) OVER 5.5 Assists | +123 (DraftKings via ESPN) | 6.4 | 60% | 42% | +0.35 |
| Baylor Scheierman (BOS) UNDER 7.5 Points | -126 (DraftKings via ESPN) | 5.4 | 75% | 53% | +0.34 |
| Giannis Antetokounmpo (MIA) UNDER 5.5 Assists | +116 (DraftKings via ESPN) | 4.9 | 62% | 43% | +0.33 |

Combined probability 17.1%; parlay pays 19.4x; expected profit per 1 staked +2.33.

Top single picks by model edge:

- Jalen Suggs (ORL) OVER 4.5 Assists: model 61% vs book 42%, EV +0.38 at +125 (projection 4.5)
- Daniss Jenkins (DET) OVER 5.5 Assists: model 60% vs book 42%, EV +0.35 at +123 (projection 6.4)
- Kevin Huerter (DET) OVER 3.5 Assists: model 58% vs book 40%, EV +0.34 at +133 (projection 4.1)
- Baylor Scheierman (BOS) UNDER 7.5 Points: model 75% vs book 53%, EV +0.34 at -126 (projection 5.4)
- Giannis Antetokounmpo (MIA) UNDER 5.5 Assists: model 62% vs book 43%, EV +0.33 at +116 (projection 4.9)
- Anthony Davis (WAS) UNDER 23.5 Points: model 67% vs book 49%, EV +0.31 at -106 (projection 20.4)
- Jayson Tatum (BOS) UNDER 28.5 Points: model 72% vs book 52%, EV +0.31 at -124 (projection 20.8)
- Davion Mitchell (MIA) UNDER 8.5 Assists: model 71% vs book 51%, EV +0.29 at -122 (projection 6.8)
- Shai Gilgeous-Alexander (OKC) OVER 5.5 Assists: model 63% vs book 46%, EV +0.28 at +103 (projection 6.5)
- Baylor Scheierman (BOS) UNDER 1.5 3-pointers made: model 71% vs book 54%, EV +0.24 at -136 (projection 1.0)
- Kelly Oubre Jr. (IND) UNDER 12.5 Points: model 65% vs book 49%, EV +0.24 at -110 (projection 11.0)
- Mikal Bridges (NYK) UNDER 12.5 Points: model 69% vs book 53%, EV +0.23 at -129 (projection 10.2)

## DET at ATL (game 401910029)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Onyeka Okongwu (ATL) UNDER 1.5 Blocks | -244 (DraftKings via ESPN) | 1.1 | 67% | 67% | -0.06 |
| John Collins (DET) UNDER 1.5 3-pointers made | -235 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Jalen Johnson (ATL) UNDER 1.5 Steals | -221 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

Combined probability 28.3%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Onyeka Okongwu (ATL) UNDER 1.5 Blocks: 67%, EV -0.06 at -244
- John Collins (DET) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -235
- Jalen Johnson (ATL) UNDER 1.5 Steals: 65%, EV -0.06 at -221
- Cade Cunningham (DET) UNDER 1.5 Steals: 62%, EV -0.06 at -199
- Daniss Jenkins (DET) OVER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Paul Reed (DET) UNDER 2.5 Assists: 61%, EV -0.06 at -190
- Cade Cunningham (DET) OVER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Jalen Johnson (ATL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -182

## OKC at MIA (game 401910030)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks | -215 (DraftKings via ESPN) | 0.9 | 64% | 64% | -0.06 |
| Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals | -202 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -198 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |

Combined probability 24.9%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks: 64%, EV -0.06 at -215
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 63%, EV -0.06 at -202
- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Jared McCain (OKC) UNDER 2.5 Assists: 61%, EV -0.06 at -187
- Klay Thompson (MIA) UNDER 2.5 Rebounds: 60%, EV -0.06 at -181
- Aday Mara (OKC) UNDER 2.5 Assists: 60%, EV -0.06 at -180
- Davion Mitchell (MIA) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -169

## ORL at WAS (game 401910031)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Anthony Davis (WAS) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Alex Sarr (WAS) UNDER 1.5 3-pointers made | -226 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 Steals | -206 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |

Combined probability 27.3%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Anthony Davis (WAS) UNDER 1.5 Steals: 66%, EV -0.06 at -243
- Alex Sarr (WAS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -226
- Alex Sarr (WAS) UNDER 1.5 Blocks: 64%, EV -0.06 at -213
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 63%, EV -0.06 at -206
- Anthony Davis (WAS) UNDER 1.5 Blocks: 63%, EV -0.06 at -201
- Trae Young (WAS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -188
- Tristan da Silva (ORL) OVER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Kyshawn George (WAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184

## DEN at CHI (game 401910032)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nikola Jokic (DEN) OVER 0.5 Blocks | -210 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |
| DeMar DeRozan (DEN) UNDER 0.5 3-pointers made | -190 (DraftKings via ESPN) | 0.5 | 61% | 61% | -0.06 |
| Christian Braun (DEN) UNDER 2.5 Assists | -184 (DraftKings via ESPN) | 2.7 | 61% | 61% | -0.06 |

Combined probability 23.7%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Nikola Jokic (DEN) OVER 0.5 Blocks: 63%, EV -0.06 at -210
- DeMar DeRozan (DEN) UNDER 0.5 3-pointers made: 61%, EV -0.06 at -190
- Christian Braun (DEN) UNDER 2.5 Assists: 61%, EV -0.06 at -184
- Cameron Johnson (DEN) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -180
- Isaac Okoro (CHI) UNDER 3.5 Rebounds: 59%, EV -0.06 at -172
- Aaron Gordon (DEN) OVER 1.5 Assists: 59%, EV -0.06 at -171
- Matas Buzelis (CHI) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -167
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -164

## DAL at UTA (game 401910033)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 1.5 Steals | -225 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Darryn Peterson (UTA) UNDER 1.5 Steals | -217 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Ace Bailey (UTA) OVER 1.5 Assists | -195 (DraftKings via ESPN) | 2.2 | 62% | 62% | -0.06 |

Combined probability 25.8%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Kyrie Irving (DAL) UNDER 1.5 Steals: 65%, EV -0.06 at -225
- Darryn Peterson (UTA) UNDER 1.5 Steals: 64%, EV -0.06 at -217
- Ace Bailey (UTA) OVER 1.5 Assists: 62%, EV -0.06 at -195
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -174
- Darryn Peterson (UTA) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -164
- Kyrie Irving (DAL) OVER 3.5 Rebounds: 58%, EV -0.06 at -162
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 58%, EV -0.06 at -161
- Caleb Martin (DAL) UNDER 2.5 Assists: 58%, EV -0.06 at -159

## IND at NYK (game 401910034)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Hart (NYK) UNDER 1.5 3-pointers made | -188 (DraftKings via ESPN) | 1.3 | 61% | 61% | -0.06 |
| Pascal Siakam (IND) OVER 2.5 Assists | -166 (DraftKings via ESPN) | 3.5 | 59% | 59% | -0.06 |
| Jalen Brunson (NYK) UNDER 3.5 Rebounds | -165 (DraftKings via ESPN) | 3.3 | 58% | 58% | -0.06 |

Combined probability 20.9%; parlay pays 3.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Josh Hart (NYK) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Pascal Siakam (IND) OVER 2.5 Assists: 59%, EV -0.06 at -166
- Jalen Brunson (NYK) UNDER 3.5 Rebounds: 58%, EV -0.06 at -165
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -160
- Mikal Bridges (NYK) UNDER 3.5 Rebounds: 56%, EV -0.06 at -147
- Pascal Siakam (IND) OVER 5.5 Rebounds: 56%, EV -0.06 at -147
- Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made: 56%, EV -0.06 at -146
- Josh Hart (NYK) UNDER 1.5 Steals: 55%, EV -0.07 at -146

## BOS at GSW (game 401910035)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brandin Podziemski (GSW) OVER 0.5 Steals | -243 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Will Richard (GSW) UNDER 1.5 3-pointers made | -225 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Gui Santos (GSW) UNDER 2.5 Assists | -186 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |

Combined probability 26.3%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Brandin Podziemski (GSW) OVER 0.5 Steals: 66%, EV -0.06 at -243
- Will Richard (GSW) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -225
- Gui Santos (GSW) UNDER 2.5 Assists: 61%, EV -0.06 at -186
- Baylor Scheierman (BOS) UNDER 2.5 Assists: 60%, EV -0.06 at -179
- Brandin Podziemski (GSW) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -173
- Payton Pritchard (BOS) OVER 2.5 Rebounds: 59%, EV -0.06 at -170
- Jayson Tatum (BOS) OVER 2.5 3-pointers made: 59%, EV -0.06 at -166
- Yaxel Lendeborg (GSW) OVER 1.5 3-pointers made: 58%, EV -0.06 at -165
