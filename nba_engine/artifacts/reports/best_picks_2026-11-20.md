# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-20T17:36:43Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Amen Thompson (HOU) UNDER 0.5 3-pointers made | -340 (DraftKings via ESPN) | 0.5 | 73% | 73% | -0.06 |
| Jamal Shead (TOR) UNDER 1.5 3-pointers made | -233 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Jeremiah Fears (NOP) UNDER 1.5 Steals | -232 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Ziaire Williams (LAL) OVER 0.5 3-pointers made | -202 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |

**Combined probability 19.7%; parlay pays 4.0x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Amen Thompson (HOU) UNDER 0.5 3-pointers made (73%); Jamal Shead (TOR) UNDER 1.5 3-pointers made (66%); Jeremiah Fears (NOP) UNDER 1.5 Steals (66%). Combined probability 31.4%; parlay pays 2.6x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) UNDER 6.5 Assists | -113 (DraftKings via ESPN) | 5.1 | 72% | 50% | +0.35 |
| Jeremiah Fears (NOP) UNDER 5.5 Assists | +102 (DraftKings via ESPN) | 4.5 | 66% | 46% | +0.33 |

Combined probability 47.3%; parlay pays 3.8x; expected profit per 1 staked +0.80.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) UNDER 6.5 Assists | -113 (DraftKings via ESPN) | 5.1 | 72% | 50% | +0.35 |
| Jeremiah Fears (NOP) UNDER 5.5 Assists | +102 (DraftKings via ESPN) | 4.5 | 66% | 46% | +0.33 |
| Jamison Battle (TOR) UNDER 3.5 Rebounds | -125 (DraftKings via ESPN) | 2.4 | 73% | 52% | +0.32 |

Combined probability 34.7%; parlay pays 6.9x; expected profit per 1 staked +1.38.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) UNDER 6.5 Assists | -113 (DraftKings via ESPN) | 5.1 | 72% | 50% | +0.35 |
| Jeremiah Fears (NOP) UNDER 5.5 Assists | +102 (DraftKings via ESPN) | 4.5 | 66% | 46% | +0.33 |
| Jamison Battle (TOR) UNDER 3.5 Rebounds | -125 (DraftKings via ESPN) | 2.4 | 73% | 52% | +0.32 |
| Darryn Peterson (UTA) UNDER 17.5 Points | -103 (DraftKings via ESPN) | 15.2 | 66% | 48% | +0.31 |

Combined probability 23.0%; parlay pays 13.5x; expected profit per 1 staked +2.11.

Top single picks by model edge:

- Alperen Sengun (HOU) UNDER 6.5 Assists: model 72% vs book 50%, EV +0.35 at -113 (projection 5.1)
- Jeremiah Fears (NOP) UNDER 5.5 Assists: model 66% vs book 46%, EV +0.33 at +102 (projection 4.5)
- Jamison Battle (TOR) UNDER 3.5 Rebounds: model 73% vs book 52%, EV +0.32 at -125 (projection 2.4)
- Alperen Sengun (HOU) UNDER 8.5 Rebounds: model 67% vs book 48%, EV +0.31 at -105 (projection 6.9)
- Darryn Peterson (UTA) UNDER 17.5 Points: model 66% vs book 48%, EV +0.31 at -103 (projection 15.2)
- Malik Monk (SAC) UNDER 3.5 Assists: model 60% vs book 43%, EV +0.29 at +116 (projection 3.1)
- Malik Monk (SAC) UNDER 11.5 Points: model 70% vs book 51%, EV +0.28 at -119 (projection 9.2)
- Daniss Jenkins (DET) OVER 5.5 Assists: model 59% vs book 43%, EV +0.27 at +116 (projection 6.2)
- Jakob Poeltl (TOR) UNDER 7.5 Rebounds: model 66% vs book 49%, EV +0.27 at -108 (projection 6.2)
- Tre Jones (CHI) UNDER 13.5 Points: model 68% vs book 51%, EV +0.26 at -117 (projection 11.2)
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: model 67% vs book 50%, EV +0.26 at -115 (projection 2.8)
- Julius Randle (BKN) UNDER 4.5 Assists: model 67% vs book 50%, EV +0.26 at -113 (projection 3.7)

