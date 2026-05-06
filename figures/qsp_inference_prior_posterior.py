"""Demo prior vs. posterior marginal plot for the qsp-inference project page.

Calls qsp_inference.audit.plots._plot_one_marginal per panel so the panels
match the real audit's rendering, but builds the figure ourselves so we can
size the text up and drop the suptitle.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

from qsp_inference.audit.plots import _plot_one_marginal

OUT = Path(__file__).resolve().parent.parent / "assets" / "images" / "qsp-inference-prior-vs-posterior.png"

PARAMS = {
    "k_PK_clearance":   {"mu": np.log(0.5),  "prior_sigma": 0.8, "post_mu": np.log(0.55), "post_sigma": 0.18},
    "V_d":              {"mu": np.log(3.0),  "prior_sigma": 0.6, "post_mu": np.log(3.4),  "post_sigma": 0.20},
    "q_T_in":           {"mu": np.log(1e-3), "prior_sigma": 1.2, "post_mu": np.log(1.4e-3), "post_sigma": 0.55},
    "k_T_prolif":       {"mu": np.log(0.2),  "prior_sigma": 0.7, "post_mu": np.log(0.21), "post_sigma": 0.65},
    "EC50_IFNg":        {"mu": np.log(2.0),  "prior_sigma": 1.0, "post_mu": np.log(1.6),  "post_sigma": 0.30},
    "n_Hill":           {"mu": np.log(2.0),  "prior_sigma": 0.4, "post_mu": np.log(2.05), "post_sigma": 0.38},
}

rng = np.random.default_rng(7)
priors = {}
params_data = {}
joint_samples = {}
for name, p in PARAMS.items():
    priors[name] = {"mu": p["mu"], "sigma": p["prior_sigma"]}
    samps = np.exp(rng.normal(p["post_mu"], p["post_sigma"], size=4000))
    joint_samples[name] = samps
    params_data[name] = {"joint": {
        "median": float(np.median(samps)),
        "sigma":  float(np.std(np.log(samps))),
    }}

names = list(PARAMS)
ncols = 3
nrows = (len(names) + ncols - 1) // ncols

fig, axes = plt.subplots(
    nrows, ncols,
    figsize=(4.4 * ncols, 2.8 * nrows),
    constrained_layout=True,
)
axes = np.atleast_2d(axes).flatten()

for ax, name in zip(axes, names):
    _plot_one_marginal(ax, name, priors, params_data, joint_samples)
    ax.set_title(name, fontsize=14, fontweight="bold")
    ax.tick_params(axis="x", labelsize=11)

for ax in axes[len(names):]:
    ax.set_visible(False)

# Single shared legend across the figure
fig.legend(
    handles=[
        Patch(facecolor="#cc4444", alpha=0.30, label="Prior"),
        Patch(facecolor="#2266aa", alpha=0.30, label="Posterior"),
    ],
    loc="upper center",
    ncol=2,
    fontsize=12,
    frameon=False,
    bbox_to_anchor=(0.5, 1.06),
)

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=160, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote {OUT}")
