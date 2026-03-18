# ============================================================
# FitCom - AI Coach (Final Refactored Version)
# Author: Anand Kumar
#
# Purpose:
# Provide intelligent health insights based on latest report
# ============================================================

import streamlit as st
import pandas as pd
import os

from sidebar import render_sidebar
from ui.theme import apply_theme
from ui.components import page_header, section, card_start, card_end

# -------------------------------------------------------
# INIT
# -------------------------------------------------------

render_sidebar()
apply_theme()

FILE_NAME = "fitcom_reports.csv"

page_header("AI Coach", "Personalized fitness insights")

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

if not os.path.exists(FILE_NAME):
    st.info("No reports available yet.")
    st.stop()

df = pd.read_csv(FILE_NAME)

# Ensure date format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -------------------------------------------------------
# USER SELECTION
# -------------------------------------------------------

section("Select Member")

card_start()

users = sorted(df["Name"].dropna().unique())

selected_user = st.selectbox("Choose Member", users)

card_end()

# -------------------------------------------------------
# GET LATEST RECORD
# -------------------------------------------------------

user_df = df[df["Name"] == selected_user].sort_values("Date")

if user_df.empty:
    st.warning("No data found for this member.")
    st.stop()

latest = user_df.iloc[-1]

# -------------------------------------------------------
# SHOW LATEST METRICS
# -------------------------------------------------------

section("Latest Metrics")

card_start()

display_df = pd.DataFrame([latest]).drop(columns=["Photo"], errors="ignore")

st.dataframe(display_df, use_container_width=True)

card_end()

# -------------------------------------------------------
# AI COACH LOGIC (PRESERVED)
# -------------------------------------------------------

def ai_coach(row):

    tips = []

    # BMI check
    if row["BMI"] > 25:
        tips.append("BMI is high. Focus on fat loss and calorie deficit.")

    # Body fat
    if row["BodyFat"] > 20:
        tips.append("Body fat is above optimal. Add cardio and monitor diet.")

    # Muscle mass
    if row["MuscleMass"] < 30:
        tips.append("Muscle mass is low. Include strength training.")

    # Hydration
    if row["BodyWater"] < 50:
        tips.append("Hydration is low. Increase water intake.")

    # Visceral fat
    if row["VisceralFat"] > 10:
        tips.append("Visceral fat is high. Reduce sugar and processed food.")

    # Protein
    if row["ProteinRate"] < 15:
        tips.append("Protein intake is low. Increase protein consumption.")

    return tips

tips = ai_coach(latest)

# -------------------------------------------------------
# RECOMMENDATIONS
# -------------------------------------------------------

section("AI Recommendations")

card_start()

if tips:
    for tip in tips:
        st.success(tip)
else:
    st.success("Great job! All parameters are within healthy range 💪")

card_end()

# -------------------------------------------------------
# QUICK SUMMARY INSIGHT (ADDED, NON-INTRUSIVE)
# -------------------------------------------------------

section("Quick Insight")

card_start()

if len(user_df) > 1:
    prev = user_df.iloc[-2]

    weight_change = latest["Weight"] - prev["Weight"]
    fat_change = latest["BodyFat"] - prev["BodyFat"]

    st.write(f"Weight Change: **{round(weight_change,2)} kg**")
    st.write(f"Body Fat Change: **{round(fat_change,2)} %**")

    if weight_change < 0:
        st.success("Positive trend in weight reduction 📉")
    else:
        st.info("Monitor weight trend")

else:
    st.info("Not enough data for trend insights")

card_end()