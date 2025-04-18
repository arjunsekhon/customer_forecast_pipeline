import pandas as pd
import numpy as np
from pathlib import Path
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus

from config import PRESCRIPTIVE_BUDGET, MAX_MONTHLY_SPEND

# Paths
DATA_DIR = Path("data")
FORECAST_CSV = DATA_DIR / "forecasts.csv"
PRESCRIPTIONS_CSV = DATA_DIR / "prescriptions.csv"

# Statistical concepts:
# - Linear regression: estimates spend ↦ net_new relationship (predictive)
# - Linear programming: maximizes objective under budget constraint (prescriptive)

def optimise():
    # 1. Load historical data to fit spend ↦ net_new model
    hist = pd.read_csv(DATA_DIR / "transformed_data.csv", parse_dates=["period_date"])
    # Fit simple linear regression: net_new = a + b * marketing_spend
    coeffs = np.polyfit(hist["marketing_spend"], hist["net_new"], 1)
    b, a = coeffs
    print(f"Regression fit: net_new = {a:.2f} + {b:.4f} * spend")

    # 2. Load forecast periods
    df_fc = pd.read_csv(FORECAST_CSV, parse_dates=["period_date"])
    periods = df_fc["period_date"].dt.to_period("M").astype(str)

    # 3. Define LP problem
    prob = LpProblem("Spend_Allocation", LpMaximize)
    # Decision variables: spend_t for each period
    spend_vars = {
        p: LpVariable(f"Spend_{p}", lowBound=0, upBound=MAX_MONTHLY_SPEND)
        for p in periods
    }

    # Objective: maximize total estimated net_new = sum(a + b*spend_t)
    # Constants drop out; equivalent to maximizing b * sum(spend_t)
    prob += b * lpSum(spend_vars[p] for p in periods), "Maximize_Net_New"

    # Constraint: total spend ≤ budget
    prob += lpSum(spend_vars[p] for p in periods) <= PRESCRIPTIVE_BUDGET, "Total_Budget"

    # 4. Solve
    prob.solve()
    print(f"Optimization status: {LpStatus[prob.status]}")

    # 5. Export prescriptions
    records = []
    for p in periods:
        spend = spend_vars[p].varValue
        est_net = a + b * spend
        records.append({"period_date": f"{p}-01", "optimal_spend": spend, "estimated_net_new": est_net})

    pd.DataFrame(records).to_csv(PRESCRIPTIONS_CSV, index=False)
    print(f"Prescriptions written to {PRESCRIPTIONS_CSV}")

if __name__ == "__main__":
    optimise()
