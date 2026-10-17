"""
Project-wide configuration for the INHANCE trial simulation.

All numeric parameters used across the project are defined here,
so that changes propagate consistently.
"""

# ============================================================================
# Randomization
# ============================================================================
N_TOTAL = 840
N_GROUPS = 7
BLOCK_LENGTHS = (7, 14)
STRATA = ("Current smoker", "Ex-smoker")

GROUP_LABELS = (
    "Indacaterol75",
    "Indacaterol150",
    "Indacaterol300",
    "Indacaterol600",
    "Formoterol",
    "Tiotropium",
    "Placebo",
)

# ============================================================================
# Simulation
# ============================================================================
SEED = 1128
BALANCE_CORRECTION = 0.6      # strength of baseline balance correction

# Endpoint simulation
ENDPOINT_SD = 0.5             # standard deviation of endpoints (L)
RHO_ENDPOINT = 0.6            # correlation between two endpoints
RHO_COVARIATE = 0.3           # correlation between endpoint and baseline FEV1/FVC
COVARIATE_WEIGHT = 0.55       # weight of covariate shift

# Table 2 theoretical means (Day 15)
ENDPOINT_MEANS = {
    "trough": {
        "Indacaterol75":  1.46,
        "Indacaterol150": 1.49,
        "Indacaterol300": 1.53,
        "Indacaterol600": 1.505,
        "Formoterol":     1.423,
        "Tiotropium":     1.448,
        "Placebo":        1.31,
    },
    "auc": {
        "Indacaterol75":  1.51,
        "Indacaterol150": 1.54,
        "Indacaterol300": 1.59,
        "Indacaterol600": 1.54,
        "Formoterol":     1.53,
        "Tiotropium":     1.50,
        "Placebo":        1.31,
    },
}

# ============================================================================
# Dose selection
# ============================================================================
MCID = 0.12                   # minimal clinically important difference (L)
DOSE_ORDER = (
    "Indacaterol75",
    "Indacaterol150",
    "Indacaterol300",
    "Indacaterol600",
)

# ============================================================================
# Sample size / power (Question 4)
# ============================================================================
SIGMA = 270                   # mL, standard deviation of FEV1
DELTA_SUPERIORITY = 120       # mL, Indacaterol vs Placebo
DELTA_NONINFERIORITY = -55    # mL, non-inferiority margin
ALPHA = 0.05
POWER_TARGET = 0.85
N_COMPARISONS = 4             # Bonferroni correction divisor

# ============================================================================
# Reference drugs for Interim Analysis
# ============================================================================
REF_DRUG_TIO = "Tiotropium"
REF_DRUG_FOR = "Formoterol"
REF_DRUG_PBO = "Placebo"
