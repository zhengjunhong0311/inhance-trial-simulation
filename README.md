# INHANCE: Adaptive Seamless Trial Simulation

Python replication of the INHANCE Phase II/III adaptive seamless dose-selection trial in COPD.

## Overview

This project reproduces the complete statistical workflow of the INHANCE trial — a real Phase II/III adaptive seamless design used to select doses of indacaterol for COPD treatment. The implementation covers:

- Stratified block randomization and baseline simulation
- Interim analysis with ANCOVA and automated dose selection
- Sample size and power estimation
- **Seamless inference and multiplicity control (FWER simulation)**

## Project Structure

   inhance-trial-simulation/
├── src/                        # Reusable Python modules
│   ├── config.py               # Global parameters & reference drugs
│   ├── randomization.py        # Stratified block randomization
│   ├── simulate.py             # Baseline and endpoint simulations
│   ├── analysis.py             # ANCOVA and threshold computation
│   ├── dose_selection.py       # 8-rule dose selection logic
│   └── sample_size.py          # Sample size and power functions
├── tests/                      # Unit tests (pytest)
│   └── test_randomization.py
├── notebooks/                  # (Optional: move your .ipynb here later)
├── 01_randomization.ipynb
├── 02_endpoints.ipynb
├── 03_interim_analysis.ipynb
├── 04_sample_size.ipynb
├── 05_seamless_inference.ipynb # FWER simulation
├── 06_final_oc_and_fwer.ipynb  # Advanced 10k OC simulation
├── dose_selection.png
├── fwer_simulation.png
├── requirements.txt
├── LICENSE
└── .gitignore

## Key Figure

![Interim dose selection](dose_selection.png)

*Interim dose selection based on ANCOVA-adjusted LS Mean differences. Red dots indicate selected doses; the dashed red line marks the selection threshold.*

## Methods

### 1. Randomization & Baseline
- Stratified block randomization (smoking status; block length 7 or 14).
- Parametric baseline simulation with group-mean correction.
- Balance assessment via ANOVA, chi-square, and SMD.

### 2. Interim Analysis
- ANCOVA with baseline FEV1/FVC and smoking status as covariates.
- LS Mean difference vs Placebo with 95% CI.
- Automated 8-rule dose selection algorithm.

### 3. Seamless Inference & Multiplicity Control

To demonstrate the necessity of multiplicity adjustment in adaptive seamless designs, we simulated 10,000 trials under the null hypothesis (involving 2 endpoints × 2 selected doses = 4 comparisons). 

As shown in the figure below:
- **Naive Pooling** (directly merging stages without adjustment) causes the Family-Wise Error Rate (FWER) to inflate severely to **19.70%**.
- **Bonferroni correction** (α/4 = 0.0125) successfully controls the FWER but is overly conservative.
- **Fisher's Combination Test** (combining stage-wise p-values) also controls the error rate near the nominal 5% level while theoretically retaining higher statistical power by utilizing both stages' information.

![FWER Simulation](fwer_simulation_advanced.png)

*Note: Error bars represent the 95% Monte Carlo confidence intervals based on 10,000 simulations.*

## Quick Start

    git clone https://github.com/zhengjunhong0311/inhance-trial-simulation.git
    cd inhance-trial-simulation
    pip install -r requirements.txt
    jupyter lab notebooks/

All results are reproducible with fixed random seed (1128).

## References

- Donohue JF, et al. Once-daily bronchodilators for chronic obstructive pulmonary disease: indacaterol versus tiotropium. *Am J Respir Crit Care Med*. 2010;182(2):155-62.
- Barnes PJ, et al. Integrating indacaterol dose selection in a clinical study in COPD using an adaptive seamless design. *Stat Methods Med Res*. 2010;23(3):165-71.

## License

MIT
