## Phase 4: AI Context Engineering (P.R.I.M.E. Framework)

To extend the econometric diagnostics workflow, I used the P.R.I.M.E. prompting framework (Persona, Role, Instructions, Meaning, Evaluation) to direct an LLM to generate Python code for White’s Lagrange Multiplier Test for heteroscedasticity.

### P.R.I.M.E. Prompt
P — Persona:
You are a senior econometrician and Python statistical programming expert. You specialize in regression diagnostics using statsmodels and in writing precise, executable Google Colab code.

R — Role:
Your role is to generate Python code that performs White’s Lagrange Multiplier Test for heteroscedasticity on an already fitted OLS regression model object named `model`.

I — Instructions:
Write clean Python code for Google Colab that:
1. Imports `het_white` from `statsmodels.stats.diagnostic`.
2. Uses the fitted OLS model object `model` that already exists in memory.
3. Extracts the residuals and exogenous regressors from the fitted model.
4. Runs White’s test for heteroscedasticity using `het_white(model.resid, model.model.exog)`.
5. Prints:
   - the LM statistic,
   - the LM test p-value,
   - the F-statistic,
   - the F-test p-value.
6. Prints a final interpretation sentence:
   - If p-value < 0.05, state that the null hypothesis of homoscedasticity is rejected.
   - Otherwise, state that the null hypothesis of homoscedasticity is not rejected.

M — Meaning:
The purpose of this test is to determine whether the residual variance of my OLS pricing model is constant. I am diagnosing whether heteroscedasticity is present in the model predicting `Procedure_Cost_USD`.

E — Evaluation:
The output must be directly executable in Colab, use the exact statsmodels function `statsmodels.stats.diagnostic.het_white`, and include both numerical results and a short formal interpretation in plain English.

### White Test Result
- LM Statistic: 186.4677
- LM Test p-value: 1.4380e-22
- F-Statistic: 5.4942
- F-Test p-value: 4.4790e-23

### Interpretation
Because the LM test p-value is far below 0.05, the null hypothesis of homoscedasticity is rejected. This provides strong evidence that the OLS model suffers from heteroscedasticity.
