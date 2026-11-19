# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-19T02:57:35Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jarrett Allen (CLE) OVER 0.5 Blocks | -243 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Trae Young (WAS) OVER 0.5 Steals | -241 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Kelly Oubre Jr. (IND) OVER 0.5 Steals | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Darius Acuff Jr. (SAC) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |

**Combined probability 19.3%; parlay pays 4.0x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Jarrett Allen (CLE) OVER 0.5 Blocks (66%); Trae Young (WAS) OVER 0.5 Steals (66%); Kelly Oubre Jr. (IND) OVER 0.5 Steals (66%). Combined probability 29.1%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Mitchell (CLE) OVER 5.5 Assists | +119 (DraftKings via ESPN) | 5.8 | 63% | 43% | +0.38 |
| Tyler Herro (MIL) UNDER 21.5 Points | -115 (DraftKings via ESPN) | 14.9 | 72% | 51% | +0.34 |

Combined probability 45.4%; parlay pays 4.1x; expected profit per 1 staked +0.86.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Mitchell (CLE) OVER 5.5 Assists | +119 (DraftKings via ESPN) | 5.8 | 63% | 43% | +0.38 |
| Tyler Herro (MIL) UNDER 21.5 Points | -115 (DraftKings via ESPN) | 14.9 | 72% | 51% | +0.34 |
| Jabari Walker (PHI) UNDER 5.5 Rebounds | -115 (DraftKings via ESPN) | 4.0 | 71% | 50% | +0.32 |

Combined probability 32.1%; parlay pays 7.7x; expected profit per 1 staked +1.46.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Mitchell (CLE) OVER 5.5 Assists | +119 (DraftKings via ESPN) | 5.8 | 63% | 43% | +0.38 |
| Tyler Herro (MIL) UNDER 21.5 Points | -115 (DraftKings via ESPN) | 14.9 | 72% | 51% | +0.34 |
| Jabari Walker (PHI) UNDER 5.5 Rebounds | -115 (DraftKings via ESPN) | 4.0 | 71% | 50% | +0.32 |
| Charles Bassey (GSW) UNDER 6.5 Rebounds | +100 (DraftKings via ESPN) | 5.3 | 64% | 47% | +0.28 |

Combined probability 20.6%; parlay pays 15.3x; expected profit per 1 staked +2.16.

Top single picks by model edge:

- Donovan Mitchell (CLE) OVER 5.5 Assists: model 63% vs book 43%, EV +0.38 at +119 (projection 5.8)
- Tyler Herro (MIL) UNDER 21.5 Points: model 72% vs book 51%, EV +0.34 at -115 (projection 14.9)
- Jabari Walker (PHI) UNDER 5.5 Rebounds: model 71% vs book 50%, EV +0.32 at -115 (projection 4.0)
- James Harden (CLE) OVER 6.5 Assists: model 67% vs book 48%, EV +0.31 at -105 (projection 7.0)
- James Harden (CLE) OVER 18.5 Points: model 65% vs book 48%, EV +0.30 at -102 (projection 19.8)
- Andrew Wiggins (MIA) OVER 3.5 Rebounds: model 57% vs book 41%, EV +0.29 at +128 (projection 3.9)
- Charles Bassey (GSW) UNDER 6.5 Rebounds: model 64% vs book 47%, EV +0.28 at +100 (projection 5.3)
- Tyler Herro (MIL) UNDER 4.5 Assists: model 62% vs book 45%, EV +0.28 at +107 (projection 3.3)
- Luke Kennard (PHX) UNDER 1.5 3-pointers made: model 63% vs book 46%, EV +0.28 at +103 (projection 1.3)
- Brayden Burries (MIL) UNDER 13.5 Points: model 70% vs book 52%, EV +0.28 at -121 (projection 11.1)
- Brayden Burries (MIL) UNDER 0.5 Steals: model 52% vs book 38%, EV +0.27 at +144 (projection 0.7)
- Jakob Poeltl (TOR) UNDER 12.5 Points: model 71% vs book 52%, EV +0.27 at -125 (projection 10.0)

## MEM at CLE (game 401910007)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jarrett Allen (CLE) OVER 0.5 Blocks | -243 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Cedric Coward (MEM) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Cameron Boozer (MEM) OVER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 2.4 | 62% | 62% | -0.06 |

Combined probability 27.2%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jarrett Allen (CLE) OVER 0.5 Blocks: 66%, EV -0.06 at -243
- Cedric Coward (MEM) UNDER 1.5 Steals: 66%, EV -0.06 at -236
- Cameron Boozer (MEM) OVER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Tyrese Proctor (CLE) OVER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Meleek Thomas (CLE) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -194
- Cam Spencer (MEM) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -193
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 61%, EV -0.06 at -191
- Jaylen Wells (MEM) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183

