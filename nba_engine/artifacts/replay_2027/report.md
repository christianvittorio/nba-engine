# Season replay: 107 games, 2026-10-20 to 2026-11-02

Every game forecast from the model state before its day, then the real result and box score compared. Start state rebuilt from seasons 2022-2026 (ESPN results); 2000 simulations per game. No injury information is replayed, and these replay forecasts are not the immutable live forecasts (those only exist for games forecast before tip-off).

## 1. Who wins

| model | winner right | accuracy | Brier | log-loss |
|---|---|---|---|---|
| Simulator | 70/107 | 65.4% | 0.2164 | 0.6188 |
| Elo | 67/107 | 62.6% | 0.2249 | 0.6371 |
| Simulator + back-to-back | 70/107 | 65.4% | 0.2150 | 0.6154 |
| Simulator + back-to-back + form | 69/107 | 64.5% | 0.2125 | 0.6099 |
| Home-court constant | 55/107 | 51.4% | 0.2514 | 0.6959 |

Home teams won 51.4% of games; the simulator expected 55.2%.

## 2. Scores

| quantity | predicted avg | actual avg | bias | MAE |
|---|---|---|---|---|
| Home points | 115.7 | 114.2 | -1.44 | 10.04 |
| Away points | 113.6 | 112.6 | -0.97 | 10.30 |
| Total points | 229.2 | 226.8 | -2.41 | 15.82 |
| Margin (home - away) | 2.1 | 1.6 | -0.47 | 11.74 |
| Possessions | 99.1 | 102.4 | +3.26 | 4.87 |

For comparison, always guessing the season-to-date average (226.8 total) would give a total MAE of 16.26 and always guessing the average margin a margin MAE of 13.30 (that comparison uses the full set of results, so it flatters the baseline).

Predicted ranges that actually contained the result (nominal 50% / 80%): 50% margin: 49.5%; 80% margin: 77.6%; 50% total: 43.0%; 80% total: 79.4%.

Overtime: the simulator said 2.2%; 4.7% of these games went to overtime. Three-pointers made per game 26.4, attempts 75.7, free-throw attempts 50.4, turnovers 30.7, offensive rebounds 24.2 (actual, both teams).

### Biggest margin misses

| date | game | predicted (home-away) | actual (home-away) | P(home) | winner right? | margin error | total error |
|---|---|---|---|---|---|---|---|
| 2026-10-23 | ATL at CHA | 115-112 | 81-128 | 56% | NO | -49 | -18 |
| 2026-10-21 | PHX at POR | 112-111 | 124-83 | 54% | yes | +40 | -16 |
| 2026-10-28 | OKC at DAL | 109-121 | 120-96 | 19% | NO | +36 | -14 |
| 2026-10-21 | CHI at TOR | 121-112 | 135-92 | 74% | yes | +34 | -6 |
| 2026-11-02 | DET at CHA | 106-109 | 91-124 | 41% | yes | -29 | -0 |
| 2026-10-29 | MEM at POR | 121-113 | 103-124 | 70% | NO | -29 | -7 |
| 2026-10-26 | GSW at DEN | 120-113 | 114-134 | 68% | NO | -27 | +15 |
| 2026-10-31 | ATL at NOP | 116-121 | 121-99 | 39% | NO | +26 | -17 |
| 2026-10-25 | IND at BKN | 113-114 | 109-136 | 47% | yes | -26 | +18 |
| 2026-10-21 | MIN at MIA | 119-118 | 106-131 | 53% | NO | -26 | +0 |

### Biggest total misses

