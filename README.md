# Image Denoising with Probabilistic Models

This project implements and compares different probabilistic approaches for image denoising, developed as part of ISYE 6416 - Computational Statistics.

## Overview

The repository contains implementations of:
- **EPLL (Expected Patch Log Likelihood)**: Uses Gaussian Mixture Models (GMM) to learn patch priors
- **MRF (Markov Random Fields)**: Implements both Gibbs and Metropolis-Hastings-based denoising approaches

You can read the full report *[here](Report/EM%20-%20MRF%20Final%20Report.pdf)*

## Project Structure

```
.
├── data/
│   ├── Set12/          # Training and test images
│   └── BSDS300/        # Additional test dataset
├── model/
│   ├── EPLL/
│   │   ├── exploration.ipynb
│   │   └── learned_priors/
│   └── MRF/
│       └── MRF.ipynb
├── Report/             # Project Report
└── README.md
```

## Methods Implemented

### EPLL (Expected Patch Log Likelihood)
- Patch-based prior learning using GMM
- Half-Quadratic Splitting (HQS) optimization
- Auto-differentiation based optimization
- Supports multiple patch sizes and stride configurations

### MRF (Markov Random Fields)
- Iterative Conditional Modes (ICM)
- MCMC with Metropolis-Hastings sampling
- Energy-based formulation with smoothness and fidelity terms

## Usage

See individual notebooks in `model/EPLL/` and `model/MRF/` for detailed implementations and examples.
