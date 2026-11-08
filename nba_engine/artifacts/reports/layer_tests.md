# Layer tests: 5054 stored games, 2022-10-18 to 2026-11-06 
## 1. Market closing line vs our model (1039 games with both) 
- Margin error (MAE): market close 11.050, market open 11.271, our model 11.685
- Total error (MAE): market close 14.625, our model 15.130
- Win log-loss: market 0.5697, our model 0.6099
- Margin blend: actual - market = -0.092 x (model - market), standard error 0.097  (0 = the market already contains everything our model knows)
- Blended margin MAE 11.033
- Total blend: actual - market total = 0.069 x (model - market), standard error 0.107
- Line movement: actual - open = 1.20 x (close - open), standard error 0.18  (1 = the move fully reflects new information; 0 = noise)
 | |our margin differs from market by| games | market MAE | our MAE | our side beat the closing line | |---|---|---|---|---|
| (0.0, 1.5] | 295 | 11.03 | 11.08 | 48.1% |
| (1.5, 3.0] | 252 | 11.41 | 11.70 | 46.8% |
| (3.0, 5.0] | 223 | 11.10 | 11.39 | 51.6% |
| (5.0, 100.0] | 264 | 10.60 | 12.53 | 48.9% |
 ## 2. Quarters (5047 games) 
- First-quarter share of regulation points 0.2532 (sd 0.0314); first-half share 0.5046 (sd 0.0383). A 0.75x first-quarter pace would be a 0.19 share; the data shows 0.25.
- Average points by quarter (both teams): Q1 57.7, Q2 57.3, Q3 57.9, Q4 55.1
 ## 3. Officials (5054 games) 
- fouls: a game's crew average of OTHER games predicts this game's fouls with slope 2.10 (se 0.18); crew averages range 39.7 to 45.2 (league 41.9)
- free_throws: a game's crew average of OTHER games predicts this game's free_throws with slope 1.75 (se 0.21); crew averages range 42.9 to 48.6 (league 45.3)
- Total points error of our model vs the crew's free-throw tendency: +0.16 points per extra free throw of crew average, se 0.81 (1034 games). Crew free-throw average sd 0.73
- Same against the market total: +0.12 (se 0.78) -> the market already prices the crew
 ## 4. Lineups (5054 games with starters) 
- Lineup stints 268664; minutes captured per team-game 48.0 of 48 (should be 48)
- Best five-man lineups so far (min 10 minutes):  29 11m +120.9, 3 13m +115.1, 2 11m +107.7, 11 11m +106.0, 22 13m +103.9
 ## 5. Shot quality by zone (849434 shots) 
- Next-game points per shot ~ 0.64 x team's recent actual + -0.01 x team's recent shot-quality (zone mix at league zone accuracy); se 0.04 and 0.07. Shot quality carries real information when its coefficient is clearly above zero.
- Correlation of next-game points/shot with: recent actual 0.175, recent shot-quality 0.008