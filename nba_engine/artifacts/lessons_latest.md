- **Us versus the book (all 125 games with a line):** margin miss 11.6 vs 11.2; total miss 14.9 vs 13.9. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Live scoreboard (log-loss, lower is better, 27 finished games with every version):** elo_v2 0.536, blend_v2 0.543, final_v2 0.545, sim_mc_all 0.559, sim_mc 0.562. Small sample, so treat gaps under about 0.03 as noise.
- **Margin bias:** -1.3 ± 1.3 over 126 games, so there is no bias to correct.
- **Total bias:** +1.7 ± 1.7 over 126 games, so there is no bias to correct.
- **How much of today was luck:** 22% of today's games missed by 15+ points (season 30%); pure noise at our error size predicts about 29%. Today was no worse than normal variance.
- **Teams that surprised us:** BOS beat our projection by 25; DAL fell short of our projection by 25; WAS fell short of our projection by 16. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts +0.33 today, +0.58 season; reb +0.03 today, +0.15 season; ast -0.11 today, +0.09 season; tpm -0.02 today, +0.02 season; stl -0.02 today, +0.07 season; blk +0.05 today, -0.01 season; tov -0.07 today, +0.07 season.
- **Availability:** 0 expected players sat and 10 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our pts projections are too high by 0.58 per player-game (4 standard errors over 1802 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
