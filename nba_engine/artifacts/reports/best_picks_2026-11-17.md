# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-16T23:12:27Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made | -300 (DraftKings via ESPN) | 0.5 | 71% | 71% | -0.06 |
| Jaden McDaniels (MIN) OVER 0.5 Steals | -241 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Trae Young (WAS) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Alperen Sengun (HOU) OVER 0.5 Steals | -239 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |

**Combined probability 20.5%; parlay pays 3.8x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made (71%); Jaden McDaniels (MIN) OVER 0.5 Steals (66%); Trae Young (WAS) UNDER 1.5 Steals (66%). Combined probability 30.9%; parlay pays 2.7x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -105 (DraftKings via ESPN) | 5.1 | 70% | 48% | +0.37 |
| Michael Porter Jr. (BKN) UNDER 22.5 Points | -119 (DraftKings via ESPN) | 16.2 | 72% | 51% | +0.32 |

Combined probability 50.3%; parlay pays 3.6x; expected profit per 1 staked +0.81.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -105 (DraftKings via ESPN) | 5.1 | 70% | 48% | +0.37 |
| Michael Porter Jr. (BKN) UNDER 22.5 Points | -119 (DraftKings via ESPN) | 16.2 | 72% | 51% | +0.32 |
| James Harden (CLE) OVER 17.5 Points | -110 (DraftKings via ESPN) | 19.7 | 69% | 49% | +0.32 |

Combined probability 34.8%; parlay pays 6.9x; expected profit per 1 staked +1.39.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 6.5 Assists | -105 (DraftKings via ESPN) | 5.1 | 70% | 48% | +0.37 |
| Michael Porter Jr. (BKN) UNDER 22.5 Points | -119 (DraftKings via ESPN) | 16.2 | 72% | 51% | +0.32 |
| James Harden (CLE) OVER 17.5 Points | -110 (DraftKings via ESPN) | 19.7 | 69% | 49% | +0.32 |
| Jonathan Kuminga (MIN) OVER 12.5 Points | -112 (DraftKings via ESPN) | 16.4 | 69% | 50% | +0.31 |

Combined probability 24.1%; parlay pays 13.0x; expected profit per 1 staked +2.12.

Top single picks by model edge:

- Franz Wagner (ORL) UNDER 6.5 Assists: model 70% vs book 48%, EV +0.37 at -105 (projection 5.1)
- Michael Porter Jr. (BKN) UNDER 22.5 Points: model 72% vs book 51%, EV +0.32 at -119 (projection 16.2)
- James Harden (CLE) OVER 17.5 Points: model 69% vs book 49%, EV +0.32 at -110 (projection 19.7)
- Jonathan Kuminga (MIN) OVER 12.5 Points: model 69% vs book 50%, EV +0.31 at -112 (projection 16.4)
- Anfernee Simons (PHI) UNDER 10.5 Points: model 65% vs book 47%, EV +0.29 at -101 (projection 9.1)
- Tyrese Proctor (CLE) OVER 3.5 Assists: model 64% vs book 47%, EV +0.28 at +101 (projection 4.4)
- Josh Giddey (CHI) OVER 1.5 3-pointers made: model 53% vs book 39%, EV +0.28 at +142 (projection 1.8)
- AJ Dybantsa (WAS) OVER 5.5 Rebounds: model 63% vs book 46%, EV +0.28 at +103 (projection 6.3)
- Sam Hauser (BOS) UNDER 1.5 3-pointers made: model 54% vs book 40%, EV +0.27 at +137 (projection 1.6)
- Donovan Mitchell (CLE) OVER 5.5 Assists: model 64% vs book 47%, EV +0.26 at -102 (projection 5.8)
- Mitchell Robinson (BOS) UNDER 5.5 Points: model 65% vs book 49%, EV +0.26 at -106 (projection 4.7)
- Miles Bridges (PHX) UNDER 14.5 Points: model 67% vs book 51%, EV +0.25 at -117 (projection 12.1)

