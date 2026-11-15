# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-15T20:38:57Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dyson Daniels (ATL) UNDER 0.5 3-pointers made | -275 (DraftKings via ESPN) | 0.7 | 69% | 69% | -0.06 |
| Alex Sarr (WAS) OVER 0.5 3-pointers made | -234 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Dylan Harper (SAS) UNDER 1.5 3-pointers made | -229 (DraftKings via ESPN) | 1.5 | 65% | 65% | -0.06 |
| Dillon Brooks (PHX) OVER 0.5 Steals | -228 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

**Combined probability 19.4%; parlay pays 4.0x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Dyson Daniels (ATL) UNDER 0.5 3-pointers made (69%); Alex Sarr (WAS) OVER 0.5 3-pointers made (66%); Dylan Harper (SAS) UNDER 1.5 3-pointers made (65%). Combined probability 29.7%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Reed Sheppard (HOU) UNDER 3.5 Assists | +105 (DraftKings via ESPN) | 2.7 | 70% | 46% | +0.43 |
| Brayden Burries (MIL) UNDER 2.5 Assists | +118 (DraftKings via ESPN) | 2.2 | 62% | 43% | +0.36 |

Combined probability 43.4%; parlay pays 4.5x; expected profit per 1 staked +0.94.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Reed Sheppard (HOU) UNDER 3.5 Assists | +105 (DraftKings via ESPN) | 2.7 | 70% | 46% | +0.43 |
| Brayden Burries (MIL) UNDER 2.5 Assists | +118 (DraftKings via ESPN) | 2.2 | 62% | 43% | +0.36 |
| Keldon Johnson (SAS) OVER 10.5 Points | +101 (DraftKings via ESPN) | 13.8 | 66% | 47% | +0.33 |

Combined probability 28.7%; parlay pays 9.0x; expected profit per 1 staked +1.58.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Reed Sheppard (HOU) UNDER 3.5 Assists | +105 (DraftKings via ESPN) | 2.7 | 70% | 46% | +0.43 |
| Brayden Burries (MIL) UNDER 2.5 Assists | +118 (DraftKings via ESPN) | 2.2 | 62% | 43% | +0.36 |
| Keldon Johnson (SAS) OVER 10.5 Points | +101 (DraftKings via ESPN) | 13.8 | 66% | 47% | +0.33 |
| Daniel Gafford (DAL) UNDER 7.5 Points | +110 (DraftKings via ESPN) | 6.7 | 63% | 45% | +0.32 |

Combined probability 18.0%; parlay pays 18.9x; expected profit per 1 staked +2.40.

Top single picks by model edge:

- Reed Sheppard (HOU) UNDER 3.5 Assists: model 70% vs book 46%, EV +0.43 at +105 (projection 2.7)
- Brayden Burries (MIL) UNDER 2.5 Assists: model 62% vs book 43%, EV +0.36 at +118 (projection 2.2)
- Brayden Burries (MIL) UNDER 11.5 Points: model 70% vs book 49%, EV +0.34 at -108 (projection 9.3)
- Reed Sheppard (HOU) UNDER 2.5 3-pointers made: model 67% vs book 47%, EV +0.33 at -102 (projection 1.9)
- Keldon Johnson (SAS) OVER 10.5 Points: model 66% vs book 47%, EV +0.33 at +101 (projection 13.8)
- Keyonte George (UTA) OVER 20.5 Points: model 67% vs book 48%, EV +0.32 at -103 (projection 22.1)
- Daniel Gafford (DAL) UNDER 7.5 Points: model 63% vs book 45%, EV +0.32 at +110 (projection 6.7)
- Ace Bailey (UTA) OVER 14.5 Points: model 68% vs book 49%, EV +0.31 at -109 (projection 18.7)
- Tyler Herro (MIL) UNDER 4.5 Assists: model 60% vs book 44%, EV +0.28 at +114 (projection 3.6)
- De'Andre Hunter (SAC) OVER 4.5 Rebounds: model 59% vs book 44%, EV +0.25 at +113 (projection 4.4)
- Sandro Mamukelashvili (LAL) OVER 1.5 3-pointers made: model 52% vs book 40%, EV +0.24 at +137 (projection 1.7)
- Nate Ament (MIL) UNDER 8.5 Points: model 65% vs book 50%, EV +0.23 at -113 (projection 7.2)

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
| Dillon Brooks (PHX) OVER 0.5 Steals | -228 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Devin Booker (PHX) OVER 0.5 Steals | -210 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |
| Miles Bridges (PHX) OVER 0.5 Steals | -197 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |

Combined probability 25.7%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Dillon Brooks (PHX) OVER 0.5 Steals: 65%, EV -0.06 at -228
- Devin Booker (PHX) OVER 0.5 Steals: 63%, EV -0.06 at -210
- Miles Bridges (PHX) OVER 0.5 Steals: 62%, EV -0.06 at -197
- Jalen Green (PHX) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -195
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Jalen Green (PHX) UNDER 3.5 Rebounds: 60%, EV -0.06 at -174
- Devin Booker (PHX) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Devin Booker (PHX) UNDER 3.5 Rebounds: 59%, EV -0.06 at -168

## CHA at LAC (game 401909987)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -219 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Sion James (CHA) UNDER 1.5 3-pointers made | -197 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| Rui Hachimura (LAC) OVER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 1.5 | 61% | 61% | -0.06 |

Combined probability 24.6%; parlay pays 3.4x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 64%, EV -0.06 at -219
- Sion James (CHA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -197
- Rui Hachimura (LAC) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Naz Reid (CHA) OVER 1.5 Assists: 61%, EV -0.06 at -190
- Keaton Wagler (LAC) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -182
- Gradey Dick (LAC) OVER 0.5 3-pointers made: 60%, EV -0.06 at -181
- Naz Reid (CHA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Brook Lopez (LAC) UNDER 1.5 Assists: 59%, EV -0.06 at -173

## SAS at UTA (game 401909988)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dylan Harper (SAS) UNDER 1.5 3-pointers made | -229 (DraftKings via ESPN) | 1.5 | 65% | 65% | -0.06 |
| Keyonte George (UTA) OVER 1.5 3-pointers made | -187 (DraftKings via ESPN) | 2.3 | 61% | 61% | -0.06 |
| Josh Okogie (UTA) OVER 2.5 Rebounds | -168 (DraftKings via ESPN) | 3.0 | 59% | 59% | -0.06 |

Combined probability 23.4%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Dylan Harper (SAS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -229
- Keyonte George (UTA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Josh Okogie (UTA) OVER 2.5 Rebounds: 59%, EV -0.06 at -168
- Darryn Peterson (UTA) UNDER 4.5 Rebounds: 58%, EV -0.06 at -163
- Victor Wembanyama (SAS) OVER 2.5 Assists: 57%, EV -0.06 at -154
- Darryn Peterson (UTA) OVER 3.5 Assists: 57%, EV -0.06 at -153
- Darryn Peterson (UTA) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -153
- Keyonte George (UTA) OVER 3.5 Rebounds: 56%, EV -0.06 at -151

## DAL at BOS (game 401909989)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Zaccharie Risacher (DAL) UNDER 1.5 3-pointers made | -214 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Derrick White (BOS) UNDER 2.5 3-pointers made | -182 (DraftKings via ESPN) | 2.0 | 60% | 60% | -0.06 |
| Naji Marshall (DAL) OVER 0.5 3-pointers made | -173 (DraftKings via ESPN) | 0.9 | 59% | 59% | -0.06 |

Combined probability 23.0%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Zaccharie Risacher (DAL) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -214
- Derrick White (BOS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -182
- Naji Marshall (DAL) OVER 0.5 3-pointers made: 59%, EV -0.06 at -173
- Cooper Flagg (DAL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -170
- P.J. Washington (DAL) OVER 1.5 3-pointers made: 59%, EV -0.06 at -168
- Paul George (BOS) OVER 2.5 3-pointers made: 58%, EV -0.06 at -162
- Payton Pritchard (BOS) UNDER 3.5 Rebounds: 57%, EV -0.06 at -154
- Payton Pritchard (BOS) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -154

## NYK at TOR (game 401909990)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) OVER 0.5 3-pointers made | -192 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| OG Anunoby (NYK) UNDER 2.5 3-pointers made | -186 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |
| Ja'Kobe Walter (TOR) UNDER 2.5 3-pointers made | -158 (DraftKings via ESPN) | 2.5 | 57% | 57% | -0.06 |

Combined probability 21.6%; parlay pays 3.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Mikal Bridges (NYK) OVER 0.5 3-pointers made: 62%, EV -0.06 at -192
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -186
- Ja'Kobe Walter (TOR) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -158
- Karl-Anthony Towns (NYK) UNDER 3.5 Assists: 57%, EV -0.06 at -157
- Jalen Brunson (NYK) OVER 5.5 Assists: 57%, EV -0.06 at -155
- OG Anunoby (NYK) OVER 4.5 Rebounds: 57%, EV -0.06 at -153
- RJ Barrett (TOR) UNDER 4.5 Assists: 56%, EV -0.06 at -151
- Jalen Brunson (NYK) UNDER 2.5 3-pointers made: 56%, EV -0.06 at -149

## HOU at WAS (game 401909991)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alex Sarr (WAS) OVER 0.5 3-pointers made | -234 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 1.1 | 61% | 61% | -0.06 |
| Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made | -182 (DraftKings via ESPN) | 2.1 | 60% | 60% | -0.06 |

Combined probability 24.4%; parlay pays 3.4x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Alex Sarr (WAS) OVER 0.5 3-pointers made: 66%, EV -0.06 at -234
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -182
- Kyshawn George (WAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -182
- Trae Young (WAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181
- AJ Dybantsa (WAS) UNDER 2.5 Assists: 60%, EV -0.06 at -177
- Tre Johnson (WAS) UNDER 2.5 Rebounds: 59%, EV -0.06 at -174
- Tari Eason (HOU) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -164

## ATL at MIL (game 401909992)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dyson Daniels (ATL) UNDER 0.5 3-pointers made | -275 (DraftKings via ESPN) | 0.7 | 69% | 69% | -0.06 |
| Aaron Wiggins (ATL) OVER 1.5 3-pointers made | -185 (DraftKings via ESPN) | 2.6 | 61% | 61% | -0.06 |
| Myles Turner (MIL) OVER 1.5 Assists | -184 (DraftKings via ESPN) | 1.6 | 61% | 61% | -0.06 |

Combined probability 25.5%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Dyson Daniels (ATL) UNDER 0.5 3-pointers made: 69%, EV -0.06 at -275
- Aaron Wiggins (ATL) OVER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Myles Turner (MIL) OVER 1.5 Assists: 61%, EV -0.06 at -184
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -174
- CJ McCollum (ATL) OVER 2.5 Rebounds: 59%, EV -0.06 at -171
- CJ McCollum (ATL) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -164
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -162
- Nickeil Alexander-Walker (ATL) OVER 2.5 Assists: 58%, EV -0.06 at -160

## OKC at SAC (game 401909993)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made | -175 (DraftKings via ESPN) | 2.2 | 60% | 60% | -0.06 |
| De'Andre Hunter (SAC) UNDER 2.5 3-pointers made | -167 (DraftKings via ESPN) | 1.9 | 59% | 59% | -0.06 |
| Isaiah Hartenstein (OKC) UNDER 4.5 Assists | -165 (DraftKings via ESPN) | 4.3 | 58% | 58% | -0.06 |

Combined probability 20.4%; parlay pays 4.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- De'Andre Hunter (SAC) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -167
- Isaiah Hartenstein (OKC) UNDER 4.5 Assists: 58%, EV -0.06 at -165
- Shai Gilgeous-Alexander (OKC) OVER 3.5 Rebounds: 58%, EV -0.06 at -163
- De'Andre Hunter (SAC) UNDER 1.5 Assists: 57%, EV -0.06 at -157
- Jared McCain (OKC) UNDER 2.5 Assists: 57%, EV -0.06 at -156
- Darius Acuff Jr. (SAC) OVER 2.5 3-pointers made: 57%, EV -0.06 at -153
- Zach LaVine (SAC) UNDER 3.5 Rebounds: 56%, EV -0.06 at -149
