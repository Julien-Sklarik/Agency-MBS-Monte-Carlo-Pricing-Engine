from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from .rates import simulate_hull_white_paths, discount_factors_from_paths
from .models import fit_binary_model, load_model, CORE_FEATURES, smm_from_features, default_prob_from_features
from .cashflow import project_pool_cashflows
from .utils import set_seed
import yaml
from numpy.linalg import norm

def run_training(cfg_path: str) -> dict:
    cfg = yaml.safe_load(open(cfg_path, "r"))
    set_seed(cfg["seed"])
    df = pd.read_csv(cfg["data"]["csv_path"])
    out_dir = Path(cfg["artifacts_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    res = {}
    res["prepay"] = fit_binary_model(df, cfg["labels"]["prepay"], str(out_dir / "prepay_model.joblib"))
    res["default"] = fit_binary_model(df, cfg["labels"]["default"], str(out_dir / "default_model.joblib"))
    with open(out_dir / "training_report.txt", "w", encoding="utf-8") as f:
        for k, v in res.items():
            f.write(f"{k}  {v}\n")
    return res

def price_one(cfg_path: str) -> dict:
    cfg = yaml.safe_load(open(cfg_path, "r"))
    set_seed(cfg["seed"])

    # rate paths
    n_paths = cfg["rates"]["n_paths"]
    n_steps = cfg["rates"]["n_steps"]
    dt = cfg["rates"]["dt"]
    r0 = cfg["rates"]["r0"]
    a = cfg["rates"]["a"]
    sigma = cfg["rates"]["sigma"]
    theta = cfg["rates"]["theta"]
    r_paths = simulate_hull_white_paths(n_paths, n_steps, dt, a, sigma, r0, theta)
    df_paths = discount_factors_from_paths(r_paths, dt)

    # models
    df_all = pd.read_csv(cfg["data"]["csv_path"])
    X = df_all[CORE_FEATURES].fillna(method="ffill").fillna(method="bfill").values

    prepay_pipe = load_model(str(Path(cfg["artifacts_dir"]) / "prepay_model.joblib"))
    default_pipe = load_model(str(Path(cfg["artifacts_dir"]) / "default_model.joblib"))

    smm_vec = np.clip(smm_from_features(prepay_pipe, X), 1e-6, 0.6)
    dmm_vec = np.clip(default_prob_from_features(default_pipe, X), 1e-6, 0.2)

    # cashflows per path
    pool = cfg["pool"]
    cash_per_path = []
    pv_per_path = []
    for i in range(n_paths):
        cf = project_pool_cashflows(
            pool_size=pool["upb"],
            wac=pool["wac"],
            maturity_months=pool["maturity_months"],
            smm_series=smm_vec,
            default_series=dmm_vec,
            loss_severity=pool["loss_severity"]
        )
        # discount along path
        steps = min(len(cf), n_steps)
        df_line = df_paths[i, :steps]
        pv = float(np.sum(cf["cash_to_investor"].values[:steps] * df_line))
        cash_per_path.append(cf)
        pv_per_path.append(pv)

    price_mc = float(np.mean(pv_per_path))
    out = {
        "price_mc": price_mc,
        "pv_per_path_summary": {
            "mean": float(np.mean(pv_per_path)),
            "std": float(np.std(pv_per_path)),
            "min": float(np.min(pv_per_path)),
            "max": float(np.max(pv_per_path)),
        }
    }
    Path(cfg["artifacts_dir"]).mkdir(parents=True, exist_ok=True)
    with open(Path(cfg["artifacts_dir"]) / "pricing_report.txt", "w", encoding="utf-8") as f:
        f.write(str(out))
    return out
