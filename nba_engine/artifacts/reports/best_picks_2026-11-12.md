# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-11T16:56:39Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Jayson Tatum (BOS) OVER 0.5 Steals | -241 (DraftKings via ESPN) | 0.7 | 66% | 66% | -0.06 |
| Marcus Smart (HOU) UNDER 1.5 3-pointers made | -238 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |

**Combined probability 19.2%; parlay pays 4.0x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: De'Aaron Fox (SAS) UNDER 1.5 Steals (66%); Jayson Tatum (BOS) OVER 0.5 Steals (66%); Marcus Smart (HOU) UNDER 1.5 3-pointers made (66%). Combined probability 29.1%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyler Herro (MIL) UNDER 19.5 Points | -115 (DraftKings via ESPN) | 14.0 | 74% | 51% | +0.38 |
| Victor Wembanyama (SAS) UNDER 29.5 Points | -109 (DraftKings via ESPN) | 24.5 | 71% | 49% | +0.36 |

Combined probability 52.3%; parlay pays 3.6x; expected profit per 1 staked +0.87.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyler Herro (MIL) UNDER 19.5 Points | -115 (DraftKings via ESPN) | 14.0 | 74% | 51% | +0.38 |
| Victor Wembanyama (SAS) UNDER 29.5 Points | -109 (DraftKings via ESPN) | 24.5 | 71% | 49% | +0.36 |
| Sidy Cissoko (POR) UNDER 8.5 Points | -125 (DraftKings via ESPN) | 6.4 | 73% | 52% | +0.32 |

Combined probability 38.3%; parlay pays 6.5x; expected profit per 1 staked +1.47.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyler Herro (MIL) UNDER 19.5 Points | -115 (DraftKings via ESPN) | 14.0 | 74% | 51% | +0.38 |
| Victor Wembanyama (SAS) UNDER 29.5 Points | -109 (DraftKings via ESPN) | 24.5 | 71% | 49% | +0.36 |
| Sidy Cissoko (POR) UNDER 8.5 Points | -125 (DraftKings via ESPN) | 6.4 | 73% | 52% | +0.32 |
| Jayson Tatum (BOS) UNDER 26.5 Points | -118 (DraftKings via ESPN) | 20.0 | 71% | 51% | +0.30 |

Combined probability 27.0%; parlay pays 11.9x; expected profit per 1 staked +2.22.

Top single picks by model edge:

- Tyler Herro (MIL) UNDER 19.5 Points: model 74% vs book 51%, EV +0.38 at -115 (projection 14.0)
- Victor Wembanyama (SAS) UNDER 29.5 Points: model 71% vs book 49%, EV +0.36 at -109 (projection 24.5)
- Norman Powell (CHI) UNDER 18.5 Points: model 69% vs book 49%, EV +0.33 at -108 (projection 13.6)
- Sidy Cissoko (POR) UNDER 8.5 Points: model 73% vs book 52%, EV +0.32 at -125 (projection 6.4)
- Jake LaRavia (LAL) OVER 3.5 Rebounds: model 61% vs book 43%, EV +0.31 at +116 (projection 4.2)
- Jayson Tatum (BOS) UNDER 26.5 Points: model 71% vs book 51%, EV +0.30 at -118 (projection 20.0)
- Brayden Burries (MIL) UNDER 2.5 Assists: model 60% vs book 43%, EV +0.30 at +117 (projection 2.3)
- Ajay Mitchell (OKC) UNDER 18.5 Points: model 67% vs book 49%, EV +0.30 at -107 (projection 15.8)
- Andrew Nembhard (IND) OVER 7.5 Assists: model 61% vs book 45%, EV +0.28 at +109 (projection 7.7)
- Derrick White (BOS) UNDER 13.5 Points: model 69% vs book 52%, EV +0.27 at -121 (projection 11.0)
- Damian Lillard (POR) UNDER 19.5 Points: model 65% vs book 49%, EV +0.27 at -106 (projection 17.3)
- Luka Doncic (LAL) UNDER 34.5 Points: model 65% vs book 49%, EV +0.26 at -107 (projection 27.6)

## WAS at IND (game 401909966)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -206 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Kyshawn George (WAS) UNDER 2.5 3-pointers made | -180 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |
| Aaron Nesmith (IND) UNDER 2.5 3-pointers made | -173 (DraftKings via ESPN) | 1.8 | 59% | 59% | -0.06 |

