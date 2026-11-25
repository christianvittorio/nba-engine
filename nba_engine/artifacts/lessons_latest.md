- **Us versus the book (all 189 games with a line):** margin miss 11.3 vs 10.8; total miss 15.7 vs 14.6. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Live scoreboard (log-loss, lower is better, 91 finished games with every version):** elo_v2 0.647, blend_v2 0.648, sim_mc 0.655, final_v2 0.666, sim_mc_all 0.667. Small sample, so treat gaps under about 0.03 as noise.
- **Margin bias:** -0.2 ± 1.1 over 190 games, so there is no bias to correct.
- **Total bias:** +1.8 ± 1.4 over 190 games, so there is no bias to correct.
- **How much of today was luck:** 33% of today's games missed by 15+ points (season 28%); pure noise at our error size predicts about 29%. Today was no worse than normal variance.
- **Teams that surprised us:** DEN fell short of our projection by 27; DAL beat our projection by 27; ORL fell short of our projection by 14. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts +0.63 today, +0.64 season; reb +0.11 today, +0.12 season; ast +0.15 today, +0.11 season; tpm -0.10 today, +0.03 season; stl +0.04 today, +0.05 season; blk -0.02 today, +0.01 season; tov -0.06 today, +0.04 season.
- **Availability:** 0 expected players sat and 2 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our pts projections are too high by 0.64 per player-game (6 standard errors over 3101 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
