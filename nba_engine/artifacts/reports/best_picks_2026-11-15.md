# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-15T16:08:16Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dyson Daniels (ATL) UNDER 0.5 3-pointers made | -274 (DraftKings via ESPN) | 0.7 | 69% | 69% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -233 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Dylan Harper (SAS) UNDER 1.5 3-pointers made | -227 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Zaccharie Risacher (DAL) UNDER 1.5 3-pointers made | -223 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

**Combined probability 19.2%; parlay pays 4.1x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Dyson Daniels (ATL) UNDER 0.5 3-pointers made (69%); Derrick Jones Jr. (LAC) UNDER 1.5 Assists (66%); Dylan Harper (SAS) UNDER 1.5 3-pointers made (65%). Combined probability 29.5%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Reed Sheppard (HOU) UNDER 3.5 Assists | +113 (DraftKings via ESPN) | 2.7 | 69% | 44% | +0.48 |
| Ivica Zubac (IND) UNDER 12.5 Points | -102 (DraftKings via ESPN) | 10.3 | 70% | 48% | +0.38 |

Combined probability 48.2%; parlay pays 4.2x; expected profit per 1 staked +1.03.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Reed Sheppard (HOU) UNDER 3.5 Assists | +113 (DraftKings via ESPN) | 2.7 | 69% | 44% | +0.48 |
| Ivica Zubac (IND) UNDER 12.5 Points | -102 (DraftKings via ESPN) | 10.3 | 70% | 48% | +0.38 |
| Keyonte George (UTA) OVER 20.5 Points | -108 (DraftKings via ESPN) | 21.8 | 68% | 49% | +0.31 |

Combined probability 32.8%; parlay pays 8.1x; expected profit per 1 staked +1.66.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Reed Sheppard (HOU) UNDER 3.5 Assists | +113 (DraftKings via ESPN) | 2.7 | 69% | 44% | +0.48 |
| Ivica Zubac (IND) UNDER 12.5 Points | -102 (DraftKings via ESPN) | 10.3 | 70% | 48% | +0.38 |
| Keyonte George (UTA) OVER 20.5 Points | -108 (DraftKings via ESPN) | 21.8 | 68% | 49% | +0.31 |
| Brayden Burries (MIL) UNDER 11.5 Points | -118 (DraftKings via ESPN) | 9.3 | 70% | 51% | +0.29 |

Combined probability 22.9%; parlay pays 15.0x; expected profit per 1 staked +2.43.

Top single picks by model edge:

- Reed Sheppard (HOU) UNDER 3.5 Assists: model 69% vs book 44%, EV +0.48 at +113 (projection 2.7)
- Ivica Zubac (IND) UNDER 12.5 Points: model 70% vs book 48%, EV +0.38 at -102 (projection 10.3)
- Reed Sheppard (HOU) UNDER 2.5 3-pointers made: model 66% vs book 47%, EV +0.32 at +100 (projection 1.9)
- Keyonte George (UTA) OVER 20.5 Points: model 68% vs book 49%, EV +0.31 at -108 (projection 21.8)
- Brayden Burries (MIL) UNDER 11.5 Points: model 70% vs book 51%, EV +0.29 at -118 (projection 9.3)
- Tyler Herro (MIL) UNDER 4.5 Assists: model 60% vs book 43%, EV +0.29 at +116 (projection 3.6)
- Alex Sarr (WAS) OVER 10.5 Points: model 65% vs book 48%, EV +0.27 at -105 (projection 13.4)
- Jayson Tatum (BOS) UNDER 27.5 Points: model 67% vs book 50%, EV +0.27 at -112 (projection 21.2)
- P.J. Washington (DAL) UNDER 1.5 3-pointers made: model 54% vs book 40%, EV +0.27 at +135 (projection 1.5)
- Keyonte George (UTA) OVER 5.5 Assists: model 64% vs book 48%, EV +0.25 at -105 (projection 5.8)
- Alperen Sengun (HOU) OVER 20.5 Points: model 63% vs book 48%, EV +0.24 at -104 (projection 23.3)
- Nate Ament (MIL) UNDER 8.5 Points: model 65% vs book 50%, EV +0.24 at -112 (projection 7.2)

