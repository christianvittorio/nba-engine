# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-25T22:56:30Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Shai Gilgeous-Alexander (OKC) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Bobby Portis (MIA) UNDER 1.5 3-pointers made | -223 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -223 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Noah Clowney (BKN) UNDER 1.5 3-pointers made | -220 (DraftKings via ESPN) | 1.5 | 65% | 65% | -0.06 |

**Combined probability 17.8%; parlay pays 4.4x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Shai Gilgeous-Alexander (OKC) OVER 0.5 Steals (66%); Bobby Portis (MIA) UNDER 1.5 3-pointers made (65%); Derrick Jones Jr. (LAC) UNDER 1.5 Assists (65%). Combined probability 27.6%; parlay pays 3.0x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Karl-Anthony Towns (NYK) OVER 3.5 Assists | -116 (DraftKings via ESPN) | 4.4 | 70% | 50% | +0.31 |
| Anfernee Simons (PHI) OVER 9.5 Points | -104 (DraftKings via ESPN) | 12.4 | 63% | 48% | +0.24 |

Combined probability 44.2%; parlay pays 3.7x; expected profit per 1 staked +0.62.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Karl-Anthony Towns (NYK) OVER 3.5 Assists | -116 (DraftKings via ESPN) | 4.4 | 70% | 50% | +0.31 |
| Anfernee Simons (PHI) OVER 9.5 Points | -104 (DraftKings via ESPN) | 12.4 | 63% | 48% | +0.24 |
| Scoot Henderson (POR) OVER 10.5 Points | +100 (DraftKings via ESPN) | 13.0 | 62% | 47% | +0.23 |

Combined probability 27.2%; parlay pays 7.3x; expected profit per 1 staked +0.99.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Karl-Anthony Towns (NYK) OVER 3.5 Assists | -116 (DraftKings via ESPN) | 4.4 | 70% | 50% | +0.31 |
| Anfernee Simons (PHI) OVER 9.5 Points | -104 (DraftKings via ESPN) | 12.4 | 63% | 48% | +0.24 |
| Scoot Henderson (POR) OVER 10.5 Points | +100 (DraftKings via ESPN) | 13.0 | 62% | 47% | +0.23 |
| De'Andre Hunter (SAC) OVER 15.5 Points | -122 (DraftKings via ESPN) | 17.2 | 67% | 52% | +0.22 |

Combined probability 18.3%; parlay pays 13.3x; expected profit per 1 staked +1.43.

Top single picks by model edge:

- Karl-Anthony Towns (NYK) OVER 3.5 Assists: model 70% vs book 50%, EV +0.31 at -116 (projection 4.4)
- Josh Hart (NYK) OVER 9.5 Points: model 66% vs book 48%, EV +0.30 at -102 (projection 12.5)
- Jalen Brunson (NYK) OVER 6.5 Assists: model 60% vs book 45%, EV +0.26 at +109 (projection 7.4)
- Anfernee Simons (PHI) OVER 9.5 Points: model 63% vs book 48%, EV +0.24 at -104 (projection 12.4)
- Scoot Henderson (POR) OVER 10.5 Points: model 62% vs book 47%, EV +0.23 at +100 (projection 13.0)
- De'Andre Hunter (SAC) OVER 15.5 Points: model 67% vs book 52%, EV +0.22 at -122 (projection 17.2)
- Tyler Herro (MIL) UNDER 2.5 3-pointers made: model 53% vs book 41%, EV +0.22 at +131 (projection 2.5)
- Tyler Herro (MIL) UNDER 22.5 Points: model 65% vs book 50%, EV +0.21 at -115 (projection 19.9)
- Mikal Bridges (NYK) OVER 2.5 Assists: model 62% vs book 48%, EV +0.20 at -105 (projection 3.2)
- Cam Spencer (MEM) OVER 1.5 3-pointers made: model 57% vs book 45%, EV +0.20 at +109 (projection 2.0)
- Naz Reid (CHA) OVER 19.5 Points: model 65% vs book 51%, EV +0.20 at -120 (projection 23.2)
- Josh Hart (NYK) OVER 4.5 Assists: model 62% vs book 48%, EV +0.20 at -106 (projection 5.4)

## MIA at PHI (game 401909317)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bobby Portis (MIA) UNDER 1.5 3-pointers made | -223 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |
| Bam Adebayo (MIA) UNDER 1.5 3-pointers made | -210 (DraftKings via ESPN) | 1.4 | 64% | 64% | -0.06 |
| Andrew Wiggins (MIA) UNDER 1.5 3-pointers made | -208 (DraftKings via ESPN) | 1.4 | 63% | 63% | -0.06 |

