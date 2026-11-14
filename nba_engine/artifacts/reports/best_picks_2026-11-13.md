# Best over/under picks and parlays with sportsbook lines (injury-adjusted projections, run 2026-11-14T02:00:01Z UTC)

Lines and prices are the DraftKings prop lines on the board before tip-off (from ESPN's feed, no key). **Backtest verdict: the model has earned no weight against the book on any stat** (see props_backtest.md): its disagreements with DraftKings have not beaten the book on finished games, so picks are shrunk to the book and no leg shows value. Treat the lists below as the book's own most likely outcomes, which still lose to the vig.  For each prop the model's probability for each side is compared with the book: EV is the expected profit per 1 staked at the book's price, using the model's probability (corrected by the calibration bias measured so far). Only legs with EV above 0, a model probability between 52% and 75%, and a model projection within 35% of the line are kept. **The model has not been proven to beat the market** (the market's closing line beat it on team margins), so a positive EV here is the model disagreeing with the book, not a guaranteed edge. Every pick is logged and graded against results in `picks_grade.md`. Parlay probability multiplies the legs (players treated as independent; legs in one game are usually positively linked), and parlay odds multiply the legs' decimal prices.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) UNDER 0.5 Blocks | -258 (DraftKings via ESPN) | 0.4 | 68% | 68% | -0.06 |
| Jaxson Hayes (UTA) UNDER 1.5 Blocks | -244 (DraftKings via ESPN) | 1.2 | 67% | 67% | -0.06 |
| Stephon Castle (SAS) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Darius Garland (LAC) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |

**Combined probability 19.5%; parlay pays 4.0x; expected profit per 1 staked -0.23.**

Safest 3-leg slate parlay: Mikal Bridges (NYK) UNDER 0.5 Blocks (68%); Jaxson Hayes (UTA) UNDER 1.5 Blocks (67%); Stephon Castle (SAS) OVER 0.5 Steals (66%). Combined probability 29.6%; parlay pays 2.8x; expected profit per 1 staked -0.17.

## Our model's own picks (unshrunk model probabilities)

These use the simulator's probabilities as they are, not pulled toward the book, and rank legs by the model's expected profit at DraftKings' price. **The backtest says the model has not beaten the book, so treat this as the model's opinion, not a proven edge.** Every pick is logged and graded in `picks_grade.md`, so the track record builds up.

**Best 2-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Okogie (UTA) UNDER 3.5 Rebounds | +105 (DraftKings via ESPN) | 2.6 | 69% | 46% | +0.41 |
| Rui Hachimura (LAC) UNDER 14.5 Points | -110 (DraftKings via ESPN) | 10.2 | 71% | 49% | +0.35 |

Combined probability 48.8%; parlay pays 3.9x; expected profit per 1 staked +0.91.

**Best 3-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Okogie (UTA) UNDER 3.5 Rebounds | +105 (DraftKings via ESPN) | 2.6 | 69% | 46% | +0.41 |
| Rui Hachimura (LAC) UNDER 14.5 Points | -110 (DraftKings via ESPN) | 10.2 | 71% | 49% | +0.35 |
| Bam Adebayo (MIA) OVER 1.5 3-pointers made | +141 (DraftKings via ESPN) | 1.9 | 56% | 39% | +0.35 |

Combined probability 27.4%; parlay pays 9.4x; expected profit per 1 staked +1.58.

**Best 4-leg slate parlay (one leg per game, ranked by model edge)**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Okogie (UTA) UNDER 3.5 Rebounds | +105 (DraftKings via ESPN) | 2.6 | 69% | 46% | +0.41 |
| Rui Hachimura (LAC) UNDER 14.5 Points | -110 (DraftKings via ESPN) | 10.2 | 71% | 49% | +0.35 |
| Bam Adebayo (MIA) OVER 1.5 3-pointers made | +141 (DraftKings via ESPN) | 1.9 | 56% | 39% | +0.35 |
| Cameron Boozer (MEM) UNDER 0.5 Steals | +116 (DraftKings via ESPN) | 0.5 | 62% | 43% | +0.34 |

Combined probability 17.0%; parlay pays 20.4x; expected profit per 1 staked +2.47.

Top single picks by model edge:

