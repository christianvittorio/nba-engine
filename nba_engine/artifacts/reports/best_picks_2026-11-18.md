# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-18T21:43:37Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brandin Podziemski (GSW) OVER 0.5 Steals | -248 (DraftKings via ESPN) | 1.0 | 67% | 67% | -0.06 |
| Trae Young (WAS) OVER 0.5 Steals | -239 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -237 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Darius Acuff Jr. (SAC) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |

**Combined probability 19.2%; parlay pays 4.0x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Brandin Podziemski (GSW) OVER 0.5 Steals (67%); Trae Young (WAS) OVER 0.5 Steals (66%); Bam Adebayo (MIA) UNDER 1.5 3-pointers made (66%). Combined probability 29.2%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Luka Doncic (LAL) OVER 1.5 Steals | +141 (DraftKings via ESPN) | 1.7 | 57% | 39% | +0.37 |
| James Harden (CLE) OVER 6.5 Assists | +111 (DraftKings via ESPN) | 6.8 | 64% | 44% | +0.35 |

Combined probability 36.4%; parlay pays 5.1x; expected profit per 1 staked +0.85.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Luka Doncic (LAL) OVER 1.5 Steals | +141 (DraftKings via ESPN) | 1.7 | 57% | 39% | +0.37 |
| James Harden (CLE) OVER 6.5 Assists | +111 (DraftKings via ESPN) | 6.8 | 64% | 44% | +0.35 |
| Tyler Herro (MIL) UNDER 21.5 Points | -117 (DraftKings via ESPN) | 14.9 | 72% | 51% | +0.33 |

Combined probability 26.2%; parlay pays 9.4x; expected profit per 1 staked +1.47.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Luka Doncic (LAL) OVER 1.5 Steals | +141 (DraftKings via ESPN) | 1.7 | 57% | 39% | +0.37 |
| James Harden (CLE) OVER 6.5 Assists | +111 (DraftKings via ESPN) | 6.8 | 64% | 44% | +0.35 |
| Tyler Herro (MIL) UNDER 21.5 Points | -117 (DraftKings via ESPN) | 14.9 | 72% | 51% | +0.33 |
| Luguentz Dort (ATL) UNDER 10.5 Points | -124 (DraftKings via ESPN) | 8.2 | 71% | 52% | +0.28 |

Combined probability 18.5%; parlay pays 17.0x; expected profit per 1 staked +2.16.

Top single picks by model edge:

- Luka Doncic (LAL) OVER 1.5 Steals: model 57% vs book 39%, EV +0.37 at +141 (projection 1.7)
- James Harden (CLE) OVER 6.5 Assists: model 64% vs book 44%, EV +0.35 at +111 (projection 6.8)
- Tyler Herro (MIL) UNDER 21.5 Points: model 72% vs book 51%, EV +0.33 at -117 (projection 14.9)
- Luguentz Dort (ATL) UNDER 10.5 Points: model 71% vs book 52%, EV +0.28 at -124 (projection 8.2)
- Alperen Sengun (HOU) UNDER 6.5 Assists: model 61% vs book 45%, EV +0.27 at +110 (projection 5.9)
- Luke Kennard (PHX) UNDER 1.5 3-pointers made: model 63% vs book 47%, EV +0.27 at +101 (projection 1.3)
- Tyler Herro (MIL) UNDER 2.5 3-pointers made: model 58% vs book 43%, EV +0.26 at +116 (projection 1.9)
- Tyler Herro (MIL) UNDER 4.5 Assists: model 62% vs book 46%, EV +0.25 at +103 (projection 3.3)
- James Harden (CLE) OVER 17.5 Points: model 66% vs book 50%, EV +0.25 at -112 (projection 19.0)
- Jalen Johnson (ATL) OVER 1.5 3-pointers made: model 54% vs book 40%, EV +0.25 at +134 (projection 1.6)
- Kevin Durant (HOU) UNDER 23.5 Points: model 69% vs book 52%, EV +0.25 at -123 (projection 20.2)
- Al Horford (GSW) UNDER 4.5 Rebounds: model 70% vs book 52%, EV +0.25 at -127 (projection 3.3)

## MEM at CLE (game 401910007)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) UNDER 1.5 Steals | -227 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Jarrett Allen (CLE) UNDER 1.5 Blocks | -211 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -201 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |

Combined probability 25.9%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Cedric Coward (MEM) UNDER 1.5 Steals: 65%, EV -0.06 at -227
- Jarrett Allen (CLE) UNDER 1.5 Blocks: 64%, EV -0.06 at -211
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 63%, EV -0.06 at -201
- Cam Spencer (MEM) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -195
- Cameron Boozer (MEM) OVER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Tyrese Proctor (CLE) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Cedric Coward (MEM) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -183
- Jaylen Wells (MEM) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183

