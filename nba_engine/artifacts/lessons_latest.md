- **Us versus the book (all 138 games with a line):** margin miss 11.7 vs 11.4; total miss 14.9 vs 13.9. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Live scoreboard (log-loss, lower is better, 40 finished games with every version):** sim_mc 0.620, blend_v2 0.622, elo_v2 0.624, sim_mc_all 0.637, final_v2 0.645. Small sample, so treat gaps under about 0.03 as noise.
- **Margin bias:** -0.6 ± 1.3 over 139 games, so there is no bias to correct.
- **Total bias:** +1.7 ± 1.6 over 139 games, so there is no bias to correct.
- **How much of today was luck:** 40% of today's games missed by 15+ points (season 32%); pure noise at our error size predicts about 29%. Today was no worse than normal variance.
- **Teams that surprised us:** LAC fell short of our projection by 34; UTA beat our projection by 34; SAS fell short of our projection by 15. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts +0.66 today, +0.61 season; reb -0.14 today, +0.13 season; ast +0.13 today, +0.10 season; tpm -0.06 today, +0.02 season; stl +0.07 today, +0.06 season; blk +0.06 today, +0.00 season; tov +0.01 today, +0.07 season.
- **Availability:** 0 expected players sat and 5 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our pts projections are too high by 0.61 per player-game (5 standard errors over 2067 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
