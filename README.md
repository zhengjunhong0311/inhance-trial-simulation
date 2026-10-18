# INHANCE: Adaptive Seamless Trial Simulation

Python replication of the INHANCE Phase II/III adaptive seamless dose-selection trial in COPD.

## Overview

This project reproduces the complete statistical workflow of the INHANCE trial — a real Phase II/III adaptive seamless design used to select doses of indacaterol for COPD treatment. The implementation covers:

- Stratified block randomization and baseline simulation
- Interim analysis with ANCOVA and automated dose selection
- Sample size and power estimation
- **Seamless inference and multiplicity control (FWER simulation)**
- **Operating Characteristics (OC) simulation under realistic dose-response**

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
    ├── 01_randomization.ipynb
    ├── 02_endpoints.ipynb
    ├── 03_interim_analysis.ipynb
    ├── 04_sample_size.ipynb
    ├── 05_seamless_inference.ipynb # FWER simulation
    ├── 06_final_oc_and_fwer.ipynb  # Advanced 10k OC simulation
    ├── dose_selection.png
    ├── fwer_simulation.png
    ├── fwer_simulation_advanced.png
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

### 3. Operating Characteristics (FWER & Power Simulation)

To rigorously evaluate the operating characteristics of the adaptive seamless design, we conducted a **10,000-run Monte Carlo simulation** (incorporating a bivariate normal distribution with ρ=0.6 between endpoints to reflect realistic test correlations).

**Under H0 (Type I Error Control):**
- **Naive Pooling** inflates the FWER severely to **18.90%**.
- **Bonferroni** strictly controls the FWER at **5.51%**.
- **Fisher Combination** also controls the FWER near the nominal level at **5.92%**.

**Under H1 (Statistical Power):**
With realistic dose-response effects (50-140 mL) and an adjusted significance level (α/4 = 0.0125), **Naive Pooling** achieves the highest power (83.59%) but is invalid due to FWER inflation. **Bonferroni** retains 60.91% power, while **Fisher Combination** yields 57.98% power.

**Methodological Insight (Winner's Curse & Over-conservativeness):**
The simulation reveals two critical statistical realities:
1. **Winner's Curse:** Bonferroni and Fisher slightly exceed 5% under H0 because selecting the top doses at interim induces selection bias.
2. **Fisher's Conservativeness:** In a multi-endpoint setting with a strict α/4, the unweighted Fisher combination can be overly conservative, resulting in lower power than naive Bonferroni. This highlights why modern seamless designs require sophisticated approaches like **weighted combination tests (e.g., Cui-Hung-Wang)** or **closed testing procedures** to maintain power while strictly controlling FWER.

![FWER and Power Simulation](final_fwer_and_power.png)

### 4. Operating Characteristics (OC) Simulation

To evaluate the operating characteristics under a realistic dose-response relationship (effects of 50, 80, 110, and 140 mL for the four doses), we simulated 500 seamless trials. 

- **Correct Selection Rate at Interim:** 83.6% (reflects the uncertainty of selecting the true maximum dose due to sampling noise at N=120/group).
- **Overall Power (Success Rate):** 96.8% (with Bonferroni adjustment α/4 = 0.0125).

*Note: The analytical sample size calculation (N=518/group) does not account for the variance reduction from ANCOVA baseline adjustment. In practice, adjusting for FEV1/FVC yields a variance deflation factor, potentially reducing the required sample size. This simulation evaluates operating characteristics based on the unadjusted SD (270 mL) for a conservative estimation.*

## Quick Start

    git clone https://github.com/zhengjunhong0311/inhance-trial-simulation.git
    cd inhance-trial-simulation
    pip install -r requirements.txt
    jupyter lab

All results are reproducible with fixed random seed (1128).

## References

- Donohue JF, et al. Once-daily bronchodilators for chronic obstructive pulmonary disease: indacaterol versus tiotropium. *Am J Respir Crit Care Med*. 2010;182(2):155-62.
- Barnes PJ, et al. Integrating indacaterol dose selection in a clinical study in COPD using an adaptive seamless design. *Stat Methods Med Res*. 2010;23(3):165-71.

## License

MIT