## HOU at IND (game 401910008)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kelly Oubre Jr. (IND) UNDER 1.5 Steals | -235 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Fred VanVleet (HOU) UNDER 1.5 Steals | -231 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Amen Thompson (HOU) UNDER 1.5 Steals | -207 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 27.2%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Kelly Oubre Jr. (IND) UNDER 1.5 Steals: 66%, EV -0.06 at -235
- Fred VanVleet (HOU) UNDER 1.5 Steals: 65%, EV -0.06 at -231
- Amen Thompson (HOU) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181
- Aaron Nesmith (IND) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Fred VanVleet (HOU) UNDER 3.5 Rebounds: 58%, EV -0.06 at -165
- Kevin Durant (HOU) OVER 1.5 3-pointers made: 57%, EV -0.06 at -157

## MIL at MIA (game 401910009)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -237 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks | -238 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Myles Turner (MIL) OVER 1.5 Assists | -188 (DraftKings via ESPN) | 1.6 | 61% | 61% | -0.06 |

Combined probability 26.7%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -237
- Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks: 66%, EV -0.06 at -238
- Myles Turner (MIL) OVER 1.5 Assists: 61%, EV -0.06 at -188
- Bam Adebayo (MIA) UNDER 1.5 Steals: 61%, EV -0.06 at -188
- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Davion Mitchell (MIA) OVER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Bam Adebayo (MIA) UNDER 3.5 Assists: 58%, EV -0.06 at -161

## PHI at ORL (game 401910010)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Joel Embiid (PHI) UNDER 1.5 3-pointers made | -234 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Dean Wade (PHI) UNDER 1.5 3-pointers made | -213 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Anfernee Simons (PHI) UNDER 2.5 3-pointers made | -185 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |

Combined probability 25.6%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Joel Embiid (PHI) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -234
- Dean Wade (PHI) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -213
- Anfernee Simons (PHI) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 61%, EV -0.06 at -185
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: 60%, EV -0.06 at -179
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 60%, EV -0.06 at -177
- Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Anthony Black (ORL) UNDER 1.5 Steals: 59%, EV -0.06 at -169

## CHI at BKN (game 401910011)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Noah Clowney (BKN) OVER 0.5 3-pointers made | -210 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Patrick Williams (CHI) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |
| Isaac Okoro (CHI) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |

Combined probability 24.3%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Noah Clowney (BKN) OVER 0.5 3-pointers made: 64%, EV -0.06 at -210
- Patrick Williams (CHI) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Isaac Okoro (CHI) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Matas Buzelis (CHI) OVER 1.5 Assists: 62%, EV -0.06 at -193
- Jalen Smith (CHI) UNDER 2.5 Assists: 62%, EV -0.06 at -192
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Isaac Okoro (CHI) OVER 1.5 Assists: 60%, EV -0.06 at -174
- Michael Porter Jr. (BKN) OVER 1.5 Assists: 59%, EV -0.06 at -173

## WAS at TOR (game 401910012)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Trae Young (WAS) OVER 0.5 Steals | -239 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Anthony Davis (WAS) UNDER 1.5 Steals | -234 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |

