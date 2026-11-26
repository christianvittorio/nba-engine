# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-26T03:59:19Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Shai Gilgeous-Alexander (OKC) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Mikal Bridges (NYK) OVER 0.5 Steals | -231 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Bobby Portis (MIA) UNDER 1.5 3-pointers made | -223 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -223 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |

**Combined probability 18.1%; parlay pays 4.3x; expected profit per 1 staked -0.22.**

Safest 3-leg slate parlay: Shai Gilgeous-Alexander (OKC) OVER 0.5 Steals (66%); Mikal Bridges (NYK) OVER 0.5 Steals (65%); Bobby Portis (MIA) UNDER 1.5 3-pointers made (65%). Combined probability 27.9%; parlay pays 3.0x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kris Murray (MEM) UNDER 2.5 Rebounds | +101 (DraftKings via ESPN) | 2.0 | 65% | 47% | +0.31 |
| Josh Hart (NYK) OVER 9.5 Points | -103 (DraftKings via ESPN) | 12.5 | 66% | 48% | +0.30 |

Combined probability 43.0%; parlay pays 4.0x; expected profit per 1 staked +0.70.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kris Murray (MEM) UNDER 2.5 Rebounds | +101 (DraftKings via ESPN) | 2.0 | 65% | 47% | +0.31 |
| Josh Hart (NYK) OVER 9.5 Points | -103 (DraftKings via ESPN) | 12.5 | 66% | 48% | +0.30 |
| Jared McCain (OKC) OVER 13.5 Points | -122 (DraftKings via ESPN) | 17.6 | 69% | 52% | +0.25 |

Combined probability 29.5%; parlay pays 7.2x; expected profit per 1 staked +1.12.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Kris Murray (MEM) UNDER 2.5 Rebounds | +101 (DraftKings via ESPN) | 2.0 | 65% | 47% | +0.31 |
| Josh Hart (NYK) OVER 9.5 Points | -103 (DraftKings via ESPN) | 12.5 | 66% | 48% | +0.30 |
| Jared McCain (OKC) OVER 13.5 Points | -122 (DraftKings via ESPN) | 17.6 | 69% | 52% | +0.25 |
| Malik Monk (SAC) UNDER 10.5 Points | -110 (DraftKings via ESPN) | 9.2 | 64% | 49% | +0.22 |

Combined probability 18.8%; parlay pays 13.8x; expected profit per 1 staked +1.58.

Top single picks by model edge:

- Kris Murray (MEM) UNDER 2.5 Rebounds: model 65% vs book 47%, EV +0.31 at +101 (projection 2.0)
- Josh Hart (NYK) OVER 9.5 Points: model 66% vs book 48%, EV +0.30 at -103 (projection 12.5)
- Keaton Wagler (LAC) OVER 2.5 Rebounds: model 59% vs book 43%, EV +0.28 at +118 (projection 3.1)
- Jared McCain (OKC) OVER 13.5 Points: model 69% vs book 52%, EV +0.25 at -122 (projection 17.6)
- Jalen Brunson (NYK) OVER 6.5 Assists: model 60% vs book 46%, EV +0.23 at +104 (projection 7.4)
- Malik Monk (SAC) UNDER 10.5 Points: model 64% vs book 49%, EV +0.22 at -110 (projection 9.2)
- Kenrich Williams (OKC) OVER 8.5 Points: model 61% vs book 47%, EV +0.21 at +100 (projection 10.6)
- Luke Kennard (PHX) UNDER 6.5 Points: model 67% vs book 53%, EV +0.20 at -127 (projection 5.4)
- Scoot Henderson (POR) OVER 10.5 Points: model 61% vs book 48%, EV +0.20 at -103 (projection 13.1)
- Naz Reid (CHA) OVER 19.5 Points: model 65% vs book 51%, EV +0.20 at -120 (projection 23.2)
- De'Andre Hunter (SAC) OVER 15.5 Points: model 66% vs book 52%, EV +0.20 at -125 (projection 17.1)
- Karl-Anthony Towns (NYK) OVER 3.5 Assists: model 70% vs book 55%, EV +0.19 at -142 (projection 4.4)

## MIA at PHI (game 401909317)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Bobby Portis (MIA) UNDER 1.5 3-pointers made | -223 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
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
| Buddy Hield (CHI) UNDER 2.5 Assists | -192 (DraftKings via ESPN) | 2.4 | 62% | 62% | -0.06 |
| Moussa Diabate (CHA) OVER 1.5 Assists | -186 (DraftKings via ESPN) | 3.1 | 61% | 61% | -0.06 |
| Nic Claxton (CHI) UNDER 2.5 Assists | -177 (DraftKings via ESPN) | 2.3 | 60% | 60% | -0.06 |

