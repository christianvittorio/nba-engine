# Season replay: 123 games, 2026-10-20 to 2026-11-05

Every game forecast from the model state before its day, then the real result and box score compared. Start state rebuilt from seasons 2022-2026 (ESPN results); 2000 simulations per game. No injury information is replayed, and these replay forecasts are not the immutable live forecasts (those only exist for games forecast before tip-off).

## 1. Who wins

| model | winner right | accuracy | Brier | log-loss |
|---|---|---|---|---|
| Simulator | 84/123 | 68.3% | 0.2123 | 0.6104 |
| Elo | 77/123 | 62.6% | 0.2239 | 0.6343 |
| Simulator + back-to-back | 82/123 | 66.7% | 0.2105 | 0.6061 |
| Simulator + back-to-back + form | 82/123 | 66.7% | 0.2088 | 0.6020 |
| Simulator + availability (who actually played) | 79/123 | 64.2% | 0.2150 | 0.6150 |
| Simulator + availability + back-to-back + form | 80/123 | 65.0% | 0.2118 | 0.6068 |
| Home-court constant | 64/123 | 52.0% | 0.2507 | 0.6945 |

Home teams won 52.0% of games; the simulator expected 55.6%.

## 2. Scores

| quantity | predicted avg | actual avg | bias | MAE |
|---|---|---|---|---|
| Home points | 115.7 | 114.3 | -1.40 | 9.77 |
| Away points | 113.4 | 112.5 | -0.98 | 9.73 |
| Total points | 229.1 | 226.8 | -2.38 | 15.06 |
| Margin (home - away) | 2.3 | 1.9 | -0.41 | 11.37 |
| Total points, with availability | 227.9 | 226.8 | -1.16 | 14.72 |
| Margin, with availability | 2.2 | 1.9 | -0.33 | 11.51 |
| Possessions | 100.0 | 102.4 | +2.40 | 4.37 |

For comparison, always guessing the season-to-date average (226.8 total) would give a total MAE of 15.38 and always guessing the average margin a margin MAE of 12.99 (that comparison uses the full set of results, so it flatters the baseline).

Predicted ranges that actually contained the result (nominal 50% / 80%): 50% margin: 48.8%; 80% margin: 78.0%; 50% total: 47.2%; 80% total: 81.3%.

Overtime: the simulator said 2.2%; 5.7% of these games went to overtime. Three-pointers made per game 26.3, attempts 75.6, free-throw attempts 50.7, turnovers 30.5, offensive rebounds 24.2 (actual, both teams).

### Biggest margin misses

| date | game | predicted (home-away) | actual (home-away) | P(home) | winner right? | margin error | total error |
|---|---|---|---|---|---|---|---|
| 2026-10-23 | ATL at CHA | 115-112 | 81-128 | 57% | NO | -50 | -18 |
| 2026-10-21 | PHX at POR | 113-110 | 124-83 | 57% | yes | +39 | -16 |
| 2026-10-21 | CHI at TOR | 121-112 | 135-92 | 76% | yes | +34 | -6 |
| 2026-10-28 | OKC at DAL | 110-120 | 120-96 | 26% | NO | +33 | -14 |
| 2026-10-29 | MEM at POR | 121-112 | 103-124 | 74% | NO | -30 | -7 |
| 2026-11-02 | DET at CHA | 104-108 | 91-124 | 40% | yes | -29 | +3 |
| 2026-10-26 | GSW at DEN | 120-112 | 114-134 | 71% | NO | -28 | +16 |
| 2026-10-25 | IND at BKN | 114-114 | 109-136 | 49% | yes | -27 | +17 |
| 2026-10-21 | MIN at MIA | 120-119 | 106-131 | 52% | NO | -26 | -1 |
| 2026-10-31 | ATL at NOP | 117-120 | 121-99 | 42% | NO | +25 | -17 |

### Biggest total misses