Combined probability 26.1%; parlay pays 3.2x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -223
- Bam Adebayo (MIA) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -210
- Andrew Wiggins (MIA) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -208
- LeBron James (PHI) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -201
- Davion Mitchell (MIA) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -190
- Anfernee Simons (PHI) OVER 1.5 3-pointers made: 57%, EV -0.06 at -159
- Davion Mitchell (MIA) OVER 2.5 Rebounds: 57%, EV -0.06 at -155
- Bobby Portis (MIA) UNDER 4.5 Rebounds: 57%, EV -0.06 at -153

## CHI at CHA (game 401909318)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Sion James (CHA) UNDER 1.5 3-pointers made | -198 (DraftKings via ESPN) | 1.5 | 62% | 62% | -0.06 |
| Moussa Diabate (CHA) OVER 1.5 Assists | -194 (DraftKings via ESPN) | 3.1 | 62% | 62% | -0.06 |
| Buddy Hield (CHI) UNDER 2.5 Assists | -192 (DraftKings via ESPN) | 2.4 | 62% | 62% | -0.06 |

Combined probability 23.8%; parlay pays 3.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Sion James (CHA) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -198
- Moussa Diabate (CHA) OVER 1.5 Assists: 62%, EV -0.06 at -194
- Buddy Hield (CHI) UNDER 2.5 Assists: 62%, EV -0.06 at -192
- Nic Claxton (CHI) UNDER 2.5 Assists: 60%, EV -0.06 at -177
- Isaac Okoro (CHI) OVER 2.5 Rebounds: 59%, EV -0.06 at -170
- Coby White (CHA) UNDER 3.5 Rebounds: 58%, EV -0.06 at -165
- Sion James (CHA) UNDER 3.5 Assists: 58%, EV -0.06 at -164
- Royce O'Neale (CHA) UNDER 3.5 Rebounds: 58%, EV -0.06 at -163

## CLE at NYK (game 401909319)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Karl-Anthony Towns (NYK) OVER 1.5 3-pointers made | -189 (DraftKings via ESPN) | 2.2 | 61% | 61% | -0.06 |
| Josh Hart (NYK) UNDER 1.5 Steals | -181 (DraftKings via ESPN) | 1.3 | 60% | 60% | -0.07 |
| Tyrese Proctor (CLE) UNDER 1.5 3-pointers made | -174 (DraftKings via ESPN) | 1.7 | 59% | 59% | -0.06 |

Combined probability 22.0%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Karl-Anthony Towns (NYK) OVER 1.5 3-pointers made: 61%, EV -0.06 at -189
- Josh Hart (NYK) UNDER 1.5 Steals: 60%, EV -0.07 at -181
- Tyrese Proctor (CLE) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -174
- Mikal Bridges (NYK) UNDER 3.5 Rebounds: 59%, EV -0.06 at -170
- Donovan Mitchell (CLE) UNDER 4.5 Rebounds: 57%, EV -0.06 at -159
- Jalen Brunson (NYK) OVER 2.5 Rebounds: 57%, EV -0.06 at -159
- Landry Shamet (NYK) OVER 1.5 Assists: 57%, EV -0.06 at -157
- Josh Hart (NYK) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -155

## MIN at OKC (game 401909320)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Shai Gilgeous-Alexander (OKC) OVER 0.5 Steals | -233 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Ajay Mitchell (OKC) OVER 0.5 3-pointers made | -222 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Rudy Gobert (MIN) UNDER 1.5 Blocks | -211 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 27.0%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Shai Gilgeous-Alexander (OKC) OVER 0.5 Steals: 66%, EV -0.06 at -233
- Ajay Mitchell (OKC) OVER 0.5 3-pointers made: 65%, EV -0.06 at -222
- Rudy Gobert (MIN) UNDER 1.5 Blocks: 64%, EV -0.06 at -211
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -180
- Ayo Dosunmu (MIN) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- LaMelo Ball (MIN) UNDER 1.5 Steals: 59%, EV -0.07 at -171
- Isaiah Hartenstein (OKC) OVER 3.5 Assists: 58%, EV -0.06 at -159

## LAC at MEM (game 401909321)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -223 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Max Strus (LAC) OVER 1.5 Assists | -182 (DraftKings via ESPN) | 2.8 | 60% | 60% | -0.06 |
| Rui Hachimura (LAC) UNDER 1.5 Assists | -181 (DraftKings via ESPN) | 1.3 | 60% | 60% | -0.06 |

Combined probability 23.6%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 65%, EV -0.06 at -223
- Max Strus (LAC) OVER 1.5 Assists: 60%, EV -0.06 at -182
- Rui Hachimura (LAC) UNDER 1.5 Assists: 60%, EV -0.06 at -181
- Jaylen Wells (MEM) UNDER 1.5 Assists: 58%, EV -0.06 at -165
- Max Strus (LAC) OVER 1.5 3-pointers made: 58%, EV -0.06 at -164
- Cedric Coward (MEM) UNDER 3.5 Assists: 57%, EV -0.06 at -157
- Cedric Coward (MEM) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -157
- Darius Garland (LAC) UNDER 2.5 Rebounds: 56%, EV -0.06 at -151

