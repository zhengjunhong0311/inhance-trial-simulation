"""
Sample size and power estimation for the INHANCE trial.

Question 4: analytical sample size for non-inferiority / superiority,
plus Monte Carlo power estimation for the interim analysis scenario.
"""

import numpy as np
from scipy import stats

from . import config


# ============================================================================
# Analytical sample size
# ============================================================================
def sample_size_onesided(
    delta: float,
    sigma: float,
    alpha_adj: float,
    power: float,
) -> int:
    """
    Sample size per group for a one-sided two-sample comparison.

    Parameters
    ----------
    delta : float
        Expected difference (positive).
    sigma : float
        Standard deviation.
    alpha_adj : float
        Adjusted one-sided significance level.
    power : float
        Target power.

    Returns
    -------
    int
        Required sample size per group.
    """
    z_alpha = stats.norm.ppf(1 - alpha_adj)
    z_beta = stats.norm.ppf(power)
    n = 2 * (z_alpha + z_beta) ** 2 * sigma ** 2 / delta ** 2
    return int(np.ceil(n))


def required_sample_size(
    sigma: float = config.SIGMA,
    delta_sup: float = config.DELTA_SUPERIORITY,
    delta_noninf: float = config.DELTA_NONINFERIORITY,
    alpha: float = config.ALPHA,
    power: float = config.POWER_TARGET,
    n_comp: int = config.N_COMPARISONS,
) -> dict:
    """
    Compute required sample size for both superiority and
    non-inferiority hypotheses.

    Returns
    -------
    dict
        with keys: alpha_adj, n_superiority, n_noninferiority, n_final, n_total
    """
    alpha_adj = alpha / n_comp
    n_sup = sample_size_onesided(delta_sup, sigma, alpha_adj, power)
    n_noninf = sample_size_onesided(abs(delta_noninf), sigma, alpha_adj, power)
    n_final = max(n_sup, n_noninf)
    return {
        "alpha_adj": alpha_adj,
        "n_superiority": n_sup,
        "n_noninferiority": n_noninf,
        "n_final": n_final,
        "n_total": n_final * n_comp,
    }


# ============================================================================
# Monte Carlo power (Question 4, task 2)
# ============================================================================
def estimate_power_pure(
    n_sim: int = 5000,
    n_per_group: int = 120,
    sigma: float = config.SIGMA,
    delta: float = config.DELTA_SUPERIORITY,
    alpha: float = config.ALPHA,
    n_comp: int = config.N_COMPARISONS,
    seed: int = 2025,
) -> float:
    """
    Estimate power of a single superiority test via Monte Carlo.

    Simulates placebo and treatment arms (each n_per_group subjects),
    performs a one-sided t-test at alpha / n_comp, returns the
    proportion of significant results.
    """
    rng = np.random.default_rng(seed)
    alpha_adj = alpha / n_comp
    successes = 0

    for _ in range(n_sim):
        placebo = rng.normal(0, sigma, n_per_group)
        treatment = rng.normal(delta, sigma, n_per_group)
        t_stat, p_two = stats.ttest_ind(treatment, placebo, equal_var=False)
        p_one = p_two / 2 if t_stat > 0 else 1.0
        if p_one < alpha_adj:
            successes += 1

    return successes / n_sim


def theoretical_power(
    n_per_group: int = 120,
    sigma: float = config.SIGMA,
    delta: float = config.DELTA_SUPERIORITY,
    alpha: float = config.ALPHA,
    n_comp: int = config.N_COMPARISONS,
) -> float:
    """
    Analytical power for a one-sided two-sample comparison.
    """
    alpha_adj = alpha / n_comp
    z_alpha = stats.norm.ppf(1 - alpha_adj)
    ncp = (delta / sigma) * np.sqrt(n_per_group / 2)
    return 1 - stats.norm.cdf(z_alpha - ncp)
