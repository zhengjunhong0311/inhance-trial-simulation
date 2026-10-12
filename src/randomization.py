"""
Stratified block randomization for the INHANCE trial.

Question 1: stratified by smoking status, variable block length (7 or 14),
1:1:1:1:1:1:1 allocation across 7 treatment groups.
"""

import numpy as np
import pandas as pd

from . import config


def stratified_block_randomization(
    n_total: int = config.N_TOTAL,
    n_groups: int = config.N_GROUPS,
    block_lengths: tuple = config.BLOCK_LENGTHS,
    strata: tuple = config.STRATA,
    group_labels: tuple = config.GROUP_LABELS,
    seed: int = config.SEED,
) -> pd.DataFrame:
    """
    Perform stratified block randomization.

    Within each stratum, subjects are allocated using variable-length blocks.
    Block lengths must be multiples of `n_groups` to keep groups balanced
    within each block.

    Parameters
    ----------
    n_total : int
        Total number of subjects.
    n_groups : int
        Number of treatment arms.
    block_lengths : tuple of int
        Candidate block lengths (must be multiples of n_groups).
    strata : tuple of str
        Stratification levels.
    group_labels : tuple of str
        Treatment arm labels.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Randomization table with columns:
        ParticipantID, SmokingStatus, BlockID, BlockLength,
        WithinBlockSeq, GroupCode, GroupLabel.

    References
    ----------
    ICH E9(R1): Addendum on Estimands and Sensitivity Analysis.
    药物临床试验适应性设计指导原则（试行）.
    """
    rng = np.random.default_rng(seed)
    n_per_stratum = n_total // len(strata)

    records = []
    pid = 1

    for stratum in strata:
        # Build block-length sequence for this stratum
        blocks = []
        remaining = n_per_stratum
        while remaining > 0:
            bl = rng.choice(block_lengths)
            if bl > remaining:
                bl = remaining
            blocks.append(bl)
            remaining -= bl

        assert sum(blocks) == n_per_stratum, "Block sum must equal stratum size"

        block_id = 1
        for bl in blocks:
            assert bl % n_groups == 0, \
                f"Block length {bl} must be a multiple of {n_groups}"

            reps = bl // n_groups
            group_seq = np.repeat(np.arange(1, n_groups + 1), reps)
            rng.shuffle(group_seq)

            for i, g in enumerate(group_seq, start=1):
                records.append({
                    "ParticipantID": f"P{pid:04d}",
                    "SmokingStatus": stratum,
                    "BlockID": f"{'Cur' if stratum == 'Current smoker' else 'Ex'}_{block_id:03d}",
                    "BlockLength": bl,
                    "WithinBlockSeq": i,
                    "GroupCode": g,
                    "GroupLabel": group_labels[g - 1],
                })
                pid += 1
            block_id += 1

    return pd.DataFrame(records)
