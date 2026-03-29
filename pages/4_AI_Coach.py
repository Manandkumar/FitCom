# ============================================================
# FitCom - HIIT Analytics Dashboard
# Author: Anand Kumar
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sidebar import render_sidebar
from storage import load_hiit_sessions


st.set_page_config(page_title="HIIT Analytics", layout="wide")

render_sidebar()

st.title("🏋️ HIIT Performance Dashboard")

user = st.session_state.get("user")

if not user:
    st.error("Please login")
    st.stop()

# ============================================================
# LOAD DATA
# ============================================================

sessions = load_hiit_sessions(user)

if not sessions:
    st.info("No HIIT sessions yet")
    st.stop()

df = pd.DataFrame(sessions)
df = df.sort_values(by="Date")

# ============================================================
# METRICS
# ============================================================

st.subheader("📊 Performance Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Workouts", len(df))
col2.metric("Avg Calories", int(df["Calories"].mean()))
col3.metric("Avg Heart Rate", int(df["HeartRate"].mean()))

st.markdown("---")

# ============================================================
# TRENDS
# ============================================================

st.subheader("📈 Trends")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Calories"], marker='o')
    ax.set_title("Calories Burn Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Duration"], marker='o')
    ax.set_title("Workout Duration Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.markdown("---")

# ============================================================
# FITNESS SCORE
# ============================================================

st.subheader("🔥 Fitness Score")

score = 0

score += min(len(df) * 5, 50)
score += min(df["Calories"].mean() / 10, 25)
score += min(df["Duration"].mean() / 2, 25)

score = int(score)

st.metric("Your Fitness Score", score)

if score > 80:
    st.success("Excellent fitness level 🔥")
elif score > 60:
    st.info("Good progress 💪")
else:
    st.warning("Needs improvement 🚀")

st.markdown("---")

# ============================================================
# DATA TABLE
# ============================================================

st.subheader("📋 HIIT Sessions")

st.dataframe(df, use_container_width=True)