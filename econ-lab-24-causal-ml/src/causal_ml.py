import numpy as np
import pandas as pd


def summarize_ate(estimate: float, ci_lower: float, ci_upper: float) -> pd.DataFrame:
    """
    Return a one-row summary table for an ATE estimate.

    Parameters
    ----------
    estimate : float
        Point estimate of the average treatment effect.
    ci_lower : float
        Lower bound of the confidence interval.
    ci_upper : float
        Upper bound of the confidence interval.

    Returns
    -------
    pd.DataFrame
        A tidy summary table.
    """
    return pd.DataFrame(
        {
            "estimate": [estimate],
            "ci_lower": [ci_lower],
            "ci_upper": [ci_upper],
        }
    )


def classify_high_response(cate: np.ndarray, percentile: float = 75) -> np.ndarray:
    """
    Classify observations as high-response if their CATE is above
    the chosen percentile threshold.

    Parameters
    ----------
    cate : np.ndarray
        Array of individual treatment effect estimates.
    percentile : float, default=75
        Percentile cutoff used to define the high-response subgroup.

    Returns
    -------
    np.ndarray
        Boolean array indicating high-response observations.
    """
    threshold = np.percentile(cate, percentile)
    return cate >= threshold


def compare_group_means(
    data: pd.DataFrame,
    mask: np.ndarray,
    columns: list[str],
) -> pd.DataFrame:
    """
    Compare mean characteristics for a subgroup vs. the rest of the sample.

    Parameters
    ----------
    data : pd.DataFrame
        Input dataframe.
    mask : np.ndarray
        Boolean mask defining the subgroup.
    columns : list[str]
        Columns to compare.

    Returns
    -------
    pd.DataFrame
        Table of subgroup and non-subgroup means.
    """
    subgroup = data.loc[mask, columns]
    remainder = data.loc[~mask, columns]

    return pd.DataFrame(
        {
            "high_response_mean": subgroup.mean(),
            "other_mean": remainder.mean(),
        }
    )


def cate_by_quartile(
    data: pd.DataFrame,
    income_col: str,
    cate_col: str,
) -> pd.DataFrame:
    """
    Compute mean, standard deviation, and count of CATEs by income quartile.

    Parameters
    ----------
    data : pd.DataFrame
        Input dataframe containing income and CATE columns.
    income_col : str
        Name of income column.
    cate_col : str
        Name of CATE column.

    Returns
    -------
    pd.DataFrame
        Quartile-level summary table.
    """
    temp = data.copy()
    temp["inc_quartile"] = pd.qcut(temp[income_col], q=4, labels=["Q1", "Q2", "Q3", "Q4"])

    return temp.groupby("inc_quartile")[cate_col].agg(["mean", "std", "count"])


def sensitivity_interval(
    theta_lower: float,
    theta_hat: float,
    theta_upper: float,
) -> dict:
    """
    Package a sensitivity-analysis interval into a simple dictionary.

    Parameters
    ----------
    theta_lower : float
        Lower sensitivity bound.
    theta_hat : float
        Point estimate.
    theta_upper : float
        Upper sensitivity bound.

    Returns
    -------
    dict
        Dictionary with labeled interval components.
    """
    return {
        "theta_lower": theta_lower,
        "theta_hat": theta_hat,
        "theta_upper": theta_upper,
    }
