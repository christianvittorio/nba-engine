# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-14T15:37:59Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |
| Nikola Jokic (DEN) UNDER 1.5 Steals | -210 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |
| Matas Buzelis (CHI) OVER 1.5 3-pointers made | -188 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |

**Combined probability 16.5%; parlay pays 4.7x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Bam Adebayo (MIA) UNDER 1.5 3-pointers made (66%); Donovan Mitchell (CLE) UNDER 1.5 Steals (64%); Nikola Jokic (DEN) UNDER 1.5 Steals (63%). Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.18.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nolan Traore (BKN) UNDER 3.5 Assists | +125 (DraftKings via ESPN) | 2.6 | 62% | 42% | +0.41 |
| Davion Mitchell (MIA) UNDER 7.5 Assists | +110 (DraftKings via ESPN) | 6.5 | 64% | 45% | +0.35 |

Combined probability 40.1%; parlay pays 4.7x; expected profit per 1 staked +0.90.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nolan Traore (BKN) UNDER 3.5 Assists | +125 (DraftKings via ESPN) | 2.6 | 62% | 42% | +0.41 |
| Davion Mitchell (MIA) UNDER 7.5 Assists | +110 (DraftKings via ESPN) | 6.5 | 64% | 45% | +0.35 |
| P.J. Washington (DAL) UNDER 1.5 3-pointers made | +137 (DraftKings via ESPN) | 1.6 | 54% | 40% | +0.27 |

Combined probability 21.5%; parlay pays 11.2x; expected profit per 1 staked +1.41.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nolan Traore (BKN) UNDER 3.5 Assists | +125 (DraftKings via ESPN) | 2.6 | 62% | 42% | +0.41 |
| Davion Mitchell (MIA) UNDER 7.5 Assists | +110 (DraftKings via ESPN) | 6.5 | 64% | 45% | +0.35 |
| P.J. Washington (DAL) UNDER 1.5 3-pointers made | +137 (DraftKings via ESPN) | 1.6 | 54% | 40% | +0.27 |
| LaMelo Ball (MIN) UNDER 4.5 Rebounds | -122 (DraftKings via ESPN) | 3.5 | 69% | 51% | +0.25 |

Combined probability 14.8%; parlay pays 20.4x; expected profit per 1 staked +2.03.

Top single picks by model edge:

- Nolan Traore (BKN) UNDER 3.5 Assists: model 62% vs book 42%, EV +0.41 at +125 (projection 2.6)
- Julius Randle (BKN) UNDER 21.5 Points: model 75% vs book 51%, EV +0.39 at -116 (projection 17.1)
- Davion Mitchell (MIA) UNDER 7.5 Assists: model 64% vs book 45%, EV +0.35 at +110 (projection 6.5)
- Nolan Traore (BKN) UNDER 12.5 Points: model 70% vs book 50%, EV +0.32 at -111 (projection 8.8)
- Cameron Boozer (MEM) UNDER 17.5 Points: model 68% vs book 50%, EV +0.28 at -112 (projection 14.8)
- Julius Randle (BKN) UNDER 4.5 Assists: model 61% vs book 45%, EV +0.28 at +110 (projection 4.0)
- Giannis Antetokounmpo (MIA) UNDER 28.5 Points: model 69% vs book 51%, EV +0.28 at -115 (projection 24.4)
- Davion Mitchell (MIA) UNDER 14.5 Points: model 69% vs book 51%, EV +0.28 at -116 (projection 12.3)
- Davion Mitchell (MIA) OVER 2.5 Rebounds: model 58% vs book 43%, EV +0.28 at +120 (projection 2.9)
- P.J. Washington (DAL) UNDER 1.5 3-pointers made: model 54% vs book 40%, EV +0.27 at +137 (projection 1.6)
- LaMelo Ball (MIN) UNDER 4.5 Rebounds: model 69% vs book 51%, EV +0.25 at -122 (projection 3.5)
- Giannis Antetokounmpo (MIA) UNDER 11.5 Rebounds: model 61% vs book 46%, EV +0.24 at +105 (projection 10.1)

## DEN at NOP (game 401909980)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nikola Jokic (DEN) UNDER 1.5 Steals | -210 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |
| Aaron Gordon (DEN) UNDER 1.5 3-pointers made | -207 (DraftKings via ESPN) | 1.5 | 63% | 63% | -0.06 |
| Herbert Jones (NOP) UNDER 1.5 3-pointers made | -183 (DraftKings via ESPN) | 1.3 | 61% | 61% | -0.06 |

