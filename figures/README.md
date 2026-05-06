# Figure generation

Python scripts for the synthetic / illustrative figures used on the project pages.
Each script reuses a public plotting function from `qsp-inference` and feeds it
fabricated inputs, so the images live in this repo and have no dependency on a
private project's data.

Outputs go to `../assets/images/`. Run from this directory:

```
python qsp_inference_dag.py                # parameter-target inference DAG
python qsp_inference_prior_posterior.py    # prior vs. posterior marginals
python qsp_inference_trajectory_ppc.py     # Stage 2 PPC trajectory bands
```

Requirements: `qsp-inference` (with `[audit]` extra for graphviz),
`matplotlib`, `numpy`, `pyyaml`, `scipy`.
