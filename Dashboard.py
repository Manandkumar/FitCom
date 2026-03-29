# ============================================================
# FitCom - My Dashboard (Final Enhanced)
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sidebar import render_sidebar
from storage import load_reports

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(page_title="FitCom Dashboard", layout="wide")

# ============================================================
# LOGIN CHECK
# ============================================================

user = st.session_state.get("user")

if not user:
    from login import login
    login()
    st.stop()

# ============================================================
# UI
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

records = []

for _, entries in data.items():
    for r in entries:
        if not r.get("IsDeleted", False):  # ✅ FIX
            records.append(r)

if not records:
    st.info("No active records found.")
    st.stop()

df = pd.DataFrame(records)

# ✅ Fix date sorting properly
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.sort_values(by="Date")

latest = df.iloc[-1]

# ============================================================
# METRICS
# ============================================================

st.subheader("📊 Latest Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Weight (kg)", latest.get("Weight", 0))
col2.metric("BMI", latest.get("BMI", 0))
col3.metric("Body Fat (%)", latest.get("BodyFat", 0))
col4.metric("Muscle Mass", latest.get("MuscleMass", 0))
col5.metric("Health Score", latest.get("HealthScore", 0))

# ============================================================
# HIIT SECTION
# ============================================================

st.markdown("---")
st.subheader("🔥 Latest HIIT Session")

hiit = latest.get("HIIT", {})

if hiit:
    col1, col2, col3 = st.columns(3)

    col1.write(f"📅 Date: {hiit.get('Date')}")
    col2.write(f"🔢 Session: {hiit.get('SessionNo')}")
    col3.write(f"⏱ Duration: {hiit.get('Duration')} mins")

    st.markdown("### Performance")

    st.write(f"🏃 Running: {hiit.get('RunningDistance', 0)} km")
    st.write(f"🚜 Sledge Push: {hiit.get('SledgePush', 0)} kg")
    st.write(f"🚜 Sledge Pull: {hiit.get('SledgePull', 0)} kg")
    st.write(f"🏋️ Lunge Walk: {hiit.get('LungeWalk', 0)} kg")
    st.write(f"🧳 Farmers Carry: {hiit.get('FarmersCarry', 0)} kg")
    st.write(f"📦 Box Jumps: {hiit.get('BoxJump', 0)}")
    st.write(f"🏐 Wall Balls: {hiit.get('WallBall', 0)}")

else:
    st.info("No HIIT session recorded")

# ============================================================
# TRENDS
# ============================================================

st.markdown("---")
st.subheader("📈 Progress Trends")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Weight Trend")

    if "Weight" in df.columns:
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["Weight"], marker='o')
        ax.set_xlabel("Date")
        ax.set_ylabel("Weight")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("No weight data available")

with col2:
    st.markdown("### BMI Trend")

    if "BMI" in df.columns:
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["BMI"], marker='o')
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("No BMI data available")

# ============================================================
# INSIGHTS
# ============================================================

st.markdown("---")
st.subheader("🧠 Insights")

insights = []

bmi = latest.get("BMI", 0)
fat = latest.get("BodyFat", 0)
score = latest.get("HealthScore", 0)

if bmi > 25:
    insights.append("⚠️ BMI is above normal range")
else:
    insights.append("✅ BMI is within healthy range")

if fat > 25:
    insights.append("⚠️ Body fat is high")
else:
    insights.append("✅ Body fat is under control")

if score >= 75:
    insights.append("🔥 Excellent fitness level")
elif score >= 50:
    insights.append("👍 Moderate fitness level")
else:
    insights.append("⚠️ Needs improvement")

if len(df) > 1:
    if df.iloc[-1]["Weight"] > df.iloc[0]["Weight"]:
        insights.append("📈 Weight increasing trend")
    else:
        insights.append("📉 Weight decreasing trend")

for i in insights:
    st.write(i)

# ============================================================
# TABLE
# ============================================================

st.markdown("---")
st.subheader("📋 My Records")

st.dataframe(df, use_container_width=True)