## HOU at IND (game 401910008)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kelly Oubre Jr. (IND) OVER 0.5 Steals | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Fred VanVleet (HOU) OVER 0.5 Steals | -228 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Amen Thompson (HOU) UNDER 1.5 Steals | -209 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 27.3%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Kelly Oubre Jr. (IND) OVER 0.5 Steals: 66%, EV -0.06 at -239
- Fred VanVleet (HOU) OVER 0.5 Steals: 65%, EV -0.06 at -228
- Amen Thompson (HOU) UNDER 1.5 Steals: 63%, EV -0.06 at -209
- Tari Eason (HOU) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Obi Toppin (IND) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Jabari Smith Jr. (HOU) OVER 1.5 3-pointers made: 62%, EV -0.06 at -193
- Aaron Nesmith (IND) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -189
- Fred VanVleet (HOU) UNDER 3.5 Rebounds: 59%, EV -0.06 at -170

## MIL at MIA (game 401910009)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -225 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |
| Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks | -227 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Nate Ament (MIL) OVER 0.5 3-pointers made | -223 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

Combined probability 27.4%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -225
- Giannis Antetokounmpo (MIA) UNDER 1.5 Blocks: 65%, EV -0.06 at -227
- Nate Ament (MIL) OVER 0.5 3-pointers made: 65%, EV -0.06 at -223
- Giannis Antetokounmpo (MIA) OVER 0.5 Steals: 64%, EV -0.06 at -217
- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -197
- Davion Mitchell (MIA) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -194
- Brayden Burries (MIL) OVER 0.5 Steals: 62%, EV -0.06 at -193
- Bam Adebayo (MIA) UNDER 1.5 Steals: 60%, EV -0.06 at -175

## PHI at ORL (game 401910010)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Joel Embiid (PHI) UNDER 1.5 Blocks | -224 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Anfernee Simons (PHI) UNDER 2.5 Assists | -176 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |
| Desmond Bane (ORL) UNDER 3.5 3-pointers made | -171 (DraftKings via ESPN) | 2.4 | 59% | 59% | -0.06 |

Combined probability 22.9%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Joel Embiid (PHI) UNDER 1.5 Blocks: 65%, EV -0.06 at -224
- Joel Embiid (PHI) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -217
- Anfernee Simons (PHI) UNDER 2.5 Assists: 60%, EV -0.06 at -176
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -171
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 59%, EV -0.06 at -171
- Anthony Black (ORL) UNDER 1.5 Steals: 58%, EV -0.06 at -165
- Kentavious Caldwell-Pope (PHI) OVER 1.5 Assists: 56%, EV -0.06 at -150
- Kentavious Caldwell-Pope (PHI) OVER 2.5 Rebounds: 56%, EV -0.06 at -148

## CHI at BKN (game 401910011)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Noah Clowney (BKN) OVER 0.5 3-pointers made | -209 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Isaac Okoro (CHI) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Matas Buzelis (CHI) OVER 1.5 Assists | -193 (DraftKings via ESPN) | 2.3 | 62% | 62% | -0.06 |

Combined probability 24.3%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Noah Clowney (BKN) OVER 0.5 3-pointers made: 63%, EV -0.06 at -209
- Isaac Okoro (CHI) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Matas Buzelis (CHI) OVER 1.5 Assists: 62%, EV -0.06 at -193
- Jalen Smith (CHI) UNDER 2.5 Assists: 61%, EV -0.06 at -187
- Patrick Williams (CHI) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Isaac Okoro (CHI) OVER 1.5 Assists: 59%, EV -0.06 at -174
- Isaac Okoro (CHI) UNDER 3.5 Rebounds: 59%, EV -0.06 at -174

## WAS at TOR (game 401910012)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Trae Young (WAS) OVER 0.5 Steals | -241 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 Steals | -238 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Anthony Davis (WAS) UNDER 1.5 Steals | -227 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

