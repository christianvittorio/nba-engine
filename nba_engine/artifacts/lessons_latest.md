- **Us versus the book (all 102 games with a line):** margin miss 11.7 vs 11.0; total miss 15.1 vs 13.9. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Margin bias:** -1.0 ± 1.5 over 103 games, so there is no bias to correct.
- **Total bias:** +3.2 ± 1.9 over 103 games, so there is no bias to correct.
- **How much of today was luck:** 25% of today's games missed by 15+ points (season 31%); pure noise at our error size predicts about 29%. Today was no worse than normal variance.
- **Teams that surprised us:** MIN beat our projection by 31; DAL fell short of our projection by 31; PHI beat our projection by 11. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts -0.07 today, +0.74 season; reb +0.18 today, +0.21 season; ast -0.15 today, +0.15 season; tpm -0.06 today, +0.03 season; stl +0.02 today, +0.09 season; blk -0.03 today, -0.01 season; tov -0.01 today, +0.08 season.
- **Availability:** 0 expected players sat and 4 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our pts projections are too high by 0.74 per player-game (5 standard errors over 1353 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Our reb projections are too high by 0.21 per player-game (3 standard errors over 1353 player-games): shift the reb ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
