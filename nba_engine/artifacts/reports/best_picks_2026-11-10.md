# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-10T02:43:18Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dylan Harper (SAS) OVER 0.5 3-pointers made | -241 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Aaron Gordon (DEN) UNDER 0.5 Blocks | -235 (DraftKings via ESPN) | 0.3 | 66% | 66% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -229 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |

**Combined probability 18.8%; parlay pays 4.1x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Dylan Harper (SAS) OVER 0.5 3-pointers made (66%); Kyrie Irving (DAL) UNDER 1.5 Steals (66%); Aaron Gordon (DEN) UNDER 0.5 Blocks (66%). Combined probability 28.8%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Grayson Allen (CHA) UNDER 1.5 Steals | -197 (DraftKings via ESPN) | 1.0 | 75% | 62% | +0.13 |
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -222 (DraftKings via ESPN) | 1.0 | 74% | 65% | +0.07 |

Combined probability 55.4%; parlay pays 2.2x; expected profit per 1 staked +0.21.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Grayson Allen (CHA) UNDER 1.5 Steals | -197 (DraftKings via ESPN) | 1.0 | 75% | 62% | +0.13 |
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -222 (DraftKings via ESPN) | 1.0 | 74% | 65% | +0.07 |
| Kyshawn George (WAS) UNDER 2.5 3-pointers made | -189 (DraftKings via ESPN) | 1.8 | 73% | 61% | +0.11 |

Combined probability 40.2%; parlay pays 3.3x; expected profit per 1 staked +0.35.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Grayson Allen (CHA) UNDER 1.5 Steals | -197 (DraftKings via ESPN) | 1.0 | 75% | 62% | +0.13 |
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -222 (DraftKings via ESPN) | 1.0 | 74% | 65% | +0.07 |
| Kyshawn George (WAS) UNDER 2.5 3-pointers made | -189 (DraftKings via ESPN) | 1.8 | 73% | 61% | +0.11 |
| Jamal Shead (TOR) UNDER 11.5 Points | -118 (DraftKings via ESPN) | 9.5 | 71% | 51% | +0.31 |

Combined probability 28.5%; parlay pays 6.2x; expected profit per 1 staked +0.76.

Top single picks by model edge:

- Saddiq Bey (NOP) UNDER 5.5 Rebounds: model 69% vs book 48%, EV +0.34 at -105 (projection 4.4)
- Zach Edey (MEM) UNDER 9.5 Points: model 66% vs book 47%, EV +0.33 at +101 (projection 8.2)
- Julian Champagnie (SAS) UNDER 11.5 Points: model 74% vs book 52%, EV +0.32 at -125 (projection 9.1)
- Miles Bridges (PHX) OVER 6.5 Rebounds: model 61% vs book 43%, EV +0.32 at +116 (projection 7.4)
- Herbert Jones (NOP) UNDER 3.5 Rebounds: model 70% vs book 50%, EV +0.31 at -115 (projection 2.7)
- Jamal Shead (TOR) UNDER 11.5 Points: model 71% vs book 51%, EV +0.31 at -118 (projection 9.5)
- Jamal Shead (TOR) UNDER 8.5 Assists: model 62% vs book 45%, EV +0.29 at +108 (projection 7.5)
- Cade Cunningham (DET) UNDER 25.5 Points: model 66% vs book 49%, EV +0.28 at -106 (projection 22.7)
- Julian Champagnie (SAS) UNDER 2.5 3-pointers made: model 70% vs book 52%, EV +0.27 at -124 (projection 1.9)
- Derik Queen (NOP) UNDER 7.5 Rebounds: model 67% vs book 49%, EV +0.26 at -112 (projection 6.1)
- Evan Mobley (CLE) UNDER 0.5 Steals: model 57% vs book 42%, EV +0.26 at +121 (projection 0.6)
- Alperen Sengun (HOU) OVER 0.5 3-pointers made: model 55% vs book 42%, EV +0.24 at +125 (projection 0.8)

## LAL at ATL (game 401909952)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nickeil Alexander-Walker (ATL) UNDER 1.5 Steals | -206 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |
| Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made | -203 (DraftKings via ESPN) | 1.6 | 63% | 63% | -0.06 |
| Walker Kessler (LAL) OVER 0.5 Steals | -199 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |

Combined probability 24.7%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Nickeil Alexander-Walker (ATL) UNDER 1.5 Steals: 63%, EV -0.06 at -206
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Walker Kessler (LAL) OVER 0.5 Steals: 62%, EV -0.06 at -199
- Walker Kessler (LAL) UNDER 2.5 Blocks: 62%, EV -0.06 at -197
- CJ McCollum (ATL) UNDER 2.5 Rebounds: 61%, EV -0.06 at -187
- Collin Sexton (LAL) UNDER 2.5 Rebounds: 61%, EV -0.06 at -187
- Aaron Wiggins (ATL) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -182
- Matisse Thybulle (LAL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -168

## CLE at CHA (game 401909953)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -229 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Evan Mobley (CLE) UNDER 1.5 Blocks | -224 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Tidjane Salaun (CHA) UNDER 1.5 3-pointers made | -214 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

Combined probability 27.0%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Donovan Mitchell (CLE) UNDER 1.5 Steals: 65%, EV -0.06 at -229
- Evan Mobley (CLE) UNDER 1.5 Blocks: 65%, EV -0.06 at -224
- Tidjane Salaun (CHA) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -214
- James Harden (CLE) UNDER 1.5 Steals: 64%, EV -0.06 at -214
- Mario Hezonja (CLE) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -211
- Ryan Kalkbrenner (CHA) UNDER 1.5 Blocks: 63%, EV -0.06 at -208
- Evan Mobley (CLE) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -205
- Grayson Allen (CHA) UNDER 1.5 Steals: 62%, EV -0.06 at -197

## WAS at DET (game 401909954)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alex Sarr (WAS) OVER 0.5 3-pointers made | -223 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Trae Young (WAS) OVER 0.5 Steals | -221 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -217 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Alex Sarr (WAS) OVER 0.5 3-pointers made: 65%, EV -0.06 at -223
- Trae Young (WAS) OVER 0.5 Steals: 65%, EV -0.06 at -221
- Alex Sarr (WAS) UNDER 1.5 Blocks: 65%, EV -0.06 at -221
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -217
- Kyshawn George (WAS) UNDER 1.5 Steals: 64%, EV -0.06 at -216
- Cade Cunningham (DET) UNDER 1.5 Steals: 62%, EV -0.06 at -199
- Alex Sarr (WAS) OVER 1.5 Assists: 62%, EV -0.06 at -192
- AJ Dybantsa (WAS) UNDER 1.5 Steals: 62%, EV -0.06 at -192

## MEM at TOR (game 401909955)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jaylen Wells (MEM) UNDER 1.5 Assists | -183 (DraftKings via ESPN) | 1.3 | 61% | 61% | -0.06 |
| Ja'Kobe Walter (TOR) UNDER 1.5 Steals | -183 (DraftKings via ESPN) | 1.3 | 61% | 61% | -0.06 |
| Cam Spencer (MEM) UNDER 1.5 3-pointers made | -164 (DraftKings via ESPN) | 1.2 | 58% | 58% | -0.06 |

Combined probability 21.3%; parlay pays 3.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jaylen Wells (MEM) UNDER 1.5 Assists: 61%, EV -0.06 at -183
- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 61%, EV -0.06 at -183
- Ja'Kobe Walter (TOR) UNDER 2.5 Assists: 60%, EV -0.06 at -175
- Jaylen Wells (MEM) OVER 2.5 Rebounds: 59%, EV -0.06 at -170
- Cam Spencer (MEM) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -164
- Jerami Grant (MEM) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -157
- RJ Barrett (TOR) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -157
- Ty Jerome (MEM) OVER 2.5 Rebounds: 57%, EV -0.06 at -156

## IND at DAL (game 401909956)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kyrie Irving (DAL) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Pascal Siakam (IND) OVER 0.5 Steals | -226 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Jarace Walker (IND) UNDER 1.5 3-pointers made | -202 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Kyrie Irving (DAL) UNDER 1.5 Steals: 66%, EV -0.06 at -237
- Pascal Siakam (IND) OVER 0.5 Steals: 65%, EV -0.06 at -226
- Jarace Walker (IND) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -202
- Aaron Nesmith (IND) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Daniel Gafford (DAL) UNDER 1.5 Blocks: 60%, EV -0.06 at -177
- Pascal Siakam (IND) OVER 2.5 Assists: 60%, EV -0.06 at -174
- Pascal Siakam (IND) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Cooper Flagg (DAL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -172

## DEN at HOU (game 401909957)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Aaron Gordon (DEN) UNDER 0.5 Blocks | -235 (DraftKings via ESPN) | 0.3 | 66% | 66% | -0.06 |
| Alperen Sengun (HOU) OVER 0.5 Steals | -227 (DraftKings via ESPN) | 0.8 | 65% | 65% | -0.06 |
| Amen Thompson (HOU) OVER 0.5 Steals | -222 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |

Combined probability 27.6%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Aaron Gordon (DEN) UNDER 0.5 Blocks: 66%, EV -0.06 at -235
- Alperen Sengun (HOU) OVER 0.5 Steals: 65%, EV -0.06 at -227
- Amen Thompson (HOU) OVER 0.5 Steals: 65%, EV -0.06 at -222
- Fred VanVleet (HOU) OVER 0.5 Steals: 64%, EV -0.06 at -216
- Tari Eason (HOU) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Cameron Johnson (DEN) OVER 0.5 Steals: 62%, EV -0.06 at -193
- DeMar DeRozan (DEN) UNDER 0.5 3-pointers made: 62%, EV -0.06 at -191
- Aaron Gordon (DEN) OVER 1.5 Assists: 62%, EV -0.06 at -191

## SAS at PHX (game 401909958)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dylan Harper (SAS) OVER 0.5 3-pointers made | -241 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 3-pointers made | -222 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -222 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

Combined probability 27.8%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dylan Harper (SAS) OVER 0.5 3-pointers made: 66%, EV -0.06 at -241
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -222
- Victor Wembanyama (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -222
- Harrison Barnes (SAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -216
- Keldon Johnson (SAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -213
- Jalen Green (PHX) OVER 0.5 Steals: 63%, EV -0.06 at -202
- Stephon Castle (SAS) OVER 0.5 Steals: 62%, EV -0.06 at -199
- Collin Gillespie (PHX) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177

## NOP at GSW (game 401909959)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -221 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Stephen Curry (GSW) UNDER 1.5 Steals | -209 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |
| De'Anthony Melton (GSW) UNDER 1.5 Steals | -193 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |

Combined probability 25.2%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -221
- Stephen Curry (GSW) UNDER 1.5 Steals: 63%, EV -0.06 at -209
- De'Anthony Melton (GSW) UNDER 1.5 Steals: 62%, EV -0.06 at -193
- De'Anthony Melton (GSW) UNDER 2.5 Assists: 61%, EV -0.06 at -189
- Saddiq Bey (NOP) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- Brandin Podziemski (GSW) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -178
- Brandon Williams (GSW) UNDER 2.5 Rebounds: 59%, EV -0.06 at -173
- Herbert Jones (NOP) OVER 1.5 Assists: 57%, EV -0.06 at -156
