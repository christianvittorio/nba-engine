- **Us versus the book (all 169 games with a line):** margin miss 11.4 vs 10.9; total miss 15.5 vs 14.3. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Live scoreboard (log-loss, lower is better, 71 finished games with every version):** elo_v2 0.638, blend_v2 0.639, sim_mc 0.645, sim_mc_all 0.661, final_v2 0.662. Small sample, so treat gaps under about 0.03 as noise.
- **Margin bias:** -0.1 ± 1.1 over 170 games, so there is no bias to correct.
- **Total bias:** +2.2 ± 1.5 over 170 games, so there is no bias to correct.
- **How much of today was luck:** 17% of today's games missed by 15+ points (season 29%); pure noise at our error size predicts about 29%. Today was no worse than normal variance.
- **Teams that surprised us:** SAC beat our projection by 15; BOS fell short of our projection by 15; DAL beat our projection by 11. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts +0.85 today, +0.66 season; reb -0.65 today, +0.14 season; ast +0.37 today, +0.12 season; tpm +0.18 today, +0.04 season; stl +0.09 today, +0.06 season; blk -0.10 today, +0.01 season; tov +0.06 today, +0.04 season.
- **Availability:** 0 expected players sat and 4 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our pts projections are too high by 0.66 per player-game (6 standard errors over 2689 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
