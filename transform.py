import pandas as pd
from pathlib import Path

data_dir = Path("data")
staging_csv = data_dir / "raw_data.csv"
transformed_csv = data_dir / "transformed_data.csv"

def transform():
    # 1. Load the staged raw data
    df = pd.read_csv(staging_csv, parse_dates=["period_date"])

    # 2. Compute net new customers (inflow - outflow)
    df["net_new"] = df["new_customers"] - df["churned_customers"]

    # 3. Cumulative customer base (level component of time series)
    df["customer_base"] = df["net_new"].cumsum() + df.loc[0, "opening_customers"]

    # 4. Add a time index for regression/ARIMA models for linear trend modeling
    df["time_index"] = range(1, len(df) + 1)

    # 5. Save the transformed data
    df.to_csv(transformed_csv, index=False)
    print(f"Transformed data written to {transformed_csv}")

if __name__ == "__main__":
    transform()
