
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle

st.set_page_config(page_title="Bitcoin Portfolio Explorer", layout="wide")

st.title("📊 Bitcoin Portfolio Liquidation Explorer")

@st.cache_data
def fetch_data():
    data = pickle.load(Data/project1.pkl)
    return data


df_raw = fetch_data()




st.subheader("Parameters")
c1, c2, c3, c4 = st.columns(4)
with c1:
    sel_ltv = st.selectbox("LTV:", [pct_label(v) for v in ltv_vals], index=0, key="ltv")
with c2:
    sel_mc  = st.selectbox("Margin Call:", [pct_label(v) for v in mc_vals], index=0, key="mc")
with c3:
    sel_lt  = st.selectbox("Liquidation:", [pct_label(v) for v in lt_vals], index=0, key="lt")
with c4:
    sel_yrs = st.selectbox("Years:", [str(v) for v in yr_vals], index=0, key="yrs")


c5, _ = st.columns([1,3])
with c5:
    sel_win = st.selectbox("Window (hours):", [str(v) for v in win_vals], index=0, key="win")


ltv = from_pct_text(sel_ltv); mc = from_pct_text(sel_mc); lt = from_pct_text(sel_lt)
win = int(sel_win); yrs = int(sel_yrs)


candidates = index_df[
    np.isclose(index_df["LTV"], ltv) &
    np.isclose(index_df["Margin_Call"], mc) &
    np.isclose(index_df["Liquidation_Threshold"], lt) &
    (index_df["Window"] == win) & (index_df["Years"] == yrs)
]
if candidates.empty:
    st.error("No portfolio for this parameter set.")
    st.stop()

key = candidates.iloc[0]["key"]
df_raw = scenario[key].copy()


all_liq = bool(df_raw.get("Liquidated", pd.Series([False]*len(df_raw))).all())
total_liq = int(df_raw.get("Liquidated", pd.Series([False]*len(df_raw))).sum())

# “Average Liquidation Counts”
avg_liq_rate = (total_liq / len(df_raw)) * 100 if len(df_raw) else 0.0

st.markdown(f"**All Liquidated:** {all_liq}")
st.markdown(f"**Total Liquidations:** {total_liq},  **Average Liquidation Counts:** {avg_liq_rate:.2f}%")


sample_n = min(15, len(df_raw))
sample_df = df_raw.sample(n=sample_n, random_state=42).sort_index()


for col in ["Entry_Date", "Maturity_Date", "Liquidation_Date"]:
    if col in sample_df.columns:
        sample_df[col] = pd.to_datetime(sample_df[col], errors="coerce").dt.strftime("%Y-%m-%d")


st.dataframe(sample_df, use_container_width=True)


