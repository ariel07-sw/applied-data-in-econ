import streamlit as st
import plotly.graph_objects as go

baseline_ate = 1548.2438
baseline_se = 781.279

st.set_page_config(page_title="Job Training Dashboard", layout="wide")
st.title("ECON 5200: Job Training Effect Dashboard")

st.write("Interactive what-if dashboard for the estimated effect of job training on post-program earnings.")

multiplier = st.sidebar.slider(
    "Treatment intensity multiplier",
    min_value=0.5,
    max_value=3.0,
    value=1.0,
    step=0.1
)

effect = baseline_ate * multiplier
se = baseline_se * multiplier
ci_low = effect - 1.96 * se
ci_high = effect + 1.96 * se

c1, c2, c3 = st.columns(3)
c1.metric("Estimated Effect", f"{effect:.2f}")
c2.metric("95% CI Lower", f"{ci_low:.2f}")
c3.metric("95% CI Upper", f"{ci_high:.2f}")

st.markdown(
    f"If treatment intensity changes to **{multiplier:.1f}x**, the estimated effect becomes **{effect:.2f}** "
    f"with a 95% confidence interval of **[{ci_low:.2f}, {ci_high:.2f}]**."
)

xs = [x / 10 for x in range(5, 31)]
ys = [baseline_ate * x for x in xs]
lows = [y - 1.96 * baseline_se * x for x, y in zip(xs, ys)]
highs = [y + 1.96 * baseline_se * x for x, y in zip(xs, ys)]

fig = go.Figure()
fig.add_trace(go.Scatter(x=xs, y=highs, mode="lines", line=dict(width=0), showlegend=False))
fig.add_trace(go.Scatter(x=xs, y=lows, mode="lines", fill="tonexty", line=dict(width=0), name="95% CI"))
fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="Estimated Effect"))
fig.add_vline(x=multiplier, line_dash="dash")

fig.update_layout(
    title="What-If: Effect vs. Treatment Intensity",
    xaxis_title="Treatment Intensity Multiplier",
    yaxis_title="Estimated Effect on Earnings"
)

st.plotly_chart(fig, use_container_width=True)

double_effect = baseline_ate * 2
double_low = double_effect - 1.96 * baseline_se * 2
double_high = double_effect + 1.96 * baseline_se * 2

st.subheader("Counterfactual Scenario")
st.write(
    f"If treatment intensity doubled, the estimated effect would be **{double_effect:.2f}** "
    f"(95% CI: [{double_low:.2f}, {double_high:.2f}])."
)
