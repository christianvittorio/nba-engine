# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-25T19:01:22Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -227 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -223 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Ajay Mitchell (OKC) OVER 0.5 3-pointers made | -215 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Tari Eason (HOU) UNDER 1.5 3-pointers made | -215 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

**Combined probability 17.3%; parlay pays 4.5x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Bam Adebayo (MIA) UNDER 1.5 3-pointers made (65%); Derrick Jones Jr. (LAC) UNDER 1.5 Assists (65%); Ajay Mitchell (OKC) OVER 0.5 3-pointers made (64%). Combined probability 27.1%; parlay pays 3.1x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Davion Mitchell (MIA) UNDER 15.5 Points | -111 (DraftKings via ESPN) | 13.3 | 68% | 50% | +0.30 |
| Tyler Herro (MIL) UNDER 22.5 Points | -104 (DraftKings via ESPN) | 19.9 | 65% | 48% | +0.27 |

Combined probability 44.1%; parlay pays 3.7x; expected profit per 1 staked +0.65.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Davion Mitchell (MIA) UNDER 15.5 Points | -111 (DraftKings via ESPN) | 13.3 | 68% | 50% | +0.30 |
| Tyler Herro (MIL) UNDER 22.5 Points | -104 (DraftKings via ESPN) | 19.9 | 65% | 48% | +0.27 |
| Karl-Anthony Towns (NYK) OVER 3.5 Assists | -130 (DraftKings via ESPN) | 4.4 | 70% | 53% | +0.24 |

Combined probability 30.9%; parlay pays 6.6x; expected profit per 1 staked +1.04.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Davion Mitchell (MIA) UNDER 15.5 Points | -111 (DraftKings via ESPN) | 13.3 | 68% | 50% | +0.30 |
| Tyler Herro (MIL) UNDER 22.5 Points | -104 (DraftKings via ESPN) | 19.9 | 65% | 48% | +0.27 |
| Karl-Anthony Towns (NYK) OVER 3.5 Assists | -130 (DraftKings via ESPN) | 4.4 | 70% | 53% | +0.24 |
| Khaman Maluach (PHX) UNDER 6.5 Points | -121 (DraftKings via ESPN) | 5.5 | 67% | 52% | +0.22 |

Combined probability 20.6%; parlay pays 12.0x; expected profit per 1 staked +1.48.

Top single picks by model edge:

- Davion Mitchell (MIA) UNDER 15.5 Points: model 68% vs book 50%, EV +0.30 at -111 (projection 13.3)
- Tyler Herro (MIL) UNDER 22.5 Points: model 65% vs book 48%, EV +0.27 at -104 (projection 19.9)
- Tyrese Maxey (PHI) UNDER 25.5 Points: model 64% vs book 48%, EV +0.25 at -104 (projection 20.3)
- Karl-Anthony Towns (NYK) OVER 3.5 Assists: model 70% vs book 53%, EV +0.24 at -130 (projection 4.4)
- Jalen Brunson (NYK) OVER 5.5 Assists: model 71% vs book 54%, EV +0.23 at -137 (projection 7.4)
- Giannis Antetokounmpo (MIA) UNDER 28.5 Points: model 63% vs book 48%, EV +0.23 at -105 (projection 23.1)
- Khaman Maluach (PHX) UNDER 6.5 Points: model 67% vs book 52%, EV +0.22 at -121 (projection 5.5)
- Stephon Castle (SAS) UNDER 19.5 Points: model 63% vs book 49%, EV +0.21 at -110 (projection 17.7)
- Scoot Henderson (POR) OVER 10.5 Points: model 62% vs book 48%, EV +0.21 at -104 (projection 13.0)
- Noah Clowney (BKN) OVER 3.5 Rebounds: model 55% vs book 43%, EV +0.20 at +119 (projection 4.0)
- Miles Bridges (PHX) UNDER 13.5 Points: model 61% vs book 48%, EV +0.20 at -103 (projection 12.5)
- Naz Reid (CHA) OVER 20.5 Points: model 61% vs book 48%, EV +0.20 at -103 (projection 23.2)

## MIA at PHI (game 401909317)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -227 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |
| Davion Mitchell (MIA) UNDER 2.5 3-pointers made | -190 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |
| LeBron James (PHI) UNDER 1.5 3-pointers made | -182 (DraftKings via ESPN) | 1.1 | 60% | 60% | -0.06 |

