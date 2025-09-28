Agency MBS Monte Carlo Pricing Engine

A clean project that prices an agency mortgage pool with a one factor short rate model and loan level termination models for prepay and default. It grew from graduate research and is now structured like a production ready prototype for a buy side or sell side quant team.

What you get
* An interest rate path simulator with the Hull White one factor dynamic
* Loan level logistic models for prepay and default with easy training on csv data
* A cashflow engine at monthly frequency with SMM and default handling
* Monte Carlo pricing with OAS style spread solving and risk measures like DV01 and key rate dv01
* Reproducible runs via a single python entry point and config

Quick start
* Create and activate a virtual env of your choice
* pip install -r requirements.txt
* python scripts/train_models.py configs/example_config.yaml
* python scripts/price_example.py configs/example_config.yaml

Project layout
* src mbs_lab
    * rates.py   interest rate simulation
    * models.py  logistic models for prepay and default
    * cashflow.py  mortgage cashflow projection
    * engine.py  orchestration for pricing and risk
    * utils.py   helpers and shared types
* scripts
    * train_models.py  learn models from csv data
    * price_example.py  run pricing for one pool and produce outputs in docs
* configs
    * example_config.yaml  all knobs for a quick run
* data synthetic
    * generate_synth.py  small synthetic csvs with the right schema
* notebooks
    * exploration.ipynb  free form exploration note for visuals and checks
* tests
    * test_shapes.py  sanity checks to keep things from breaking
* docs
    * sample_outputs.md  markdown snapshots from a run on the synthetic data

Input data schema
The trainer expects a single csv with one row per loan month. The minimal set of columns is
* loan_id  string or int
* month_id  int count from origination month equal to one
* is_prepay  zero or one monthly flag
* is_default  zero or one monthly flag
* original_rate  annual percent
* current_balance  currency
* current_ltv  percent
* fico  integer credit score
* zip5  five digit postal code
* age_months  loan age in months
* coupon_diff  current mortgage rate minus origination rate in percent
* hpi_change_yr  local home price change percent over one year
* remaining_maturity  months

Notes
* The repo is presented as an independent project and does not mention coursework
* The code uses sklearn not scikit learn to keep names simple in requirements
* All randomness is seeded for repeatable runs
