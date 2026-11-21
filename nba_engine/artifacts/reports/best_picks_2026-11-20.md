# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-21T03:00:27Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Amen Thompson (HOU) UNDER 0.5 3-pointers made | -311 (DraftKings via ESPN) | 0.5 | 71% | 71% | -0.06 |
| Kevin Huerter (DET) OVER 0.5 Steals | -247 (DraftKings via ESPN) | 1.1 | 67% | 67% | -0.06 |
| Ziaire Williams (LAL) OVER 0.5 3-pointers made | -242 (DraftKings via ESPN) | 1.4 | 67% | 67% | -0.06 |
| Onyeka Okongwu (ATL) OVER 0.5 Blocks | -243 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |

**Combined probability 21.1%; parlay pays 3.7x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Amen Thompson (HOU) UNDER 0.5 3-pointers made (71%); Kevin Huerter (DET) OVER 0.5 Steals (67%); Ziaire Williams (LAL) OVER 0.5 3-pointers made (67%). Combined probability 31.7%; parlay pays 2.6x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Quenton Jackson (IND) OVER 2.5 Assists | +116 (DraftKings via ESPN) | 3.4 | 63% | 43% | +0.36 |
| Darryn Peterson (UTA) UNDER 18.5 Points | -113 (DraftKings via ESPN) | 15.2 | 72% | 50% | +0.35 |

Combined probability 45.2%; parlay pays 4.1x; expected profit per 1 staked +0.84.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Quenton Jackson (IND) OVER 2.5 Assists | +116 (DraftKings via ESPN) | 3.4 | 63% | 43% | +0.36 |
| Darryn Peterson (UTA) UNDER 18.5 Points | -113 (DraftKings via ESPN) | 15.2 | 72% | 50% | +0.35 |
| Alperen Sengun (HOU) UNDER 19.5 Points | -112 (DraftKings via ESPN) | 16.1 | 71% | 50% | +0.35 |

Combined probability 32.2%; parlay pays 7.7x; expected profit per 1 staked +1.48.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Quenton Jackson (IND) OVER 2.5 Assists | +116 (DraftKings via ESPN) | 3.4 | 63% | 43% | +0.36 |
| Darryn Peterson (UTA) UNDER 18.5 Points | -113 (DraftKings via ESPN) | 15.2 | 72% | 50% | +0.35 |
| Alperen Sengun (HOU) UNDER 19.5 Points | -112 (DraftKings via ESPN) | 16.1 | 71% | 50% | +0.35 |
| Jeremiah Fears (NOP) UNDER 5.5 Assists | -123 (DraftKings via ESPN) | 4.2 | 72% | 52% | +0.31 |

Combined probability 23.3%; parlay pays 14.0x; expected profit per 1 staked +2.25.

Top single picks by model edge:

- Quenton Jackson (IND) OVER 2.5 Assists: model 63% vs book 43%, EV +0.36 at +116 (projection 3.4)
- Darryn Peterson (UTA) UNDER 18.5 Points: model 72% vs book 50%, EV +0.35 at -113 (projection 15.2)
- Alperen Sengun (HOU) UNDER 19.5 Points: model 71% vs book 50%, EV +0.35 at -112 (projection 16.1)
- Alperen Sengun (HOU) UNDER 8.5 Rebounds: model 67% vs book 47%, EV +0.33 at -102 (projection 6.9)
- Jeremiah Fears (NOP) UNDER 5.5 Assists: model 72% vs book 52%, EV +0.31 at -123 (projection 4.2)
- Cade Cunningham (DET) OVER 8.5 Assists: model 63% vs book 45%, EV +0.30 at +106 (projection 8.5)
- Quenton Jackson (IND) OVER 2.5 Rebounds: model 62% vs book 45%, EV +0.29 at +108 (projection 3.3)
- Walker Kessler (LAL) OVER 1.5 Assists: model 64% vs book 47%, EV +0.29 at +101 (projection 2.0)
- Jakob Poeltl (TOR) UNDER 7.5 Rebounds: model 66% vs book 48%, EV +0.28 at -105 (projection 6.2)
- Shai Gilgeous-Alexander (OKC) OVER 5.5 Assists: model 65% vs book 48%, EV +0.28 at -104 (projection 6.7)
- Daniss Jenkins (DET) OVER 5.5 Assists: model 59% vs book 43%, EV +0.28 at +117 (projection 6.2)
- Alperen Sengun (HOU) UNDER 6.5 Assists: model 72% vs book 54%, EV +0.25 at -134 (projection 5.1)

