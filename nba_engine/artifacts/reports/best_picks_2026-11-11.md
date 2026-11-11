# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-11T15:21:41Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick White (BOS) OVER 0.5 Steals | -248 (DraftKings via ESPN) | 0.8 | 67% | 67% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Marcus Smart (HOU) OVER 0.5 3-pointers made | -236 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |

**Combined probability 19.3%; parlay pays 4.0x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Derrick White (BOS) OVER 0.5 Steals (67%); De'Aaron Fox (SAS) UNDER 1.5 Steals (66%); Donovan Mitchell (CLE) UNDER 1.5 Steals (66%). Combined probability 29.3%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyler Herro (MIL) UNDER 19.5 Points | -109 (DraftKings via ESPN) | 14.0 | 74% | 49% | +0.41 |
| Victor Wembanyama (SAS) UNDER 29.5 Points | -109 (DraftKings via ESPN) | 24.5 | 71% | 49% | +0.36 |

Combined probability 52.3%; parlay pays 3.7x; expected profit per 1 staked +0.92.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyler Herro (MIL) UNDER 19.5 Points | -109 (DraftKings via ESPN) | 14.0 | 74% | 49% | +0.41 |
| Victor Wembanyama (SAS) UNDER 29.5 Points | -109 (DraftKings via ESPN) | 24.5 | 71% | 49% | +0.36 |
| Jayson Tatum (BOS) UNDER 26.5 Points | -109 (DraftKings via ESPN) | 20.0 | 71% | 49% | +0.35 |

Combined probability 36.9%; parlay pays 7.0x; expected profit per 1 staked +1.60.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyler Herro (MIL) UNDER 19.5 Points | -109 (DraftKings via ESPN) | 14.0 | 74% | 49% | +0.41 |
| Victor Wembanyama (SAS) UNDER 29.5 Points | -109 (DraftKings via ESPN) | 24.5 | 71% | 49% | +0.36 |
| Jayson Tatum (BOS) UNDER 26.5 Points | -109 (DraftKings via ESPN) | 20.0 | 71% | 49% | +0.35 |
| Day'Ron Sharpe (BKN) UNDER 3.5 Assists | +114 (DraftKings via ESPN) | 3.1 | 62% | 44% | +0.33 |

Combined probability 22.9%; parlay pays 15.1x; expected profit per 1 staked +2.46.

Top single picks by model edge:

- Tyler Herro (MIL) UNDER 19.5 Points: model 74% vs book 49%, EV +0.41 at -109 (projection 14.0)
- Victor Wembanyama (SAS) UNDER 29.5 Points: model 71% vs book 49%, EV +0.36 at -109 (projection 24.5)
- Jayson Tatum (BOS) UNDER 26.5 Points: model 71% vs book 49%, EV +0.35 at -109 (projection 20.0)
- Day'Ron Sharpe (BKN) UNDER 3.5 Assists: model 62% vs book 44%, EV +0.33 at +114 (projection 3.1)
- Ajay Mitchell (OKC) UNDER 18.5 Points: model 67% vs book 48%, EV +0.33 at -103 (projection 15.8)
- Norman Powell (CHI) UNDER 18.5 Points: model 69% vs book 49%, EV +0.32 at -110 (projection 13.6)
- Andrew Nembhard (IND) OVER 7.5 Assists: model 61% vs book 44%, EV +0.32 at +115 (projection 7.7)
- Jake LaRavia (LAL) OVER 3.5 Rebounds: model 61% vs book 43%, EV +0.31 at +116 (projection 4.2)
- Brayden Burries (MIL) UNDER 2.5 Assists: model 60% vs book 43%, EV +0.30 at +117 (projection 2.3)
- Damian Lillard (POR) UNDER 20.5 Points: model 69% vs book 50%, EV +0.30 at -114 (projection 17.3)
- Franz Wagner (ORL) UNDER 7.5 Assists: model 67% vs book 49%, EV +0.28 at -110 (projection 6.2)
- Michael Porter Jr. (BKN) UNDER 23.5 Points: model 70% vs book 52%, EV +0.28 at -121 (projection 19.8)