Combined probability 24.3%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Nikola Jokic (DEN) UNDER 1.5 Steals: 63%, EV -0.06 at -210
- Aaron Gordon (DEN) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -207
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -183
- Cameron Johnson (DEN) OVER 1.5 Assists: 60%, EV -0.06 at -176
- Cameron Johnson (DEN) OVER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Christian Braun (DEN) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Herbert Jones (NOP) UNDER 3.5 Rebounds: 58%, EV -0.06 at -159
- Nikola Jokic (DEN) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -158

## DAL at CLE (game 401909981)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Mitchell (CLE) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 1.3 | 64% | 64% | -0.06 |
| Peyton Watson (CLE) UNDER 2.5 Assists | -184 (DraftKings via ESPN) | 2.4 | 61% | 61% | -0.06 |
| P.J. Washington (DAL) OVER 1.5 3-pointers made | -181 (DraftKings via ESPN) | 1.6 | 60% | 60% | -0.06 |

Combined probability 23.5%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Donovan Mitchell (CLE) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- Peyton Watson (CLE) UNDER 2.5 Assists: 61%, EV -0.06 at -184
- P.J. Washington (DAL) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Kyrie Irving (DAL) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -168
- Peyton Watson (CLE) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -161
- Naji Marshall (DAL) UNDER 3.5 Rebounds: 58%, EV -0.06 at -160
- Meleek Thomas (CLE) UNDER 3.5 Rebounds: 57%, EV -0.06 at -156
- P.J. Washington (DAL) UNDER 1.5 Assists: 57%, EV -0.06 at -155

## DET at MIA (game 401909982)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -240 (DraftKings via ESPN) | 1.4 | 66% | 66% | -0.06 |
| Davion Mitchell (MIA) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Cade Cunningham (DET) UNDER 1.5 Steals | -207 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |

Combined probability 27.5%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -240
- Davion Mitchell (MIA) OVER 0.5 Steals: 66%, EV -0.06 at -233
- Cade Cunningham (DET) UNDER 1.5 Steals: 63%, EV -0.06 at -207
- Davion Mitchell (MIA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -187
- Bam Adebayo (MIA) UNDER 1.5 Steals: 61%, EV -0.06 at -185
- Duncan Robinson (DET) UNDER 2.5 Assists: 59%, EV -0.06 at -167
- Davion Mitchell (MIA) UNDER 2.5 Rebounds: 57%, EV -0.06 at -159
- Pelle Larsson (MIA) UNDER 3.5 Assists: 57%, EV -0.06 at -153

## BKN at MEM (game 401909983)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Michael Porter Jr. (BKN) UNDER 2.5 Assists | -186 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| Jaylen Wells (MEM) UNDER 1.5 Assists | -170 (DraftKings via ESPN) | 1.4 | 59% | 59% | -0.06 |
| Nolan Traore (BKN) OVER 3.5 Assists | -165 (DraftKings via ESPN) | 2.6 | 58% | 58% | -0.06 |

Combined probability 21.0%; parlay pays 3.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Michael Porter Jr. (BKN) UNDER 2.5 Assists: 61%, EV -0.06 at -186
- Jaylen Wells (MEM) UNDER 1.5 Assists: 59%, EV -0.06 at -170
- Nolan Traore (BKN) OVER 3.5 Assists: 58%, EV -0.06 at -165
- Ty Jerome (MEM) OVER 2.5 Rebounds: 58%, EV -0.06 at -162
- Jerami Grant (MEM) UNDER 2.5 Rebounds: 58%, EV -0.06 at -160
- Cedric Coward (MEM) OVER 2.5 Assists: 58%, EV -0.06 at -159
- Jerami Grant (MEM) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -155
- Day'Ron Sharpe (BKN) UNDER 4.5 Assists: 57%, EV -0.06 at -154

## CHI at MIN (game 401909984)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Matas Buzelis (CHI) OVER 1.5 3-pointers made | -188 (DraftKings via ESPN) | 1.9 | 61% | 61% | -0.06 |
| Jonathan Kuminga (MIN) UNDER 1.5 3-pointers made | -181 (DraftKings via ESPN) | 1.6 | 60% | 60% | -0.06 |
| Josh Giddey (CHI) UNDER 1.5 3-pointers made | -173 (DraftKings via ESPN) | 1.5 | 59% | 59% | -0.06 |

Combined probability 22.0%; parlay pays 3.8x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Matas Buzelis (CHI) OVER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Jonathan Kuminga (MIN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Josh Giddey (CHI) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -173
- Ayo Dosunmu (MIN) UNDER 4.5 Assists: 58%, EV -0.06 at -164
- Jaden McDaniels (MIN) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -153
- Jaden McDaniels (MIN) UNDER 6.5 Rebounds: 57%, EV -0.06 at -152
- Matas Buzelis (CHI) UNDER 5.5 Rebounds: 56%, EV -0.06 at -150
- LaMelo Ball (MIN) OVER 6.5 Assists: 56%, EV -0.06 at -147
