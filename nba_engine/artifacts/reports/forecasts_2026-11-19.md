# NBA forecasts for 2026-11-19
Data refresh: last successful run 2026-11-19T21:59:00Z UTC. Model nbaengine-0.1.0.

- GSW at MEM (game 401910019): P(home) sim 0.524 / Elo 0.624; mean score 116.4-115.3 (total 231.8); margin 50% [-9.1, 11.1], 80% [-18.2, 20.2]; total 80% [206.6, 256.4]; P(OT) 0.049; projected final MEM 116 - GSW 115 (the average outcome, not a single exact score).
  - betting line: MEM margin +6.5, total 225.5; our simulator +1.1 (differs by -5.4); line-centred P(home) 0.659.
  - injury-adjusted: P(home) sim 0.524, margin shift +0.5 pts; rotation players listed out: GG Jackson (home), Ty Jerome (home), Stephen Curry (away), Brandon Williams (away).
  - with rest and injuries: P(home) sim 0.533, margin shift +0.9 pts; second night of a back-to-back: home, away.
  - with back-to-back, form and injuries: P(home) sim 0.532, margin shift +0.9 pts; coming off a 10+ point win: neither team.
- POR at MIL (game 401910020): P(home) sim 0.322 / Elo 0.266; mean score 109.3-116.3 (total 225.6); margin 50% [-17.1, 3.1], 80% [-26.2, 12.2]; total 80% [201.7, 250.4]; P(OT) 0.044; projected final POR 116 - MIL 109 (the average outcome, not a single exact score).
  - betting line: MIL margin -10.5, total 229.5; our simulator -7.0 (differs by +3.5); line-centred P(home) 0.240.
  - injury-adjusted: P(home) sim 0.339, margin shift +1.1 pts; rotation players listed out: Ousmane Dieng (home), Vit Krejci (away), Robert Williams III (away), Chris Youngblood (away).
  - with rest and injuries: P(home) sim 0.283, margin shift -1.4 pts; second night of a back-to-back: home.
  - with back-to-back, form and injuries: P(home) sim 0.282, margin shift -1.4 pts; coming off a 10+ point win: neither team.
- NYK at MIN (game 401910021): P(home) sim 0.538 / Elo 0.595; mean score 109.7-108.3 (total 217.9); margin 50% [-8.1, 11.0], 80% [-18.3, 20.0]; total 80% [193.7, 242.4]; P(OT) 0.052; projected final MIN 110 - NYK 108 (the average outcome, not a single exact score).
  - betting line: MIN margin -1.5, total 215.5; our simulator +1.4 (differs by +2.9); line-centred P(home) 0.487.
  - injury-adjusted: P(home) sim 0.538, margin shift -0.0 pts; rotation players listed out: Jaylen Clark (home).
  - with rest and injuries: P(home) sim 0.538, margin shift -0.0 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.538, margin shift -0.0 pts; coming off a 10+ point win: neither team.
- LAC at SAS (game 401910022): P(home) sim 0.725 / Elo 0.881; mean score 116.4-107.8 (total 224.2); margin 50% [-2.3, 19.1], 80% [-10.2, 27.0]; total 80% [199.6, 248.4]; P(OT) 0.042; projected final SAS 116 - LAC 108 (the average outcome, not a single exact score).
  - betting line: SAS margin +15.5, total 225.5; our simulator +8.6 (differs by -6.9); line-centred P(home) 0.862.
  - injury-adjusted: P(home) sim 0.698, margin shift -1.6 pts; rotation players listed out: Dylan Harper (home).
  - with rest and injuries: P(home) sim 0.698, margin shift -1.6 pts; second night of a back-to-back: neither team.
  - with back-to-back, form and injuries: P(home) sim 0.698, margin shift -1.6 pts; coming off a 10+ point win: neither team.

monitor: last 151 completed forecasted games - log loss blend_v2=0.6682, elo=0.6074, elo_all=0.6078, elo_full=0.6254, elo_inj=0.6235, elo_rest=0.6058, elo_sit=0.5967, elo_v2=0.6708, final_v2=0.6877, home_const=0.6980, sim_mc=0.6052, sim_mc_all=0.5919, sim_mc_av=0.6175, sim_mc_avsit=0.6140, sim_mc_full=0.6040, sim_mc_inj=0.6031, sim_mc_mkt=0.6082, sim_mc_raw=0.6087, sim_mc_rest=0.5956, sim_mc_sit=0.5890

Known gaps: injuries come only from ESPN's unofficial list; no confirmed lineups, no travel distance; rest/injury-adjusted lines are separate and experimental (rest effect fitted on 2023-2026 projections, see artifacts/rest_fit.json).