# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-16T19:20:53Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) OVER 0.5 Steals | -243 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Jaylen Brown (PHI) OVER 0.5 Steals | -242 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Ayo Dosunmu (MIN) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |

**Combined probability 19.4%; parlay pays 4.0x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Alperen Sengun (HOU) OVER 0.5 Steals (66%); Jaylen Brown (PHI) OVER 0.5 Steals (66%); Ayo Dosunmu (MIN) UNDER 1.5 Steals (66%). Combined probability 29.3%; parlay pays 2.8x; expected profit per 1 staked -0.18.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -111 (DraftKings via ESPN) | 5.1 | 70% | 49% | +0.34 |
| Michael Porter Jr. (BKN) UNDER 22.5 Points | -124 (DraftKings via ESPN) | 16.2 | 72% | 52% | +0.30 |

Combined probability 50.5%; parlay pays 3.4x; expected profit per 1 staked +0.74.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -111 (DraftKings via ESPN) | 5.1 | 70% | 49% | +0.34 |
| Michael Porter Jr. (BKN) UNDER 22.5 Points | -124 (DraftKings via ESPN) | 16.2 | 72% | 52% | +0.30 |
| AJ Dybantsa (WAS) OVER 5.5 Rebounds | +106 (DraftKings via ESPN) | 6.3 | 63% | 45% | +0.30 |

Combined probability 31.8%; parlay pays 7.1x; expected profit per 1 staked +1.25.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -111 (DraftKings via ESPN) | 5.1 | 70% | 49% | +0.34 |
| Michael Porter Jr. (BKN) UNDER 22.5 Points | -124 (DraftKings via ESPN) | 16.2 | 72% | 52% | +0.30 |
| AJ Dybantsa (WAS) OVER 5.5 Rebounds | +106 (DraftKings via ESPN) | 6.3 | 63% | 45% | +0.30 |
| Miles Bridges (PHX) UNDER 14.5 Points | -108 (DraftKings via ESPN) | 12.1 | 67% | 49% | +0.29 |

Combined probability 21.4%; parlay pays 13.6x; expected profit per 1 staked +1.91.

Top single picks by model edge:

- Franz Wagner (ORL) UNDER 6.5 Assists: model 70% vs book 49%, EV +0.34 at -111 (projection 5.1)
- Sam Hauser (BOS) UNDER 1.5 3-pointers made: model 58% vs book 42%, EV +0.31 at +125 (projection 1.4)
- Michael Porter Jr. (BKN) UNDER 22.5 Points: model 72% vs book 52%, EV +0.30 at -124 (projection 16.2)
- AJ Dybantsa (WAS) OVER 5.5 Rebounds: model 63% vs book 45%, EV +0.30 at +106 (projection 6.3)
- Miles Bridges (PHX) UNDER 14.5 Points: model 67% vs book 49%, EV +0.29 at -108 (projection 12.1)
- Jonathan Kuminga (MIN) OVER 13.5 Points: model 64% vs book 47%, EV +0.29 at +100 (projection 16.4)
- Ayo Dosunmu (MIN) OVER 3.5 Assists: model 57% vs book 42%, EV +0.27 at +122 (projection 4.0)
- Josh Giddey (CHI) OVER 1.5 3-pointers made: model 53% vs book 40%, EV +0.26 at +136 (projection 1.8)
- Giannis Antetokounmpo (MIA) UNDER 28.5 Points: model 64% vs book 49%, EV +0.25 at -106 (projection 25.4)
- Damian Lillard (POR) UNDER 2.5 3-pointers made: model 55% vs book 41%, EV +0.23 at +126 (projection 2.4)
- Davion Mitchell (MIA) UNDER 7.5 Assists: model 59% vs book 45%, EV +0.22 at +106 (projection 6.7)
- Julius Randle (BKN) UNDER 4.5 Assists: model 59% vs book 46%, EV +0.21 at +105 (projection 4.1)

