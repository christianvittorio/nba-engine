# Best over/under leans and parlays (injury-adjusted projections, run 2026-11-09T08:06:30Z UTC)

**Read this first.** I do not have sportsbook prop lines, so the line used for each leg is a stand-in: the player's last-10-game average rounded to the nearest half. Books price off recent form too, so a lean means the model, with the injuries and the opponent, disagrees with recent form. It does not mean there is a +EV bet: the real line and price may differ, and the model is not proven to beat the market (the market's closing line beat it on team margins). Check real lines with `python scripts/prop_price.py "<player>" <stat> <line>`. Probabilities are shifted by the calibration bias measured so far (the ladders ran high on overs). A parlay's probability multiplies its legs, treating players as independent; real legs in one game are usually positively linked, so treat it as approximate. Legs are skipped when the model and recent form differ by more than 30% (more likely a model miss), when the model is more than 75% sure, and for 0.5 steal/block lines. Legs void if the player does not play; only players with P(play) of at least 0.85 and 18+ projected minutes are used.

## Best parlay across the whole slate (4 legs, one per game)

| Leg | Model proj | Recent avg | Win prob |
|---|---|---|---|
| Noah Clowney (BKN) UNDER 1.5 Turnovers | 0.9 | 1.1 | 75% |
| Sam Hauser (BOS) UNDER 9.5 Points | 7.2 | 9.4 | 75% |
| Tyrese Maxey (PHI) UNDER 6.5 2-pointers made | 5.3 | 6.7 | 75% |
| De'Andre Hunter (SAC) OVER 16.5 Pts+Reb | 20.2 | 16.0 | 75% |

