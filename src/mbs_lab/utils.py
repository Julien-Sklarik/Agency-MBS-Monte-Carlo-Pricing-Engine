from __future__ import annotations
import numpy as np
import pandas as pd
import pathlib
import json

def set_seed(seed: int = 42) -> None:
    import random
    import numpy as np
    random.seed(seed)
    np.random.seed(seed)

def to_monthly_rate(annual_rate: float) -> float:
    return annual_rate / 12.0

def load_csv(path):
    return pd.read_csv(path)

def save_json(obj, path):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