| date | game | predicted (home-away) | actual (home-away) | P(home) | winner right? | margin error | total error |
|---|---|---|---|---|---|---|---|
| 2026-10-30 | CHA at WAS | 109-117 | 95-79 | 29% | NO | +24 | -52 |
| 2026-10-22 | DEN at OKC | 119-113 | 96-84 | 66% | yes | +6 | -52 |
| 2026-10-28 | DEN at NOP | 118-123 | 91-104 | 38% | yes | -8 | -46 |
| 2026-10-24 | NOP at DEN | 123-114 | 141-135 | 74% | yes | -3 | +40 |
| 2026-10-28 | LAL at LAC | 115-113 | 87-103 | 53% | NO | -17 | -38 |
| 2026-11-01 | BKN at IND | 115-110 | 90-98 | 64% | NO | -13 | -37 |
| 2026-10-27 | POR at LAL | 116-113 | 129-136 | 59% | NO | -11 | +36 |
| 2026-10-28 | CHA at DET | 113-108 | 97-89 | 66% | yes | +3 | -36 |
| 2026-10-31 | POR at UTA | 116-122 | 90-112 | 34% | yes | -16 | -35 |
| 2026-10-27 | BKN at BOS | 116-99 | 125-124 | 89% | yes | -15 | +34 |

### Every game

