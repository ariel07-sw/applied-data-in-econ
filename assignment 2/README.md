# Audit 02: Deconstructing Statistical Lies

## Overview

This audit investigates how data can mislead decision-makers when statistical distortions are not properly identified.  
Using simulation and controlled experiments, I deconstructed three common analytical traps:

- **Latency Skew**
- **False Positive Paradox**
- **Survivorship Bias**

The goal was not just to compute metrics — but to expose where intuition fails and quantitative reasoning must intervene.

---

## 1️⃣ Latency Skew — When Time Distorts Truth

### Problem  
Average performance metrics can be artificially inflated when slow observations are dropped or underrepresented.

### Mechanism  
In systems with high variance response times (e.g., platform latency, API response, or user engagement timing), the distribution is often right-skewed. If:

- Outliers are removed  
- Time windows are truncated  
- Only successful events are logged  

→ The **mean becomes misleadingly optimistic**.

### Key Finding  

- Standard Deviation (SD) exploded when extreme latency values were included.
- Median Absolute Deviation (MAD) remained stable.

This confirms:

> The mean reacts violently to outliers.  
> Robust statistics (median, MAD) preserve structural truth.

### Insight  

Latency Skew creates a false perception of performance stability.  
Robust measures must replace naive averages in operational dashboards.

---

## 2️⃣ False Positive Paradox — Accuracy Is Not Probability

### Scenario  
A detection model claims **98% accuracy**.  
However, the base rate of the event is extremely low (e.g., 0.1%).

### Bayesian Audit  

We computed:

P(Event | Flagged)

Across multiple base rate scenarios.

### Key Finding  

Even with:
- 98% Sensitivity
- 98% Specificity

When the base rate = 0.1%:

P(True Event | Positive Flag) << 50%

Most positive signals were false.

### Insight  

> High accuracy does NOT imply high predictive reliability.

Base rates dominate inference.  
Ignoring prior probabilities produces systemic overconfidence.

---

## 3️⃣ Survivorship Bias — The Graveyard Problem

### Simulation  
10,000 token launches generated via a Pareto (power law) distribution.

- 99% near zero market cap
- 1% extreme winners

Two datasets were constructed:

- `df_all` → Full population (The Graveyard)
- `df_survivors` → Top 1% only

### Key Finding  

| Dataset | Mean Market Cap |
|----------|----------------|
| All Tokens | Low |
| Survivors Only | Extremely High |

By observing only survivors, the average outcome appeared massively inflated.

### Insight  

> Observing winners only manufactures optimism.

This bias is common in:

- Crypto markets  
- Venture capital  
- Startup ecosystems  
- Artist success narratives  

True risk assessment requires full-distribution visibility.

---

## 🔬 Technical Tools Used

- `numpy` (Power Law simulations)
- `pandas` (Dataset segmentation)
- `matplotlib` (Comparative histograms)
- Bayesian probability modeling
- Robust dispersion metrics (MAD vs SD)

---

## 🎯 Strategic Conclusion

Across all three audits, a common pattern emerged:

| Bias | Root Cause | Illusion Created |
|------|------------|-----------------|
| Latency Skew | Outlier sensitivity | Stability illusion |
| False Positives | Base rate neglect | Predictive illusion |
| Survivorship Bias | Sample truncation | Success illusion |

Statistical lies are rarely intentional —  
they emerge from ignoring distributional structure.

The true skill in data science is not computing numbers.  
It is defending reality against seductive averages.
