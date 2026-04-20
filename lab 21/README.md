# Time Series Forecasting — ARIMA, GARCH & Bootstrap

## Objective
This project develops a professional time series forecasting workflow by diagnosing and correcting a broken ARIMA pipeline, extending the analysis with GARCH volatility modeling, and implementing reusable forecast evaluation tools for backtesting and uncertainty quantification.

## Methodology
- Diagnosed three modeling errors in the original ARIMA pipeline:
  - incorrect differencing on non-stationary CPI data
  - omitted seasonality in monthly CPI
  - missing residual diagnostics before forecasting
- Rebuilt the forecasting pipeline using SARIMA with appropriate differencing and seasonal structure for monthly CPI
- Verified model adequacy using the Augmented Dickey-Fuller test and Ljung-Box residual diagnostics
- Modeled S&P 500 daily log-return volatility with a GARCH(1,1) specification
- Evaluated volatility persistence using `alpha[1]`, `beta[1]`, `alpha + beta`, and the half-life of volatility shocks
- Built a reusable `forecast_evaluation.py` module with:
  - `compute_mase()` for scale-free forecast accuracy evaluation
  - `backtest_expanding_window()` for rolling real-time backtesting
- Extended the workflow with block bootstrap forecast intervals to generate distribution-free forecast uncertainty bands

## Key Findings
- The corrected SARIMA workflow substantially improved the original broken CPI forecasting pipeline by addressing both non-stationarity and monthly seasonality.
- Residual diagnostics showed that model adequacy must be checked explicitly rather than assuming a fitted ARIMA specification is valid.
- S&P 500 returns exhibited strong volatility clustering, justifying a conditional variance model rather than a constant-variance assumption.
- The GARCH(1,1) results indicated persistent but mean-reverting volatility, with `alpha + beta` below 1.
- Estimated volatility persistence was high, implying that market shocks decay gradually rather than disappearing immediately.
- The maximum conditional volatility occurred during the COVID-era market shock, consistent with extreme financial stress.
- The reusable evaluation module makes the workflow portable across future forecasting tasks and supports more production-style model validation.

## Project Structure
- `notebooks/` — diagnostic lab notebook and analysis workflow
- `src/forecast_evaluation.py` — reusable forecast evaluation and backtesting functions
- `figures/` — exported charts and visual outputs
- `README.md` — project summary and documentation

## Tools Used
- Python
- pandas
- numpy
- matplotlib
- statsmodels
- pmdarima
- arch
- yfinance
- fredapi

## Professional Takeaway
This lab demonstrates an end-to-end forecasting workflow that moves beyond fitting a model mechanically. It emphasizes diagnostic discipline, volatility modeling, reusable evaluation utilities, and robust interval construction, which are all essential for applied economic and financial time series analysis.
