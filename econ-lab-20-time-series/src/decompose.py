"""
decompose.py — Time Series Decomposition & Diagnostics Module

Reusable functions for STL decomposition, stationarity testing,
structural break detection, MSTL decomposition, and block-bootstrap
trend uncertainty estimation.

Author: [Your Name]
Course: ECON 5200, Lab 20
"""

from __future__ import annotations

import warnings
from typing import Any

import numpy as np
import pandas as pd
import ruptures as rpt
from statsmodels.tsa.seasonal import STL, MSTL
from statsmodels.tsa.stattools import adfuller, kpss


def _validate_series(series: pd.Series) -> pd.Series:
    """Validate input and return a cleaned numeric pandas Series.

    Args:
        series: Input time series.

    Returns:
        Cleaned numeric Series with missing values removed.

    Raises:
        TypeError: If input is not a pandas Series.
        ValueError: If too few valid observations remain.
    """
    if not isinstance(series, pd.Series):
        raise TypeError("series must be a pandas Series")

    clean = pd.to_numeric(series, errors="coerce").dropna()

    if len(clean) < 8:
        raise ValueError("series is too short after dropping missing values")

    return clean


def _choose_regression(series: pd.Series) -> str:
    """Choose deterministic terms for ADF/KPSS testing.

    Uses a simple trend heuristic:
    - 'ct' for strongly trending series
    - 'c' otherwise

    Args:
        series: Input series.

    Returns:
        Regression specifier ('c' or 'ct').
    """
    clean = _validate_series(series)
    x = np.arange(len(clean), dtype=float)
    y = clean.values.astype(float)

    if np.std(y) == 0:
        return "c"

    corr = np.corrcoef(x, y)[0, 1]
    if np.isnan(corr):
        return "c"

    return "ct" if abs(corr) >= 0.6 else "c"


def infer_period_from_index(index: pd.DatetimeIndex) -> int:
    """Infer a default seasonal period from a DatetimeIndex.

    Args:
        index: DatetimeIndex.

    Returns:
        Default seasonal period:
        - 12 for monthly
        - 4 for quarterly
        - 52 for weekly
        - 7 for daily
        - 24 for hourly
        - 12 otherwise
    """
    freq = pd.infer_freq(index)
    if freq is None:
        return 12

    freq = freq.upper()

    if freq.startswith("M"):
        return 12
    if freq.startswith("Q"):
        return 4
    if freq.startswith("W"):
        return 52
    if freq.startswith("D"):
        return 7
    if freq.startswith("H"):
        return 24

    return 12


def run_stl(
    series: pd.Series,
    period: int = 12,
    log_transform: bool = True,
    robust: bool = True
):
    """Apply STL decomposition with optional log-transform.

    Args:
        series: Time series with DatetimeIndex.
        period: Seasonal period (12=monthly, 4=quarterly).
        log_transform: Whether to log-transform before STL.
        robust: Whether to use robust STL fitting.

    Returns:
        STL result object with .trend, .seasonal, and .resid.

    Raises:
        ValueError: If period is invalid or log-transform is impossible.
    """
    clean = _validate_series(series)

    if period < 2:
        raise ValueError("period must be at least 2")

    if log_transform:
        if (clean <= 0).any():
            raise ValueError("series contains non-positive values; cannot log-transform")
        clean = np.log(clean)

    return STL(clean, period=period, robust=robust).fit()


def run_mstl(
    series: pd.Series,
    periods: list[int] | tuple[int, ...],
    log_transform: bool = False,
    robust: bool = True,
):
    """Apply MSTL decomposition for multiple seasonal periods.

    Args:
        series: Time series with DatetimeIndex.
        periods: Seasonal periods, e.g. [24, 168].
        log_transform: Whether to log-transform before decomposition.
        robust: Included for API consistency.

    Returns:
        MSTL result object with .trend, .seasonal, and .resid.

    Raises:
        ValueError: If periods are invalid or log-transform is impossible.
    """
    clean = _validate_series(series)

    if not periods or any(p < 2 for p in periods):
        raise ValueError("periods must be a non-empty list of integers >= 2")

    if log_transform:
        if (clean <= 0).any():
            raise ValueError("series contains non-positive values; cannot log-transform")
        clean = np.log(clean)

    return MSTL(clean, periods=list(periods)).fit()


def test_stationarity(series: pd.Series, alpha: float = 0.05) -> dict[str, Any]:
    """Run ADF and KPSS tests and return a 2x2 verdict.

    ADF null: unit root (non-stationary)
    KPSS null: stationary

    Args:
        series: Time series to test.
        alpha: Significance level.

    Returns:
        Dictionary with:
        - adf_stat
        - adf_p
        - kpss_stat
        - kpss_p
        - adf_regression
        - kpss_regression
        - verdict

        Verdict is one of:
        'stationary', 'non-stationary', 'contradictory', 'inconclusive'
    """
    clean = _validate_series(series)

    adf_regression = _choose_regression(clean)
    kpss_regression = "ct" if adf_regression == "ct" else "c"

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        adf_stat, adf_p, _, _, _, _ = adfuller(
            clean,
            autolag="AIC",
            regression=adf_regression,
        )

        kpss_stat, kpss_p, _, _ = kpss(
            clean,
            regression=kpss_regression,
            nlags="auto",
        )

    adf_reject = adf_p < alpha
    kpss_reject = kpss_p < alpha

    if adf_reject and not kpss_reject:
        verdict = "stationary"
    elif (not adf_reject) and kpss_reject:
        verdict = "non-stationary"
    elif adf_reject and kpss_reject:
        verdict = "contradictory"
    else:
        verdict = "inconclusive"

    return {
        "adf_stat": float(adf_stat),
        "adf_p": float(adf_p),
        "kpss_stat": float(kpss_stat),
        "kpss_p": float(kpss_p),
        "adf_regression": adf_regression,
        "kpss_regression": kpss_regression,
        "verdict": verdict,
    }


