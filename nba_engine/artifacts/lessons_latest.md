- **Us versus the book (all 186 games with a line):** margin miss 11.2 vs 10.7; total miss 15.6 vs 14.4. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Live scoreboard (log-loss, lower is better, 88 finished games with every version):** elo_v2 0.646, blend_v2 0.647, sim_mc 0.655, final_v2 0.664, sim_mc_all 0.667. Small sample, so treat gaps under about 0.03 as noise.
- **Margin bias:** -0.5 ± 1.1 over 187 games, so there is no bias to correct.
- **Total bias:** +1.7 ± 1.4 over 187 games, so there is no bias to correct.
- **How much of today was luck:** 20% of today's games missed by 15+ points (season 28%); pure noise at our error size predicts about 29%. Today was no worse than normal variance.
- **Teams that surprised us:** CHI beat our projection by 20; CLE fell short of our projection by 20; PHI fell short of our projection by 18. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts +0.60 today, +0.64 season; reb +0.10 today, +0.12 season; ast +0.07 today, +0.10 season; tpm +0.06 today, +0.03 season; stl +0.08 today, +0.05 season; blk -0.03 today, +0.01 season; tov +0.13 today, +0.04 season.
- **Availability:** 0 expected players sat and 28 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our pts projections are too high by 0.64 per player-game (6 standard errors over 3039 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
