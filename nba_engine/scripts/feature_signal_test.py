"""Which of the proposed extra inputs carry signal for player stats beyond the current forecast?  Walk-forward 2025-26 forecasts (confirmed lineup),
every feature computed only from games before the one being forecast. Univariate regression of the forecast error (actual - forecast) on each feature,
robust t-statistics, split-half sign check. With ~70 tests, |t| above about 3 is the bar, plus the same sign in both halves."""
import sys
import numpy as np, pandas as pd
GEO = {"ATL": (33.76, -84.40, 0), "BOS": (42.37, -71.06, 0), "BKN": (40.68, -73.97, 0), "CHA": (35.23, -80.84, 0), "CHI": (41.88, -87.67, -1), "CLE": (41.50, -81.69, 0),
       "DAL": (32.79, -96.81, -1), "DEN": (39.75, -105.00, -2), "DET": (42.34, -83.06, 0), "GSW": (37.77, -122.39, -3), "HOU": (29.75, -95.36, -1), "IND": (39.76, -86.16, 0),
       "LAC": (34.04, -118.27, -3), "LAL": (34.04, -118.27, -3), "MEM": (35.14, -90.05, -1), "MIA": (25.78, -80.19, 0), "MIL": (43.04, -87.92, -1), "MIN": (44.98, -93.28, -1),
       "NOP": (29.95, -90.08, -1), "NYK": (40.75, -73.99, 0), "OKC": (35.46, -97.52, -1), "ORL": (28.54, -81.38, 0), "PHI": (39.90, -75.17, 0), "PHX": (33.45, -112.07, -2),
       "POR": (45.53, -122.67, -3), "SAC": (38.58, -121.50, -3), "SAS": (29.43, -98.44, -1), "TOR": (43.64, -79.38, 0), "UTA": (40.77, -111.90, -2), "WAS": (38.90, -77.02, 0)}


def km(a, b):
    la1, lo1, la2, lo2 = map(np.radians, (*GEO[a][:2], *GEO[b][:2]))
    h = np.sin((la2 - la1) / 2) ** 2 + np.cos(la1) * np.cos(la2) * np.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * np.arcsin(np.sqrt(h))


