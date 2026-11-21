"""Progressive baselines and validation-only statistical challengers.

Baselines: home-adjusted Elo, regularized margin/total regression.
Candidate: optional LightGBM (never assumed superior to Ridge or Elo).
A candidate is only 'selected' after a fully chronological train/validation/
untouched test split. All outputs reconcile margin+total with team scores.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
import numpy as np
import pandas as pd
from typing import Any

ELO_VERSION = "elo-v2.0"
RIDGE_VERSION = "ridge-margin-total-v2.0"
CANDIDATE_VERSION = "lgbm-margin-total-v2.0"


@dataclass(frozen=True)
class TeamForecast:
    home_mean: float
    away_mean: float
    p_home: float
    model_version: str
    margin_sigma: float = 13.5
    total_sigma: float = 19.0
    def __post_init__(self):
        if not 0 < self.p_home < 1:
            raise ValueError("Invalid win probability")
        if self.home_mean < 0 or self.away_mean < 0:
            raise ValueError("Negative team score")
    @property
    def margin(self):
        return self.home_mean-self.away_mean
    @property
    def total(self):
        return self.home_mean+self.away_mean
    def as_dict(self):
        return {
            "home_score":round(self.home_mean,3),
            "away_score":round(self.away_mean,3),
            "margin":round(self.margin,3),
            "total":round(self.total,3),
            "home_win_probability":round(self.p_home,5),
            "margin_sd":round(self.margin_sigma,3),
            "total_sd":round(self.total_sigma,3),
            "model_version":self.model_version,
        }

class Elo:
    """Sports-reference-style margin-sensitive Elo, day-by-day updates."""
    def __init__(self, home_rating=55.0, k=18.0, regression=0.75):
        self.home_rating=home_rating
        self.k=k
        self.regression=regression
        self.rating:dict[str,float]={}
        self._season=None

    def start_season(self,season:int):
        if self._season is not None and self._season != season:
            self.rating={t:1500+(r-1500)*self.regression for t,r in self.rating.items()}
        self._season=season

    def predict(self,home:str,away:str,neutral=False) -> TeamForecast:
        diff=self.rating.get(home,1500.0)-self.rating.get(away,1500.0)
        diff+=0 if neutral else self.home_rating
        p=1/(1+10**(-diff/400))
        margin=diff/27.0
        # Elo alone is not a reliable total projection: neutral fixed prior.
        return TeamForecast(112.0+margin/2,112.0-margin/2,p,ELO_VERSION)

    def update(self,home:str,away:str,actual_home:int,actual_away:int,neutral=False):
        if actual_home==actual_away:
            raise ValueError("Final NBA game cannot be tied")
        outcome=1.0 if actual_home>actual_away else 0.0
        old=self.predict(home,away,neutral)
        mov=abs(actual_home-actual_away)
        margin_factor=((mov+3)**0.8)/max(2.0,7.5+.006*(self.rating.get(home,1500)
                            -self.rating.get(away,1500)+self.home_rating))
        delta=self.k*margin_factor*(outcome-old.p_home)
        self.rating[home]=self.rating.get(home,1500)+delta
        self.rating[away]=self.rating.get(away,1500)-delta

    def pregame_series(self,games:pd.DataFrame) -> pd.DataFrame:
        needed={"season","game_date","game_id","home_team_id","away_team_id",
                "home_score","away_score"}
        if not needed <= set(games):
            raise ValueError(f"Missing Elo game columns {needed-set(games)}")
        data=games.sort_values(["season","game_date","game_id"])
        results=[]
        # Predict an entire day before ingesting any same-day results.
        for (season,day),group in data.groupby(["season","game_date"],sort=True):
            self.start_season(int(season))
            for row in group.itertuples(index=False):
                p=self.predict(str(row.home_team_id),str(row.away_team_id),
                               bool(getattr(row,"neutral_site",False)))
                results.append({"game_id":str(row.game_id),"game_date":str(day),
                                "season":int(season),**p.as_dict()})
            for row in group.itertuples(index=False):
                self.update(str(row.home_team_id),str(row.away_team_id),
                            int(row.home_score),int(row.away_score),
                            bool(getattr(row,"neutral_site",False)))
        return pd.DataFrame(results)


def _sigmoid_margin(margin: float, scale: float) -> float:
    return float(np.clip(1.0/(1.0+exp(-float(np.clip(margin/scale,-30,30)))),
                         1e-4,1-1e-4))


def chronological_split(frame:pd.DataFrame, train_before:str,
                        validation_before:str) -> tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame]:
    if not train_before < validation_before:
        raise ValueError("Train cutoff must be earlier than validation cutoff")
    if "game_date" not in frame:
        raise ValueError("game_date required")
    if frame.game_date.isna().any():
        raise ValueError("Cannot split games with unknown dates")
    df=frame.copy()
    df["game_date"]=df.game_date.astype(str).str[:10]
    train=df[df.game_date<train_before].copy()
    val=df[(df.game_date>=train_before)&(df.game_date<validation_before)].copy()
    test=df[df.game_date>=validation_before].copy()
    if min(len(train),len(val),len(test))<2:
        raise ValueError("Need at least two training, validation and test games")
    if set(train.game_date)&set(val.game_date) or set(val.game_date)&set(test.game_date):
        raise ValueError("Overlapping chronological partitions")
    return train,val,test


class RegressionPair:
    """Two *separate targets*, score margin and total; reconstructed scores agree."""
    def __init__(self,kind="ridge",alpha=20.0,seed=241):
        if kind not in ("ridge","lightgbm"):
            raise ValueError("Expected ridge or lightgbm")
        self.kind=kind
        self.alpha=alpha
        self.seed=seed
        self.feature_cols:list[str]=[]
        self.margin=None
        self.total=None
        self.win_scale=8.0
        self.margin_sigma=13.5
        self.total_sigma=19.0
        self.trained=False

    def _model(self):
        if self.kind=="ridge":
            from sklearn.pipeline import make_pipeline
            from sklearn.impute import SimpleImputer
            from sklearn.preprocessing import StandardScaler
            from sklearn.linear_model import Ridge
            return make_pipeline(SimpleImputer(strategy="median",add_indicator=True),
                                 StandardScaler(),Ridge(alpha=self.alpha))
        try:
            import lightgbm as lgb
        except ImportError as exc:
            raise RuntimeError("Optional LightGBM candidate requires pip install lightgbm") from exc
        return lgb.LGBMRegressor(n_estimators=220,max_depth=4,num_leaves=15,
                                 learning_rate=.035,reg_lambda=8.0,
                                 min_child_samples=25,verbosity=-1,
                                 random_state=self.seed,n_jobs=2)

    def fit(self, frame:pd.DataFrame,features:list[str]):
        if not features:
            raise ValueError("No features")
        self.feature_cols=list(features)
        X=frame[self.feature_cols].apply(pd.to_numeric,errors="coerce")
        if not np.isfinite(X.to_numpy(dtype=float)).any():
            raise ValueError("No finite numeric training features")
        h=frame.home_score.astype(float)
        a=frame.away_score.astype(float)
        self.margin=self._model()
        self.total=self._model()
        self.margin.fit(X,h-a)
        self.total.fit(X,h+a)
        self.trained=True
        return self

    def predict_array(self, frame:pd.DataFrame) -> tuple[np.ndarray,np.ndarray]:
        if not self.trained:
            raise RuntimeError("Model has not been fitted")
        X=frame.reindex(columns=self.feature_cols).apply(pd.to_numeric,errors="coerce")
        return np.asarray(self.margin.predict(X)),np.asarray(self.total.predict(X))

    def predict(self, features:dict[str,Any]) -> TeamForecast:
        margin,total=self.predict_array(pd.DataFrame([features]))
        mu_m=float(margin[0])
        mu_t=max(120,float(total[0]))
        h=max(0,(mu_t+mu_m)/2)
        a=max(0,(mu_t-mu_m)/2)
        # Reconcile *after* clipping, margin and total on forecast properties.
        return TeamForecast(h,a,_sigmoid_margin(h-a,self.win_scale),
                            RIDGE_VERSION if self.kind=="ridge" else CANDIDATE_VERSION,
                            self.margin_sigma,self.total_sigma)

def _loss(model:RegressionPair, data:pd.DataFrame):
    m,t=model.predict_array(data)
    truth_m=(data.home_score-data.away_score).to_numpy()
    truth_t=(data.home_score+data.away_score).to_numpy()
    return float(np.mean(np.abs(m-truth_m))+np.mean(np.abs(t-truth_t)))


def train_candidates(frame:pd.DataFrame,features:list[str],train_before:str,
                     validation_before:str,enable_lightgbm=False) -> dict:
    """Choose on validation exclusively. Test partition is *never* used to tune."""
    train,val,test=chronological_split(frame,train_before,validation_before)
    candidates=[]
    for alpha in (1.0,10.0,50.0,200.0):
        obj=RegressionPair(kind="ridge",alpha=alpha).fit(train,features)
        candidates.append(("ridge",alpha,_loss(obj,val),obj))
    if enable_lightgbm:
        obj=RegressionPair(kind="lightgbm").fit(train,features)
        candidates.append(("lightgbm",None,_loss(obj,val),obj))
    candidates.sort(key=lambda x:x[2])
    best=candidates[0]
    model=best[3]
    # Learn probability calibration and residual uncertainty from validation only.
    val_margin,val_total=model.predict_array(val)
    y=(val.home_score>val.away_score).to_numpy(dtype=float)
    scales=(5,7,9,11,13,17)
    scores=[]
    for scale in scales:
        p=np.clip(1/(1+np.exp(-np.clip(val_margin/scale,-30,30))),1e-4,1-1e-4)
        scores.append(float(np.mean(-y*np.log(p)-(1-y)*np.log(1-p))))
    model.win_scale=float(scales[int(np.argmin(scores))])
    actual_margin=(val.home_score-val.away_score).to_numpy()
    actual_total=(val.home_score+val.away_score).to_numpy()
    model.margin_sigma=max(6.0,float(np.std(actual_margin-val_margin)))
    model.total_sigma=max(8.0,float(np.std(actual_total-val_total)))
    # Do not refit on test; frozen selection is directly evaluated there.
    m,t=model.predict_array(test)
    p=np.clip(1/(1+np.exp(-np.clip(m/model.win_scale,-30,30))),1e-4,1-1e-4)
    yy=(test.home_score>test.away_score).to_numpy(dtype=float)
    return {
        "selected_kind":best[0],"selected_alpha":best[1],
        "candidate":model,
        "train_n":len(train),"validation_n":len(val),"test_n":len(test),
        "validation_objectives":[{
            "model":kind,"alpha":alpha,"margin_plus_total_mae":round(loss,4)}
            for kind,alpha,loss,_ in candidates
        ],
        "test_metrics":{
            "margin_mae":round(float(np.mean(np.abs(m-(test.home_score-test.away_score)))),4),
            "total_mae":round(float(np.mean(np.abs(t-(test.home_score+test.away_score)))),4),
            "win_log_loss":round(float(np.mean(-yy*np.log(p)-(1-yy)*np.log(1-p))),4),
            "win_brier":round(float(np.mean((p-yy)**2)),4),
            "winner_accuracy":round(float(np.mean((p>=0.5)==yy)),4),
        },
        "train_before":train_before,"validation_before":validation_before,
        "uses_test_to_select":False,
    }