| date | game | predicted (home-away) | actual (home-away) | P(home) | winner right? | margin error | total error |
|---|---|---|---|---|---|---|---|
| 2026-10-20 | BOS at DET | 111-109 | 121-113 | 54% | yes | +7 | +14 |
| 2026-10-20 | PHI at NYK | 116-108 | 100-106 | 71% | NO | -14 | -19 |
| 2026-10-20 | OKC at SAS | 115-114 | 104-116 | 50% | yes | -12 | -9 |
| 2026-10-21 | MIN at MIA | 119-118 | 106-131 | 53% | NO | -26 | +0 |
| 2026-10-21 | GSW at LAL | 116-112 | 127-105 | 63% | yes | +17 | +4 |
| 2026-10-21 | ATL at ORL | 116-116 | 125-132 | 48% | yes | -6 | +25 |
| 2026-10-21 | MIL at WAS | 115-117 | 128-116 | 46% | NO | +14 | +12 |
| 2026-10-21 | CHA at BKN | 103-113 | 103-110 | 23% | yes | +3 | -3 |
| 2026-10-21 | CHI at TOR | 121-112 | 135-92 | 74% | yes | +34 | -6 |
| 2026-10-21 | UTA at MEM | 125-122 | 123-103 | 57% | yes | +17 | -20 |
| 2026-10-21 | IND at NOP | 121-117 | 120-123 | 60% | NO | -7 | +5 |
| 2026-10-21 | DAL at HOU | 120-110 | 128-110 | 75% | yes | +8 | +9 |
| 2026-10-21 | PHX at POR | 112-111 | 124-83 | 54% | yes | +40 | -16 |
| 2026-10-21 | SAC at LAC | 118-109 | 121-96 | 76% | yes | +15 | -10 |
| 2026-10-22 | CLE at PHI | 114-117 | 114-106 | 43% | NO | +11 | -11 |
| 2026-10-22 | DEN at OKC | 119-113 | 96-84 | 66% | yes | +6 | -52 |
| 2026-10-23 | NYK at BOS | 109-105 | 107-103 | 60% | yes | +0 | -4 |
| 2026-10-23 | HOU at SAS | 114-111 | 110-114 | 57% | NO | -7 | -1 |
| 2026-10-23 | ATL at CHA | 115-112 | 81-128 | 56% | NO | -49 | -18 |
| 2026-10-23 | DAL at IND | 119-117 | 105-121 | 54% | NO | -18 | -10 |
| 2026-10-23 | MIN at ORL | 113-114 | 93-115 | 50% | NO | -22 | -19 |
| 2026-10-23 | TOR at WAS | 110-120 | 102-112 | 23% | yes | -0 | -16 |
| 2026-10-23 | DET at MIA | 114-117 | 111-128 | 40% | yes | -13 | +8 |
| 2026-10-23 | CHI at MIL | 117-116 | 125-132 | 51% | NO | -8 | +24 |
| 2026-10-23 | NOP at UTA | 120-122 | 120-119 | 45% | NO | +3 | -4 |
| 2026-10-23 | MEM at GSW | 119-114 | 108-111 | 62% | NO | -8 | -14 |
| 2026-10-23 | LAC at LAL | 113-110 | 125-117 | 56% | yes | +6 | +19 |
| 2026-10-23 | POR at SAC | 110-117 | 120-128 | 34% | yes | -2 | +21 |
| 2026-10-24 | MIA at CHA | 116-112 | 115-110 | 60% | yes | +1 | -3 |
| 2026-10-24 | BKN at CLE | 118-104 | 125-121 | 83% | yes | -10 | +24 |
| 2026-10-24 | MIL at PHI | 116-109 | 127-116 | 69% | yes | +4 | +18 |
| 2026-10-24 | HOU at ATL | 114-113 | 114-121 | 52% | NO | -8 | +8 |
| 2026-10-24 | WAS at CHI | 124-117 | 120-124 | 67% | NO | -11 | +3 |
| 2026-10-24 | SAS at DAL | 113-121 | 106-122 | 30% | yes | -9 | -6 |
| 2026-10-24 | NOP at DEN | 123-114 | 141-135 | 74% | yes | -3 | +40 |
| 2026-10-24 | GSW at PHX | 111-109 | 131-122 | 56% | yes | +7 | +34 |
| 2026-10-25 | LAL at UTA | 116-124 | 123-132 | 28% | yes | -1 | +14 |
| 2026-10-25 | IND at BKN | 113-114 | 109-136 | 47% | yes | -26 | +18 |
| 2026-10-25 | ORL at NYK | 115-108 | 102-111 | 68% | NO | -16 | -11 |
| 2026-10-25 | TOR at MIN | 114-112 | 117-94 | 55% | yes | +21 | -16 |
| 2026-10-25 | LAC at OKC | 116-108 | 108-101 | 71% | yes | -1 | -14 |
| 2026-10-25 | DET at PHI | 112-117 | 93-106 | 39% | yes | -8 | -30 |
| 2026-10-25 | MEM at SAC | 119-119 | 112-123 | 49% | yes | -10 | -3 |
| 2026-10-26 | WAS at CHA | 120-108 | 110-103 | 82% | yes | -5 | -16 |
| 2026-10-26 | MIN at CLE | 117-116 | 127-125 | 55% | yes | +0 | +19 |
| 2026-10-26 | CHI at BOS | 122-108 | 134-99 | 83% | yes | +22 | +3 |
| 2026-10-26 | DAL at MIA | 123-116 | 109-113 | 69% | NO | -11 | -18 |
| 2026-10-26 | IND at MIL | 117-116 | 110-102 | 52% | yes | +7 | -20 |
| 2026-10-26 | PHX at OKC | 115-105 | 125-114 | 77% | yes | +1 | +19 |
| 2026-10-26 | ATL at HOU | 117-114 | 120-110 | 56% | yes | +7 | -1 |
| 2026-10-26 | MEM at UTA | 122-123 | 105-110 | 47% | yes | -4 | -31 |
| 2026-10-26 | GSW at DEN | 120-113 | 114-134 | 68% | NO | -27 | +15 |
| 2026-10-27 | BKN at BOS | 116-99 | 125-124 | 89% | yes | -15 | +34 |
| 2026-10-27 | DET at NYK | 110-110 | 111-97 | 48% | NO | +15 | -12 |
| 2026-10-27 | SAC at SAS | 123-108 | 130-103 | 85% | yes | +13 | +2 |
| 2026-10-27 | POR at LAL | 116-113 | 129-136 | 59% | NO | -11 | +36 |
| 2026-10-28 | MIA at ATL | 122-118 | 117-129 | 61% | NO | -16 | +6 |
| 2026-10-28 | WAS at CLE | 126-112 | 121-111 | 84% | yes | -4 | -6 |
| 2026-10-28 | CHA at DET | 113-108 | 97-89 | 66% | yes | +3 | -36 |
| 2026-10-28 | PHI at IND | 115-118 | 109-114 | 43% | yes | -2 | -10 |
| 2026-10-28 | ORL at TOR | 115-110 | 129-99 | 61% | yes | +25 | +4 |
| 2026-10-28 | NYK at CHI | 112-120 | 127-133 | 28% | yes | +2 | +29 |
| 2026-10-28 | HOU at MIL | 108-116 | 100-132 | 27% | yes | -23 | +8 |
| 2026-10-28 | GSW at MIN | 118-112 | 114-119 | 68% | NO | -12 | +3 |
| 2026-10-28 | DEN at NOP | 118-123 | 91-104 | 38% | yes | -8 | -46 |
| 2026-10-28 | SAS at UTA | 116-126 | 111-117 | 23% | yes | +5 | -14 |
| 2026-10-28 | OKC at DAL | 109-121 | 120-96 | 19% | NO | +36 | -14 |
| 2026-10-28 | LAL at LAC | 115-113 | 87-103 | 53% | NO | -17 | -38 |
| 2026-10-29 | CLE at ATL | 118-118 | 114-111 | 52% | yes | +2 | -11 |
| 2026-10-29 | SAC at NOP | 120-115 | 132-120 | 64% | yes | +7 | +17 |
| 2026-10-29 | MEM at POR | 121-113 | 103-124 | 70% | NO | -29 | -7 |
| 2026-10-30 | CHA at WAS | 109-117 | 95-79 | 29% | NO | +24 | -52 |
| 2026-10-30 | CHI at BOS | 122-108 | 125-111 | 83% | yes | +0 | +6 |
| 2026-10-30 | DET at BKN | 102-115 | 94-110 | 17% | yes | -3 | -14 |
| 2026-10-30 | NYK at PHI | 110-113 | 98-93 | 42% | NO | +8 | -32 |
| 2026-10-30 | ORL at TOR | 115-109 | 114-121 | 65% | NO | -13 | +12 |
| 2026-10-30 | IND at MIA | 123-116 | 145-125 | 66% | yes | +13 | +32 |
| 2026-10-30 | HOU at DAL | 111-118 | 116-111 | 30% | NO | +12 | -2 |
| 2026-10-30 | LAC at MIN | 114-109 | 127-101 | 61% | yes | +22 | +5 |
| 2026-10-30 | LAL at GSW | 113-115 | 112-95 | 45% | NO | +19 | -22 |
| 2026-10-30 | DEN at PHX | 112-115 | 120-127 | 44% | yes | -4 | +20 |
| 2026-10-31 | POR at UTA | 116-122 | 90-112 | 34% | yes | -16 | -35 |
| 2026-10-31 | PHI at CHA | 111-107 | 104-109 | 61% | NO | -9 | -5 |
| 2026-10-31 | ATL at NOP | 116-121 | 121-99 | 39% | NO | +26 | -17 |
| 2026-10-31 | SAC at MEM | 121-115 | 136-105 | 65% | yes | +25 | +5 |
| 2026-10-31 | CLE at MIL | 111-119 | 111-136 | 28% | yes | -17 | +17 |
| 2026-10-31 | MIN at SAS | 116-113 | 121-111 | 57% | yes | +7 | +4 |
| 2026-10-31 | OKC at HOU | 109-111 | 119-98 | 47% | NO | +22 | -3 |
| 2026-11-01 | BOS at ORL | 107-112 | 97-108 | 35% | yes | -6 | -15 |
| 2026-11-01 | BKN at IND | 115-110 | 90-98 | 64% | NO | -13 | -37 |
| 2026-11-01 | LAC at GSW | 112-110 | 124-112 | 53% | yes | +10 | +14 |
| 2026-11-01 | TOR at LAL | 113-111 | 131-125 | 54% | yes | +4 | +32 |
| 2026-11-02 | OKC at CLE | 114-114 | 112-117 | 49% | yes | -5 | +1 |
| 2026-11-02 | DET at CHA | 106-109 | 91-124 | 41% | yes | -29 | -0 |
| 2026-11-02 | ATL at IND | 115-120 | 104-108 | 36% | yes | +1 | -22 |
| 2026-11-02 | BKN at NYK | 114-100 | 103-90 | 83% | yes | -0 | -21 |
| 2026-11-02 | WAS at ORL | 119-110 | 94-103 | 73% | NO | -18 | -32 |
| 2026-11-02 | CHI at PHI | 121-113 | 126-107 | 70% | yes | +11 | -1 |
| 2026-11-02 | SAC at DAL | 120-114 | 100-115 | 68% | NO | -22 | -19 |
| 2026-11-02 | NOP at MEM | 120-118 | 134-135 | 52% | NO | -2 | +31 |
| 2026-11-02 | MIL at MIN | 120-107 | 112-100 | 81% | yes | -0 | -15 |
| 2026-11-02 | BOS at HOU | 108-108 | 109-93 | 50% | yes | +16 | -14 |
| 2026-11-02 | UTA at SAS | 125-111 | 119-97 | 85% | yes | +7 | -20 |
| 2026-11-02 | POR at DEN | 118-113 | 110-118 | 60% | NO | -12 | -3 |
| 2026-11-02 | PHX at GSW | 113-110 | 116-113 | 59% | yes | -0 | +6 |
| 2026-11-02 | TOR at LAC | 110-111 | 118-125 | 49% | yes | -7 | +22 |
| 2026-11-02 | MIA at LAL | 120-116 | 138-117 | 62% | yes | +16 | +19 |

