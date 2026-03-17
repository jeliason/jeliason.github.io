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

## Extraction

MAPLE provides two structured YAML schemas for extracting calibration data from papers.

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5em; margin: 1em 0;">
<div style="border-left: 3px solid #2563eb; padding-left: 1em;">
<strong style="color: #2563eb;">SubmodelTargets</strong> — in vitro and preclinical data with self-contained forward models (algebraic, dose-response, power law, ODE). Each target pairs extracted data with a forward model, bootstrap observation code, and a source relevance assessment.
</div>
<div style="border-left: 3px solid #dc2626; padding-left: 1em;">
<strong style="color: #dc2626;">CalibrationTargets</strong> — clinical and in vivo observables (tumor volumes, immune cell densities, treatment response rates) requiring full QSP model simulation. These capture the observable, experimental context, intervention scenarios, and Monte Carlo derivation code.
</div>
</div>

Both schemas are filled out **interactively using an MCP server with Claude Code**. The server exposes the extraction prompt, valid enum values, a multi-step workflow guide, and hard rules that LLMs commonly violate during extraction (e.g., inventing uncertainties, using wrong input types).

A `validate_target` tool runs three levels of checks:

- **Schema validation** — Pydantic model with 30+ validators
- **Prior derivation** — bootstrap + forward model inversion + distribution fitting + translation sigma
- **Snippet verification** — checks that every extracted value appears in the source paper text (Europe PMC full text or source PDFs), catching hallucinated numbers before they enter the pipeline

## Inference

All SubmodelTargets are combined into a **joint NumPyro model** for MCMC inference. A source relevance rubric scores each target across eight axes — species, indication, TME compatibility, measurement directness, and others — and maps these to a translation sigma that widens the likelihood for that target. Mouse in vitro data naturally contributes less than human clinical data constraining the same parameter.

The joint posterior is parameterized as **marginal distributions + a Gaussian copula** that preserves posterior correlations.

## Two-Stage Calibration

<div style="display: flex; align-items: center; gap: 1em; margin: 1.5em 0; font-size: 0.95em;">
<div style="flex: 1; background: #eff6ff; border-radius: 8px; padding: 1em; border: 1px solid #bfdbfe;">
<strong style="color: #2563eb;">Stage 1 — MAPLE</strong><br>
SubmodelTargets<br>
In vitro / preclinical data<br>
Joint MCMC (NumPyro/NUTS)<br>
<em>Output:</em> marginals + Gaussian copula
</div>
<div style="font-size: 1.5em; color: #64748b;">&rarr;</div>
<div style="flex: 1; background: #fef2f2; border-radius: 8px; padding: 1em; border: 1px solid #fecaca;">
<strong style="color: #dc2626;">Stage 2 — qsp-sbi</strong><br>
CalibrationTargets<br>
Clinical data + full QSP simulator<br>
Copula prior from Stage 1 + SBI (SNPE-C)<br>
<em>Output:</em> final posterior
</div>
</div>

## Links

- **Preprint:** [Structured Schemas for LLM-Modeler Collaboration in Quantitative Systems Pharmacology Model Calibration](https://www.biorxiv.org/content/10.64898/2026.03.05.709623v1) — bioRxiv, 2026
- [MAPLE repository](https://github.com/popellab/maple)
