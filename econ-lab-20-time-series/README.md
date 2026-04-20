# Time Series Diagnostics & Advanced Decomposition

## Objective
This project develops a diagnosis-first workflow for time series analysis, combining decomposition, stationarity testing, structural break detection, and uncertainty quantification into a reusable and portfolio-ready toolkit.

## Project Overview
In this lab, I implemented a structured time series diagnostics pipeline using both macroeconomic and simulated data. The workflow began by identifying and correcting methodological errors in seasonal decomposition and stationarity testing, and then extended into multi-seasonal decomposition, block bootstrap uncertainty estimation, and regime-based structural analysis.

The project was designed not only to demonstrate correct statistical reasoning, but also to package the analysis into reusable components suitable for applied economic and data science work.

## Methodology
- Diagnosed and fixed a broken STL decomposition applied directly to multiplicative retail sales data by introducing a log transformation.
- Corrected a misspecified Augmented Dickey-Fuller (ADF) test by using the appropriate deterministic terms for trending GDP data.
- Applied MSTL to simulated hourly electricity demand with both daily and weekly seasonal cycles.
- Implemented a moving block bootstrap to generate uncertainty bands for the GDP trend while preserving residual autocorrelation.
- Detected structural breaks in GDP growth using the PELT algorithm.
- Conducted per-regime ADF and KPSS stationarity tests after segmentation.
- Built a reusable `decompose.py` module with:
  - `run_stl()`
  - `test_stationarity()`
  - `detect_breaks()`
- Extended the project with AI-assisted module and app design for a more production-oriented workflow.

## Key Findings
- Retail sales exhibit multiplicative seasonality, so applying additive STL directly to the raw series distorts the seasonal component. A log transformation corrected this issue.
- Real GDP in levels is non-stationary under the correct ADF specification with constant and trend, consistent with macroeconomic theory.
- Differenced GDP behaves much closer to a stationary process.
- MSTL successfully separated daily and weekly seasonal components in the simulated electricity demand series.
- Block bootstrap confidence bands for GDP trend were wider during recessionary periods, indicating higher trend uncertainty during macroeconomic stress.
- Structural break detection identified regime changes in GDP growth, and stationarity testing suggested that growth is more plausibly stationary within regimes than across the full sample.

## Main Economic Interpretation
The central result is that GDP behaves like an **I(1) macroeconomic series in levels**, while growth rates are substantially more stable once structural changes are taken into account. This reinforces the importance of matching decomposition and testing methods to the actual data-generating process rather than relying on default settings.

## Files
- `notebooks/` — lab notebook and analysis workflow
- `src/decompose.py` — reusable decomposition and diagnostics module
- `figures/` — exported plots and screenshots
- `requirements.txt` — project dependencies
- `verification_log.md` — AI usage, modifications, and validation notes

## How to Reproduce
1. Install dependencies from `requirements.txt`.
2. Add your FRED API key where required.
3. Run the notebook from top to bottom to reproduce all results.
4. Export the reusable functions into `src/decompose.py`.
5. Run the module self-tests and notebook verification checks.
6. Optionally run the Streamlit app for the AI-assisted expansion.

## Skills Demonstrated
- Time series decomposition
- Stationarity testing
- Model specification diagnosis
- Multi-seasonal analysis with MSTL
- Structural break detection
- Bootstrap uncertainty quantification
- Reusable Python module design
- Applied economic interpretation of macro time series
