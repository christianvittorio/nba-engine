# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-22T21:22:56Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brandin Podziemski (GSW) OVER 0.5 Steals | -244 (DraftKings via ESPN) | 0.8 | 67% | 67% | -0.06 |
| Josh Green (UTA) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Jalen Johnson (ATL) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Anthony Davis (WAS) UNDER 1.5 Steals | -233 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |

**Combined probability 19.2%; parlay pays 4.0x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Brandin Podziemski (GSW) OVER 0.5 Steals (67%); Josh Green (UTA) UNDER 1.5 3-pointers made (66%); Jalen Johnson (ATL) UNDER 1.5 Steals (66%). Combined probability 29.2%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Karl-Anthony Towns (NYK) OVER 3.5 Assists | +112 (DraftKings via ESPN) | 4.0 | 65% | 44% | +0.38 |
| Giannis Antetokounmpo (MIA) UNDER 5.5 Assists | +112 (DraftKings via ESPN) | 4.9 | 62% | 44% | +0.31 |

Combined probability 40.2%; parlay pays 4.5x; expected profit per 1 staked +0.81.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Karl-Anthony Towns (NYK) OVER 3.5 Assists | +112 (DraftKings via ESPN) | 4.0 | 65% | 44% | +0.38 |
| Giannis Antetokounmpo (MIA) UNDER 5.5 Assists | +112 (DraftKings via ESPN) | 4.9 | 62% | 44% | +0.31 |
| Anthony Davis (WAS) UNDER 23.5 Points | -107 (DraftKings via ESPN) | 20.4 | 67% | 49% | +0.30 |

Combined probability 27.1%; parlay pays 8.7x; expected profit per 1 staked +1.36.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Karl-Anthony Towns (NYK) OVER 3.5 Assists | +112 (DraftKings via ESPN) | 4.0 | 65% | 44% | +0.38 |
| Giannis Antetokounmpo (MIA) UNDER 5.5 Assists | +112 (DraftKings via ESPN) | 4.9 | 62% | 44% | +0.31 |
| Anthony Davis (WAS) UNDER 23.5 Points | -107 (DraftKings via ESPN) | 20.4 | 67% | 49% | +0.30 |
| Cade Cunningham (DET) OVER 8.5 Assists | -105 (DraftKings via ESPN) | 8.7 | 65% | 48% | +0.27 |

Combined probability 17.7%; parlay pays 17.0x; expected profit per 1 staked +2.00.

Top single picks by model edge:

- Karl-Anthony Towns (NYK) OVER 3.5 Assists: model 65% vs book 44%, EV +0.38 at +112 (projection 4.0)
- Josh Hart (NYK) UNDER 8.5 Rebounds: model 70% vs book 49%, EV +0.34 at -108 (projection 6.8)
- Giannis Antetokounmpo (MIA) UNDER 5.5 Assists: model 62% vs book 44%, EV +0.31 at +112 (projection 4.9)
- Anthony Davis (WAS) UNDER 23.5 Points: model 67% vs book 49%, EV +0.30 at -107 (projection 20.4)
- Davion Mitchell (MIA) UNDER 8.5 Assists: model 71% vs book 51%, EV +0.29 at -122 (projection 6.8)
- Bam Adebayo (MIA) UNDER 19.5 Points: model 66% vs book 49%, EV +0.28 at -108 (projection 16.9)
- Cade Cunningham (DET) OVER 8.5 Assists: model 65% vs book 48%, EV +0.27 at -105 (projection 8.7)
- Payton Pritchard (BOS) OVER 4.5 Assists: model 60% vs book 45%, EV +0.27 at +110 (projection 5.3)
- Ausar Thompson (DET) OVER 4.5 Assists: model 58% vs book 43%, EV +0.25 at +116 (projection 5.2)
- Karl-Anthony Towns (NYK) OVER 20.5 Points: model 65% vs book 49%, EV +0.24 at -109 (projection 21.2)
- Kelly Oubre Jr. (IND) UNDER 12.5 Points: model 65% vs book 49%, EV +0.24 at -110 (projection 11.0)
- Naji Marshall (DAL) UNDER 3.5 Rebounds: model 61% vs book 47%, EV +0.22 at +101 (projection 3.1)

## DET at ATL (game 401910029)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Johnson (ATL) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| John Collins (DET) OVER 0.5 3-pointers made | -237 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Onyeka Okongwu (ATL) UNDER 1.5 Blocks | -237 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |

Combined probability 28.9%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jalen Johnson (ATL) UNDER 1.5 Steals: 66%, EV -0.06 at -241
- John Collins (DET) OVER 0.5 3-pointers made: 66%, EV -0.06 at -237
- Onyeka Okongwu (ATL) UNDER 1.5 Blocks: 66%, EV -0.06 at -237
- Cade Cunningham (DET) UNDER 1.5 Steals: 62%, EV -0.06 at -198
- Onyeka Okongwu (ATL) UNDER 2.5 Assists: 62%, EV -0.06 at -194
- Aaron Wiggins (ATL) UNDER 2.5 Assists: 61%, EV -0.06 at -190
- Daniss Jenkins (DET) OVER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Cade Cunningham (DET) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181