Combined probability 22.5%; parlay pays 3.7x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Buddy Hield (CHI) UNDER 2.5 Assists: 62%, EV -0.06 at -192
- Moussa Diabate (CHA) OVER 1.5 Assists: 61%, EV -0.06 at -186
- Nic Claxton (CHI) UNDER 2.5 Assists: 60%, EV -0.06 at -177
- Sion James (CHA) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Isaac Okoro (CHI) OVER 2.5 Rebounds: 60%, EV -0.06 at -175
- Coby White (CHA) UNDER 3.5 Rebounds: 58%, EV -0.06 at -165
- Tre Jones (CHI) UNDER 2.5 Rebounds: 58%, EV -0.06 at -164
- Sion James (CHA) UNDER 3.5 Assists: 58%, EV -0.06 at -164

## CLE at NYK (game 401909319)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) OVER 0.5 Steals | -231 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Karl-Anthony Towns (NYK) OVER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 2.2 | 62% | 62% | -0.06 |
| Landry Shamet (NYK) OVER 1.5 Assists | -179 (DraftKings via ESPN) | 2.3 | 60% | 60% | -0.06 |

Combined probability 24.4%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Mikal Bridges (NYK) OVER 0.5 Steals: 65%, EV -0.06 at -231
- Karl-Anthony Towns (NYK) OVER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Landry Shamet (NYK) OVER 1.5 Assists: 60%, EV -0.06 at -179
- Landry Shamet (NYK) UNDER 2.5 Rebounds: 60%, EV -0.06 at -176
- Josh Hart (NYK) UNDER 1.5 Steals: 60%, EV -0.06 at -175
- Tyrese Proctor (CLE) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -171
- Mikal Bridges (NYK) UNDER 3.5 Rebounds: 59%, EV -0.06 at -166
- Josh Hart (NYK) UNDER 1.5 3-pointers made: 57%, EV -0.06 at -155

## MIN at OKC (game 401909320)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Shai Gilgeous-Alexander (OKC) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 1.0 | 66% | 66% | -0.06 |
| Ajay Mitchell (OKC) OVER 0.5 3-pointers made | -231 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Rudy Gobert (MIN) UNDER 1.5 Blocks | -212 (DraftKings via ESPN) | 1.1 | 64% | 64% | -0.06 |

Combined probability 27.5%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Shai Gilgeous-Alexander (OKC) OVER 0.5 Steals: 66%, EV -0.06 at -236
- Ajay Mitchell (OKC) OVER 0.5 3-pointers made: 66%, EV -0.06 at -231
- Rudy Gobert (MIN) UNDER 1.5 Blocks: 64%, EV -0.06 at -212
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -202
- Ayo Dosunmu (MIN) OVER 1.5 3-pointers made: 61%, EV -0.06 at -187
- Jared McCain (OKC) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -172
- Shai Gilgeous-Alexander (OKC) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -171
- LaMelo Ball (MIN) UNDER 1.5 Steals: 58%, EV -0.07 at -164

## LAC at MEM (game 401909321)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Derrick Jones Jr. (LAC) UNDER 1.5 Assists | -223 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Rui Hachimura (LAC) UNDER 1.5 Assists | -181 (DraftKings via ESPN) | 1.3 | 60% | 60% | -0.06 |
| Max Strus (LAC) OVER 1.5 Assists | -174 (DraftKings via ESPN) | 2.8 | 60% | 60% | -0.06 |

Combined probability 23.3%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 65%, EV -0.06 at -223
- Rui Hachimura (LAC) UNDER 1.5 Assists: 60%, EV -0.06 at -181
- Max Strus (LAC) OVER 1.5 Assists: 60%, EV -0.06 at -174
- Keaton Wagler (LAC) OVER 1.5 Assists: 59%, EV -0.06 at -170
- Max Strus (LAC) OVER 1.5 3-pointers made: 59%, EV -0.06 at -166
- Jaylen Wells (MEM) UNDER 1.5 Assists: 58%, EV -0.06 at -165
- Cedric Coward (MEM) UNDER 2.5 3-pointers made: 57%, EV -0.06 at -158
- Cedric Coward (MEM) UNDER 3.5 Assists: 57%, EV -0.06 at -158

