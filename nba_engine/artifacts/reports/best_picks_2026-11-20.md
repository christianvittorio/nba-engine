# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-19T18:00:49Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) UNDER 1.5 Steals | -238 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Victor Wembanyama (SAS) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Mikal Bridges (NYK) UNDER 1.5 3-pointers made | -233 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -209 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |

**Combined probability 18.1%; parlay pays 4.3x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Cedric Coward (MEM) UNDER 1.5 Steals (66%); Victor Wembanyama (SAS) OVER 0.5 Steals (66%); Mikal Bridges (NYK) UNDER 1.5 3-pointers made (66%). Combined probability 28.6%; parlay pays 2.9x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Myles Turner (MIL) UNDER 1.5 3-pointers made | +100 (DraftKings via ESPN) | 1.1 | 63% | 47% | +0.27 |
| Cedric Coward (MEM) OVER 14.5 Points | -109 (DraftKings via ESPN) | 17.4 | 64% | 49% | +0.22 |

Combined probability 40.3%; parlay pays 3.8x; expected profit per 1 staked +0.55.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Myles Turner (MIL) UNDER 1.5 3-pointers made | +100 (DraftKings via ESPN) | 1.1 | 63% | 47% | +0.27 |
| Cedric Coward (MEM) OVER 14.5 Points | -109 (DraftKings via ESPN) | 17.4 | 64% | 49% | +0.22 |
| LaMelo Ball (MIN) UNDER 5.5 Assists | -101 (DraftKings via ESPN) | 5.0 | 59% | 47% | +0.18 |

Combined probability 23.9%; parlay pays 7.6x; expected profit per 1 staked +0.82.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Myles Turner (MIL) UNDER 1.5 3-pointers made | +100 (DraftKings via ESPN) | 1.1 | 63% | 47% | +0.27 |
| Cedric Coward (MEM) OVER 14.5 Points | -109 (DraftKings via ESPN) | 17.4 | 64% | 49% | +0.22 |
| LaMelo Ball (MIN) UNDER 5.5 Assists | -101 (DraftKings via ESPN) | 5.0 | 59% | 47% | +0.18 |
| Julian Champagnie (SAS) UNDER 2.5 3-pointers made | +104 (DraftKings via ESPN) | 2.3 | 57% | 46% | +0.16 |

Combined probability 13.6%; parlay pays 15.6x; expected profit per 1 staked +1.11.

Top single picks by model edge:

- Myles Turner (MIL) UNDER 1.5 3-pointers made: model 63% vs book 47%, EV +0.27 at +100 (projection 1.1)
- Myles Turner (MIL) UNDER 1.5 Assists: model 53% vs book 39%, EV +0.26 at +138 (projection 1.4)
- Cedric Coward (MEM) OVER 14.5 Points: model 64% vs book 49%, EV +0.22 at -109 (projection 17.4)
- Tyler Herro (MIL) UNDER 3.5 Assists: model 56% vs book 43%, EV +0.21 at +116 (projection 2.8)
- LaMelo Ball (MIN) UNDER 5.5 Assists: model 59% vs book 47%, EV +0.18 at -101 (projection 5.0)
- LaMelo Ball (MIN) UNDER 19.5 Points: model 64% vs book 52%, EV +0.17 at -122 (projection 17.2)
- Deni Avdija (POR) OVER 5.5 Assists: model 63% vs book 51%, EV +0.16 at -119 (projection 5.9)
- Julian Champagnie (SAS) UNDER 2.5 3-pointers made: model 57% vs book 46%, EV +0.16 at +104 (projection 2.3)
- Brayden Burries (MIL) UNDER 2.5 Assists: model 64% vs book 51%, EV +0.16 at -122 (projection 2.1)
- Yaxel Lendeborg (GSW) UNDER 4.5 Assists: model 64% vs book 52%, EV +0.15 at -126 (projection 3.9)
- Jalen Brunson (NYK) UNDER 2.5 3-pointers made: model 62% vs book 51%, EV +0.15 at -118 (projection 2.1)
- Kyle Kuzma (MIL) UNDER 1.5 3-pointers made: model 62% vs book 51%, EV +0.15 at -119 (projection 1.3)

