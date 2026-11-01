# NBA forecasts for 2026-11-01
Data refresh: last successful run 2026-11-01T18:44:15Z UTC. Model nbaengine-0.1.0.

- BOS at ORL (game 401909903): P(home) sim 0.372 / Elo 0.458; mean score 110.8-115.7 (total 226.5); margin 50% [-14.0, 4.0], 80% [-21.0, 11.0]; total 80% [204.0, 249.0]; P(OT) 0.023; most frequent exact score 118-117 (rarely hit).
- BKN at IND (game 401909904): P(home) sim 0.636 / Elo 0.681; mean score 118.6-113.3 (total 232.0); margin 50% [-4.0, 14.0], 80% [-12.0, 22.0]; total 80% [209.0, 255.0]; P(OT) 0.022; most frequent exact score 121-112 (rarely hit).
- LAC at GSW (game 401909905): P(home) sim 0.534 / Elo 0.624; mean score 115.4-114.0 (total 229.4); margin 50% [-8.0, 10.0], 80% [-15.0, 18.0]; total 80% [206.0, 253.0]; P(OT) 0.023; most frequent exact score 119-114 (rarely hit).
- TOR at LAL (game 401909906): P(home) sim 0.539 / Elo 0.652; mean score 116.2-114.7 (total 230.9); margin 50% [-7.0, 10.0], 80% [-15.0, 17.0]; total 80% [208.0, 254.0]; P(OT) 0.026; most frequent exact score 116-118 (rarely hit).

monitor: last 17 completed forecasted games - log loss elo=0.6131, home_const=0.6677, sim_mc=0.6614, sim_mc_raw=0.6627
  (fewer than 100 games: too noisy to judge drift)

Known gaps: injuries come only from ESPN's unofficial list (injury-adjusted lines are separate and experimental), no confirmed lineups, no rest/travel features.