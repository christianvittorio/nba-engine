# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-12T02:44:55Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ty Jerome (MEM) OVER 0.5 Steals | -242 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Jaxson Hayes (UTA) UNDER 1.5 Blocks | -238 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Draymond Green (GSW) OVER 0.5 Steals | -237 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -234 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |

**Combined probability 19.0%; parlay pays 4.1x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Ty Jerome (MEM) OVER 0.5 Steals (66%); Jaxson Hayes (UTA) UNDER 1.5 Blocks (66%); Draymond Green (GSW) OVER 0.5 Steals (66%). Combined probability 28.9%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 4.5 Assists | -127 (DraftKings via ESPN) | 3.3 | 75% | 52% | +0.34 |
| Nate Ament (MIL) UNDER 8.5 Points | +103 (DraftKings via ESPN) | 7.3 | 65% | 46% | +0.32 |

Combined probability 48.8%; parlay pays 3.6x; expected profit per 1 staked +0.77.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 4.5 Assists | -127 (DraftKings via ESPN) | 3.3 | 75% | 52% | +0.34 |
| Nate Ament (MIL) UNDER 8.5 Points | +103 (DraftKings via ESPN) | 7.3 | 65% | 46% | +0.32 |
| Alex Caruso (OKC) UNDER 8.5 Points | -110 (DraftKings via ESPN) | 5.8 | 69% | 49% | +0.32 |

Combined probability 33.7%; parlay pays 6.9x; expected profit per 1 staked +1.34.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darryn Peterson (UTA) UNDER 4.5 Assists | -127 (DraftKings via ESPN) | 3.3 | 75% | 52% | +0.34 |
| Nate Ament (MIL) UNDER 8.5 Points | +103 (DraftKings via ESPN) | 7.3 | 65% | 46% | +0.32 |
| Alex Caruso (OKC) UNDER 8.5 Points | -110 (DraftKings via ESPN) | 5.8 | 69% | 49% | +0.32 |
| James Harden (CLE) UNDER 0.5 Steals | +146 (DraftKings via ESPN) | 0.7 | 53% | 38% | +0.29 |

Combined probability 17.7%; parlay pays 17.0x; expected profit per 1 staked +2.02.

Top single picks by model edge:

- Darryn Peterson (UTA) UNDER 4.5 Assists: model 75% vs book 52%, EV +0.34 at -127 (projection 3.3)
- Nate Ament (MIL) UNDER 8.5 Points: model 65% vs book 46%, EV +0.32 at +103 (projection 7.3)
- Alex Caruso (OKC) UNDER 8.5 Points: model 69% vs book 49%, EV +0.32 at -110 (projection 5.8)
- Tyler Herro (MIL) UNDER 20.5 Points: model 71% vs book 51%, EV +0.30 at -119 (projection 15.5)
- Alex Caruso (OKC) UNDER 3.5 Rebounds: model 64% vs book 46%, EV +0.30 at +104 (projection 2.5)
- James Harden (CLE) UNDER 0.5 Steals: model 53% vs book 38%, EV +0.29 at +146 (projection 0.7)
- Sidy Cissoko (POR) UNDER 8.5 Points: model 71% vs book 53%, EV +0.26 at -127 (projection 6.8)
- Julian Champagnie (SAS) UNDER 2.5 3-pointers made: model 63% vs book 47%, EV +0.26 at +100 (projection 2.2)
- Sandro Mamukelashvili (LAL) OVER 4.5 Rebounds: model 60% vs book 45%, EV +0.26 at +110 (projection 5.2)
- Donovan Mitchell (CLE) UNDER 23.5 Points: model 64% vs book 48%, EV +0.25 at -105 (projection 20.9)
- Alex Caruso (OKC) UNDER 2.5 Assists: model 60% vs book 45%, EV +0.24 at +107 (projection 2.0)
- Brayden Burries (MIL) UNDER 3.5 Assists: model 75% vs book 56%, EV +0.24 at -151 (projection 2.5)

## WAS at IND (game 401909966)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -195 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Kyshawn George (WAS) UNDER 2.5 3-pointers made | -183 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |
| Trae Young (WAS) UNDER 2.5 3-pointers made | -175 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |

Combined probability 22.4%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -195
- Kyshawn George (WAS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -183
- Trae Young (WAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Aaron Nesmith (IND) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Tre Johnson (WAS) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -160
- Andrew Nembhard (IND) OVER 1.5 3-pointers made: 57%, EV -0.06 at -156
- AJ Dybantsa (WAS) UNDER 2.5 Assists: 56%, EV -0.06 at -151
- Trae Young (WAS) OVER 8.5 Assists: 56%, EV -0.06 at -148

## CLE at NYK (game 401909967)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -234 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Evan Mobley (CLE) UNDER 1.5 Blocks | -205 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Miles McBride (NYK) UNDER 1.5 Assists | -200 (DraftKings via ESPN) | 1.7 | 62% | 62% | -0.06 |

Combined probability 25.8%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Donovan Mitchell (CLE) UNDER 1.5 Steals: 66%, EV -0.06 at -234
- Evan Mobley (CLE) UNDER 1.5 Blocks: 63%, EV -0.06 at -205
- Miles McBride (NYK) UNDER 1.5 Assists: 62%, EV -0.06 at -200
- OG Anunoby (NYK) UNDER 1.5 Steals: 62%, EV -0.06 at -196
- James Harden (CLE) OVER 0.5 Steals: 62%, EV -0.06 at -196
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -177
- Meleek Thomas (CLE) UNDER 1.5 Assists: 60%, EV -0.06 at -177

## BOS at TOR (game 401909968)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick White (BOS) UNDER 1.5 Steals | -212 (DraftKings via ESPN) | 0.8 | 64% | 64% | -0.06 |
| Jayson Tatum (BOS) UNDER 1.5 Steals | -200 (DraftKings via ESPN) | 0.7 | 62% | 62% | -0.06 |
| Ja'Kobe Walter (TOR) UNDER 2.5 Assists | -196 (DraftKings via ESPN) | 2.3 | 62% | 62% | -0.06 |

Combined probability 24.7%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Derrick White (BOS) UNDER 1.5 Steals: 64%, EV -0.06 at -212
- Jayson Tatum (BOS) UNDER 1.5 Steals: 62%, EV -0.06 at -200
- Ja'Kobe Walter (TOR) UNDER 2.5 Assists: 62%, EV -0.06 at -196
- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 61%, EV -0.06 at -189
- Derrick White (BOS) OVER 1.5 3-pointers made: 60%, EV -0.06 at -182
- Collin Murray-Boyles (TOR) OVER 1.5 Assists: 59%, EV -0.06 at -173
- Neemias Queta (BOS) UNDER 1.5 Blocks: 59%, EV -0.06 at -172
- Sam Hauser (BOS) OVER 1.5 3-pointers made: 59%, EV -0.06 at -169

## SAS at CHI (game 401909969)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dylan Harper (SAS) OVER 0.5 3-pointers made | -230 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -229 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Caleb Wilson (CHI) UNDER 1.5 Steals | -228 (DraftKings via ESPN) | 1.5 | 65% | 65% | -0.06 |

Combined probability 27.8%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Dylan Harper (SAS) OVER 0.5 3-pointers made: 65%, EV -0.06 at -230
- De'Aaron Fox (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -229
- Caleb Wilson (CHI) UNDER 1.5 Steals: 65%, EV -0.06 at -228
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -217
- Tre Jones (CHI) UNDER 0.5 3-pointers made: 64%, EV -0.06 at -217
- Julian Champagnie (SAS) OVER 0.5 Steals: 64%, EV -0.06 at -217
- Victor Wembanyama (SAS) UNDER 1.5 Steals: 64%, EV -0.06 at -217
- Matas Buzelis (CHI) OVER 1.5 Assists: 61%, EV -0.06 at -190

## DEN at MEM (game 401909970)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ty Jerome (MEM) OVER 0.5 Steals | -242 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Zach Edey (MEM) UNDER 1.5 Blocks | -224 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Jamal Murray (DEN) UNDER 1.5 Steals | -220 (DraftKings via ESPN) | 0.9 | 64% | 64% | -0.06 |

Combined probability 27.7%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ty Jerome (MEM) OVER 0.5 Steals: 66%, EV -0.06 at -242
- Zach Edey (MEM) UNDER 1.5 Blocks: 65%, EV -0.06 at -224
- Jamal Murray (DEN) UNDER 1.5 Steals: 64%, EV -0.06 at -220
- Nikola Jokic (DEN) OVER 0.5 Blocks: 64%, EV -0.06 at -212
- Cam Spencer (MEM) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -197
- Christian Braun (DEN) UNDER 1.5 Steals: 62%, EV -0.06 at -197
- Cedric Coward (MEM) OVER 0.5 Steals: 62%, EV -0.06 at -192
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185

## LAL at MIL (game 401909971)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made | -230 (DraftKings via ESPN) | 1.7 | 65% | 65% | -0.06 |
| Collin Sexton (LAL) UNDER 1.5 3-pointers made | -208 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |
| Kel'el Ware (MIL) OVER 0.5 3-pointers made | -208 (DraftKings via ESPN) | 0.7 | 63% | 63% | -0.06 |

Combined probability 26.3%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -230
- Collin Sexton (LAL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -208
- Kel'el Ware (MIL) OVER 0.5 3-pointers made: 63%, EV -0.06 at -208
- Walker Kessler (LAL) OVER 0.5 Steals: 62%, EV -0.06 at -195
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Matisse Thybulle (LAL) UNDER 2.5 Rebounds: 62%, EV -0.06 at -192
- Jake LaRavia (LAL) OVER 0.5 3-pointers made: 61%, EV -0.06 at -189
- Austin Reaves (LAL) OVER 0.5 Steals: 61%, EV -0.06 at -185

## BKN at NOP (game 401909972)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Michael Porter Jr. (BKN) OVER 0.5 Steals | -231 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Karlo Matkovic (NOP) OVER 0.5 3-pointers made | -214 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Keon Ellis (BKN) OVER 0.5 3-pointers made | -212 (DraftKings via ESPN) | 0.9 | 64% | 64% | -0.06 |

Combined probability 26.7%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Michael Porter Jr. (BKN) OVER 0.5 Steals: 65%, EV -0.06 at -231
- Karlo Matkovic (NOP) OVER 0.5 3-pointers made: 64%, EV -0.06 at -214
- Keon Ellis (BKN) OVER 0.5 3-pointers made: 64%, EV -0.06 at -212
- Keon Ellis (BKN) UNDER 2.5 Rebounds: 62%, EV -0.06 at -192
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Dejounte Murray (NOP) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -174
- Michael Porter Jr. (BKN) UNDER 2.5 Assists: 59%, EV -0.06 at -173
- Saddiq Bey (NOP) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171

## ORL at UTA (game 401909973)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jaxson Hayes (UTA) UNDER 1.5 Blocks | -238 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Darryn Peterson (UTA) OVER 0.5 Steals | -218 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Josh Green (UTA) UNDER 1.5 3-pointers made | -206 (DraftKings via ESPN) | 0.8 | 63% | 63% | -0.06 |

Combined probability 26.8%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jaxson Hayes (UTA) UNDER 1.5 Blocks: 66%, EV -0.06 at -238
- Darryn Peterson (UTA) OVER 0.5 Steals: 64%, EV -0.06 at -218
- Josh Green (UTA) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Ace Bailey (UTA) OVER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Darryn Peterson (UTA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Keyonte George (UTA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Franz Wagner (ORL) UNDER 1.5 Steals: 60%, EV -0.06 at -175
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -168

## GSW at HOU (game 401909974)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Draymond Green (GSW) OVER 0.5 Steals | -237 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Tari Eason (HOU) OVER 0.5 3-pointers made | -234 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Stephen Curry (GSW) UNDER 1.5 Steals | -230 (DraftKings via ESPN) | 0.8 | 65% | 65% | -0.06 |

Combined probability 28.4%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Draymond Green (GSW) OVER 0.5 Steals: 66%, EV -0.06 at -237
- Tari Eason (HOU) OVER 0.5 3-pointers made: 66%, EV -0.06 at -234
- Stephen Curry (GSW) UNDER 1.5 Steals: 65%, EV -0.06 at -230
- Tari Eason (HOU) OVER 0.5 Steals: 65%, EV -0.06 at -223
- Marcus Smart (HOU) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -217
- De'Anthony Melton (GSW) UNDER 1.5 Steals: 64%, EV -0.06 at -218
- Amen Thompson (HOU) UNDER 1.5 Steals: 63%, EV -0.06 at -210
- Brandin Podziemski (GSW) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -193

## OKC at POR (game 401909975)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -213 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Kenrich Williams (OKC) OVER 0.5 3-pointers made | -198 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Sidy Cissoko (POR) UNDER 2.5 Assists | -195 (DraftKings via ESPN) | 2.0 | 62% | 62% | -0.06 |

Combined probability 24.7%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Donovan Clingan (POR) OVER 0.5 3-pointers made: 64%, EV -0.06 at -213
- Kenrich Williams (OKC) OVER 0.5 3-pointers made: 62%, EV -0.06 at -198
- Sidy Cissoko (POR) UNDER 2.5 Assists: 62%, EV -0.06 at -195
- Sidy Cissoko (POR) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Damian Lillard (POR) UNDER 3.5 3-pointers made: 60%, EV -0.06 at -175
- Shai Gilgeous-Alexander (OKC) OVER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Alex Caruso (OKC) UNDER 1.5 Steals: 59%, EV -0.06 at -169
- Jared McCain (OKC) UNDER 3.5 Rebounds: 59%, EV -0.06 at -167