Combined probability 28.2%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Trae Young (WAS) OVER 0.5 Steals: 66%, EV -0.06 at -239
- Anthony Davis (WAS) UNDER 1.5 Steals: 66%, EV -0.06 at -234
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 65%, EV -0.06 at -226
- Alex Sarr (WAS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -223
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -209
- Anthony Davis (WAS) UNDER 1.5 Blocks: 63%, EV -0.06 at -204
- Ja'Kobe Walter (TOR) OVER 1.5 Assists: 62%, EV -0.06 at -192
- Jamal Shead (TOR) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185

## DET at NOP (game 401910013)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| John Collins (DET) UNDER 1.5 3-pointers made | -200 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| Kevin Huerter (DET) UNDER 2.5 3-pointers made | -195 (DraftKings via ESPN) | 2.2 | 62% | 62% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |

Combined probability 24.0%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- John Collins (DET) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -200
- Kevin Huerter (DET) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -195
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Daniss Jenkins (DET) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -192
- Zion Williamson (NOP) UNDER 1.5 Steals: 60%, EV -0.06 at -176
- Cade Cunningham (DET) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Herbert Jones (NOP) UNDER 1.5 Steals: 58%, EV -0.07 at -164
- Zion Williamson (NOP) OVER 2.5 Assists: 58%, EV -0.06 at -163

## ATL at OKC (game 401910014)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Johnson (ATL) UNDER 1.5 Steals | -235 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Alex Caruso (OKC) UNDER 1.5 3-pointers made | -192 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made | -187 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |

Combined probability 24.8%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jalen Johnson (ATL) UNDER 1.5 Steals: 66%, EV -0.06 at -235
- Alex Caruso (OKC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -187
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 61%, EV -0.06 at -185
- Jalen Johnson (ATL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Aday Mara (OKC) UNDER 1.5 Blocks: 60%, EV -0.06 at -178
- Jared McCain (OKC) OVER 1.5 Assists: 60%, EV -0.06 at -177
- Nickeil Alexander-Walker (ATL) UNDER 3.5 Assists: 59%, EV -0.06 at -171

## BOS at DEN (game 401910015)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Christian Braun (DEN) UNDER 2.5 Assists | -198 (DraftKings via ESPN) | 2.3 | 62% | 62% | -0.06 |
| Sam Hauser (BOS) OVER 1.5 3-pointers made | -188 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |
| Derrick White (BOS) OVER 1.5 3-pointers made | -183 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |

Combined probability 23.1%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Christian Braun (DEN) UNDER 2.5 Assists: 62%, EV -0.06 at -198
- Sam Hauser (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Derrick White (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Aaron Gordon (DEN) OVER 1.5 Assists: 60%, EV -0.06 at -178
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -173
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Derrick White (BOS) UNDER 3.5 Rebounds: 59%, EV -0.06 at -167
- Payton Pritchard (BOS) UNDER 3.5 Rebounds: 59%, EV -0.06 at -166

## GSW at DAL (game 401910016)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brandin Podziemski (GSW) OVER 0.5 Steals | -248 (DraftKings via ESPN) | 1.0 | 67% | 67% | -0.06 |
| P.J. Washington (DAL) UNDER 1.5 Assists | -234 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -223 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

Combined probability 28.5%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Brandin Podziemski (GSW) OVER 0.5 Steals: 67%, EV -0.06 at -248
- P.J. Washington (DAL) UNDER 1.5 Assists: 66%, EV -0.06 at -234
- Kyrie Irving (DAL) UNDER 1.5 Steals: 65%, EV -0.06 at -223
- Cooper Flagg (DAL) UNDER 1.5 Steals: 61%, EV -0.06 at -188
- Yaxel Lendeborg (GSW) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -176
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 57%, EV -0.06 at -157
- Yaxel Lendeborg (GSW) UNDER 4.5 Assists: 57%, EV -0.06 at -157
- Caleb Martin (DAL) UNDER 2.5 Assists: 57%, EV -0.06 at -156

## UTA at LAL (game 401910017)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jake LaRavia (LAL) OVER 0.5 3-pointers made | -219 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Luka Doncic (LAL) UNDER 1.5 Steals | -189 (DraftKings via ESPN) | 1.7 | 61% | 61% | -0.06 |
| Ace Bailey (UTA) OVER 1.5 3-pointers made | -183 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |

Combined probability 23.9%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jake LaRavia (LAL) OVER 0.5 3-pointers made: 64%, EV -0.06 at -219
- Luka Doncic (LAL) UNDER 1.5 Steals: 61%, EV -0.06 at -189
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Darryn Peterson (UTA) UNDER 4.5 Assists: 57%, EV -0.06 at -159
- Ace Bailey (UTA) UNDER 5.5 Rebounds: 57%, EV -0.06 at -156
- Darryn Peterson (UTA) UNDER 4.5 Rebounds: 57%, EV -0.06 at -155
- Sandro Mamukelashvili (LAL) OVER 4.5 Rebounds: 57%, EV -0.06 at -154
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 56%, EV -0.06 at -150

## PHX at SAC (game 401910018)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darius Acuff Jr. (SAC) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Collin Gillespie (PHX) UNDER 1.5 Steals | -222 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Zach LaVine (SAC) OVER 2.5 Rebounds | -175 (DraftKings via ESPN) | 2.7 | 60% | 60% | -0.06 |

Combined probability 25.4%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Darius Acuff Jr. (SAC) UNDER 1.5 Steals: 66%, EV -0.06 at -236
- Collin Gillespie (PHX) UNDER 1.5 Steals: 65%, EV -0.06 at -222
- Zach LaVine (SAC) OVER 2.5 Rebounds: 60%, EV -0.06 at -175
- Devin Booker (PHX) OVER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Devin Booker (PHX) UNDER 3.5 Rebounds: 59%, EV -0.06 at -174
- Collin Gillespie (PHX) UNDER 3.5 Rebounds: 59%, EV -0.06 at -173
- Darius Acuff Jr. (SAC) OVER 2.5 3-pointers made: 59%, EV -0.06 at -173
- Jalen Green (PHX) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -170
