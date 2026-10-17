"""
Statistical analysis functions for the INHANCE trial.

Question 3: ANCOVA with LS Mean estimation and threshold computation.
"""

import pandas as pd
import statsmodels.formula.api as smf

from . import config


# ============================================================================
# ANCOVA + LS Mean
# ============================================================================
def get_lsmean_diff(
    data: pd.DataFrame,
    endpoint: str,
    ref: str = config.REF_DRUG_PBO,  # <-- 改这里
) -> pd.DataFrame:
    """
    Fit ANCOVA and extract LS Mean difference vs reference group.

    Model: endpoint ~ C(Group, Treatment(ref)) + FEV1_FVC + C(SmokingHistory)

    Parameters
    ----------
    data : pd.DataFrame
        Input data with columns: Group, FEV1_FVC, SmokingHistory, and
        the endpoint of interest.
    endpoint : str
        Name of the endpoint column.
    ref : str
        Reference group (default "Placebo").

    Returns
    -------
    pd.DataFrame
        Indexed by Group, with columns:
        LS_Mean_Diff, CI_Lower, CI_Upper, p_value.
    """
    formula = (
        f"{endpoint} ~ C(Group, Treatment('{ref}')) "
        f"+ FEV1_FVC + C(SmokingHistory)"
    )
    model = smf.ols(formula, data=data).fit()

    results = []
    for g in data["Group"].unique():
        if g == ref:
            continue
        coef = f"C(Group, Treatment('{ref}'))[T.{g}]"
        if coef not in model.params.index:
            continue
        results.append({
            "Group": g,
            "LS_Mean_Diff": model.params[coef],
            "CI_Lower": model.conf_int().loc[coef, 0],
            "CI_Upper": model.conf_int().loc[coef, 1],
            "p_value": model.pvalues[coef],
        })

    return pd.DataFrame(results).set_index("Group")


# ============================================================================
# Threshold computation
# ============================================================================
def compute_thresholds(
    trough_res: pd.DataFrame,
    auc_res: pd.DataFrame,
    mcid: float = config.MCID,
) -> tuple:
    """
    Compute threshold X (trough) and Y (AUC).

    Threshold X = max(Tio vs Pbo, For vs Pbo, MCID)
    Threshold Y = max(Tio vs Pbo, For vs Pbo)

    Parameters
    ----------
    trough_res : pd.DataFrame
        LS Mean results for trough FEV1.
    auc_res : pd.DataFrame
        LS Mean results for FEV1 AUC1-4h.
    mcid : float
        Minimal clinically important difference.

    Returns
    -------
    tuple
        (X, Y, X_candidates, Y_candidates)
    """
       X_candidates = [
        trough_res.loc["Tiotropium", "LS_Mean_Diff"],
        trough_res.loc["Formoterol", "LS_Mean_Diff"],
        mcid,
    ]
    Y_candidates = [
        auc_res.loc["Tiotropium", "LS_Mean_Diff"],
        auc_res.loc["Formoterol", "LS_Mean_Diff"],
    ]
    return max(X_candidates), max(Y_candidates), X_candidates, Y_candidates
