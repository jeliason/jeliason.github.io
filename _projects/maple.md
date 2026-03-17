---
layout: post
title: "MAPLE: Model-Aware Parameterization from Literature Evidence"
description: "A pipeline for extracting QSP calibration data from scientific literature and producing informative priors via joint Bayesian inference."
tags:
  - quantitative systems pharmacology
  - Bayesian inference
  - prior elicitation
  - literature extraction
  - simulation-based inference
  - pancreatic cancer
  - LLM-assisted extraction
---

## Summary

QSP models have many biological parameters, and most can't be measured directly in the clinical context being modeled. The relevant data is usually scattered across papers, often from different species or indications. MAPLE provides a structured pipeline for turning those measurements into informative priors that account for the gap between the experimental and model contexts.

MAPLE provides two structured YAML schemas for extracting calibration data from papers, and an inference pipeline that turns those extractions into priors for downstream calibration.

## Two Extraction Schemas

**SubmodelTargets** are for in vitro and preclinical data where a self-contained forward model (algebraic formula, dose-response curve, power law, ODE) connects the literature measurement to model parameters. Each target includes the extracted data with provenance, the forward model, bootstrap-based observation code, and a source relevance assessment that quantifies the gap between the experimental and model contexts.

**CalibrationTargets** are for clinical and in vivo observables — tumor volumes, immune cell densities from biopsies, treatment response rates — where the measurement requires the full QSP model to simulate. These capture the observable definition, experimental context (species, indication, treatment history), intervention scenarios, and Monte Carlo code that derives calibration statistics from the extracted data.

Both schemas are filled out interactively using an MCP server with Claude Code. The server exposes the full extraction prompt, valid enum values, a multi-step workflow guide (model investigation, literature search, PDF collection, YAML writing, validation), and hard rules that LLMs commonly violate during extraction (e.g., inventing uncertainties, using wrong input types). A `validate_target` tool runs schema validation, prior derivation (bootstrap + forward model inversion + distribution fitting + translation sigma), and snippet verification — checking that every extracted value actually appears in the source paper text (via Europe PMC full text or source PDFs). This catches hallucinated numbers before they enter the pipeline.

## Submodel Prior Inference

All SubmodelTargets are combined into a joint NumPyro model for MCMC inference. A source relevance rubric scores each target across eight axes — species, indication, TME compatibility, measurement directness, and others — and maps these to a translation sigma that widens the likelihood for that target. Mouse in vitro data naturally contributes less than human clinical data constraining the same parameter. The joint posterior is parameterized as marginal distributions plus a Gaussian copula that preserves posterior correlations.

## Two-Stage Calibration

| Stage | MAPLE schema | Data | Method | Output |
|-------|-------------|------|--------|--------|
| 1 (MAPLE) | SubmodelTargets | In vitro / preclinical + self-contained forward models | Joint MCMC (NumPyro/NUTS) | Marginals + Gaussian copula |
| 2 (qsp-sbi) | CalibrationTargets | Clinical observables + full QSP simulator | SBI (SNPE-C) | Final posterior |

## Links

- **Preprint:** [Structured Schemas for LLM-Modeler Collaboration in Quantitative Systems Pharmacology Model Calibration](https://www.biorxiv.org/content/10.64898/2026.03.05.709623v1) — bioRxiv, 2026
- [MAPLE repository](https://github.com/popellab/maple)