## ORL at BOS (game 401909994)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Franz Wagner (ORL) UNDER 1.5 Steals | -219 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Jayson Tatum (BOS) OVER 0.5 Steals | -197 (DraftKings via ESPN) | 0.9 | 62% | 62% | -0.06 |
| Payton Pritchard (BOS) OVER 1.5 3-pointers made | -184 (DraftKings via ESPN) | 2.1 | 61% | 61% | -0.06 |

Combined probability 24.3%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Franz Wagner (ORL) UNDER 1.5 Steals: 64%, EV -0.06 at -219
- Jayson Tatum (BOS) OVER 0.5 Steals: 62%, EV -0.06 at -197
- Payton Pritchard (BOS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Sam Hauser (BOS) OVER 1.5 3-pointers made: 60%, EV -0.06 at -182
- Payton Pritchard (BOS) OVER 2.5 Rebounds: 60%, EV -0.06 at -174
- Derrick White (BOS) OVER 0.5 Steals: 59%, EV -0.06 at -172
- Derrick White (BOS) OVER 1.5 3-pointers made: 59%, EV -0.06 at -166
- Sam Hauser (BOS) UNDER 3.5 Rebounds: 58%, EV -0.06 at -162

## CHI at CLE (game 401909995)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Isaac Okoro (CHI) OVER 0.5 3-pointers made | -227 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -204 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Josh Giddey (CHI) UNDER 1.5 3-pointers made | -189 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |

Combined probability 25.1%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Isaac Okoro (CHI) OVER 0.5 3-pointers made: 65%, EV -0.06 at -227
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 63%, EV -0.06 at -204
- Josh Giddey (CHI) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Matas Buzelis (CHI) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181
- Matas Buzelis (CHI) UNDER 2.5 Assists: 60%, EV -0.06 at -176
- Meleek Thomas (CLE) OVER 1.5 3-pointers made: 59%, EV -0.06 at -170
- James Harden (CLE) OVER 6.5 Assists: 56%, EV -0.06 at -149

## MEM at WAS (game 401909996)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Trae Young (WAS) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Taylor Hendricks (MEM) UNDER 1.5 3-pointers made | -236 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Anthony Davis (WAS) UNDER 1.5 Steals | -237 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |

Combined probability 28.8%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Trae Young (WAS) UNDER 1.5 Steals: 66%, EV -0.06 at -239
- Taylor Hendricks (MEM) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -236
- Anthony Davis (WAS) UNDER 1.5 Steals: 66%, EV -0.06 at -237
- Cam Spencer (MEM) UNDER 1.5 Steals: 66%, EV -0.06 at -233
- AJ Dybantsa (WAS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -225
- AJ Dybantsa (WAS) OVER 0.5 Steals: 65%, EV -0.06 at -227
- Kyshawn George (WAS) OVER 0.5 Blocks: 64%, EV -0.06 at -216
- Jaylen Wells (MEM) OVER 0.5 Steals: 64%, EV -0.06 at -211

## PHI at BKN (game 401909997)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made | -300 (DraftKings via ESPN) | 0.5 | 71% | 71% | -0.06 |
| Jaylen Brown (PHI) UNDER 1.5 Steals | -233 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Julius Randle (BKN) UNDER 1.5 3-pointers made | -189 (DraftKings via ESPN) | 1.3 | 61% | 61% | -0.06 |

Combined probability 28.4%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Day'Ron Sharpe (BKN) UNDER 0.5 3-pointers made: 71%, EV -0.06 at -300
- Day'Ron Sharpe (BKN) OVER 0.5 Blocks: 66%, EV -0.06 at -234
- Jaylen Brown (PHI) UNDER 1.5 Steals: 66%, EV -0.06 at -233
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -189
- VJ Edgecombe (PHI) UNDER 1.5 Steals: 61%, EV -0.06 at -188
- Tyrese Maxey (PHI) UNDER 1.5 Steals: 60%, EV -0.06 at -179
- Dean Wade (PHI) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Anfernee Simons (PHI) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -170

## HOU at MIA (game 401909998)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Alperen Sengun (HOU) OVER 0.5 Steals | -239 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Bobby Portis (MIA) OVER 0.5 3-pointers made | -231 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Fred VanVleet (HOU) UNDER 1.5 Steals | -226 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

Combined probability 28.2%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Alperen Sengun (HOU) OVER 0.5 Steals: 66%, EV -0.06 at -239
- Bobby Portis (MIA) OVER 0.5 3-pointers made: 65%, EV -0.06 at -231
- Fred VanVleet (HOU) UNDER 1.5 Steals: 65%, EV -0.06 at -226
- Andrew Wiggins (MIA) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -205
- Jabari Smith Jr. (HOU) OVER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Davion Mitchell (MIA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Fred VanVleet (HOU) UNDER 3.5 Rebounds: 59%, EV -0.06 at -173
- Amen Thompson (HOU) UNDER 1.5 Steals: 59%, EV -0.07 at -170

## POR at MIN (game 401909999)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jaden McDaniels (MIN) OVER 0.5 Steals | -241 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Damian Lillard (POR) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Ayo Dosunmu (MIN) UNDER 1.5 Steals | -234 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |

Combined probability 28.6%; parlay pays 2.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jaden McDaniels (MIN) OVER 0.5 Steals: 66%, EV -0.06 at -241
- Damian Lillard (POR) OVER 0.5 Steals: 66%, EV -0.06 at -236
- Ayo Dosunmu (MIN) UNDER 1.5 Steals: 66%, EV -0.06 at -234
- Jrue Holiday (POR) OVER 0.5 Steals: 63%, EV -0.06 at -208
- Jonathan Kuminga (MIN) OVER 0.5 Steals: 63%, EV -0.06 at -208
- Toumani Camara (POR) UNDER 1.5 Steals: 63%, EV -0.06 at -202
- Jaden McDaniels (MIN) OVER 0.5 Blocks: 62%, EV -0.06 at -200
- Deni Avdija (POR) OVER 0.5 Steals: 62%, EV -0.06 at -199

## GSW at NOP (game 401910000)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brandin Podziemski (GSW) UNDER 1.5 Steals | -221 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -209 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| De'Anthony Melton (GSW) OVER 1.5 3-pointers made | -191 (DraftKings via ESPN) | 1.8 | 62% | 62% | -0.06 |

Combined probability 25.2%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Brandin Podziemski (GSW) UNDER 1.5 Steals: 65%, EV -0.06 at -221
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -209
- De'Anthony Melton (GSW) OVER 1.5 3-pointers made: 62%, EV -0.06 at -191
- Herbert Jones (NOP) UNDER 1.5 Steals: 59%, EV -0.06 at -170
- Zion Williamson (NOP) UNDER 3.5 Assists: 59%, EV -0.06 at -167
- Herbert Jones (NOP) OVER 1.5 Assists: 58%, EV -0.06 at -165
- Yaxel Lendeborg (GSW) OVER 3.5 Assists: 58%, EV -0.06 at -165
- De'Anthony Melton (GSW) OVER 3.5 Rebounds: 58%, EV -0.06 at -161

## PHX at DEN (game 401910001)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Dillon Brooks (PHX) UNDER 2.5 Assists | -196 (DraftKings via ESPN) | 1.7 | 62% | 62% | -0.06 |
| Cameron Johnson (DEN) OVER 1.5 3-pointers made | -187 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |
| Christian Braun (DEN) UNDER 2.5 Assists | -180 (DraftKings via ESPN) | 2.4 | 60% | 60% | -0.06 |

Combined probability 22.9%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Dillon Brooks (PHX) UNDER 2.5 Assists: 62%, EV -0.06 at -196
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Christian Braun (DEN) UNDER 2.5 Assists: 60%, EV -0.06 at -180
- Cameron Johnson (DEN) OVER 1.5 Assists: 59%, EV -0.06 at -173
- Collin Gillespie (PHX) OVER 2.5 Rebounds: 59%, EV -0.06 at -172
- Nikola Jokic (DEN) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Jalen Green (PHX) OVER 2.5 Rebounds: 59%, EV -0.06 at -169
- Devin Booker (PHX) OVER 2.5 Rebounds: 59%, EV -0.06 at -167
