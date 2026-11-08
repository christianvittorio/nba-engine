"""Tests of the ESPN-data layers against the engine's walk-forward predictions. Prints results; writes artifacts/reports/layer_tests.md.
 1 odds     market closing line vs our model (MAE, win log-loss), optimal blend, line-movement information, agreement buckets
 2 quarters first-half and first-quarter share of points
 3 officials crew tendencies (leave-one-out) vs fouls / free throws / total points
 4 lineups  on/off and lineup tables sanity (needs starter flags)
 5 clutch   team clutch net vs close-game results"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); os.chdir(ROOT)
import numpy as np, pandas as pd
from nbaengine.gamedata import load_all
from nbaengine import layers as L
FIX = {"GS": "GSW", "NY": "NYK", "NO": "NOP", "SA": "SAS", "UTAH": "UTA", "WSH": "WAS"}
OUT = []


def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def ll(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4); return float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean())


def model_table():
    """our walk-forward / live predictions keyed by (date, home, away): margin, total, home win prob"""
    P = pd.concat([pd.read_csv(f"data/processed/trend_proj_{s}.csv") for s in (2023, 2024, 2025, 2026)])
    P = P.rename(columns={"m_mean": "pred_margin", "t_mean": "pred_total", "sim_p_home": "pred_p"})[["date", "home", "away", "home_pts", "away_pts", "pred_margin", "pred_total", "pred_p", "elo_p_home"]]
    try:
        import sqlite3
        c = sqlite3.connect("artifacts/live.sqlite")
        q = """SELECT d.date, g.home, g.away, r.home_pts, r.away_pts, f.mean_margin pred_margin, f.mean_total pred_total, f.p_home pred_p FROM forecasts f
               JOIN results r USING(season, game_id) JOIN games g USING(season, game_id) JOIN game_dates d USING(season, game_id) WHERE f.model_name='sim_mc'"""
        P = pd.concat([P, pd.read_sql_query(q, c)])
    except Exception as ex:
        say("live forecasts unavailable:", ex)
    return P.drop_duplicates(["date", "home", "away"])


def main():
    G = list(load_all("artifacts/gamedata")); say(f"# Layer tests: {len(G)} stored games, {min(g['date'] for g in G)} to {max(g['date'] for g in G)}", "")
    team = {}
    for g in G:
        for tid, t in g["teams"].items():
            team[(g["game_id"], t["home_away"])] = FIX.get(t["abbr"], t["abbr"])
    # ------------------------------------------------------------------ 1 odds
    O = L.odds(G)
    O["home"] = [team.get((i, "home")) for i in O.game_id]; O["away"] = [team.get((i, "away")) for i in O.game_id]
    M = model_table().merge(O, on=["date", "home", "away"])
    M = M.dropna(subset=["spread_close", "pred_margin"])
    say(f"## 1. Market closing line vs our model ({len(M)} games with both)", "")
    if len(M) > 50:
        M["act_margin"] = M.home_pts - M.away_pts; M["mkt_margin"] = -M.spread_close; M["mkt_open_margin"] = -M.spread_open
        M["mkt_p"] = L.implied_home_prob(M).to_numpy(); M["act_tot"] = M.home_pts + M.away_pts
        y = (M.act_margin > 0).astype(float)
        mae = lambda a, b: float((a - b).abs().mean())
        say(f"- Margin error (MAE): market close {mae(M.act_margin, M.mkt_margin):.3f}, market open {mae(M.act_margin, M.mkt_open_margin):.3f}, our model {mae(M.act_margin, M.pred_margin):.3f}")
        say(f"- Total error (MAE): market close {mae(M.act_tot, M.total_close):.3f}, our model {mae(M.act_tot, M.pred_total):.3f}")
        okp = M.mkt_p.notna(); y = y[okp]; M = M[okp].copy()
        say(f"- Win log-loss: market {ll(M.mkt_p.to_numpy(), y.to_numpy()):.4f}, our model {ll(M.pred_p.to_numpy(), y.to_numpy()):.4f}")
        # blend weight for margin: act = w*model + (1-w)*market
        d = M.pred_margin - M.mkt_margin; e = M.act_margin - M.mkt_margin
        w = float((d * e).sum() / (d * d).sum()); se = float(np.sqrt(((e - w * d) ** 2).sum() / (len(d) - 1) / (d * d).sum()))
        say(f"- Margin blend: actual - market = {w:.3f} x (model - market), standard error {se:.3f}  (0 = the market already contains everything our model knows)")
        b = (w * M.pred_margin + (1 - w) * M.mkt_margin)
        say(f"- Blended margin MAE {mae(M.act_margin, b):.3f}")
        dt = M.pred_total - M.total_close; et = M.act_tot - M.total_close
        wt = float((dt * et).sum() / (dt * dt).sum()); set_ = float(np.sqrt(((et - wt * dt) ** 2).sum() / (len(dt) - 1) / (dt * dt).sum()))
        say(f"- Total blend: actual - market total = {wt:.3f} x (model - market), standard error {set_:.3f}")
        # line movement: does the move from open to close predict what the open got wrong?
        mv = M.mkt_margin - M.mkt_open_margin; eo = M.act_margin - M.mkt_open_margin
        k = float((mv * eo).sum() / (mv * mv).sum()); sk = float(np.sqrt(((eo - k * mv) ** 2).sum() / (len(mv) - 1) / (mv * mv).sum()))
        say(f"- Line movement: actual - open = {k:.2f} x (close - open), standard error {sk:.2f}  (1 = the move fully reflects new information; 0 = noise)")
        # agreement buckets: when our margin differs from the market's, who is closer?
        M["gap"] = M.pred_margin - M.mkt_margin; M["bucket"] = pd.cut(M.gap.abs(), [0, 1.5, 3, 5, 100])
        rows = []
        for bk, g in M.groupby("bucket", observed=True):
            rows.append(f"| {bk} | {len(g)} | {mae(g.act_margin, g.mkt_margin):.2f} | {mae(g.act_margin, g.pred_margin):.2f} | {float((np.sign(g.gap) == np.sign(g.act_margin - g.mkt_margin)).mean()):.1%} |")
        say("", "| |our margin differs from market by| games | market MAE | our MAE | our side beat the closing line |", "|---|---|---|---|---|"); [say(r) for r in rows]
    # ------------------------------------------------------------------ 2 quarters
    Q = L.quarters(G)
    say("", f"## 2. Quarters ({len(Q)} games)", "")
    if len(Q):
        say(f"- First-quarter share of regulation points {Q.q1_share.mean():.4f} (sd {Q.q1_share.std():.4f}); first-half share {Q.h1_share.mean():.4f} (sd {Q.h1_share.std():.4f}). A 0.75x first-quarter pace would be a 0.19 share; the data shows 0.25.")
        say(f"- Average points by quarter (both teams): " + ", ".join(f"Q{i} {(Q[f'h_q{i}'] + Q[f'a_q{i}']).mean():.1f}" for i in range(1, 5)))
    # ------------------------------------------------------------------ 3 officials
    Of = L.officials(G)
    say("", f"## 3. Officials ({len(Of)} games)", "")
    if len(Of) > 200:
        Of = Of.sort_values("date"); rows = []
        cnt = {}
        for crew_member in set(m for c in Of.crew for m in c):
            cnt[crew_member] = Of[Of.crew.map(lambda c: crew_member in c)]
        def loo(col):
            out = []
            for i, r in Of.iterrows():
                vals = [cnt[m][cnt[m].game_id != r.game_id][col].mean() for m in r.crew if len(cnt[m]) > 8]
                out.append(np.mean(vals) if vals else np.nan)
            return np.array(out)
        for col in ("fouls", "free_throws"):
            x = loo(col); y = Of[col].to_numpy(float); m = ~np.isnan(x)
            xc = x[m] - x[m].mean(); b = (xc * (y[m] - y[m].mean())).sum() / (xc ** 2).sum(); se = np.sqrt((((y[m] - y[m].mean()) - b * xc) ** 2).sum() / (m.sum() - 2) / (xc ** 2).sum())
            say(f"- {col}: a game's crew average of OTHER games predicts this game's {col} with slope {b:.2f} (se {se:.2f}); crew averages range {np.nanmin(x):.1f} to {np.nanmax(x):.1f} (league {Of[col].mean():.1f})")
        # does the crew predict points and free throws beyond our forecast?
        crew_ft = {}
        for i, r in Of.iterrows():
            vals = [cnt[m][cnt[m].game_id != r.game_id].free_throws.mean() for m in r.crew if len(cnt[m]) > 8]
            crew_ft[r.game_id] = np.mean(vals) if vals else np.nan
        Of["crew_ft"] = Of.game_id.map(crew_ft)
        Mo = M.merge(Of[["game_id", "crew_ft"]].assign(date=Of.date).merge(O[["game_id", "home", "away"]], on="game_id")[["date", "home", "away", "crew_ft"]], on=["date", "home", "away"]).dropna(subset=["crew_ft"])
        x = Mo.crew_ft - Mo.crew_ft.mean(); e = (Mo.act_tot - Mo.pred_total)
        b = float((x * (e - e.mean())).sum() / (x * x).sum()); se = float(np.sqrt((((e - e.mean()) - b * x) ** 2).sum() / (len(x) - 2) / (x * x).sum()))
        say(f"- Total points error of our model vs the crew's free-throw tendency: {b:+.2f} points per extra free throw of crew average, se {se:.2f} ({len(Mo)} games). Crew free-throw average sd {x.std():.2f}")
        e2 = (Mo.act_tot - Mo.total_close)
        b2 = float((x * (e2 - e2.mean())).sum() / (x * x).sum()); se2 = float(np.sqrt((((e2 - e2.mean()) - b2 * x) ** 2).sum() / (len(x) - 2) / (x * x).sum()))
        say(f"- Same against the market total: {b2:+.2f} (se {se2:.2f}) -> {'the market already prices the crew' if abs(b2/se2) < 2 else 'the market does NOT fully price the crew'}")
    # ------------------------------------------------------------------ 4 lineups
    S = L.stints(G)
    say("", f"## 4. Lineups ({S.game_id.nunique() if len(S) else 0} games with starters)", "")
    if len(S):
        T = L.lineup_table(S, 10)
        say(f"- Lineup stints {len(S)}; minutes captured per team-game {S.groupby(['game_id','team']).sec.sum().mean()/60:.1f} of 48 (should be 48)")
        say("- Best five-man lineups so far (min 10 minutes): ", ", ".join(f"{r.team} {r.min:.0f}m {r.net_per48:+.1f}" for r in T.head(5).itertuples()))
    # ------------------------------------------------------------------ 5 shot quality
    Sh = L.shots(G)
    say("", f"## 5. Shot quality by zone ({len(Sh)} shots)", "")
    if len(Sh) > 20000:
        lg = Sh.groupby("zone").made.mean(); Sh["exp"] = Sh.zone.map(lg) * np.where(Sh.is3, 3, 2); Sh["pts"] = Sh.made * np.where(Sh.is3, 3, 2)
        tg = Sh.groupby(["game_id", "team", "date"]).agg(act=("pts", "mean"), exp=("exp", "mean"), n=("pts", "size")).reset_index().sort_values("date")
        tg["act_ew"] = tg.groupby("team").act.transform(lambda x: x.shift().ewm(halflife=15, min_periods=5).mean())
        tg["exp_ew"] = tg.groupby("team").exp.transform(lambda x: x.shift().ewm(halflife=15, min_periods=5).mean())
        d = tg.dropna(subset=["act_ew", "exp_ew"])
        X = np.column_stack([np.ones(len(d)), d.act_ew, d.exp_ew]); beta, *_ = np.linalg.lstsq(X, d.act.to_numpy(), rcond=None)
        r0 = d.act - d.act_ew.mean(); res = d.act.to_numpy() - X @ beta
        cov = np.linalg.inv(X.T @ X) * res.var()
        say(f"- Next-game points per shot ~ {beta[1]:.2f} x team's recent actual + {beta[2]:.2f} x team's recent shot-quality (zone mix at league zone accuracy); se {np.sqrt(cov[1,1]):.2f} and {np.sqrt(cov[2,2]):.2f}. Shot quality carries real information when its coefficient is clearly above zero.")
        say(f"- Correlation of next-game points/shot with: recent actual {np.corrcoef(d.act, d.act_ew)[0,1]:.3f}, recent shot-quality {np.corrcoef(d.act, d.exp_ew)[0,1]:.3f}")
    open("artifacts/reports/layer_tests.md", "w").write("\n".join(OUT))


if __name__ == "__main__":
    main()