Combined probability 28.5%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Trae Young (WAS) OVER 0.5 Steals: 66%, EV -0.06 at -241
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 66%, EV -0.06 at -238
- Anthony Davis (WAS) UNDER 1.5 Steals: 65%, EV -0.06 at -227
- Alex Sarr (WAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -215
- Anthony Davis (WAS) UNDER 1.5 Blocks: 63%, EV -0.06 at -208
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -202
- Trae Young (WAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Kyshawn George (WAS) OVER 0.5 Steals: 60%, EV -0.06 at -178

## DET at NOP (game 401910013)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -200 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| Daniss Jenkins (DET) UNDER 2.5 3-pointers made | -194 (DraftKings via ESPN) | 2.3 | 62% | 62% | -0.06 |
| John Collins (DET) UNDER 1.5 3-pointers made | -187 (DraftKings via ESPN) | 1.4 | 61% | 61% | -0.06 |

Combined probability 23.6%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -200
- Daniss Jenkins (DET) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -194
- John Collins (DET) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Kevin Huerter (DET) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -170
- Zion Williamson (NOP) OVER 2.5 Assists: 59%, EV -0.06 at -168
- Derik Queen (NOP) UNDER 2.5 Assists: 59%, EV -0.06 at -168
- Zion Williamson (NOP) UNDER 1.5 Steals: 58%, EV -0.06 at -166
- Herbert Jones (NOP) UNDER 1.5 Steals: 57%, EV -0.06 at -156

## ATL at OKC (game 401910014)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Johnson (ATL) UNDER 1.5 Steals | -233 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Kenrich Williams (OKC) UNDER 1.5 3-pointers made | -224 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Alex Caruso (OKC) UNDER 1.5 3-pointers made | -208 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 27.0%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jalen Johnson (ATL) UNDER 1.5 Steals: 66%, EV -0.06 at -233
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -224
- Alex Caruso (OKC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -208
- Shai Gilgeous-Alexander (OKC) OVER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Onyeka Okongwu (ATL) OVER 0.5 Blocks: 61%, EV -0.06 at -189
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 61%, EV -0.06 at -184
- Nickeil Alexander-Walker (ATL) UNDER 3.5 Assists: 60%, EV -0.06 at -179
- Jalen Johnson (ATL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -179

## BOS at DEN (game 401910015)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jayson Tatum (BOS) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Baylor Scheierman (BOS) UNDER 1.5 3-pointers made | -224 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Sam Hauser (BOS) UNDER 2.5 3-pointers made | -193 (DraftKings via ESPN) | 1.8 | 62% | 62% | -0.06 |

Combined probability 26.3%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jayson Tatum (BOS) OVER 0.5 Steals: 66%, EV -0.06 at -233
- Baylor Scheierman (BOS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -224
- Sam Hauser (BOS) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -193
- Derrick White (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Cameron Johnson (DEN) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- Cameron Johnson (DEN) OVER 1.5 Assists: 61%, EV -0.06 at -184
- DeMar DeRozan (DEN) UNDER 2.5 Rebounds: 61%, EV -0.06 at -184
- Aaron Gordon (DEN) UNDER 2.5 Assists: 60%, EV -0.06 at -179

## GSW at DAL (game 401910016)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brandin Podziemski (GSW) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -223 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Cooper Flagg (DAL) UNDER 1.5 Steals | -194 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |

Combined probability 26.4%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Brandin Podziemski (GSW) OVER 0.5 Steals: 66%, EV -0.06 at -236
- Kyrie Irving (DAL) UNDER 1.5 Steals: 65%, EV -0.06 at -223
- Cooper Flagg (DAL) UNDER 1.5 Steals: 62%, EV -0.06 at -194
- De'Anthony Melton (GSW) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Yaxel Lendeborg (GSW) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181
- Zaccharie Risacher (DAL) OVER 0.5 3-pointers made: 60%, EV -0.06 at -177
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -167
- P.J. Washington (DAL) UNDER 1.5 Assists: 58%, EV -0.06 at -161

## UTA at LAL (game 401910017)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ace Bailey (UTA) UNDER 2.5 Assists | -190 (DraftKings via ESPN) | 2.2 | 61% | 61% | -0.06 |
| Brice Sensabaugh (UTA) OVER 1.5 3-pointers made | -186 (DraftKings via ESPN) | 2.5 | 61% | 61% | -0.06 |
| Keyonte George (UTA) UNDER 2.5 3-pointers made | -171 (DraftKings via ESPN) | 2.2 | 59% | 59% | -0.06 |

Combined probability 22.1%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ace Bailey (UTA) UNDER 2.5 Assists: 61%, EV -0.06 at -190
- Brice Sensabaugh (UTA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Keyonte George (UTA) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -171
- Darryn Peterson (UTA) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -164
- Sandro Mamukelashvili (LAL) UNDER 4.5 Rebounds: 58%, EV -0.06 at -163
- Jake LaRavia (LAL) OVER 0.5 3-pointers made: 58%, EV -0.06 at -161
- Matisse Thybulle (LAL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -159
- Collin Sexton (LAL) OVER 2.5 Assists: 57%, EV -0.06 at -159

## PHX at SAC (game 401910018)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darius Acuff Jr. (SAC) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Collin Gillespie (PHX) UNDER 1.5 Steals | -217 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |
| Dylan Cardwell (SAC) OVER 0.5 Blocks | -215 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |

Combined probability 27.2%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Darius Acuff Jr. (SAC) UNDER 1.5 Steals: 66%, EV -0.06 at -239
- Collin Gillespie (PHX) UNDER 1.5 Steals: 64%, EV -0.06 at -217
- Dylan Cardwell (SAC) OVER 0.5 Blocks: 64%, EV -0.06 at -215
- Devin Booker (PHX) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Darius Acuff Jr. (SAC) OVER 2.5 3-pointers made: 59%, EV -0.06 at -172
- Keegan Murray (SAC) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Jalen Green (PHX) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -170
- Collin Gillespie (PHX) UNDER 3.5 Rebounds: 59%, EV -0.06 at -169
