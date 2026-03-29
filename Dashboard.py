# ============================================================
# FitCom Dashboard (Final Enhanced with Score Trend)
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sidebar import render_sidebar
from storage import load_reports
from utils import calculate_health_score

st.set_page_config(layout="wide")
render_sidebar()

# ============================================================
# LOGIN
# ============================================================

user = st.session_state.get("user")

if not user:
    from login import login
    login()
    st.stop()

st.title("🏠 My Fitness Dashboard")
st.markdown("---")

# ============================================================
# LOAD DATA
# ============================================================

data = load_reports()

records = []
for _, entries in data.items():
    for r in entries:
        if not r.get("IsDeleted", False):
            records.append(r)

if not records:
    st.info("No records found")
    st.stop()

df = pd.DataFrame(records)

# Safe date handling
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.sort_values("Date")

latest = df.iloc[-1]

# ============================================================
# HEALTH SCORE (FIX + FALLBACK)
# ============================================================

health_score = latest.get("HealthScore")

if not health_score or health_score == 0:
    health_score, health_status = calculate_health_score(latest)
else:
    health_status = latest.get("HealthStatus", "")

# ============================================================
# METRICS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Weight", latest.get("Weight", 0))
col2.metric("BMI", latest.get("BMI", 0))
col3.metric("Body Fat", latest.get("BodyFat", 0))
col4.metric("Muscle", latest.get("MuscleMass", 0))
col5.metric("Health Score", health_score)

st.write(f"Status: {health_status}")

# ============================================================
# PHOTO
# ============================================================

st.subheader("📸 Latest Photo")

if latest.get("Photo"):
    st.image(latest["Photo"], width=250)
else:
    st.info("No photo uploaded")

# ============================================================
# HIIT
# ============================================================

st.subheader("🔥 HIIT Session")

hiit = latest.get("HIIT", {})

if hiit:
    st.write(f"📅 Date: {hiit.get('Date')}")
    st.write(f"🔢 Session: {hiit.get('SessionNo')}")
    st.write(f"⏱ Duration: {hiit.get('Duration')} mins")

    st.markdown("### Performance")
    st.write(f"🏃 Running: {hiit.get('RunningDistance', 0)} km")
    st.write(f"🚜 Push: {hiit.get('SledgePush', 0)} kg")
    st.write(f"🚜 Pull: {hiit.get('SledgePull', 0)} kg")
    st.write(f"🏋️ Lunge: {hiit.get('LungeWalk', 0)} kg")
    st.write(f"🧳 Carry: {hiit.get('FarmersCarry', 0)} kg")
    st.write(f"📦 Box: {hiit.get('BoxJump', 0)}")
    st.write(f"🏐 Wall Ball: {hiit.get('WallBall', 0)}")
else:
    st.info("No HIIT data")

# ============================================================
# TRENDS
# ============================================================

st.markdown("---")
st.subheader("📈 Trends")

col1, col2 = st.columns(2)

# Weight Trend
with col1:
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Weight"], marker='o')
    ax.set_title("Weight Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# BMI Trend
with col2:
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["BMI"], marker='o')
    ax.set_title("BMI Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ============================================================
# 🔥 HEALTH SCORE TREND (NEW)
# ============================================================

st.markdown("---")
st.subheader("📈 Health Score Trend")

scores = []

for _, row in df.iterrows():
    score = row.get("HealthScore")

    # fallback for old records
    if not score or score == 0:
        score, _ = calculate_health_score(row)

    scores.append(score)

df["ComputedHealthScore"] = scores

fig, ax = plt.subplots()
ax.plot(df["Date"], df["ComputedHealthScore"], marker='o')
ax.set_title("Health Score Progress")
ax.set_ylabel("Score")
plt.xticks(rotation=45)

st.pyplot(fig)

# ============================================================
# TABLE
# ============================================================

st.markdown("---")
st.subheader("📋 Records")

st.dataframe(df, use_container_width=True)