## WAS at IND (game 401909966)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -206 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Kyshawn George (WAS) OVER 1.5 3-pointers made | -191 (DraftKings via ESPN) | 1.9 | 62% | 62% | -0.06 |
| Aaron Nesmith (IND) UNDER 2.5 3-pointers made | -179 (DraftKings via ESPN) | 1.8 | 60% | 60% | -0.06 |

Combined probability 23.4%; parlay pays 3.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Kyshawn George (WAS) OVER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Aaron Nesmith (IND) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -179
- Trae Young (WAS) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -173
- Tre Johnson (WAS) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -153
- Andrew Nembhard (IND) UNDER 7.5 Assists: 56%, EV -0.06 at -152
- Andrew Nembhard (IND) OVER 1.5 3-pointers made: 56%, EV -0.06 at -152
- AJ Dybantsa (WAS) UNDER 2.5 Assists: 56%, EV -0.06 at -151

## CLE at NYK (game 401909967)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| OG Anunoby (NYK) UNDER 2.5 Assists | -191 (DraftKings via ESPN) | 2.2 | 62% | 62% | -0.06 |
| Evan Mobley (CLE) UNDER 1.5 3-pointers made | -184 (DraftKings via ESPN) | 1.3 | 61% | 61% | -0.06 |

Combined probability 24.7%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Donovan Mitchell (CLE) UNDER 1.5 Steals: 66%, EV -0.06 at -237
- OG Anunoby (NYK) UNDER 2.5 Assists: 62%, EV -0.06 at -191
- Evan Mobley (CLE) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Landry Shamet (NYK) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- OG Anunoby (NYK) UNDER 1.5 Steals: 60%, EV -0.06 at -176
- Jalen Brunson (NYK) UNDER 3.5 Rebounds: 58%, EV -0.06 at -160
- Karl-Anthony Towns (NYK) UNDER 3.5 Assists: 57%, EV -0.06 at -159

## BOS at TOR (game 401909968)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick White (BOS) OVER 0.5 Steals | -248 (DraftKings via ESPN) | 0.8 | 67% | 67% | -0.06 |
| Jayson Tatum (BOS) OVER 0.5 Steals | -241 (DraftKings via ESPN) | 0.7 | 66% | 66% | -0.06 |
| Payton Pritchard (BOS) UNDER 2.5 3-pointers made | -178 (DraftKings via ESPN) | 2.1 | 60% | 60% | -0.06 |