## IND at PHI (game 401909985)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dean Wade (PHI) OVER 0.5 3-pointers made | -219 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made | -212 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Aaron Nesmith (IND) UNDER 2.5 3-pointers made | -186 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |

Combined probability 25.0%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dean Wade (PHI) OVER 0.5 3-pointers made: 64%, EV -0.06 at -219
- Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -212
- Aaron Nesmith (IND) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -186
- Andrew Nembhard (IND) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- Anfernee Simons (PHI) UNDER 2.5 Rebounds: 61%, EV -0.06 at -184
- Anfernee Simons (PHI) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- VJ Edgecombe (PHI) OVER 2.5 Assists: 59%, EV -0.06 at -170
- LeBron James (PHI) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -166

## LAL at PHX (game 401909986)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Green (PHX) UNDER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 1.6 | 61% | 61% | -0.06 |
| Dillon Brooks (PHX) OVER 1.5 Assists | -179 (DraftKings via ESPN) | 1.8 | 60% | 60% | -0.06 |
| Devin Booker (PHX) UNDER 3.5 Rebounds | -175 (DraftKings via ESPN) | 3.1 | 60% | 60% | -0.06 |

Combined probability 22.0%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jalen Green (PHX) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Dillon Brooks (PHX) OVER 1.5 Assists: 60%, EV -0.06 at -179
- Devin Booker (PHX) UNDER 3.5 Rebounds: 60%, EV -0.06 at -175
- Jalen Green (PHX) UNDER 3.5 Rebounds: 59%, EV -0.06 at -173
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Collin Gillespie (PHX) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -171
- Devin Booker (PHX) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Collin Gillespie (PHX) UNDER 3.5 Assists: 58%, EV -0.06 at -165

## CHA at LAC (game 401909987)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -233 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Gradey Dick (LAC) OVER 0.5 3-pointers made | -205 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |
| Naz Reid (CHA) OVER 1.5 Assists | -197 (DraftKings via ESPN) | 2.7 | 62% | 62% | -0.06 |

