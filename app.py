
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bitcoin Portfolio Explorer", layout="wide")

st.title("📊 Bitcoin Portfolio Margin Call and Liquidation Explorer")

uploaded_file = st.sidebar.file_uploader("Upload scenario_dict.pkl", type="pkl")
use_demo = st.sidebar.checkbox("Use demo data", value=True)

if uploaded_file is not None:
    scenario_dict = pd.read_pickle(uploaded_file)
elif use_demo:
    import numpy as np
    # demo dict
    demo_df = pd.DataFrame({
        "Borrower": [f"B{i}" for i in range(10)],
        "Margin_Call_Count": np.random.randint(0, 5, 10),
        "Liquidated": np.random.choice([True, False], 10),
        "Time_to_Liquidation": np.random.randint(10, 100, 10)
    })
    scenario_dict = {"LTV_Initial=0.4, Margin_Call=0.7, Liquidation_Threshold=0.9, Window=48, Years=2": demo_df}
else:
    st.warning("Please upload a PKL file or use demo data.")
    st.stop()

# sidebar selectors
keys = list(scenario_dict.keys())
selected_key = st.sidebar.selectbox("Select Scenario", keys)
df = scenario_dict[selected_key]

st.subheader("Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Margin Calls", int(df['Margin_Call_Count'].sum()))
col2.metric("Total Liquidations", int(df['Liquidated'].sum()))
col3.metric("Avg. Time to Liquidation", f"{df['Time_to_Liquidation'].mean():.1f} h")

st.subheader("Sample Portfolio Data")
st.dataframe(df.head(20))

st.subheader("Distribution of Margin Calls")
fig, ax = plt.subplots()
df['Margin_Call_Count'].hist(ax=ax)
st.pyplot(fig)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "portfolio.csv", "text/csv")