| date | game | predicted (home-away) | actual (home-away) | P(home) | winner right? | margin error | total error |
|---|---|---|---|---|---|---|---|
| 2026-10-22 | DEN at OKC | 118-114 | 96-84 | 61% | yes | +8 | -52 |
| 2026-10-30 | CHA at WAS | 109-115 | 95-79 | 34% | NO | +22 | -50 |
| 2026-10-28 | DEN at NOP | 119-122 | 91-104 | 42% | yes | -10 | -46 |
| 2026-10-24 | NOP at DEN | 121-114 | 141-135 | 70% | yes | -2 | +41 |
| 2026-10-28 | LAL at LAC | 115-115 | 87-103 | 48% | yes | -16 | -40 |
| 2026-11-01 | BKN at IND | 115-111 | 90-98 | 60% | NO | -12 | -39 |
| 2026-10-27 | POR at LAL | 116-113 | 129-136 | 57% | NO | -10 | +36 |
| 2026-10-28 | CHA at DET | 113-109 | 97-89 | 60% | yes | +4 | -35 |
| 2026-10-31 | POR at UTA | 115-121 | 90-112 | 36% | yes | -17 | -34 |
| 2026-10-24 | GSW at PHX | 111-109 | 131-122 | 56% | yes | +7 | +33 |

### Every game

