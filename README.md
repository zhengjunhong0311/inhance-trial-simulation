# INHANCE: Adaptive Seamless Trial Simulation

Python replication of the INHANCE Phase II/III adaptive seamless dose-selection trial in COPD.

## Project Structure

inhance-adaptive-trial/
├── notebooks/          # Analysis notebooks
├── outputs/
│   ├── figures/        # Plots
│   └── tables/         # Data tables
├── src/                # Reusable Python modules
└── docs/               # Documentation

## Methods

- Stratified block randomization (smoking status; block length 7/14)
- ANCOVA with baseline FEV1/FVC and smoking status
- LS Mean difference vs Placebo with 95% CI
- 8-rule dose selection algorithm

## References

- Donohue JF, et al. Am J Respir Crit Care Med. 2010;182(2):155-62.

## License

MIT