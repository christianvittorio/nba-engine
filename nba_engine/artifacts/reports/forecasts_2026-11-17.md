# NBA forecasts for 2026-11-17
Data refresh: last successful run 2026-11-17T22:01:09Z UTC. Model nbaengine-0.1.0.

- NYK at TOR (game 401910002): P(home) sim 0.439 / Elo 0.465; mean score 107.2-109.5 (total 216.7); margin 50% [-12.0, 8.3], 80% [-21.0, 17.3]; total 80% [192.7, 241.4]; P(OT) 0.049; projected final NYK 109 - TOR 107 (the average outcome, not a single exact score).
  - betting line: TOR margin -3.5, total 214.5; our simulator -2.2 (differs by +1.3); line-centred P(home) 0.411.
  - injury-adjusted: P(home) sim 0.439, margin shift -0.0 pts; rotation players listed out: none.
  - with rest and injuries: P(home) sim 0.439, margin shift +0.0 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.439, margin shift +0.0 pts; coming off a 10+ point win: neither team.
- POR at MIN (game 401910003): P(home) sim 0.629 / Elo 0.654; mean score 116.0-110.9 (total 226.8); margin 50% [-5.1, 15.1], 80% [-14.2, 24.2]; total 80% [202.6, 251.4]; P(OT) 0.048; projected final MIN 116 - POR 111 (the average outcome, not a single exact score).
  - betting line: MIN margin +1.5, total 227.5; our simulator +5.1 (differs by +3.6); line-centred P(home) 0.553.
  - injury-adjusted: P(home) sim 0.631, margin shift +0.1 pts; rotation players listed out: Jaylen Clark (home), Vit Krejci (away), Chris Youngblood (away).
  - with rest and injuries: P(home) sim 0.639, margin shift +0.5 pts; second night of a back-to-back: home, away.
  - with back-to-back, form and injuries: P(home) sim 0.639, margin shift +0.4 pts; coming off a 10+ point win: neither team.
- DET at SAS (game 401910004): P(home) sim 0.576 / Elo 0.704; mean score 113.7-110.6 (total 224.4); margin 50% [-7.1, 13.1], 80% [-15.0, 22.2]; total 80% [200.7, 248.4]; P(OT) 0.047; projected final SAS 114 - DET 111 (the average outcome, not a single exact score).
  - betting line: SAS margin +9.5, total 222.5; our simulator +3.1 (differs by -6.4); line-centred P(home) 0.739.
  - injury-adjusted: P(home) sim 0.605, margin shift +1.1 pts; rotation players listed out: Ronald Holland II (away), Taurean Prince (away), Duncan Robinson (away).
  - with rest and injuries: P(home) sim 0.605, margin shift +1.1 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.605, margin shift +1.1 pts; coming off a 10+ point win: neither team.
- UTA at LAC (game 401910006): P(home) sim 0.747 / Elo 0.813; mean score 120.0-110.7 (total 230.7); margin 50% [-2.3, 19.1], 80% [-9.0, 28.2]; total 80% [206.7, 255.4]; P(OT) 0.042; projected final LAC 120 - UTA 111 (the average outcome, not a single exact score).
  - betting line: LAC margin +6.5, total 225.5; our simulator +9.2 (differs by +2.7); line-centred P(home) 0.700.
  - injury-adjusted: P(home) sim 0.814, margin shift +2.9 pts; rotation players listed out: Jaxson Hayes (away), Lauri Markkanen (away).
  - with rest and injuries: P(home) sim 0.814, margin shift +2.9 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.814, margin shift +2.9 pts; coming off a 10+ point win: neither team.
- CHA at LAL (game 401910005): P(home) sim 0.679 / Elo 0.795; mean score 114.6-107.5 (total 222.1); margin 50% [-3.1, 17.1], 80% [-11.0, 26.2]; total 80% [197.6, 246.4]; P(OT) 0.044; projected final LAL 115 - CHA 107 (the average outcome, not a single exact score).
  - betting line: LAL margin +7.5, total 221.5; our simulator +7.1 (differs by -0.4); line-centred P(home) 0.694.
  - injury-adjusted: P(home) sim 0.619, margin shift -2.8 pts; rotation players listed out: Walker Kessler (home), Austin Reaves (home), Kon Knueppel (away), Dennis Schroder (away).
  - with rest and injuries: P(home) sim 0.619, margin shift -2.8 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.619, margin shift -2.8 pts; coming off a 10+ point win: neither team.

monitor: last 134 completed forecasted games - log loss blend_v2=0.5978, elo=0.5744, elo_all=0.5552, elo_full=0.5812, elo_inj=0.5775, elo_rest=0.5678, elo_sit=0.5529, elo_v2=0.5962, final_v2=0.6092, home_const=0.6924, sim_mc=0.5810, sim_mc_all=0.5512, sim_mc_av=0.5642, sim_mc_avsit=0.5628, sim_mc_full=0.5691, sim_mc_inj=0.5672, sim_mc_mkt=0.5675, sim_mc_raw=0.5880, sim_mc_rest=0.5663, sim_mc_sit=0.5555

Known gaps: injuries come only from ESPN's unofficial list; no confirmed lineups, no travel distance; rest/injury-adjusted lines are separate and experimental (rest effect fitted on 2023-2026 projections, see artifacts/rest_fit.json).