## BKN at MIL (game 401909322)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Noah Clowney (BKN) UNDER 1.5 3-pointers made | -206 (DraftKings via ESPN) | 1.6 | 63% | 63% | -0.06 |
| Egor Demin (BKN) OVER 1.5 3-pointers made | -181 (DraftKings via ESPN) | 2.2 | 60% | 60% | -0.06 |
| Michael Porter Jr. (BKN) UNDER 3.5 3-pointers made | -176 (DraftKings via ESPN) | 2.8 | 60% | 60% | -0.06 |

Combined probability 22.8%; parlay pays 3.6x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Noah Clowney (BKN) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Egor Demin (BKN) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Michael Porter Jr. (BKN) UNDER 3.5 3-pointers made: 60%, EV -0.06 at -176
- Brayden Burries (MIL) OVER 2.5 Assists: 59%, EV -0.06 at -170
- Michael Porter Jr. (BKN) OVER 1.5 Assists: 59%, EV -0.06 at -169
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -168
- Day'Ron Sharpe (BKN) UNDER 4.5 Assists: 58%, EV -0.06 at -160
- Jaime Jaquez Jr. (MIL) OVER 3.5 Rebounds: 57%, EV -0.06 at -158

## PHX at HOU (game 401909323)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Tari Eason (HOU) UNDER 1.5 3-pointers made | -216 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |
| Jabari Smith Jr. (HOU) OVER 1.5 3-pointers made | -178 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |
| Collin Gillespie (PHX) OVER 1.5 3-pointers made | -176 (DraftKings via ESPN) | 1.9 | 60% | 60% | -0.06 |

Combined probability 23.0%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Tari Eason (HOU) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -216
- Jabari Smith Jr. (HOU) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Collin Gillespie (PHX) OVER 1.5 3-pointers made: 60%, EV -0.06 at -176
- Luke Kennard (PHX) UNDER 1.5 3-pointers made: 59%, EV -0.06 at -167
- Devin Booker (PHX) UNDER 3.5 Rebounds: 59%, EV -0.06 at -167
- Amen Thompson (HOU) UNDER 3.5 Assists: 58%, EV -0.06 at -160
- Devin Booker (PHX) UNDER 5.5 Assists: 57%, EV -0.06 at -154
- Collin Gillespie (PHX) UNDER 3.5 Assists: 57%, EV -0.06 at -154

## SAC at GSW (game 401909324)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Will Richard (GSW) OVER 0.5 3-pointers made | -201 (DraftKings via ESPN) | 1.1 | 63% | 63% | -0.06 |
| De'Andre Hunter (SAC) OVER 1.5 3-pointers made | -196 (DraftKings via ESPN) | 2.2 | 62% | 62% | -0.06 |
| Gui Santos (GSW) OVER 1.5 Assists | -192 (DraftKings via ESPN) | 2.4 | 62% | 62% | -0.06 |

Combined probability 23.9%; parlay pays 3.4x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Will Richard (GSW) OVER 0.5 3-pointers made: 63%, EV -0.06 at -201
- De'Andre Hunter (SAC) OVER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Gui Santos (GSW) OVER 1.5 Assists: 62%, EV -0.06 at -192
- De'Andre Hunter (SAC) OVER 1.5 Assists: 60%, EV -0.06 at -177
- Darius Acuff Jr. (SAC) UNDER 3.5 Rebounds: 60%, EV -0.06 at -177
- Will Richard (GSW) UNDER 2.5 Rebounds: 59%, EV -0.06 at -173
- De'Anthony Melton (GSW) OVER 1.5 3-pointers made: 59%, EV -0.06 at -170
- De'Anthony Melton (GSW) OVER 2.5 Assists: 59%, EV -0.06 at -167

## SAS at POR (game 401909325)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -223 (DraftKings via ESPN) | 1.4 | 65% | 65% | -0.06 |
| Jrue Holiday (POR) UNDER 2.5 3-pointers made | -188 (DraftKings via ESPN) | 2.3 | 61% | 61% | -0.06 |
| Scoot Henderson (POR) UNDER 2.5 Rebounds | -176 (DraftKings via ESPN) | 2.5 | 60% | 60% | -0.06 |

Combined probability 23.7%; parlay pays 3.5x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Victor Wembanyama (SAS) UNDER 1.5 Steals: 65%, EV -0.06 at -223
- Jrue Holiday (POR) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -188
- Scoot Henderson (POR) UNDER 2.5 Rebounds: 60%, EV -0.06 at -176
- Devin Vassell (SAS) OVER 2.5 Assists: 60%, EV -0.06 at -175
- Victor Wembanyama (SAS) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Scoot Henderson (POR) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -174
- Damian Lillard (POR) UNDER 3.5 3-pointers made: 59%, EV -0.06 at -172
- Toumani Camara (POR) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -170
