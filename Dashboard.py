# ============================================================
# FitCom Dashboard (FINAL - SaaS Ready & Stable)
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- SAFE IMPORTS ----------------
try:
    from sidebar import render_sidebar
    from storage import load_reports, load_hiit_sessions
    from utils import calculate_health_score
except Exception as e:
    st.error(f"Import error: {e}")
    st.stop()

from login import login

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- AUTH CHECK ----------------
st.write("Session:", st.session_state)  # Debug (remove later)

user = st.session_state.get("user")

if not user:
    login()
    st.stop()

# ---------------- SIDEBAR ----------------
render_sidebar()

# ---------------- TITLE ----------------
st.title("🏠 My Fitness Dashboard")

# ============================================================
# 📊 LOAD DATA
# ============================================================

try:
    data = load_reports()
except Exception as e:
    st.error(f"Error loading reports: {e}")
    st.stop()

records = []

for _, entries in data.items():
    for r in entries:
        # ✅ SaaS filter (IMPORTANT)
        if not r.get("IsDeleted") and r.get("UserId") == user:
            records.append(r)

if not records:
    st.info("No records found for your account.")
    st.stop()

# ---------------- DATAFRAME ----------------
df = pd.DataFrame(records)

# Safety checks
required_cols = ["Date", "Weight", "BMI", "BodyFat", "MuscleMass"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing column: {col}")
        st.stop()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])
df = df.sort_values("Date")

latest = df.iloc[-1]

# ============================================================
# 💪 HEALTH SCORE
# ============================================================

score = latest.get("HealthScore")

if not score or score == 0:
    score, status = calculate_health_score(latest)
else:
    status = latest.get("HealthStatus", "No status")

# ============================================================
# 📊 METRICS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Weight", latest.get("Weight", "-"))
col2.metric("BMI", latest.get("BMI", "-"))
col3.metric("Body Fat", latest.get("BodyFat", "-"))
col4.metric("Muscle", latest.get("MuscleMass", "-"))
col5.metric("Health Score", score)

st.write(f"**Status:** {status}")

# ============================================================
# 📸 PHOTO
# ============================================================

st.subheader("📸 Latest Photo")

if latest.get("Photo"):
    st.image(latest["Photo"], width=250)
else:
    st.info("No photo available")

# ============================================================
# 🔥 HIIT SESSIONS
# ============================================================

st.subheader("🔥 HIIT Sessions")

try:
    sessions = load_hiit_sessions(user)
except Exception as e:
    st.error(f"Error loading HIIT sessions: {e}")
    sessions = []

if sessions:
    last = sessions[-1]

    st.write(f"**Date:** {last.get('Date', '-')}")
    st.write(f"**Workout:** {last.get('Workout', '-')}")
    st.write(f"**Duration:** {last.get('Duration', '-')} mins")
else:
    st.info("No HIIT sessions found")

# ============================================================
# 📈 TRENDS
# ============================================================

st.subheader("📈 Fitness Trends")

def plot_chart(x, y, title):
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')
    ax.set_title(title)
    ax.grid(True)
    st.pyplot(fig)

# Weight
plot_chart(df["Date"], df["Weight"], "Weight Trend")

# BMI
plot_chart(df["Date"], df["BMI"], "BMI Trend")

# ============================================================
# 💯 HEALTH SCORE TREND
# ============================================================

scores = []

for _, row in df.iterrows():
    s = row.get("HealthScore")
    if not s or s == 0:
        s, _ = calculate_health_score(row)
    scores.append(s)

df["Score"] = scores

plot_chart(df["Date"], df["Score"], "Health Score Trend")

# ============================================================
# 📋 DATA TABLE
# ============================================================

st.subheader("📋 Full Data")

st.dataframe(df, use_container_width=True)