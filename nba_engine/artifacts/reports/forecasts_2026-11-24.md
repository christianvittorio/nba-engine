# NBA forecasts for 2026-11-24
Data refresh: last successful run 2026-11-24T23:24:23Z UTC. Model nbaengine-0.1.0.

- DET at ORL (game 401909314): P(home) sim 0.395 / Elo 0.386; mean score 107.3-111.4 (total 218.7); margin 50% [-14.1, 6.1], 80% [-23.2, 14.0]; total 80% [194.7, 242.4]; P(OT) 0.045; projected final DET 111 - ORL 107 (the average outcome, not a single exact score).
  - betting line: ORL margin -2.5, total 212.5; our simulator -4.1 (differs by -1.6); line-centred P(home) 0.416.
  - injury-adjusted: P(home) sim 0.396, margin shift +1.0 pts; rotation players listed out: Ebuka Okorie (away), Taurean Prince (away), Duncan Robinson (away).
  - with rest and injuries: P(home) sim 0.396, margin shift +1.0 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.396, margin shift +1.0 pts; coming off a 10+ point win: neither team.
- BOS at WAS (game 401909315): P(home) sim 0.196 / Elo 0.248; mean score 103.0-114.9 (total 217.8); margin 50% [-22.1, -3.0], 80% [-31.2, 7.2]; total 80% [193.6, 242.4]; P(OT) 0.037; projected final BOS 115 - WAS 103 (the average outcome, not a single exact score).
  - betting line: WAS margin -11.5, total 218.5; our simulator -11.9 (differs by -0.4); line-centred P(home) 0.205.
  - injury-adjusted: P(home) sim 0.209, margin shift +0.5 pts; rotation players listed out: Mitchell Robinson (away).
  - with rest and injuries: P(home) sim 0.209, margin shift +0.5 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.237, margin shift +2.2 pts; coming off a 10+ point win: home.
- DAL at DEN (game 401909316): P(home) sim 0.714 / Elo 0.786; mean score 120.0-112.2 (total 232.2); margin 50% [-2.1, 18.1], 80% [-11.2, 26.0]; total 80% [207.6, 257.4]; P(OT) 0.045; projected final DEN 120 - DAL 112 (the average outcome, not a single exact score).
  - betting line: DEN margin +8.5, total 234.5; our simulator +7.8 (differs by -0.7); line-centred P(home) 0.731.
  - injury-adjusted: P(home) sim 0.718, margin shift +0.1 pts; rotation players listed out: Tobi Lawal (away).
  - with rest and injuries: P(home) sim 0.718, margin shift +0.1 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.718, margin shift +0.1 pts; coming off a 10+ point win: neither team.

monitor: last 187 completed forecasted games - log loss blend_v2=0.6473, elo=0.6061, elo_all=0.6090, elo_full=0.6216, elo_inj=0.6183, elo_rest=0.6071, elo_sit=0.6018, elo_v2=0.6460, final_v2=0.6643, home_const=0.6925, sim_mc=0.6113, sim_mc_all=0.6050, sim_mc_av=0.6239, sim_mc_avsit=0.6247, sim_mc_full=0.6124, sim_mc_inj=0.6104, sim_mc_mkt=0.6026, sim_mc_raw=0.6137, sim_mc_rest=0.6061, sim_mc_sit=0.6035

Known gaps: injuries come only from ESPN's unofficial list; no confirmed lineups, no travel distance; rest/injury-adjusted lines are separate and experimental (rest effect fitted on 2023-2026 projections, see artifacts/rest_fit.json).