Combined probability 24.2%; parlay pays 3.4x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -227
- Davion Mitchell (MIA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -190
- LeBron James (PHI) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -182
- VJ Edgecombe (PHI) UNDER 4.5 Assists: 58%, EV -0.06 at -160
- Davion Mitchell (MIA) UNDER 3.5 Rebounds: 57%, EV -0.06 at -156

## CHI at CHA (game 401909318)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Moussa Diabate (CHA) OVER 1.5 Assists | -194 (DraftKings via ESPN) | 3.1 | 62% | 62% | -0.06 |
| Jalen Smith (CHI) UNDER 2.5 Assists | -192 (DraftKings via ESPN) | 1.8 | 62% | 62% | -0.06 |
| Sion James (CHA) UNDER 1.5 3-pointers made | -190 (DraftKings via ESPN) | 1.5 | 61% | 61% | -0.06 |

Combined probability 23.4%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Moussa Diabate (CHA) OVER 1.5 Assists: 62%, EV -0.06 at -194
- Jalen Smith (CHI) UNDER 2.5 Assists: 62%, EV -0.06 at -192
- Sion James (CHA) UNDER 1.5 3-pointers made: 61%, EV -0.06 at -190
- Isaac Okoro (CHI) OVER 1.5 Assists: 61%, EV -0.06 at -187
- Buddy Hield (CHI) UNDER 2.5 Assists: 61%, EV -0.06 at -186
- Coby White (CHA) UNDER 3.5 Rebounds: 59%, EV -0.06 at -168
- Isaac Okoro (CHI) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -166
- Jalen Smith (CHI) OVER 1.5 3-pointers made: 58%, EV -0.06 at -163

## CLE at NYK (game 401909319)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Karl-Anthony Towns (NYK) OVER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 2.2 | 62% | 62% | -0.06 |
| Landry Shamet (NYK) UNDER 2.5 Assists | -180 (DraftKings via ESPN) | 2.3 | 60% | 60% | -0.06 |
| Tyrese Proctor (CLE) UNDER 1.5 3-pointers made | -172 (DraftKings via ESPN) | 1.7 | 59% | 59% | -0.06 |

Combined probability 22.1%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Karl-Anthony Towns (NYK) OVER 1.5 3-pointers made: 62%, EV -0.06 at -194
- Landry Shamet (NYK) UNDER 2.5 Assists: 60%, EV -0.06 at -180
- Tyrese Proctor (CLE) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Mikal Bridges (NYK) OVER 2.5 Rebounds: 59%, EV -0.06 at -168
- James Harden (CLE) UNDER 2.5 3-pointers made: 56%, EV -0.06 at -148
- James Harden (CLE) UNDER 6.5 Assists: 55%, EV -0.07 at -146
- Donovan Mitchell (CLE) UNDER 4.5 Rebounds: 55%, EV -0.06 at -143
- Landry Shamet (NYK) OVER 2.5 3-pointers made: 55%, EV -0.06 at -143

## MIN at OKC (game 401909320)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Ajay Mitchell (OKC) OVER 0.5 3-pointers made | -215 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made | -186 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |
| Kenrich Williams (OKC) UNDER 1.5 3-pointers made | -172 (DraftKings via ESPN) | 1.4 | 59% | 59% | -0.06 |

Combined probability 23.1%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Ajay Mitchell (OKC) OVER 0.5 3-pointers made: 64%, EV -0.06 at -215
- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -186
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Terrence Shannon Jr. (MIN) UNDER 3.5 Rebounds: 59%, EV -0.06 at -167
- Ayo Dosunmu (MIN) OVER 1.5 3-pointers made: 58%, EV -0.06 at -162
- Isaiah Hartenstein (OKC) OVER 3.5 Assists: 58%, EV -0.06 at -161
- Kenrich Williams (OKC) UNDER 5.5 Rebounds: 57%, EV -0.06 at -155
- Jonathan Kuminga (MIN) UNDER 2.5 Assists: 56%, EV -0.06 at -152

## LAC at MEM (game 401909321)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -223 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Max Strus (LAC) OVER 1.5 Assists | -191 (DraftKings via ESPN) | 2.8 | 62% | 62% | -0.06 |
| Rui Hachimura (LAC) UNDER 1.5 Assists | -174 (DraftKings via ESPN) | 1.3 | 59% | 59% | -0.06 |

Combined probability 23.7%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 65%, EV -0.06 at -223
- Max Strus (LAC) OVER 1.5 Assists: 62%, EV -0.06 at -191
- Rui Hachimura (LAC) UNDER 1.5 Assists: 59%, EV -0.06 at -174
- Max Strus (LAC) OVER 1.5 3-pointers made: 58%, EV -0.06 at -164
- Cedric Coward (MEM) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -162
- Jaylen Wells (MEM) UNDER 1.5 Assists: 58%, EV -0.06 at -161
- Cedric Coward (MEM) UNDER 3.5 Assists: 56%, EV -0.06 at -147
- Taylor Hendricks (MEM) UNDER 4.5 Rebounds: 55%, EV -0.06 at -145

## BKN at MIL (game 401909322)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Michael Porter Jr. (BKN) OVER 1.5 Assists | -198 (DraftKings via ESPN) | 2.0 | 62% | 62% | -0.06 |
| Noah Clowney (BKN) UNDER 1.5 3-pointers made | -197 (DraftKings via ESPN) | 1.5 | 62% | 62% | -0.06 |
| Egor Demin (BKN) OVER 1.5 3-pointers made | -188 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |

Combined probability 23.7%; parlay pays 3.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Michael Porter Jr. (BKN) OVER 1.5 Assists: 62%, EV -0.06 at -198
- Noah Clowney (BKN) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -197
- Egor Demin (BKN) OVER 1.5 3-pointers made: 61%, EV -0.06 at -188
- Myles Turner (MIL) UNDER 2.5 Assists: 61%, EV -0.06 at -186
- Danny Wolf (BKN) UNDER 2.5 Assists: 60%, EV -0.06 at -181
- Brayden Burries (MIL) UNDER 3.5 Assists: 59%, EV -0.06 at -166
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -163
- Jaime Jaquez Jr. (MIL) OVER 2.5 Assists: 58%, EV -0.06 at -161

## PHX at HOU (game 401909323)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tari Eason (HOU) UNDER 1.5 3-pointers made | -215 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Amen Thompson (HOU) OVER 2.5 Assists | -177 (DraftKings via ESPN) | 3.1 | 60% | 60% | -0.06 |
| Devin Booker (PHX) OVER 2.5 Rebounds | -169 (DraftKings via ESPN) | 3.1 | 59% | 59% | -0.06 |

Combined probability 22.6%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Tari Eason (HOU) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -215
- Amen Thompson (HOU) OVER 2.5 Assists: 60%, EV -0.06 at -177
- Devin Booker (PHX) OVER 2.5 Rebounds: 59%, EV -0.06 at -169
- Collin Gillespie (PHX) OVER 1.5 3-pointers made: 59%, EV -0.06 at -169
- Jabari Smith Jr. (HOU) OVER 1.5 3-pointers made: 58%, EV -0.06 at -164
- Jalen Green (PHX) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -161
- Devin Booker (PHX) UNDER 5.5 Assists: 57%, EV -0.06 at -154
- Collin Gillespie (PHX) UNDER 3.5 Assists: 57%, EV -0.06 at -154

## SAC at GSW (game 401909324)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| De'Anthony Melton (GSW) UNDER 2.5 3-pointers made | -192 (DraftKings via ESPN) | 1.9 | 62% | 62% | -0.06 |
| Zach LaVine (SAC) UNDER 2.5 3-pointers made | -173 (DraftKings via ESPN) | 2.1 | 59% | 59% | -0.06 |
| De'Andre Hunter (SAC) OVER 1.5 Assists | -169 (DraftKings via ESPN) | 2.2 | 59% | 59% | -0.06 |

Combined probability 21.6%; parlay pays 3.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- De'Anthony Melton (GSW) UNDER 2.5 3-pointers made: 62%, EV -0.06 at -192
- Zach LaVine (SAC) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -173
- De'Andre Hunter (SAC) OVER 1.5 Assists: 59%, EV -0.06 at -169
- Darius Acuff Jr. (SAC) UNDER 3.5 Rebounds: 58%, EV -0.06 at -165
- De'Andre Hunter (SAC) OVER 1.5 3-pointers made: 57%, EV -0.06 at -157
- Yaxel Lendeborg (GSW) OVER 3.5 Assists: 57%, EV -0.06 at -155
- Domantas Sabonis (SAC) OVER 4.5 Assists: 57%, EV -0.06 at -153
- Draymond Green (GSW) OVER 4.5 Rebounds: 56%, EV -0.06 at -151

## SAS at POR (game 401909325)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Stephon Castle (SAS) OVER 1.5 3-pointers made | -185 (DraftKings via ESPN) | 1.8 | 61% | 61% | -0.06 |
| Toumani Camara (POR) UNDER 2.5 3-pointers made | -184 (DraftKings via ESPN) | 2.4 | 61% | 61% | -0.06 |
| Scoot Henderson (POR) UNDER 1.5 3-pointers made | -180 (DraftKings via ESPN) | 1.6 | 60% | 60% | -0.06 |

Combined probability 22.3%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Stephon Castle (SAS) OVER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Toumani Camara (POR) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -184
- Scoot Henderson (POR) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -180
- Jrue Holiday (POR) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Damian Lillard (POR) UNDER 3.5 3-pointers made: 60%, EV -0.06 at -175
- Sidy Cissoko (POR) UNDER 3.5 Rebounds: 59%, EV -0.06 at -166
- Victor Wembanyama (SAS) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -160
- Devin Vassell (SAS) OVER 1.5 3-pointers made: 57%, EV -0.06 at -156
