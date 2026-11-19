# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-19T21:59:10Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -230 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Mikal Bridges (NYK) UNDER 1.5 3-pointers made | -225 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Donovan Clingan (POR) OVER 1.5 Blocks | -177 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.07 |

**Combined probability 16.6%; parlay pays 4.6x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Cedric Coward (MEM) OVER 0.5 Steals (66%); De'Aaron Fox (SAS) UNDER 1.5 Steals (65%); Mikal Bridges (NYK) UNDER 1.5 3-pointers made (65%). Combined probability 27.9%; parlay pays 3.0x; expected profit per 1 staked -0.18.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kel'el Ware (MIL) UNDER 7.5 Rebounds | +106 (DraftKings via ESPN) | 6.0 | 67% | 45% | +0.37 |
| LaMelo Ball (MIN) UNDER 5.5 Assists | +109 (DraftKings via ESPN) | 5.0 | 59% | 45% | +0.24 |

Combined probability 39.6%; parlay pays 4.3x; expected profit per 1 staked +0.70.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kel'el Ware (MIL) UNDER 7.5 Rebounds | +106 (DraftKings via ESPN) | 6.0 | 67% | 45% | +0.37 |
| LaMelo Ball (MIN) UNDER 5.5 Assists | +109 (DraftKings via ESPN) | 5.0 | 59% | 45% | +0.24 |
| Jaylen Wells (MEM) OVER 10.5 Points | -102 (DraftKings via ESPN) | 13.0 | 61% | 48% | +0.20 |

Combined probability 24.0%; parlay pays 8.5x; expected profit per 1 staked +1.05.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kel'el Ware (MIL) UNDER 7.5 Rebounds | +106 (DraftKings via ESPN) | 6.0 | 67% | 45% | +0.37 |
| LaMelo Ball (MIN) UNDER 5.5 Assists | +109 (DraftKings via ESPN) | 5.0 | 59% | 45% | +0.24 |
| Jaylen Wells (MEM) OVER 10.5 Points | -102 (DraftKings via ESPN) | 13.0 | 61% | 48% | +0.20 |
| Julian Champagnie (SAS) UNDER 2.5 3-pointers made | +103 (DraftKings via ESPN) | 2.3 | 57% | 46% | +0.15 |

Combined probability 13.7%; parlay pays 17.3x; expected profit per 1 staked +1.36.

Top single picks by model edge:

- Kel'el Ware (MIL) UNDER 7.5 Rebounds: model 67% vs book 45%, EV +0.37 at +106 (projection 6.0)
- LaMelo Ball (MIN) UNDER 5.5 Assists: model 59% vs book 45%, EV +0.24 at +109 (projection 5.0)
- Nate Ament (MIL) UNDER 3.5 Rebounds: model 68% vs book 52%, EV +0.22 at -124 (projection 2.6)
- Jaylen Wells (MEM) OVER 10.5 Points: model 61% vs book 48%, EV +0.20 at -102 (projection 13.0)
- LaMelo Ball (MIN) UNDER 19.5 Points: model 64% vs book 51%, EV +0.19 at -118 (projection 17.2)
- Jalen Brunson (NYK) UNDER 2.5 3-pointers made: model 62% vs book 49%, EV +0.18 at -112 (projection 2.1)
- Jerami Grant (MEM) OVER 10.5 Points: model 65% vs book 52%, EV +0.17 at -123 (projection 11.7)
- Deni Avdija (POR) OVER 5.5 Assists: model 64% vs book 51%, EV +0.17 at -120 (projection 6.0)
- Nate Ament (MIL) UNDER 8.5 Points: model 60% vs book 48%, EV +0.17 at -104 (projection 8.0)
- Tyler Herro (MIL) UNDER 20.5 Points: model 59% vs book 48%, EV +0.17 at -104 (projection 16.4)
- Charles Bassey (GSW) UNDER 7.5 Rebounds: model 67% vs book 54%, EV +0.16 at -137 (projection 6.0)
- Cedric Coward (MEM) OVER 15.5 Points: model 58% vs book 48%, EV +0.15 at -102 (projection 17.5)

## GSW at MEM (game 401910019)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Brandin Podziemski (GSW) UNDER 1.5 Steals | -218 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Cam Spencer (MEM) OVER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 2.2 | 62% | 62% | -0.06 |

Combined probability 26.1%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Cedric Coward (MEM) OVER 0.5 Steals: 66%, EV -0.06 at -233
- Brandin Podziemski (GSW) UNDER 1.5 Steals: 64%, EV -0.06 at -218
- Cam Spencer (MEM) OVER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Yaxel Lendeborg (GSW) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -190
- Cedric Coward (MEM) OVER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Will Richard (GSW) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -184
- Cameron Boozer (MEM) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Gui Santos (GSW) UNDER 2.5 Assists: 59%, EV -0.06 at -171

## POR at MIL (game 401910020)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Donovan Clingan (POR) OVER 1.5 Blocks | -177 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.07 |
| Sidy Cissoko (POR) OVER 1.5 Assists | -173 (DraftKings via ESPN) | 2.4 | 59% | 59% | -0.06 |
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -173 (DraftKings via ESPN) | 1.5 | 59% | 59% | -0.06 |

Combined probability 21.1%; parlay pays 3.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Donovan Clingan (POR) OVER 1.5 Blocks: 60%, EV -0.07 at -177
- Sidy Cissoko (POR) OVER 1.5 Assists: 59%, EV -0.06 at -173
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -173
- Jrue Holiday (POR) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -165
- Jrue Holiday (POR) OVER 3.5 Rebounds: 58%, EV -0.06 at -159
- Deni Avdija (POR) OVER 1.5 3-pointers made: 57%, EV -0.06 at -157
- Tyler Herro (MIL) UNDER 4.5 Assists: 57%, EV -0.06 at -156
- Tyler Herro (MIL) UNDER 4.5 Rebounds: 57%, EV -0.06 at -154

## NYK at MIN (game 401910021)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) UNDER 1.5 3-pointers made | -225 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Josh Hart (NYK) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| Jonathan Kuminga (MIN) UNDER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 1.2 | 61% | 61% | -0.06 |

Combined probability 25.5%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -225
- Josh Hart (NYK) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- Jonathan Kuminga (MIN) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Rudy Gobert (MIN) UNDER 1.5 Blocks: 61%, EV -0.06 at -190
- OG Anunoby (NYK) UNDER 1.5 Steals: 61%, EV -0.06 at -188
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -187
- Ayo Dosunmu (MIN) OVER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Mikal Bridges (NYK) OVER 2.5 Rebounds: 60%, EV -0.06 at -176

## LAC at SAS (game 401910022)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -230 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Victor Wembanyama (SAS) OVER 0.5 Steals | -228 (DraftKings via ESPN) | 1.1 | 65% | 65% | -0.06 |
| Rui Hachimura (LAC) UNDER 1.5 Assists | -203 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |

Combined probability 26.7%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- De'Aaron Fox (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -230
- Victor Wembanyama (SAS) OVER 0.5 Steals: 65%, EV -0.06 at -228
- Rui Hachimura (LAC) UNDER 1.5 Assists: 63%, EV -0.06 at -203
- Keaton Wagler (LAC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -199
- Victor Wembanyama (SAS) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -185
- Kris Dunn (LAC) UNDER 3.5 Rebounds: 60%, EV -0.06 at -176
- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 60%, EV -0.06 at -174
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -173
