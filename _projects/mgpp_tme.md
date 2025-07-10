---
layout: post
title: "Joint Modeling of Tumor–Immune Spatial Interactions"
description: "A statistically grounded approach to modeling tumor–immune spatial interactions using joint species distribution models on imaging mass cytometry data."
tags:
  - tumor microenvironment
  - spatial point processes
  - Gibbs models
  - joint species distribution models
  - spatial omics
  - imaging mass cytometry
  - ecological modeling
  - colorectal cancer
  - cell–cell interactions
---

## Summary

We present a statistical framework for modeling cell–cell spatial interactions in the tumor microenvironment (TME) using multitype Gibbs point process (MGPP) models as joint species distribution models (JSDMs). Applied to imaging mass cytometry data from 35 colorectal cancer patients, our approach captures spatial dependencies among 16 cell types, adjusts for microenvironmental covariates, and reveals prognostic tumor–immune and stromal–immune relationships. Granulocyte interactions emerged as strong survival predictors, with spatial patterns varying across immune subtypes.

## What Can MGPP Models Answer?

MGPP models let us formally address key questions about spatial structure and function in the TME:

| General Question                                                                                     | Specific to the TME                                                                                             |
|------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Are cell types *positively* or *negatively* correlated in space, adjusting for other cells and covariates? | Are B cells and granulocytes positively or negatively correlated in this patient, after controlling for others? |
| How do cell type interactions vary across spatial scales?                                            | At which scales are Tregs repulsive or attractive toward each other?                                            |
| Can estimated interaction parameters predict clinical outcomes?                                      | How well does the interaction between CD8+ T cells and granulocytes predict patient survival?                   |
| Can we predict the distribution of an unmeasured cell type from others and spatial context?          | Can we infer M2 macrophage locations in images where they weren’t directly measured?                            |

## Links

- **Paper:** [Investigating Ecological Interactions in the Tumor Microenvironment Using Joint Species Distribution Models for Point Patterns](https://doi.org/10.51387/24-NEJSDS66)
- [Code](https://github.com/jeliason/mgpp_TME)  
- [Vignette](https://htmlpreview.github.io/?https://raw.githubusercontent.com/jeliason/mgpp_TME/main/mgpp_example_workflow.html)

## Key Advantages

- Adjusts for spatial and patient-level covariates  
- Models joint interactions between multiple cell types  
- Provides uncertainty estimates for interaction effects  
- Enables prediction and residual-based model assessment