## BKN at MIL (game 401909322)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Noah Clowney (BKN) UNDER 1.5 3-pointers made | -220 (DraftKings via ESPN) | 1.5 | 65% | 65% | -0.06 |
| Michael Porter Jr. (BKN) OVER 1.5 Assists | -182 (DraftKings via ESPN) | 2.0 | 61% | 61% | -0.06 |
| Egor Demin (BKN) OVER 1.5 3-pointers made | -174 (DraftKings via ESPN) | 2.0 | 60% | 60% | -0.06 |

Combined probability 23.3%; parlay pays 3.5x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Noah Clowney (BKN) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -220
- Michael Porter Jr. (BKN) OVER 1.5 Assists: 61%, EV -0.06 at -182
- Egor Demin (BKN) OVER 1.5 3-pointers made: 60%, EV -0.06 at -174
- Tyler Herro (MIL) OVER 2.5 3-pointers made: 59%, EV -0.06 at -174
- Michael Porter Jr. (BKN) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -167
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Brayden Burries (MIL) UNDER 3.5 Assists: 58%, EV -0.06 at -164
- Myles Turner (MIL) OVER 1.5 Assists: 57%, EV -0.06 at -158

## PHX at HOU (game 401909323)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tari Eason (HOU) UNDER 1.5 3-pointers made | -220 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Jabari Smith Jr. (HOU) OVER 1.5 3-pointers made | -178 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |
| Devin Booker (PHX) OVER 2.5 Rebounds | -169 (DraftKings via ESPN) | 3.1 | 59% | 59% | -0.06 |

Combined probability 22.8%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Tari Eason (HOU) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -220
- Jabari Smith Jr. (HOU) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Devin Booker (PHX) OVER 2.5 Rebounds: 59%, EV -0.06 at -169
- Collin Gillespie (PHX) OVER 1.5 3-pointers made: 59%, EV -0.06 at -169
- Miles Bridges (PHX) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -165
- Amen Thompson (HOU) UNDER 3.5 Assists: 58%, EV -0.06 at -160
- Jalen Green (PHX) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -159
- Devin Booker (PHX) UNDER 5.5 Assists: 57%, EV -0.06 at -159

## SAC at GSW (game 401909324)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| De'Andre Hunter (SAC) OVER 1.5 3-pointers made | -194 (DraftKings via ESPN) | 2.2 | 62% | 62% | -0.06 |
| De'Anthony Melton (GSW) OVER 1.5 3-pointers made | -181 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |
| Darius Acuff Jr. (SAC) UNDER 3.5 Rebounds | -168 (DraftKings via ESPN) | 3.3 | 59% | 59% | -0.06 |

Combined probability 21.9%; parlay pays 3.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- De'Andre Hunter (SAC) OVER 1.5 3-pointers made: 62%, EV -0.06 at -194
- De'Anthony Melton (GSW) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181
- De'Anthony Melton (GSW) UNDER 3.5 Assists: 60%, EV -0.06 at -176
- De'Andre Hunter (SAC) OVER 1.5 Assists: 60%, EV -0.06 at -174
- Darius Acuff Jr. (SAC) UNDER 3.5 Rebounds: 59%, EV -0.06 at -168
- Brandin Podziemski (GSW) UNDER 4.5 Assists: 58%, EV -0.06 at -164
- Yaxel Lendeborg (GSW) OVER 1.5 3-pointers made: 57%, EV -0.06 at -156
- Domantas Sabonis (SAC) OVER 4.5 Assists: 57%, EV -0.06 at -156

## SAS at POR (game 401909325)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jrue Holiday (POR) UNDER 2.5 3-pointers made | -184 (DraftKings via ESPN) | 2.4 | 61% | 61% | -0.06 |
| Scoot Henderson (POR) UNDER 1.5 3-pointers made | -172 (DraftKings via ESPN) | 1.6 | 59% | 59% | -0.06 |
| Toumani Camara (POR) UNDER 2.5 3-pointers made | -171 (DraftKings via ESPN) | 2.4 | 59% | 59% | -0.06 |

Combined probability 21.3%; parlay pays 3.9x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jrue Holiday (POR) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -184
- Scoot Henderson (POR) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -172
- Toumani Camara (POR) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -171
- Scoot Henderson (POR) UNDER 2.5 Rebounds: 59%, EV -0.06 at -170
- Stephon Castle (SAS) OVER 1.5 3-pointers made: 59%, EV -0.06 at -170
- Sidy Cissoko (POR) UNDER 3.5 Rebounds: 59%, EV -0.06 at -169
- Victor Wembanyama (SAS) UNDER 2.5 3-pointers made: 58%, EV -0.06 at -165
- Damian Lillard (POR) UNDER 3.5 Rebounds: 58%, EV -0.06 at -161
