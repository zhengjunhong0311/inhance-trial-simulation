"""
Simulation functions for the INHANCE trial.

Question 2: baseline data simulation + merging with randomization.
Question 3: dual-endpoint simulation (binary normal, correlated with baseline).
"""

import numpy as np
import pandas as pd

from . import config


# ============================================================================
# Baseline simulation (Question 2)
# ============================================================================
def simulate_baseline(
    random_df: pd.DataFrame,
    seed: int = config.SEED,
    balance_correction: float = config.BALANCE_CORRECTION,
) -> pd.DataFrame:
    """
    Simulate baseline characteristics for all subjects, then apply a
    modest group-mean correction toward the overall mean to mimic the
    balance achieved by stratified randomization.

    Parameters
    ----------
    random_df : pd.DataFrame
        Randomization table from `stratified_block_randomization`.
    seed : int
        Random seed.
    balance_correction : float
        Strength of the group-mean correction (0 = no correction,
        1 = full correction). Default 0.6.

    Returns
    -------
    pd.DataFrame
        Baseline data with columns:
        ID, Age, Sex, Height, Weight, BMI, COPD_Duration, FEV1,
        FEV1_pred_pct, FVC, FEV1_FVC, SmokingHistory, ConcomitantICS.
    """
    rng = np.random.default_rng(seed)
    n = len(random_df)

    # Continuous variables
    age = rng.normal(64.5, 9.0, n).clip(40, 85)
    height = rng.normal(168.5, 9.4, n).clip(140, 200)
    weight = rng.normal(78.5, 18.8, n).clip(35, 160)
    bmi = weight / (height / 100) ** 2 + rng.normal(0, 0.5, n)
    copd_yrs = rng.gamma(shape=2.0, scale=3.5, size=n).clip(0.5, 40)
    fev1 = rng.normal(1.50, 0.49, n).clip(0.5, 3.5)
    fev1_pct = rng.normal(52.9, 13.2, n).clip(20, 90)
    fvc = rng.normal(2.86, 0.85, n).clip(1.2, 5.5)
    ratio = (fev1 / fvc) + rng.normal(0, 0.005, n)
    ratio = ratio.clip(0.2, 0.8)

    # Categorical variables
    sex = rng.binomial(1, 0.42, n)
    ics = rng.binomial(1, 0.39, n)
    smoke = random_df["SmokingStatus"].values

    df = pd.DataFrame({
        "ID": random_df["ParticipantID"].values,
        "Age": age, "Sex": sex, "Height": height, "Weight": weight,
        "BMI": bmi, "COPD_Duration": copd_yrs, "FEV1": fev1,
        "FEV1_pred_pct": fev1_pct, "FVC": fvc, "FEV1_FVC": ratio,
        "SmokingHistory": smoke, "ConcomitantICS": ics,
        "Group": random_df["GroupLabel"].values,
    })

    # Group-mean correction for continuous variables
    num_vars = ["Age", "Height", "Weight", "BMI", "COPD_Duration",
                "FEV1", "FEV1_pred_pct", "FVC", "FEV1_FVC"]
    target_mean = df[num_vars].mean()
    for v in num_vars:
        for g in df["Group"].unique():
            mask = df["Group"] == g
            group_mean = df.loc[mask, v].mean()
            shift = (target_mean[v] - group_mean) * balance_correction
            df.loc[mask, v] = df.loc[mask, v] + shift

    # Proportion correction for categorical variables
    for v in ["Sex", "ConcomitantICS"]:
        target_p = df[v].mean()
        for g in df["Group"].unique():
            mask = df["Group"] == g
            group_p = df.loc[mask, v].mean()
            n_flip = int(abs(group_p - target_p) * mask.sum() * 0.5)
            if n_flip > 0:
                if group_p > target_p:
                    ones = df.loc[mask & (df[v] == 1)].index
                    flip_idx = rng.choice(ones, min(n_flip, len(ones)), replace=False)
                    df.loc[flip_idx, v] = 0
                else:
                    zeros = df.loc[mask & (df[v] == 0)].index
                    flip_idx = rng.choice(zeros, min(n_flip, len(zeros)), replace=False)
                    df.loc[flip_idx, v] = 1

    return df.drop(columns=["Group"])


def merge_with_randomization(
    data1: pd.DataFrame,
    random_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge baseline data with the randomization table to form DATA2.

    Parameters
    ----------
    data1 : pd.DataFrame
        Baseline data.
    random_df : pd.DataFrame
        Randomization table.

    Returns
    -------
    pd.DataFrame
        Merged data with group information.
    """
    rand_cols = ["ParticipantID", "SmokingStatus", "BlockID",
                 "BlockLength", "WithinBlockSeq", "GroupCode", "GroupLabel"]
    data2 = data1.merge(
        random_df[rand_cols],
        left_on="ID", right_on="ParticipantID",
        how="inner",
    ).rename(columns={"GroupLabel": "Group"})

    assert (data2["SmokingStatus"] == data2["SmokingHistory"]).all(), \
        "Smoking status mismatch between baseline and randomization"
    return data2.drop(columns=["ParticipantID"])


# ============================================================================
# Dual-endpoint simulation (Question 3)
# ============================================================================
def simulate_endpoints(
    data2: pd.DataFrame,
    seed: int = config.SEED,
    sd: float = config.ENDPOINT_SD,
    rho_ep: float = config.RHO_ENDPOINT,
    rho_cov: float = config.RHO_COVARIATE,
    covariate_weight: float = config.COVARIATE_WEIGHT,
) -> pd.DataFrame:
    """
    Simulate Day-15 dual endpoints (trough FEV1 and FEV1 AUC1-4h).

    Two endpoints follow a bivariate normal distribution with correlation
    `rho_ep`. Both are correlated with baseline FEV1/FVC through a
    standardized covariate shift.

    Parameters
    ----------
    data2 : pd.DataFrame
        Merged baseline + randomization data.
    seed : int
        Random seed.
    sd : float
        Standard deviation of both endpoints.
    rho_ep : float
        Correlation between the two endpoints.
    rho_cov : float
        Correlation between endpoints and baseline FEV1/FVC.
    covariate_weight : float
        Weight controlling the magnitude of the covariate shift.

    Returns
    -------
    pd.DataFrame
        `data2` with two added columns: FEV1_Trough_D15 and FEV1_AUC_1_4h_D15.
    """
    rng = np.random.default_rng(seed)
    df = data2.copy()
    n = len(df)

    ratio_std = (df["FEV1_FVC"] - df["FEV1_FVC"].mean()) / df["FEV1_FVC"].std()

    trough = np.zeros(n)
    auc = np.zeros(n)

    means_trough = config.ENDPOINT_MEANS["trough"]
    means_auc = config.ENDPOINT_MEANS["auc"]

    for g in df["Group"].unique():
        idx = (df["Group"] == g).values
        ng = idx.sum()

        z1 = rng.normal(0, 1, ng)
        z2 = rng.normal(0, 1, ng)
        w1 = z1
        w2 = rho_ep * z1 + np.sqrt(1 - rho_ep ** 2) * z2

        cov_shift = rho_cov * ratio_std[idx].values

        trough[idx] = means_trough[g] + sd * w1 + covariate_weight * cov_shift
        auc[idx] = means_auc[g] + sd * w2 + covariate_weight * cov_shift

    df["FEV1_Trough_D15"] = trough
    df["FEV1_AUC_1_4h_D15"] = auc
    return df
