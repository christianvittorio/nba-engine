# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-11T21:03:29Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ty Jerome (MEM) OVER 0.5 Steals | -244 (DraftKings via ESPN) | 0.8 | 67% | 67% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Kenrich Williams (OKC) OVER 0.5 3-pointers made | -236 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Al Horford (GSW) UNDER 1.5 3-pointers made | -232 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |

**Combined probability 19.1%; parlay pays 4.1x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Ty Jerome (MEM) OVER 0.5 Steals (67%); De'Aaron Fox (SAS) UNDER 1.5 Steals (66%); Kenrich Williams (OKC) OVER 0.5 3-pointers made (66%). Combined probability 29.1%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 4.5 Assists | +107 (DraftKings via ESPN) | 3.3 | 75% | 45% | +0.55 |
| Victor Wembanyama (SAS) UNDER 29.5 Points | -103 (DraftKings via ESPN) | 24.6 | 70% | 48% | +0.38 |

Combined probability 52.5%; parlay pays 4.1x; expected profit per 1 staked +1.14.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 4.5 Assists | +107 (DraftKings via ESPN) | 3.3 | 75% | 45% | +0.55 |
| Victor Wembanyama (SAS) UNDER 29.5 Points | -103 (DraftKings via ESPN) | 24.6 | 70% | 48% | +0.38 |
| Sidy Cissoko (POR) UNDER 8.5 Points | -119 (DraftKings via ESPN) | 6.4 | 73% | 51% | +0.35 |

Combined probability 38.5%; parlay pays 7.5x; expected profit per 1 staked +1.89.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 4.5 Assists | +107 (DraftKings via ESPN) | 3.3 | 75% | 45% | +0.55 |
| Victor Wembanyama (SAS) UNDER 29.5 Points | -103 (DraftKings via ESPN) | 24.6 | 70% | 48% | +0.38 |
| Sidy Cissoko (POR) UNDER 8.5 Points | -119 (DraftKings via ESPN) | 6.4 | 73% | 51% | +0.35 |
| Baylor Scheierman (BOS) UNDER 8.5 Points | -119 (DraftKings via ESPN) | 6.4 | 73% | 51% | +0.34 |

Combined probability 28.1%; parlay pays 13.8x; expected profit per 1 staked +2.88.

Top single picks by model edge:

- Darryn Peterson (UTA) UNDER 4.5 Assists: model 75% vs book 45%, EV +0.55 at +107 (projection 3.3)
- Victor Wembanyama (SAS) UNDER 29.5 Points: model 70% vs book 48%, EV +0.38 at -103 (projection 24.6)
- Sidy Cissoko (POR) UNDER 8.5 Points: model 73% vs book 51%, EV +0.35 at -119 (projection 6.4)
- Baylor Scheierman (BOS) UNDER 8.5 Points: model 73% vs book 51%, EV +0.34 at -119 (projection 6.4)
- Michael Porter Jr. (BKN) UNDER 24.5 Points: model 73% vs book 51%, EV +0.34 at -119 (projection 20.2)
- Dylan Harper (SAS) UNDER 17.5 Points: model 70% vs book 49%, EV +0.33 at -109 (projection 14.9)
- Norman Powell (CHI) UNDER 18.5 Points: model 68% vs book 48%, EV +0.32 at -105 (projection 13.7)
- Brayden Burries (MIL) UNDER 13.5 Points: model 72% vs book 52%, EV +0.31 at -124 (projection 10.7)
- Shai Gilgeous-Alexander (OKC) UNDER 32.5 Points: model 67% vs book 48%, EV +0.30 at -105 (projection 28.3)
- Ajay Mitchell (OKC) UNDER 18.5 Points: model 67% vs book 49%, EV +0.30 at -107 (projection 15.8)
- Jaime Jaquez Jr. (MIL) UNDER 15.5 Points: model 72% vs book 52%, EV +0.30 at -124 (projection 12.6)
- Josh Okogie (UTA) UNDER 6.5 Points: model 69% vs book 51%, EV +0.29 at -116 (projection 5.3)

## WAS at IND (game 401909966)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -206 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Kyshawn George (WAS) UNDER 2.5 3-pointers made | -190 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |
| Trae Young (WAS) UNDER 2.5 3-pointers made | -175 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |

Combined probability 23.1%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Kyshawn George (WAS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -190
- Trae Young (WAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Aaron Nesmith (IND) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -173
- AJ Dybantsa (WAS) UNDER 2.5 Assists: 57%, EV -0.06 at -158
- Tre Johnson (WAS) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -155
- Andrew Nembhard (IND) OVER 1.5 3-pointers made: 56%, EV -0.06 at -152
- Alex Sarr (WAS) UNDER 7.5 Rebounds: 56%, EV -0.06 at -148

## CLE at NYK (game 401909967)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -234 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| OG Anunoby (NYK) UNDER 2.5 Assists | -188 (DraftKings via ESPN) | 2.2 | 61% | 61% | -0.06 |
| Evan Mobley (CLE) UNDER 1.5 3-pointers made | -180 (DraftKings via ESPN) | 1.3 | 60% | 60% | -0.06 |

Combined probability 24.2%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Donovan Mitchell (CLE) UNDER 1.5 Steals: 66%, EV -0.06 at -234
- OG Anunoby (NYK) UNDER 2.5 Assists: 61%, EV -0.06 at -188
- OG Anunoby (NYK) UNDER 1.5 Steals: 61%, EV -0.06 at -186
- Evan Mobley (CLE) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -164
- James Harden (CLE) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -153
- Landry Shamet (NYK) OVER 1.5 3-pointers made: 56%, EV -0.00 at -130
- Jalen Brunson (NYK) UNDER 3.5 Rebounds: 56%, EV -0.06 at -151

## BOS at TOR (game 401909968)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick White (BOS) UNDER 1.5 Steals | -221 (DraftKings via ESPN) | 0.8 | 65% | 65% | -0.06 |
| Jayson Tatum (BOS) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 0.7 | 64% | 64% | -0.06 |
| RJ Barrett (TOR) UNDER 2.5 3-pointers made | -180 (DraftKings via ESPN) | 2.1 | 60% | 60% | -0.06 |

Combined probability 24.9%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Derrick White (BOS) UNDER 1.5 Steals: 65%, EV -0.06 at -221
- Jayson Tatum (BOS) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- Derrick White (BOS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -183
- RJ Barrett (TOR) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -180
- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 59%, EV -0.07 at -174
- Payton Pritchard (BOS) UNDER 3.5 Rebounds: 58%, EV -0.06 at -161
- Ja'Kobe Walter (TOR) UNDER 4.5 Rebounds: 57%, EV -0.06 at -155
- Neemias Queta (BOS) UNDER 1.5 Assists: 57%, EV -0.06 at -154

## SAS at CHI (game 401909969)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Dylan Harper (SAS) OVER 0.5 3-pointers made | -232 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Victor Wembanyama (SAS) OVER 0.5 Steals | -232 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |

Combined probability 28.5%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- De'Aaron Fox (SAS) UNDER 1.5 Steals: 66%, EV -0.06 at -241
- Dylan Harper (SAS) OVER 0.5 3-pointers made: 66%, EV -0.06 at -232
- Victor Wembanyama (SAS) OVER 0.5 Steals: 66%, EV -0.06 at -232
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -229
- Josh Giddey (CHI) OVER 0.5 Steals: 63%, EV -0.06 at -201
- Devin Vassell (SAS) UNDER 1.5 Steals: 62%, EV -0.06 at -199
- Caleb Wilson (CHI) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -186
- Caleb Wilson (CHI) UNDER 1.5 Steals: 60%, EV -0.06 at -180

## DEN at MEM (game 401909970)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ty Jerome (MEM) OVER 0.5 Steals | -244 (DraftKings via ESPN) | 0.8 | 67% | 67% | -0.06 |
| Jamal Murray (DEN) OVER 0.5 Steals | -235 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Cedric Coward (MEM) OVER 0.5 Steals | -223 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

Combined probability 28.3%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ty Jerome (MEM) OVER 0.5 Steals: 67%, EV -0.06 at -244
- Jamal Murray (DEN) OVER 0.5 Steals: 66%, EV -0.06 at -235
- Cedric Coward (MEM) OVER 0.5 Steals: 65%, EV -0.06 at -223
- Nikola Jokic (DEN) OVER 0.5 Blocks: 64%, EV -0.06 at -212
- Christian Braun (DEN) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -193
- Cam Spencer (MEM) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 60%, EV -0.06 at -179

## LAL at MIL (game 401909971)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Walker Kessler (LAL) OVER 0.5 Steals | -209 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |
| Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.7 | 62% | 62% | -0.06 |
| Austin Reaves (LAL) OVER 0.5 Steals | -193 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |

Combined probability 24.2%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Walker Kessler (LAL) OVER 0.5 Steals: 63%, EV -0.06 at -209
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Austin Reaves (LAL) OVER 0.5 Steals: 62%, EV -0.06 at -193
- Walker Kessler (LAL) OVER 1.5 Blocks: 61%, EV -0.06 at -186
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Brayden Burries (MIL) OVER 2.5 Assists: 59%, EV -0.06 at -167
- Austin Reaves (LAL) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -160
- Tyler Herro (MIL) OVER 3.5 Assists: 58%, EV -0.06 at -160

## BKN at NOP (game 401909972)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Karlo Matkovic (NOP) OVER 0.5 3-pointers made | -198 (DraftKings via ESPN) | 0.9 | 62% | 62% | -0.06 |
| Julius Randle (BKN) UNDER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -186 (DraftKings via ESPN) | 1.0 | 61% | 61% | -0.06 |

Combined probability 23.5%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Karlo Matkovic (NOP) OVER 0.5 3-pointers made: 62%, EV -0.06 at -198
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Michael Porter Jr. (BKN) UNDER 2.5 Assists: 60%, EV -0.06 at -180
- Saddiq Bey (NOP) OVER 1.5 Assists: 60%, EV -0.06 at -179
- Dejounte Murray (NOP) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -170
- Nolan Traore (BKN) UNDER 2.5 Rebounds: 59%, EV -0.06 at -169
- Saddiq Bey (NOP) OVER 1.5 3-pointers made: 59%, EV -0.06 at -168

## ORL at UTA (game 401909973)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Green (UTA) UNDER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 0.8 | 62% | 62% | -0.06 |
| Ace Bailey (UTA) UNDER 2.5 3-pointers made | -189 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| Darryn Peterson (UTA) UNDER 2.5 3-pointers made | -179 (DraftKings via ESPN) | 1.8 | 60% | 60% | -0.06 |

Combined probability 22.9%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Josh Green (UTA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Ace Bailey (UTA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -189
- Darryn Peterson (UTA) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -179
- Desmond Bane (ORL) OVER 2.5 Assists: 58%, EV -0.06 at -164
- Desmond Bane (ORL) OVER 2.5 3-pointers made: 57%, EV -0.06 at -156
- Franz Wagner (ORL) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -156
- Desmond Bane (ORL) UNDER 4.5 Rebounds: 56%, EV -0.06 at -152
- Josh Green (UTA) UNDER 2.5 Rebounds: 56%, EV -0.06 at -150

## GSW at HOU (game 401909974)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Al Horford (GSW) UNDER 1.5 3-pointers made | -232 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Marcus Smart (HOU) OVER 0.5 3-pointers made | -223 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Tari Eason (HOU) OVER 0.5 3-pointers made | -213 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 27.2%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Al Horford (GSW) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -232
- Marcus Smart (HOU) OVER 0.5 3-pointers made: 65%, EV -0.06 at -223
- Tari Eason (HOU) OVER 0.5 3-pointers made: 64%, EV -0.06 at -213
- Stephen Curry (GSW) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Amen Thompson (HOU) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Brandin Podziemski (GSW) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -194
- De'Anthony Melton (GSW) UNDER 1.5 Steals: 61%, EV -0.06 at -185
- Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -182

## OKC at POR (game 401909975)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kenrich Williams (OKC) OVER 0.5 3-pointers made | -236 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Ajay Mitchell (OKC) UNDER 1.5 3-pointers made | -226 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -216 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

Combined probability 27.6%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Kenrich Williams (OKC) OVER 0.5 3-pointers made: 66%, EV -0.06 at -236
- Ajay Mitchell (OKC) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -226
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 64%, EV -0.06 at -216
- Ajay Mitchell (OKC) UNDER 1.5 Steals: 61%, EV -0.06 at -183
- Jared McCain (OKC) OVER 2.5 Rebounds: 59%, EV -0.06 at -170
- Damian Lillard (POR) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -169
- Jared McCain (OKC) OVER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Shai Gilgeous-Alexander (OKC) OVER 3.5 Rebounds: 59%, EV -0.06 at -166
