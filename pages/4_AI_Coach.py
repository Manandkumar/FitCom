# ============================================================
# FitCom - AI Coach (Personalized Insights)
# Author: Anand Kumar
# ============================================================

import streamlit as st
import pandas as pd

from sidebar import render_sidebar
from storage import load_reports, load_hiit_sessions


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(page_title="AI Coach", layout="wide")

render_sidebar()

st.title("🤖 AI Fitness Coach")

# ============================================================
# USER CHECK
# ============================================================

user = st.session_state.get("user")

if not user:
    st.error("Please login")
    st.stop()

# ============================================================
# LOAD DATA
# ============================================================

report_data = load_reports()
hiit_data = load_hiit_sessions(user)

# Flatten report data
records = []
for _, entries in report_data.items():
    for r in entries:
        records.append(r)

if not records:
    st.info("Add body records first")
    st.stop()

df_body = pd.DataFrame(records)
df_body = df_body.sort_values(by="Date")

latest = df_body.iloc[-1]

# ============================================================
# AI ANALYSIS
# ============================================================

st.subheader("🧠 Your Fitness Insights")

insights = []

# ------------------------------------------------------------
# BMI ANALYSIS
# ------------------------------------------------------------
bmi = latest.get("BMI", 0)

if bmi < 18.5:
    insights.append("⚠️ You are underweight. Consider a calorie surplus diet.")
elif bmi < 25:
    insights.append("✅ Your BMI is in a healthy range. Maintain consistency.")
else:
    insights.append("⚠️ BMI is high. Focus on fat loss and HIIT training.")

# ------------------------------------------------------------
# BODY FAT ANALYSIS
# ------------------------------------------------------------
fat = latest.get("BodyFat", 0)

if fat > 25:
    insights.append("⚠️ Body fat is high. Increase cardio and reduce sugar intake.")
else:
    insights.append("✅ Body fat is under control. Keep it up!")

# ------------------------------------------------------------
# WEIGHT TREND
# ------------------------------------------------------------
if len(df_body) > 1:
    if df_body.iloc[-1]["Weight"] > df_body.iloc[0]["Weight"]:
        insights.append("📈 Your weight is increasing over time.")
    else:
        insights.append("📉 Your weight is decreasing. Good progress!")

# ------------------------------------------------------------
# HIIT ANALYSIS
# ------------------------------------------------------------
if hiit_data:
    df_hiit = pd.DataFrame(hiit_data)

    avg_calories = df_hiit["Calories"].mean()
    workouts = len(df_hiit)

    if workouts < 3:
        insights.append("⚠️ Low workout frequency. Aim for 3–4 sessions per week.")
    else:
        insights.append("💪 Great workout consistency!")

    if avg_calories < 200:
        insights.append("🔥 Increase workout intensity to burn more calories.")
    else:
        insights.append("🔥 Good calorie burn. Keep pushing!")

else:
    insights.append("⚠️ No HIIT sessions logged. Start training to improve fitness.")

# ============================================================
# DISPLAY INSIGHTS
# ============================================================

for i in insights:
    st.write(i)

st.markdown("---")

# ============================================================
# ACTION PLAN
# ============================================================

st.subheader("📋 Recommended Action Plan")

actions = []

if bmi > 25:
    actions.append("🏃 Do HIIT workouts 4x per week")
    actions.append("🥗 Maintain calorie deficit diet")

if fat > 25:
    actions.append("🚫 Reduce sugar & processed food")
    actions.append("🥦 Increase protein intake")

if hiit_data:
    actions.append("📅 Maintain workout consistency")

actions.append("💧 Drink at least 3L water daily")
actions.append("😴 Sleep 7-8 hours")

for a in actions:
    st.write(a)

st.markdown("---")

# ============================================================
# MOTIVATION
# ============================================================

st.subheader("🔥 Motivation")

st.success("Consistency beats intensity. Keep showing up every day 💪")