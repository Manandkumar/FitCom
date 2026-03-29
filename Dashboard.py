# ============================================================
# FitCom - My Dashboard (SaaS Version)
# Author: Anand Kumar
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sidebar
from sidebar import render_sidebar

# Storage
from storage import load_reports

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FitCom Dashboard",
    layout="wide"
)

# ============================================================
# LOGIN CHECK
# ============================================================

user = st.session_state.get("user")

if not user:
    from login import login
    login()
    st.stop()

# ============================================================
# UI START
# ============================================================

render_sidebar()

st.title("🏠 My Fitness Dashboard")
st.caption("Track your fitness journey and progress")

st.markdown("---")

# ============================================================
# LOAD DATA
# ============================================================

data = load_reports()

if not data:
    st.info("No records found. Please add your first fitness record.")
    st.stop()

# Convert to dataframe
records = []

for _, entries in data.items():
    for r in entries:
        records.append(r)

df = pd.DataFrame(records)

# Sort by date
df = df.sort_values(by="Date")

# ============================================================
# LATEST METRICS
# ============================================================

latest = df.iloc[-1]

st.subheader("📊 Latest Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Weight (kg)", latest.get("Weight", 0))
col2.metric("BMI", latest.get("BMI", 0))
col3.metric("Body Fat (%)", latest.get("BodyFat", 0))
col4.metric("Muscle Mass", latest.get("MuscleMass", 0))

st.markdown("---")

# ============================================================
# TRENDS
# ============================================================

st.subheader("📈 Progress Trends")

col1, col2 = st.columns(2)

# Weight trend
with col1:
    st.markdown("### Weight Trend")

    if "Weight" in df.columns:
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["Weight"], marker='o')
        ax.set_xlabel("Date")
        ax.set_ylabel("Weight")
        ax.set_title("Weight Progress")
        plt.xticks(rotation=45)

        st.pyplot(fig)
    else:
        st.info("No weight data available")


# BMI trend
with col2:
    st.markdown("### BMI Trend")

    if "BMI" in df.columns:
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["BMI"], marker='o')
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.set_title("BMI Progress")
        plt.xticks(rotation=45)

        st.pyplot(fig)
    else:
        st.info("No BMI data available")

st.markdown("---")

# ============================================================
# INSIGHTS
# ============================================================

st.subheader("🧠 Insights")

weight = latest.get("Weight", 0)
bmi = latest.get("BMI", 0)
fat = latest.get("BodyFat", 0)

insights = []

if bmi > 25:
    insights.append("⚠️ BMI is above normal range")
else:
    insights.append("✅ BMI is within healthy range")

if fat > 25:
    insights.append("⚠️ Body fat is high")
else:
    insights.append("✅ Body fat is under control")

if len(df) > 1:
    if df.iloc[-1]["Weight"] > df.iloc[0]["Weight"]:
        insights.append("📈 Weight increasing trend")
    else:
        insights.append("📉 Weight decreasing trend")

for i in insights:
    st.write(i)

st.markdown("---")

# ============================================================
# DATA TABLE
# ============================================================

st.subheader("📋 My Records")

st.dataframe(df, use_container_width=True)