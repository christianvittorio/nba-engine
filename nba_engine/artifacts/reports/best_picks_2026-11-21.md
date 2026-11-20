# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-20T21:41:48Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Amen Thompson (HOU) UNDER 0.5 3-pointers made | -335 (DraftKings via ESPN) | 0.5 | 73% | 73% | -0.06 |
| Jeremiah Fears (NOP) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Ziaire Williams (LAL) OVER 0.5 3-pointers made | -239 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Kevin Huerter (DET) OVER 0.5 Steals | -240 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |

**Combined probability 21.2%; parlay pays 3.7x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Amen Thompson (HOU) UNDER 0.5 3-pointers made (73%); Jeremiah Fears (NOP) UNDER 1.5 Steals (66%); Ziaire Williams (LAL) OVER 0.5 3-pointers made (66%). Combined probability 32.0%; parlay pays 2.6x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) UNDER 19.5 Points | -106 (DraftKings via ESPN) | 16.1 | 71% | 49% | +0.38 |
| Jakob Poeltl (TOR) UNDER 7.5 Rebounds | +103 (DraftKings via ESPN) | 6.2 | 66% | 46% | +0.34 |

Combined probability 46.8%; parlay pays 3.9x; expected profit per 1 staked +0.85.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) UNDER 19.5 Points | -106 (DraftKings via ESPN) | 16.1 | 71% | 49% | +0.38 |
| Jakob Poeltl (TOR) UNDER 7.5 Rebounds | +103 (DraftKings via ESPN) | 6.2 | 66% | 46% | +0.34 |
| Darryn Peterson (UTA) UNDER 18.5 Points | -122 (DraftKings via ESPN) | 15.2 | 72% | 52% | +0.30 |

Combined probability 33.6%; parlay pays 7.2x; expected profit per 1 staked +1.41.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) UNDER 19.5 Points | -106 (DraftKings via ESPN) | 16.1 | 71% | 49% | +0.38 |
| Jakob Poeltl (TOR) UNDER 7.5 Rebounds | +103 (DraftKings via ESPN) | 6.2 | 66% | 46% | +0.34 |
| Darryn Peterson (UTA) UNDER 18.5 Points | -122 (DraftKings via ESPN) | 15.2 | 72% | 52% | +0.30 |
| Jeremiah Fears (NOP) UNDER 5.5 Assists | -104 (DraftKings via ESPN) | 4.5 | 66% | 48% | +0.29 |

Combined probability 22.1%; parlay pays 14.1x; expected profit per 1 staked +2.12.

Top single picks by model edge:

- Alperen Sengun (HOU) UNDER 19.5 Points: model 71% vs book 49%, EV +0.38 at -106 (projection 16.1)
- Jakob Poeltl (TOR) UNDER 7.5 Rebounds: model 66% vs book 46%, EV +0.34 at +103 (projection 6.2)
- Jamison Battle (TOR) UNDER 3.5 Rebounds: model 73% vs book 52%, EV +0.31 at -127 (projection 2.4)
- Darryn Peterson (UTA) UNDER 18.5 Points: model 72% vs book 52%, EV +0.30 at -122 (projection 15.2)
- Jeremiah Fears (NOP) UNDER 5.5 Assists: model 66% vs book 48%, EV +0.29 at -104 (projection 4.5)
- Walker Kessler (LAL) OVER 1.5 Assists: model 64% vs book 47%, EV +0.29 at +101 (projection 2.0)
- Alperen Sengun (HOU) UNDER 6.5 Assists: model 72% vs book 52%, EV +0.29 at -125 (projection 5.1)
- Shai Gilgeous-Alexander (OKC) OVER 5.5 Assists: model 62% vs book 46%, EV +0.26 at +105 (projection 6.3)
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: model 67% vs book 50%, EV +0.26 at -115 (projection 2.8)
- De'Andre Hunter (SAC) OVER 13.5 Points: model 62% vs book 47%, EV +0.24 at -101 (projection 14.0)
- Jamal Shead (TOR) OVER 5.5 Assists: model 56% vs book 43%, EV +0.24 at +119 (projection 6.1)
- Julius Randle (BKN) UNDER 4.5 Assists: model 67% vs book 51%, EV +0.24 at -117 (projection 3.7)