## 3. Team by team

| team | games | wins | expected wins | points vs proj | allowed vs proj |
|---|---|---|---|---|---|
| CHA | 8 | 3 | 4.8 | -16.0 | -0.7 |
| SAS | 7 | 5 | 4.8 | -2.3 | -4.0 |
| BOS | 7 | 5 | 4.8 | +1.0 | +2.4 |
| LAL | 8 | 6 | 4.7 | +6.0 | +2.1 |
| HOU | 8 | 7 | 4.6 | +5.2 | -4.7 |
| OKC | 7 | 5 | 4.5 | -7.7 | -2.6 |
| MIN | 8 | 5 | 4.5 | +3.2 | -5.7 |
| CLE | 7 | 4 | 4.5 | +1.3 | +3.3 |
| NYK | 7 | 3 | 4.4 | -6.8 | -3.1 |
| DET | 7 | 6 | 4.3 | -1.5 | -8.4 |
| ATL | 8 | 4 | 4.3 | -2.0 | -1.9 |
| TOR | 7 | 4 | 4.2 | +4.2 | +0.2 |
| PHI | 8 | 7 | 3.9 | -2.3 | -8.9 |
| IND | 8 | 2 | 3.7 | -4.0 | -1.5 |
| GSW | 8 | 5 | 3.6 | +4.7 | +0.3 |
| DEN | 6 | 3 | 3.5 | -5.2 | +0.7 |
| MEM | 7 | 6 | 3.5 | +3.7 | -9.3 |
| MIA | 7 | 2 | 3.5 | +0.4 | +5.8 |
| LAC | 7 | 1 | 3.4 | -3.4 | +3.0 |
| POR | 6 | 5 | 3.4 | +4.0 | -4.6 |
| NOP | 7 | 3 | 3.3 | +3.3 | +0.5 |
| ORL | 7 | 2 | 3.1 | -6.0 | +0.8 |
| MIL | 7 | 1 | 2.6 | -1.0 | +7.3 |
| DAL | 7 | 4 | 2.5 | -1.5 | -7.0 |
| CHI | 7 | 1 | 2.3 | -0.8 | +9.0 |
| UTA | 7 | 1 | 2.3 | -10.5 | -5.2 |
| SAC | 7 | 1 | 2.2 | -2.7 | +4.5 |
| PHX | 5 | 1 | 2.1 | +2.5 | +10.1 |
| WAS | 7 | 4 | 1.9 | -2.3 | -13.0 |
| BKN | 7 | 1 | 1.7 | +1.0 | -0.8 |

