- **Us versus the book (all 98 games with a line):** margin miss 11.6 vs 11.0; total miss 14.8 vs 13.5. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Margin bias:** -0.5 ± 1.5 over 99 games, so there is no bias to correct.
- **Total bias:** we have been too high by 3.9 on average over 99 games (2.1 standard errors).
- **How much of today was luck:** 10% of today's games missed by 15+ points (season 31%); pure noise at our error size predicts about 29%. Today was no worse than normal variance.
- **Teams that surprised us:** NOP fell short of our projection by 41; BKN beat our projection by 41; POR beat our projection by 14. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts +0.09 today, +0.79 season; reb +0.43 today, +0.21 season; ast +0.11 today, +0.17 season; tpm -0.12 today, +0.04 season; stl +0.03 today, +0.09 season; blk -0.08 today, -0.00 season; tov +0.11 today, +0.09 season.
- **Availability:** 0 expected players sat and 8 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our ast projections are too high by 0.17 per player-game (3 standard errors over 1271 player-games): shift the ast ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Our pts projections are too high by 0.79 per player-game (5 standard errors over 1271 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Our reb projections are too high by 0.21 per player-game (3 standard errors over 1271 player-games): shift the reb ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
