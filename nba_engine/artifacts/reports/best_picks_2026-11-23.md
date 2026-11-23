# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-23T20:56:10Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 1.5 Steals | -247 (DraftKings via ESPN) | 1.3 | 67% | 67% | -0.06 |
| Moussa Diabate (CHA) OVER 0.5 Blocks | -239 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Ziaire Williams (LAL) UNDER 1.5 3-pointers made | -227 (DraftKings via ESPN) | 1.5 | 65% | 65% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -221 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |

**Combined probability 18.6%; parlay pays 4.2x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Tyrese Maxey (PHI) UNDER 1.5 Steals (67%); Moussa Diabate (CHA) OVER 0.5 Blocks (66%); Ziaire Williams (LAL) UNDER 1.5 3-pointers made (65%). Combined probability 28.8%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikel Brown Jr. (BKN) OVER 2.5 Rebounds | +140 (DraftKings via ESPN) | 3.0 | 67% | 39% | +0.60 |
| Julian Champagnie (SAS) UNDER 13.5 Points | -126 (DraftKings via ESPN) | 10.3 | 75% | 53% | +0.34 |

Combined probability 49.7%; parlay pays 4.3x; expected profit per 1 staked +1.14.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikel Brown Jr. (BKN) OVER 2.5 Rebounds | +140 (DraftKings via ESPN) | 3.0 | 67% | 39% | +0.60 |
| Julian Champagnie (SAS) UNDER 13.5 Points | -126 (DraftKings via ESPN) | 10.3 | 75% | 53% | +0.34 |
| Pascal Siakam (IND) OVER 21.5 Points | -107 (DraftKings via ESPN) | 26.4 | 69% | 49% | +0.33 |

Combined probability 34.1%; parlay pays 8.3x; expected profit per 1 staked +1.84.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikel Brown Jr. (BKN) OVER 2.5 Rebounds | +140 (DraftKings via ESPN) | 3.0 | 67% | 39% | +0.60 |
| Julian Champagnie (SAS) UNDER 13.5 Points | -126 (DraftKings via ESPN) | 10.3 | 75% | 53% | +0.34 |
| Pascal Siakam (IND) OVER 21.5 Points | -107 (DraftKings via ESPN) | 26.4 | 69% | 49% | +0.33 |
| Tyrese Maxey (PHI) UNDER 25.5 Points | -119 (DraftKings via ESPN) | 18.7 | 72% | 51% | +0.32 |

Combined probability 24.5%; parlay pays 15.3x; expected profit per 1 staked +2.76.

Top single picks by model edge:

- Mikel Brown Jr. (BKN) OVER 2.5 Rebounds: model 67% vs book 39%, EV +0.60 at +140 (projection 3.0)
- Mikel Brown Jr. (BKN) UNDER 1.5 3-pointers made: model 66% vs book 41%, EV +0.51 at +129 (projection 1.0)
- Julian Champagnie (SAS) UNDER 13.5 Points: model 75% vs book 53%, EV +0.34 at -126 (projection 10.3)
- Julian Champagnie (SAS) UNDER 2.5 3-pointers made: model 59% vs book 41%, EV +0.33 at +127 (projection 2.3)
- Pascal Siakam (IND) OVER 21.5 Points: model 69% vs book 49%, EV +0.33 at -107 (projection 26.4)
- Tyrese Maxey (PHI) UNDER 25.5 Points: model 72% vs book 51%, EV +0.32 at -119 (projection 18.7)
- Shai Gilgeous-Alexander (OKC) OVER 5.5 Assists: model 63% vs book 44%, EV +0.32 at +111 (projection 5.8)
- Mikel Brown Jr. (BKN) UNDER 13.5 Points: model 71% vs book 51%, EV +0.31 at -119 (projection 9.2)
- Jrue Holiday (POR) OVER 4.5 Assists: model 59% vs book 43%, EV +0.30 at +120 (projection 5.2)
- Stephon Castle (SAS) UNDER 19.5 Points: model 69% vs book 50%, EV +0.30 at -113 (projection 16.7)
- James Harden (CLE) OVER 18.5 Points: model 67% vs book 49%, EV +0.29 at -108 (projection 19.9)
- Josh Giddey (CHI) OVER 9.5 Assists: model 61% vs book 45%, EV +0.28 at +109 (projection 10.7)

## MEM at CHA (game 401910036)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Moussa Diabate (CHA) OVER 0.5 Blocks | -239 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Cedric Coward (MEM) OVER 1.5 3-pointers made | -180 (DraftKings via ESPN) | 2.5 | 60% | 60% | -0.06 |
| Coby White (CHA) OVER 1.5 3-pointers made | -174 (DraftKings via ESPN) | 2.1 | 59% | 59% | -0.06 |