Combined probability 25.8%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 66%, EV -0.06 at -233
- Gradey Dick (LAC) OVER 0.5 3-pointers made: 63%, EV -0.06 at -205
- Naz Reid (CHA) OVER 1.5 Assists: 62%, EV -0.06 at -197
- Sion James (CHA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -195
- Rui Hachimura (LAC) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -194
- Keaton Wagler (LAC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Max Strus (LAC) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Max Strus (LAC) UNDER 2.5 Assists: 60%, EV -0.06 at -176

## SAS at UTA (game 401909988)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dylan Harper (SAS) UNDER 1.5 3-pointers made | -227 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -223 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Keyonte George (UTA) UNDER 2.5 3-pointers made | -191 (DraftKings via ESPN) | 2.3 | 62% | 62% | -0.06 |

Combined probability 26.0%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dylan Harper (SAS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -227
- De'Aaron Fox (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -223
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -197
- Keyonte George (UTA) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -191
- Julian Champagnie (SAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -180
- Josh Okogie (UTA) OVER 2.5 Rebounds: 58%, EV -0.06 at -165
- Julian Champagnie (SAS) OVER 3.5 Rebounds: 58%, EV -0.06 at -162
- Victor Wembanyama (SAS) OVER 2.5 Assists: 58%, EV -0.06 at -162

## DAL at BOS (game 401909989)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zaccharie Risacher (DAL) UNDER 1.5 3-pointers made | -223 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Derrick White (BOS) UNDER 2.5 3-pointers made | -185 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| Naji Marshall (DAL) OVER 0.5 3-pointers made | -181 (DraftKings via ESPN) | 0.9 | 60% | 60% | -0.06 |

Combined probability 23.9%; parlay pays 3.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Zaccharie Risacher (DAL) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -223
- Derrick White (BOS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- Naji Marshall (DAL) OVER 0.5 3-pointers made: 60%, EV -0.06 at -181
- P.J. Washington (DAL) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Cooper Flagg (DAL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -166
- Caleb Martin (DAL) UNDER 3.5 Rebounds: 58%, EV -0.06 at -165
- Naji Marshall (DAL) OVER 2.5 Assists: 58%, EV -0.06 at -163
- Paul George (BOS) OVER 2.5 3-pointers made: 58%, EV -0.06 at -162

## NYK at TOR (game 401909990)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| OG Anunoby (NYK) UNDER 2.5 3-pointers made | -196 (DraftKings via ESPN) | 2.1 | 62% | 62% | -0.06 |
| Mikal Bridges (NYK) OVER 0.5 3-pointers made | -192 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| Ja'Kobe Walter (TOR) UNDER 2.5 3-pointers made | -159 (DraftKings via ESPN) | 2.5 | 57% | 57% | -0.06 |

Combined probability 22.0%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -196
- Mikal Bridges (NYK) OVER 0.5 3-pointers made: 62%, EV -0.06 at -192
- Ja'Kobe Walter (TOR) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -159
- Jalen Brunson (NYK) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -154
- RJ Barrett (TOR) OVER 5.5 Rebounds: 57%, EV -0.06 at -154
- OG Anunoby (NYK) UNDER 5.5 Rebounds: 56%, EV -0.06 at -151
- RJ Barrett (TOR) UNDER 4.5 Assists: 56%, EV -0.06 at -151
- Jalen Brunson (NYK) OVER 5.5 Assists: 56%, EV -0.06 at -150

## HOU at WAS (game 401909991)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alex Sarr (WAS) OVER 0.5 3-pointers made | -221 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -191 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made | -188 (DraftKings via ESPN) | 2.2 | 61% | 61% | -0.06 |

Combined probability 24.4%; parlay pays 3.4x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Alex Sarr (WAS) OVER 0.5 3-pointers made: 65%, EV -0.06 at -221
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -188
- Kyshawn George (WAS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -187
- AJ Dybantsa (WAS) UNDER 2.5 Assists: 60%, EV -0.06 at -177
- Trae Young (WAS) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -173
- Tre Johnson (WAS) UNDER 2.5 Rebounds: 59%, EV -0.06 at -169
- Kevin Durant (HOU) OVER 3.5 Assists: 58%, EV -0.06 at -161

## ATL at MIL (game 401909992)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dyson Daniels (ATL) UNDER 0.5 3-pointers made | -274 (DraftKings via ESPN) | 0.7 | 69% | 69% | -0.06 |
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -174 (DraftKings via ESPN) | 1.0 | 60% | 60% | -0.06 |
| Aaron Wiggins (ATL) OVER 1.5 3-pointers made | -173 (DraftKings via ESPN) | 2.6 | 59% | 59% | -0.06 |

Combined probability 24.4%; parlay pays 3.4x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dyson Daniels (ATL) UNDER 0.5 3-pointers made: 69%, EV -0.06 at -274
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -174
- Aaron Wiggins (ATL) OVER 1.5 3-pointers made: 59%, EV -0.06 at -173
- Myles Turner (MIL) UNDER 2.5 Assists: 59%, EV -0.06 at -173
- Luguentz Dort (ATL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -169
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -168
- CJ McCollum (ATL) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -164
- Brayden Burries (MIL) UNDER 3.5 Assists: 58%, EV -0.06 at -161

## OKC at SAC (game 401909993)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made | -186 (DraftKings via ESPN) | 2.2 | 61% | 61% | -0.06 |
| De'Andre Hunter (SAC) UNDER 2.5 3-pointers made | -178 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |
| Jared McCain (OKC) UNDER 2.5 Assists | -162 (DraftKings via ESPN) | 2.2 | 58% | 58% | -0.06 |

Combined probability 21.2%; parlay pays 3.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -186
- De'Andre Hunter (SAC) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -178
- Shai Gilgeous-Alexander (OKC) OVER 3.5 Rebounds: 58%, EV -0.06 at -165
- Jared McCain (OKC) UNDER 2.5 Assists: 58%, EV -0.06 at -162
- Domantas Sabonis (SAC) OVER 4.5 Assists: 58%, EV -0.06 at -161
- Isaiah Hartenstein (OKC) UNDER 4.5 Assists: 58%, EV -0.06 at -159
- Darius Acuff Jr. (SAC) OVER 2.5 3-pointers made: 58%, EV -0.06 at -159
- De'Andre Hunter (SAC) UNDER 1.5 Assists: 56%, EV -0.06 at -152
