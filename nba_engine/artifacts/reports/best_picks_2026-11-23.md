# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-24T01:30:08Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) UNDER 1.5 Steals | -244 (DraftKings via ESPN) | 0.9 | 67% | 67% | -0.06 |
| Moussa Diabate (CHA) OVER 0.5 Blocks | -239 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Sidy Cissoko (POR) OVER 0.5 3-pointers made | -235 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Josh Green (UTA) UNDER 1.5 3-pointers made | -230 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

**Combined probability 19.0%; parlay pays 4.1x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Alperen Sengun (HOU) UNDER 1.5 Steals (67%); Moussa Diabate (CHA) OVER 0.5 Blocks (66%); Sidy Cissoko (POR) OVER 0.5 3-pointers made (66%). Combined probability 29.0%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikel Brown Jr. (BKN) OVER 2.5 Rebounds | +126 (DraftKings via ESPN) | 3.0 | 67% | 41% | +0.51 |
| Julian Champagnie (SAS) UNDER 5.5 Rebounds | +111 (DraftKings via ESPN) | 4.5 | 67% | 44% | +0.41 |

Combined probability 44.4%; parlay pays 4.8x; expected profit per 1 staked +1.12.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikel Brown Jr. (BKN) OVER 2.5 Rebounds | +126 (DraftKings via ESPN) | 3.0 | 67% | 41% | +0.51 |
| Julian Champagnie (SAS) UNDER 5.5 Rebounds | +111 (DraftKings via ESPN) | 4.5 | 67% | 44% | +0.41 |
| Zion Williamson (NOP) UNDER 22.5 Points | -117 (DraftKings via ESPN) | 16.5 | 72% | 51% | +0.34 |

Combined probability 32.0%; parlay pays 8.8x; expected profit per 1 staked +1.83.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikel Brown Jr. (BKN) OVER 2.5 Rebounds | +126 (DraftKings via ESPN) | 3.0 | 67% | 41% | +0.51 |
| Julian Champagnie (SAS) UNDER 5.5 Rebounds | +111 (DraftKings via ESPN) | 4.5 | 67% | 44% | +0.41 |
| Zion Williamson (NOP) UNDER 22.5 Points | -117 (DraftKings via ESPN) | 16.5 | 72% | 51% | +0.34 |
| Scoot Henderson (POR) OVER 9.5 Points | -107 (DraftKings via ESPN) | 12.7 | 66% | 49% | +0.28 |

Combined probability 21.1%; parlay pays 17.1x; expected profit per 1 staked +2.62.

Top single picks by model edge:

- Mikel Brown Jr. (BKN) OVER 2.5 Rebounds: model 67% vs book 41%, EV +0.51 at +126 (projection 3.0)
- Julian Champagnie (SAS) UNDER 5.5 Rebounds: model 67% vs book 44%, EV +0.41 at +111 (projection 4.5)
- Zion Williamson (NOP) UNDER 22.5 Points: model 72% vs book 51%, EV +0.34 at -117 (projection 16.5)
- Jeremiah Fears (NOP) UNDER 5.5 Assists: model 69% vs book 49%, EV +0.31 at -111 (projection 4.5)
- Scoot Henderson (POR) OVER 9.5 Points: model 66% vs book 49%, EV +0.28 at -107 (projection 12.7)
- Shai Gilgeous-Alexander (OKC) OVER 5.5 Assists: model 63% vs book 46%, EV +0.28 at +104 (projection 5.8)
- Immanuel Quickley (TOR) OVER 2.5 3-pointers made: model 63% vs book 46%, EV +0.28 at +103 (projection 3.2)
- Matisse Thybulle (LAL) OVER 2.5 Rebounds: model 55% vs book 41%, EV +0.28 at +130 (projection 2.8)
- Damian Lillard (POR) OVER 4.5 Assists: model 56% vs book 41%, EV +0.27 at +126 (projection 5.0)
- Jaylen Wells (MEM) OVER 9.5 Points: model 66% vs book 49%, EV +0.27 at -109 (projection 12.7)
- Jrue Holiday (POR) OVER 4.5 Assists: model 59% vs book 44%, EV +0.26 at +113 (projection 5.2)
- Devin Vassell (SAS) UNDER 16.5 Points: model 66% vs book 50%, EV +0.25 at -113 (projection 14.3)

## MEM at CHA (game 401910036)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Moussa Diabate (CHA) OVER 0.5 Blocks | -239 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Cedric Coward (MEM) UNDER 1.5 Steals | -219 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |
| Taylor Hendricks (MEM) OVER 0.5 3-pointers made | -191 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |

