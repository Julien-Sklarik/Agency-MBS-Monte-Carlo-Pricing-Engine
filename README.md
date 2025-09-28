# Agency MBS Monte Carlo Pricing Engine

I built this project to price agency mortgage pools using a one-factor short rate model together with loan-level termination models for prepayment and default. The work started during my time at UC Berkeley.

---

## What I did

I implemented an interest rate path simulator based on the Hull-White one-factor model.  
I trained logistic models for prepayment and default on loan-level data.  
I built a cashflow engine that projects balances and losses at monthly frequency.  
I wrapped everything in a Monte Carlo pricing engine that produces OAS-style spread results and standard risk metrics such as DV01.

---

## Why it matters

Liquidity, prepayment, and default dynamics strongly influence mortgage pricing.  
By combining rate simulations with loan-level termination models, I was able to extract realistic cashflows and price pools under multiple scenarios.  
This type of framework is directly useful for both buy-side and sell-side trading desks.

---

## Quick start

1. Create and activate a virtual environment of your choice  
2. Install dependencies  

