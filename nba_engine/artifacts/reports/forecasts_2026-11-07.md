# NBA forecasts for 2026-11-07
Data refresh: last successful run 2026-11-07T15:28:22Z UTC. Model nbaengine-0.1.0.

- DEN at IND (game 401909938): P(home) sim 0.302 / Elo 0.282; mean score 112.6-120.1 (total 232.7); margin 50% [-17.0, 2.1], 80% [-26.0, 11.2]; total 80% [208.6, 257.4]; P(OT) 0.050; most frequent exact score 114-113 (rarely hit).
  - injury-adjusted: P(home) sim 0.234, margin shift -2.4 pts; rotation players listed out: Tyrese Haliburton (home), J. Strawther (away).
  - with rest and injuries: P(home) sim 0.234, margin shift -2.4 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.198, margin shift -4.1 pts; coming off a 10+ point win: away.
- BKN at ATL (game 401909939): P(home) sim 0.806 / Elo 0.859; mean score 117.1-105.0 (total 222.1); margin 50% [3.0, 22.1], 80% [-7.2, 31.2]; total 80% [197.6, 246.4]; P(OT) 0.038; most frequent exact score 121-105 (rarely hit).
  - injury-adjusted: P(home) sim 0.760, margin shift -2.6 pts; rotation players listed out: Jalen Johnson (home), Jock Landale (home), Egor Demin (away).
  - with rest and injuries: P(home) sim 0.696, margin shift -5.0 pts; second night of a back-to-back: home.
  - with back-to-back, form and injuries: P(home) sim 0.647, margin shift -6.7 pts; coming off a 10+ point win: away.
- NYK at CLE (game 401909940): P(home) sim 0.539 / Elo 0.585; mean score 112.6-111.1 (total 223.7); margin 50% [-9.3, 12.1], 80% [-18.3, 20.0]; total 80% [199.7, 248.4]; P(OT) 0.046; most frequent exact score 113-115 (rarely hit).
  - injury-adjusted: P(home) sim 0.539, margin shift +0.3 pts; rotation players listed out: Jaylon Tyson (home), Josh Hart (away).
  - with rest and injuries: P(home) sim 0.490, margin shift -2.2 pts; second night of a back-to-back: home.
  - with back-to-back, form and injuries: P(home) sim 0.490, margin shift -2.2 pts; coming off a 10+ point win: home, away.
- WAS at OKC (game 401909941): P(home) sim 0.883 / Elo 0.899; mean score 121.0-104.8 (total 225.9); margin 50% [7.0, 26.1], 80% [-3.2, 35.2]; total 80% [201.6, 250.4]; P(OT) 0.032; most frequent exact score 125-105 (rarely hit).
  - injury-adjusted: P(home) sim 0.854, margin shift -1.7 pts; rotation players listed out: Chet Holmgren (home), Cason Wallace (home), Jalen Williams (home), Reece Beekman (away), Justin Champagnie (away).
  - with rest and injuries: P(home) sim 0.858, margin shift -1.4 pts; second night of a back-to-back: home, away.
  - with back-to-back, form and injuries: P(home) sim 0.886, margin shift +0.3 pts; coming off a 10+ point win: home.
- ORL at GSW (game 401909942): P(home) sim 0.591 / Elo 0.659; mean score 113.6-109.8 (total 223.4); margin 50% [-6.1, 13.0], 80% [-15.2, 22.0]; total 80% [199.7, 247.4]; P(OT) 0.052; most frequent exact score 110-106 (rarely hit).
  - injury-adjusted: P(home) sim 0.679, margin shift +3.0 pts; rotation players listed out: Paolo Banchero (away), Jalen Suggs (away).
  - with rest and injuries: P(home) sim 0.679, margin shift +3.0 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.730, margin shift +4.6 pts; coming off a 10+ point win: home.
- HOU at PHX (game 401909943): P(home) sim 0.406 / Elo 0.433; mean score 107.5-111.3 (total 218.8); margin 50% [-13.0, 6.1], 80% [-22.0, 15.2]; total 80% [195.7, 242.3]; P(OT) 0.051; most frequent exact score 114-113 (rarely hit).
  - injury-adjusted: P(home) sim 0.407, margin shift +0.7 pts; rotation players listed out: Steven Adams (away), Clint Capela (away).
  - with rest and injuries: P(home) sim 0.407, margin shift +0.7 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.457, margin shift +2.3 pts; coming off a 10+ point win: home.
- SAS at POR (game 401909944): P(home) sim 0.448 / Elo 0.439; mean score 112.7-115.0 (total 227.7); margin 50% [-12.1, 8.1], 80% [-21.2, 16.0]; total 80% [203.7, 252.4]; P(OT) 0.051; most frequent exact score 115-114 (rarely hit).
  - injury-adjusted: P(home) sim 0.370, margin shift -2.8 pts; rotation players listed out: Vit Krejci (home), Ja Morant (home), S. Sharpe (home).
  - with rest and injuries: P(home) sim 0.381, margin shift -2.5 pts; second night of a back-to-back: home, away.
  - with back-to-back, form and injuries: P(home) sim 0.329, margin shift -4.2 pts; coming off a 10+ point win: away.

monitor: last 61 completed forecasted games - log loss elo=0.5895, elo_all=0.5471, elo_full=0.6124, elo_inj=0.6161, elo_rest=0.5658, elo_sit=0.5257, home_const=0.6901, sim_mc=0.5930, sim_mc_all=0.5246, sim_mc_full=0.5708, sim_mc_inj=0.5765, sim_mc_raw=0.5995, sim_mc_rest=0.5484, sim_mc_sit=0.5172
  (fewer than 100 games: too noisy to judge drift)

Known gaps: injuries come only from ESPN's unofficial list; no confirmed lineups, no travel distance; rest/injury-adjusted lines are separate and experimental (rest effect fitted on 2023-2026 projections, see artifacts/rest_fit.json).