# Trends and streaks report

Projections are walk-forward (each game projected from earlier games only), seasons 2023-2026 (2022 = warm-up). No sportsbook lines exist in this data: 'beat the projection' means better than the model, not a cashed bet.

## 1. Rest: what the model does not know

Home team's margin minus the model's projected margin, regressed on whether each side is on the second night of a back-to-back.

| Seasons | Home team on B2B | Away team on B2B | Games |
|---|---|---|---|
| 2023-24 | -2.15 pts (se 0.78) | +3.11 pts (se 0.71) | 2460 |
| 2025-26 | -2.68 pts (se 0.77) | +2.42 pts (se 0.76) | 2460 |

A negative number means the home team did worse than projected. The same direction and size in both halves is the evidence that this is real. A rest adjustment fitted on 2023-24 improved 2025-26 margin accuracy only slightly (log-loss 0.6104 to 0.6089), so it is a modest, real edge, not a big one.

## 2. League-wide situations (found on 2023-24, re-measured on 2025-26)

16 of the top 25 moved the same direction in the later seasons (a coin flip would give about half). The ones that held are two families: the rest effect, and mismatches (good teams against bad opponents beat the projected margin, bad teams fall short of it, so the model's margins look a little too compressed). The month-of-season rows (for example February totals) flipped sign between the two periods: that is what a luck-only pattern looks like.

| Situation | Outcome | n found | Edge found | n later | Edge later | Held up |
|---|---|---|---|---|---|---|
| proj_total=225-230 & month=Feb | over_total | 146 | -20.5% | 186 | +8.2% | no |
| next_day_game=no game tomorrow & month=Feb | over_total | 546 | -10.3% | 548 | +3.2% | no |
| proj_total=<220 & month=Apr | over_total | 92 | +24.6% | 20 | +10.1% | yes |
| favorite=fav & prev_vs_model=beat model by 8+ | beat_margin | 229 | +15.3% | 280 | +6.3% | yes |
| opp_rest=1d & month=Feb | over_total | 400 | -11.3% | 409 | +6.4% | no |
| rest=1d & month=Feb | over_total | 400 | -11.3% | 409 | +6.4% | no |
| favorite=dog & record=bad team (.400-) | beat_margin | 364 | -11.8% | 408 | -5.2% | yes |
| favorite=fav & opp_record=bad opp (.400-) | beat_margin | 363 | +11.7% | 412 | +5.1% | yes |
| proj_total=<220 & month=Oct | over_total | 62 | +28.1% | 32 | +12.6% | yes |
| prev_ot=prev regulation & month=Feb | over_total | 639 | -8.6% | 654 | +3.5% | no |
| month=Feb | over_total | 674 | -8.4% | 684 | +3.3% | no |
| rest_edge=equal rest & month=Feb | over_total | 390 | -10.8% | 418 | +4.7% | no |
| rest=B2B & prev_result=won close | beat_margin | 195 | -15.1% | 194 | -8.8% | yes |
| proj_pts=<108 & month=Apr | over_total | 73 | +24.7% | 23 | +11.0% | yes |
| rest=B2B & rest_edge=less rest | beat_margin | 599 | -8.5% | 609 | -7.8% | yes |
| opp_rest=B2B & rest_edge=more rest | beat_margin | 599 | +8.5% | 609 | +7.8% | yes |
| rest_edge=equal rest & proj_pts=<108 | over_total | 251 | +12.8% | 253 | -2.1% | no |
| rest=B2B & prev_vs_model=near model | beat_margin | 357 | -10.7% | 404 | -6.9% | yes |
| rest_edge=less rest & prev_vs_model=near model | beat_margin | 495 | -9.1% | 490 | -4.9% | yes |
| month=Feb & part=middle | over_total | 640 | -7.7% | 684 | +3.3% | no |
| rest_edge=less rest & next_day_game=no game tomorrow | beat_margin | 1006 | -6.2% | 981 | -4.7% | yes |
| venue=away & opp_record=bad opp (.400-) | beat_margin | 433 | +9.4% | 548 | +4.3% | yes |
| venue=home & record=bad team (.400-) | beat_margin | 433 | -9.4% | 548 | -4.3% | yes |
| rest=B2B & rest_edge=less rest | win | 599 | -7.5% | 609 | -5.6% | yes |
| opp_rest=B2B & rest_edge=more rest | win | 599 | +7.5% | 609 | +5.6% | yes |

## 3. 'Team A is 22-0 in this spot': how often does luck alone produce that?

Team-specific situations of up to three features with at least 12 games where the team won every game (or lost every game). The luck-only world redraws every result from the model's own win probabilities, so no situation matters by construction.

| Run length | Real data | Luck-only world (average of 20) |
|---|---|---|
| 12+ games | 114 | 73.0 |
| 15+ games | 33 | 25.5 |
| 20+ games | 11 | 4.7 |

The longest perfect run luck alone produced in 20 simulated worlds was 30 games. Spotting a perfect run in a hand-picked spot is therefore weak evidence by itself. The least likely real runs, given who the opponents were:

| Team | Situation | Run | Model's chance of this run |
|---|---|---|---|
| LAL | proj_total=230-235 & opp_record=bad opp (.400-) | 21-0 | 0.0179% |
| UTA | favorite=dog & proj_total=235+ & opp_record=middling opp | 0-18 | 0.0989% |
| DET | favorite=fav & streak=no streak | 20-0 | 0.1012% |
| CHA | opp_rest=1d & favorite=dog & proj_total=220-225 | 0-18 | 0.1816% |
| CHA | opp_rest=1d & favorite=dog & next_day_game=plays tomorrow | 0-17 | 0.1849% |
| DET | favorite=fav & streak=no streak & next_day_game=no game tomorrow | 18-0 | 0.1885% |
| LAL | proj_total=230-235 & next_day_game=no game tomorrow & opp_record=bad opp (.400-) | 16-0 | 0.2629% |
| POR | streak=lost 3+ straight & next_day_game=no game tomorrow & opp_record=good opp (.600+) | 0-15 | 0.2775% |

## 4. Example: home, second night of a back-to-back, projected total above 212.5

| outcome                                            |   n |   hits |   misses |   hit rate |   expected rate |   z (vs expected) |   current run |   longest hit run |
|:---------------------------------------------------|----:|-------:|---------:|-----------:|----------------:|------------------:|--------------:|------------------:|
| won the game                                       | 790 |    393 |      397 |      0.497 |           0.571 |            -4.462 |             1 |                 7 |
| beat the model's projected margin                  | 790 |    353 |      437 |      0.447 |           0.506 |            -3.309 |             1 |                 9 |
| game total went over the model's projected total   | 790 |    388 |      402 |      0.491 |           0.496 |            -0.27  |            -1 |                 7 |
| scored more than the model's projected team points | 790 |    353 |      437 |      0.447 |           0.494 |            -2.657 |            -1 |                 6 |
| won by 10+                                         | 790 |    213 |      577 |      0.27  |           0.308 |            -2.316 |             1 |                 4 |
| game went to overtime                              | 790 |     42 |      748 |      0.053 |           0.05  |             0.354 |           -19 |                 2 |
