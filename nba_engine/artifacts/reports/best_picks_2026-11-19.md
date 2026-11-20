# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-20T02:53:03Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Brunson (NYK) UNDER 0.5 Blocks | -358 (DraftKings via ESPN) | 0.2 | 74% | 74% | -0.06 |
| Brandin Podziemski (GSW) UNDER 1.5 Steals | -245 (DraftKings via ESPN) | 1.0 | 67% | 67% | -0.06 |
| Victor Wembanyama (SAS) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -200 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |

**Combined probability 20.2%; parlay pays 3.8x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Jalen Brunson (NYK) UNDER 0.5 Blocks (74%); Brandin Podziemski (GSW) UNDER 1.5 Steals (67%); Victor Wembanyama (SAS) OVER 0.5 Steals (66%). Combined probability 32.3%; parlay pays 2.6x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kel'el Ware (MIL) UNDER 11.5 Points | +100 (DraftKings via ESPN) | 9.3 | 70% | 47% | +0.40 |
| Karl-Anthony Towns (NYK) UNDER 0.5 Blocks | +109 (DraftKings via ESPN) | 0.4 | 64% | 45% | +0.33 |

Combined probability 44.6%; parlay pays 4.2x; expected profit per 1 staked +0.86.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kel'el Ware (MIL) UNDER 11.5 Points | +100 (DraftKings via ESPN) | 9.3 | 70% | 47% | +0.40 |
| Karl-Anthony Towns (NYK) UNDER 0.5 Blocks | +109 (DraftKings via ESPN) | 0.4 | 64% | 45% | +0.33 |
| Taylor Hendricks (MEM) UNDER 10.5 Points | -112 (DraftKings via ESPN) | 9.1 | 64% | 50% | +0.22 |

Combined probability 28.6%; parlay pays 7.9x; expected profit per 1 staked +1.26.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kel'el Ware (MIL) UNDER 11.5 Points | +100 (DraftKings via ESPN) | 9.3 | 70% | 47% | +0.40 |
| Karl-Anthony Towns (NYK) UNDER 0.5 Blocks | +109 (DraftKings via ESPN) | 0.4 | 64% | 45% | +0.33 |
| Taylor Hendricks (MEM) UNDER 10.5 Points | -112 (DraftKings via ESPN) | 9.1 | 64% | 50% | +0.22 |
| Kris Dunn (LAC) OVER 2.5 Rebounds | -122 (DraftKings via ESPN) | 3.2 | 62% | 51% | +0.13 |

Combined probability 17.8%; parlay pays 14.4x; expected profit per 1 staked +1.57.

Top single picks by model edge:

- Kel'el Ware (MIL) UNDER 11.5 Points: model 70% vs book 47%, EV +0.40 at +100 (projection 9.3)
- Karl-Anthony Towns (NYK) UNDER 0.5 Blocks: model 64% vs book 45%, EV +0.33 at +109 (projection 0.4)
- Nate Ament (MIL) UNDER 3.5 Rebounds: model 69% vs book 49%, EV +0.31 at -112 (projection 2.6)
- Jrue Holiday (POR) OVER 2.5 3-pointers made: model 57% vs book 43%, EV +0.25 at +117 (projection 3.0)
- Taylor Hendricks (MEM) UNDER 10.5 Points: model 64% vs book 50%, EV +0.22 at -112 (projection 9.1)
- Toumani Camara (POR) OVER 2.5 3-pointers made: model 61% vs book 47%, EV +0.21 at +100 (projection 3.1)
- Jaylen Wells (MEM) OVER 10.5 Points: model 61% vs book 48%, EV +0.20 at -102 (projection 13.0)
- Rudy Gobert (MIN) UNDER 0.5 Steals: model 64% vs book 50%, EV +0.20 at -114 (projection 0.5)
- Scoot Henderson (POR) OVER 2.5 Assists: model 56% vs book 44%, EV +0.19 at +112 (projection 3.0)
- Jerami Grant (MEM) OVER 10.5 Points: model 65% vs book 52%, EV +0.18 at -121 (projection 11.7)
- Charles Bassey (GSW) UNDER 6.5 Rebounds: model 57% vs book 45%, EV +0.18 at +108 (projection 6.0)
- LaMelo Ball (MIN) UNDER 5.5 Assists: model 59% vs book 47%, EV +0.17 at -102 (projection 5.0)

