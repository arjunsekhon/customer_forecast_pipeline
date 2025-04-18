import pandas as pd
import numpy as np
from pathlib import Path

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Paths
DATA_DIR = Path("data")
TRANSFORMED_CSV = DATA_DIR / "transformed_data.csv"
FORECAST_CSV = DATA_DIR / "forecasts.csv"
MC_CSV = DATA_DIR / "monte_carlo_results.csv"

# Statistical concepts:
# - Decomposition: separates series into trend, seasonality, and residual (descriptive)
# - Exponential Smoothing (ETS): captures level, trend, and (optionally) seasonality (predictive)
# - Monte Carlo: simulates random deviations around point forecasts (probabilistic predictive)

def forecast():
    # 1. Load transformed data
    df = pd.read_csv(TRANSFORMED_CSV, parse_dates=["period_date"])
    df.set_index("period_date", inplace=True)

    n_obs = len(df)
    seasonal_periods = 12

    # 2. Decompose net_new into components if sufficient history
    if n_obs >= 2 * seasonal_periods:
        decomposition = seasonal_decompose(df["net_new"], model="multiplicative", period=seasonal_periods)
        resid = decomposition.resid.dropna()
        print("Performed seasonal decomposition (trend, seasonal, residual).")
    else:
        print(f"Insufficient data for seasonal decomposition (need ≥{2*seasonal_periods}, got {n_obs}); skipping.")
        # Use deviations from mean as residuals
        resid = df["net_new"] - df["net_new"].mean()
        resid = resid.fillna(0)

    resid_std = resid.std()

    # 3. Fit ETS model (with or without seasonality)
    if n_obs >= 2 * seasonal_periods:
        print("Fitting ETS model with additive trend and multiplicative seasonality.")
        model = ExponentialSmoothing(
            df["net_new"],
            trend="add",
            seasonal="mul",
            seasonal_periods=seasonal_periods
        )
    else:
        print("Fitting ETS model with additive trend only (no seasonality).")
        model = ExponentialSmoothing(
            df["net_new"],
            trend="add",
            seasonal=None
        )

    fit = model.fit()
    print("ETS model fitted.")

    # 4. Generate point forecasts
    future_periods = seasonal_periods if n_obs >= seasonal_periods else n_obs
    last_date = df.index[-1] + pd.offsets.MonthBegin()
    forecast_index = pd.date_range(start=last_date, periods=future_periods, freq="MS")
    point_forecast = fit.forecast(future_periods)

    point_df = pd.DataFrame({
        "period_date": forecast_index,
        "forecast_net_new": point_forecast.values
    })
    point_df.to_csv(FORECAST_CSV, index=False)
    print(f"Point forecasts written to {FORECAST_CSV}")

    # 5. Monte Carlo simulation around forecasts
    rng = np.random.default_rng()
    # reshape loc to (future_periods, 1) for broadcasting
    loc = point_forecast.values.reshape(-1, 1)
    scale = resid_std
    sims = rng.normal(loc=loc, scale=scale, size=(future_periods, 1000))

    mc_df = pd.DataFrame(sims, index=forecast_index)
    mc_df.to_csv(MC_CSV)
    print(f"Monte Carlo results written to {MC_CSV}")

if __name__ == "__main__":
    forecast()