Combined probability 23.7%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Moussa Diabate (CHA) OVER 0.5 Blocks: 66%, EV -0.06 at -239
- Cedric Coward (MEM) OVER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Cedric Coward (MEM) OVER 2.5 Assists: 60%, EV -0.06 at -174
- Coby White (CHA) OVER 1.5 3-pointers made: 59%, EV -0.06 at -174
- Moussa Diabate (CHA) OVER 1.5 Assists: 59%, EV -0.06 at -174
- Cam Spencer (MEM) UNDER 3.5 Rebounds: 59%, EV -0.06 at -170
- Naz Reid (CHA) OVER 0.5 Steals: 59%, EV -0.06 at -168
- Sion James (CHA) OVER 3.5 Rebounds: 59%, EV -0.06 at -166

## POR at PHI (game 401910037)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 1.5 Steals | -247 (DraftKings via ESPN) | 1.3 | 67% | 67% | -0.06 |
| Joel Embiid (PHI) UNDER 1.5 Blocks | -240 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Sidy Cissoko (POR) UNDER 1.5 3-pointers made | -232 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |

Combined probability 29.1%; parlay pays 2.8x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Tyrese Maxey (PHI) UNDER 1.5 Steals: 67%, EV -0.06 at -247
- Joel Embiid (PHI) UNDER 1.5 Blocks: 66%, EV -0.06 at -240
- Joel Embiid (PHI) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -235
- Sidy Cissoko (POR) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -232
- Toumani Camara (POR) UNDER 1.5 Steals: 65%, EV -0.06 at -222
- Jrue Holiday (POR) OVER 0.5 Steals: 63%, EV -0.06 at -205
- Scoot Henderson (POR) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 61%, EV -0.06 at -187

## OKC at IND (game 401910038)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ajay Mitchell (OKC) OVER 0.5 3-pointers made | -206 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Jared McCain (OKC) UNDER 2.5 Assists | -194 (DraftKings via ESPN) | 2.3 | 62% | 62% | -0.06 |
| Kelly Oubre Jr. (IND) UNDER 4.5 Rebounds | -160 (DraftKings via ESPN) | 4.0 | 58% | 58% | -0.06 |

Combined probability 22.5%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ajay Mitchell (OKC) OVER 0.5 3-pointers made: 63%, EV -0.06 at -206
- Jared McCain (OKC) UNDER 2.5 Assists: 62%, EV -0.06 at -194
- Kelly Oubre Jr. (IND) UNDER 4.5 Rebounds: 58%, EV -0.06 at -160
- Shai Gilgeous-Alexander (OKC) OVER 3.5 Rebounds: 57%, EV -0.06 at -157
- Isaiah Hartenstein (OKC) OVER 3.5 Assists: 57%, EV -0.06 at -155
- Shai Gilgeous-Alexander (OKC) OVER 1.5 3-pointers made: 57%, EV -0.06 at -154
- Jared McCain (OKC) UNDER 3.5 Rebounds: 56%, EV -0.06 at -149
- Pascal Siakam (IND) OVER 5.5 Rebounds: 56%, EV -0.06 at -146

## MIL at TOR (game 401910039)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ja'Kobe Walter (TOR) UNDER 1.5 Steals | -195 (DraftKings via ESPN) | 1.5 | 62% | 62% | -0.06 |
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -192 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Kyle Kuzma (MIL) UNDER 2.5 Assists | -184 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |

Combined probability 23.2%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 62%, EV -0.06 at -195
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Kyle Kuzma (MIL) UNDER 2.5 Assists: 61%, EV -0.06 at -184
- Ja'Kobe Walter (TOR) UNDER 2.5 Assists: 61%, EV -0.06 at -184
- Jakob Poeltl (TOR) OVER 1.5 Assists: 59%, EV -0.06 at -169
- Tyler Herro (MIL) UNDER 4.5 Assists: 58%, EV -0.06 at -165
- Ja'Kobe Walter (TOR) OVER 3.5 Rebounds: 57%, EV -0.06 at -157
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -157

## BKN at MIN (game 401910040)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Terrence Shannon Jr. (MIN) UNDER 1.5 3-pointers made | -203 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |
| Rudy Gobert (MIN) UNDER 1.5 Blocks | -195 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| Danny Wolf (BKN) UNDER 1.5 3-pointers made | -191 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |

Combined probability 23.9%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Terrence Shannon Jr. (MIN) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Rudy Gobert (MIN) UNDER 1.5 Blocks: 62%, EV -0.06 at -195
- Danny Wolf (BKN) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Mikel Brown Jr. (BKN) UNDER 2.5 Rebounds: 61%, EV -0.06 at -186
- Jaden McDaniels (MIN) UNDER 1.5 Steals: 60%, EV -0.07 at -181
- Michael Porter Jr. (BKN) OVER 1.5 Assists: 59%, EV -0.06 at -173
- Mikel Brown Jr. (BKN) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Ayo Dosunmu (MIN) OVER 1.5 3-pointers made: 58%, EV -0.06 at -164

## CLE at CHI (game 401910041)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tyrese Proctor (CLE) OVER 2.5 Rebounds | -169 (DraftKings via ESPN) | 3.7 | 59% | 59% | -0.06 |
| Isaac Okoro (CHI) OVER 2.5 Rebounds | -166 (DraftKings via ESPN) | 3.3 | 58% | 58% | -0.06 |
| Donovan Mitchell (CLE) OVER 4.5 Assists | -161 (DraftKings via ESPN) | 5.1 | 58% | 58% | -0.06 |

