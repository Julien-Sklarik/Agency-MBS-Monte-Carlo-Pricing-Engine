from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import joblib
from pathlib import Path

CORE_FEATURES = [
    "original_rate",
    "current_ltv",
    "fico",
    "age_months",
    "coupon_diff",
    "hpi_change_yr",
    "remaining_maturity",
]

def _make_pipeline():
    return Pipeline([
        ("scaler", StandardScaler(with_mean=True, with_std=True)),
        ("logit", LogisticRegression(max_iter=1000, n_jobs=None))
    ])

def fit_binary_model(df: pd.DataFrame, label: str, model_path: str) -> dict:
    df = df.dropna(subset=CORE_FEATURES + [label]).copy()
    X = df[CORE_FEATURES].values
    y = df[label].astype(int).values
    pipe = _make_pipeline()
    pipe.fit(X, y)
    pred = pipe.predict_proba(X)[:, 1]
    auc = roc_auc_score(y, pred)
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, model_path)
    return {"label": label, "auc_in_sample": float(auc), "n_obs": int(len(df))}

def load_model(model_path: str):
    return joblib.load(model_path)

def smm_from_features(pipe, X: np.ndarray, floor: float = 1e-6, cap: float = 0.6) -> np.ndarray:
    p = pipe.predict_proba(X)[:, 1]
    p = np.clip(p, floor, cap)
    return p

def default_prob_from_features(pipe, X: np.ndarray, floor: float = 1e-6, cap: float = 0.2) -> np.ndarray:
    p = pipe.predict_proba(X)[:, 1]
    p = np.clip(p, floor, cap)
    return p
