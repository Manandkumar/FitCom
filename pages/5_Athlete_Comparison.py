# ============================================================
# FitCom - Leaderboard
# Author: Anand Kumar
# ============================================================

import streamlit as st
import pandas as pd

from sidebar import render_sidebar
from storage import load_all_reports


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(page_title="Leaderboard", layout="wide")

render_sidebar()

st.title("🏆 Leaderboard")
st.caption("Compare fitness metrics across all users")

st.markdown("---")


# ============================================================
# LOAD DATA
# ============================================================

data = load_all_reports()

if not data:
    st.info("No data available")
    st.stop()

df = pd.DataFrame(data)

# Ensure sorting by Date
df = df.sort_values(by="Date")

# Get latest record per user
latest_df = df.groupby("UserId").tail(1)


# ============================================================
# TOP PERFORMERS
# ============================================================

st.subheader("🥇 Top Performers")

col1, col2, col3 = st.columns(3)

# Lowest Body Fat
if "BodyFat" in latest_df.columns:
    best_fat = latest_df.sort_values(by="BodyFat").head(5)
    col1.markdown("### 🔥 Lowest Body Fat")
    col1.dataframe(best_fat[["UserId", "BodyFat"]], use_container_width=True)

# Highest Muscle Mass
if "MuscleMass" in latest_df.columns:
    best_muscle = latest_df.sort_values(by="MuscleMass", ascending=False).head(5)
    col2.markdown("### 💪 Highest Muscle")
    col2.dataframe(best_muscle[["UserId", "MuscleMass"]], use_container_width=True)

# Best BMI (closest to 22)
if "BMI" in latest_df.columns:
    latest_df["BMI_diff"] = (latest_df["BMI"] - 22).abs()
    best_bmi = latest_df.sort_values(by="BMI_diff").head(5)
    col3.markdown("### ⚖️ Best BMI")
    col3.dataframe(best_bmi[["UserId", "BMI"]], use_container_width=True)

st.markdown("---")


# ============================================================
# FULL TABLE
# ============================================================

st.subheader("📋 All Users")

st.dataframe(latest_df, use_container_width=True)