| date | game | predicted (home-away) | actual (home-away) | P(home) | winner right? | margin error | total error |
|---|---|---|---|---|---|---|---|
| 2026-10-20 | BOS at DET | 112-109 | 121-113 | 56% | yes | +5 | +13 |
| 2026-10-20 | PHI at NYK | 116-109 | 100-106 | 68% | NO | -13 | -19 |
| 2026-10-20 | OKC at SAS | 116-114 | 104-116 | 55% | NO | -14 | -10 |
| 2026-10-21 | MIN at MIA | 120-119 | 106-131 | 52% | NO | -26 | -1 |
| 2026-10-21 | GSW at LAL | 117-111 | 127-105 | 64% | yes | +16 | +4 |
| 2026-10-21 | ATL at ORL | 116-117 | 125-132 | 47% | yes | -6 | +24 |
| 2026-10-21 | MIL at WAS | 116-116 | 128-116 | 51% | yes | +12 | +12 |
| 2026-10-21 | CHA at BKN | 104-114 | 103-110 | 23% | yes | +3 | -5 |
| 2026-10-21 | CHI at TOR | 121-112 | 135-92 | 76% | yes | +34 | -6 |
| 2026-10-21 | UTA at MEM | 123-123 | 123-103 | 52% | yes | +19 | -20 |
| 2026-10-21 | IND at NOP | 121-116 | 120-123 | 63% | NO | -8 | +6 |
| 2026-10-21 | DAL at HOU | 120-111 | 128-110 | 75% | yes | +9 | +8 |
| 2026-10-21 | PHX at POR | 113-110 | 124-83 | 57% | yes | +39 | -16 |
| 2026-10-21 | SAC at LAC | 118-110 | 121-96 | 73% | yes | +17 | -11 |
| 2026-10-22 | CLE at PHI | 115-116 | 114-106 | 46% | NO | +10 | -11 |
| 2026-10-22 | DEN at OKC | 118-114 | 96-84 | 61% | yes | +8 | -52 |
| 2026-10-23 | NYK at BOS | 109-107 | 107-103 | 56% | yes | +2 | -6 |
| 2026-10-23 | HOU at SAS | 114-112 | 110-114 | 57% | NO | -7 | -2 |
| 2026-10-23 | ATL at CHA | 115-112 | 81-128 | 57% | NO | -50 | -18 |
| 2026-10-23 | DAL at IND | 119-117 | 105-121 | 56% | NO | -18 | -10 |
| 2026-10-23 | MIN at ORL | 115-116 | 93-115 | 49% | yes | -21 | -22 |
| 2026-10-23 | TOR at WAS | 111-120 | 102-112 | 26% | yes | -1 | -16 |
| 2026-10-23 | DET at MIA | 114-119 | 111-128 | 38% | yes | -12 | +5 |
| 2026-10-23 | CHI at MIL | 117-115 | 125-132 | 55% | NO | -9 | +25 |
| 2026-10-23 | NOP at UTA | 120-123 | 120-119 | 43% | NO | +4 | -4 |
| 2026-10-23 | MEM at GSW | 119-114 | 108-111 | 61% | NO | -7 | -14 |
| 2026-10-23 | LAC at LAL | 113-110 | 125-117 | 56% | yes | +5 | +19 |
| 2026-10-23 | POR at SAC | 109-118 | 120-128 | 29% | yes | +0 | +21 |
| 2026-10-24 | MIA at CHA | 118-112 | 115-110 | 62% | yes | -0 | -5 |
| 2026-10-24 | BKN at CLE | 117-105 | 125-121 | 81% | yes | -8 | +24 |
| 2026-10-24 | MIL at PHI | 117-109 | 127-116 | 70% | yes | +3 | +17 |
| 2026-10-24 | HOU at ATL | 114-113 | 114-121 | 53% | NO | -8 | +7 |
| 2026-10-24 | WAS at CHI | 122-120 | 120-124 | 57% | NO | -7 | +2 |
| 2026-10-24 | SAS at DAL | 114-120 | 106-122 | 33% | yes | -9 | -6 |
| 2026-10-24 | NOP at DEN | 121-114 | 141-135 | 70% | yes | -2 | +41 |
| 2026-10-24 | GSW at PHX | 111-109 | 131-122 | 56% | yes | +7 | +33 |
| 2026-10-25 | LAL at UTA | 116-124 | 123-132 | 30% | yes | -1 | +14 |
| 2026-10-25 | IND at BKN | 114-114 | 109-136 | 49% | yes | -27 | +17 |
| 2026-10-25 | ORL at NYK | 115-109 | 102-111 | 68% | NO | -16 | -11 |
| 2026-10-25 | TOR at MIN | 114-114 | 117-94 | 52% | yes | +22 | -17 |
| 2026-10-25 | LAC at OKC | 115-108 | 108-101 | 68% | yes | +0 | -14 |
| 2026-10-25 | DET at PHI | 113-117 | 93-106 | 39% | yes | -8 | -31 |
| 2026-10-25 | MEM at SAC | 118-119 | 112-123 | 46% | yes | -9 | -2 |
| 2026-10-26 | WAS at CHA | 120-110 | 110-103 | 75% | yes | -3 | -17 |
| 2026-10-26 | MIN at CLE | 116-116 | 127-125 | 51% | yes | +2 | +20 |
| 2026-10-26 | CHI at BOS | 122-109 | 134-99 | 82% | yes | +22 | +2 |
| 2026-10-26 | DAL at MIA | 123-118 | 109-113 | 64% | NO | -9 | -19 |
| 2026-10-26 | IND at MIL | 117-117 | 110-102 | 51% | yes | +8 | -21 |
| 2026-10-26 | PHX at OKC | 114-105 | 125-114 | 74% | yes | +2 | +20 |
| 2026-10-26 | ATL at HOU | 117-114 | 120-110 | 55% | yes | +8 | -1 |
| 2026-10-26 | MEM at UTA | 123-123 | 105-110 | 48% | yes | -5 | -31 |
| 2026-10-26 | GSW at DEN | 120-112 | 114-134 | 71% | NO | -28 | +16 |
| 2026-10-27 | BKN at BOS | 116-102 | 125-124 | 85% | yes | -14 | +31 |
| 2026-10-27 | DET at NYK | 109-111 | 111-97 | 44% | NO | +16 | -12 |
| 2026-10-27 | SAC at SAS | 122-108 | 130-103 | 86% | yes | +12 | +3 |
| 2026-10-27 | POR at LAL | 116-113 | 129-136 | 57% | NO | -10 | +36 |
| 2026-10-28 | MIA at ATL | 123-116 | 117-129 | 65% | NO | -18 | +7 |
| 2026-10-28 | WAS at CLE | 124-113 | 121-111 | 75% | yes | -0 | -5 |
| 2026-10-28 | CHA at DET | 113-109 | 97-89 | 60% | yes | +4 | -35 |
| 2026-10-28 | PHI at IND | 115-117 | 109-114 | 43% | yes | -3 | -9 |
| 2026-10-28 | ORL at TOR | 116-110 | 129-99 | 65% | yes | +24 | +2 |
| 2026-10-28 | NYK at CHI | 111-120 | 127-133 | 26% | yes | +3 | +30 |
| 2026-10-28 | HOU at MIL | 109-118 | 100-132 | 26% | yes | -23 | +6 |
| 2026-10-28 | GSW at MIN | 119-112 | 114-119 | 68% | NO | -12 | +2 |
| 2026-10-28 | DEN at NOP | 119-122 | 91-104 | 42% | yes | -10 | -46 |
| 2026-10-28 | SAS at UTA | 116-125 | 111-117 | 28% | yes | +3 | -12 |
| 2026-10-28 | OKC at DAL | 110-120 | 120-96 | 26% | NO | +33 | -14 |
| 2026-10-28 | LAL at LAC | 115-115 | 87-103 | 48% | yes | -16 | -40 |
| 2026-10-29 | CLE at ATL | 119-116 | 114-111 | 55% | yes | +1 | -10 |
| 2026-10-29 | SAC at NOP | 121-114 | 132-120 | 68% | yes | +5 | +18 |
| 2026-10-29 | MEM at POR | 121-112 | 103-124 | 74% | NO | -30 | -7 |
| 2026-10-30 | CHA at WAS | 109-115 | 95-79 | 34% | NO | +22 | -50 |
| 2026-10-30 | CHI at BOS | 123-109 | 125-111 | 83% | yes | +1 | +4 |
| 2026-10-30 | DET at BKN | 103-115 | 94-110 | 20% | yes | -4 | -14 |
| 2026-10-30 | NYK at PHI | 110-112 | 98-93 | 47% | NO | +6 | -31 |
| 2026-10-30 | ORL at TOR | 117-108 | 114-121 | 72% | NO | -15 | +10 |
| 2026-10-30 | IND at MIA | 122-116 | 145-125 | 65% | yes | +14 | +32 |
| 2026-10-30 | HOU at DAL | 112-119 | 116-111 | 32% | NO | +12 | -4 |
| 2026-10-30 | LAC at MIN | 114-110 | 127-101 | 61% | yes | +22 | +4 |
| 2026-10-30 | LAL at GSW | 114-117 | 112-95 | 43% | NO | +20 | -24 |
| 2026-10-30 | DEN at PHX | 111-114 | 120-127 | 44% | yes | -5 | +22 |
| 2026-10-31 | POR at UTA | 115-121 | 90-112 | 36% | yes | -17 | -34 |
| 2026-10-31 | PHI at CHA | 109-106 | 104-109 | 56% | NO | -8 | -2 |
| 2026-10-31 | ATL at NOP | 117-120 | 121-99 | 42% | NO | +25 | -17 |
| 2026-10-31 | SAC at MEM | 122-114 | 136-105 | 71% | yes | +23 | +5 |
| 2026-10-31 | CLE at MIL | 112-119 | 111-136 | 31% | yes | -17 | +16 |
| 2026-10-31 | MIN at SAS | 115-113 | 121-111 | 56% | yes | +8 | +4 |
| 2026-10-31 | OKC at HOU | 111-110 | 119-98 | 53% | yes | +20 | -4 |
| 2026-11-01 | BOS at ORL | 109-114 | 97-108 | 38% | yes | -6 | -17 |
| 2026-11-01 | BKN at IND | 115-111 | 90-98 | 60% | NO | -12 | -39 |
| 2026-11-01 | LAC at GSW | 113-110 | 124-112 | 57% | yes | +9 | +14 |
| 2026-11-01 | TOR at LAL | 113-112 | 131-125 | 53% | yes | +5 | +32 |
| 2026-11-02 | OKC at CLE | 114-113 | 112-117 | 53% | NO | -6 | +2 |
| 2026-11-02 | DET at CHA | 104-108 | 91-124 | 40% | yes | -29 | +3 |
| 2026-11-02 | ATL at IND | 114-119 | 104-108 | 37% | yes | +1 | -22 |
| 2026-11-02 | BKN at NYK | 113-102 | 103-90 | 79% | yes | +2 | -21 |
| 2026-11-02 | WAS at ORL | 117-112 | 94-103 | 63% | NO | -14 | -32 |
| 2026-11-02 | CHI at PHI | 121-112 | 126-107 | 72% | yes | +10 | -0 |
| 2026-11-02 | SAC at DAL | 121-113 | 100-115 | 72% | NO | -23 | -19 |
| 2026-11-02 | NOP at MEM | 119-118 | 134-135 | 53% | NO | -2 | +32 |
| 2026-11-02 | MIL at MIN | 121-107 | 112-100 | 83% | yes | -1 | -16 |
| 2026-11-02 | BOS at HOU | 111-109 | 109-93 | 54% | yes | +14 | -17 |
| 2026-11-02 | UTA at SAS | 123-109 | 119-97 | 85% | yes | +8 | -17 |
| 2026-11-02 | POR at DEN | 116-114 | 110-118 | 56% | NO | -11 | -2 |
| 2026-11-02 | PHX at GSW | 114-111 | 116-113 | 58% | yes | -0 | +4 |
| 2026-11-02 | TOR at LAC | 110-113 | 118-125 | 42% | yes | -4 | +21 |
| 2026-11-02 | MIA at LAL | 121-116 | 138-117 | 62% | yes | +16 | +17 |
| 2026-11-04 | PHI at DET | 113-105 | 106-112 | 71% | NO | -14 | +0 |
| 2026-11-04 | ATL at WAS | 113-117 | 105-120 | 39% | yes | -11 | -5 |
| 2026-11-04 | MIL at BOS | 118-104 | 109-102 | 85% | yes | -7 | -10 |
| 2026-11-04 | CHA at BKN | 103-106 | 114-104 | 41% | NO | +14 | +9 |
| 2026-11-04 | CHI at NYK | 120-107 | 135-105 | 83% | yes | +17 | +13 |
| 2026-11-04 | IND at MEM | 119-114 | 103-107 | 63% | NO | -9 | -24 |
| 2026-11-04 | UTA at NOP | 122-115 | 120-113 | 69% | yes | -1 | -4 |
| 2026-11-04 | CLE at OKC | 114-112 | 124-116 | 57% | yes | +5 | +14 |
| 2026-11-04 | MIN at HOU | 113-109 | 107-117 | 60% | NO | -14 | +2 |
| 2026-11-04 | TOR at DEN | 115-113 | 128-109 | 52% | yes | +18 | +9 |
| 2026-11-04 | POR at PHX | 111-113 | 119-132 | 43% | yes | -11 | +27 |
| 2026-11-04 | DAL at SAS | 120-109 | 112-111 | 79% | yes | -10 | -6 |
| 2026-11-04 | LAL at SAC | 112-121 | 103-116 | 26% | yes | -4 | -14 |
| 2026-11-04 | MIA at LAC | 117-117 | 116-117 | 50% | yes | -2 | -1 |
| 2026-11-05 | ORL at PHX | 112-110 | 117-104 | 55% | yes | +11 | -1 |
| 2026-11-05 | MIA at GSW | 120-116 | 120-100 | 59% | yes | +16 | -17 |

