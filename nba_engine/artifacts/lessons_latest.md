- **Us versus the book (all 154 games with a line):** margin miss 11.7 vs 11.3; total miss 14.8 vs 13.6. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Live scoreboard (log-loss, lower is better, 56 finished games with every version):** blend_v2 0.655, elo_v2 0.656, sim_mc 0.657, sim_mc_all 0.669, final_v2 0.672. Small sample, so treat gaps under about 0.03 as noise.
- **Margin bias:** -0.1 ± 1.2 over 155 games, so there is no bias to correct.
- **Total bias:** +1.6 ± 1.5 over 155 games, so there is no bias to correct.
- **How much of today was luck:** 25% of today's games missed by 15+ points (season 32%); pure noise at our error size predicts about 29%. Today was no worse than normal variance.
- **Teams that surprised us:** MEM beat our projection by 27; GSW fell short of our projection by 27; MIN fell short of our projection by 4. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts +0.27 today, +0.62 season; reb +0.34 today, +0.18 season; ast +0.12 today, +0.10 season; tpm +0.09 today, +0.02 season; stl -0.24 today, +0.05 season; blk +0.05 today, +0.01 season; tov -0.45 today, +0.04 season.
- **Availability:** 0 expected players sat and 6 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our pts projections are too high by 0.62 per player-game (5 standard errors over 2397 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Our reb projections are too high by 0.18 per player-game (3 standard errors over 2397 player-games): shift the reb ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