## CHA at ATL (game 401909305)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Onyeka Okongwu (ATL) OVER 0.5 Blocks | -243 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Nickeil Alexander-Walker (ATL) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |
| Dyson Daniels (ATL) UNDER 0.5 Blocks | -218 (DraftKings via ESPN) | 0.3 | 64% | 64% | -0.06 |

Combined probability 27.7%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Onyeka Okongwu (ATL) OVER 0.5 Blocks: 66%, EV -0.06 at -243
- Nickeil Alexander-Walker (ATL) UNDER 1.5 Steals: 65%, EV -0.06 at -226
- Dyson Daniels (ATL) UNDER 0.5 Blocks: 64%, EV -0.06 at -218
- Onyeka Okongwu (ATL) OVER 0.5 Steals: 64%, EV -0.06 at -215
- Jalen Johnson (ATL) UNDER 1.5 Steals: 62%, EV -0.06 at -192
- Naz Reid (CHA) OVER 0.5 Steals: 61%, EV -0.07 at -184
- Jalen Johnson (ATL) UNDER 0.5 Blocks: 60%, EV -0.07 at -181
- Coby White (CHA) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -179

## ORL at BKN (game 401909306)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Desmond Bane (ORL) OVER 0.5 Steals | -218 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Julius Randle (BKN) UNDER 1.5 3-pointers made | -157 (DraftKings via ESPN) | 1.4 | 57% | 57% | -0.06 |

Combined probability 23.9%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Franz Wagner (ORL) UNDER 1.5 Steals: 65%, EV -0.06 at -226
- Desmond Bane (ORL) OVER 0.5 Steals: 64%, EV -0.06 at -218
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -157
- Moritz Wagner (BKN) OVER 2.5 Rebounds: 57%, EV -0.06 at -156
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 57%, EV -0.06 at -153
- Egor Demin (BKN) OVER 1.5 3-pointers made: 57%, EV -0.06 at -153
- Michael Porter Jr. (BKN) OVER 2.5 3-pointers made: 56%, EV -0.06 at -150
- Franz Wagner (ORL) UNDER 1.5 3-pointers made: 56%, EV -0.06 at -149

## IND at CLE (game 401909307)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Obi Toppin (IND) UNDER 1.5 Assists | -229 (DraftKings via ESPN) | 1.5 | 65% | 65% | -0.06 |
| James Harden (CLE) OVER 0.5 Steals | -209 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |
| Jarrett Allen (CLE) OVER 0.5 Blocks | -207 (DraftKings via ESPN) | 0.8 | 63% | 63% | -0.06 |

Combined probability 26.2%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Obi Toppin (IND) UNDER 1.5 Assists: 65%, EV -0.06 at -229
- Obi Toppin (IND) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -226
- James Harden (CLE) OVER 0.5 Steals: 63%, EV -0.06 at -209
- Jarrett Allen (CLE) OVER 0.5 Blocks: 63%, EV -0.06 at -207
- Kelly Oubre Jr. (IND) UNDER 1.5 Assists: 63%, EV -0.06 at -203
- Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Aaron Nesmith (IND) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -192
- Tyrese Proctor (CLE) OVER 1.5 3-pointers made: 61%, EV -0.06 at -186

## TOR at DET (game 401909308)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kevin Huerter (DET) OVER 0.5 Steals | -247 (DraftKings via ESPN) | 1.1 | 67% | 67% | -0.06 |
| Daniss Jenkins (DET) OVER 0.5 Steals | -238 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Jamal Shead (TOR) UNDER 1.5 Steals | -228 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 28.7%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Kevin Huerter (DET) OVER 0.5 Steals: 67%, EV -0.06 at -247
- Daniss Jenkins (DET) OVER 0.5 Steals: 66%, EV -0.06 at -238
- Jamal Shead (TOR) UNDER 1.5 Steals: 65%, EV -0.06 at -228
- Jamal Shead (TOR) OVER 0.5 3-pointers made: 65%, EV -0.06 at -220
- Cade Cunningham (DET) UNDER 1.5 Steals: 64%, EV -0.06 at -219
- Jakob Poeltl (TOR) OVER 0.5 Steals: 63%, EV -0.06 at -206
- Jamison Battle (TOR) UNDER 1.5 Assists: 62%, EV -0.06 at -197
- Ausar Thompson (DET) OVER 0.5 Blocks: 62%, EV -0.06 at -196

## WAS at CHI (game 401909309)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| AJ Dybantsa (WAS) UNDER 1.5 Steals | -207 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |
| Matas Buzelis (CHI) OVER 0.5 Blocks | -203 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |
| Isaac Okoro (CHI) OVER 0.5 Steals | -201 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |

Combined probability 24.8%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- AJ Dybantsa (WAS) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Matas Buzelis (CHI) OVER 0.5 Blocks: 63%, EV -0.06 at -203
- Isaac Okoro (CHI) OVER 0.5 Steals: 63%, EV -0.06 at -201
- Matas Buzelis (CHI) UNDER 2.5 Assists: 62%, EV -0.06 at -193
- Alex Sarr (WAS) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Isaac Okoro (CHI) OVER 1.5 Assists: 61%, EV -0.06 at -182
- Anthony Davis (WAS) UNDER 2.5 Assists: 60%, EV -0.06 at -181
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -180

## NOP at OKC (game 401909310)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jeremiah Fears (NOP) OVER 0.5 Steals | -240 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Herbert Jones (NOP) OVER 0.5 Steals | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Zion Williamson (NOP) UNDER 1.5 Steals | -238 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |

Combined probability 28.9%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jeremiah Fears (NOP) OVER 0.5 Steals: 66%, EV -0.06 at -240
- Herbert Jones (NOP) OVER 0.5 Steals: 66%, EV -0.06 at -239
- Zion Williamson (NOP) UNDER 1.5 Steals: 66%, EV -0.06 at -238
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -204
- Jared McCain (OKC) OVER 0.5 Steals: 63%, EV -0.06 at -201
- Derik Queen (NOP) UNDER 2.5 Assists: 62%, EV -0.06 at -194
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 62%, EV -0.06 at -192
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -190

## PHX at UTA (game 401909311)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Collin Gillespie (PHX) UNDER 1.5 Steals | -222 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Darryn Peterson (UTA) UNDER 1.5 Steals | -221 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Devin Booker (PHX) OVER 1.5 3-pointers made | -182 (DraftKings via ESPN) | 2.0 | 60% | 60% | -0.06 |

Combined probability 25.2%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Collin Gillespie (PHX) UNDER 1.5 Steals: 65%, EV -0.06 at -222
- Darryn Peterson (UTA) UNDER 1.5 Steals: 65%, EV -0.06 at -221
- Devin Booker (PHX) OVER 1.5 3-pointers made: 60%, EV -0.06 at -182
- Ace Bailey (UTA) UNDER 2.5 Assists: 60%, EV -0.06 at -179
- Jalen Green (PHX) UNDER 3.5 Assists: 59%, EV -0.06 at -172
- Collin Gillespie (PHX) OVER 2.5 Rebounds: 59%, EV -0.06 at -167
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Brice Sensabaugh (UTA) UNDER 3.5 Rebounds: 58%, EV -0.06 at -166

## HOU at DEN (game 401909312)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Amen Thompson (HOU) UNDER 0.5 3-pointers made | -311 (DraftKings via ESPN) | 0.5 | 71% | 71% | -0.06 |
| Christian Braun (DEN) UNDER 1.5 Steals | -231 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Jamal Murray (DEN) OVER 0.5 Steals | -219 (DraftKings via ESPN) | 0.9 | 64% | 64% | -0.06 |

Combined probability 30.0%; parlay pays 2.8x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Amen Thompson (HOU) UNDER 0.5 3-pointers made: 71%, EV -0.06 at -311
- Christian Braun (DEN) UNDER 1.5 Steals: 65%, EV -0.06 at -231
- Jamal Murray (DEN) OVER 0.5 Steals: 64%, EV -0.06 at -219
- Alperen Sengun (HOU) OVER 0.5 Steals: 64%, EV -0.06 at -218
- Aaron Gordon (DEN) UNDER 0.5 Blocks: 64%, EV -0.06 at -217
- Amen Thompson (HOU) UNDER 1.5 Steals: 64%, EV -0.06 at -211
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Christian Braun (DEN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -187

## SAC at LAL (game 401909313)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ziaire Williams (LAL) OVER 0.5 3-pointers made | -242 (DraftKings via ESPN) | 1.4 | 67% | 67% | -0.06 |
| Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made | -197 (DraftKings via ESPN) | 1.6 | 62% | 62% | -0.06 |
| Matisse Thybulle (LAL) UNDER 2.5 Steals | -190 (DraftKings via ESPN) | 2.4 | 61% | 61% | -0.06 |

Combined probability 25.4%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Ziaire Williams (LAL) OVER 0.5 3-pointers made: 67%, EV -0.06 at -242
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -197
- Matisse Thybulle (LAL) UNDER 2.5 Steals: 61%, EV -0.06 at -190
- Zach LaVine (SAC) OVER 2.5 Rebounds: 59%, EV -0.06 at -173
- Collin Sexton (LAL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -163
- De'Andre Hunter (SAC) OVER 1.5 3-pointers made: 58%, EV -0.06 at -163
- Malik Monk (SAC) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -161
- Jake LaRavia (LAL) OVER 3.5 Rebounds: 58%, EV -0.06 at -161