## CHA at ATL (game 401909305)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Onyeka Okongwu (ATL) OVER 1.5 3-pointers made | -184 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |
| Naz Reid (CHA) UNDER 2.5 3-pointers made | -171 (DraftKings via ESPN) | 2.8 | 59% | 59% | -0.06 |
| Sion James (CHA) UNDER 1.5 3-pointers made | -167 (DraftKings via ESPN) | 1.4 | 59% | 59% | -0.06 |

Combined probability 21.0%; parlay pays 3.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Onyeka Okongwu (ATL) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Naz Reid (CHA) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -171
- Sion James (CHA) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Coby White (CHA) OVER 1.5 3-pointers made: 58%, EV -0.06 at -163
- Jalen Johnson (ATL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -161
- Sion James (CHA) OVER 3.5 Rebounds: 57%, EV -0.06 at -158
- Nickeil Alexander-Walker (ATL) UNDER 3.5 Assists: 57%, EV -0.06 at -157
- Coby White (CHA) UNDER 4.5 Assists: 57%, EV -0.06 at -155

## ORL at BKN (game 401909306)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nolan Traore (BKN) UNDER 2.5 Rebounds | -181 (DraftKings via ESPN) | 1.6 | 60% | 60% | -0.06 |
| Julius Randle (BKN) UNDER 1.5 3-pointers made | -179 (DraftKings via ESPN) | 1.3 | 60% | 60% | -0.06 |
| Egor Demin (BKN) UNDER 2.5 3-pointers made | -175 (DraftKings via ESPN) | 1.7 | 60% | 60% | -0.06 |

Combined probability 21.7%; parlay pays 3.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Nolan Traore (BKN) UNDER 2.5 Rebounds: 60%, EV -0.06 at -181
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Nolan Traore (BKN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Egor Demin (BKN) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Nolan Traore (BKN) UNDER 3.5 Assists: 59%, EV -0.06 at -171
- Anthony Black (ORL) UNDER 4.5 Rebounds: 57%, EV -0.06 at -154
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 57%, EV -0.06 at -153
- Michael Porter Jr. (BKN) OVER 1.5 Assists: 55%, EV -0.07 at -146

## IND at CLE (game 401909307)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Aaron Nesmith (IND) UNDER 2.5 3-pointers made | -189 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |
| Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made | -180 (DraftKings via ESPN) | 1.3 | 60% | 60% | -0.06 |
| Tyrese Proctor (CLE) UNDER 3.5 Assists | -163 (DraftKings via ESPN) | 3.6 | 58% | 58% | -0.06 |

Combined probability 21.4%; parlay pays 3.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Aaron Nesmith (IND) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -189
- Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Aaron Nesmith (IND) OVER 1.5 Assists: 58%, EV -0.06 at -163
- Tyrese Proctor (CLE) UNDER 3.5 Assists: 58%, EV -0.06 at -163
- Tyrese Proctor (CLE) OVER 1.5 3-pointers made: 57%, EV -0.06 at -153
- James Harden (CLE) UNDER 5.5 Rebounds: 56%, EV -0.06 at -146
- James Harden (CLE) OVER 6.5 Assists: 55%, EV -0.06 at -145
- James Harden (CLE) UNDER 2.5 3-pointers made: 55%, EV -0.06 at -144

## TOR at DET (game 401909308)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jamal Shead (TOR) UNDER 1.5 3-pointers made | -233 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Cade Cunningham (DET) OVER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| John Collins (DET) UNDER 1.5 3-pointers made | -189 (DraftKings via ESPN) | 1.4 | 61% | 61% | -0.06 |

Combined probability 24.8%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jamal Shead (TOR) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -233
- Jamal Shead (TOR) UNDER 2.5 Rebounds: 62%, EV -0.06 at -193
- Cade Cunningham (DET) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- John Collins (DET) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Jamison Battle (TOR) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -172
- Javonte Green (DET) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Jakob Poeltl (TOR) OVER 1.5 Assists: 59%, EV -0.06 at -168
- Daniss Jenkins (DET) OVER 1.5 3-pointers made: 59%, EV -0.06 at -168

## WAS at CHI (game 401909309)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alex Sarr (WAS) UNDER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Trae Young (WAS) OVER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -189 (DraftKings via ESPN) | 1.3 | 61% | 61% | -0.06 |

Combined probability 23.4%; parlay pays 3.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Alex Sarr (WAS) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Trae Young (WAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Jalen Smith (CHI) UNDER 2.5 Assists: 61%, EV -0.06 at -183
- Matas Buzelis (CHI) UNDER 2.5 Assists: 61%, EV -0.06 at -182
- Kyshawn George (WAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -177
- Isaac Okoro (CHI) OVER 1.5 Assists: 59%, EV -0.06 at -173
- Anthony Davis (WAS) UNDER 2.5 Assists: 59%, EV -0.06 at -169

## NOP at OKC (game 401909310)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jeremiah Fears (NOP) UNDER 1.5 Steals | -232 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Kenrich Williams (OKC) UNDER 1.5 3-pointers made | -210 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |

Combined probability 25.8%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jeremiah Fears (NOP) UNDER 1.5 Steals: 66%, EV -0.06 at -232
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -210
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Saddiq Bey (NOP) UNDER 2.5 Assists: 62%, EV -0.06 at -194
- Saddiq Bey (NOP) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -182
- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -172
- Jared McCain (OKC) UNDER 3.5 Rebounds: 59%, EV -0.06 at -171
- Jared McCain (OKC) UNDER 2.5 Assists: 59%, EV -0.06 at -167

## PHX at UTA (game 401909311)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Devin Booker (PHX) OVER 1.5 3-pointers made | -183 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| Jalen Green (PHX) OVER 2.5 Assists | -175 (DraftKings via ESPN) | 3.0 | 60% | 60% | -0.06 |
| Ace Bailey (UTA) OVER 1.5 3-pointers made | -175 (DraftKings via ESPN) | 2.0 | 60% | 60% | -0.06 |

Combined probability 21.5%; parlay pays 3.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Devin Booker (PHX) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Jalen Green (PHX) OVER 2.5 Assists: 60%, EV -0.06 at -175
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Ace Bailey (UTA) UNDER 2.5 Assists: 59%, EV -0.06 at -167
- Darryn Peterson (UTA) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -167
- Collin Gillespie (PHX) UNDER 3.5 Rebounds: 58%, EV -0.06 at -163
- Brice Sensabaugh (UTA) UNDER 3.5 Rebounds: 57%, EV -0.06 at -154
- Darryn Peterson (UTA) UNDER 4.5 Assists: 56%, EV -0.06 at -151

## HOU at DEN (game 401909312)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Amen Thompson (HOU) UNDER 0.5 3-pointers made | -340 (DraftKings via ESPN) | 0.5 | 73% | 73% | -0.06 |
| Alperen Sengun (HOU) OVER 0.5 Steals | -228 (DraftKings via ESPN) | 0.7 | 65% | 65% | -0.06 |
| Christian Braun (DEN) UNDER 2.5 Assists | -195 (DraftKings via ESPN) | 2.4 | 62% | 62% | -0.06 |

Combined probability 29.5%; parlay pays 2.8x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Amen Thompson (HOU) UNDER 0.5 3-pointers made: 73%, EV -0.06 at -340
- Alperen Sengun (HOU) OVER 0.5 Steals: 65%, EV -0.06 at -228
- Amen Thompson (HOU) UNDER 1.5 Steals: 62%, EV -0.06 at -198
- Christian Braun (DEN) UNDER 2.5 Assists: 62%, EV -0.06 at -195
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Christian Braun (DEN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Nikola Jokic (DEN) UNDER 1.5 Steals: 60%, EV -0.06 at -177
- Aaron Gordon (DEN) OVER 1.5 Assists: 59%, EV -0.06 at -173

## SAC at LAL (game 401909313)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ziaire Williams (LAL) OVER 0.5 3-pointers made | -202 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |
| Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made | -191 (DraftKings via ESPN) | 1.6 | 62% | 62% | -0.06 |
| Darius Acuff Jr. (SAC) OVER 2.5 3-pointers made | -171 (DraftKings via ESPN) | 3.0 | 59% | 59% | -0.06 |

Combined probability 22.8%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ziaire Williams (LAL) OVER 0.5 3-pointers made: 63%, EV -0.06 at -202
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Darius Acuff Jr. (SAC) OVER 2.5 3-pointers made: 59%, EV -0.06 at -171
- Zach LaVine (SAC) UNDER 3.5 Rebounds: 59%, EV -0.06 at -166
- Matisse Thybulle (LAL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -166
- Jake LaRavia (LAL) OVER 3.5 Rebounds: 58%, EV -0.06 at -162
- De'Andre Hunter (SAC) OVER 1.5 3-pointers made: 58%, EV -0.06 at -162
- Matisse Thybulle (LAL) UNDER 2.5 Rebounds: 57%, EV -0.06 at -155