## GSW at MEM (game 401910019)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Cedric Coward (MEM) UNDER 1.5 Steals | -238 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Brandin Podziemski (GSW) UNDER 1.5 Steals | -223 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Gui Santos (GSW) UNDER 2.5 Assists | -181 (DraftKings via ESPN) | 2.3 | 60% | 60% | -0.06 |

Combined probability 25.8%; parlay pays 3.2x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Cedric Coward (MEM) UNDER 1.5 Steals: 66%, EV -0.06 at -238
- Brandin Podziemski (GSW) UNDER 1.5 Steals: 65%, EV -0.06 at -223
- Gui Santos (GSW) UNDER 2.5 Assists: 60%, EV -0.06 at -181
- Yaxel Lendeborg (GSW) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Cedric Coward (MEM) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Cameron Boozer (MEM) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Gui Santos (GSW) OVER 3.5 Rebounds: 58%, EV -0.06 at -159
- Brandin Podziemski (GSW) UNDER 4.5 Assists: 57%, EV -0.06 at -153

## POR at MIL (game 401910020)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made | -209 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -197 (DraftKings via ESPN) | 1.1 | 62% | 62% | -0.06 |
| Myles Turner (MIL) OVER 1.5 Assists | -183 (DraftKings via ESPN) | 1.4 | 61% | 61% | -0.06 |

Combined probability 24.0%; parlay pays 3.4x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -209
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -197
- Myles Turner (MIL) OVER 1.5 Assists: 61%, EV -0.06 at -183
- Donovan Clingan (POR) OVER 1.5 Blocks: 60%, EV -0.06 at -177
- Deni Avdija (POR) OVER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Sidy Cissoko (POR) OVER 1.5 Assists: 58%, EV -0.06 at -164
- Jrue Holiday (POR) OVER 3.5 Rebounds: 58%, EV -0.06 at -163
- Sidy Cissoko (POR) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -160

## NYK at MIN (game 401910021)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) UNDER 1.5 3-pointers made | -233 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Josh Hart (NYK) UNDER 1.5 Steals | -215 (DraftKings via ESPN) | 1.0 | 64% | 64% | -0.06 |
| OG Anunoby (NYK) UNDER 2.5 3-pointers made | -194 (DraftKings via ESPN) | 1.9 | 62% | 62% | -0.06 |

Combined probability 26.0%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 66%, EV -0.06 at -233
- Josh Hart (NYK) UNDER 1.5 Steals: 64%, EV -0.06 at -215
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -194
- Rudy Gobert (MIN) UNDER 1.5 Blocks: 61%, EV -0.06 at -190
- OG Anunoby (NYK) UNDER 1.5 Steals: 60%, EV -0.06 at -182
- Josh Hart (NYK) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Ayo Dosunmu (MIN) OVER 1.5 3-pointers made: 60%, EV -0.06 at -179
- Jonathan Kuminga (MIN) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178

## LAC at SAS (game 401910022)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| De'Aaron Fox (SAS) UNDER 1.5 Steals | -230 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Keaton Wagler (LAC) UNDER 1.5 3-pointers made | -205 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |

Combined probability 27.1%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Victor Wembanyama (SAS) OVER 0.5 Steals: 66%, EV -0.06 at -236
- De'Aaron Fox (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -230
- Keaton Wagler (LAC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -205
- Kris Dunn (LAC) OVER 2.5 Rebounds: 60%, EV -0.06 at -179
- Victor Wembanyama (SAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -178
- Kris Dunn (LAC) UNDER 1.5 Steals: 59%, EV -0.06 at -169
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -166
- Victor Wembanyama (SAS) UNDER 3.5 Assists: 58%, EV -0.06 at -166