## 3. Team by team

| team | games | wins | expected wins | points vs proj | allowed vs proj |
|---|---|---|---|---|---|
| SAS | 8 | 6 | 5.6 | -2.6 | -3.1 |
| LAL | 9 | 7 | 5.5 | +4.3 | +0.6 |
| BOS | 8 | 6 | 5.4 | -0.6 | +0.5 |
| CHA | 9 | 3 | 5.3 | -14.0 | +0.7 |
| HOU | 9 | 7 | 5.3 | +3.1 | -3.8 |
| NYK | 8 | 4 | 5.1 | -3.9 | -3.3 |
| DET | 8 | 6 | 5.1 | -2.4 | -6.5 |
| MIN | 9 | 6 | 5.0 | +3.2 | -5.9 |
| ATL | 9 | 5 | 4.9 | -1.6 | -2.3 |
| TOR | 8 | 4 | 4.9 | +2.2 | +1.9 |
| OKC | 8 | 6 | 4.7 | -4.7 | -2.5 |
| CLE | 8 | 4 | 4.7 | +2.4 | +3.7 |
| PHI | 9 | 8 | 4.3 | -1.6 | -8.1 |
| MIA | 9 | 3 | 4.2 | -1.5 | +3.6 |
| GSW | 9 | 6 | 4.2 | +4.1 | -2.0 |
| NOP | 8 | 4 | 4.2 | +2.3 | +0.9 |
| MEM | 8 | 6 | 4.1 | +1.4 | -8.9 |
| POR | 7 | 6 | 4.1 | +5.8 | -2.2 |
| IND | 9 | 3 | 4.0 | -4.5 | -3.3 |
| DEN | 7 | 4 | 4.0 | -1.9 | +0.3 |
| LAC | 8 | 1 | 3.7 | -3.1 | +2.0 |
| ORL | 8 | 2 | 3.4 | -6.2 | +0.2 |
| PHX | 7 | 2 | 3.1 | +3.7 | +9.1 |
| DAL | 8 | 4 | 2.9 | -1.8 | -7.0 |
| WAS | 8 | 4 | 2.8 | -4.0 | -9.8 |
| UTA | 8 | 1 | 2.8 | -9.3 | -4.1 |
| MIL | 8 | 1 | 2.7 | -1.2 | +4.8 |
| CHI | 8 | 1 | 2.3 | -0.6 | +9.2 |
| SAC | 8 | 1 | 2.3 | -2.9 | +2.9 |
| BKN | 8 | 2 | 2.3 | +1.2 | -1.1 |

