"""
Dose selection rules and visualization for the INHANCE trial.

Question 3: implement the 8 predefined dose selection rules and
produce the dose selection plot.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from . import config


# ============================================================================
# 8-rule dose selection
# ============================================================================
def select_doses(
    trough_res: pd.DataFrame,
    auc_res: pd.DataFrame,
    X: float,
    Y: float,
    dose_order: tuple = config.DOSE_ORDER,
) -> tuple:
    """
    Apply the 8 predefined dose selection rules.

    Returns
    -------
    tuple
        (chosen_low, chosen_high, rule_id, reason)
    """
    doses = list(dose_order)

    meet_X = {d: trough_res.loc[d, "LS_Mean_Diff"] >= X for d in doses}
    meet_Y = {d: auc_res.loc[d, "LS_Mean_Diff"] >= Y for d in doses}

    meet_X_list = [d for d in doses if meet_X[d]]
    meet_Y_list = [d for d in doses if meet_Y[d]]
    meet_both = [d for d in doses if meet_X[d] and meet_Y[d]]

    def next_higher(d):
        i = doses.index(d)
        return doses[min(i + 1, len(doses) - 1)]

    # Rule 1
    if len(meet_both) > 1:
        return meet_both[0], next_higher(meet_both[0]), "1", \
            f"Multiple doses meet both; select lowest ({meet_both[0]}) + next higher"
    # Rule 2
    if len(meet_both) == 1:
        return meet_both[0], next_higher(meet_both[0]), "2", \
            f"Only {meet_both[0]} meets both"
    # Rule 3
    if len(meet_X_list) > 1 and len(meet_Y_list) == 0:
        closest = max(meet_X_list, key=lambda d: auc_res.loc[d, "LS_Mean_Diff"])
        return closest, next_higher(closest), "3", \
            f"Multiple meet X, none meet Y; pick {closest} closest to Y"
    # Rule 4
    if len(meet_X_list) == 1 and len(meet_Y_list) == 0:
        return meet_X_list[0], next_higher(meet_X_list[0]), "4", \
            f"Only {meet_X_list[0]} meets X, none meet Y"
    # Rule 5
    if len(meet_Y_list) > 1 and len(meet_X_list) == 0:
        closest = max(meet_Y_list, key=lambda d: trough_res.loc[d, "LS_Mean_Diff"])
        return closest, next_higher(closest), "5", \
            f"Multiple meet Y, none meet X; pick {closest} closest to X"
    # Rule 6
    if len(meet_Y_list) == 1 and len(meet_X_list) == 0:
        return meet_Y_list[0], next_higher(meet_Y_list[0]), "6", \
            f"Only {meet_Y_list[0]} meets Y, none meet X"
    # Rule 7
    if len(meet_X_list) == 1 and len(meet_Y_list) == 1:
        return meet_X_list[0], next_higher(meet_X_list[0]), "7", \
            "One meets X and one meets Y (distinct)"
    # Rule 8
    closest = max(doses, key=lambda d: trough_res.loc[d, "LS_Mean_Diff"])
    return closest, next_higher(closest), "8", \
        f"None meet threshold; pick {closest} closest to X"


# ============================================================================
# Dose selection plot
# ============================================================================
def plot_dose_selection(
    trough_res: pd.DataFrame,
    auc_res: pd.DataFrame,
    X: float,
    Y: float,
    chosen_low: str,
    chosen_high: str,
    savepath: str,
    dose_order: tuple = config.DOSE_ORDER,
) -> None:
    """
    Plot the interim dose selection decision figure.
    """
    # Set Chinese font
    plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    doses = list(dose_order)
    x = np.arange(len(doses))
    short = [d.replace("Indacaterol", "") for d in doses]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

    for ax, res, thr, title, ylab in [
        (axes[0], trough_res, X, "第15天谷水平 FEV1", "LS Mean Diff (L)"),
        (axes[1], auc_res, Y, "第15天 FEV1 AUC1-4h", "LS Mean Diff (L)"),
    ]:
        means = res.loc[doses, "LS_Mean_Diff"].values
        errs = np.vstack([
            means - res.loc[doses, "CI_Lower"].values,
            res.loc[doses, "CI_Upper"].values - means,
        ])
        colors = ["#d62728" if d in (chosen_low, chosen_high) else "#1f77b4"
                  for d in doses]

        ax.errorbar(x, means, yerr=errs, fmt="o", capsize=6,
                    markersize=10, color="black", ecolor="gray", zorder=2)
        for xi, m, c in zip(x, means, colors):
            ax.scatter(xi, m, s=180, color=c, zorder=3)

        ax.axhline(thr, color="red", ls="--", lw=1.5,
                   label=f"阈值 = {thr:.3f}")
        ax.axhline(0, color="gray", ls=":", lw=1)
        ax.set_xticks(x)
        ax.set_xticklabels(short)
        ax.set_xlabel("Indacaterol 剂量 (μg)")
        ax.set_ylabel(ylab)
        ax.set_title(title)
        ax.legend(loc="lower right")
        ax.grid(alpha=0.3)

    plt.suptitle(f"期中剂量选择：选中 {chosen_low} 与 {chosen_high}",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(savepath, dpi=150, bbox_inches="tight")
    plt.show()