## CHA at ATL (game 401909305)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Onyeka Okongwu (ATL) UNDER 1.5 Blocks | -238 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Jalen Johnson (ATL) UNDER 1.5 Steals | -200 (DraftKings via ESPN) | 0.9 | 62% | 62% | -0.06 |
| Coby White (CHA) UNDER 2.5 3-pointers made | -180 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |

Combined probability 24.8%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Onyeka Okongwu (ATL) UNDER 1.5 Blocks: 66%, EV -0.06 at -238
- Jalen Johnson (ATL) UNDER 1.5 Steals: 62%, EV -0.06 at -200
- Onyeka Okongwu (ATL) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -195
- Coby White (CHA) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -180
- Luguentz Dort (ATL) OVER 2.5 Rebounds: 57%, EV -0.06 at -157
- Nickeil Alexander-Walker (ATL) UNDER 3.5 Assists: 57%, EV -0.06 at -156
- Coby White (CHA) UNDER 4.5 Assists: 57%, EV -0.06 at -152
- Sion James (CHA) UNDER 4.5 Rebounds: 56%, EV -0.06 at -152

## ORL at BKN (game 401909306)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 1.5 Steals | -227 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Desmond Bane (ORL) OVER 0.5 Steals | -226 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Julius Randle (BKN) UNDER 1.5 3-pointers made | -179 (DraftKings via ESPN) | 1.3 | 60% | 60% | -0.06 |

Combined probability 25.4%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Franz Wagner (ORL) UNDER 1.5 Steals: 65%, EV -0.06 at -227
- Desmond Bane (ORL) OVER 0.5 Steals: 65%, EV -0.06 at -226
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Nolan Traore (BKN) UNDER 2.5 Rebounds: 60%, EV -0.06 at -178
- Egor Demin (BKN) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -174
- Nolan Traore (BKN) UNDER 3.5 Assists: 58%, EV -0.06 at -166
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 57%, EV -0.06 at -159
- Nolan Traore (BKN) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -157

## IND at CLE (game 401909307)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| James Harden (CLE) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Jarrett Allen (CLE) UNDER 1.5 Blocks | -233 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Aaron Nesmith (IND) OVER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.9 | 62% | 62% | -0.06 |

Combined probability 26.6%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- James Harden (CLE) OVER 0.5 Steals: 66%, EV -0.06 at -233
- Jarrett Allen (CLE) UNDER 1.5 Blocks: 66%, EV -0.06 at -233
- Aaron Nesmith (IND) OVER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Aaron Nesmith (IND) OVER 1.5 Assists: 60%, EV -0.06 at -177
- Tyrese Proctor (CLE) OVER 1.5 3-pointers made: 59%, EV -0.06 at -174
- Tyrese Proctor (CLE) UNDER 3.5 Assists: 58%, EV -0.06 at -165
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 58%, EV -0.07 at -160

## TOR at DET (game 401909308)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kevin Huerter (DET) OVER 0.5 Steals | -240 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Jamal Shead (TOR) OVER 0.5 3-pointers made | -237 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Cade Cunningham (DET) UNDER 1.5 Steals | -230 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

Combined probability 28.5%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Kevin Huerter (DET) OVER 0.5 Steals: 66%, EV -0.06 at -240
- Jamal Shead (TOR) OVER 0.5 3-pointers made: 66%, EV -0.06 at -237
- Jamal Shead (TOR) UNDER 1.5 Steals: 65%, EV -0.06 at -231
- Cade Cunningham (DET) UNDER 1.5 Steals: 65%, EV -0.06 at -230
- Daniss Jenkins (DET) OVER 0.5 Steals: 65%, EV -0.06 at -228
- Jakob Poeltl (TOR) OVER 0.5 Steals: 63%, EV -0.06 at -206
- Ausar Thompson (DET) OVER 0.5 Blocks: 62%, EV -0.06 at -197
- Cade Cunningham (DET) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181

## WAS at CHI (game 401909309)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| AJ Dybantsa (WAS) UNDER 1.5 Steals | -211 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |
| Alex Sarr (WAS) UNDER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Matas Buzelis (CHI) OVER 0.5 Blocks | -197 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |

Combined probability 24.5%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- AJ Dybantsa (WAS) UNDER 1.5 Steals: 64%, EV -0.06 at -211
- Alex Sarr (WAS) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Matas Buzelis (CHI) OVER 0.5 Blocks: 62%, EV -0.06 at -197
- Matas Buzelis (CHI) OVER 0.5 Steals: 62%, EV -0.06 at -197
- Jalen Smith (CHI) UNDER 2.5 Assists: 61%, EV -0.06 at -189
- Trae Young (WAS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -188
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Isaac Okoro (CHI) OVER 0.5 Steals: 61%, EV -0.06 at -187

## NOP at OKC (game 401909310)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jeremiah Fears (NOP) UNDER 1.5 Steals | -243 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 Steals | -231 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Zion Williamson (NOP) UNDER 1.5 Steals | -229 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

Combined probability 28.4%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jeremiah Fears (NOP) UNDER 1.5 Steals: 66%, EV -0.06 at -243
- Herbert Jones (NOP) UNDER 1.5 Steals: 65%, EV -0.06 at -231
- Zion Williamson (NOP) UNDER 1.5 Steals: 65%, EV -0.06 at -229
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -215
- Shai Gilgeous-Alexander (OKC) OVER 0.5 Blocks: 64%, EV -0.06 at -215
- Jared McCain (OKC) OVER 0.5 Steals: 63%, EV -0.06 at -207
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 62%, EV -0.06 at -197
- Saddiq Bey (NOP) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190

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
- Collin Gillespie (PHX) OVER 2.5 Rebounds: 59%, EV -0.06 at -173
- Jalen Green (PHX) UNDER 3.5 Assists: 59%, EV -0.06 at -172
- Ace Bailey (UTA) UNDER 2.5 Assists: 59%, EV -0.06 at -170
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Dillon Brooks (PHX) OVER 1.5 Assists: 57%, EV -0.06 at -158

## HOU at DEN (game 401909312)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Amen Thompson (HOU) UNDER 0.5 3-pointers made | -335 (DraftKings via ESPN) | 0.5 | 73% | 73% | -0.06 |
| Alperen Sengun (HOU) OVER 0.5 Steals | -231 (DraftKings via ESPN) | 0.7 | 65% | 65% | -0.06 |
| Jamal Murray (DEN) OVER 0.5 Steals | -227 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 31.0%; parlay pays 2.7x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Amen Thompson (HOU) UNDER 0.5 3-pointers made: 73%, EV -0.06 at -335
- Alperen Sengun (HOU) OVER 0.5 Steals: 65%, EV -0.06 at -231
- Jamal Murray (DEN) OVER 0.5 Steals: 65%, EV -0.06 at -227
- Christian Braun (DEN) UNDER 1.5 Steals: 65%, EV -0.06 at -223
- Amen Thompson (HOU) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Christian Braun (DEN) OVER 1.5 Assists: 61%, EV -0.06 at -187
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Christian Braun (DEN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184

## SAC at LAL (game 401909313)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ziaire Williams (LAL) OVER 0.5 3-pointers made | -239 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made | -199 (DraftKings via ESPN) | 1.6 | 62% | 62% | -0.06 |
| Matisse Thybulle (LAL) UNDER 2.5 Steals | -190 (DraftKings via ESPN) | 2.4 | 61% | 61% | -0.06 |

Combined probability 25.4%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Ziaire Williams (LAL) OVER 0.5 3-pointers made: 66%, EV -0.06 at -239
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -199
- Matisse Thybulle (LAL) UNDER 2.5 Steals: 61%, EV -0.06 at -190
- Zach LaVine (SAC) UNDER 3.5 Rebounds: 59%, EV -0.06 at -172
- Darius Acuff Jr. (SAC) OVER 2.5 3-pointers made: 59%, EV -0.06 at -171
- Jake LaRavia (LAL) OVER 3.5 Rebounds: 58%, EV -0.06 at -164
- Collin Sexton (LAL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -162
- Walker Kessler (LAL) OVER 1.5 Blocks: 58%, EV -0.07 at -160
