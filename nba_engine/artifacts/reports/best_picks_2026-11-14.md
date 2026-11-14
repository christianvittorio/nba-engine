# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-14T20:13:41Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Davion Mitchell (MIA) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Peyton Watson (CLE) UNDER 1.5 Blocks | -237 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Matas Buzelis (CHI) UNDER 2.5 3-pointers made | -179 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |

**Combined probability 16.8%; parlay pays 4.6x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Davion Mitchell (MIA) UNDER 1.5 Steals (66%); Peyton Watson (CLE) UNDER 1.5 Blocks (66%); Herbert Jones (NOP) UNDER 1.5 Steals (64%). Combined probability 27.9%; parlay pays 3.0x; expected profit per 1 staked -0.18.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) UNDER 3.5 Assists | +107 (DraftKings via ESPN) | 2.9 | 65% | 45% | +0.35 |
| Giannis Antetokounmpo (MIA) UNDER 29.5 Points | -123 (DraftKings via ESPN) | 24.4 | 73% | 52% | +0.32 |

Combined probability 47.3%; parlay pays 3.8x; expected profit per 1 staked +0.77.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) UNDER 3.5 Assists | +107 (DraftKings via ESPN) | 2.9 | 65% | 45% | +0.35 |
| Giannis Antetokounmpo (MIA) UNDER 29.5 Points | -123 (DraftKings via ESPN) | 24.4 | 73% | 52% | +0.32 |
| Zaccharie Risacher (DAL) OVER 3.5 Rebounds | +126 (DraftKings via ESPN) | 4.0 | 56% | 41% | +0.26 |

Combined probability 26.4%; parlay pays 8.5x; expected profit per 1 staked +1.24.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) UNDER 3.5 Assists | +107 (DraftKings via ESPN) | 2.9 | 65% | 45% | +0.35 |
| Giannis Antetokounmpo (MIA) UNDER 29.5 Points | -123 (DraftKings via ESPN) | 24.4 | 73% | 52% | +0.32 |
| Zaccharie Risacher (DAL) OVER 3.5 Rebounds | +126 (DraftKings via ESPN) | 4.0 | 56% | 41% | +0.26 |
| LaMelo Ball (MIN) UNDER 4.5 Rebounds | -133 (DraftKings via ESPN) | 3.5 | 68% | 53% | +0.20 |

Combined probability 18.1%; parlay pays 14.9x; expected profit per 1 staked +1.69.

Top single picks by model edge:

- Day'Ron Sharpe (BKN) UNDER 3.5 Assists: model 65% vs book 45%, EV +0.35 at +107 (projection 2.9)
- Julius Randle (BKN) UNDER 20.5 Points: model 71% vs book 50%, EV +0.33 at -114 (projection 17.2)
- Giannis Antetokounmpo (MIA) UNDER 29.5 Points: model 73% vs book 52%, EV +0.32 at -123 (projection 24.4)
- Michael Porter Jr. (BKN) UNDER 22.5 Points: model 70% vs book 51%, EV +0.29 at -119 (projection 18.9)
- Cam Spencer (MEM) UNDER 6.5 Assists: model 64% vs book 47%, EV +0.29 at +100 (projection 5.5)
- Davion Mitchell (MIA) UNDER 8.5 Assists: model 75% vs book 55%, EV +0.29 at -139 (projection 6.5)
- Davion Mitchell (MIA) OVER 2.5 Rebounds: model 58% vs book 43%, EV +0.28 at +120 (projection 2.9)
- Giannis Antetokounmpo (MIA) UNDER 5.5 Assists: model 70% vs book 52%, EV +0.27 at -124 (projection 4.3)
- Zaccharie Risacher (DAL) OVER 3.5 Rebounds: model 56% vs book 41%, EV +0.26 at +126 (projection 4.0)
- P.J. Washington (DAL) UNDER 1.5 3-pointers made: model 54% vs book 40%, EV +0.26 at +134 (projection 1.5)
- Davion Mitchell (MIA) UNDER 14.5 Points: model 69% vs book 53%, EV +0.23 at -126 (projection 12.3)
- Davion Mitchell (MIA) UNDER 1.5 3-pointers made: model 52% vs book 40%, EV +0.23 at +136 (projection 1.6)

## DEN at NOP (game 401909980)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Herbert Jones (NOP) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |
| Nikola Jokic (DEN) UNDER 1.5 Steals | -209 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |
| Cameron Johnson (DEN) OVER 1.5 Assists | -191 (DraftKings via ESPN) | 2.5 | 62% | 62% | -0.06 |