- Josh Okogie (UTA) UNDER 3.5 Rebounds: model 69% vs book 46%, EV +0.41 at +105 (projection 2.6)
- Josh Okogie (UTA) UNDER 1.5 Assists: model 71% vs book 47%, EV +0.41 at -102 (projection 1.1)
- Rui Hachimura (LAC) UNDER 14.5 Points: model 71% vs book 49%, EV +0.35 at -110 (projection 10.2)
- Bam Adebayo (MIA) OVER 1.5 3-pointers made: model 56% vs book 39%, EV +0.35 at +141 (projection 1.9)
- Ajay Mitchell (OKC) UNDER 18.5 Points: model 74% vs book 51%, EV +0.35 at -120 (projection 13.0)
- Cameron Boozer (MEM) UNDER 0.5 Steals: model 62% vs book 43%, EV +0.34 at +116 (projection 0.5)
- Bam Adebayo (MIA) OVER 18.5 Points: model 71% vs book 50%, EV +0.32 at -115 (projection 23.6)
- Nate Ament (MIL) UNDER 8.5 Points: model 71% vs book 51%, EV +0.31 at -119 (projection 6.6)
- Brayden Burries (MIL) UNDER 11.5 Points: model 69% vs book 50%, EV +0.30 at -113 (projection 9.6)
- Tyler Herro (MIL) UNDER 2.5 3-pointers made: model 65% vs book 47%, EV +0.30 at -102 (projection 1.9)
- Domantas Sabonis (SAC) UNDER 5.5 Assists: model 62% vs book 45%, EV +0.29 at +107 (projection 4.3)
- Draymond Green (GSW) OVER 5.5 Assists: model 64% vs book 47%, EV +0.29 at +101 (projection 6.8)

## NYK at IND (game 401909296)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mikal Bridges (NYK) UNDER 0.5 Blocks | -258 (DraftKings via ESPN) | 0.4 | 68% | 68% | -0.06 |
| OG Anunoby (NYK) UNDER 1.5 Steals | -210 (DraftKings via ESPN) | 1.2 | 63% | 63% | -0.06 |
| Andrew Nembhard (IND) OVER 0.5 Steals | -193 (DraftKings via ESPN) | 0.6 | 62% | 62% | -0.06 |

Combined probability 26.4%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Mikal Bridges (NYK) UNDER 0.5 Blocks: 68%, EV -0.06 at -258
- Mikal Bridges (NYK) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -228
- OG Anunoby (NYK) UNDER 1.5 Steals: 63%, EV -0.06 at -210
- Andrew Nembhard (IND) OVER 0.5 Steals: 62%, EV -0.06 at -193
- Landry Shamet (NYK) UNDER 2.5 Rebounds: 62%, EV -0.06 at -191
- OG Anunoby (NYK) UNDER 2.5 3-pointers made: 61%, EV -0.06 at -189
- Aaron Nesmith (IND) OVER 1.5 3-pointers made: 60%, EV -0.06 at -181
- Andrew Nembhard (IND) OVER 1.5 3-pointers made: 60%, EV -0.06 at -178

## MIL at ORL (game 401909297)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Nate Ament (MIL) UNDER 1.5 3-pointers made | -207 (DraftKings via ESPN) | 0.8 | 63% | 63% | -0.06 |
| Brayden Burries (MIL) UNDER 1.5 3-pointers made | -202 (DraftKings via ESPN) | 1.0 | 63% | 63% | -0.06 |
| Franz Wagner (ORL) UNDER 1.5 Steals | -200 (DraftKings via ESPN) | 1.3 | 62% | 62% | -0.06 |

