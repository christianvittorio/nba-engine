# NBA forecasts for 2026-11-12
Data refresh: last successful run 2026-11-12T17:24:45Z UTC. Model nbaengine-0.1.0.

- TOR at PHI (game 401909976): P(home) sim 0.508 / Elo 0.652; mean score 110.9-110.5 (total 221.4); margin 50% [-9.1, 10.0], 80% [-18.2, 19.0]; total 80% [197.7, 245.4]; P(OT) 0.047; projected final PHI 111 - TOR 111 (the average outcome, not a single exact score).
  - betting line: PHI margin +8.5, total 223.5; our simulator +0.4 (differs by -8.1); line-centred P(home) 0.711.
  - injury-adjusted: P(home) sim 0.563, margin shift +2.0 pts; rotation players listed out: Adem Bona (home), Scottie Barnes (away).
  - with rest and injuries: P(home) sim 0.639, margin shift +4.8 pts; second night of a back-to-back: away.
  - with back-to-back, form and injuries: P(home) sim 0.640, margin shift +4.8 pts; coming off a 10+ point win: neither team.
- DET at WAS (game 401909977): P(home) sim 0.161 / Elo 0.198; mean score 105.5-119.2 (total 224.7); margin 50% [-24.1, -3.9], 80% [-32.0, 5.2]; total 80% [200.7, 248.4]; P(OT) 0.035; projected final DET 119 - WAS 105 (the average outcome, not a single exact score).
  - betting line: WAS margin -10.5, total 220.5; our simulator -13.7 (differs by -3.2); line-centred P(home) 0.208.
  - injury-adjusted: P(home) sim 0.152, margin shift -0.3 pts; rotation players listed out: Justin Champagnie (home), Isaiah Joe (away).
  - with rest and injuries: P(home) sim 0.109, margin shift -2.8 pts; second night of a back-to-back: home.
  - with back-to-back, form and injuries: P(home) sim 0.089, margin shift -4.5 pts; coming off a 10+ point win: away.
- DAL at MIN (game 401909978): P(home) sim 0.718 / Elo 0.798; mean score 118.0-109.6 (total 227.7); margin 50% [-2.1, 18.1], 80% [-11.2, 27.2]; total 80% [203.7, 251.5]; P(OT) 0.041; projected final MIN 118 - DAL 110 (the average outcome, not a single exact score).
  - betting line: MIN margin +5.5, total 226.5; our simulator +8.4 (differs by +2.9); line-centred P(home) 0.665.
  - injury-adjusted: P(home) sim 0.665, margin shift -2.6 pts; rotation players listed out: Anthony Edwards (home), Sergio de Larrea (away).
  - with rest and injuries: P(home) sim 0.665, margin shift -2.6 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.695, margin shift -0.9 pts; coming off a 10+ point win: home.
- CHA at PHX (game 401909979): P(home) sim 0.543 / Elo 0.630; mean score 108.3-106.9 (total 215.2); margin 50% [-8.1, 11.0], 80% [-17.2, 20.0]; total 80% [190.6, 239.4]; P(OT) 0.046; projected final PHX 108 - CHA 107 (the average outcome, not a single exact score).
  - betting line: PHX margin +6.5, total 214.5; our simulator +1.5 (differs by -5.0); line-centred P(home) 0.664.
  - injury-adjusted: P(home) sim 0.568, margin shift +1.1 pts; rotation players listed out: Kon Knueppel (away), Dennis Schroder (away).
  - with rest and injuries: P(home) sim 0.568, margin shift +1.1 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.568, margin shift +1.1 pts; coming off a 10+ point win: home, away.

monitor: last 99 completed forecasted games - log loss elo=0.5688, elo_all=0.5265, elo_full=0.5650, elo_inj=0.5656, elo_rest=0.5527, elo_sit=0.5302, home_const=0.6955, sim_mc=0.5728, sim_mc_all=0.5186, sim_mc_av=0.5208, sim_mc_avsit=0.5174, sim_mc_full=0.5473, sim_mc_inj=0.5491, sim_mc_mkt=0.5239, sim_mc_raw=0.5815, sim_mc_rest=0.5445, sim_mc_sit=0.5283
  (fewer than 100 games: too noisy to judge drift)

Known gaps: injuries come only from ESPN's unofficial list; no confirmed lineups, no travel distance; rest/injury-adjusted lines are separate and experimental (rest effect fitted on 2023-2026 projections, see artifacts/rest_fit.json).