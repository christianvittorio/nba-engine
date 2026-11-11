- **Us versus the book (all 88 games with a line):** margin miss 11.8 vs 11.1; total miss 15.2 vs 13.9. The book is closer on totals, so our totals should be pulled toward the line. The book is closer on margins.
- **Margin bias:** -1.0 ± 1.6 over 89 games, so there is no bias to correct.
- **Total bias:** we have been too high by 4.6 on average over 89 games (2.3 standard errors).
- **How much of today was luck:** 67% of today's games missed by 15+ points (season 34%); pure noise at our error size predicts about 29%. Today was noisier than normal, so do not over-read it.
- **Teams that surprised us:** POR beat our projection by 25; OKC fell short of our projection by 25; PHX beat our projection by 22. Elo and the team profiles absorb these results automatically tomorrow; a single result moves a rating only a few points.
- **Player projections (projection minus actual, per player-game):** pts +0.64 today, +0.93 season; reb +0.20 today, +0.17 season; ast +0.10 today, +0.17 season; tpm -0.06 today, +0.07 season; stl +0.19 today, +0.10 season; blk +0.10 today, +0.01 season; tov +0.16 today, +0.08 season.
- **Availability:** 0 expected players sat and 10 unexpected players played today. Each miss feeds the play-probability calibration automatically.

**What changes next:**

- Use the market-centred total (`sim_mc_mkt`) for total bets; our own total has been less accurate than the line.
- Our ast projections are too high by 0.17 per player-game (3 standard errors over 1072 player-games): shift the ast ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Our pts projections are too high by 0.93 per player-game (5 standard errors over 1072 player-games): shift the pts ladders by that amount before pricing over/unders. (Ladder calibration covers part of this automatically; the rest is a pending change.)
- Already automatic: Elo ratings, team style profiles, player rates, the scoring-level correction, and the ladder and play-probability calibration all update from today's results.
- Pending (see `miss_analysis_2026-11-11.md`): refit Elo's home advantage (80 to about 45), stretch win probabilities, blend with Elo, correct the points projection bias.
