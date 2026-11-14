# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-14T18:57:45Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Davion Mitchell (MIA) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Peyton Watson (CLE) UNDER 1.5 Blocks | -227 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Nikola Jokic (DEN) UNDER 1.5 Steals | -209 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |
| Josh Giddey (CHI) UNDER 1.5 3-pointers made | -185 (DraftKings via ESPN) | 1.5 | 61% | 61% | -0.06 |

**Combined probability 16.6%; parlay pays 4.7x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Davion Mitchell (MIA) UNDER 1.5 Steals (66%); Peyton Watson (CLE) UNDER 1.5 Blocks (65%); Nikola Jokic (DEN) UNDER 1.5 Steals (63%). Combined probability 27.2%; parlay pays 3.0x; expected profit per 1 staked -0.18.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) UNDER 3.5 Assists | +109 (DraftKings via ESPN) | 2.9 | 65% | 45% | +0.36 |
| Giannis Antetokounmpo (MIA) UNDER 28.5 Points | -107 (DraftKings via ESPN) | 24.4 | 69% | 49% | +0.33 |

Combined probability 44.6%; parlay pays 4.0x; expected profit per 1 staked +0.80.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) UNDER 3.5 Assists | +109 (DraftKings via ESPN) | 2.9 | 65% | 45% | +0.36 |
| Giannis Antetokounmpo (MIA) UNDER 28.5 Points | -107 (DraftKings via ESPN) | 24.4 | 69% | 49% | +0.33 |
| James Harden (CLE) OVER 6.5 Assists | +114 (DraftKings via ESPN) | 7.5 | 61% | 44% | +0.31 |

Combined probability 27.4%; parlay pays 8.7x; expected profit per 1 staked +1.37.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Day'Ron Sharpe (BKN) UNDER 3.5 Assists | +109 (DraftKings via ESPN) | 2.9 | 65% | 45% | +0.36 |
| Giannis Antetokounmpo (MIA) UNDER 28.5 Points | -107 (DraftKings via ESPN) | 24.4 | 69% | 49% | +0.33 |
| James Harden (CLE) OVER 6.5 Assists | +114 (DraftKings via ESPN) | 7.5 | 61% | 44% | +0.31 |
| LaMelo Ball (MIN) UNDER 4.5 Rebounds | -133 (DraftKings via ESPN) | 3.5 | 68% | 53% | +0.20 |

Combined probability 18.8%; parlay pays 15.2x; expected profit per 1 staked +1.84.

Top single picks by model edge:

- Day'Ron Sharpe (BKN) UNDER 3.5 Assists: model 65% vs book 45%, EV +0.36 at +109 (projection 2.9)
- Michael Porter Jr. (BKN) UNDER 22.5 Points: model 72% vs book 51%, EV +0.33 at -116 (projection 18.7)
- Giannis Antetokounmpo (MIA) UNDER 28.5 Points: model 69% vs book 49%, EV +0.33 at -107 (projection 24.4)
- James Harden (CLE) OVER 6.5 Assists: model 61% vs book 44%, EV +0.31 at +114 (projection 7.5)
- Davion Mitchell (MIA) OVER 2.5 Rebounds: model 58% vs book 41%, EV +0.31 at +126 (projection 2.9)
- Davion Mitchell (MIA) UNDER 8.5 Assists: model 75% vs book 55%, EV +0.29 at -139 (projection 6.5)
- Julius Randle (BKN) UNDER 20.5 Points: model 70% vs book 51%, EV +0.28 at -120 (projection 17.1)
- Giannis Antetokounmpo (MIA) UNDER 5.5 Assists: model 70% vs book 52%, EV +0.27 at -124 (projection 4.3)
- P.J. Washington (DAL) UNDER 1.5 3-pointers made: model 54% vs book 40%, EV +0.26 at +134 (projection 1.5)
- Cameron Boozer (MEM) UNDER 17.5 Points: model 68% vs book 51%, EV +0.24 at -120 (projection 14.8)
- Zaccharie Risacher (DAL) OVER 3.5 Rebounds: model 56% vs book 43%, EV +0.23 at +120 (projection 4.0)
- Davion Mitchell (MIA) UNDER 1.5 3-pointers made: model 52% vs book 40%, EV +0.22 at +134 (projection 1.6)

