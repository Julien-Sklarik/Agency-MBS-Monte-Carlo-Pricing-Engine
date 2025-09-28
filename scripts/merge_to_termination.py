import sys
import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage  python scripts/merge_to_termination.py path_to_default.csv path_to_prepay.csv out_csv")
        raise SystemExit(1)
    path_def = sys.argv[1]
    path_pre = sys.argv[2]
    out_csv = sys.argv[3]

    d = pd.read_csv(path_def)
    p = pd.read_csv(path_pre)

    key_cols = ["loan_id", "month_id"]
    d = d.rename(columns={"isdefault": "is_default", "isdefault_month": "month_id", "loanid": "loan_id"})
    p = p.rename(columns={"isprepaid": "is_prepay", "isprepaid_month": "month_id", "loanid": "loan_id"})

    df = pd.merge(d, p, on=key_cols, how="outer", suffixes=("_d", "_p"))
    if "is_default" not in df.columns and "isdefault" in df.columns:
        df["is_default"] = df["isdefault"]
    if "is_prepay" not in df.columns and "isprepaid" in df.columns:
        df["is_prepay"] = df["isprepaid"]

    for c in ["is_default", "is_prepay"]:
        if c not in df.columns:
            df[c] = 0
        df[c] = df[c].fillna(0).astype(int)

    df.to_csv(out_csv, index=False)
    print("wrote", out_csv)
