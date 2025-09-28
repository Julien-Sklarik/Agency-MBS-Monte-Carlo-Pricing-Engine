import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(7)
n_loans = 1000
hpi_yr = rng.normal(0.03, 0.05, size=n_loans)
fico = rng.integers(620, 800, size=n_loans)
orig_rate = rng.uniform(0.025, 0.05, size=n_loans)
ltv0 = rng.uniform(0.6, 0.95, size=n_loans)
maturity = rng.integers(240, 360, size=n_loans)
zip5 = rng.integers(90000, 96162, size=n_loans)

rows = []
for i in range(n_loans):
    bal = rng.uniform(150000, 800000)
    months = int(maturity[i])
    for m in range(1, months + 1):
        age = m
        ltv = max(0.2, ltv0[i] * (1.0 - 0.001 * m))
        coup_diff = orig_rate[i] - rng.uniform(0.02, 0.06)
        is_pre = 1 if rng.random() < max(0.0, 0.02 + 0.4 * max(0.0, -coup_diff)) else 0
        is_def = 1 if rng.random() < max(0.0, 0.001 + 0.02 * max(0.0, ltv - 0.8)) else 0
        rows.append({
            "loan_id": i,
            "month_id": m,
            "is_prepay": is_pre,
            "is_default": is_def,
            "original_rate": float(orig_rate[i]),
            "current_balance": float(bal),
            "current_ltv": float(ltv),
            "fico": int(fico[i]),
            "zip5": int(zip5[i]),
            "age_months": int(age),
            "coupon_diff": float(coup_diff),
            "hpi_change_yr": float(hpi_yr[i]),
            "remaining_maturity": int(months - m + 1)
        })
        if is_pre == 1 or is_def == 1:
            break

df = pd.DataFrame.from_records(rows)
out_dir = Path("data/synthetic")
out_dir.mkdir(parents=True, exist_ok=True)
df.to_csv(out_dir / "termination_sample.csv", index=False)
print("wrote", out_dir / "termination_sample.csv")