Small samples (a handful of games per team): differences of a few points are noise.

## 4. Player stats

### Lineup unknown (what the daily job stores): every rostered rotation player, 0 if they did not play

| stat | n | forecast avg | actual avg | bias | MAE | MAE last-10 avg | 50% range | 80% range |
|---|---|---|---|---|---|---|---|---|
| min | 2988 | 15.81 | 14.78 | -1.028 | 9.16 | 11.43 | 66.4% | 86.4% |
| pts | 2988 | 7.70 | 7.05 | -0.643 | 5.28 | 6.84 | 69.6% | 90.3% |
| reb | 2988 | 2.88 | 2.70 | -0.176 | 2.09 | 2.69 | 73.8% | 91.8% |
| ast | 2988 | 1.77 | 1.66 | -0.110 | 1.39 | 1.78 | 79.0% | 93.3% |
| stl | 2988 | 0.55 | 0.53 | -0.029 | 0.62 | 0.77 | 85.7% | 94.4% |
| blk | 2988 | 0.32 | 0.30 | -0.019 | 0.41 | 0.49 | 88.3% | 95.2% |
| tov | 2988 | 0.92 | 0.95 | +0.022 | 0.89 | 1.10 | 80.7% | 93.0% |
| tpm | 2988 | 0.89 | 0.82 | -0.065 | 0.84 | 1.05 | 83.9% | 94.2% |
| pra | 2988 | 12.34 | 11.41 | -0.929 | 7.83 | 10.16 | 68.4% | 88.1% |

