# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-18T17:51:51Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Joel Embiid (PHI) UNDER 1.5 3-pointers made | -245 (DraftKings via ESPN) | 1.1 | 67% | 67% | -0.06 |
| Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks | -236 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Kelly Oubre Jr. (IND) UNDER 1.5 Steals | -235 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Jalen Johnson (ATL) UNDER 1.5 Steals | -235 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |

**Combined probability 19.0%; parlay pays 4.1x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Joel Embiid (PHI) UNDER 1.5 3-pointers made (67%); Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks (66%); Kelly Oubre Jr. (IND) UNDER 1.5 Steals (66%). Combined probability 28.9%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyler Herro (MIL) UNDER 4.5 Assists | -103 (DraftKings via ESPN) | 3.0 | 68% | 47% | +0.35 |
| Daniss Jenkins (DET) OVER 5.5 Assists | +117 (DraftKings via ESPN) | 6.4 | 61% | 43% | +0.33 |

Combined probability 41.8%; parlay pays 4.3x; expected profit per 1 staked +0.79.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyler Herro (MIL) UNDER 4.5 Assists | -103 (DraftKings via ESPN) | 3.0 | 68% | 47% | +0.35 |
| Daniss Jenkins (DET) OVER 5.5 Assists | +117 (DraftKings via ESPN) | 6.4 | 61% | 43% | +0.33 |
| Luka Doncic (LAL) OVER 1.5 Steals | +135 (DraftKings via ESPN) | 1.7 | 56% | 40% | +0.32 |

Combined probability 23.4%; parlay pays 10.1x; expected profit per 1 staked +1.35.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyler Herro (MIL) UNDER 4.5 Assists | -103 (DraftKings via ESPN) | 3.0 | 68% | 47% | +0.35 |
| Daniss Jenkins (DET) OVER 5.5 Assists | +117 (DraftKings via ESPN) | 6.4 | 61% | 43% | +0.33 |
| Luka Doncic (LAL) OVER 1.5 Steals | +135 (DraftKings via ESPN) | 1.7 | 56% | 40% | +0.32 |
| Luke Kennard (PHX) UNDER 8.5 Points | -107 (DraftKings via ESPN) | 7.2 | 66% | 49% | +0.27 |

Combined probability 15.4%; parlay pays 19.4x; expected profit per 1 staked +1.99.

Top single picks by model edge:

- Tyler Herro (MIL) UNDER 4.5 Assists: model 68% vs book 47%, EV +0.35 at -103 (projection 3.0)
- Tyler Herro (MIL) UNDER 2.5 3-pointers made: model 63% vs book 44%, EV +0.34 at +113 (projection 1.8)
- Daniss Jenkins (DET) OVER 5.5 Assists: model 61% vs book 43%, EV +0.33 at +117 (projection 6.4)
- Luka Doncic (LAL) OVER 1.5 Steals: model 56% vs book 40%, EV +0.32 at +135 (projection 1.7)
- Andrew Wiggins (MIA) OVER 3.5 Rebounds: model 56% vs book 41%, EV +0.27 at +127 (projection 3.8)
- Luke Kennard (PHX) UNDER 8.5 Points: model 66% vs book 49%, EV +0.27 at -107 (projection 7.2)
- Ivica Zubac (IND) UNDER 9.5 Rebounds: model 72% vs book 53%, EV +0.26 at -133 (projection 7.3)
- Luke Kennard (PHX) UNDER 1.5 3-pointers made: model 63% vs book 47%, EV +0.26 at +100 (projection 1.3)
- Luguentz Dort (ATL) UNDER 10.5 Points: model 71% vs book 53%, EV +0.26 at -129 (projection 8.2)
- Al Horford (GSW) UNDER 2.5 Assists: model 63% vs book 47%, EV +0.26 at +100 (projection 2.1)
- Al Horford (GSW) UNDER 1.5 3-pointers made: model 69% vs book 52%, EV +0.25 at -124 (projection 1.1)
- Jalen Johnson (ATL) OVER 1.5 3-pointers made: model 54% vs book 40%, EV +0.25 at +134 (projection 1.6)

## MEM at CLE (game 401910007)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) UNDER 1.5 Steals | -227 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Cam Spencer (MEM) UNDER 2.5 3-pointers made | -189 (DraftKings via ESPN) | 2.2 | 61% | 61% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -185 (DraftKings via ESPN) | 1.2 | 61% | 61% | -0.06 |

Combined probability 24.2%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Cedric Coward (MEM) UNDER 1.5 Steals: 65%, EV -0.06 at -227
- Cam Spencer (MEM) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -189
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 61%, EV -0.06 at -185
- Cedric Coward (MEM) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -183
- Jaylen Wells (MEM) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Jarrett Allen (CLE) UNDER 1.5 Blocks: 61%, EV -0.07 at -184
- Cameron Boozer (MEM) OVER 1.5 3-pointers made: 60%, EV -0.06 at -182
- Peyton Watson (CLE) UNDER 1.5 Blocks: 58%, EV -0.06 at -165