## OKC at MIA (game 401910030)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks | -222 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals | -203 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -198 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |

Combined probability 25.3%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks: 65%, EV -0.06 at -222
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 63%, EV -0.06 at -203
- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Klay Thompson (MIA) UNDER 2.5 Rebounds: 60%, EV -0.06 at -175
- Shai Gilgeous-Alexander (OKC) OVER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Bam Adebayo (MIA) UNDER 1.5 Steals: 58%, EV -0.06 at -162
- Davion Mitchell (MIA) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -162

## ORL at WAS (game 401910031)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Anthony Davis (WAS) UNDER 1.5 Steals | -233 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Alex Sarr (WAS) UNDER 1.5 3-pointers made | -209 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 Steals | -199 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |

Combined probability 26.0%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Anthony Davis (WAS) UNDER 1.5 Steals: 66%, EV -0.06 at -233
- Alex Sarr (WAS) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -209
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 62%, EV -0.06 at -199
- Tristan da Silva (ORL) OVER 1.5 3-pointers made: 62%, EV -0.06 at -197
- Anthony Davis (WAS) UNDER 1.5 Blocks: 62%, EV -0.06 at -194
- Kyshawn George (WAS) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -191
- Alex Sarr (WAS) UNDER 1.5 Blocks: 61%, EV -0.06 at -185
- Anthony Davis (WAS) OVER 1.5 Assists: 61%, EV -0.06 at -184

## DEN at CHI (game 401910032)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Christian Braun (DEN) UNDER 1.5 Steals | -212 (DraftKings via ESPN) | 1.6 | 64% | 64% | -0.06 |
| Patrick Williams (CHI) UNDER 1.5 3-pointers made | -208 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |
| Isaac Okoro (CHI) UNDER 1.5 3-pointers made | -198 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |

Combined probability 25.1%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Christian Braun (DEN) UNDER 1.5 Steals: 64%, EV -0.06 at -212
- Patrick Williams (CHI) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -208
- Isaac Okoro (CHI) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Josh Giddey (CHI) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Nikola Jokic (DEN) OVER 0.5 Blocks: 61%, EV -0.06 at -190
- DeMar DeRozan (DEN) UNDER 0.5 3-pointers made: 61%, EV -0.06 at -184
- Buddy Hield (CHI) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -176
- Cameron Johnson (DEN) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -176

## DAL at UTA (game 401910033)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Green (UTA) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Darryn Peterson (UTA) UNDER 1.5 Steals | -230 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

Combined probability 28.5%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Josh Green (UTA) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -240
- Kyrie Irving (DAL) UNDER 1.5 Steals: 66%, EV -0.06 at -236
- Darryn Peterson (UTA) UNDER 1.5 Steals: 65%, EV -0.06 at -230
- Ace Bailey (UTA) OVER 1.5 Assists: 61%, EV -0.06 at -185
- Darryn Peterson (UTA) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -165
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 58%, EV -0.06 at -164
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 58%, EV -0.06 at -162
- Kyrie Irving (DAL) OVER 3.5 Rebounds: 58%, EV -0.06 at -161

## IND at NYK (game 401910034)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Hart (NYK) UNDER 1.5 3-pointers made | -175 (DraftKings via ESPN) | 1.6 | 60% | 60% | -0.06 |
| Pascal Siakam (IND) OVER 2.5 Assists | -166 (DraftKings via ESPN) | 3.5 | 58% | 58% | -0.06 |
| Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made | -153 (DraftKings via ESPN) | 1.3 | 57% | 57% | -0.06 |

Combined probability 19.7%; parlay pays 4.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Josh Hart (NYK) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Pascal Siakam (IND) OVER 2.5 Assists: 58%, EV -0.06 at -166
- Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -153
- Pascal Siakam (IND) UNDER 6.5 Rebounds: 57%, EV -0.06 at -153
- Karl-Anthony Towns (NYK) UNDER 3.5 Assists: 56%, EV -0.06 at -147
- Obi Toppin (IND) UNDER 4.5 Rebounds: 55%, EV -0.06 at -145
- Josh Hart (NYK) OVER 3.5 Assists: 55%, EV -0.06 at -144

## BOS at GSW (game 401910035)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brandin Podziemski (GSW) OVER 0.5 Steals | -244 (DraftKings via ESPN) | 0.8 | 67% | 67% | -0.06 |
| Will Richard (GSW) UNDER 1.5 3-pointers made | -197 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Yaxel Lendeborg (GSW) OVER 1.5 3-pointers made | -188 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |

Combined probability 25.3%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Brandin Podziemski (GSW) OVER 0.5 Steals: 67%, EV -0.06 at -244
- Will Richard (GSW) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -197
- Yaxel Lendeborg (GSW) OVER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Gui Santos (GSW) UNDER 2.5 Assists: 60%, EV -0.06 at -182
- Baylor Scheierman (BOS) OVER 1.5 Assists: 60%, EV -0.06 at -176
- Payton Pritchard (BOS) UNDER 3.5 Rebounds: 59%, EV -0.06 at -166
- Neemias Queta (BOS) UNDER 1.5 Blocks: 58%, EV -0.06 at -165
- Brandin Podziemski (GSW) UNDER 4.5 Assists: 58%, EV -0.06 at -164
