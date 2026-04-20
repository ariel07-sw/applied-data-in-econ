## Causal ML — DML and Causal Forests for Policy Evaluation

### Objective
Estimate the causal effect of 401(k) eligibility on net financial assets using modern double machine learning methods, while contrasting average treatment effect estimation with heterogeneity-focused causal forest analysis for policy targeting.

### Methodology
- Diagnosed and corrected a broken manual 2-fold cross-fitting DML implementation by fixing three core issues:
  - data leakage from training and predicting on the same fold
  - missing residualization of the treatment variable
  - incorrect final estimating equation for the treatment effect
- Verified the corrected manual DML procedure on a simulated data-generating process with known truth, confirming recovery of the true ATE of 5.0
- Estimated the average treatment effect of 401(k) eligibility on net financial assets using the `DoubleML` framework
- Specified Random Forest nuisance learners for both the outcome and treatment models and used 5-fold cross-fitting to reduce overfitting bias
- Conducted sensitivity analysis to evaluate how robust the estimated ATE is to potential unobserved confounding
- Fit an `EconML` `CausalForestDML` model to recover individual-level conditional average treatment effects (CATEs)
- Compared quartile-based subgroup DML to causal-forest-based heterogeneity estimation in order to assess whether coarse subgrouping masks meaningful within-group variation

### Key Findings
- The corrected manual DML implementation successfully recovered the true simulated ATE, validating the logic of cross-fitting, dual residualization, and the IV-style final estimator.
- In the 401(k) application, DoubleML estimated a statistically significant positive effect of eligibility on net financial assets of approximately **$8,441**, with a **95% confidence interval of about [$7,613, $9,269]**.
- Sensitivity analysis indicated that the main ATE estimate is reasonably robust to moderate omitted-variable bias, with the treatment effect remaining positive under the specified confounding bounds.
- The causal forest revealed meaningful **individual-level treatment heterogeneity** that is not captured by quartile-level subgroup DML alone.
- Taken together, the results show that DML is well suited for credible policy-level ATE estimation, while causal forests provide a richer tool for identifying which households are likely to benefit more strongly from treatment.

### Interpretation
This lab demonstrates the complementarity between debiased causal effect estimation and flexible heterogeneity discovery. For policy evaluation, DML provides a transparent and defensible estimate of the average effect; for targeting and distributional analysis, causal forests uncover finer-grained treatment-effect variation that coarse subgroup methods can miss.
