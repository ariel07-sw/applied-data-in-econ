## Audit 02: Deconstructing Statistical Lies.

> Goal: Visualize how statistical narratives break under **power-law** (Pareto) markets — especially when analysts only study “survivors”.

This audit highlights three recurring distortions in real-world data work:

- **Latency Skew** (time window / exposure differences)
- **False Positives** (tail events mistaken for skill)
- **Survivorship Bias** (filtering failures creates fake “average success”)

---

### 1) Core Simulation (10,000 token launches)

We simulate **10,000** token launches with a **Pareto (power-law)** distribution:

- **99%** of tokens are near zero (the “graveyard”)
- **1%** are heavy-tailed “winners” (the “survivors”)

We create:

- `df_all`: all tokens (The Graveyard)
- `df_survivors`: top 1% by `peak_market_cap`

---

### 2) Python Code (Numpy + Matplotlib, dual histograms + mean comparison)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Parameters (teacher-aligned)
# ----------------------------
N = 10_000
TOP_PCT = 0.01
SEED = 42

rng = np.random.default_rng(SEED)

# ---------------------------------------------
# Step 1: Simulate Peak Market Cap (Power Law)
# 99% near zero, 1% heavy-tailed Pareto winners
# ---------------------------------------------
is_winner = rng.random(N) < TOP_PCT  # ~1% winners

peak_market_cap = np.zeros(N, dtype=float)

# 99% "near zero": small random noise (close to 0)
# (You can tweak the scale if you want "even closer to zero".)
peak_market_cap[~is_winner] = rng.uniform(0, 50_000, size=(~is_winner).sum())

# 1% winners: Pareto (power-law) + scale
alpha = 1.5            # tail heaviness (lower = fatter tail)
scale = 1_000_000       # scaling to make $-level market caps visible
peak_market_cap[is_winner] = (rng.pareto(alpha, size=is_winner.sum()) + 1) * scale

# ----------------------------
# Step 2: Build DataFrames
# ----------------------------
df_all = pd.DataFrame({"peak_market_cap": peak_market_cap})

# Define survivors as Top 1% cutoff
cutoff = df_all["peak_market_cap"].quantile(1 - TOP_PCT)
df_survivors = df_all[df_all["peak_market_cap"] >= cutoff].copy()

# ----------------------------
# Step 3: Print Bias Evidence
# ----------------------------
mean_all = df_all["peak_market_cap"].mean()
mean_survivors = df_survivors["peak_market_cap"].mean()
bias_factor = mean_survivors / mean_all if mean_all > 0 else np.nan

print("=== Survivorship Bias Check ===")
print(f"Total tokens (df_all): {len(df_all):,}")
print(f"Survivors (top 1%):    {len(df_survivors):,}")
print(f"Top 1% cutoff:         ${cutoff:,.2f}\n")

print(f"Mean Peak Market Cap (ALL):       ${mean_all:,.2f}")
print(f"Mean Peak Market Cap (SURVIVORS): ${mean_survivors:,.2f}\n")

print(f"Bias factor (Survivors / All): {bias_factor:.2f}")

# ---------------------------------------------------------
# Step 4: Dual Histograms (Linear + Log count recommended)
# ---------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# All tokens
axes[0].hist(df_all["peak_market_cap"], bins=80)
axes[0].set_title("The Graveyard (All Tokens) - Linear Scale")
axes[0].set_xlabel("Peak Market Cap ($)")
axes[0].set_ylabel("Count")

# Survivors
axes[1].hist(df_survivors["peak_market_cap"], bins=40)
axes[1].set_title("Survivors (Top 1%) - Linear Scale")
axes[1].set_xlabel("Peak Market Cap ($)")
axes[1].set_ylabel("Count")

plt.tight_layout()
plt.show()

# Optional: log-count view (recommended for power-law)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df_all["peak_market_cap"], bins=80, log=True)
axes[0].set_title("The Graveyard (All Tokens) - Log Count")
axes[0].set_xlabel("Peak Market Cap ($)")
axes[0].set_ylabel("Count (log)")

axes[1].hist(df_survivors["peak_market_cap"], bins=40, log=True)
axes[1].set_title("Survivors (Top 1%) - Log Count")
axes[1].set_xlabel("Peak Market Cap ($)")
axes[1].set_ylabel("Count (log)")

plt.tight_layout()
plt.show()
=== Survivorship Bias Check ===
Total tokens (df_all): 10,000
Survivors (top 1%):    100
Top 1% cutoff:         $9,134,108.54

Mean Peak Market Cap (ALL):       $1,936,723.29
Mean Peak Market Cap (SURVIVORS): $16,549,004.95

Bias factor (Survivors / All): 8.54