Combined probability 25.0%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Herbert Jones (NOP) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- Nikola Jokic (DEN) UNDER 1.5 Steals: 63%, EV -0.06 at -209
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -203
- Cameron Johnson (DEN) OVER 1.5 Assists: 62%, EV -0.06 at -191
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Jeremiah Fears (NOP) UNDER 1.5 Steals: 60%, EV -0.07 at -177
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Christian Braun (DEN) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171

## DAL at CLE (game 401909981)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Peyton Watson (CLE) UNDER 1.5 Blocks | -237 (DraftKings via ESPN) | 1.3 | 66% | 66% | -0.06 |
| James Harden (CLE) UNDER 1.5 Steals | -210 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -207 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |

Combined probability 26.4%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Peyton Watson (CLE) UNDER 1.5 Blocks: 66%, EV -0.06 at -237
- James Harden (CLE) UNDER 1.5 Steals: 63%, EV -0.06 at -210
- Kyrie Irving (DAL) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 61%, EV -0.06 at -190
- P.J. Washington (DAL) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Peyton Watson (CLE) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 60%, EV -0.06 at -174
- Naji Marshall (DAL) OVER 2.5 Assists: 59%, EV -0.06 at -172

## DET at MIA (game 401909982)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Davion Mitchell (MIA) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Bam Adebayo (MIA) OVER 0.5 3-pointers made | -222 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |
| Cade Cunningham (DET) UNDER 1.5 Steals | -205 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Davion Mitchell (MIA) UNDER 1.5 Steals: 66%, EV -0.06 at -239
- Bam Adebayo (MIA) OVER 0.5 3-pointers made: 65%, EV -0.06 at -222
- Cade Cunningham (DET) UNDER 1.5 Steals: 63%, EV -0.06 at -205
- Davion Mitchell (MIA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Bam Adebayo (MIA) UNDER 1.5 Steals: 60%, EV -0.06 at -178
- Duncan Robinson (DET) UNDER 2.5 Assists: 59%, EV -0.06 at -174
- Andrew Wiggins (MIA) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -170
- Andrew Wiggins (MIA) UNDER 3.5 Rebounds: 58%, EV -0.06 at -164

## BKN at MEM (game 401909983)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Michael Porter Jr. (BKN) OVER 1.5 Assists | -173 (DraftKings via ESPN) | 2.0 | 59% | 59% | -0.06 |
| Cedric Coward (MEM) OVER 2.5 Assists | -168 (DraftKings via ESPN) | 3.5 | 59% | 59% | -0.06 |
| Jerami Grant (MEM) UNDER 2.5 Rebounds | -166 (DraftKings via ESPN) | 2.4 | 59% | 59% | -0.06 |

Combined probability 20.4%; parlay pays 4.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Michael Porter Jr. (BKN) OVER 1.5 Assists: 59%, EV -0.06 at -173
- Cedric Coward (MEM) OVER 2.5 Assists: 59%, EV -0.06 at -168
- Jerami Grant (MEM) UNDER 2.5 Rebounds: 59%, EV -0.06 at -166
- Jaylen Wells (MEM) UNDER 1.5 Assists: 58%, EV -0.06 at -163
- Cam Spencer (MEM) UNDER 4.5 Rebounds: 58%, EV -0.06 at -162
- Michael Porter Jr. (BKN) UNDER 3.5 3-pointers made: 57%, EV -0.06 at -156
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -153
- Nolan Traore (BKN) UNDER 1.5 3-pointers made: 56%, EV -0.06 at -151

## CHI at MIN (game 401909984)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Matas Buzelis (CHI) UNDER 2.5 3-pointers made | -179 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |
| Josh Giddey (CHI) UNDER 1.5 3-pointers made | -178 (DraftKings via ESPN) | 1.5 | 60% | 60% | -0.06 |
| Rudy Gobert (MIN) UNDER 1.5 Blocks | -178 (DraftKings via ESPN) | 1.3 | 60% | 60% | -0.06 |

Combined probability 21.6%; parlay pays 3.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Matas Buzelis (CHI) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -179
- Josh Giddey (CHI) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Rudy Gobert (MIN) UNDER 1.5 Blocks: 60%, EV -0.06 at -178
- LaMelo Ball (MIN) UNDER 1.5 Steals: 60%, EV -0.06 at -178
- Jonathan Kuminga (MIN) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -174
- Ayo Dosunmu (MIN) OVER 3.5 Assists: 57%, EV -0.06 at -157
- Jaden McDaniels (MIN) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -153
- Jaden McDaniels (MIN) UNDER 6.5 Rebounds: 56%, EV -0.06 at -151
