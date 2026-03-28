import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Startup Valuation Simulator", layout="wide")

st.title("🚀 Startup Valuation Under Uncertainty")
st.write("A Monte Carlo simulation tool for fintech startup valuation")

# -------------------------
# SIDEBAR INPUTS
# -------------------------
st.sidebar.header("📊 Input Assumptions")

# Market Inputs
TAM = st.sidebar.number_input("Total Addressable Market (₹ Cr)", value=10000)
growth_mean = st.sidebar.slider("Expected Growth Rate (%)", 0, 100, 20)
growth_std = st.sidebar.slider("Growth Uncertainty (σ)", 0, 50, 10)

market_share_mean = st.sidebar.slider("Expected Market Share (%)", 0, 50, 5)

# Economics
margin_low = st.sidebar.slider("Min Margin (%)", 0, 50, 10)
margin_high = st.sidebar.slider("Max Margin (%)", 10, 80, 30)

multiple = st.sidebar.slider("Valuation Multiple", 5, 30, 15)

# Risk
prob_success = st.sidebar.slider("Probability of Success (%)", 10, 100, 60)

# Simulation size
simulations = st.sidebar.slider("Number of Simulations", 100, 5000, 1000)

# Scenario shock
shock = st.sidebar.selectbox(
    "Scenario",
    ["Base Case", "Regulatory Shock", "Funding Winter"]
)

# -------------------------
# ADJUST FOR SCENARIOS
# -------------------------
if shock == "Regulatory Shock":
    prob_success *= 0.7
    margin_high *= 0.8

elif shock == "Funding Winter":
    multiple *= 0.7

# -------------------------
# MONTE CARLO SIMULATION
# -------------------------
valuations = []

for _ in range(simulations):
    growth = np.random.normal(growth_mean/100, growth_std/100)
    market_share = np.random.beta(2, 5) * (market_share_mean/100)
    margin = np.random.uniform(margin_low/100, margin_high/100)

    revenue = TAM * market_share * (1 + growth)
    profit = revenue * margin

    val = profit * multiple

    # Apply probability of success
    val = val * (prob_success/100)

    valuations.append(val)

valuations = np.array(valuations)

# -------------------------
# OUTPUT METRICS
# -------------------------
st.subheader("📈 Valuation Distribution")

col1, col2, col3 = st.columns(3)

col1.metric("Median Valuation (₹ Cr)", f"{np.median(valuations):,.0f}")
col2.metric("Downside (5th %ile)", f"{np.percentile(valuations,5):,.0f}")
col3.metric("Upside (95th %ile)", f"{np.percentile(valuations,95):,.0f}")

# -------------------------
# PLOT
# -------------------------
fig, ax = plt.subplots()
ax.hist(valuations, bins=50)
ax.set_title("Valuation Distribution")
ax.set_xlabel("Valuation (₹ Cr)")
ax.set_ylabel("Frequency")

st.pyplot(fig)

# -------------------------
# DECISION SECTION
# -------------------------
st.subheader("💰 Your Investment Decision")

user_investment = st.number_input("How much would you invest? (₹ Cr)", value=100)

expected_value = np.mean(valuations)

st.write(f"📊 Expected Valuation: ₹ {expected_value:,.0f} Cr")

# Comparison
if user_investment > expected_value:
    st.warning("⚠️ You are investing ABOVE expected value (possible optimism / narrative bias)")
else:
    st.success("✅ Your investment aligns with model valuation")

# -------------------------
# DATA TABLE (OPTIONAL)
# -------------------------
if st.checkbox("Show Raw Simulation Data"):
    df = pd.DataFrame(valuations, columns=["Valuation"])
    st.dataframe(df.head(100))