Combined probability 22.6%; parlay pays 3.6x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Kyshawn George (WAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -180
- Aaron Nesmith (IND) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -173
- Trae Young (WAS) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -167
- AJ Dybantsa (WAS) UNDER 2.5 Assists: 57%, EV -0.06 at -156
- Tre Johnson (WAS) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -156
- Andrew Nembhard (IND) OVER 1.5 3-pointers made: 56%, EV -0.06 at -152
- Trae Young (WAS) OVER 8.5 Assists: 56%, EV -0.06 at -148

## CLE at NYK (game 401909967)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| OG Anunoby (NYK) UNDER 2.5 Assists | -183 (DraftKings via ESPN) | 2.2 | 61% | 61% | -0.06 |
| Mikal Bridges (NYK) UNDER 1.5 3-pointers made | -178 (DraftKings via ESPN) | 1.2 | 60% | 60% | -0.06 |

Combined probability 24.0%; parlay pays 3.4x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Donovan Mitchell (CLE) UNDER 1.5 Steals: 66%, EV -0.06 at -237
- OG Anunoby (NYK) UNDER 2.5 Assists: 61%, EV -0.06 at -183
- OG Anunoby (NYK) UNDER 1.5 Steals: 61%, EV -0.06 at -183
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Landry Shamet (NYK) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Evan Mobley (CLE) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Karl-Anthony Towns (NYK) OVER 2.5 Assists: 59%, EV -0.06 at -170
- Jalen Brunson (NYK) UNDER 3.5 Rebounds: 58%, EV -0.06 at -160

## BOS at TOR (game 401909968)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jayson Tatum (BOS) OVER 0.5 Steals | -241 (DraftKings via ESPN) | 0.7 | 66% | 66% | -0.06 |
| Derrick White (BOS) OVER 0.5 Steals | -239 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Payton Pritchard (BOS) OVER 1.5 3-pointers made | -187 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |

Combined probability 26.8%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jayson Tatum (BOS) OVER 0.5 Steals: 66%, EV -0.06 at -241
- Derrick White (BOS) OVER 0.5 Steals: 66%, EV -0.06 at -239
- Payton Pritchard (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- RJ Barrett (TOR) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181
- Derrick White (BOS) OVER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 59%, EV -0.06 at -174
- Neemias Queta (BOS) UNDER 1.5 Assists: 58%, EV -0.06 at -163
- Payton Pritchard (BOS) OVER 2.5 Rebounds: 58%, EV -0.06 at -163

## SAS at CHI (game 401909969)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Victor Wembanyama (SAS) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Dylan Harper (SAS) OVER 0.5 3-pointers made | -227 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |

Combined probability 28.4%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- De'Aaron Fox (SAS) UNDER 1.5 Steals: 66%, EV -0.06 at -242
- Victor Wembanyama (SAS) OVER 0.5 Steals: 66%, EV -0.06 at -233
- Dylan Harper (SAS) OVER 0.5 3-pointers made: 65%, EV -0.06 at -227
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -226
- Devin Vassell (SAS) UNDER 1.5 Steals: 62%, EV -0.06 at -196
- Josh Giddey (CHI) OVER 0.5 Steals: 61%, EV -0.06 at -190
- Caleb Wilson (CHI) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Norman Powell (CHI) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -167

## DEN at MEM (game 401909970)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ty Jerome (MEM) OVER 0.5 Steals | -232 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Jamal Murray (DEN) OVER 0.5 Steals | -225 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Cedric Coward (MEM) OVER 0.5 Steals | -212 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |

Combined probability 27.0%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ty Jerome (MEM) OVER 0.5 Steals: 66%, EV -0.06 at -232
- Jamal Murray (DEN) OVER 0.5 Steals: 65%, EV -0.06 at -225
- Cedric Coward (MEM) OVER 0.5 Steals: 64%, EV -0.06 at -212
- Nikola Jokic (DEN) OVER 0.5 Blocks: 64%, EV -0.06 at -211
- Christian Braun (DEN) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -193
- Cam Spencer (MEM) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178

## LAL at MIL (game 401909971)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Walker Kessler (LAL) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Austin Reaves (LAL) OVER 0.5 Steals | -220 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -211 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Walker Kessler (LAL) OVER 0.5 Steals: 66%, EV -0.06 at -233
- Austin Reaves (LAL) OVER 0.5 Steals: 64%, EV -0.06 at -220
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -211
- Kyle Kuzma (MIL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -195
- Walker Kessler (LAL) UNDER 2.5 Blocks: 62%, EV -0.06 at -193
- Jake LaRavia (LAL) OVER 0.5 3-pointers made: 59%, EV -0.06 at -172
- Austin Reaves (LAL) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -170

## BKN at NOP (game 401909972)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Karlo Matkovic (NOP) OVER 0.5 3-pointers made | -218 (DraftKings via ESPN) | 0.9 | 64% | 64% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -192 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |
| Michael Porter Jr. (BKN) OVER 1.5 Assists | -179 (DraftKings via ESPN) | 2.2 | 60% | 60% | -0.06 |

Combined probability 23.8%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Karlo Matkovic (NOP) OVER 0.5 3-pointers made: 64%, EV -0.06 at -218
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Michael Porter Jr. (BKN) OVER 1.5 Assists: 60%, EV -0.06 at -179
- Moritz Wagner (BKN) OVER 0.5 3-pointers made: 59%, EV -0.06 at -170
- Nolan Traore (BKN) UNDER 2.5 Rebounds: 59%, EV -0.06 at -170
- Dejounte Murray (NOP) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Saddiq Bey (NOP) OVER 1.5 Assists: 58%, EV -0.06 at -160
- Dejounte Murray (NOP) OVER 4.5 Assists: 57%, EV -0.06 at -157

## ORL at UTA (game 401909973)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Desmond Bane (ORL) OVER 2.5 Assists | -166 (DraftKings via ESPN) | 3.3 | 59% | 59% | -0.06 |
| Franz Wagner (ORL) UNDER 1.5 3-pointers made | -150 (DraftKings via ESPN) | 1.7 | 56% | 56% | -0.06 |

Combined probability 32.9%; parlay pays 2.7x; expected profit per 1 staked -0.12.

Top single picks (over or under, whichever the model prefers):

- Desmond Bane (ORL) OVER 2.5 Assists: 59%, EV -0.06 at -166
- Desmond Bane (ORL) OVER 2.5 3-pointers made: 58%, EV -0.06 at -161
- Franz Wagner (ORL) UNDER 1.5 3-pointers made: 56%, EV -0.06 at -150

## GSW at HOU (game 401909974)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Marcus Smart (HOU) UNDER 1.5 3-pointers made | -238 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Al Horford (GSW) UNDER 1.5 3-pointers made | -224 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Tari Eason (HOU) OVER 0.5 3-pointers made | -222 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

Combined probability 27.8%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Marcus Smart (HOU) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -238
- Al Horford (GSW) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -224
- Tari Eason (HOU) OVER 0.5 3-pointers made: 65%, EV -0.06 at -222
- Amen Thompson (HOU) UNDER 1.5 Steals: 64%, EV -0.06 at -216
- Brandin Podziemski (GSW) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -184
- Tari Eason (HOU) UNDER 1.5 Steals: 59%, EV -0.07 at -174
- Fred VanVleet (HOU) UNDER 3.5 Rebounds: 59%, EV -0.06 at -172
- De'Anthony Melton (GSW) UNDER 2.5 Assists: 59%, EV -0.06 at -171

## OKC at POR (game 401909975)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -231 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Kenrich Williams (OKC) OVER 0.5 3-pointers made | -228 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Ajay Mitchell (OKC) UNDER 1.5 3-pointers made | -220 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

Combined probability 27.7%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Donovan Clingan (POR) OVER 0.5 3-pointers made: 66%, EV -0.06 at -231
- Kenrich Williams (OKC) OVER 0.5 3-pointers made: 65%, EV -0.06 at -228
- Ajay Mitchell (OKC) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -220
- Ajay Mitchell (OKC) UNDER 1.5 Steals: 61%, EV -0.06 at -183
- Shai Gilgeous-Alexander (OKC) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Damian Lillard (POR) OVER 2.5 3-pointers made: 58%, EV -0.06 at -164
- Shai Gilgeous-Alexander (OKC) OVER 3.5 Rebounds: 58%, EV -0.06 at -161
- Jrue Holiday (POR) OVER 3.5 Rebounds: 58%, EV -0.06 at -160
