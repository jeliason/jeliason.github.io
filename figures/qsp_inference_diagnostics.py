"""Demo Stage 2 SBI diagnostics for the qsp-inference project page.

Generates a synthetic held-out test set and an NPE-like posterior, then
produces a single 4-panel summary figure covering the four core diagnostics
in the Stage 2 audit: recovery, posterior contraction, calibration ECDF,
and posterior predictive coverage.

Each panel is a one-axis summary across parameters / observables, not the
per-parameter grids produced by the public diagnostic plotters. Use the
upstream functions in ``qsp_inference.inference.diagnostics`` if you want
the full per-parameter breakdown.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "assets" / "images" / "qsp-inference-diagnostics.png"

PARAM_NAMES = [
    "k_PK_clearance", "V_d", "q_T_in", "k_T_prolif", "EC50_IFNg", "n_Hill",
]
n_params = len(PARAM_NAMES)
n_test = 200
n_post = 1000

rng = np.random.default_rng(11)

prior_sd = np.array([0.8, 0.6, 1.2, 0.7, 1.0, 0.4])
theta_test = rng.normal(0.0, prior_sd[None, :], size=(n_test, n_params))

post_sd_factor = np.array([0.65, 0.80, 0.95, 1.00, 0.75, 0.90])
bias = np.array([0.10, 0.20, -0.25, 0.15, -0.18, 0.08])
cal_noise = np.array([0.55, 0.70, 0.95, 1.00, 0.65, 0.80])

post_sd = post_sd_factor * prior_sd
post_means = theta_test + bias[None, :] + rng.normal(0, cal_noise[None, :], size=(n_test, n_params))
samples = post_means[None, :, :] + rng.normal(0, post_sd[None, None, :], size=(n_post, n_test, n_params))
prior_var = prior_sd ** 2

# ---- per-parameter summaries -----------------------------------------------
median_post = np.median(samples, axis=0)             # (n_test, n_params)
var_post = np.var(samples, axis=0)                   # (n_test, n_params)
contraction = 1.0 - var_post / prior_var[None, :]    # (n_test, n_params)
mean_contraction = contraction.mean(axis=0)          # (n_params,)

# Calibration ranks
ranks = np.zeros((n_test, n_params))
for i in range(n_test):
    for j in range(n_params):
        ranks[i, j] = (samples[:, i, j] <= theta_test[i, j]).mean()

# ---- PPC coverage data -----------------------------------------------------
obs_specs = [
    ("Tumor volume @ wk 6 (cm³)", np.log(45),  0.55, np.log(110)),
    ("CD8+ density (cells/mm²)",  np.log(120), 0.50, np.log(95)),
    ("Treg / CD8 ratio",          np.log(0.4), 0.40, np.log(0.95)),
    ("IFN-γ AUC (ng·day/mL)",     np.log(8.0), 0.55, np.log(7.2)),
]
n_sims = 1500
log_x_pp = np.zeros((n_sims, len(obs_specs)))
log_obs = np.zeros(len(obs_specs))
obs_names = [s[0] for s in obs_specs]
for i, (_, mu, sd, mu_obs) in enumerate(obs_specs):
    log_x_pp[:, i] = rng.normal(mu, sd, size=n_sims)
    log_obs[i] = mu_obs

pp_q05 = np.percentile(log_x_pp, 5, axis=0)
pp_q50 = np.percentile(log_x_pp, 50, axis=0)
pp_q95 = np.percentile(log_x_pp, 95, axis=0)


# ---- 4-panel figure --------------------------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(18, 4.6))
PALETTE = plt.cm.tab10.colors

# Panel 1: Recovery — true vs. posterior median, all parameters overlaid
ax = axes[0]
all_lo, all_hi = [], []
for j in range(n_params):
    ax.scatter(theta_test[:, j], median_post[:, j],
               s=10, alpha=0.45, color=PALETTE[j % 10], label=PARAM_NAMES[j])
    all_lo.append(min(theta_test[:, j].min(), median_post[:, j].min()))
    all_hi.append(max(theta_test[:, j].max(), median_post[:, j].max()))
lo, hi = min(all_lo), max(all_hi)
ax.plot([lo, hi], [lo, hi], "k--", lw=1)
ax.set_xlabel("True (log-space)", fontsize=11)
ax.set_ylabel("Posterior median", fontsize=11)
ax.set_title("Recovery", fontsize=13, fontweight="bold")
ax.legend(fontsize=7, loc="best", ncol=2, frameon=False)
ax.grid(alpha=0.3)

# Panel 2: Posterior contraction per parameter
ax = axes[1]
ax.barh(range(n_params), mean_contraction,
        color=[PALETTE[j % 10] for j in range(n_params)])
ax.set_yticks(range(n_params))
ax.set_yticklabels(PARAM_NAMES, fontsize=9)
ax.set_xlim(0, 1)
ax.axvline(0, color="k", lw=0.6)
ax.set_xlabel(r"$1 - \mathrm{var}_\mathrm{post}/\mathrm{var}_\mathrm{prior}$", fontsize=11)
ax.set_title("Posterior contraction", fontsize=13, fontweight="bold")
ax.invert_yaxis()
ax.grid(axis="x", alpha=0.3)

# Panel 3: Calibration ECDF (difference from uniform), one curve per parameter
ax = axes[2]
ks_band = 1.36 / np.sqrt(n_test)
ax.fill_between([0, 1], -ks_band, ks_band, color="gray", alpha=0.25, label="KS 95%")
for j in range(n_params):
    sorted_r = np.sort(ranks[:, j])
    ecdf = np.arange(1, n_test + 1) / n_test
    ax.plot(sorted_r, ecdf - sorted_r, color=PALETTE[j % 10], lw=1.2,
            alpha=0.9, label=PARAM_NAMES[j])
ax.axhline(0, color="k", lw=0.6, ls="--")
ax.set_xlim(0, 1)
ax.set_xlabel("Rank quantile", fontsize=11)
ax.set_ylabel("ECDF − uniform", fontsize=11)
ax.set_title("Calibration ECDF", fontsize=13, fontweight="bold")
ax.grid(alpha=0.3)

# Panel 4: PPC coverage — 5–95% band per observable with observed value marked
ax = axes[3]
y = np.arange(len(obs_names))
for i in y:
    ax.plot([pp_q05[i], pp_q95[i]], [i, i], color="steelblue", lw=4, alpha=0.5)
    ax.plot(pp_q50[i], i, "o", color="steelblue", markersize=6)
    ax.plot(log_obs[i], i, "X", color="crimson", markersize=10,
            label="Observed" if i == 0 else None)
ax.set_yticks(y)
ax.set_yticklabels(obs_names, fontsize=9)
ax.set_xlabel("Predictive value (log-space)", fontsize=11)
ax.set_title("PPC coverage", fontsize=13, fontweight="bold")
ax.legend(fontsize=8, loc="lower right", frameon=False)
ax.invert_yaxis()
ax.grid(axis="x", alpha=0.3)

plt.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"wrote {OUT}")