Combined probability 19.9%; parlay pays 4.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Tyrese Proctor (CLE) OVER 2.5 Rebounds: 59%, EV -0.06 at -169
- Isaac Okoro (CHI) OVER 2.5 Rebounds: 58%, EV -0.06 at -166
- Donovan Mitchell (CLE) OVER 4.5 Assists: 58%, EV -0.06 at -161
- Isaac Okoro (CHI) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -155
- Tyrese Proctor (CLE) UNDER 1.5 3-pointers made: 56%, EV -0.06 at -147
- Donovan Mitchell (CLE) OVER 2.5 3-pointers made: 56%, EV -0.06 at -147
- Josh Giddey (CHI) UNDER 7.5 Rebounds: 55%, EV -0.06 at -144
- Josh Giddey (CHI) UNDER 9.5 Assists: 55%, EV -0.06 at -143

## PHX at NOP (game 401910042)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -221 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Devin Booker (PHX) OVER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| Saddiq Bey (NOP) UNDER 2.5 3-pointers made | -177 (DraftKings via ESPN) | 2.1 | 60% | 60% | -0.06 |

Combined probability 23.8%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -221
- Devin Booker (PHX) OVER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Saddiq Bey (NOP) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -177
- Jalen Green (PHX) OVER 2.5 Assists: 60%, EV -0.06 at -176
- Derik Queen (NOP) UNDER 2.5 Assists: 59%, EV -0.06 at -173
- Dillon Brooks (PHX) OVER 1.5 Assists: 58%, EV -0.06 at -165
- Herbert Jones (NOP) OVER 2.5 Rebounds: 58%, EV -0.06 at -165
- Saddiq Bey (NOP) UNDER 2.5 Assists: 58%, EV -0.06 at -162

## LAC at HOU (game 401910043)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Keaton Wagler (LAC) OVER 0.5 3-pointers made | -205 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |
| Derrick Jones Jr. (LAC) OVER 0.5 3-pointers made | -191 (DraftKings via ESPN) | 1.0 | 62% | 62% | -0.06 |
| Max Strus (LAC) UNDER 2.5 3-pointers made | -188 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |

Combined probability 23.7%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Keaton Wagler (LAC) OVER 0.5 3-pointers made: 63%, EV -0.06 at -205
- Derrick Jones Jr. (LAC) OVER 0.5 3-pointers made: 62%, EV -0.06 at -191
- Max Strus (LAC) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -188
- Jabari Smith Jr. (HOU) OVER 1.5 3-pointers made: 58%, EV -0.06 at -162
- Amen Thompson (HOU) OVER 2.5 Assists: 58%, EV -0.06 at -161
- Fred VanVleet (HOU) OVER 2.5 Rebounds: 57%, EV -0.06 at -156
- Fred VanVleet (HOU) UNDER 5.5 Assists: 56%, EV -0.06 at -152
- Rui Hachimura (LAC) OVER 1.5 3-pointers made: 56%, EV -0.06 at -150

## UTA at LAL (game 401910044)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ziaire Williams (LAL) UNDER 1.5 3-pointers made | -227 (DraftKings via ESPN) | 1.5 | 65% | 65% | -0.06 |
| Collin Sexton (LAL) UNDER 1.5 3-pointers made | -219 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |
| Quentin Grimes (LAL) UNDER 2.5 3-pointers made | -194 (DraftKings via ESPN) | 1.8 | 62% | 62% | -0.06 |

Combined probability 26.0%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Ziaire Williams (LAL) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -227
- Collin Sexton (LAL) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -219
- Quentin Grimes (LAL) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -194
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Ace Bailey (UTA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -186
- Walker Kessler (LAL) OVER 1.5 Blocks: 60%, EV -0.06 at -179
- Walker Kessler (LAL) OVER 0.5 Steals: 60%, EV -0.06 at -178
- Keyonte George (UTA) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -164

## SAS at SAC (game 401910045)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -211 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |
| Stephon Castle (SAS) UNDER 2.5 3-pointers made | -192 (DraftKings via ESPN) | 1.8 | 62% | 62% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 3-pointers made | -185 (DraftKings via ESPN) | 1.2 | 61% | 61% | -0.06 |

Combined probability 23.8%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Victor Wembanyama (SAS) UNDER 1.5 Steals: 64%, EV -0.06 at -211
- Stephon Castle (SAS) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -192
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Victor Wembanyama (SAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181
- Victor Wembanyama (SAS) OVER 2.5 Assists: 60%, EV -0.06 at -180
- De'Andre Hunter (SAC) OVER 1.5 3-pointers made: 59%, EV -0.06 at -169
- Julian Champagnie (SAS) OVER 2.5 3-pointers made: 59%, EV -0.06 at -168
- Devin Vassell (SAS) OVER 2.5 Assists: 58%, EV -0.06 at -162