## HOU at IND (game 401910008)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kelly Oubre Jr. (IND) UNDER 1.5 Steals | -235 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Fred VanVleet (HOU) UNDER 1.5 Steals | -231 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Amen Thompson (HOU) UNDER 1.5 Steals | -208 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 27.2%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Kelly Oubre Jr. (IND) UNDER 1.5 Steals: 66%, EV -0.06 at -235
- Fred VanVleet (HOU) UNDER 1.5 Steals: 65%, EV -0.06 at -231
- Amen Thompson (HOU) UNDER 1.5 Steals: 63%, EV -0.06 at -208
- Kelly Oubre Jr. (IND) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181
- Aaron Nesmith (IND) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Fred VanVleet (HOU) UNDER 3.5 Rebounds: 58%, EV -0.06 at -163
- Kevin Durant (HOU) OVER 1.5 3-pointers made: 57%, EV -0.06 at -157

## MIL at MIA (game 401910009)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks | -236 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -234 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Davion Mitchell (MIA) OVER 1.5 3-pointers made | -176 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |

Combined probability 25.9%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks: 66%, EV -0.06 at -236
- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -234
- Bam Adebayo (MIA) UNDER 1.5 Steals: 62%, EV -0.06 at -193
- Davion Mitchell (MIA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Myles Turner (MIL) OVER 1.5 Assists: 60%, EV -0.06 at -175
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Andrew Wiggins (MIA) UNDER 3.5 Rebounds: 59%, EV -0.06 at -167
- Brayden Burries (MIL) UNDER 3.5 Assists: 58%, EV -0.06 at -161

## PHI at ORL (game 401910010)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Joel Embiid (PHI) UNDER 1.5 3-pointers made | -245 (DraftKings via ESPN) | 1.1 | 67% | 67% | -0.06 |
| Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made | -222 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Dean Wade (PHI) UNDER 1.5 3-pointers made | -215 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

Combined probability 27.6%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Joel Embiid (PHI) UNDER 1.5 3-pointers made: 67%, EV -0.06 at -245
- Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -222
- Dean Wade (PHI) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -215
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 63%, EV -0.06 at -205
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 62%, EV -0.06 at -199
- Anfernee Simons (PHI) UNDER 2.5 Rebounds: 61%, EV -0.06 at -188
- Anfernee Simons (PHI) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -180
- Joel Embiid (PHI) UNDER 3.5 Assists: 60%, EV -0.06 at -177

## CHI at BKN (game 401910011)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Noah Clowney (BKN) OVER 0.5 3-pointers made | -214 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Isaac Okoro (CHI) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Patrick Williams (CHI) UNDER 1.5 3-pointers made | -193 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |

Combined probability 24.4%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Noah Clowney (BKN) OVER 0.5 3-pointers made: 64%, EV -0.06 at -214
- Isaac Okoro (CHI) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Patrick Williams (CHI) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -193
- Jalen Smith (CHI) OVER 1.5 Assists: 61%, EV -0.06 at -189
- Matas Buzelis (CHI) OVER 1.5 Assists: 61%, EV -0.06 at -186
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Isaac Okoro (CHI) OVER 1.5 Assists: 60%, EV -0.06 at -174
- Michael Porter Jr. (BKN) OVER 1.5 Assists: 59%, EV -0.06 at -173

## WAS at TOR (game 401910012)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| AJ Dybantsa (WAS) UNDER 1.5 Steals | -231 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Alex Sarr (WAS) UNDER 1.5 3-pointers made | -212 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Kyshawn George (WAS) OVER 1.5 3-pointers made | -173 (DraftKings via ESPN) | 1.9 | 59% | 59% | -0.06 |

Combined probability 24.8%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- AJ Dybantsa (WAS) UNDER 1.5 Steals: 65%, EV -0.06 at -231
- Alex Sarr (WAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -212
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -204
- AJ Dybantsa (WAS) UNDER 2.5 Assists: 61%, EV -0.06 at -188
- Kyshawn George (WAS) OVER 1.5 3-pointers made: 59%, EV -0.06 at -173
- Trae Young (WAS) OVER 1.5 3-pointers made: 59%, EV -0.06 at -170
- Alex Sarr (WAS) OVER 1.5 Assists: 58%, EV -0.06 at -162
- Alex Sarr (WAS) UNDER 1.5 Blocks: 57%, EV -0.07 at -155

## DET at NOP (game 401910013)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| John Collins (DET) UNDER 1.5 3-pointers made | -207 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Cade Cunningham (DET) OVER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 2.3 | 62% | 62% | -0.06 |
| Kevin Huerter (DET) OVER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |

Combined probability 24.0%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- John Collins (DET) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -207
- Cade Cunningham (DET) OVER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Kevin Huerter (DET) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Zion Williamson (NOP) UNDER 1.5 Steals: 61%, EV -0.06 at -184
- Daniss Jenkins (DET) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Herbert Jones (NOP) UNDER 3.5 Rebounds: 59%, EV -0.06 at -171
- Kevin Huerter (DET) OVER 2.5 Assists: 58%, EV -0.06 at -164

## ATL at OKC (game 401910014)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Johnson (ATL) UNDER 1.5 Steals | -235 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals | -193 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| Alex Caruso (OKC) UNDER 1.5 3-pointers made | -183 (DraftKings via ESPN) | 1.1 | 61% | 61% | -0.06 |

Combined probability 24.6%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jalen Johnson (ATL) UNDER 1.5 Steals: 66%, EV -0.06 at -235
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 62%, EV -0.06 at -193
- Alex Caruso (OKC) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Shai Gilgeous-Alexander (OKC) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Jalen Johnson (ATL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Luguentz Dort (ATL) UNDER 3.5 Rebounds: 59%, EV -0.06 at -173
- Nickeil Alexander-Walker (ATL) UNDER 3.5 Assists: 59%, EV -0.06 at -171

## BOS at DEN (game 401910015)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Christian Braun (DEN) UNDER 2.5 Assists | -198 (DraftKings via ESPN) | 2.3 | 62% | 62% | -0.06 |
| Sam Hauser (BOS) OVER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |
| Derrick White (BOS) OVER 1.5 3-pointers made | -183 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |

Combined probability 23.2%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Christian Braun (DEN) UNDER 2.5 Assists: 62%, EV -0.06 at -198
- Sam Hauser (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Derrick White (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Aaron Gordon (DEN) OVER 1.5 Assists: 60%, EV -0.06 at -178
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Payton Pritchard (BOS) UNDER 3.5 Rebounds: 59%, EV -0.06 at -171
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Derrick White (BOS) UNDER 3.5 Rebounds: 59%, EV -0.06 at -167

## GSW at DAL (game 401910016)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 1.5 Steals | -216 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Cooper Flagg (DAL) UNDER 1.5 Steals | -182 (DraftKings via ESPN) | 1.4 | 60% | 60% | -0.06 |
| Yaxel Lendeborg (GSW) UNDER 2.5 3-pointers made | -168 (DraftKings via ESPN) | 2.4 | 59% | 59% | -0.06 |

Combined probability 22.7%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Kyrie Irving (DAL) UNDER 1.5 Steals: 64%, EV -0.06 at -216
- Cooper Flagg (DAL) UNDER 1.5 Steals: 60%, EV -0.06 at -182
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 60%, EV -0.06 at -179
- Yaxel Lendeborg (GSW) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -168
- P.J. Washington (DAL) OVER 1.5 3-pointers made: 58%, EV -0.06 at -160
- Caleb Martin (DAL) UNDER 2.5 Assists: 57%, EV -0.06 at -157
- Caleb Martin (DAL) UNDER 3.5 Rebounds: 57%, EV -0.06 at -155
- P.J. Washington (DAL) UNDER 6.5 Rebounds: 57%, EV -0.06 at -154

## UTA at LAL (game 401910017)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Luka Doncic (LAL) UNDER 1.5 Steals | -180 (DraftKings via ESPN) | 1.7 | 60% | 60% | -0.06 |
| Keyonte George (UTA) OVER 3.5 Rebounds | -166 (DraftKings via ESPN) | 3.3 | 59% | 59% | -0.06 |
| Ace Bailey (UTA) OVER 1.5 3-pointers made | -163 (DraftKings via ESPN) | 2.0 | 58% | 58% | -0.06 |

Combined probability 20.5%; parlay pays 4.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Luka Doncic (LAL) UNDER 1.5 Steals: 60%, EV -0.06 at -180
- Keyonte George (UTA) OVER 3.5 Rebounds: 59%, EV -0.06 at -166
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 58%, EV -0.06 at -163
- Walker Kessler (LAL) OVER 1.5 Blocks: 58%, EV -0.06 at -162
- Darryn Peterson (UTA) UNDER 4.5 Assists: 58%, EV -0.06 at -159
- Keyonte George (UTA) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -157
- Darryn Peterson (UTA) UNDER 2.5 3-pointers made: 56%, EV -0.06 at -151
- Keyonte George (UTA) UNDER 7.5 Assists: 56%, EV -0.06 at -148

## PHX at SAC (game 401910018)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darius Acuff Jr. (SAC) UNDER 1.5 Steals | -235 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Collin Gillespie (PHX) UNDER 1.5 Steals | -210 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |
| Devin Booker (PHX) OVER 1.5 3-pointers made | -183 (DraftKings via ESPN) | 2.2 | 61% | 61% | -0.06 |

Combined probability 25.3%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Darius Acuff Jr. (SAC) UNDER 1.5 Steals: 66%, EV -0.06 at -235
- Collin Gillespie (PHX) UNDER 1.5 Steals: 63%, EV -0.06 at -210
- Devin Booker (PHX) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Zach LaVine (SAC) UNDER 3.5 Rebounds: 60%, EV -0.06 at -176
- Darius Acuff Jr. (SAC) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -171
- Devin Booker (PHX) UNDER 5.5 Assists: 58%, EV -0.06 at -162
- Miles Bridges (PHX) UNDER 2.5 Assists: 57%, EV -0.06 at -159
- Collin Gillespie (PHX) UNDER 3.5 Rebounds: 57%, EV -0.06 at -159
