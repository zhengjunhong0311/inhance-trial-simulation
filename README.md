# INHANCE: Adaptive Seamless Trial Simulation

Python replication of the INHANCE Phase II/III adaptive seamless dose-selection trial in COPD.

## Overview

This project reproduces the statistical workflow of the INHANCE trial — a real Phase II/III adaptive seamless design used to select doses of indacaterol for COPD treatment. The implementation covers:

- Stratified block randomization
- Baseline simulation and balance assessment
- Interim analysis with ANCOVA and dose selection

## Project Structure

    inhance-trial-simulation/
    ├── notebooks/
    │   └── 01-randomization.ipynb
    ├── dose_selection.png
    ├── README.md
    ├── requirements.txt
    └── .gitignore

## Methods

### Randomization

- Stratified by smoking status (current smoker / ex-smoker)
- Variable block length (7 or 14)
- 1:1:1:1:1:1:1 allocation across 7 treatment groups
- Total sample size: 840 subjects, 120 per group

### Baseline Simulation

- Parametric simulation based on published Table 1 characteristics
- Variables: age, sex, height, weight, BMI, COPD duration, FEV1, FVC
- Baseline balance assessed by ANOVA, chi-square, and standardized mean difference (SMD)

### Interim Analysis

- ANCOVA with baseline FEV1/FVC and smoking status as covariates
- LS Mean difference vs placebo with 95% CI
- Automated dose selection using predefined threshold rules
- Rule 1 triggered: selected Indacaterol 75 ug and 150 ug

## Quick Start

    git clone https://github.com/zhengjunhong0311/inhance-trial-simulation.git
    cd inhance-trial-simulation
    pip install -r requirements.txt
    jupyter lab notebooks/

All results are reproducible with fixed random seed (1128).

## References

- Donohue JF, et al. Once-daily bronchodilators for chronic obstructive pulmonary disease: indacaterol versus tiotropium. Am J Respir Crit Care Med. 2010;182(2):155-62.
- Barnes PJ, et al. Integrating indacaterol dose selection in a clinical study in COPD using an adaptive seamless design. Stat Methods Med Res. 2010;23(3):165-71.

## License

MIT
