- **Us versus the book (all 133 games with a line):** margin miss 11.7 vs 11.3; total miss 14.9 vs 13.9. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Live scoreboard (log-loss, lower is better, 35 finished games with every version):** elo_v2 0.596, blend_v2 0.598, sim_mc 0.604, final_v2 0.609, sim_mc_all 0.610. Small sample, so treat gaps under about 0.03 as noise.
- **Margin bias:** -1.1 ± 1.3 over 134 games, so there is no bias to correct.
- **Total bias:** +1.5 ± 1.7 over 134 games, so there is no bias to correct.
- **How much of today was luck:** 50% of today's games missed by 15+ points (season 31%); pure noise at our error size predicts about 29%. Today was noisier than normal, so do not over-read it.
- **Teams that surprised us:** NOP beat our projection by 24; GSW fell short of our projection by 24; MIA beat our projection by 22. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts +0.86 today, +0.61 season; reb +0.14 today, +0.14 season; ast +0.20 today, +0.10 season; tpm +0.11 today, +0.03 season; stl -0.01 today, +0.06 season; blk +0.02 today, -0.00 season; tov +0.08 today, +0.07 season.
- **Availability:** 0 expected players sat and 13 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our pts projections are too high by 0.61 per player-game (4 standard errors over 1969 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
