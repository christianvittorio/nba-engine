import pandas as pd, numpy as np, sys
sys.path.insert(0,"/home/claude/nba-engine/nba_engine")
from nbaengine.elo import Elo, EloParams
R="/home/claude/nba-engine/nba_engine/data/processed/"
S=(2022,2023,2024,2025,2026)
G=pd.concat([pd.read_csv(R+f"games_cdn_{y}.csv",usecols=["game_id","home","away","home_pts","away_pts","date"]).assign(season=y) for y in S]).sort_values(["season","date","game_id"]).reset_index(drop=True)
G["am"]=G.home_pts-G.away_pts; G["win"]=(G.am>0)*1.0
P=pd.concat([pd.read_csv(R+f"player_games_{y}.csv",usecols=["game_id","season","team","player_id","name","min","pts","reb","oreb","ast","stl","blk","tov","fgm","fga","ftm","fta"]) for y in S]); P=P[P["min"]>0]
# ---- player impact per season: ridge regression of home margin on (home minute share - away minute share)
def impacts(season, alpha=30.0):
    g=G[G.season==season]; p=P[P.season==season].merge(g[["game_id","home","away"]],on="game_id")
    p["side"]=np.where(p.team==p.home,1.0,-1.0); p["x"]=p["min"]/240.0*p.side
    ids=sorted(p.player_id.unique()); ix={i:k for k,i in enumerate(ids)}; gi={x:k for k,x in enumerate(g.game_id)}
    from scipy import sparse
    X=sparse.coo_matrix((p.x.values,(p.game_id.map(gi).values,p.player_id.map(ix).values)),shape=(len(g),len(ids))).tocsr()
    y=g.am.values-g.am.mean()
    from sklearn.linear_model import Ridge
    m=Ridge(alpha=alpha*1e-0,fit_intercept=False).fit(X,y)
    return dict(zip(ids,m.coef_)), p.groupby("player_id")["min"].mean().to_dict()

def roster_strength(roster_minutes, coef):
    # roster_minutes: {player: weight minutes}; top 10 by weight, scaled to at most 240
    items=sorted(roster_minutes.items(),key=lambda kv:-kv[1])[:10]; tot=sum(w for _,w in items) or 1.0; sc=min(1.0,240.0/tot)
    return sum((w*sc/240.0)*coef.get(p,0.0) for p,w in items)
def impacts_gs(season):
    p=P[P.season==season].copy(); p["gs"]=p.pts+0.4*p.fgm-0.7*p.fga-0.4*(p.fta-p.ftm)+0.7*p.oreb+0.3*(p.reb-p.oreb)+p.stl+0.7*p.ast+0.7*p.blk-p.tov
    a=p.groupby("player_id").agg(gs=("gs","sum"),m=("min","sum")); lg=a.gs.sum()/a.m.sum()
    sh=a.m/(a.m+1500.0); return dict(zip(a.index,(a.gs/a.m-lg)*sh*5.0)), p.groupby("player_id")["min"].mean().to_dict()
import os
COEF={s:(impacts_gs(s) if os.environ.get("METRIC")=="gs" else impacts(s)) for s in S}
delta={}
for s in (2023,2024,2025,2026):
    cp,mp=COEF[s-1]
    first=G[G.season==s].copy(); ids=set()
    for t in sorted(set(first.home)|set(first.away)):
        tg=first[(first.home==t)|(first.away==t)].game_id.head(10)
        new=P[(P.season==s)&(P.team==t)&(P.game_id.isin(tg))].player_id.unique()
        rn={p:min(mp.get(p,10.0),36.0) for p in new}
        pt=P[(P.season==s-1)&(P.team==t)]; g_=pt.groupby("player_id")["min"].agg(["mean","size"]); g_=g_[g_["size"]>=10]
        ro={p:min(v,36.0) for p,v in g_["mean"].items()}
        delta[(s,t)]=(roster_strength(rn,cp)-roster_strength(ro,cp), roster_strength(rn,cp), roster_strength(ro,cp))
D=pd.DataFrame([(s,t,*v) for (s,t),v in delta.items()],columns=["season","team","delta","new","old"])
print("delta spread: sd %.2f max %.2f min %.2f"%(D.delta.std(),D.delta.max(),D.delta.min()))
print(D.sort_values("delta").head(4).to_string(),"\n",D.sort_values("delta").tail(4).to_string())
# ---- Elo walk-forward (modern HA 45), record diff and games played
e=Elo(EloParams(k=20,home_adv=45,carryover=0.7,init=1505,mov_scale=1.0)); gp={}; rows=[]
cur=None
for r in G.itertuples():
    e.new_season(r.season)
    if r.season!=cur: gp={}; cur=r.season
    pr=e.predict(r.home,r.away); rows.append((pr["elo_diff"],gp.get(r.home,0),gp.get(r.away,0)))
    e.update(r.home,r.away,r.home_pts,r.away_pts); gp[r.home]=gp.get(r.home,0)+1; gp[r.away]=gp.get(r.away,0)+1
G[["ed","gph","gpa"]]=rows
dm={k:v[0] for k,v in delta.items()}
G["dh"]=[dm.get((s,t),np.nan) for s,t in zip(G.season,G.home)]; G["da"]=[dm.get((s,t),np.nan) for s,t in zip(G.season,G.away)]
H=G[G.season>=2023].copy()
H["gpm"]=(H.gph+H.gpa)/2
def fit(X,y,l2=1e-3):
    b=np.zeros(X.shape[1])
    for _ in range(100):
        p=1/(1+np.exp(-X@b)); g=X.T@(p-y)+l2*b; W=p*(1-p); Hh=(X*W[:,None]).T@X+l2*np.eye(len(b)); b-=np.linalg.solve(Hh,g)
    return b
ll=lambda p,y:-np.mean(y*np.log(np.clip(p,1e-4,1-1e-4))+(1-y)*np.log(1-np.clip(p,1e-4,1-1e-4)))
def feats(d,tau,use):
    f=(d.dh-d.da)*np.exp(-d.gpm/tau) if use else 0*d.ed
    return np.c_[np.ones(len(d)),d.ed/100.0,f]
for tau in (10,20,40):
    out=[]
    for tr,te in (((2023,2024),(2025,2026)),((2025,2026),(2023,2024)),((2023,2026),(2024,2025))):
        a=H[H.season.isin(tr)]; b=H[H.season.isin(te)]
        for early in (True,False):
            aa=a[a.gpm<25] if early else a; bb=b[b.gpm<25] if early else b
            w1=fit(feats(aa,tau,True),aa.win.values); w0=fit(feats(aa,tau,False)[:,:2],aa.win.values)
            p1=1/(1+np.exp(-feats(bb,tau,True)@w1)); p0=1/(1+np.exp(-feats(bb,tau,False)[:,:2]@w0))
            out.append((tr,te,"early" if early else "all",len(bb),ll(p0,bb.win.values),ll(p1,bb.win.values),w1[2]))
    print("tau",tau)
    for o in out: print("  train",o[0],"test",o[1],o[2],"n",o[3],"elo-only %.4f with roster %.4f coef %.3f"%(o[4],o[5],o[6]))