Combined probability 26.2%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Moussa Diabate (CHA) OVER 0.5 Blocks: 66%, EV -0.06 at -239
- Cedric Coward (MEM) UNDER 1.5 Steals: 64%, EV -0.06 at -219
- Taylor Hendricks (MEM) OVER 0.5 3-pointers made: 62%, EV -0.06 at -191
- Cedric Coward (MEM) OVER 2.5 Assists: 60%, EV -0.06 at -179
- Cedric Coward (MEM) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -179
- Coby White (CHA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Sion James (CHA) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Cam Spencer (MEM) OVER 2.5 Rebounds: 60%, EV -0.06 at -175

## POR at PHI (game 401910037)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Sidy Cissoko (POR) OVER 0.5 3-pointers made | -235 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Toumani Camara (POR) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Tyrese Maxey (PHI) OVER 0.5 Steals | -224 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |

Combined probability 27.8%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Sidy Cissoko (POR) OVER 0.5 3-pointers made: 66%, EV -0.06 at -235
- Toumani Camara (POR) UNDER 1.5 Steals: 65%, EV -0.06 at -226
- Tyrese Maxey (PHI) OVER 0.5 Steals: 65%, EV -0.06 at -224
- Scoot Henderson (POR) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -204
- Jrue Holiday (POR) OVER 0.5 Steals: 63%, EV -0.06 at -201
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 61%, EV -0.06 at -185
- VJ Edgecombe (PHI) UNDER 0.5 Blocks: 61%, EV -0.06 at -184
- Jrue Holiday (POR) OVER 1.5 3-pointers made: 61%, EV -0.06 at -182

## OKC at IND (game 401910038)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ajay Mitchell (OKC) UNDER 1.5 Steals | -227 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals | -211 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Quenton Jackson (IND) UNDER 1.5 3-pointers made | -202 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |

Combined probability 26.0%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ajay Mitchell (OKC) UNDER 1.5 Steals: 65%, EV -0.06 at -227
- Ajay Mitchell (OKC) OVER 0.5 3-pointers made: 65%, EV -0.06 at -223
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 64%, EV -0.06 at -211
- Quenton Jackson (IND) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -202
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Jared McCain (OKC) UNDER 2.5 Assists: 60%, EV -0.06 at -179
- Shai Gilgeous-Alexander (OKC) OVER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Obi Toppin (IND) UNDER 4.5 Rebounds: 57%, EV -0.06 at -156

## MIL at TOR (game 401910039)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ja'Kobe Walter (TOR) UNDER 1.5 Steals | -207 (DraftKings via ESPN) | 1.5 | 63% | 63% | -0.06 |
| Kyle Kuzma (MIL) OVER 1.5 Assists | -192 (DraftKings via ESPN) | 1.9 | 62% | 62% | -0.06 |
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -192 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |

Combined probability 24.0%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ja'Kobe Walter (TOR) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Kyle Kuzma (MIL) OVER 1.5 Assists: 62%, EV -0.06 at -192
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Ja'Kobe Walter (TOR) UNDER 2.5 Assists: 61%, EV -0.06 at -187
- Tyler Herro (MIL) OVER 3.5 Assists: 56%, EV -0.06 at -152
- Ja'Kobe Walter (TOR) OVER 3.5 Rebounds: 56%, EV -0.06 at -152
- Kyle Kuzma (MIL) UNDER 1.5 3-pointers made: 56%, EV -0.06 at -151
- Jaime Jaquez Jr. (MIL) OVER 2.5 Assists: 56%, EV -0.06 at -150

## BKN at MIN (game 401910040)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Rudy Gobert (MIN) UNDER 1.5 Blocks | -195 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| Danny Wolf (BKN) UNDER 1.5 3-pointers made | -191 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |
| Mikel Brown Jr. (BKN) UNDER 2.5 3-pointers made | -190 (DraftKings via ESPN) | 1.0 | 61% | 61% | -0.06 |

Combined probability 23.4%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Rudy Gobert (MIN) UNDER 1.5 Blocks: 62%, EV -0.06 at -195
- Danny Wolf (BKN) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Mikel Brown Jr. (BKN) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -190
- Michael Porter Jr. (BKN) OVER 1.5 Assists: 61%, EV -0.06 at -189
- Terrence Shannon Jr. (MIN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Trey Lyles (MIN) OVER 0.5 3-pointers made: 61%, EV -0.06 at -183
- Jaden McDaniels (MIN) UNDER 1.5 Steals: 59%, EV -0.06 at -174
- Ayo Dosunmu (MIN) UNDER 1.5 Steals: 59%, EV -0.06 at -169

## CLE at CHI (game 401910041)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| James Harden (CLE) UNDER 1.5 Steals | -212 (DraftKings via ESPN) | 0.9 | 64% | 64% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -195 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Meleek Thomas (CLE) OVER 0.5 Steals | -173 (DraftKings via ESPN) | 1.3 | 59% | 59% | -0.06 |

Combined probability 23.3%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- James Harden (CLE) UNDER 1.5 Steals: 64%, EV -0.06 at -212
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 62%, EV -0.06 at -195
- Meleek Thomas (CLE) OVER 0.5 Steals: 59%, EV -0.06 at -173
- Tyrese Proctor (CLE) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -163
- Donovan Mitchell (CLE) OVER 4.5 Assists: 58%, EV -0.06 at -159
- Isaac Okoro (CHI) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -156
- Tyrese Proctor (CLE) OVER 2.5 Rebounds: 57%, EV -0.06 at -156
- Matas Buzelis (CHI) UNDER 5.5 Rebounds: 56%, EV -0.06 at -152

## PHX at NOP (game 401910042)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -199 (DraftKings via ESPN) | 1.2 | 62% | 62% | -0.06 |
| Saddiq Bey (NOP) OVER 1.5 3-pointers made | -182 (DraftKings via ESPN) | 2.1 | 60% | 60% | -0.06 |
| Derik Queen (NOP) UNDER 2.5 Assists | -180 (DraftKings via ESPN) | 2.3 | 60% | 60% | -0.06 |

Combined probability 22.8%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -199
- Herbert Jones (NOP) OVER 1.5 Assists: 60%, EV -0.06 at -182
- Saddiq Bey (NOP) OVER 1.5 3-pointers made: 60%, EV -0.06 at -182
- Derik Queen (NOP) UNDER 2.5 Assists: 60%, EV -0.06 at -180
- Devin Booker (PHX) OVER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Collin Gillespie (PHX) UNDER 1.5 Steals: 60%, EV -0.06 at -177
- Dillon Brooks (PHX) OVER 1.5 Assists: 59%, EV -0.06 at -171
- Jalen Green (PHX) OVER 2.5 Assists: 59%, EV -0.06 at -166

## LAC at HOU (game 401910043)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) UNDER 1.5 Steals | -244 (DraftKings via ESPN) | 0.9 | 67% | 67% | -0.06 |
| Amen Thompson (HOU) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Derrick Jones Jr. (LAC) OVER 0.5 3-pointers made | -235 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |

Combined probability 29.0%; parlay pays 2.8x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Alperen Sengun (HOU) UNDER 1.5 Steals: 67%, EV -0.06 at -244
- Amen Thompson (HOU) UNDER 1.5 Steals: 66%, EV -0.06 at -241
- Derrick Jones Jr. (LAC) OVER 0.5 3-pointers made: 66%, EV -0.06 at -235
- Darius Garland (LAC) OVER 0.5 Steals: 65%, EV -0.06 at -223
- Keaton Wagler (LAC) OVER 0.5 3-pointers made: 65%, EV -0.06 at -222
- Jabari Smith Jr. (HOU) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Brook Lopez (LAC) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Keaton Wagler (LAC) OVER 1.5 Assists: 60%, EV -0.06 at -179

## UTA at LAL (game 401910044)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Green (UTA) UNDER 1.5 3-pointers made | -230 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Ziaire Williams (LAL) UNDER 1.5 3-pointers made | -227 (DraftKings via ESPN) | 1.5 | 65% | 65% | -0.06 |
| Collin Sexton (LAL) UNDER 1.5 3-pointers made | -224 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |

Combined probability 27.7%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Josh Green (UTA) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -230
- Ziaire Williams (LAL) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -227
- Collin Sexton (LAL) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -224
- Quentin Grimes (LAL) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -195
- Darryn Peterson (UTA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -187
- Sandro Mamukelashvili (LAL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Keyonte George (UTA) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Walker Kessler (LAL) OVER 1.5 Blocks: 60%, EV -0.06 at -181

## SAS at SAC (game 401910045)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Devin Vassell (SAS) OVER 1.5 3-pointers made | -174 (DraftKings via ESPN) | 2.2 | 60% | 60% | -0.06 |
| Stephon Castle (SAS) OVER 1.5 3-pointers made | -167 (DraftKings via ESPN) | 2.1 | 59% | 59% | -0.06 |
| Zach LaVine (SAC) UNDER 3.5 Rebounds | -164 (DraftKings via ESPN) | 2.8 | 58% | 58% | -0.06 |

Combined probability 20.3%; parlay pays 4.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Devin Vassell (SAS) OVER 1.5 3-pointers made: 60%, EV -0.06 at -174
- Stephon Castle (SAS) OVER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Zach LaVine (SAC) UNDER 3.5 Rebounds: 58%, EV -0.06 at -164
- De'Andre Hunter (SAC) OVER 3.5 Rebounds: 58%, EV -0.06 at -163
- Julian Champagnie (SAS) OVER 1.5 Assists: 58%, EV -0.06 at -162
- De'Andre Hunter (SAC) OVER 1.5 3-pointers made: 58%, EV -0.06 at -161
- Darius Acuff Jr. (SAC) UNDER 3.5 Rebounds: 58%, EV -0.06 at -160
- Zach LaVine (SAC) UNDER 2.5 Assists: 57%, EV -0.06 at -157
