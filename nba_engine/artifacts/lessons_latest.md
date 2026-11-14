- **Us versus the book (all 111 games with a line):** margin miss 11.8 vs 11.1; total miss 14.8 vs 13.7. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Live scoreboard (log-loss, lower is better, 13 finished games with every version):** final_v2 0.536, sim_mc_all 0.560, elo_v2 0.581, blend_v2 0.588, sim_mc 0.606. Small sample, so treat gaps under about 0.03 as noise.
- **Margin bias:** -1.2 ± 1.4 over 112 games, so there is no bias to correct.
- **Total bias:** +2.9 ± 1.8 over 112 games, so there is no bias to correct.
- **How much of today was luck:** 22% of today's games missed by 15+ points (season 30%); pure noise at our error size predicts about 29%. Today was no worse than normal variance.
- **Teams that surprised us:** NOP fell short of our projection by 32; MEM beat our projection by 32; SAS beat our projection by 31. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts +0.33 today, +0.69 season; reb -0.13 today, +0.17 season; ast +0.06 today, +0.14 season; tpm -0.02 today, +0.02 season; stl +0.08 today, +0.08 season; blk -0.03 today, -0.01 season; tov +0.15 today, +0.09 season.
- **Availability:** 0 expected players sat and 10 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our pts projections are too high by 0.69 per player-game (5 standard errors over 1533 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
