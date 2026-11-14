# NBA forecasts for 2026-11-14
Data refresh: last successful run 2026-11-14T15:37:50Z UTC. Model nbaengine-0.1.0.

- DEN at NOP (game 401909980): P(home) sim 0.318 / Elo 0.284; mean score 114.7-121.8 (total 236.4); margin 50% [-17.1, 3.1], 80% [-26.2, 12.2]; total 80% [212.7, 261.4]; P(OT) 0.044; projected final DEN 122 - NOP 115 (the average outcome, not a single exact score).
  - betting line: NOP margin -12.5, total 234.5; our simulator -7.1 (differs by +5.4); line-centred P(home) 0.192.
  - injury-adjusted: P(home) sim 0.231, margin shift -3.1 pts; rotation players listed out: Trey Murphy III (home), Dejounte Murray (home), Trendon Watford (home).
  - with rest and injuries: P(home) sim 0.179, margin shift -5.5 pts; second night of a back-to-back: home.
  - with back-to-back, form and injuries: P(home) sim 0.178, margin shift -5.6 pts; coming off a 10+ point win: neither team.
- DAL at CLE (game 401909981): P(home) sim 0.699 / Elo 0.758; mean score 120.1-112.4 (total 232.5); margin 50% [-2.1, 18.1], 80% [-11.2, 27.2]; total 80% [208.7, 257.4]; P(OT) 0.045; projected final CLE 120 - DAL 112 (the average outcome, not a single exact score).
  - betting line: CLE margin -1.5, total 231.5; our simulator +7.8 (differs by +9.3); line-centred P(home) 0.484.
  - injury-adjusted: P(home) sim 0.690, margin shift -0.3 pts; rotation players listed out: Sam Merrill (home).
  - with rest and injuries: P(home) sim 0.641, margin shift -2.8 pts; second night of a back-to-back: home.
  - with back-to-back, form and injuries: P(home) sim 0.640, margin shift -2.8 pts; coming off a 10+ point win: neither team.
- DET at MIA (game 401909982): P(home) sim 0.363 / Elo 0.378; mean score 112.3-117.5 (total 229.8); margin 50% [-15.1, 5.1], 80% [-24.2, 13.0]; total 80% [205.7, 254.4]; P(OT) 0.050; projected final DET 118 - MIA 112 (the average outcome, not a single exact score).
  - betting line: MIA margin -4.5, total 228.5; our simulator -5.2 (differs by -0.7); line-centred P(home) 0.371.
  - injury-adjusted: P(home) sim 0.363, margin shift -0.0 pts; rotation players listed out: none.
  - with rest and injuries: P(home) sim 0.294, margin shift -2.5 pts; second night of a back-to-back: home.
  - with back-to-back, form and injuries: P(home) sim 0.339, margin shift -0.8 pts; coming off a 10+ point win: home.
- BKN at MEM (game 401909983): P(home) sim 0.682 / Elo 0.733; mean score 115.9-108.7 (total 224.7); margin 50% [-3.1, 17.1], 80% [-12.2, 26.2]; total 80% [200.6, 248.3]; P(OT) 0.046; projected final MEM 116 - BKN 109 (the average outcome, not a single exact score).
  - betting line: MEM margin +3.5, total 228.5; our simulator +7.2 (differs by +3.7); line-centred P(home) 0.608.
  - injury-adjusted: P(home) sim 0.669, margin shift -0.6 pts; rotation players listed out: Scotty Pippen Jr. (home).
  - with rest and injuries: P(home) sim 0.617, margin shift -3.1 pts; second night of a back-to-back: home.
  - with back-to-back, form and injuries: P(home) sim 0.615, margin shift -3.1 pts; coming off a 10+ point win: home, away.
- CHI at MIN (game 401909984): P(home) sim 0.838 / Elo 0.870; mean score 124.1-110.4 (total 234.5); margin 50% [3.9, 24.1], 80% [-5.2, 33.2]; total 80% [209.6, 259.4]; P(OT) 0.035; projected final MIN 124 - CHI 110 (the average outcome, not a single exact score).
  - betting line: MIN margin +15.5, total 235.5; our simulator +13.8 (differs by -1.7); line-centred P(home) 0.868.
  - injury-adjusted: P(home) sim 0.856, margin shift +0.9 pts; rotation players listed out: Caleb Wilson (away).
  - with rest and injuries: P(home) sim 0.898, margin shift +3.7 pts; second night of a back-to-back: away.
  - with back-to-back, form and injuries: P(home) sim 0.918, margin shift +5.4 pts; coming off a 10+ point win: home.

monitor: last 112 completed forecasted games - log loss blend_v2=0.5879, elo=0.5661, elo_all=0.5216, elo_full=0.5601, elo_inj=0.5625, elo_rest=0.5495, elo_sit=0.5251, elo_v2=0.5813, final_v2=0.5360, home_const=0.6893, sim_mc=0.5767, sim_mc_all=0.5256, sim_mc_av=0.5412, sim_mc_avsit=0.5285, sim_mc_full=0.5519, sim_mc_inj=0.5554, sim_mc_mkt=0.5321, sim_mc_raw=0.5852, sim_mc_rest=0.5514, sim_mc_sit=0.5354

Known gaps: injuries come only from ESPN's unofficial list; no confirmed lineups, no travel distance; rest/injury-adjusted lines are separate and experimental (rest effect fitted on 2023-2026 projections, see artifacts/rest_fit.json).