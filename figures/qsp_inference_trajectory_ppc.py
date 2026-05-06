"""Demo posterior-predictive trajectory plot for the qsp-inference project page.

Reuses ``qsp_inference.inference.posterior_predictive.plot_posterior_predictive_spaghetti``
with synthetic trajectories that mimic noisy tumor-volume and biomarker time
courses under a calibrated QSP model. A fraction of the population has
intrinsic / acquired resistance, an observation-noise process is layered on
top of the latent dynamics, and CD8+ density picks up rougher per-patient
fluctuations. No project-specific data required.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from qsp_inference.inference.posterior_predictive import plot_posterior_predictive_spaghetti

OUT = Path(__file__).resolve().parent.parent / "assets" / "images" / "qsp-inference-trajectory-ppc.png"

rng = np.random.default_rng(42)
n_samples = 200
time = np.linspace(0, 180, 90)  # days
t_treat = 30


def tumor_traj(rng):
    r = rng.lognormal(np.log(0.04), 0.30)
    K = rng.lognormal(np.log(120), 0.35)
    V0 = rng.lognormal(np.log(8.0), 0.30)

    # Three response regimes: deep response, partial, primary refractory.
    regime = rng.choice(["deep", "partial", "refractory"], p=[0.45, 0.40, 0.15])
    if regime == "deep":
        eff = rng.lognormal(np.log(0.10), 0.30)
        recur_t = rng.lognormal(np.log(140), 0.25)  # late acquired resistance
        recur_strength = rng.lognormal(np.log(0.5), 0.4)
    elif regime == "partial":
        eff = rng.lognormal(np.log(0.04), 0.35)
        recur_t = rng.lognormal(np.log(80), 0.30)
        recur_strength = rng.lognormal(np.log(0.7), 0.4)
    else:  # refractory — keeps growing through treatment
        eff = rng.lognormal(np.log(0.005), 0.5)
        recur_t = 1e9
        recur_strength = 0.0

    V = np.empty_like(time)
    V[0] = V0
    # Coloured-noise process: AR(1) on log-V drives observation/biological wobble
    eps = 0.0
    for i in range(1, len(time)):
        dt = time[i] - time[i - 1]
        kill = eff if time[i] >= t_treat else 0.0
        # Resistance kicks in around recur_t — gradual loss of treatment effect
        kill *= 1.0 / (1.0 + np.exp((time[i] - recur_t) / 8.0)) ** recur_strength
        growth = r * V[i - 1] * (1 - V[i - 1] / K)
        # Smooth biological wobble — high AR coefficient, tiny innovation
        eps = 0.97 * eps + rng.normal(0, 0.015)
        V[i] = max(V[i - 1] + (growth - kill * V[i - 1]) * dt, 1e-3) * np.exp(eps)
    return V


def cd8_traj(rng):
    base = rng.lognormal(np.log(40.0), 0.40)
    expand = rng.lognormal(np.log(3.0), 0.50)
    tau_up = rng.lognormal(np.log(15.0), 0.30)
    tau_decay = rng.lognormal(np.log(70.0), 0.30)
    contract_at = rng.lognormal(np.log(60.0), 0.25)  # exhaustion onset

    after_treat = np.maximum(0, time - t_treat)
    # Up-rise then exhaustion-driven decay
    rise = expand * (1 - np.exp(-after_treat / tau_up))
    decay = np.exp(-np.maximum(0, time - (t_treat + contract_at)) / tau_decay)
    latent = base * (1 + rise * decay)
    # Slowly-drifting biological variation in log-space
    eps = 0.0
    out = np.empty_like(time)
    for i in range(len(time)):
        eps = 0.96 * eps + rng.normal(0, 0.04)
        out[i] = latent[i] * np.exp(eps)
    return out


tumor = np.stack([tumor_traj(rng) for _ in range(n_samples)])
cd8 = np.stack([cd8_traj(rng) for _ in range(n_samples)])

pp_sim_results = {
    "time": time,
    "simulations": {
        "Tumor volume (cm³)": tumor,
        "CD8+ T cells (cells/mm²)": cd8,
    },
    "species_names": ["Tumor volume (cm³)", "CD8+ T cells (cells/mm²)"],
}

fig, _ = plot_posterior_predictive_spaghetti(
    pp_sim_results,
    figsize=(11, 4),
    max_cols=2,
    alpha=0.08,
    credible_level=0.9,
    show=False,
)

# Drop the auto-suptitle for the website figure.
fig.suptitle("")

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=140, bbox_inches="tight")
plt.close(fig)
print(f"wrote {OUT}")