Small samples (a handful of games per team): differences of a few points are noise.

## 4. Player stats

### Lineup unknown (what the daily job stores): every rostered rotation player, 0 if they did not play

| stat | n | forecast avg | actual avg | bias | MAE | MAE last-10 avg | 50% range | 80% range |
|---|---|---|---|---|---|---|---|---|
| min | 3435 | 15.95 | 14.98 | -0.969 | 8.91 | 11.19 | 66.3% | 86.7% |
| pts | 3435 | 7.69 | 7.13 | -0.555 | 5.19 | 6.71 | 69.8% | 90.2% |
| reb | 3435 | 2.91 | 2.75 | -0.164 | 2.07 | 2.67 | 73.6% | 91.6% |
| ast | 3435 | 1.76 | 1.68 | -0.089 | 1.37 | 1.76 | 79.1% | 93.4% |
| stl | 3435 | 0.56 | 0.53 | -0.032 | 0.61 | 0.76 | 86.2% | 94.4% |
| blk | 3435 | 0.32 | 0.31 | -0.014 | 0.41 | 0.49 | 88.2% | 95.2% |
| tov | 3435 | 0.94 | 0.95 | +0.017 | 0.88 | 1.09 | 80.8% | 93.2% |
| tpm | 3435 | 0.88 | 0.83 | -0.058 | 0.83 | 1.03 | 83.7% | 94.1% |
| pra | 3435 | 12.36 | 11.55 | -0.807 | 7.67 | 9.94 | 68.5% | 88.5% |