def detect_breaks(series: pd.Series, pen: float = 10) -> list[pd.Timestamp]:
    """Detect structural breaks using the PELT algorithm.

    Args:
        series: Time series with DatetimeIndex.
        pen: Penalty parameter. Higher values return fewer breaks.

    Returns:
        List of break dates as pd.Timestamp, excluding the terminal endpoint.
    """
    clean = _validate_series(series)

    if not isinstance(clean.index, pd.DatetimeIndex):
        raise TypeError("series must have a DatetimeIndex")

    signal = clean.values.astype(float)
    algo = rpt.Pelt(model="rbf").fit(signal)
    breakpoints = algo.predict(pen=pen)

    dates: list[pd.Timestamp] = []
    for bp in breakpoints:
        if bp < len(clean):
            dates.append(pd.Timestamp(clean.index[bp]))

    return dates


def block_bootstrap_trend(
    series: pd.Series,
    n_bootstrap: int = 200,
    block_size: int = 8,
    period: int | None = None,
    log_transform: bool = True,
    robust: bool = True,
) -> dict[str, Any]:
    """Generate block-bootstrap STL trend confidence bands.

    Args:
        series: Input series.
        n_bootstrap: Number of bootstrap replications.
        block_size: Length of sampled residual blocks.
        period: Seasonal period. If None, infer from index.
        log_transform: Whether to log-transform before STL.
        robust: Whether to use robust STL.

    Returns:
        Dict with:
        - original_result
        - trend_lower
        - trend_upper
        - boot_trends
        - ci_width
    """
    clean = _validate_series(series)

    if not isinstance(clean.index, pd.DatetimeIndex):
        raise TypeError("series must have a DatetimeIndex")

    if period is None:
        period = infer_period_from_index(clean.index)

    if block_size < 2:
        raise ValueError("block_size must be at least 2")

    original_result = run_stl(
        clean,
        period=period,
        log_transform=log_transform,
        robust=robust,
    )

    base_series = np.log(clean) if log_transform else clean.copy()
    n = len(base_series)

    original_trend = original_result.trend
    original_seasonal = original_result.seasonal
    original_resid = original_result.resid.values

    boot_trends = np.zeros((n_bootstrap, n))

    for b in range(n_bootstrap):
        boot_resid = np.zeros(n)
        idx = 0

        while idx < n:
            start = np.random.randint(0, n - block_size + 1)
            block = original_resid[start:start + block_size]
            end = min(idx + block_size, n)

            # Block bootstrap preserves local autocorrelation because
            # adjacent residuals stay together within sampled blocks.
            # An i.i.d. bootstrap would break this time dependence.
            boot_resid[idx:end] = block[:end - idx]
            idx = end

        boot_series = pd.Series(
            original_trend.values + original_seasonal.values + boot_resid,
            index=base_series.index,
        )

        if getattr(base_series.index, "freq", None) is not None:
            boot_series.index.freq = base_series.index.freq

        boot_result = STL(boot_series, period=period, robust=robust).fit()
        boot_trends[b, :] = boot_result.trend.values

    trend_lower = np.percentile(boot_trends, 5, axis=0)
    trend_upper = np.percentile(boot_trends, 95, axis=0)
    ci_width = trend_upper - trend_lower

    return {
        "original_result": original_result,
        "trend_lower": trend_lower,
        "trend_upper": trend_upper,
        "boot_trends": boot_trends,
        "ci_width": ci_width,
    }


if __name__ == "__main__":
    print("decompose.py loaded successfully.")

    idx = pd.date_range("2020-01-01", periods=72, freq="MS")
    toy = pd.Series(
        100 + 0.5 * np.arange(72) + 10 * np.sin(2 * np.pi * np.arange(72) / 12),
        index=idx,
    )

    stl_res = run_stl(toy, period=12, log_transform=False)
    print("run_stl ok:", hasattr(stl_res, "trend"))

    stat_res = test_stationarity(toy.diff().dropna())
    print("test_stationarity verdict:", stat_res["verdict"])

    break_res = detect_breaks(toy.diff().dropna(), pen=5)
    print("detect_breaks returned", len(break_res), "breaks")

    ci_res = block_bootstrap_trend(
        toy,
        n_bootstrap=20,
        block_size=6,
        period=12,
        log_transform=False,
    )
    print("bootstrap ci mean width:", float(np.mean(ci_res["ci_width"])))