## DEN at NOP (game 401909980)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nikola Jokic (DEN) UNDER 1.5 Steals | -209 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |
| Aaron Gordon (DEN) UNDER 1.5 3-pointers made | -207 (DraftKings via ESPN) | 1.5 | 63% | 63% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 Steals | -207 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 25.3%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Nikola Jokic (DEN) UNDER 1.5 Steals: 63%, EV -0.06 at -209
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -207
- Herbert Jones (NOP) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Cameron Johnson (DEN) OVER 1.5 Assists: 62%, EV -0.06 at -191
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Jeremiah Fears (NOP) UNDER 1.5 Steals: 60%, EV -0.07 at -177
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Zion Williamson (NOP) UNDER 3.5 Assists: 58%, EV -0.06 at -165

## DAL at CLE (game 401909981)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Peyton Watson (CLE) UNDER 1.5 Blocks | -227 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Kyrie Irving (DAL) UNDER 1.5 Steals | -214 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| James Harden (CLE) UNDER 1.5 Steals | -210 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |

Combined probability 26.3%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Peyton Watson (CLE) UNDER 1.5 Blocks: 65%, EV -0.06 at -227
- Kyrie Irving (DAL) UNDER 1.5 Steals: 64%, EV -0.06 at -214
- James Harden (CLE) UNDER 1.5 Steals: 63%, EV -0.06 at -210
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 62%, EV -0.06 at -196
- P.J. Washington (DAL) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Peyton Watson (CLE) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -175
- Naji Marshall (DAL) OVER 2.5 Assists: 59%, EV -0.06 at -173
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -172

## DET at MIA (game 401909982)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Davion Mitchell (MIA) UNDER 1.5 Steals | -239 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Cade Cunningham (DET) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |
| Bam Adebayo (MIA) OVER 0.5 3-pointers made | -213 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |

Combined probability 27.0%; parlay pays 3.1x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Davion Mitchell (MIA) UNDER 1.5 Steals: 66%, EV -0.06 at -239
- Cade Cunningham (DET) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- Bam Adebayo (MIA) OVER 0.5 3-pointers made: 64%, EV -0.06 at -213
- Davion Mitchell (MIA) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Bam Adebayo (MIA) UNDER 1.5 Steals: 60%, EV -0.06 at -178
- Duncan Robinson (DET) UNDER 2.5 Assists: 59%, EV -0.06 at -174
- Davion Mitchell (MIA) UNDER 2.5 Rebounds: 59%, EV -0.06 at -166
- John Collins (DET) OVER 5.5 Rebounds: 56%, EV -0.06 at -152

## BKN at MEM (game 401909983)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Michael Porter Jr. (BKN) UNDER 2.5 Assists | -183 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| Jaylen Wells (MEM) UNDER 1.5 Assists | -170 (DraftKings via ESPN) | 1.4 | 59% | 59% | -0.06 |
| Ty Jerome (MEM) UNDER 2.5 3-pointers made | -166 (DraftKings via ESPN) | 2.4 | 59% | 59% | -0.06 |

Combined probability 20.9%; parlay pays 3.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Michael Porter Jr. (BKN) UNDER 2.5 Assists: 61%, EV -0.06 at -183
- Jaylen Wells (MEM) UNDER 1.5 Assists: 59%, EV -0.06 at -170
- Ty Jerome (MEM) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -166
- Jerami Grant (MEM) UNDER 2.5 Rebounds: 58%, EV -0.06 at -165
- Jerami Grant (MEM) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Cedric Coward (MEM) OVER 2.5 Assists: 57%, EV -0.06 at -158
- Julius Randle (BKN) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -155
- Ty Jerome (MEM) OVER 2.5 Rebounds: 57%, EV -0.06 at -154

## CHI at MIN (game 401909984)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Giddey (CHI) UNDER 1.5 3-pointers made | -185 (DraftKings via ESPN) | 1.5 | 61% | 61% | -0.06 |
| Jonathan Kuminga (MIN) UNDER 1.5 3-pointers made | -182 (DraftKings via ESPN) | 1.6 | 60% | 60% | -0.06 |
| Matas Buzelis (CHI) UNDER 2.5 3-pointers made | -179 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |

Combined probability 22.1%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Josh Giddey (CHI) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Jonathan Kuminga (MIN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -182
- Matas Buzelis (CHI) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -179
- LaMelo Ball (MIN) UNDER 1.5 Steals: 59%, EV -0.06 at -172
- Rudy Gobert (MIN) UNDER 1.5 Blocks: 59%, EV -0.06 at -170
- Ayo Dosunmu (MIN) OVER 3.5 Assists: 57%, EV -0.06 at -153
- Jaden McDaniels (MIN) UNDER 3.5 Assists: 56%, EV -0.06 at -152
- Jaden McDaniels (MIN) UNDER 6.5 Rebounds: 56%, EV -0.06 at -146