Combined probability 26.6%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Derrick White (BOS) OVER 0.5 Steals: 67%, EV -0.06 at -248
- Jayson Tatum (BOS) OVER 0.5 Steals: 66%, EV -0.06 at -241
- Derrick White (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Payton Pritchard (BOS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -178
- RJ Barrett (TOR) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 59%, EV -0.06 at -174
- RJ Barrett (TOR) OVER 3.5 Assists: 59%, EV -0.06 at -168
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
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -214
- Devin Vassell (SAS) UNDER 1.5 Steals: 63%, EV -0.06 at -202
- Josh Giddey (CHI) OVER 0.5 Steals: 61%, EV -0.06 at -190
- Caleb Wilson (CHI) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Norman Powell (CHI) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -167

## DEN at MEM (game 401909970)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jamal Murray (DEN) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Ty Jerome (MEM) OVER 0.5 Steals | -232 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Cedric Coward (MEM) OVER 0.5 Steals | -212 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |

Combined probability 27.3%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jamal Murray (DEN) OVER 0.5 Steals: 66%, EV -0.06 at -233
- Ty Jerome (MEM) OVER 0.5 Steals: 66%, EV -0.06 at -232
- Cedric Coward (MEM) OVER 0.5 Steals: 64%, EV -0.06 at -212
- Nikola Jokic (DEN) OVER 0.5 Blocks: 64%, EV -0.06 at -211
- Christian Braun (DEN) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -193
- Cam Spencer (MEM) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178

## LAL at MIL (game 401909971)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Walker Kessler (LAL) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Austin Reaves (LAL) OVER 0.5 Steals | -212 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -211 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 26.6%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Walker Kessler (LAL) OVER 0.5 Steals: 66%, EV -0.06 at -233
- Austin Reaves (LAL) OVER 0.5 Steals: 64%, EV -0.06 at -212
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -211
- Kyle Kuzma (MIL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -195
- Walker Kessler (LAL) UNDER 2.5 Blocks: 62%, EV -0.06 at -193
- Jake LaRavia (LAL) OVER 0.5 3-pointers made: 59%, EV -0.06 at -174
- Austin Reaves (LAL) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -164

## BKN at NOP (game 401909972)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Herbert Jones (NOP) OVER 0.5 3-pointers made | -211 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Karlo Matkovic (NOP) OVER 0.5 3-pointers made | -190 (DraftKings via ESPN) | 0.8 | 61% | 61% | -0.06 |
| Michael Porter Jr. (BKN) OVER 1.5 Assists | -186 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |

Combined probability 23.9%; parlay pays 3.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Herbert Jones (NOP) OVER 0.5 3-pointers made: 64%, EV -0.06 at -211
- Karlo Matkovic (NOP) OVER 0.5 3-pointers made: 61%, EV -0.06 at -190
- Michael Porter Jr. (BKN) OVER 1.5 Assists: 61%, EV -0.06 at -186
- Dejounte Murray (NOP) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Nolan Traore (BKN) UNDER 2.5 Rebounds: 60%, EV -0.06 at -176
- Saddiq Bey (NOP) OVER 1.5 Assists: 60%, EV -0.06 at -175
- Nolan Traore (BKN) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -164
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -163

## ORL at UTA (game 401909973)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Desmond Bane (ORL) OVER 2.5 3-pointers made | -161 (DraftKings via ESPN) | 2.3 | 58% | 58% | -0.06 |
| Franz Wagner (ORL) UNDER 1.5 3-pointers made | -150 (DraftKings via ESPN) | 1.7 | 56% | 56% | -0.06 |

Combined probability 32.5%; parlay pays 2.7x; expected profit per 1 staked -0.12.

Top single picks (over or under, whichever the model prefers):

- Desmond Bane (ORL) OVER 2.5 3-pointers made: 58%, EV -0.06 at -161
- Franz Wagner (ORL) UNDER 1.5 3-pointers made: 56%, EV -0.06 at -150
- Franz Wagner (ORL) UNDER 6.5 Rebounds: 56%, EV -0.06 at -147

## GSW at HOU (game 401909974)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Marcus Smart (HOU) OVER 0.5 3-pointers made | -236 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Tari Eason (HOU) OVER 0.5 3-pointers made | -228 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Al Horford (GSW) UNDER 1.5 3-pointers made | -227 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 28.1%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Marcus Smart (HOU) OVER 0.5 3-pointers made: 66%, EV -0.06 at -236
- Tari Eason (HOU) OVER 0.5 3-pointers made: 65%, EV -0.06 at -228
- Al Horford (GSW) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -227
- Amen Thompson (HOU) UNDER 1.5 Steals: 64%, EV -0.06 at -217
- Brandin Podziemski (GSW) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -190
- Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -177
- Tari Eason (HOU) UNDER 1.5 Steals: 59%, EV -0.06 at -173
- Fred VanVleet (HOU) UNDER 3.5 Rebounds: 59%, EV -0.06 at -172

## OKC at POR (game 401909975)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -229 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Kenrich Williams (OKC) OVER 0.5 3-pointers made | -227 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Ajay Mitchell (OKC) UNDER 1.5 3-pointers made | -205 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Donovan Clingan (POR) OVER 0.5 3-pointers made: 65%, EV -0.06 at -229
- Kenrich Williams (OKC) OVER 0.5 3-pointers made: 65%, EV -0.06 at -227
- Ajay Mitchell (OKC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -205
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 61%, EV -0.06 at -187
- Ajay Mitchell (OKC) UNDER 1.5 Steals: 60%, EV -0.06 at -176
- Shai Gilgeous-Alexander (OKC) OVER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Damian Lillard (POR) OVER 2.5 3-pointers made: 59%, EV -0.06 at -167
- Toumani Camara (POR) OVER 3.5 Rebounds: 58%, EV -0.06 at -162
