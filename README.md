# customer_forecast_pipeline

This repo is a simple introduction to time series analysis and the forecasting of customer counts.

First you will need to install `uv` the python package manager

```bash
curl -LsSf https://astral.sh/uv/0.6.14/install.sh | sh
```

or

```bash
brew install uv
```

Make a copy of the `.env.sample` and then change the values of the environment variables.

```bash
cp .env.sample .env
```

Then run

```bash
uv sync
```

Run script (entry script is `main.py`)

```bash
uv run
```
