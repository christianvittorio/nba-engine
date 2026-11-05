# NBA forecasts for 2026-11-05
Data refresh: last successful run 2026-11-05T20:56:08Z UTC. Model nbaengine-0.1.0.

- ORL at PHX (game 401909936): P(home) sim 0.536 / Elo 0.616; mean score 110.9-109.4 (total 220.4); margin 50% [-8.1, 11.0], 80% [-17.2, 20.0]; total 80% [196.7, 244.4]; P(OT) 0.044; most frequent exact score 103-105 (rarely hit).
  - injury-adjusted: P(home) sim 0.573, margin shift +1.8 pts; rotation players listed out: M. Williams (home), Paolo Banchero (away), Jalen Suggs (away).
  - with rest and injuries: P(home) sim 0.536, margin shift -0.7 pts; second night of a back-to-back: home.
  - with back-to-back, form and injuries: P(home) sim 0.536, margin shift -0.7 pts; coming off a 10+ point win: neither team.
- MIA at GSW (game 401909937): P(home) sim 0.547 / Elo 0.628; mean score 118.2-116.1 (total 234.2); margin 50% [-8.1, 12.1], 80% [-17.2, 21.2]; total 80% [209.6, 259.4]; P(OT) 0.052; most frequent exact score 113-118 (rarely hit).
  - injury-adjusted: P(home) sim 0.547, margin shift -0.6 pts; rotation players listed out: Gui Santos (home).
  - with rest and injuries: P(home) sim 0.601, margin shift +2.2 pts; second night of a back-to-back: away.
  - with back-to-back, form and injuries: P(home) sim 0.603, margin shift +2.3 pts; coming off a 10+ point win: neither team.

monitor: last 50 completed forecasted games - log loss elo=0.6307, elo_all=0.6632, elo_full=0.6876, elo_inj=0.6925, elo_rest=0.6270, elo_sit=0.6309, home_const=0.6903, sim_mc=0.6268, sim_mc_all=0.6074, sim_mc_full=0.6243, sim_mc_inj=0.6312, sim_mc_raw=0.6306, sim_mc_rest=0.5906, sim_mc_sit=0.5889
  (fewer than 100 games: too noisy to judge drift)

Known gaps: injuries come only from ESPN's unofficial list; no confirmed lineups, no travel distance; rest/injury-adjusted lines are separate and experimental (rest effect fitted on 2023-2026 projections, see artifacts/rest_fit.json).