Combined probability 24.8%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Nate Ament (MIL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -207
- Brayden Burries (MIL) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -202
- Franz Wagner (ORL) UNDER 1.5 Steals: 62%, EV -0.06 at -200
- Wendell Carter Jr. (ORL) OVER 0.5 3-pointers made: 60%, EV -0.06 at -179
- Jaime Jaquez Jr. (MIL) UNDER 3.5 Assists: 58%, EV -0.06 at -164
- Jaime Jaquez Jr. (MIL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -163
- Desmond Bane (ORL) UNDER 3.5 Assists: 58%, EV -0.06 at -163
- Myles Turner (MIL) UNDER 1.5 3-pointers made: 58%, EV -0.06 at -159

## CLE at MIA (game 401909298)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Mario Hezonja (CLE) OVER 0.5 3-pointers made | -227 (DraftKings via ESPN) | 1.2 | 65% | 65% | -0.06 |
| Giannis Antetokounmpo (MIA) OVER 0.5 Steals | -226 (DraftKings via ESPN) | 0.9 | 65% | 65% | -0.06 |
| James Harden (CLE) OVER 0.5 Steals | -215 (DraftKings via ESPN) | 0.8 | 64% | 64% | -0.06 |

Combined probability 27.1%; parlay pays 3.0x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Mario Hezonja (CLE) OVER 0.5 3-pointers made: 65%, EV -0.06 at -227
- Giannis Antetokounmpo (MIA) OVER 0.5 Steals: 65%, EV -0.06 at -226
- James Harden (CLE) OVER 0.5 Steals: 64%, EV -0.06 at -215
- Tyrese Proctor (CLE) UNDER 1.5 3-pointers made: 64%, EV -0.06 at -213
- Donovan Mitchell (CLE) UNDER 1.5 Steals: 64%, EV -0.06 at -214
- Bobby Portis (MIA) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -209
- Bobby Portis (MIA) UNDER 1.5 Assists: 63%, EV -0.06 at -208
- Peyton Watson (CLE) UNDER 1.5 Blocks: 63%, EV -0.06 at -205

## ATL at CHI (game 401909299)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Josh Giddey (CHI) UNDER 1.5 3-pointers made | -192 (DraftKings via ESPN) | 1.7 | 62% | 62% | -0.06 |
| Nickeil Alexander-Walker (ATL) UNDER 1.5 Steals | -191 (DraftKings via ESPN) | 1.5 | 61% | 61% | -0.06 |
| Aaron Wiggins (ATL) OVER 1.5 3-pointers made | -186 (DraftKings via ESPN) | 2.5 | 61% | 61% | -0.06 |

Combined probability 23.2%; parlay pays 3.6x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Josh Giddey (CHI) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Nickeil Alexander-Walker (ATL) UNDER 1.5 Steals: 61%, EV -0.06 at -191
- Aaron Wiggins (ATL) OVER 1.5 3-pointers made: 61%, EV -0.06 at -186
- Matas Buzelis (CHI) OVER 1.5 3-pointers made: 61%, EV -0.06 at -185
- Matas Buzelis (CHI) UNDER 2.5 Assists: 61%, EV -0.06 at -185
- CJ McCollum (ATL) OVER 2.5 Assists: 59%, EV -0.06 at -172
- Kingston Flemings (ATL) OVER 0.5 3-pointers made: 59%, EV -0.06 at -172
- Isaac Okoro (CHI) OVER 0.5 3-pointers made: 59%, EV -0.06 at -169

## MEM at NOP (game 401909300)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Herbert Jones (NOP) OVER 0.5 Steals | -235 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Cedric Coward (MEM) UNDER 1.5 Steals | -229 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Jeremiah Fears (NOP) UNDER 1.5 Steals | -212 (DraftKings via ESPN) | 1.2 | 64% | 64% | -0.06 |

Combined probability 27.3%; parlay pays 3.0x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Herbert Jones (NOP) OVER 0.5 Steals: 66%, EV -0.06 at -235
- Cedric Coward (MEM) UNDER 1.5 Steals: 65%, EV -0.06 at -229
- Jeremiah Fears (NOP) UNDER 1.5 Steals: 64%, EV -0.06 at -212
- Herbert Jones (NOP) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -195
- Karlo Matkovic (NOP) OVER 0.5 3-pointers made: 62%, EV -0.06 at -194
- Saddiq Bey (NOP) UNDER 2.5 3-pointers made: 60%, EV -0.06 at -175
- Jaylen Wells (MEM) OVER 2.5 Rebounds: 59%, EV -0.06 at -174
- Zion Williamson (NOP) OVER 2.5 Assists: 59%, EV -0.06 at -167

## UTA at HOU (game 401909301)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Jaxson Hayes (UTA) UNDER 1.5 Blocks | -244 (DraftKings via ESPN) | 1.2 | 67% | 67% | -0.06 |
| Reed Sheppard (HOU) UNDER 1.5 Steals | -240 (DraftKings via ESPN) | 1.2 | 66% | 66% | -0.06 |
| Alperen Sengun (HOU) OVER 0.5 Steals | -237 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |

Combined probability 29.0%; parlay pays 2.8x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Jaxson Hayes (UTA) UNDER 1.5 Blocks: 67%, EV -0.06 at -244
- Reed Sheppard (HOU) UNDER 1.5 Steals: 66%, EV -0.06 at -240
- Alperen Sengun (HOU) OVER 0.5 Steals: 66%, EV -0.06 at -237
- Ace Bailey (UTA) OVER 0.5 Blocks: 66%, EV -0.06 at -235
- Josh Green (UTA) UNDER 1.5 Assists: 65%, EV -0.06 at -230
- Darryn Peterson (UTA) UNDER 0.5 Blocks: 64%, EV -0.06 at -217
- Tari Eason (HOU) UNDER 1.5 3-pointers made: 63%, EV -0.06 at -206
- Fred VanVleet (HOU) UNDER 1.5 Steals: 63%, EV -0.06 at -204

## GSW at SAS (game 401909302)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Stephon Castle (SAS) OVER 0.5 Steals | -236 (DraftKings via ESPN) | 0.9 | 66% | 66% | -0.06 |
| Victor Wembanyama (SAS) UNDER 1.5 Steals | -232 (DraftKings via ESPN) | 1.1 | 66% | 66% | -0.06 |
| Dylan Harper (SAS) OVER 0.5 3-pointers made | -230 (DraftKings via ESPN) | 1.3 | 65% | 65% | -0.06 |

Combined probability 28.3%; parlay pays 2.9x; expected profit per 1 staked -0.17.

Top single picks (over or under, whichever the model prefers):

- Stephon Castle (SAS) OVER 0.5 Steals: 66%, EV -0.06 at -236
- Victor Wembanyama (SAS) UNDER 1.5 Steals: 66%, EV -0.06 at -232
- Dylan Harper (SAS) OVER 0.5 3-pointers made: 65%, EV -0.06 at -230
- Brandin Podziemski (GSW) UNDER 0.5 Blocks: 65%, EV -0.06 at -225
- De'Aaron Fox (SAS) UNDER 1.5 3-pointers made: 65%, EV -0.06 at -223
- Brandin Podziemski (GSW) UNDER 1.5 Steals: 64%, EV -0.06 at -212
- Draymond Green (GSW) OVER 0.5 Steals: 63%, EV -0.06 at -203
- Yaxel Lendeborg (GSW) OVER 0.5 Steals: 62%, EV -0.06 at -197

## POR at SAC (game 401909303)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Toumani Camara (POR) UNDER 1.5 Steals | -223 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Donovan Clingan (POR) OVER 0.5 3-pointers made | -205 (DraftKings via ESPN) | 1.3 | 63% | 63% | -0.06 |
| Sidy Cissoko (POR) UNDER 2.5 Assists | -193 (DraftKings via ESPN) | 2.1 | 62% | 62% | -0.06 |

Combined probability 25.2%; parlay pays 3.3x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Toumani Camara (POR) UNDER 1.5 Steals: 65%, EV -0.06 at -223
- Donovan Clingan (POR) OVER 0.5 3-pointers made: 63%, EV -0.06 at -205
- Sidy Cissoko (POR) UNDER 2.5 Assists: 62%, EV -0.06 at -193
- Scoot Henderson (POR) UNDER 2.5 Rebounds: 61%, EV -0.06 at -183
- Scoot Henderson (POR) UNDER 1.5 3-pointers made: 60%, EV -0.06 at -178
- Deni Avdija (POR) OVER 1.5 3-pointers made: 60%, EV -0.06 at -177
- Zach LaVine (SAC) UNDER 2.5 Assists: 60%, EV -0.06 at -177
- Jrue Holiday (POR) UNDER 2.5 3-pointers made: 59%, EV -0.06 at -169

## OKC at LAC (game 401909304)

**Best 3-leg parlay for this game:**

| Leg | Book price | Model proj | Win prob | Book fair | EV per 1 |
|---|---|---|---|---|---|
| Darius Garland (LAC) UNDER 1.5 Steals | -236 (DraftKings via ESPN) | 0.8 | 66% | 66% | -0.06 |
| Brook Lopez (LAC) UNDER 1.5 Blocks | -225 (DraftKings via ESPN) | 1.0 | 65% | 65% | -0.06 |
| Rui Hachimura (LAC) UNDER 1.5 Assists | -205 (DraftKings via ESPN) | 0.9 | 63% | 63% | -0.06 |

Combined probability 26.9%; parlay pays 3.1x; expected profit per 1 staked -0.18.

Top single picks (over or under, whichever the model prefers):

- Darius Garland (LAC) UNDER 1.5 Steals: 66%, EV -0.06 at -236
- Brook Lopez (LAC) UNDER 1.5 Blocks: 65%, EV -0.06 at -225
- Brook Lopez (LAC) UNDER 1.5 Assists: 64%, EV -0.06 at -218
- Rui Hachimura (LAC) UNDER 1.5 Assists: 63%, EV -0.06 at -205
- Alex Caruso (OKC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -196
- Derrick Jones Jr. (LAC) UNDER 1.5 Assists: 62%, EV -0.06 at -194
- Kenrich Williams (OKC) UNDER 1.5 3-pointers made: 62%, EV -0.06 at -192
- Shai Gilgeous-Alexander (OKC) UNDER 1.5 Steals: 61%, EV -0.07 at -191
