"""Calibration fitted on data strictly later than model selection and before holdout.

Probability: regularized Platt regression on the log-odds of a frozen model.
Intervals: split-conformal absolute residuals with finite-sample correction.
None of these methods guarantees calibration under distribution shift.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil
import numpy as np

EPS=1e-5

def bounded_prob(values):
    x=np.asarray(values,dtype=float)
    if np.any(~np.isfinite(x)):
        raise ValueError("Non-finite win probability")
    if np.any((x<0)|(x>1)):
        raise ValueError("Win probability outside [0,1]")
    return np.clip(x,EPS,1-EPS)

def log_loss(probs,labels):
    p=bounded_prob(probs)
    y=np.asarray(labels,dtype=float)
    if p.shape!=y.shape or not np.all(np.isin(y,(0,1))):
        raise ValueError("Mismatched win labels")
    return float(np.mean(-y*np.log(p)-(1-y)*np.log(1-p)))

def brier(probs,labels):
    p=bounded_prob(probs)
    y=np.asarray(labels,dtype=float)
    if p.shape!=y.shape or not np.all(np.isin(y,(0,1))):
        raise ValueError("Mismatched win labels")
    return float(np.mean((p-y)**2))

class PlattCalibrator:
    """Regularized logistic transformation; fit only on calibration segment."""
    def __init__(self,c=0.4):
        self.c=float(c)
        self.model=None
        self.fitted_n=0
    def fit(self,raw_probabilities,labels):
        from sklearn.linear_model import LogisticRegression
        p=bounded_prob(raw_probabilities)
        y=np.asarray(labels,dtype=int)
        if len(p)<80 or len(set(y))!=2 or len(p)!=len(y):
            raise ValueError("Need >=80 calibration games with both outcomes")
        logits=np.log(p/(1-p)).reshape(-1,1)
        self.model=LogisticRegression(C=self.c,solver="lbfgs",
                                      random_state=41,max_iter=1000)
        self.model.fit(logits,y)
        self.fitted_n=len(p)
        return self
    def predict(self,raw_probabilities):
        if self.model is None:
            raise RuntimeError("Calibrator not fitted")
        p=bounded_prob(raw_probabilities)
        logits=np.log(p/(1-p)).reshape(-1,1)
        return np.clip(self.model.predict_proba(logits)[:,1],EPS,1-EPS)
    def parameters(self):
        if self.model is None:
            raise RuntimeError("Not fitted")
        return {"coefficient":float(self.model.coef_[0,0]),
                "intercept":float(self.model.intercept_[0]),
                "regularization_c":self.c,"calibration_games":self.fitted_n}

class ConformalIntervals:
    """Symmetric prediction intervals using only future-held-out calibration errors.

    Finite-sample quantile q = sorted(abs(y-pred))[ceil((n+1)*(1-alpha))-1]
    with finite-sample guard. Multiple thresholds can share the same
    calibration segment; report realized held-out coverage separately.
    """
    def __init__(self,coverages=(.50,.80,.90)):
        values=tuple(float(x) for x in coverages)
        if not values or any(x<=0 or x>=1 for x in values):
            raise ValueError("Interval coverage must lie in (0,1)")
        self.coverages=values
        self.quantiles={}
        self.n=0
    def fit(self,predicted,actual):
        p=np.asarray(predicted,dtype=float)
        a=np.asarray(actual,dtype=float)
        if p.shape!=a.shape or len(p)<80 or not np.all(np.isfinite(p+a)):
            raise ValueError("Need >=80 finite calibration residuals")
        residuals=np.sort(np.abs(p-a))
        self.n=len(residuals)
        self.quantiles={
            str(round(level,2)):float(residuals[min(
                len(residuals)-1,ceil((len(residuals)+1)*level)-1)])
            for level in self.coverages
        }
        return self
    def intervals(self,predicted,coverage=.8):
        key=str(round(float(coverage),2))
        if key not in self.quantiles:
            raise ValueError("Coverage not fitted")
        p=np.asarray(predicted,dtype=float)
        q=self.quantiles[key]
        return p-q,p+q
    def score(self,predicted,actual):
        y=np.asarray(actual,dtype=float)
        results={}
        for level in self.coverages:
            lo,hi=self.intervals(predicted,level)
            results[str(round(level,2))]={
                "nominal_coverage":level,
                "observed_coverage":round(float(np.mean((y>=lo)&(y<=hi))),4),
                "half_width_points":round(self.quantiles[str(round(level,2))],3),
                "calibration_games":self.n,
            }
        return results

def paired_bootstrap_loss_delta(ref_prob,new_prob,y,iterations=800,seed=41):
    """Mean new-minus-reference log-loss, with paired bootstrap CI."""
    p0=bounded_prob(ref_prob);p1=bounded_prob(new_prob)
    y=np.asarray(y,dtype=float)
    if len(p0)!=len(p1) or len(p0)!=len(y) or not len(y):
        raise ValueError("Need matched games and labels")
    e0=-y*np.log(p0)-(1-y)*np.log(1-p0)
    e1=-y*np.log(p1)-(1-y)*np.log(1-p1)
    diff=e1-e0
    rng=np.random.default_rng(seed)
    n=len(diff)
    means=np.array([float(np.mean(diff[rng.integers(n,size=n)]))
                    for _ in range(iterations)])
    return {"delta_new_minus_reference":round(float(np.mean(diff)),5),
            "paired_95pct_interval":[round(float(v),5)
                for v in np.quantile(means,[.025,.975])],
            "n_games":n,"bootstrap_iterations":iterations,
            "interpretation":"Negative is better, interval spanning zero is inconclusive"}