### Told who actually played (minutes shared among them): players who played

| stat | n | forecast avg | actual avg | bias | MAE | MAE last-10 avg | 50% range | 80% range |
|---|---|---|---|---|---|---|---|---|
| min | 2339 | 21.88 | 21.73 | -0.148 | 5.22 | 5.87 | 44.9% | 75.7% |
| pts | 2339 | 10.43 | 10.25 | -0.185 | 4.68 | 5.13 | 52.1% | 81.5% |
| reb | 2339 | 4.05 | 3.97 | -0.084 | 1.87 | 2.00 | 64.0% | 87.2% |
| ast | 2339 | 2.42 | 2.37 | -0.047 | 1.34 | 1.42 | 70.9% | 90.7% |
| stl | 2339 | 0.78 | 0.78 | -0.007 | 0.72 | 0.74 | 84.8% | 93.6% |
| blk | 2339 | 0.45 | 0.45 | -0.004 | 0.51 | 0.52 | 86.1% | 95.0% |
| tov | 2339 | 1.33 | 1.38 | +0.052 | 0.95 | 1.01 | 75.8% | 92.1% |
| tpm | 2339 | 1.19 | 1.19 | +0.000 | 0.92 | 0.95 | 77.4% | 93.0% |
| pra | 2339 | 16.90 | 16.59 | -0.315 | 6.18 | 6.83 | 49.3% | 77.0% |

### Players furthest from their points projection (5+ games, told who played)

Under-delivering:

| name | games | forecast | actual | diff |
|---|---|---|---|---|
| Nique Clifford | 5 | 8.1 | 0.4 | -7.7 |
| Daeqwon Plowden | 5 | 8.0 | 2.2 | -5.8 |
| Jerami Grant | 6 | 13.5 | 8.5 | -5.0 |
| DeMar DeRozan | 5 | 15.0 | 10.2 | -4.8 |
| Aaron Gordon | 5 | 14.6 | 9.8 | -4.8 |
| Dennis Schroder | 7 | 14.2 | 9.7 | -4.5 |
| Scoot Henderson | 5 | 11.9 | 7.4 | -4.5 |
| Gui Santos | 5 | 10.6 | 6.2 | -4.4 |

Over-delivering:

| name | games | forecast | actual | diff |
|---|---|---|---|---|
| Luka Doncic | 6 | 27.3 | 40.0 | +12.7 |
| Stephen Curry | 5 | 19.4 | 31.4 | +12.0 |
| Jamal Murray | 5 | 22.2 | 31.6 | +9.4 |
| Tyrese Maxey | 7 | 21.3 | 29.3 | +8.0 |
| Isaiah Stewart | 5 | 6.6 | 14.6 | +8.0 |
| Darryn Peterson | 6 | 6.7 | 14.2 | +7.5 |
| Ty Jerome | 5 | 18.3 | 24.8 | +6.5 |
| Davion Mitchell | 6 | 10.4 | 16.8 | +6.4 |