## GSW at MEM (game 401910019)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brandin Podziemski (GSW) UNDER 1.5 Steals | -245 (DraftKings via ESPN) | 1.0 | 67% | 67% | -0.06 |
| Cedric Coward (MEM) OVER 0.5 Steals | -232 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Will Richard (GSW) OVER 0.5 3-pointers made | -229 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |

Combined probability 28.5%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Brandin Podziemski (GSW) UNDER 1.5 Steals: 67%, EV -0.06 at -245
- Cedric Coward (MEM) OVER 0.5 Steals: 66%, EV -0.06 at -232
- Will Richard (GSW) OVER 0.5 3-pointers made: 65%, EV -0.06 at -229
- Cam Spencer (MEM) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -193
- Cedric Coward (MEM) OVER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Jerami Grant (MEM) UNDER 2.5 Rebounds: 61%, EV -0.06 at -182
- De'Anthony Melton (GSW) OVER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Gui Santos (GSW) UNDER 2.5 Assists: 60%, EV -0.06 at -175

## POR at MIL (game 401910020)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -200 (DraftKings via ESPN) | 1.4 | 62% | 62% | -0.06 |
| Sidy Cissoko (POR) UNDER 2.5 Assists | -194 (DraftKings via ESPN) | 2.6 | 62% | 62% | -0.06 |
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -185 (DraftKings via ESPN) | 1.5 | 61% | 61% | -0.06 |

Combined probability 23.6%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -200
- Sidy Cissoko (POR) UNDER 2.5 Assists: 62%, EV -0.06 at -194
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Donovan Clingan (POR) OVER 1.5 Blocks: 60%, EV -0.06 at -175
- Tyler Herro (MIL) OVER 3.5 Rebounds: 59%, EV -0.06 at -167
- Jaime Jaquez Jr. (MIL) OVER 2.5 Assists: 58%, EV -0.06 at -163
- Scoot Henderson (POR) UNDER 2.5 Rebounds: 58%, EV -0.06 at -163
- Kel'el Ware (MIL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -161

## NYK at MIN (game 401910021)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jalen Brunson (NYK) UNDER 0.5 Blocks | -358 (DraftKings via ESPN) | 0.2 | 74% | 74% | -0.06 |
| Josh Hart (NYK) UNDER 0.5 Blocks | -266 (DraftKings via ESPN) | 0.2 | 68% | 68% | -0.06 |
| Ayo Dosunmu (MIN) UNDER 0.5 Blocks | -237 (DraftKings via ESPN) | 0.3 | 66% | 66% | -0.06 |

Combined probability 33.2%; parlay pays 2.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jalen Brunson (NYK) UNDER 0.5 Blocks: 74%, EV -0.06 at -358
- Josh Hart (NYK) UNDER 0.5 Blocks: 68%, EV -0.06 at -266
- Ayo Dosunmu (MIN) UNDER 0.5 Blocks: 66%, EV -0.06 at -237
- Rudy Gobert (MIN) UNDER 1.5 Blocks: 66%, EV -0.06 at -234
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -230
- Josh Hart (NYK) UNDER 1.5 Steals: 65%, EV -0.06 at -229
- Jaden McDaniels (MIN) OVER 0.5 Steals: 64%, EV -0.06 at -216
- Josh Hart (NYK) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -204

## LAC at SAS (game 401910022)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made | -234 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -230 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |

Combined probability 28.3%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Victor Wembanyama (SAS) OVER 0.5 Steals: 66%, EV -0.06 at -236
- Derrick Jones Jr. (LAC) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -234
- De'Aaron Fox (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -230
- Kris Dunn (LAC) UNDER 1.5 Steals: 65%, EV -0.06 at -222
- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 62%, EV -0.06 at -195
- Rui Hachimura (LAC) UNDER 1.5 Assists: 61%, EV -0.06 at -183
- Darius Garland (LAC) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -181
- Victor Wembanyama (SAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -178
