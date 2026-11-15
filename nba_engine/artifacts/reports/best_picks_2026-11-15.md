# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-15T19:33:51Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dyson Daniels (ATL) UNDER 0.5 3-pointers made | -285 (DraftKings via ESPN) | 0.7 | 70% | 70% | -0.06 |
| Jalen Green (PHX) OVER 0.5 Steals | -239 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Alex Sarr (WAS) OVER 0.5 3-pointers made | -236 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -234 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |

**Combined probability 19.9%; parlay pays 3.9x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Dyson Daniels (ATL) UNDER 0.5 3-pointers made (70%); Jalen Green (PHX) OVER 0.5 Steals (66%); Alex Sarr (WAS) OVER 0.5 3-pointers made (66%). Combined probability 30.4%; parlay pays 2.7x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Reed Sheppard (HOU) UNDER 3.5 Assists | +109 (DraftKings via ESPN) | 2.7 | 70% | 45% | +0.46 |
| Brayden Burries (MIL) UNDER 2.5 Assists | +120 (DraftKings via ESPN) | 2.2 | 62% | 43% | +0.37 |

Combined probability 43.4%; parlay pays 4.6x; expected profit per 1 staked +1.00.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Reed Sheppard (HOU) UNDER 3.5 Assists | +109 (DraftKings via ESPN) | 2.7 | 70% | 45% | +0.46 |
| Brayden Burries (MIL) UNDER 2.5 Assists | +120 (DraftKings via ESPN) | 2.2 | 62% | 43% | +0.37 |
| Ace Bailey (UTA) OVER 14.5 Points | -102 (DraftKings via ESPN) | 18.6 | 69% | 48% | +0.36 |

Combined probability 29.8%; parlay pays 9.1x; expected profit per 1 staked +1.72.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Reed Sheppard (HOU) UNDER 3.5 Assists | +109 (DraftKings via ESPN) | 2.7 | 70% | 45% | +0.46 |
| Brayden Burries (MIL) UNDER 2.5 Assists | +120 (DraftKings via ESPN) | 2.2 | 62% | 43% | +0.37 |
| Ace Bailey (UTA) OVER 14.5 Points | -102 (DraftKings via ESPN) | 18.6 | 69% | 48% | +0.36 |
| Cooper Flagg (DAL) UNDER 5.5 Assists | -110 (DraftKings via ESPN) | 4.5 | 67% | 49% | +0.27 |

Combined probability 19.9%; parlay pays 17.4x; expected profit per 1 staked +2.46.

Top single picks by model edge:

- Reed Sheppard (HOU) UNDER 3.5 Assists: model 70% vs book 45%, EV +0.46 at +109 (projection 2.7)
- Brayden Burries (MIL) UNDER 2.5 Assists: model 62% vs book 43%, EV +0.37 at +120 (projection 2.2)
- Reed Sheppard (HOU) UNDER 2.5 3-pointers made: model 67% vs book 46%, EV +0.37 at +103 (projection 1.9)
- Ace Bailey (UTA) OVER 14.5 Points: model 69% vs book 48%, EV +0.36 at -102 (projection 18.6)
- Brayden Burries (MIL) UNDER 11.5 Points: model 70% vs book 49%, EV +0.34 at -108 (projection 9.3)
- Keyonte George (UTA) OVER 19.5 Points: model 72% vs book 52%, EV +0.31 at -123 (projection 21.8)
- Tyler Herro (MIL) UNDER 4.5 Assists: model 60% vs book 44%, EV +0.28 at +114 (projection 3.6)
- Cooper Flagg (DAL) UNDER 5.5 Assists: model 67% vs book 49%, EV +0.27 at -110 (projection 4.5)
- De'Andre Hunter (SAC) OVER 4.5 Rebounds: model 59% vs book 44%, EV +0.25 at +113 (projection 4.4)
- Alex Sarr (WAS) OVER 10.5 Points: model 65% vs book 50%, EV +0.24 at -111 (projection 13.4)
- Nate Ament (MIL) UNDER 8.5 Points: model 65% vs book 50%, EV +0.23 at -113 (projection 7.2)
- Dylan Harper (SAS) UNDER 17.5 Points: model 66% vs book 51%, EV +0.23 at -117 (projection 15.1)