def main():
    L = pd.concat([pd.read_csv(f"data/processed/player_games_{y}.csv") for y in (2025, 2026)])
    L["date"] = pd.to_datetime(L.date); L = L.sort_values(["date", "game_id"])
    # team schedule features
    tg = L.groupby(["season", "game_id", "team"]).agg(date=("date", "first"), home=("is_home", "first"), opp=("opp", "first")).reset_index().sort_values(["date", "game_id"])
    tg["site"] = np.where(tg.home == 1, tg.team, tg.opp)
    tg["prev_date"] = tg.groupby(["season", "team"]).date.shift(); tg["prev_site"] = tg.groupby(["season", "team"]).site.shift()
    tg["team_rest"] = (tg.date - tg.prev_date).dt.days.clip(upper=6)
    ok = tg.prev_site.notna() & tg.site.map(lambda s: s in GEO) & tg.prev_site.map(lambda s: s in GEO if isinstance(s, str) else False)
    tg["travel_km"] = np.nan; tg.loc[ok, "travel_km"] = [km(a, b) for a, b in zip(tg.prev_site[ok], tg.site[ok])]
    tg["tz_shift"] = np.nan; tg.loc[ok, "tz_shift"] = [GEO[b][2] - GEO[a][2] for a, b in zip(tg.prev_site[ok], tg.site[ok])]   # negative = travelled west
    tg["team_b2b"] = (tg.team_rest == 1).astype(float)
    opp_rest = tg[["game_id", "team", "team_rest", "team_b2b"]].rename(columns={"team": "opp", "team_rest": "opp_rest", "team_b2b": "opp_b2b"})
    tg = tg.merge(opp_rest, on=["game_id", "opp"], how="left")
    # player history features (strictly before the game)
    L = L.merge(tg[["game_id", "team", "team_rest", "team_b2b", "travel_km", "tz_shift", "opp_rest", "opp_b2b"]], on=["game_id", "team"], how="left")
    L = L[L["min"] > 0].sort_values(["player_id", "date", "game_id"])
    g = L.groupby("player_id")
    L["player_rest"] = (L.date - g.date.shift()).dt.days.clip(upper=14)
    L["min_l3"] = g["min"].transform(lambda x: x.shift().rolling(3, min_periods=3).sum())
    L["games_l7d"] = g["date"].transform(lambda d: pd.Series(1, index=d.index).groupby(d.dt.floor("D")).transform("size") * 0)  # placeholder, replaced below
    L["games_l7d"] = [np.nan] * len(L)
    # games in previous 7 days
    out = []
    for pid, x in g:
        d = x.date.to_numpy(); n = np.zeros(len(d))
        j = 0
        for i in range(len(d)):
            while d[i] - d[j] > np.timedelta64(7, "D"):
                j += 1
            n[i] = i - j
        out.append(pd.Series(n, index=x.index))
    L["games_l7d"] = pd.concat(out)
    d = pd.read_pickle("/home/claude/nba_engine/artifacts/player_eval_frame.pkl")
    d = d[(d["mode"] == "confirmed") & (d.played == 1) & (d.is_new == 0)]
    tp = pd.read_csv("data/processed/trend_proj_2026.csv")[["game_id", "m_mean", "m_sd"]]
    d = d.merge(L[["game_id", "player_id", "is_home", "team_rest", "team_b2b", "travel_km", "tz_shift", "opp_rest", "opp_b2b", "player_rest", "min_l3", "games_l7d", "date"]], on=["game_id", "player_id"], how="left").merge(tp, on="game_id", how="left")
    d = d.sort_values(["player_id", "game_id"])
    from math import erf
    d["blowout_p"] = [1 - (erf((15 - abs(m)) / (s * 2 ** .5)) / 2 + erf((15 + abs(m)) / (s * 2 ** .5)) / 2) if s == s else np.nan for m, s in zip(d.m_mean, d.m_sd)]
    d["workload_l3"] = d.min_l3 - 3 * d.mean_min
    d["returning"] = (d.player_rest >= 6).astype(float)
    d["long_trip"] = (d.travel_km > 1500).astype(float)
    d["west_to_east"] = (d.tz_shift > 0).astype(float)    # travelled east
    d["east_to_west"] = (d.tz_shift < 0).astype(float)
    feats = ["is_home", "team_b2b", "opp_b2b", "team_rest", "opp_rest", "player_rest", "returning", "games_l7d", "workload_l3", "travel_km", "long_trip", "tz_shift", "west_to_east", "east_to_west", "blowout_p"]
    half = d.game_id.median(); rows = []
    for s in ("min", "pts", "reb", "ast", "tpm", "pra"):
        y = d[f"a_{s}"] - d[f"mean_{s}"]
        # bounce-back: previous played game's error of the same stat
        prev = (y.groupby(d.player_id).shift()); d[f"bounce_{s}"] = prev
        # player variance: spread of the player's last 15 actuals relative to the forecast
        d[f"sd15_{s}"] = d.groupby("player_id")[f"a_{s}"].transform(lambda x: x.shift().rolling(15, min_periods=8).std())
        for f in feats + [f"bounce_{s}"]:
            x = d[f"bounce_{s}"] if f.startswith("bounce") else d[f]
            m = x.notna() & y.notna()
            if m.sum() < 500 or x[m].std() == 0:
                continue
            def fit(mm):
                xx, yy = x[mm].to_numpy(float), y[mm].to_numpy(float); xc = xx - xx.mean()
                b = (xc * (yy - yy.mean())).sum() / (xc ** 2).sum(); e = yy - yy.mean() - b * xc
                se = np.sqrt(((xc ** 2) * e ** 2).sum()) / (xc ** 2).sum()
                return b, b / se
            b, t = fit(m); b1, t1 = fit(m & (d.game_id <= half)); b2, t2 = fit(m & (d.game_id > half))
            rows.append({"stat": s, "feature": f, "n": int(m.sum()), "effect per unit": b, "x sd": x[m].std(), "effect per 1 sd": b * x[m].std(), "t": t, "t 1st half": t1, "t 2nd half": t2})
        # variance: does the player's recent spread predict the size of the error?
        a = y.abs(); m = d[f"sd15_{s}"].notna()
        c = np.corrcoef(d.loc[m, f"sd15_{s}"], a[m])[0, 1]
        c0 = np.corrcoef(d.loc[m, f"mean_{s}"], a[m])[0, 1]
        rows.append({"stat": s, "feature": "recent spread vs |error| (corr; forecast level corr in 'effect per unit')", "n": int(m.sum()), "effect per unit": c0, "x sd": np.nan, "effect per 1 sd": c, "t": np.nan, "t 1st half": np.nan, "t 2nd half": np.nan})
    R = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    sig = R[(R.t.abs() > 3) & (np.sign(R["t 1st half"]) == np.sign(R["t 2nd half"]))]
    print("tests:", len(R), "| pass (|t|>3, same sign both halves):", len(sig))
    print(sig.round(3).to_string(index=False))
    print("\nnear misses (2.3 < |t| <= 3):"); print(R[(R.t.abs() > 2.3) & (R.t.abs() <= 3)].round(3).to_string(index=False))
    print("\nvariance rows:"); print(R[R.feature.str.startswith("recent")].round(3).to_string(index=False))
    R.to_csv("artifacts/feature_signal_test.csv", index=False)


if __name__ == "__main__":
    main()
