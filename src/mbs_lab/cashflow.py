from __future__ import annotations
import numpy as np
import pandas as pd

def scheduled_payment(balance: float, rate_annual: float, maturity_months: int) -> float:
    r = rate_annual / 12.0
    if r <= 0 or maturity_months <= 0:
        return balance / maturity_months
    ann = r * (1 + r) ** maturity_months / ((1 + r) ** maturity_months - 1)
    return balance * ann

def project_pool_cashflows(
    pool_size: float,
    wac: float,
    maturity_months: int,
    smm_series: np.ndarray,
    default_series: np.ndarray,
    loss_severity: float = 0.4
) -> pd.DataFrame:
    bal = pool_size
    pay = scheduled_payment(bal, wac, maturity_months)
    records = []
    for m in range(maturity_months):
        r_month = wac / 12.0
        interest = bal * r_month
        sched_prin = max(pay - interest, 0.0)
        smm = float(smm_series[m]) if m < len(smm_series) else float(smm_series[-1])
        dmm = float(default_series[m]) if m < len(default_series) else float(default_series[-1])
        prepay_prin = (bal - sched_prin) * smm
        default_prin = (bal - sched_prin - prepay_prin) * dmm
        loss = default_prin * loss_severity
        cash_to_investor = interest + sched_prin + prepay_prin + default_prin - loss
        new_bal = bal - sched_prin - prepay_prin - default_prin
        records.append({
            "month": m + 1,
            "balance_in": bal,
            "interest": interest,
            "scheduled_principal": sched_prin,
            "prepayment_principal": prepay_prin,
            "default_principal": default_prin,
            "loss": loss,
            "cash_to_investor": cash_to_investor,
            "balance_out": new_bal
        })
        bal = new_bal
        if bal <= 1e-6:
            break
    return pd.DataFrame.from_records(records)