## IND at PHI (game 401909985)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dean Wade (PHI) OVER 0.5 3-pointers made | -219 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made | -209 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |
| Aaron Nesmith (IND) UNDER 2.5 3-pointers made | -186 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |

Combined probability 24.9%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dean Wade (PHI) OVER 0.5 3-pointers made: 64%, EV -0.06 at -219
- Kentavious Caldwell-Pope (PHI) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -209
- Aaron Nesmith (IND) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -186
- Anfernee Simons (PHI) OVER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Ivica Zubac (IND) OVER 1.5 Assists: 60%, EV -0.06 at -182
- Anfernee Simons (PHI) UNDER 2.5 Rebounds: 59%, EV -0.06 at -168
- LeBron James (PHI) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Obi Toppin (IND) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -159

## LAL at PHX (game 401909986)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Green (PHX) OVER 0.5 Steals | -239 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Dillon Brooks (PHX) OVER 0.5 Steals | -228 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Devin Booker (PHX) OVER 0.5 Steals | -210 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |

Combined probability 27.3%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jalen Green (PHX) OVER 0.5 Steals: 66%, EV -0.06 at -239
- Dillon Brooks (PHX) OVER 0.5 Steals: 65%, EV -0.06 at -228
- Devin Booker (PHX) OVER 0.5 Steals: 63%, EV -0.06 at -210
- Miles Bridges (PHX) OVER 0.5 Steals: 61%, EV -0.06 at -190
- Jalen Green (PHX) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Devin Booker (PHX) UNDER 3.5 Rebounds: 60%, EV -0.06 at -174
- Jalen Green (PHX) UNDER 3.5 Rebounds: 59%, EV -0.06 at -173
- Devin Booker (PHX) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171

## CHA at LAC (game 401909987)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Sion James (CHA) UNDER 1.5 3-pointers made | -198 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -197 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Rui Hachimura (LAC) UNDER 1.5 Assists | -192 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |

Combined probability 23.9%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Sion James (CHA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 62%, EV -0.06 at -197
- Rui Hachimura (LAC) UNDER 1.5 Assists: 62%, EV -0.06 at -192
- Naz Reid (CHA) OVER 1.5 Assists: 61%, EV -0.06 at -190
- Rui Hachimura (LAC) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Keaton Wagler (LAC) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -182
- Naz Reid (CHA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -182
- Gradey Dick (LAC) OVER 0.5 3-pointers made: 60%, EV -0.06 at -179

## SAS at UTA (game 401909988)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -234 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Dylan Harper (SAS) UNDER 1.5 3-pointers made | -218 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |
| Keyonte George (UTA) OVER 1.5 3-pointers made | -191 (DraftKings via ESPN) | 2.3 | 62% | 62% | -0.06 |

Combined probability 26.0%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- De'Aaron Fox (SAS) UNDER 1.5 Steals: 66%, EV -0.06 at -234
- Dylan Harper (SAS) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -218
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Keyonte George (UTA) OVER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Josh Okogie (UTA) OVER 2.5 Rebounds: 58%, EV -0.06 at -164
- Darryn Peterson (UTA) UNDER 4.5 Rebounds: 58%, EV -0.06 at -162
- Dylan Harper (SAS) OVER 4.5 Rebounds: 57%, EV -0.06 at -158
- Keldon Johnson (SAS) OVER 4.5 Rebounds: 57%, EV -0.06 at -155

## DAL at BOS (game 401909989)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zaccharie Risacher (DAL) UNDER 1.5 3-pointers made | -218 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Derrick White (BOS) UNDER 2.5 3-pointers made | -190 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| Payton Pritchard (BOS) OVER 2.5 Rebounds | -172 (DraftKings via ESPN) | 3.3 | 59% | 59% | -0.06 |

Combined probability 23.4%; parlay pays 3.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Zaccharie Risacher (DAL) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -218
- Derrick White (BOS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -190
- Payton Pritchard (BOS) OVER 2.5 Rebounds: 59%, EV -0.06 at -172
- Naji Marshall (DAL) OVER 0.5 3-pointers made: 59%, EV -0.06 at -170
- Cooper Flagg (DAL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -170
- Kyrie Irving (DAL) OVER 2.5 3-pointers made: 59%, EV -0.06 at -166
- Payton Pritchard (BOS) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -163
- Paul George (BOS) OVER 2.5 3-pointers made: 58%, EV -0.06 at -162

## NYK at TOR (game 401909990)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) OVER 0.5 3-pointers made | -192 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| OG Anunoby (NYK) UNDER 2.5 3-pointers made | -186 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |
| Ja'Kobe Walter (TOR) UNDER 2.5 3-pointers made | -166 (DraftKings via ESPN) | 2.5 | 59% | 59% | -0.06 |

Combined probability 22.0%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Mikal Bridges (NYK) OVER 0.5 3-pointers made: 62%, EV -0.06 at -192
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -186
- Ja'Kobe Walter (TOR) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -166
- OG Anunoby (NYK) UNDER 5.5 Rebounds: 57%, EV -0.06 at -157
- Jalen Brunson (NYK) OVER 5.5 Assists: 57%, EV -0.06 at -155
- RJ Barrett (TOR) UNDER 4.5 Assists: 56%, EV -0.06 at -151
- Karl-Anthony Towns (NYK) UNDER 3.5 Assists: 56%, EV -0.06 at -149
- Jalen Brunson (NYK) UNDER 2.5 3-pointers made: 56%, EV -0.06 at -149

## HOU at WAS (game 401909991)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alex Sarr (WAS) OVER 0.5 3-pointers made | -236 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 1.1 | 61% | 61% | -0.06 |
| Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made | -182 (DraftKings via ESPN) | 2.1 | 60% | 60% | -0.06 |

Combined probability 24.5%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Alex Sarr (WAS) OVER 0.5 3-pointers made: 66%, EV -0.06 at -236
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -182
- Kyshawn George (WAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -182
- Trae Young (WAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181
- AJ Dybantsa (WAS) UNDER 2.5 Assists: 60%, EV -0.06 at -177
- Tre Johnson (WAS) UNDER 2.5 Rebounds: 60%, EV -0.06 at -176
- Tari Eason (HOU) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -164

## ATL at MIL (game 401909992)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dyson Daniels (ATL) UNDER 0.5 3-pointers made | -285 (DraftKings via ESPN) | 0.7 | 70% | 70% | -0.06 |
| Myles Turner (MIL) OVER 1.5 Assists | -184 (DraftKings via ESPN) | 1.6 | 61% | 61% | -0.06 |
| Aaron Wiggins (ATL) OVER 1.5 3-pointers made | -178 (DraftKings via ESPN) | 2.6 | 60% | 60% | -0.06 |

Combined probability 25.4%; parlay pays 3.3x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dyson Daniels (ATL) UNDER 0.5 3-pointers made: 70%, EV -0.06 at -285
- Myles Turner (MIL) OVER 1.5 Assists: 61%, EV -0.06 at -184
- Aaron Wiggins (ATL) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -174
- CJ McCollum (ATL) UNDER 3.5 Rebounds: 59%, EV -0.06 at -171
- CJ McCollum (ATL) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -164
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -162
- Brayden Burries (MIL) OVER 2.5 Assists: 57%, EV -0.06 at -159

## OKC at SAC (game 401909993)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| De'Andre Hunter (SAC) UNDER 2.5 3-pointers made | -176 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |
| Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made | -175 (DraftKings via ESPN) | 2.2 | 60% | 60% | -0.06 |
| Isaiah Hartenstein (OKC) UNDER 4.5 Assists | -165 (DraftKings via ESPN) | 4.3 | 58% | 58% | -0.06 |

Combined probability 20.8%; parlay pays 4.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- De'Andre Hunter (SAC) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -176
- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Shai Gilgeous-Alexander (OKC) OVER 3.5 Rebounds: 58%, EV -0.06 at -165
- Isaiah Hartenstein (OKC) UNDER 4.5 Assists: 58%, EV -0.06 at -165
- Darius Acuff Jr. (SAC) OVER 2.5 3-pointers made: 58%, EV -0.06 at -161
- Jared McCain (OKC) UNDER 2.5 Assists: 57%, EV -0.06 at -156
- De'Andre Hunter (SAC) UNDER 1.5 Assists: 56%, EV -0.06 at -152
- Zach LaVine (SAC) UNDER 3.5 Rebounds: 56%, EV -0.06 at -149