## ORL at BOS (game 401909994)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Neemias Queta (BOS) UNDER 1.5 Blocks | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Franz Wagner (ORL) UNDER 1.5 Steals | -229 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Jayson Tatum (BOS) OVER 0.5 Steals | -213 (DraftKings via ESPN) | 0.9 | 64% | 64% | -0.06 |

Combined probability 27.5%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Neemias Queta (BOS) UNDER 1.5 Blocks: 66%, EV -0.06 at -239
- Franz Wagner (ORL) UNDER 1.5 Steals: 65%, EV -0.06 at -229
- Jayson Tatum (BOS) OVER 0.5 Steals: 64%, EV -0.06 at -213
- Derrick White (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Desmond Bane (ORL) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -171
- Payton Pritchard (BOS) UNDER 3.5 Rebounds: 59%, EV -0.06 at -169
- Payton Pritchard (BOS) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -167
- Sam Hauser (BOS) OVER 1.5 3-pointers made: 58%, EV -0.06 at -166

## CHI at CLE (game 401909995)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -241 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Isaac Okoro (CHI) UNDER 1.5 3-pointers made | -238 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Matas Buzelis (CHI) UNDER 2.5 Assists | -185 (DraftKings via ESPN) | 2.2 | 61% | 61% | -0.06 |

Combined probability 26.6%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Donovan Mitchell (CLE) UNDER 1.5 Steals: 66%, EV -0.06 at -241
- Isaac Okoro (CHI) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -238
- Matas Buzelis (CHI) UNDER 2.5 Assists: 61%, EV -0.06 at -185
- Meleek Thomas (CLE) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -184
- Josh Giddey (CHI) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Matas Buzelis (CHI) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -179
- Donovan Mitchell (CLE) OVER 2.5 3-pointers made: 55%, EV -0.06 at -144

## MEM at WAS (game 401909996)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| AJ Dybantsa (WAS) UNDER 1.5 3-pointers made | -233 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Anthony Davis (WAS) UNDER 1.5 Steals | -230 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Cam Spencer (MEM) UNDER 1.5 Steals | -228 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 28.0%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -233
- Anthony Davis (WAS) UNDER 1.5 Steals: 65%, EV -0.06 at -230
- Cam Spencer (MEM) UNDER 1.5 Steals: 65%, EV -0.06 at -228
- Kyshawn George (WAS) OVER 0.5 Blocks: 65%, EV -0.06 at -224
- AJ Dybantsa (WAS) OVER 0.5 Steals: 64%, EV -0.06 at -220
- Jaylen Wells (MEM) OVER 0.5 Steals: 64%, EV -0.06 at -217
- Trae Young (WAS) UNDER 1.5 Steals: 63%, EV -0.06 at -208
- Cedric Coward (MEM) UNDER 1.5 Steals: 63%, EV -0.06 at -205

## PHI at BKN (game 401909997)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jaylen Brown (PHI) OVER 0.5 Steals | -242 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Julius Randle (BKN) UNDER 1.5 3-pointers made | -215 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |
| VJ Edgecombe (PHI) UNDER 1.5 Steals | -192 (DraftKings via ESPN) | 1.6 | 62% | 62% | -0.06 |

Combined probability 26.1%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jaylen Brown (PHI) OVER 0.5 Steals: 66%, EV -0.06 at -242
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -215
- VJ Edgecombe (PHI) UNDER 1.5 Steals: 62%, EV -0.06 at -192
- Anfernee Simons (PHI) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 60%, EV -0.06 at -178
- Michael Porter Jr. (BKN) UNDER 3.5 3-pointers made: 60%, EV -0.06 at -177
- Jaylen Brown (PHI) OVER 3.5 Assists: 59%, EV -0.06 at -167
- Danny Wolf (BKN) UNDER 2.5 Assists: 58%, EV -0.06 at -161

## HOU at MIA (game 401909998)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) OVER 0.5 Steals | -243 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Bobby Portis (MIA) UNDER 1.5 3-pointers made | -222 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Fred VanVleet (HOU) UNDER 1.5 Steals | -218 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |

Combined probability 27.6%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Alperen Sengun (HOU) OVER 0.5 Steals: 66%, EV -0.06 at -243
- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -222
- Fred VanVleet (HOU) UNDER 1.5 Steals: 64%, EV -0.06 at -218
- Andrew Wiggins (MIA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -195
- Jabari Smith Jr. (HOU) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- Amen Thompson (HOU) UNDER 1.5 Steals: 60%, EV -0.06 at -180
- Fred VanVleet (HOU) UNDER 3.5 Rebounds: 59%, EV -0.06 at -173
- Davion Mitchell (MIA) OVER 1.5 3-pointers made: 59%, EV -0.06 at -172

## POR at MIN (game 401909999)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ayo Dosunmu (MIN) UNDER 1.5 Steals | -242 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Jaden McDaniels (MIN) OVER 0.5 Steals | -231 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Damian Lillard (POR) OVER 0.5 Steals | -226 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |

Combined probability 28.2%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ayo Dosunmu (MIN) UNDER 1.5 Steals: 66%, EV -0.06 at -242
- Jaden McDaniels (MIN) OVER 0.5 Steals: 65%, EV -0.06 at -231
- Damian Lillard (POR) OVER 0.5 Steals: 65%, EV -0.06 at -226
- Toumani Camara (POR) UNDER 0.5 Blocks: 64%, EV -0.06 at -220
- Toumani Camara (POR) UNDER 1.5 Steals: 64%, EV -0.06 at -211
- Jaden McDaniels (MIN) OVER 0.5 Blocks: 63%, EV -0.06 at -209
- Jrue Holiday (POR) OVER 0.5 Steals: 63%, EV -0.06 at -208
- Jonathan Kuminga (MIN) OVER 0.5 Steals: 63%, EV -0.06 at -208

## GSW at NOP (game 401910000)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brandin Podziemski (GSW) UNDER 1.5 Steals | -225 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| De'Anthony Melton (GSW) OVER 1.5 3-pointers made | -192 (DraftKings via ESPN) | 1.8 | 62% | 62% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 Steals | -185 (DraftKings via ESPN) | 1.2 | 61% | 61% | -0.06 |

Combined probability 24.3%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Brandin Podziemski (GSW) UNDER 1.5 Steals: 65%, EV -0.06 at -225
- De'Anthony Melton (GSW) OVER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Herbert Jones (NOP) UNDER 1.5 Steals: 61%, EV -0.06 at -185
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Zion Williamson (NOP) OVER 2.5 Assists: 58%, EV -0.06 at -165
- De'Anthony Melton (GSW) UNDER 3.5 Assists: 58%, EV -0.06 at -163
- De'Anthony Melton (GSW) UNDER 4.5 Rebounds: 58%, EV -0.06 at -163
- Yaxel Lendeborg (GSW) UNDER 4.5 Assists: 57%, EV -0.06 at -159

## PHX at DEN (game 401910001)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cameron Johnson (DEN) OVER 1.5 3-pointers made | -195 (DraftKings via ESPN) | 1.9 | 62% | 62% | -0.06 |
| Dillon Brooks (PHX) UNDER 2.5 Assists | -189 (DraftKings via ESPN) | 1.7 | 61% | 61% | -0.06 |
| Devin Booker (PHX) OVER 2.5 Rebounds | -175 (DraftKings via ESPN) | 3.0 | 60% | 60% | -0.06 |

Combined probability 22.7%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 62%, EV -0.06 at -195
- Dillon Brooks (PHX) UNDER 2.5 Assists: 61%, EV -0.06 at -189
- Devin Booker (PHX) OVER 2.5 Rebounds: 60%, EV -0.06 at -175
- Cameron Johnson (DEN) OVER 1.5 Assists: 59%, EV -0.06 at -173
- Jalen Green (PHX) OVER 2.5 Rebounds: 59%, EV -0.06 at -172
- Christian Braun (DEN) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -164
- Jamal Murray (DEN) OVER 2.5 3-pointers made: 58%, EV -0.06 at -162
- Nikola Jokic (DEN) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -161
