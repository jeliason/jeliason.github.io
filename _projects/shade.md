---
layout: post
title: "SHADE: Modeling Asymmetric Spatial Interactions in Tumor Microenvironments"
description: "A multilevel Bayesian framework for quantifying direction-specific cell-cell associations in hierarchically-structured spatial tissue data."
tags:
  - tumor microenvironment
  - spatial point processes
  - multilevel modeling
  - Bayesian modeling
  - spatial omics
  - imaging mass cytometry
  - ecological modeling
  - colorectal cancer
  - cell–cell interactions
  - asymmetric interactions
---

## Summary

Understanding spatial interactions between cell types is essential for interpreting immune function, tumor progression, and tissue organization. While conventional spatial statistics often assume symmetric interactions and analyze images independently, biological systems like the tumor microenvironment frequently exhibit asymmetric, hierarchically structured spatial patterns. We introduce SHADE (Spatial Hierarchical Asymmetry via Directional Estimation), a Bayesian modeling framework that captures direction-specific cell-cell associations across multiple spatial scales using smooth interaction curves and multilevel inference.

## Workflow

![SHADE workflow](/assets/images/shade_summary_figure.png)

The workflow begins with hierarchically structured image data (cohorts → patients → images), which are processed into annotated spatial point patterns. SHADE then estimates Spatial Interaction Curves (SICs) to capture direction-specific cell-cell associations at multiple biological levels, allowing for analysis of spatial heterogeneity and uncertainty. These estimates can be compared across cohorts to identify differences in spatial organization.

## Links

- **Preprint:** [SHADE: A Multilevel Bayesian Framework for Modeling Directional Spatial Interactions in Tissue Microenvironments](https://doi.org/10.1101/2025.06.24.661393)
- [Code](https://github.com/jeliason/SHADE)  
- [Vignette](https://htmlpreview.github.io/?https://raw.githubusercontent.com/jeliason/SHADE/main/vignettes/Introduction.html)
