# ============================================================
# FitCom - AI Health Coach
# Author: Anand Kumar
#
# Notes:
# - Provides rule-based fitness insights (AI-style guidance)
# - Uses latest user data
# - Age is hidden from UI for privacy
# ============================================================

import streamlit as st
import pandas as pd
import os

# -------------------------------------------------------
# Load shared sidebar (consistent UI across app)
# -------------------------------------------------------

from sidebar import render_sidebar
render_sidebar()

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------

FILE_NAME = "fitcom_reports.csv"

st.title("🤖 AI Health Coach")

# -------------------------------------------------------
# AI LOGIC (RULE-BASED FOR NOW)
# -------------------------------------------------------
# This can later be replaced with real AI/LLM logic

def ai_coach(row):

    tips = []

    # BMI check
    if "BMI" in row and row["BMI"] > 25:
        tips.append("⚠️ BMI is slightly high. Focus on fat reduction.")

    # Body fat check
    if "BodyFat" in row and row["BodyFat"] > 20:
        tips.append("🔥 Body fat is above optimal. Add cardio sessions.")

    # Muscle check
    if "MuscleMass" in row and row["MuscleMass"] < 30:
        tips.append("💪 Muscle mass is low. Increase strength training.")

    # Water check
    if "BodyWater" in row and row["BodyWater"] < 50:
        tips.append("💧 Hydration is low. Increase water intake.")

    # Default fallback
    if not tips:
        tips.append("✅ Your body composition looks good. Keep it up!")

    return tips

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

if not os.path.exists(FILE_NAME):

    st.info("No reports available.")
    st.stop()

df = pd.read_csv(FILE_NAME)

# Convert Date for sorting
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -------------------------------------------------------
# USER SELECTION
# -------------------------------------------------------

users = sorted(df["Name"].unique())

user = st.selectbox("Select User", users)

# Get latest record for selected user
user_df = df[df["Name"] == user].sort_values("Date")

if user_df.empty:
    st.info("No data available for selected user.")
    st.stop()

latest = user_df.iloc[-1]

# -------------------------------------------------------
# DISPLAY USER DATA (Age hidden)
# -------------------------------------------------------

st.subheader("📊 Latest Metrics")

latest_display = latest.drop(labels=["Age"], errors="ignore")

st.dataframe(pd.DataFrame([latest_display]), use_container_width=True)

# -------------------------------------------------------
# AI INSIGHTS
# -------------------------------------------------------

st.subheader("🧠 AI Recommendations")

tips = ai_coach(latest)

for tip in tips:
    st.success(tip)