**Combined probability 31.3%** (fair odds about 3.2 to 1; a book's payout must beat that for it to be worth anything).

Safest 3-leg slate parlay: Noah Clowney (BKN) UNDER 1.5 Turnovers (75%); Sam Hauser (BOS) UNDER 9.5 Points (75%); Tyrese Maxey (PHI) UNDER 6.5 2-pointers made (75%) -> combined 42.0%.

## PHI at CHI (game 401909945)

**Best 3-leg parlay for this game:**

| Leg | Model proj | Recent avg | Win prob |
|---|---|---|---|
| Tyrese Maxey (PHI) UNDER 6.5 2-pointers made | 5.3 | 6.7 | 75% |
| Dean Wade (PHI) UNDER 1.5 Steals | 1.0 | 1.4 | 75% |
| Tre Jones (CHI) UNDER 4.5 Free-throw attempts | 3.1 | 4.1 | 75% |

Combined 41.6%.

Top single leans (over or under, whichever the model prefers):

- Tyrese Maxey (PHI) UNDER 6.5 2-pointers made: 75% (model 5.3 vs recent 6.7)
- Dean Wade (PHI) UNDER 1.5 Steals: 75% (model 1.0 vs recent 1.4)
- Tre Jones (CHI) UNDER 4.5 Free-throw attempts: 75% (model 3.1 vs recent 4.1)
- Caleb Wilson (CHI) UNDER 1.5 Blocks: 74% (model 0.9 vs recent 1.1)
- Tyrese Maxey (PHI) UNDER 35.5 Pts+Reb+Ast: 74% (model 29.7 vs recent 35.9)
- Jaylen Brown (PHI) UNDER 2.5 3-pointers made: 74% (model 1.6 vs recent 2.0)
- Joel Embiid (PHI) UNDER 10.5 Rebounds: 73% (model 7.5 vs recent 10.2)
- Anfernee Simons (PHI) UNDER 2.5 3-pointers made: 73% (model 1.7 vs recent 2.3)

## LAL at DET (game 401909946)

**Best 3-leg parlay for this game:**

| Leg | Model proj | Recent avg | Win prob |
|---|---|---|---|
| Ausar Thompson (DET) UNDER 12.5 Reb+Ast | 10.3 | 12.1 | 74% |
| Duncan Robinson (DET) UNDER 18.5 Points | 15.0 | 18.0 | 74% |
| Jake LaRavia (LAL) UNDER 1.5 3-pointers made | 1.0 | 1.2 | 73% |

Combined 39.8%.

Top single leans (over or under, whichever the model prefers):

- Ausar Thompson (DET) UNDER 12.5 Reb+Ast: 74% (model 10.3 vs recent 12.1)
- Duncan Robinson (DET) UNDER 18.5 Points: 74% (model 15.0 vs recent 18.0)
- Jake LaRavia (LAL) UNDER 1.5 3-pointers made: 73% (model 1.0 vs recent 1.2)
- Paul Reed (DET) UNDER 5.5 2-pointers made: 73% (model 4.5 vs recent 5.1)
- Walker Kessler (LAL) UNDER 1.5 Steals: 72% (model 1.1 vs recent 1.3)
- Austin Reaves (LAL) UNDER 1.5 Steals: 71% (model 1.1 vs recent 1.1)
- Ausar Thompson (DET) UNDER 4.5 2-pointers made: 71% (model 3.7 vs recent 4.0)
- Duncan Robinson (DET) UNDER 1.5 Turnovers: 70% (model 1.1 vs recent 1.1)

## UTA at MIN (game 401909947)

**Best 3-leg parlay for this game:**

| Leg | Model proj | Recent avg | Win prob |
|---|---|---|---|
| Jonathan Kuminga (MIN) UNDER 2.5 3-pointers made | 1.8 | 2.0 | 73% |
| Darryn Peterson (UTA) UNDER 1.5 Steals | 1.1 | 1.1 | 72% |
| Ace Bailey (UTA) UNDER 1.5 Blocks | 1.0 | 1.4 | 70% |

Combined 37.0%.

Top single leans (over or under, whichever the model prefers):

- Jonathan Kuminga (MIN) UNDER 2.5 3-pointers made: 73% (model 1.8 vs recent 2.0)
- Darryn Peterson (UTA) UNDER 1.5 Steals: 72% (model 1.1 vs recent 1.1)
- Jonathan Kuminga (MIN) OVER 22.5 Pts+Reb+Ast: 71% (model 27.8 vs recent 22.0)
- Ace Bailey (UTA) UNDER 1.5 Blocks: 70% (model 1.0 vs recent 1.4)
- Jonathan Kuminga (MIN) OVER 19.5 Pts+Reb: 70% (model 24.3 vs recent 19.0)
- Jonathan Kuminga (MIN) UNDER 1.5 Steals: 69% (model 1.1 vs recent 1.2)
- Ace Bailey (UTA) UNDER 2.5 Turnovers: 69% (model 1.9 vs recent 2.0)
- Josh Okogie (UTA) UNDER 1.5 Free-throw attempts: 67% (model 1.2 vs recent 1.0)

## BKN at DAL (game 401909948)

**Best 3-leg parlay for this game:**

| Leg | Model proj | Recent avg | Win prob |
|---|---|---|---|
| Noah Clowney (BKN) UNDER 1.5 Turnovers | 0.9 | 1.1 | 75% |
| Zaccharie Risacher (DAL) UNDER 1.5 Turnovers | 0.9 | 1.3 | 75% |
| Daniel Gafford (DAL) UNDER 3.5 2-pointers made | 2.7 | 3.4 | 74% |

Combined 41.5%.

Top single leans (over or under, whichever the model prefers):

- Noah Clowney (BKN) UNDER 1.5 Turnovers: 75% (model 0.9 vs recent 1.1)
- Zaccharie Risacher (DAL) UNDER 1.5 Turnovers: 75% (model 0.9 vs recent 1.3)
- Daniel Gafford (DAL) UNDER 3.5 2-pointers made: 74% (model 2.7 vs recent 3.4)
- Nolan Traore (BKN) UNDER 3.5 2-pointers made: 73% (model 2.7 vs recent 3.1)
- Michael Porter Jr. (BKN) UNDER 5.5 Free-throw attempts: 73% (model 4.0 vs recent 5.2)
- Nolan Traore (BKN) UNDER 2.5 Free-throw attempts: 73% (model 1.8 vs recent 2.2)
- Kyrie Irving (DAL) UNDER 5.5 2-pointers made: 73% (model 4.1 vs recent 5.2)
- Julius Randle (BKN) UNDER 7.5 Free-throw attempts: 72% (model 5.6 vs recent 7.2)

## BOS at MIL (game 401909949)

**Best 3-leg parlay for this game:**

| Leg | Model proj | Recent avg | Win prob |
|---|---|---|---|
| Sam Hauser (BOS) UNDER 9.5 Points | 7.2 | 9.4 | 75% |
| AJ Green (MIL) UNDER 12.5 Pts+Reb+Ast | 9.7 | 12.7 | 74% |
| Kyle Kuzma (MIL) UNDER 2.5 Turnovers | 1.7 | 2.1 | 74% |

Combined 41.1%.

Top single leans (over or under, whichever the model prefers):

- Sam Hauser (BOS) UNDER 9.5 Points: 75% (model 7.2 vs recent 9.4)
- AJ Green (MIL) UNDER 12.5 Pts+Reb+Ast: 74% (model 9.7 vs recent 12.7)
- Kyle Kuzma (MIL) UNDER 2.5 Turnovers: 74% (model 1.7 vs recent 2.1)
- Tyler Herro (MIL) UNDER 4.5 2-pointers made: 74% (model 3.5 vs recent 4.2)
- AJ Green (MIL) UNDER 8.5 Points: 74% (model 6.2 vs recent 8.9)
- Kyle Kuzma (MIL) UNDER 8.5 Reb+Ast: 74% (model 6.8 vs recent 8.7)
- Sam Hauser (BOS) UNDER 14.5 Pts+Reb+Ast: 74% (model 11.4 vs recent 14.0)
- Jayson Tatum (BOS) UNDER 34.5 Pts+Ast: 74% (model 26.4 vs recent 34.6)

## NOP at LAC (game 401909950)

**Best 3-leg parlay for this game:**

| Leg | Model proj | Recent avg | Win prob |
|---|---|---|---|
| Zion Williamson (NOP) UNDER 0.5 3-pointers made | 0.3 | 0.3 | 75% |
| Saddiq Bey (NOP) UNDER 22.5 Pts+Reb | 18.2 | 22.2 | 74% |
| Jeremiah Fears (NOP) UNDER 4.5 Free-throw attempts | 3.2 | 4.0 | 74% |

Combined 41.1%.

Top single leans (over or under, whichever the model prefers):

- Zion Williamson (NOP) UNDER 0.5 3-pointers made: 75% (model 0.3 vs recent 0.3)
- Saddiq Bey (NOP) UNDER 22.5 Pts+Reb: 74% (model 18.2 vs recent 22.2)
- Saddiq Bey (NOP) UNDER 24.5 Pts+Reb+Ast: 74% (model 20.1 vs recent 24.2)
- Jeremiah Fears (NOP) UNDER 4.5 Free-throw attempts: 74% (model 3.2 vs recent 4.0)
- Jeremiah Fears (NOP) UNDER 5.5 2-pointers made: 74% (model 4.4 vs recent 5.6)
- Zion Williamson (NOP) UNDER 20.5 Points: 72% (model 17.2 vs recent 20.2)
- Derrick Jones Jr. (LAC) UNDER 1.5 Turnovers: 71% (model 0.9 vs recent 1.2)
- Saddiq Bey (NOP) UNDER 2.5 Assists: 71% (model 1.9 vs recent 2.0)

## MIA at SAC (game 401909951)

**Best 3-leg parlay for this game:**

| Leg | Model proj | Recent avg | Win prob |
|---|---|---|---|
| De'Andre Hunter (SAC) OVER 16.5 Pts+Reb | 20.2 | 16.0 | 75% |
| Davion Mitchell (MIA) UNDER 2.5 3-pointers made | 1.8 | 2.2 | 74% |
| Pelle Larsson (MIA) UNDER 1.5 Steals | 1.0 | 1.3 | 73% |

Combined 40.6%.

Top single leans (over or under, whichever the model prefers):

- De'Andre Hunter (SAC) OVER 16.5 Pts+Reb: 75% (model 20.2 vs recent 16.0)
- Davion Mitchell (MIA) UNDER 2.5 3-pointers made: 74% (model 1.8 vs recent 2.2)
- Davion Mitchell (MIA) UNDER 23.5 Pts+Ast: 74% (model 19.5 vs recent 23.2)
- Pelle Larsson (MIA) UNDER 1.5 Steals: 73% (model 1.0 vs recent 1.3)
- Pelle Larsson (MIA) UNDER 4.5 Assists: 73% (model 3.4 vs recent 4.0)
- Davion Mitchell (MIA) UNDER 15.5 Points: 73% (model 12.5 vs recent 15.7)
- Bobby Portis (MIA) UNDER 6.5 Rebounds: 73% (model 4.8 vs recent 6.8)
- Pelle Larsson (MIA) UNDER 1.5 3-pointers made: 71% (model 1.1 vs recent 1.1)