### Told who actually played (minutes shared among them): players who played

| stat | n | forecast avg | actual avg | bias | MAE | MAE last-10 avg | 50% range | 80% range |
|---|---|---|---|---|---|---|---|---|
| min | 2705 | 21.79 | 21.67 | -0.119 | 5.16 | 5.81 | 45.8% | 76.4% |
| pts | 2705 | 10.33 | 10.20 | -0.128 | 4.63 | 5.06 | 52.5% | 82.0% |
| reb | 2705 | 4.04 | 3.96 | -0.075 | 1.88 | 2.00 | 64.1% | 87.5% |
| ast | 2705 | 2.39 | 2.36 | -0.031 | 1.33 | 1.42 | 71.6% | 90.8% |
| stl | 2705 | 0.78 | 0.76 | -0.014 | 0.71 | 0.74 | 85.1% | 93.7% |
| blk | 2705 | 0.45 | 0.45 | +0.003 | 0.51 | 0.52 | 85.9% | 94.7% |
| tov | 2705 | 1.32 | 1.37 | +0.045 | 0.94 | 1.00 | 76.4% | 92.4% |
| tpm | 2705 | 1.18 | 1.18 | +0.002 | 0.91 | 0.93 | 77.7% | 93.1% |
| pra | 2705 | 16.76 | 16.52 | -0.234 | 6.10 | 6.72 | 49.5% | 77.4% |

### Players furthest from their points projection (5+ games, told who played)

Under-delivering:

| name | games | forecast | actual | diff |
|---|---|---|---|---|
| Ousmane Dieng | 5 | 8.8 | 1.4 | -7.4 |
| Nique Clifford | 6 | 7.4 | 0.3 | -7.1 |
| Will Riley | 5 | 7.6 | 0.8 | -6.8 |
| Jaden Hardy | 5 | 6.8 | 1.0 | -5.8 |
| Daeqwon Plowden | 5 | 8.0 | 2.2 | -5.8 |
| DeMar DeRozan | 5 | 14.8 | 10.2 | -4.6 |
| Jerami Grant | 7 | 13.3 | 8.9 | -4.5 |
| Dennis Schroder | 8 | 13.5 | 9.1 | -4.4 |

Over-delivering:

| name | games | forecast | actual | diff |
|---|---|---|---|---|
| Luka Doncic | 7 | 27.8 | 40.0 | +12.2 |
| Stephen Curry | 6 | 19.7 | 31.0 | +11.3 |
| Victor Wembanyama | 7 | 22.5 | 31.4 | +8.9 |
| Tyrese Maxey | 8 | 20.8 | 28.0 | +7.2 |
| Jamal Murray | 6 | 22.3 | 28.7 | +6.4 |
| Isaiah Stewart | 6 | 6.9 | 13.2 | +6.3 |
| Mikel Brown Jr. | 5 | 6.9 | 13.2 | +6.3 |
| Davion Mitchell | 8 | 10.7 | 16.8 | +6.0 |
